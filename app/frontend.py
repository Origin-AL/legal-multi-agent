from fastapi.responses import HTMLResponse


INDEX_HTML = r"""
<!doctype html>
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

    .page {
      width: min(1320px, calc(100vw - 24px));
      margin: 18px auto 36px;
      display: grid;
      gap: 18px;
    }

    .hero, .panel {
      border: 1px solid var(--line);
      border-radius: var(--radius-xl);
      background: var(--panel);
      box-shadow: var(--shadow);
    }

    .hero {
      padding: 28px 28px 24px;
      position: relative;
      overflow: hidden;
    }

    .hero::after {
      content: "";
      position: absolute;
      right: -50px;
      top: -60px;
      width: 220px;
      height: 220px;
      border-radius: 999px;
      background: radial-gradient(circle, rgba(158, 76, 45, 0.14), transparent 68%);
      pointer-events: none;
    }

    .hero-badge {
      display: inline-flex;
      padding: 8px 12px;
      border-radius: 999px;
      background: rgba(34, 75, 88, 0.08);
      color: var(--teal);
      font-size: 12px;
      letter-spacing: 0.08em;
    }

    h1 {
      margin: 16px 0 10px;
      font-size: clamp(34px, 5vw, 56px);
      line-height: 1;
      letter-spacing: -0.05em;
    }

    .hero p {
      max-width: 760px;
      margin: 0;
      color: var(--muted);
      font-size: 15px;
      line-height: 1.8;
    }

    .hero-strip {
      margin-top: 18px;
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }

    .chip {
      padding: 8px 12px;
      border-radius: 999px;
      background: rgba(255,255,255,0.65);
      border: 1px solid rgba(78, 55, 31, 0.08);
      color: var(--muted);
      font-size: 12px;
    }

    .layout {
      display: grid;
      grid-template-columns: 400px minmax(0, 1fr);
      gap: 18px;
      align-items: start;
    }

    .panel-head {
      padding: 18px 22px;
      border-bottom: 1px solid var(--line);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }

    .panel-head h2 {
      margin: 0;
      font-size: 18px;
      letter-spacing: -0.02em;
    }

    .panel-head p {
      margin: 4px 0 0;
      color: var(--muted);
      font-size: 12px;
    }

    .panel-body {
      padding: 20px 22px 22px;
      display: grid;
      gap: 16px;
    }

    .field {
      display: grid;
      gap: 8px;
    }

    .field label {
      color: var(--muted);
      font-size: 13px;
      font-weight: 700;
    }

    input, textarea {
      width: 100%;
      border: 1px solid rgba(78, 55, 31, 0.14);
      border-radius: 14px;
      padding: 13px 14px;
      background: var(--panel-2);
      color: var(--ink);
      font: inherit;
      outline: none;
      transition: border-color 160ms ease, box-shadow 160ms ease;
    }

    input:focus, textarea:focus {
      border-color: rgba(158, 76, 45, 0.55);
      box-shadow: 0 0 0 4px rgba(158, 76, 45, 0.10);
    }

    textarea {
      min-height: 104px;
      resize: vertical;
      line-height: 1.65;
    }

    .actions {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }

    button {
      appearance: none;
      border: 0;
      border-radius: 14px;
      padding: 12px 15px;
      font: inherit;
      font-weight: 800;
      cursor: pointer;
      transition: transform 160ms ease, opacity 160ms ease;
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

    .status {
      min-height: 54px;
      padding: 14px;
      border-radius: 16px;
      background: rgba(255,255,255,0.48);
      border: 1px dashed rgba(78, 55, 31, 0.14);
      color: var(--muted);
      line-height: 1.7;
      white-space: pre-wrap;
    }

    .materials {
      display: grid;
      gap: 12px;
    }

    .material {
      border: 1px solid rgba(78, 55, 31, 0.10);
      border-radius: 18px;
      padding: 14px;
      background: rgba(255,255,255,0.58);
      display: grid;
      gap: 10px;
    }

    .material-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }

    .material-index {
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }

    .remove-btn {
      padding: 7px 10px;
      border-radius: 10px;
      background: rgba(142, 47, 47, 0.10);
      color: var(--bad);
      font-size: 12px;
    }

    .report {
      display: grid;
      gap: 16px;
    }

    .report-banner {
      padding: 20px 22px;
      border-radius: 24px;
      background: linear-gradient(135deg, rgba(34, 75, 88, 0.95), rgba(26, 54, 64, 0.92));
      color: #eef4f6;
      display: grid;
      gap: 14px;
    }

    .report-banner h3 {
      margin: 0;
      font-size: 24px;
      letter-spacing: -0.04em;
    }

    .report-meta {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
    }

    .meta-box {
      padding: 14px;
      border-radius: 16px;
      background: rgba(255,255,255,0.08);
      border: 1px solid rgba(255,255,255,0.10);
    }

    .meta-box .k {
      font-size: 11px;
      color: rgba(238,244,246,0.72);
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }

    .meta-box .v {
      margin-top: 8px;
      font-size: 18px;
      font-weight: 800;
      word-break: break-word;
    }

    .section {
      border: 1px solid rgba(78, 55, 31, 0.10);
      border-radius: 22px;
      background: rgba(255,255,255,0.64);
      overflow: hidden;
    }

    .section-head {
      padding: 16px 20px;
      border-bottom: 1px solid rgba(78, 55, 31, 0.08);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
    }

    .section-head h4 {
      margin: 0;
      font-size: 15px;
    }

    .section-body {
      padding: 18px 20px 20px;
      display: grid;
      gap: 12px;
    }

    .two-col {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }

    .lede {
      white-space: pre-wrap;
      line-height: 1.8;
      font-size: 15px;
      color: #342b23;
    }

    .item {
      padding: 14px;
      border-radius: 16px;
      background: rgba(255,255,255,0.68);
      border: 1px solid rgba(78, 55, 31, 0.08);
    }

    .item h5 {
      margin: 0 0 8px;
      font-size: 15px;
    }

    .item p {
      margin: 0;
      color: var(--muted);
      line-height: 1.7;
      white-space: pre-wrap;
      word-break: break-word;
    }

    .list {
      margin: 0;
      padding-left: 18px;
      color: var(--muted);
      display: grid;
      gap: 8px;
      line-height: 1.7;
    }

    .tag {
      display: inline-flex;
      align-items: center;
      padding: 6px 10px;
      border-radius: 999px;
      background: var(--accent-soft);
      color: var(--accent);
      font-size: 12px;
      font-weight: 800;
    }

    .tag.low { background: rgba(33, 102, 79, 0.12); color: var(--good); }
    .tag.medium { background: rgba(148, 100, 17, 0.12); color: var(--warn); }
    .tag.high { background: rgba(142, 47, 47, 0.12); color: var(--bad); }

    .token-row {
      margin-top: 10px;
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .token {
      padding: 5px 8px;
      border-radius: 999px;
      background: rgba(34, 75, 88, 0.08);
      color: var(--teal);
      font-size: 12px;
      font-family: var(--mono);
    }

    details {
      border: 1px solid rgba(78, 55, 31, 0.10);
      border-radius: 18px;
      background: rgba(255,255,255,0.55);
      overflow: hidden;
    }

    details summary {
      list-style: none;
      cursor: pointer;
      padding: 14px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      font-weight: 800;
    }

    details summary::-webkit-details-marker { display: none; }

    .summary-meta {
      color: var(--muted);
      font-size: 12px;
      font-weight: 600;
    }

    .debug-list {
      padding: 0 16px 16px;
      display: grid;
      gap: 12px;
    }

    pre {
      margin: 0;
      padding: 16px;
      border-radius: 14px;
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
      padding: 18px;
      border-radius: 18px;
      border: 1px dashed rgba(78, 55, 31, 0.16);
      background: rgba(255,255,255,0.42);
      color: var(--muted);
      line-height: 1.7;
    }

    @media (max-width: 1160px) {
      .layout { grid-template-columns: 1fr; }
    }

    @media (max-width: 860px) {
      .two-col, .report-meta { grid-template-columns: 1fr; }
    }

    @media (max-width: 640px) {
      .page { width: min(100vw - 14px, 100%); margin-top: 8px; }
      .hero, .panel-body, .panel-head, .section-head, .section-body { padding-left: 16px; padding-right: 16px; }
      h1 { font-size: 34px; }
    }
  </style>
</head>
<body>
  <div class="page">
    <section class="hero">
      <div class="hero-badge">\u6cd5\u5f8b\u591a Agent \u5de5\u4f5c\u53f0</div>
      <h1>\u6d4f\u89c8\u5668\u6cd5\u5f8b\u5206\u6790\u5de5\u4f5c\u533a</h1>
      <p>\u5728\u4e00\u4e2a\u9875\u9762\u91cc\u5b8c\u6210\u6848\u60c5\u5f55\u5165\u3001\u591a\u6750\u6599\u5206\u6790\u3001\u5386\u53f2\u7ed3\u679c\u56de\u67e5\u548c LLM \u8c03\u8bd5\u3002\u9875\u9762\u88ab\u6536\u7f29\u6210\u66f4\u504f\u6cd5\u5f8b\u5ba1\u67e5\u5de5\u4f5c\u6d41\uff0c\u51cf\u5c11\u4e0d\u5fc5\u8981\u7684\u89c6\u89c9\u5e72\u6270\u3002</p>
      <div class="hero-strip">
        <div class="chip">\u591a\u6750\u6599\u8f93\u5165</div>
        <div class="chip">\u62a5\u544a\u5f0f\u7ed3\u679c</div>
        <div class="chip">analysis_id \u56de\u67e5</div>
        <div class="chip">LLM \u8c03\u8bd5\u9762\u677f</div>
      </div>
    </section>

    <div class="layout">
      <section class="panel">
        <div class="panel-head">
          <div>
            <h2>\u6848\u4ef6\u8f93\u5165</h2>
            <p>\u586b\u5199\u95ee\u9898\uff0c\u7ec4\u88c5\u6750\u6599\uff0c\u76f4\u63a5\u53d1\u8d77\u5206\u6790</p>
          </div>
          <span class="tag">POST /analysis</span>
        </div>
        <div class="panel-body">
          <div class="field">
            <label for="userQuery">\u6cd5\u5f8b\u95ee\u9898</label>
            <textarea id="userQuery" placeholder="\u4f8b\u5982\uff1a\u8bf7\u5ba1\u67e5\u5408\u540c\u89e3\u9664\u6761\u6b3e\u548c\u8fdd\u7ea6\u8d23\u4efb\u98ce\u9669"></textarea>
          </div>

          <div class="field">
            <label for="caseTypeHint">\u6848\u4ef6\u7c7b\u578b\u63d0\u793a</label>
            <input id="caseTypeHint" placeholder="\u53ef\u9009\uff0c\u4f8b\u5982 contract_review" />
          </div>

          <div class="field">
            <label>\u6750\u6599\u5217\u8868</label>
            <div id="materialsList" class="materials"></div>
            <div class="actions">
              <button id="addMaterialBtn" class="btn-ghost" type="button">\u65b0\u589e\u6750\u6599</button>
            </div>
          </div>

          <div class="actions">
            <button id="analyzeBtn" class="btn-primary" type="button">\u5f00\u59cb\u5206\u6790</button>
            <button id="fillBtn" class="btn-secondary" type="button">\u8f7d\u5165\u793a\u4f8b</button>
            <button id="clearBtn" class="btn-secondary" type="button">\u6e05\u7a7a\u7ed3\u679c</button>
          </div>

          <div class="field">
            <label for="analysisIdInput">analysis_id \u56de\u67e5</label>
            <input id="analysisIdInput" placeholder="\u8f93\u5165 analysis_id \u540e\u70b9\u51fb\u52a0\u8f7d\u62a5\u544a" />
          </div>

          <div class="actions">
            <button id="fetchBtn" class="btn-secondary" type="button">\u52a0\u8f7d\u62a5\u544a</button>
            <button id="healthBtn" class="btn-secondary" type="button">\u5065\u5eb7\u68c0\u67e5</button>
          </div>

          <div id="statusBox" class="status">\u5c31\u7eea\u3002\u4f60\u53ef\u4ee5\u76f4\u63a5\u586b\u5199\u6848\u4ef6\u540e\u5f00\u59cb\u6d4b\u8bd5\u3002</div>
          <div id="healthEcho" class="status">\u8fd8\u6ca1\u6709\u6267\u884c\u5065\u5eb7\u68c0\u67e5\u3002</div>
        </div>
      </section>

      <section class="panel">
        <div class="panel-head">
          <div>
            <h2>\u5206\u6790\u62a5\u544a</h2>
            <p>\u805a\u7126\u7ed3\u8bba\uff0c\u95ee\u9898\uff0c\u4f9d\u636e\uff0c\u590d\u6838\uff0c\u8c03\u8bd5</p>
          </div>
          <span class="tag">GET /analysis/{id}</span>
        </div>
        <div class="panel-body">
          <div id="emptyState" class="empty">\u8fd8\u6ca1\u6709\u62a5\u544a\u3002\u8fd0\u884c\u4e00\u6b21\u5206\u6790\uff0c\u6216\u8005\u901a\u8fc7 analysis_id \u53d6\u56de\u5386\u53f2\u7ed3\u679c\u3002</div>

          <div id="reportShell" class="report" hidden>
            <section class="report-banner">
              <div class="chip">\u6cd5\u5f8b\u5ba1\u67e5\u8f93\u51fa</div>
              <h3 id="reportTitle">\u5206\u6790\u62a5\u544a</h3>
              <div id="reportKpis" class="report-meta"></div>
            </section>

            <section class="section">
              <div class="section-head">
                <h4>\u6838\u5fc3\u610f\u89c1</h4>
                <span id="headlineRisk" class="tag">medium</span>
              </div>
              <div class="section-body">
                <div id="draftOpinion" class="lede"></div>
              </div>
            </section>

            <div class="two-col">
              <section class="section">
                <div class="section-head">
                  <h4>\u4e8b\u5b9e\u63d0\u53d6</h4>
                  <span class="chip">\u4e8b\u5b9e</span>
                </div>
                <div id="factsList" class="section-body"></div>
              </section>

              <section class="section">
                <div class="section-head">
                  <h4>\u5efa\u8bae\u52a8\u4f5c</h4>
                  <span class="chip">\u540e\u7eed</span>
                </div>
                <div class="section-body">
                  <ul id="actionsList" class="list"></ul>
                </div>
              </section>
            </div>

            <section class="section">
              <div class="section-head">
                <h4>\u95ee\u9898\u9879\u4e0e\u98ce\u9669</h4>
                <span class="chip">\u98ce\u9669</span>
              </div>
              <div id="issuesList" class="section-body"></div>
            </section>

            <div class="two-col">
              <section class="section">
                <div class="section-head">
                  <h4>\u6cd5\u5f8b\u4f9d\u636e</h4>
                  <span class="chip">\u68c0\u7d22</span>
                </div>
                <div id="basisList" class="section-body"></div>
              </section>

              <section class="section">
                <div class="section-head">
                  <h4>\u8d44\u6df1\u590d\u6838</h4>
                  <span class="chip">\u8d28\u63a7</span>
                </div>
                <div class="section-body">
                  <ul id="reviewList" class="list"></ul>
                </div>
              </section>
            </div>

            <details>
              <summary>
                <span>Agent \u534f\u8c03\u65e5\u5fd7</span>
                <span class="summary-meta">\u5185\u90e8\u6d41\u8f6c</span>
              </summary>
              <div id="coordinationList" class="debug-list"></div>
            </details>

            <details>
              <summary>
                <span>Agent \u6267\u884c\u8f68\u8ff9</span>
                <span class="summary-meta">\u8282\u70b9\u6458\u8981</span>
              </summary>
              <div id="traceList" class="debug-list"></div>
            </details>

            <details id="debugPanel">
              <summary>
                <span>LLM \u8c03\u8bd5\u9762\u677f</span>
                <span id="debugMeta" class="summary-meta">0 entries</span>
              </summary>
              <div id="debugList" class="debug-list"></div>
            </details>

            <details>
              <summary>
                <span>\u539f\u59cb JSON</span>
                <span class="summary-meta">\u5b8c\u6574\u54cd\u5e94</span>
              </summary>
              <div class="debug-list">
                <pre id="rawJson"></pre>
              </div>
            </details>
          </div>
        </div>
      </section>
    </div>
  </div>

  <template id="materialTemplate">
    <article class="material">
      <div class="material-top">
        <div class="material-index">Material</div>
        <button class="remove-btn" type="button">\u5220\u9664</button>
      </div>
      <div class="field">
        <label>\u6807\u9898</label>
        <input data-role="title" placeholder="\u4f8b\u5982\uff1a\u670d\u52a1\u5408\u540c" />
      </div>
      <div class="field">
        <label>\u5185\u5bb9</label>
        <textarea data-role="content" placeholder="\u7c98\u8d34\u6750\u6599\u6b63\u6587"></textarea>
      </div>
    </article>
  </template>

  <script>
    function decodeUnicodeEscapes(text) {
      return String(text).replace(/\\u([0-9a-fA-F]{4})/g, (_, hex) =>
        String.fromCharCode(parseInt(hex, 16))
      );
    }

    function decodeNodeTree(root) {
      const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
      const textNodes = [];
      while (walker.nextNode()) {
        textNodes.push(walker.currentNode);
      }
      textNodes.forEach(node => {
        if (node.nodeValue && node.nodeValue.includes("\\u")) {
          node.nodeValue = decodeUnicodeEscapes(node.nodeValue);
        }
      });

      root.querySelectorAll("[placeholder]").forEach(el => {
        const value = el.getAttribute("placeholder");
        if (value && value.includes("\\u")) {
          el.setAttribute("placeholder", decodeUnicodeEscapes(value));
        }
      });

      root.querySelectorAll("input, textarea").forEach(el => {
        if (typeof el.value === "string" && el.value.includes("\\u")) {
          el.value = decodeUnicodeEscapes(el.value);
        }
      });
    }

    const example = {
      user_query: "\u8bf7\u5ba1\u67e5\u8fd9\u4efd\u5408\u540c\u4e2d\u7684\u89e3\u9664\u6761\u6b3e\u548c\u8fdd\u7ea6\u8d23\u4efb\u98ce\u9669\uff0c\u5e76\u8bf4\u660e\u89e3\u9664\u6761\u4ef6\u662f\u5426\u660e\u786e\u3001\u8fdd\u7ea6\u91d1\u662f\u5426\u53ef\u80fd\u88ab\u8c03\u51cf\u3002",
      case_type_hint: "contract_review",
      materials: [
        {
          title: "\u670d\u52a1\u5408\u540c",
          content: "\u7532\u65b9\u59d4\u6258\u4e59\u65b9\u63d0\u4f9b\u670d\u52a1\u3002\u82e5\u4e59\u65b9\u903e\u671f15\u65e5\u672a\u5b8c\u6210\u4ea4\u4ed8\uff0c\u7532\u65b9\u53ef\u4ee5\u89e3\u9664\u5408\u540c\u3002\u8fdd\u7ea6\u91d1\u6309\u5408\u540c\u603b\u4ef7\u768430%\u8ba1\u7b97\u3002"
        },
        {
          title: "\u5f80\u6765\u8bb0\u5f55",
          content: "\u4e59\u65b9\u5728\u7b2c10\u5929\u8868\u793a\u53ef\u80fd\u5ef6\u671f\uff0c\u4f46\u672a\u63d0\u4ea4\u660e\u786e\u8865\u6551\u65b9\u6848\u3002"
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
      healthBtn: document.getElementById("healthBtn"),
      analysisIdInput: document.getElementById("analysisIdInput"),
      statusBox: document.getElementById("statusBox"),
      healthEcho: document.getElementById("healthEcho"),
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

    function setStatus(message, tone = "muted") {
      el.statusBox.textContent = message;
      const colors = {
        muted: "var(--muted)",
        info: "var(--teal)",
        good: "var(--good)",
        error: "var(--bad)"
      };
      el.statusBox.style.color = colors[tone] || colors.muted;
    }

    function setHealth(message, tone = "muted") {
      el.healthEcho.textContent = message;
      const colors = {
        muted: "var(--muted)",
        good: "var(--good)",
        error: "var(--bad)"
      };
      el.healthEcho.style.color = colors[tone] || colors.muted;
    }

    function setBusy(isBusy, message) {
      el.analyzeBtn.disabled = isBusy;
      el.fetchBtn.disabled = isBusy;
      if (message) {
        setStatus(message, isBusy ? "info" : "muted");
      }
    }

    function createMaterialCard(data = {}) {
      const fragment = el.materialTemplate.content.cloneNode(true);
      const card = fragment.querySelector(".material");
      const titleInput = fragment.querySelector('[data-role="title"]');
      const contentInput = fragment.querySelector('[data-role="content"]');
      const removeBtn = fragment.querySelector(".remove-btn");

      titleInput.value = data.title || "";
      contentInput.value = data.content || "";

      removeBtn.addEventListener("click", () => {
        card.remove();
        refreshMaterialLabels();
      });

      el.materialsList.appendChild(fragment);
      refreshMaterialLabels();
    }

    function refreshMaterialLabels() {
      [...el.materialsList.children].forEach((node, index) => {
        const label = node.querySelector(".material-index");
        const removeBtn = node.querySelector(".remove-btn");
        label.textContent = `\u6750\u6599 ${index + 1}`;
        removeBtn.disabled = el.materialsList.children.length === 1;
      });
    }

    function loadExample() {
      el.userQuery.value = example.user_query;
      el.caseTypeHint.value = example.case_type_hint;
      el.materialsList.innerHTML = "";
      example.materials.forEach(item => createMaterialCard(item));
      setStatus("\u5df2\u52a0\u8f7d\u793a\u4f8b\u6570\u636e\u3002", "good");
    }

    function collectPayload() {
      const materials = [...el.materialsList.children]
        .map(node => ({
          title: node.querySelector('[data-role="title"]').value.trim(),
          content: node.querySelector('[data-role="content"]').value.trim()
        }))
        .filter(item => item.content);

      return {
        user_query: el.userQuery.value.trim(),
        case_type_hint: el.caseTypeHint.value.trim() || null,
        materials
      };
    }

    async function requestJson(url, options) {
      const response = await fetch(url, options);
      const text = await response.text();
      let parsed = null;
      try {
        parsed = text ? JSON.parse(text) : null;
      } catch {
        parsed = { raw: text };
      }
      if (!response.ok) {
        const detail = parsed && parsed.detail ? parsed.detail : text || `HTTP ${response.status}`;
        throw new Error(detail);
      }
      return parsed;
    }

    function renderList(container, items, renderer, emptyText) {
      if (!items || !items.length) {
        container.innerHTML = `<div class="empty">${escapeHtml(emptyText)}</div>`;
        return;
      }
      container.innerHTML = items.map(renderer).join("");
    }

    function renderSimpleList(container, items, emptyText) {
      if (!items || !items.length) {
        container.innerHTML = `<div class="empty">${escapeHtml(emptyText)}</div>`;
        return;
      }
      container.innerHTML = `<ul class="list">${items.map(item => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;
    }

    function renderMeta(data) {
      const items = [
        ["analysis_id", data.analysis_id],
        ["matter_type", data.matter_type],
        ["risk_level", data.risk_level],
        ["confidence", data.confidence]
      ];
      el.reportKpis.innerHTML = items.map(([k, v]) => `
        <div class="meta-box">
          <div class="k">${escapeHtml(k)}</div>
          <div class="v">${escapeHtml(v ?? "-")}</div>
        </div>
      `).join("");
    }

    function renderReport(data) {
      el.emptyState.hidden = true;
      el.reportShell.hidden = false;
      el.analysisIdInput.value = data.analysis_id || "";
      el.reportTitle.textContent = `${data.matter_type || "legal"} \u5206\u6790\u62a5\u544a`;
      el.headlineRisk.textContent = data.risk_level || "medium";
      el.headlineRisk.className = `tag ${escapeHtml(data.risk_level || "medium")}`;
      el.draftOpinion.textContent = data.draft_opinion || "\u6682\u65e0\u521d\u6b65\u610f\u89c1\u3002";
      renderMeta(data);

      renderList(
        el.factsList,
        data.facts,
        (fact, index) => `
          <div class="item">
            <h5>\u4e8b\u5b9e ${index + 1}</h5>
            <p>${escapeHtml(fact)}</p>
          </div>
        `,
        "\u6682\u65e0\u4e8b\u5b9e\u63d0\u53d6\u3002"
      );

      renderSimpleList(el.actionsList, data.suggested_actions, "\u6682\u65e0\u5efa\u8bae\u52a8\u4f5c\u3002");

      renderList(
        el.issuesList,
        data.issues,
        (issue) => `
          <div class="item">
            <h5>${escapeHtml(issue.title || "\u672a\u547d\u540d\u95ee\u9898")}</h5>
            <p>${escapeHtml(issue.analysis || "")}</p>
            <div class="token-row">
              <span class="tag ${escapeHtml(issue.risk_level || "medium")}">${escapeHtml(issue.risk_level || "medium")}</span>
            </div>
          </div>
        `,
        "\u6682\u65e0\u95ee\u9898\u9879\u3002"
      );

      renderList(
        el.basisList,
        data.legal_basis,
        (basis) => `
          <div class="item">
            <h5>${escapeHtml(basis.title || "")}</h5>
            <p>${escapeHtml(basis.excerpt || "")}</p>
            <div class="token-row">
              <span class="token">${escapeHtml(basis.source_type || "source")}</span>
              <span class="token">${escapeHtml(basis.reference_id || "")}</span>
              <span class="token">score: ${escapeHtml(basis.score ?? "-")}</span>
            </div>
          </div>
        `,
        "\u6682\u65e0\u6cd5\u5f8b\u4f9d\u636e\u3002"
      );

      renderSimpleList(el.reviewList, data.review_notes, "\u6682\u65e0\u590d\u6838\u610f\u89c1\u3002");

      renderList(
        el.coordinationList,
        data.coordination_log,
        (entry) => `
          <div class="item">
            <h5>${escapeHtml(entry.sender || "")} → ${escapeHtml(entry.recipient || "")}</h5>
            <p>${escapeHtml(entry.content || "")}</p>
          </div>
        `,
        "\u6682\u65e0\u534f\u8c03\u65e5\u5fd7\u3002"
      );

      renderList(
        el.traceList,
        data.trace,
        (entry) => `
          <div class="item">
            <h5>${escapeHtml(entry.agent_name || "")}</h5>
            <p>${escapeHtml(entry.summary || "")}</p>
          </div>
        `,
        "\u6682\u65e0\u6267\u884c\u8f68\u8ff9\u3002"
      );

      renderList(
        el.debugList,
        data.llm_debug,
        (entry) => `
          <div class="item">
            <h5>${escapeHtml(entry.agent_name || "agent")} · ${escapeHtml(entry.task || "task")}</h5>
            <pre>${escapeHtml(JSON.stringify(entry.output, null, 2))}</pre>
          </div>
        `,
        "\u6682\u65e0 LLM \u8c03\u8bd5\u8f93\u51fa\u3002"
      );

      el.debugMeta.textContent = `${Array.isArray(data.llm_debug) ? data.llm_debug.length : 0} entries`;
      el.rawJson.textContent = JSON.stringify(data, null, 2);
    }

    async function runAnalysis() {
      const payload = collectPayload();
      if (!payload.user_query) {
        setStatus("\u8bf7\u5148\u586b\u5199\u6cd5\u5f8b\u95ee\u9898\u3002", "error");
        return;
      }
      if (!payload.materials.length) {
        setStatus("\u81f3\u5c11\u9700\u8981\u4e00\u4efd\u6709\u5185\u5bb9\u7684\u6750\u6599\u3002", "error");
        return;
      }

      setBusy(true, "\u6b63\u5728\u8fd0\u884c\u591a Agent \u5206\u6790...");
      try {
        const data = await requestJson("/analysis", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        renderReport(data);
        setStatus(`\u5206\u6790\u5b8c\u6210\uff0canalysis_id: ${data.analysis_id}`, "good");
      } catch (error) {
        setStatus(`\u5206\u6790\u5931\u8d25\uff1a${error.message}`, "error");
      } finally {
        setBusy(false);
      }
    }

    async function fetchAnalysis() {
      const analysisId = el.analysisIdInput.value.trim();
      if (!analysisId) {
        setStatus("\u8bf7\u8f93\u5165 analysis_id\u3002", "error");
        return;
      }
      setBusy(true, "\u6b63\u5728\u52a0\u8f7d\u5386\u53f2\u62a5\u544a...");
      try {
        const data = await requestJson(`/analysis/${encodeURIComponent(analysisId)}`, { method: "GET" });
        renderReport(data);
        setStatus(`\u5df2\u53d6\u56de\u62a5\u544a\uff1a${data.analysis_id}`, "good");
      } catch (error) {
        setStatus(`\u52a0\u8f7d\u5931\u8d25\uff1a${error.message}`, "error");
      } finally {
        setBusy(false);
      }
    }

    async function checkHealth() {
      setHealth("\u6b63\u5728\u68c0\u67e5\u670d\u52a1\u72b6\u6001...");
      try {
        const data = await requestJson("/health", { method: "GET" });
        setHealth(`\u670d\u52a1\u6b63\u5e38\uff1a${JSON.stringify(data)}`, "good");
      } catch (error) {
        setHealth(`\u5065\u5eb7\u68c0\u67e5\u5931\u8d25\uff1a${error.message}`, "error");
      }
    }

    function clearReport() {
      el.emptyState.hidden = false;
      el.reportShell.hidden = true;
      el.analysisIdInput.value = "";
      el.rawJson.textContent = "";
      setStatus("\u5df2\u6e05\u7a7a\u7ed3\u679c\u533a\u3002");
    }

    el.addMaterialBtn.addEventListener("click", () => createMaterialCard());
    el.fillBtn.addEventListener("click", loadExample);
    el.clearBtn.addEventListener("click", clearReport);
    el.analyzeBtn.addEventListener("click", runAnalysis);
    el.fetchBtn.addEventListener("click", fetchAnalysis);
    el.healthBtn.addEventListener("click", checkHealth);

    decodeNodeTree(document.body);
    createMaterialCard();
    loadExample();
    checkHealth();
  </script>
</body>
</html>
"""


def render_index() -> HTMLResponse:
    return HTMLResponse(INDEX_HTML)
