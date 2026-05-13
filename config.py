import os
from dotenv import load_dotenv

load_dotenv()

LONGCAT_API_KEY = os.getenv("LONGCAT_API_KEY", "")
LONGCAT_BASE_URL = os.getenv("LONGCAT_BASE_URL", "https://api.longcat.chat/openai/v1")

AVAILABLE_MODELS = {
    "longcat-flash": {
        "name": "LongCat Flash Lite",
        "model_id": "LongCat-Flash-Lite",
        "api_key": LONGCAT_API_KEY,
        "base_url": LONGCAT_BASE_URL,
        "provider": "LongCat",
        "description": "LongCat 快速轻量模型，响应迅速",
    },
    "longcat-thinking": {
        "name": "LongCat Flash Thinking",
        "model_id": "LongCat-Flash-Thinking-2601",
        "api_key": LONGCAT_API_KEY,
        "base_url": LONGCAT_BASE_URL,
        "provider": "LongCat",
        "description": "LongCat 深度思考模型，推理能力强",
    },
}

COMPARISON_CATEGORIES = [
    {
        "id": "code",
        "name": "代码生成",
        "prompts": [
            "用 Python 写一个快速排序算法，要求包含详细注释",
            "用 JavaScript 实现一个防抖函数 debounce",
            "写一个 SQL 查询，找出表中重复的记录",
        ],
    },
    {
        "id": "reasoning",
        "name": "逻辑推理",
        "prompts": [
            "一个房间里有3盏灯和3个开关，你只能进房间一次，如何确定哪个开关控制哪盏灯？",
            "如果所有的 A 都是 B，所有的 B 都是 C，那么所有的 A 都是 C。这个推理正确吗？",
        ],
    },
    {
        "id": "creative",
        "name": "创意写作",
        "prompts": [
            "写一首关于人工智能的七言绝句",
            "用 200 字写一个关于未来城市的微小说",
        ],
    },
    {
        "id": "translation",
        "name": "翻译能力",
        "prompts": [
            "将以下英文翻译成中文：The quick brown fox jumps over the lazy dog.",
            "将以下中文翻译成英文：人工智能正在深刻改变我们的生活方式。",
        ],
    },
]