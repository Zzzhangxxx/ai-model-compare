import time
from openai import OpenAI
from .models import ModelResponse, ComparisonResult


class ModelComparator:
    def __init__(self, model_configs: dict):
        self.model_configs = model_configs
        self.clients = {}
        for key, config in model_configs.items():
            if config["api_key"]:
                self.clients[key] = OpenAI(
                    api_key=config["api_key"],
                    base_url=config["base_url"],
                )

    def get_available_models(self) -> list[dict]:
        return [
            {
                "key": key,
                "name": cfg["name"],
                "provider": cfg["provider"],
                "description": cfg["description"],
                "available": key in self.clients,
            }
            for key, cfg in self.model_configs.items()
        ]

    def query_model(self, model_key: str, prompt: str, system_prompt: str = "") -> ModelResponse:
        config = self.model_configs[model_key]
        if model_key not in self.clients:
            return ModelResponse(
                model_name=config["name"],
                provider=config["provider"],
                content="",
                latency_ms=0,
                error="API Key 未配置",
                success=False,
            )

        client = self.clients[model_key]
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        start_time = time.time()
        try:
            response = client.chat.completions.create(
                model=config["model_id"],
                messages=messages,
                max_tokens=2048,
                temperature=0.7,
            )
            latency_ms = (time.time() - start_time) * 1000
            content = response.choices[0].message.content or ""
            token_count = response.usage.total_tokens if response.usage else 0

            return ModelResponse(
                model_name=config["name"],
                provider=config["provider"],
                content=content,
                latency_ms=round(latency_ms, 2),
                token_count=token_count,
                success=True,
            )
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            return ModelResponse(
                model_name=config["name"],
                provider=config["provider"],
                content="",
                latency_ms=round(latency_ms, 2),
                error=str(e),
                success=False,
            )

    def compare(self, prompt: str, category: str = "custom",
                model_keys: list[str] = None,
                system_prompt: str = "") -> ComparisonResult:
        if model_keys is None:
            model_keys = list(self.clients.keys())

        result = ComparisonResult(prompt=prompt, category=category)

        for key in model_keys:
            response = self.query_model(key, prompt, system_prompt)
            result.responses.append(response)

        best = None
        best_tokens = -1
        for r in result.responses:
            if r.success and r.token_count > best_tokens:
                best_tokens = r.token_count
                best = r.model_name
        result.winner = best

        return result