from flask import Flask, render_template, request, jsonify
from config import AVAILABLE_MODELS, COMPARISON_CATEGORIES
from core import ModelComparator

app = Flask(__name__)
comparator = ModelComparator(AVAILABLE_MODELS)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/models")
def get_models():
    return jsonify(comparator.get_available_models())


@app.route("/api/categories")
def get_categories():
    return jsonify(COMPARISON_CATEGORIES)


@app.route("/api/compare", methods=["POST"])
def compare():
    data = request.get_json()
    if not data:
        return jsonify({"error": "请求体不能为空"}), 400

    prompt = data.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "请输入提示词"}), 400

    category = data.get("category", "custom")
    model_keys = data.get("models")
    system_prompt = data.get("system_prompt", "")

    result = comparator.compare(
        prompt=prompt,
        category=category,
        model_keys=model_keys,
        system_prompt=system_prompt,
    )

    return jsonify(result.to_dict())


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)