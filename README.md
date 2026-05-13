# AI 模型对比评测平台 (AI Model Comparator)

一个基于 Web 的 AI 大模型对比评测工具，支持同时向多个 AI 模型发送相同的提示词，并排对比响应质量、响应速度和 Token 消耗。

## 项目背景

随着大语言模型（LLM）的快速发展，市面上涌现了大量优秀的 AI 模型，如 Xiaomi MiMo、OpenAI GPT-4o、DeepSeek-V3 等。开发者和用户在选择模型时，往往需要对比不同模型在相同任务上的表现。本项目旨在提供一个直观、高效的模型对比平台。

## 功能特性

- **多模型并行对比**：同时向 MiMo、GPT-4o、DeepSeek-V3 等多个模型发送相同提示词
- **预设评测场景**：内置代码生成、逻辑推理、创意写作、翻译等评测场景
- **实时性能指标**：展示每个模型的响应延迟（ms）和 Token 消耗量
- **自动评选最佳**：基于 Token 利用率自动标记表现最佳的模型
- **自定义系统提示词**：支持设定 AI 角色和行为约束
- **响应式设计**：适配桌面端和移动端

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | Python Flask |
| AI SDK | OpenAI Python SDK（兼容多厂商 API） |
| 前端 | 原生 HTML/CSS/JavaScript |
| 支持的模型 | MiMo V2.5、GPT-4o、DeepSeek-V3 |

## 项目结构

```
ai-model-compare/
├── app.py                  # Flask 主应用
├── config.py               # 模型配置与预设场景
├── requirements.txt        # Python 依赖
├── .env.example            # 环境变量模板
├── core/
│   ├── __init__.py
│   ├── models.py           # 数据模型定义
│   └── comparator.py       # 模型对比核心逻辑
├── static/
│   ├── css/
│   │   └── style.css       # 样式表
│   └── js/
│       └── main.js         # 前端交互逻辑
└── templates/
    └── index.html          # 主页面模板
```

## 快速开始

### 1. 环境准备

```bash
# Python 3.10+ 推荐
python --version

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 API Key

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的 API Key
# 至少配置一个模型的 API Key 即可运行
```

**获取 API Key：**
- MiMo API：访问 [Xiaomi MiMo API 开放平台](https://platform.xiaomimimo.com/) 注册获取
- OpenAI API：访问 [OpenAI Platform](https://platform.openai.com/) 获取
- DeepSeek API：访问 [DeepSeek Platform](https://platform.deepseek.com/) 获取

### 3. 启动应用

```bash
python app.py
```

访问 http://localhost:5000 即可使用。

## 使用说明

1. 在「可用模型」面板中选择要对比的模型（已配置 API Key 的模型会自动选中）
2. 选择预设评测场景，或输入自定义提示词
3. 可选：设置系统提示词来约束 AI 行为
4. 点击「开始对比」，等待所有模型返回结果
5. 在结果面板中并排查看各模型的响应内容、延迟和 Token 消耗

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/models` | 获取可用模型列表 |
| GET | `/api/categories` | 获取预设评测场景 |
| POST | `/api/compare` | 执行模型对比 |

### POST /api/compare 请求体

```json
{
    "prompt": "用 Python 写一个快速排序算法",
    "category": "code",
    "models": ["mimo", "gpt", "deepseek"],
    "system_prompt": "你是一个专业的 Python 开发者"
}
```

## 扩展指南

### 添加新模型

在 `config.py` 的 `AVAILABLE_MODELS` 字典中添加新模型配置：

```python
"claude": {
    "name": "Claude 3.5 Sonnet",
    "model_id": "claude-3-5-sonnet-20241022",
    "api_key": os.getenv("CLAUDE_API_KEY", ""),
    "base_url": "https://api.anthropic.com/v1",
    "provider": "Anthropic",
    "description": "Anthropic 旗舰模型",
},
```

### 添加新评测场景

在 `config.py` 的 `COMPARISON_CATEGORIES` 列表中添加：

```python
{
    "id": "math",
    "name": "数学能力",
    "prompts": [
        "解方程：x² - 5x + 6 = 0",
        "计算 ∫₀¹ x² dx",
    ],
},
```

## 许可证

MIT License