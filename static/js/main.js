let selectedModels = new Set();

document.addEventListener("DOMContentLoaded", () => {
    loadModels();
    loadCategories();
    setupEventListeners();
});

async function loadModels() {
    try {
        const res = await fetch("/api/models");
        const models = await res.json();
        renderModels(models);
    } catch (err) {
        document.getElementById("modelList").innerHTML =
            '<div class="loading" style="color:var(--error);">加载模型列表失败</div>';
    }
}

function renderModels(models) {
    const container = document.getElementById("modelList");
    container.innerHTML = models
        .map(
            (m) => `
        <div class="model-card ${m.available ? "" : "unavailable"}"
             data-key="${m.key}"
             onclick="${m.available ? `toggleModel('${m.key}')` : ""}">
            <span class="status-badge ${m.available ? "available" : "unavailable"}">
                ${m.available ? "可用" : "未配置"}
            </span>
            <div class="model-name">${m.name}</div>
            <div class="model-provider">${m.provider}</div>
            <div class="model-desc">${m.description}</div>
        </div>`
        )
        .join("");

    models.forEach((m) => {
        if (m.available) {
            selectedModels.add(m.key);
            const card = container.querySelector(`[data-key="${m.key}"]`);
            if (card) card.classList.add("selected");
        }
    });
}

function toggleModel(key) {
    const card = document.querySelector(`.model-card[data-key="${key}"]`);
    if (selectedModels.has(key)) {
        selectedModels.delete(key);
        card.classList.remove("selected");
    } else {
        selectedModels.add(key);
        card.classList.add("selected");
    }
}

async function loadCategories() {
    try {
        const res = await fetch("/api/categories");
        const categories = await res.json();
        const select = document.getElementById("category");
        categories.forEach((cat) => {
            const option = document.createElement("option");
            option.value = cat.id;
            option.textContent = cat.name;
            select.appendChild(option);
        });
    } catch (err) {
        console.error("加载分类失败:", err);
    }
}

function setupEventListeners() {
    const categorySelect = document.getElementById("category");
    const promptTextarea = document.getElementById("prompt");
    const compareBtn = document.getElementById("compareBtn");

    categorySelect.addEventListener("change", async () => {
        const categoryId = categorySelect.value;
        if (categoryId === "custom") {
            promptTextarea.value = "";
            promptTextarea.placeholder = "输入你想对比的提示词...";
            return;
        }

        try {
            const res = await fetch("/api/categories");
            const categories = await res.json();
            const cat = categories.find((c) => c.id === categoryId);
            if (cat && cat.prompts.length > 0) {
                promptTextarea.value = cat.prompts[0];
                promptTextarea.placeholder = cat.prompts.join(" | ");
            }
        } catch (err) {
            console.error("加载预设提示词失败:", err);
        }
    });

    compareBtn.addEventListener("click", runComparison);
}

async function runComparison() {
    const prompt = document.getElementById("prompt").value.trim();
    if (!prompt) {
        alert("请输入提示词");
        return;
    }

    if (selectedModels.size === 0) {
        alert("请至少选择一个可用模型");
        return;
    }

    const compareBtn = document.getElementById("compareBtn");
    const statusText = document.getElementById("statusText");
    const resultsPanel = document.getElementById("resultsPanel");
    const resultsContainer = document.getElementById("resultsContainer");

    compareBtn.disabled = true;
    statusText.innerHTML = '<span class="spinner"></span>正在对比中...';
    resultsPanel.style.display = "block";
    resultsContainer.innerHTML =
        '<div class="loading"><span class="spinner"></span>等待模型响应...</div>';

    try {
        const res = await fetch("/api/compare", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                prompt: prompt,
                category: document.getElementById("category").value,
                models: Array.from(selectedModels),
                system_prompt: document.getElementById("systemPrompt").value,
            }),
        });

        const data = await res.json();
        renderResults(data);
        statusText.textContent = "对比完成";
    } catch (err) {
        resultsContainer.innerHTML =
            '<div class="loading" style="color:var(--error);">对比请求失败: ' +
            err.message +
            "</div>";
        statusText.textContent = "请求失败";
    } finally {
        compareBtn.disabled = false;
    }
}

function renderResults(data) {
    const container = document.getElementById("resultsContainer");

    const promptSection = `
        <div style="margin-bottom:16px;padding:12px;background:#fafafa;border-radius:8px;">
            <strong>提示词：</strong>${escapeHtml(data.prompt)}
        </div>`;

    const responsesHtml = data.responses
        .map(
            (r) => `
        <div class="result-card ${r.model_name === data.winner ? "winner" : ""}">
            <div class="result-header">
                <span class="model-label">
                    ${r.model_name}
                    <span style="color:var(--text-secondary);font-weight:400;">
                        (${r.provider})
                    </span>
                    ${r.model_name === data.winner ? '<span class="winner-badge">最佳</span>' : ""}
                </span>
                <span class="metrics">
                    ${r.success ? `延迟: ${r.latency_ms}ms | Tokens: ${r.token_count}` : "请求失败"}
                </span>
            </div>
            ${
                r.success
                    ? `<div class="result-body">${escapeHtml(r.content)}</div>`
                    : `<div class="result-error">错误: ${escapeHtml(r.error || "未知错误")}</div>`
            }
        </div>`
        )
        .join("");

    container.innerHTML = promptSection + '<div class="results-grid">' + responsesHtml + "</div>";
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}