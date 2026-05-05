from fastapi.responses import HTMLResponse


INDEX_HTML = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Legal Multi-Agent Studio</title>
  <style>
    :root {
      --bg: #f5efe6;
      --panel: rgba(255, 251, 245, 0.95);
      --panel-2: #fffaf3;
      --ink: #1f1a16;
      --muted: #6f675e;
      --line: rgba(78, 55, 31, 0.12);
      --accent: #9e4c2d;
      --accent-deep: #6f3018;
      --accent-soft: rgba(158, 76, 45, 0.10);
      --teal: #224b58;
      --good: #21664f;
      --warn: #946411;
      --bad: #8e2f2f;
      --shadow: 0 18px 48px rgba(67, 46, 26, 0.10);
      --radius-xl: 28px;
      --radius-lg: 20px;
      --radius-md: 14px;
      --mono: "JetBrains Mono", "Cascadia Code", Consolas, monospace;
      --sans: "PingFang SC", "Microsoft YaHei", "Noto Sans SC", "Segoe UI", sans-serif;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      font-family: var(--sans);
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(158, 76, 45, 0.12), transparent 26%),
        linear-gradient(160deg, #f7f1e7 0%, #efe4d3 55%, #ece0d0 100%);
    }

    /* ── header ── */
    .header {
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px 20px 0;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }
    .header h1 {
      margin: 0;
      font-size: 22px;
      letter-spacing: -0.03em;
    }
    .header-right {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .health-dot {
      width: 8px; height: 8px;
      border-radius: 999px;
      background: var(--muted);
      flex-shrink: 0;
    }
    .health-dot.ok { background: var(--good); }
    .health-dot.err { background: var(--bad); }
    .health-text {
      font-size: 12px;
      color: var(--muted);
    }
    .fetch-row {
      display: flex;
      gap: 8px;
      align-items: center;
    }
    .fetch-row input {
      width: 260px;
      border: 1px solid rgba(78, 55, 31, 0.14);
      border-radius: 10px;
      padding: 7px 10px;
      background: var(--panel);
      font: inherit;
      font-size: 13px;
      color: var(--ink);
      outline: none;
    }
    .fetch-row input:focus {
      border-color: rgba(158, 76, 45, 0.5);
    }

    /* ── layout ── */
    .layout {
      max-width: 1200px;
      margin: 16px auto 36px;
      padding: 0 12px;
      display: grid;
      grid-template-columns: 380px minmax(0, 1fr);
      gap: 16px;
      align-items: start;
    }

    /* ── panels ── */
    .panel {
      border: 1px solid var(--line);
      border-radius: var(--radius-xl);
      background: var(--panel);
      box-shadow: var(--shadow);
    }
    .panel-head {
      padding: 16px 20px;
      border-bottom: 1px solid var(--line);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .panel-head h2 {
      margin: 0;
      font-size: 17px;
      letter-spacing: -0.02em;
    }
    .tag {
      display: inline-flex;
      padding: 5px 10px;
      border-radius: 999px;
      background: var(--accent-soft);
      color: var(--accent);
      font-size: 11px;
      font-weight: 800;
    }
    .panel-body {
      padding: 18px 20px 20px;
      display: grid;
      gap: 14px;
    }

    /* ── form fields ── */
    .field { display: grid; gap: 6px; }
    .field label {
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
    }
    input, textarea {
      width: 100%;
      border: 1px solid rgba(78, 55, 31, 0.14);
      border-radius: 12px;
      padding: 11px 12px;
      background: var(--panel-2);
      color: var(--ink);
      font: inherit;
      font-size: 14px;
      outline: none;
      transition: border-color 160ms, box-shadow 160ms;
    }
    input:focus, textarea:focus {
      border-color: rgba(158, 76, 45, 0.55);
      box-shadow: 0 0 0 3px rgba(158, 76, 45, 0.10);
    }
    textarea {
      min-height: 90px;
      resize: vertical;
      line-height: 1.6;
    }

    /* ── materials ── */
    .materials { display: grid; gap: 10px; }
    .material {
      border: 1px solid rgba(78, 55, 31, 0.10);
      border-radius: 14px;
      padding: 12px;
      background: rgba(255,255,255,0.58);
      display: grid;
      gap: 8px;
    }
    .material-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .material-index {
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
    }
    .remove-btn {
      appearance: none;
      border: 0;
      border-radius: 8px;
      padding: 5px 10px;
      background: rgba(142, 47, 47, 0.10);
      color: var(--bad);
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
    }
    .remove-btn:hover { background: rgba(142, 47, 47, 0.18); }
    .remove-btn:disabled { opacity: 0.4; cursor: default; }

    /* ── buttons ── */
    .actions {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    button {
      appearance: none;
      border: 0;
      border-radius: 12px;
      padding: 10px 14px;
      font: inherit;
      font-size: 13px;
      font-weight: 800;
      cursor: pointer;
      transition: transform 160ms, opacity 160ms;
    }
    button:hover { transform: translateY(-1px); }
    button:disabled { opacity: 0.6; cursor: wait; transform: none; }
    .btn-primary {
      background: linear-gradient(135deg, var(--accent), var(--accent-deep));
      color: #fff8f2;
    }
    .btn-secondary {
      background: rgba(255,255,255,0.70);
      color: var(--ink);
      border: 1px solid rgba(78, 55, 31, 0.10);
    }
    .btn-ghost {
      background: rgba(34, 75, 88, 0.08);
      color: var(--teal);
    }

    /* ── status ── */
    .status {
      min-height: 40px;
      padding: 10px 12px;
      border-radius: 12px;
      background: rgba(255,255,255,0.48);
      border: 1px dashed rgba(78, 55, 31, 0.14);
      color: var(--muted);
      font-size: 13px;
      line-height: 1.6;
      white-space: pre-wrap;
    }

    /* ── report ── */
    .report { display: grid; gap: 14px; }
    .report-banner {
      padding: 18px 20px;
      border-radius: 22px;
      background: linear-gradient(135deg, rgba(34, 75, 88, 0.95), rgba(26, 54, 64, 0.92));
      color: #eef4f6;
      display: grid;
      gap: 12px;
    }
    .report-banner h3 {
      margin: 0;
      font-size: 22px;
      letter-spacing: -0.04em;
    }
    .report-meta {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 8px;
    }
    .meta-box {
      padding: 12px;
      border-radius: 14px;
      background: rgba(255,255,255,0.08);
      border: 1px solid rgba(255,255,255,0.10);
    }
    .meta-box .k {
      font-size: 10px;
      color: rgba(238,244,246,0.72);
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }
    .meta-box .v {
      margin-top: 6px;
      font-size: 16px;
      font-weight: 800;
      word-break: break-word;
    }

    /* ── sections ── */
    .section {
      border: 1px solid rgba(78, 55, 31, 0.10);
      border-radius: 18px;
      background: rgba(255,255,255,0.64);
      overflow: hidden;
    }
    .section-head {
      padding: 14px 18px;
      border-bottom: 1px solid rgba(78, 55, 31, 0.08);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .section-head h4 { margin: 0; font-size: 14px; }
    .section-body {
      padding: 16px 18px;
      display: grid;
      gap: 10px;
    }
    .two-col {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }
    .lede {
      white-space: pre-wrap;
      line-height: 1.8;
      font-size: 14px;
      color: #342b23;
    }
    .item {
      padding: 12px;
      border-radius: 14px;
      background: rgba(255,255,255,0.68);
      border: 1px solid rgba(78, 55, 31, 0.08);
    }
    .item h5 { margin: 0 0 6px; font-size: 14px; }
    .item p {
      margin: 0;
      color: var(--muted);
      line-height: 1.7;
      white-space: pre-wrap;
      word-break: break-word;
      font-size: 13px;
    }
    .list {
      margin: 0;
      padding-left: 18px;
      color: var(--muted);
      display: grid;
      gap: 6px;
      line-height: 1.7;
      font-size: 13px;
    }
    .tag.low { background: rgba(33, 102, 79, 0.12); color: var(--good); }
    .tag.medium { background: rgba(148, 100, 17, 0.12); color: var(--warn); }
    .tag.high { background: rgba(142, 47, 47, 0.12); color: var(--bad); }
    .token-row {
      margin-top: 8px;
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }
    .token {
      padding: 4px 8px;
      border-radius: 999px;
      background: rgba(34, 75, 88, 0.08);
      color: var(--teal);
      font-size: 11px;
      font-family: var(--mono);
    }

    /* ── details / accordion ── */
    details {
      border: 1px solid rgba(78, 55, 31, 0.10);
      border-radius: 16px;
      background: rgba(255,255,255,0.55);
      overflow: hidden;
    }
    details summary {
      list-style: none;
      cursor: pointer;
      padding: 12px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-weight: 800;
      font-size: 14px;
    }
    details summary::-webkit-details-marker { display: none; }
    .summary-meta {
      color: var(--muted);
      font-size: 12px;
      font-weight: 600;
    }
    .debug-list {
      padding: 0 16px 14px;
      display: grid;
      gap: 10px;
    }
    pre {
      margin: 0;
      padding: 14px;
      border-radius: 12px;
      background: #1d1814;
      color: #f7eedb;
      overflow: auto;
      white-space: pre-wrap;
      word-break: break-word;
      line-height: 1.6;
      font-family: var(--mono);
      font-size: 12px;
    }
    .empty {
      padding: 16px;
      border-radius: 16px;
      border: 1px dashed rgba(78, 55, 31, 0.16);
      background: rgba(255,255,255,0.42);
      color: var(--muted);
      font-size: 13px;
      line-height: 1.7;
    }

    @media (max-width: 960px) {
      .layout { grid-template-columns: 1fr; }
    }
    @media (max-width: 720px) {
      .two-col, .report-meta { grid-template-columns: 1fr; }
      .header { flex-direction: column; align-items: flex-start; }
      .fetch-row input { width: 100%; }
    }
  </style>
</head>
<body>

  <!-- header bar -->
  <header class="header">
    <h1>法律多 Agent 工作台</h1>
    <div class="header-right">
      <div class="fetch-row">
        <input id="analysisIdInput" placeholder="输入 analysis_id 回查..." />
        <button id="fetchBtn" class="btn-secondary" type="button">加载</button>
      </div>
      <div id="healthDot" class="health-dot"></div>
      <span id="healthText" class="health-text">检查中...</span>
    </div>
  </header>

  <div class="layout">

    <!-- left: input panel -->
    <section class="panel">
      <div class="panel-head">
        <h2>案件输入</h2>
        <span class="tag">POST /analysis</span>
      </div>
      <div class="panel-body">
        <div class="field">
          <label for="userQuery">法律问题</label>
          <textarea id="userQuery" placeholder="例如：请审查合同解除条款和违约责任风险"></textarea>
        </div>
        <div class="field">
          <label for="caseTypeHint">案件类型提示 · 可选</label>
          <input id="caseTypeHint" placeholder="例如 contract_review" />
        </div>
        <div class="field">
          <label>材料列表</label>
          <div id="materialsList" class="materials"></div>
          <div class="actions">
            <button id="addMaterialBtn" class="btn-ghost" type="button">+ 新增材料</button>
          </div>
        </div>
        <div class="actions">
          <button id="analyzeBtn" class="btn-primary" type="button">开始分析</button>
          <button id="fillBtn" class="btn-secondary" type="button">载入示例</button>
          <button id="clearBtn" class="btn-secondary" type="button">清空</button>
        </div>
        <div id="statusBox" class="status">就绪。填写案件后点击“开始分析”。</div>
      </div>
    </section>

    <!-- right: report panel -->
    <section class="panel">
      <div class="panel-head">
        <h2>分析报告</h2>
        <span class="tag">GET /analysis/{id}</span>
      </div>
      <div class="panel-body">
        <div id="emptyState" class="empty">还没有报告。运行一次分析，或通过右上角 analysis_id 取回历史结果。</div>

        <div id="reportShell" class="report" hidden>
          <section class="report-banner">
            <h3 id="reportTitle">分析报告</h3>
            <div id="reportKpis" class="report-meta"></div>
          </section>

          <section class="section">
            <div class="section-head">
              <h4>核心意见</h4>
              <span id="headlineRisk" class="tag">medium</span>
            </div>
            <div class="section-body">
              <div id="draftOpinion" class="lede"></div>
            </div>
          </section>

          <div class="two-col">
            <section class="section">
              <div class="section-head"><h4>事实提取</h4></div>
              <div id="factsList" class="section-body"></div>
            </section>
            <section class="section">
              <div class="section-head"><h4>建议动作</h4></div>
              <div class="section-body"><ul id="actionsList" class="list"></ul></div>
            </section>
          </div>

          <section class="section">
            <div class="section-head">
              <h4>问题项与风险</h4>
            </div>
            <div id="issuesList" class="section-body"></div>
          </section>

          <div class="two-col">
            <section class="section">
              <div class="section-head"><h4>法律依据</h4></div>
              <div id="basisList" class="section-body"></div>
            </section>
            <section class="section">
              <div class="section-head"><h4>资深复核</h4></div>
              <div class="section-body"><ul id="reviewList" class="list"></ul></div>
            </section>
          </div>

          <details>
            <summary>
              <span>Agent 协调日志</span>
              <span class="summary-meta">流转记录</span>
            </summary>
            <div id="coordinationList" class="debug-list"></div>
          </details>

          <details>
            <summary>
              <span>Agent 执行轨迹</span>
              <span class="summary-meta">节点摘要</span>
            </summary>
            <div id="traceList" class="debug-list"></div>
          </details>

          <details id="debugPanel">
            <summary>
              <span>LLM 调试面板</span>
              <span id="debugMeta" class="summary-meta">0 entries</span>
            </summary>
            <div id="debugList" class="debug-list"></div>
          </details>

          <details>
            <summary>
              <span>原始 JSON</span>
              <span class="summary-meta">完整响应</span>
            </summary>
            <div class="debug-list"><pre id="rawJson"></pre></div>
          </details>
        </div>
      </div>
    </section>
  </div>

  <template id="materialTemplate">
    <article class="material">
      <div class="material-top">
        <span class="material-index">材料 1</span>
        <button class="remove-btn" type="button">删除</button>
      </div>
      <div class="field">
        <label>标题</label>
        <input data-role="title" placeholder="例如：服务合同" />
      </div>
      <div class="field">
        <label>内容</label>
        <textarea data-role="content" placeholder="粘贴材料正文"></textarea>
      </div>
    </article>
  </template>

  <script>
    const example = {
      user_query: "请审查这份合同中的解除条款和违约责任风险，并说明解除条件是否明确、违约金是否可能被调减。",
      case_type_hint: "contract_review",
      materials: [
        {
          title: "服务合同",
          content: "甲方委托乙方提供服务。若乙方逾期15日未完成交付，甲方可以解除合同。违约金按合同总价的30%计算。"
        },
        {
          title: "往来记录",
          content: "乙方在第10天表示可能延期，但未提交明确补救方案。"
        }
      ]
    };

    const el = {
      userQuery: document.getElementById("userQuery"),
      caseTypeHint: document.getElementById("caseTypeHint"),
      materialsList: document.getElementById("materialsList"),
      materialTemplate: document.getElementById("materialTemplate"),
      addMaterialBtn: document.getElementById("addMaterialBtn"),
      analyzeBtn: document.getElementById("analyzeBtn"),
      fillBtn: document.getElementById("fillBtn"),
      clearBtn: document.getElementById("clearBtn"),
      fetchBtn: document.getElementById("fetchBtn"),
      analysisIdInput: document.getElementById("analysisIdInput"),
      statusBox: document.getElementById("statusBox"),
      healthDot: document.getElementById("healthDot"),
      healthText: document.getElementById("healthText"),
      emptyState: document.getElementById("emptyState"),
      reportShell: document.getElementById("reportShell"),
      reportTitle: document.getElementById("reportTitle"),
      reportKpis: document.getElementById("reportKpis"),
      headlineRisk: document.getElementById("headlineRisk"),
      draftOpinion: document.getElementById("draftOpinion"),
      factsList: document.getElementById("factsList"),
      actionsList: document.getElementById("actionsList"),
      issuesList: document.getElementById("issuesList"),
      basisList: document.getElementById("basisList"),
      reviewList: document.getElementById("reviewList"),
      coordinationList: document.getElementById("coordinationList"),
      traceList: document.getElementById("traceList"),
      debugMeta: document.getElementById("debugMeta"),
      debugList: document.getElementById("debugList"),
      rawJson: document.getElementById("rawJson")
    };

    function escapeHtml(value) {
      return String(value ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
    }

    function setStatus(message, tone) {
      el.statusBox.textContent = message;
      const colors = { muted: "var(--muted)", info: "var(--teal)", good: "var(--good)", error: "var(--bad)" };
      el.statusBox.style.color = colors[tone] || colors.muted;
    }

    function setHealth(ok) {
      el.healthDot.className = "health-dot " + (ok ? "ok" : "err");
      el.healthText.textContent = ok ? "服务正常" : "服劣异常";
    }

    function setBusy(isBusy, message) {
      el.analyzeBtn.disabled = isBusy;
      el.fetchBtn.disabled = isBusy;
      if (message) setStatus(message, isBusy ? "info" : "muted");
    }

    function createMaterialCard(data) {
      data = data || {};
      const frag = el.materialTemplate.content.cloneNode(true);
      const card = frag.querySelector(".material");
      frag.querySelector('[data-role="title"]').value = data.title || "";
      frag.querySelector('[data-role="content"]').value = data.content || "";
      frag.querySelector(".remove-btn").addEventListener("click", function() {
        card.remove();
        refreshMaterialLabels();
      });
      el.materialsList.appendChild(frag);
      refreshMaterialLabels();
    }

    function refreshMaterialLabels() {
      const children = el.materialsList.children;
      for (let i = 0; i < children.length; i++) {
        children[i].querySelector(".material-index").textContent = "材料 " + (i + 1);
        children[i].querySelector(".remove-btn").disabled = children.length === 1;
      }
    }

    function loadExample() {
      el.userQuery.value = example.user_query;
      el.caseTypeHint.value = example.case_type_hint;
      el.materialsList.innerHTML = "";
      example.materials.forEach(function(item) { createMaterialCard(item); });
      setStatus("已加载示例数据。", "good");
    }

    function collectPayload() {
      var materials = [];
      var nodes = el.materialsList.children;
      for (var i = 0; i < nodes.length; i++) {
        var t = nodes[i].querySelector('[data-role="title"]').value.trim();
        var c = nodes[i].querySelector('[data-role="content"]').value.trim();
        if (c) materials.push({ title: t, content: c });
      }
      return {
        user_query: el.userQuery.value.trim(),
        case_type_hint: el.caseTypeHint.value.trim() || null,
        materials: materials
      };
    }

    async function requestJson(url, options) {
      var response = await fetch(url, options);
      var text = await response.text();
      var parsed = null;
      try { parsed = text ? JSON.parse(text) : null; } catch(e) { parsed = { raw: text }; }
      if (!response.ok) {
        var detail = parsed && parsed.detail ? parsed.detail : text || "HTTP " + response.status;
        throw new Error(detail);
      }
      return parsed;
    }

    function renderList(container, items, renderer, emptyText) {
      if (!items || !items.length) {
        container.innerHTML = '<div class="empty">' + escapeHtml(emptyText) + '</div>';
        return;
      }
      container.innerHTML = items.map(renderer).join("");
    }

    function renderSimpleList(container, items, emptyText) {
      if (!items || !items.length) {
        container.innerHTML = '<div class="empty">' + escapeHtml(emptyText) + '</div>';
        return;
      }
      container.innerHTML = '<ul class="list">' + items.map(function(item) {
        return '<li>' + escapeHtml(item) + '</li>';
      }).join("") + '</ul>';
    }

    function renderMeta(data) {
      var items = [
        ["analysis_id", data.analysis_id],
        ["matter_type", data.matter_type],
        ["risk_level", data.risk_level],
        ["confidence", data.confidence]
      ];
      el.reportKpis.innerHTML = items.map(function(pair) {
        return '<div class="meta-box"><div class="k">' + escapeHtml(pair[0]) + '</div><div class="v">' + escapeHtml(pair[1] || "-") + '</div></div>';
      }).join("");
    }

    function renderReport(data) {
      el.emptyState.hidden = true;
      el.reportShell.hidden = false;
      el.analysisIdInput.value = data.analysis_id || "";
      el.reportTitle.textContent = (data.matter_type || "legal") + " 分析报告";
      el.headlineRisk.textContent = data.risk_level || "medium";
      el.headlineRisk.className = "tag " + escapeHtml(data.risk_level || "medium");
      el.draftOpinion.textContent = data.draft_opinion || "暂无初步意见。";
      renderMeta(data);

      renderList(el.factsList, data.facts, function(fact, index) {
        return '<div class="item"><h5>事实 ' + (index + 1) + '</h5><p>' + escapeHtml(fact) + '</p></div>';
      }, "暂无事实提取。");

      renderSimpleList(el.actionsList, data.suggested_actions, "暂无建议动作。");

      renderList(el.issuesList, data.issues, function(issue) {
        var tags = '<div class="token-row"><span class="tag ' + escapeHtml(issue.risk_level || "medium") + '">' + escapeHtml(issue.risk_level || "medium") + '</span></div>';
        return '<div class="item"><h5>' + escapeHtml(issue.title || "未命名问题") + '</h5><p>' + escapeHtml(issue.analysis || "") + '</p>' + tags + '</div>';
      }, "暂无问题项。");

      renderList(el.basisList, data.legal_basis, function(basis) {
        var tokens = '<div class="token-row"><span class="token">' + escapeHtml(basis.source_type || "") + '</span><span class="token">' + escapeHtml(basis.reference_id || "") + '</span><span class="token">score: ' + escapeHtml(basis.score != null ? basis.score : "-") + '</span></div>';
        return '<div class="item"><h5>' + escapeHtml(basis.title || "") + '</h5><p>' + escapeHtml(basis.excerpt || "") + '</p>' + tokens + '</div>';
      }, "暂无法律依据。");

      renderSimpleList(el.reviewList, data.review_notes, "暂无复核意见。");

      renderList(el.coordinationList, data.coordination_log, function(entry) {
        return '<div class="item"><h5>' + escapeHtml(entry.sender || "") + " → " + escapeHtml(entry.recipient || "") + '</h5><p>' + escapeHtml(entry.content || "") + '</p></div>';
      }, "暂无协调日志。");

      renderList(el.traceList, data.trace, function(entry) {
        return '<div class="item"><h5>' + escapeHtml(entry.agent_name || "") + '</h5><p>' + escapeHtml(entry.summary || "") + '</p></div>';
      }, "暂无执行轨迹。");

      renderList(el.debugList, data.llm_debug, function(entry) {
        return '<div class="item"><h5>' + escapeHtml(entry.agent_name || "agent") + " · " + escapeHtml(entry.task || "task") + '</h5><pre>' + escapeHtml(JSON.stringify(entry.output, null, 2)) + '</pre></div>';
      }, "暂无 LLM 调试输出。");

      el.debugMeta.textContent = (Array.isArray(data.llm_debug) ? data.llm_debug.length : 0) + " entries";
      el.rawJson.textContent = JSON.stringify(data, null, 2);
    }

    async function runAnalysis() {
      var payload = collectPayload();
      if (!payload.user_query) { setStatus("请先填写法律问题。", "error"); return; }
      if (!payload.materials.length) { setStatus("至少需要一份有内容的材料。", "error"); return; }
      setBusy(true, "正在运行多 Agent 分析...");
      try {
        var data = await requestJson("/analysis", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
        renderReport(data);
        setStatus("分析完成，analysis_id: " + data.analysis_id, "good");
      } catch (error) {
        setStatus("分析失败：" + error.message, "error");
      } finally {
        setBusy(false);
      }
    }

    async function fetchAnalysis() {
      var analysisId = el.analysisIdInput.value.trim();
      if (!analysisId) { setStatus("请输入 analysis_id。", "error"); return; }
      setBusy(true, "正在加载历史报告...");
      try {
        var data = await requestJson("/analysis/" + encodeURIComponent(analysisId), { method: "GET" });
        renderReport(data);
        setStatus("已取回报告：" + data.analysis_id, "good");
      } catch (error) {
        setStatus("加载失败：" + error.message, "error");
      } finally {
        setBusy(false);
      }
    }

    async function checkHealth() {
      try {
        await requestJson("/health", { method: "GET" });
        setHealth(true);
      } catch (error) {
        setHealth(false);
      }
    }

    function clearReport() {
      el.emptyState.hidden = false;
      el.reportShell.hidden = true;
      el.analysisIdInput.value = "";
      el.rawJson.textContent = "";
      setStatus("已清空结果区。");
    }

    el.addMaterialBtn.addEventListener("click", function() { createMaterialCard(); });
    el.fillBtn.addEventListener("click", loadExample);
    el.clearBtn.addEventListener("click", clearReport);
    el.analyzeBtn.addEventListener("click", runAnalysis);
    el.fetchBtn.addEventListener("click", fetchAnalysis);

    createMaterialCard();
    loadExample();
    checkHealth();
  </script>
</body>
</html>"""


def render_index() -> HTMLResponse:
    return HTMLResponse(INDEX_HTML)
