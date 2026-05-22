from fastapi.responses import HTMLResponse


INDEX_HTML = """<!doctype html>
<html lang="zh-CN" data-theme="light">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>律智星 · LegalMind</title>
  <style>
    :root {
      --bg: #faf7f2;
      --bg-aside: #f3ede4;
      --bg-chat: #faf7f2;
      --bg-bubble-ai: #f0ebe2;
      --bg-bubble-user: #c06030;
      --bg-input: #ffffff;
      --bg-card: #ffffff;
      --bg-hover: #f0ebe2;
      --text: #2c2418;
      --text-secondary: #8a7e6e;
      --text-muted: #b0a898;
      --text-user: #ffffff;
      --border: #e4dbd0;
      --accent: #c06030;
      --accent-light: rgba(192, 96, 48, 0.1);
      --risk-low: #3d8b37;
      --risk-low-bg: rgba(61, 139, 55, 0.1);
      --risk-med: #c08020;
      --risk-med-bg: rgba(192, 128, 32, 0.12);
      --risk-high: #c03030;
      --risk-high-bg: rgba(192, 48, 48, 0.1);
      --code-bg: #f5f0e8;
      --shadow: 0 1px 3px rgba(80, 50, 20, 0.06);
      --sidebar-w: 240px;
    }
    [data-theme="dark"] {
      --bg: #1a1614;
      --bg-aside: #211d1a;
      --bg-chat: #1a1614;
      --bg-bubble-ai: #2a2420;
      --bg-bubble-user: #c06030;
      --bg-input: #242018;
      --bg-card: #242018;
      --bg-hover: #302a24;
      --text: #e8e0d6;
      --text-secondary: #a09686;
      --text-muted: #706858;
      --text-user: #ffffff;
      --border: #3a3228;
      --accent: #d07040;
      --accent-light: rgba(208, 112, 64, 0.15);
      --code-bg: #1a1a1a;
      --shadow: 0 1px 3px rgba(0,0,0,0.3);
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, "PingFang SC", "Microsoft YaHei", "Segoe UI", sans-serif;
      color: var(--text);
      background: var(--bg);
      height: 100vh;
      overflow: hidden;
      display: flex;
    }

    /* sidebar */
    .sidebar {
      width: var(--sidebar-w);
      min-width: var(--sidebar-w);
      flex-shrink: 0;
      background: var(--bg-aside);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      height: 100vh;
    }
    .sidebar-head {
      padding: 16px;
      border-bottom: 1px solid var(--border);
    }
    .new-chat-btn {
      width: 100%;
      padding: 10px 14px;
      border: 1px solid var(--border);
      border-radius: 10px;
      background: var(--bg-chat);
      color: var(--text);
      font: inherit;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      text-align: left;
    }
    .new-chat-btn:hover { background: var(--bg-hover); }
    .history-list {
      flex: 1;
      overflow-y: auto;
      padding: 8px;
    }
    .history-item {
      padding: 10px 12px;
      border-radius: 8px;
      font-size: 13px;
      color: var(--text-secondary);
      cursor: pointer;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .history-item:hover { background: var(--bg-hover); color: var(--text); }
    .history-item.active { background: var(--accent-light); color: var(--accent); }
    .sidebar-foot {
      padding: 12px 16px;
      border-top: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .sidebar-foot input {
      width: 100%;
      padding: 7px 10px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--bg-input);
      color: var(--text);
      font: inherit;
      font-size: 12px;
      outline: none;
    }
    .sidebar-foot input:focus { border-color: var(--accent); }
    .sidebar-foot-row {
      display: flex;
      gap: 6px;
    }
    .sidebar-foot-row button {
      flex: 1;
      padding: 6px 0;
      border: 1px solid var(--border);
      border-radius: 6px;
      background: var(--bg-chat);
      color: var(--text-secondary);
      font: inherit;
      font-size: 11px;
      cursor: pointer;
    }
    .sidebar-foot-row button:hover { background: var(--bg-hover); color: var(--text); }
    .health-dot {
      width: 6px; height: 6px;
      border-radius: 999px;
      display: inline-block;
      margin-right: 4px;
      vertical-align: middle;
      background: #888;
    }
    .health-dot.ok { background: #22c55e; }
    .health-dot.err { background: #ef4444; }

    /* main */
    .main {
      flex: 1;
      display: flex;
      flex-direction: column;
      height: 100vh;
      min-width: 0;
    }
    .main-head {
      padding: 12px 20px;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--bg-chat);
    }
    .main-head h2 { font-size: 15px; font-weight: 600; }
    .theme-btn {
      width: 32px; height: 32px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--bg-chat);
      color: var(--text-secondary);
      font-size: 16px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .theme-btn:hover { background: var(--bg-hover); }
    .menu-btn {
      display: none;
      width: 32px; height: 32px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--bg-chat);
      color: var(--text-secondary);
      font-size: 18px;
      cursor: pointer;
      align-items: center;
      justify-content: center;
    }

    /* chat area */
    .chat-area {
      flex: 1;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
    }
    .chat-scroll {
      flex: 1;
      overflow-y: auto;
      padding: 24px 0;
    }
    .chat-container {
      max-width: 900px;
      margin: 0 auto;
      padding: 0 16px;
      display: flex;
      flex-direction: column;
      gap: 24px;
    }

    /* welcome */
    .welcome {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 60vh;
      text-align: center;
      padding: 40px 20px;
    }
    .welcome h1 {
      font-size: 28px;
      font-weight: 700;
      margin-bottom: 8px;
      letter-spacing: -0.02em;
    }
    .welcome p {
      color: var(--text-secondary);
      font-size: 14px;
      margin-bottom: 32px;
      max-width: 420px;
      line-height: 1.6;
    }
    .quick-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      max-width: 520px;
      width: 100%;
    }
    .quick-card {
      padding: 14px 16px;
      border: 1px solid var(--border);
      border-radius: 12px;
      background: var(--bg-card);
      text-align: left;
      cursor: pointer;
      font: inherit;
      color: var(--text);
    }
    .quick-card:hover { border-color: var(--accent); }
    .quick-card .qc-title { font-size: 13px; font-weight: 600; margin-bottom: 4px; }
    .quick-card .qc-desc { font-size: 12px; color: var(--text-secondary); line-height: 1.4; }

    /* messages */
    .msg { display: flex; gap: 12px; }
    .msg.user { flex-direction: row-reverse; }
    .msg-avatar {
      width: 36px; height: 36px;
      border-radius: 50%;
      flex-shrink: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 15px;
      font-weight: 700;
    }
    .msg.user .msg-avatar {
      background: linear-gradient(135deg, #e8d5c4, #d4b896);
      color: #6b4a2e;
      font-size: 16px;
    }
    .msg.ai .msg-avatar {
      background: linear-gradient(135deg, var(--accent), #a04820);
      color: #fff;
      font-size: 18px;
    }
    .msg-body { max-width: 820px; min-width: 0; }
    .msg.user .msg-body { text-align: right; }
    .msg-bubble {
      display: inline-block;
      padding: 12px 16px;
      border-radius: 14px;
      font-size: 14px;
      line-height: 1.7;
      text-align: left;
    }
    .msg.user .msg-bubble {
      background: var(--bg-bubble-user);
      color: var(--text-user);
      border-radius: 14px 14px 4px 14px;
    }
    .msg.ai .msg-bubble {
      background: var(--bg-bubble-ai);
      color: var(--text);
      border-radius: 14px 14px 14px 4px;
      width: 100%;
    }

    /* report cards inside ai bubble */
    .report-section {
      border: 1px solid var(--border);
      border-radius: 10px;
      margin-top: 10px;
      overflow: hidden;
    }
    .report-section:first-child { margin-top: 0; }
    .rs-head {
      padding: 10px 14px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--bg-card);
      user-select: none;
    }
    .rs-head:hover { background: var(--bg-hover); }
    .rs-head::after {
      content: "";
      width: 0; height: 0;
      border-left: 4px solid transparent;
      border-right: 4px solid transparent;
      border-top: 5px solid var(--text-secondary);
      flex-shrink: 0;
      margin-left: 8px;
    }
    .rs-head.open::after { border-top: none; border-bottom: 5px solid var(--text-secondary); }
    .rs-body {
      padding: 0 14px;
      max-height: 0;
      overflow: hidden;
      transition: max-height 0.25s ease, padding 0.25s ease;
    }
    .rs-body.open {
      max-height: 2000px;
      padding: 12px 14px;
    }
    .rs-body p, .rs-body li {
      font-size: 13px;
      line-height: 1.7;
      color: var(--text-secondary);
    }
    .rs-body ul { padding-left: 18px; }
    .rs-body li + li { margin-top: 4px; }

    /* opinion block */
    .opinion-block {
      padding: 14px 16px;
      background: linear-gradient(135deg, #8b4513, #a0522d);
      border-radius: 10px;
      color: #fdf5e6;
      margin-bottom: 10px;
    }
    [data-theme="dark"] .opinion-block {
      background: linear-gradient(135deg, #5c2e0e, #7a3b14);
    }
    .opinion-block .ob-head {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 10px;
      flex-wrap: wrap;
    }
    .opinion-block .ob-title { font-size: 14px; font-weight: 700; }
    .opinion-block .ob-text { font-size: 13px; line-height: 1.8; white-space: pre-wrap; }

    /* tags */
    .tag {
      display: inline-flex;
      padding: 2px 8px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
    }
    .tag.low { background: var(--risk-low-bg); color: var(--risk-low); }
    .tag.medium { background: var(--risk-med-bg); color: var(--risk-med); }
    .tag.high { background: var(--risk-high-bg); color: var(--risk-high); }
    .tag.on-dark { background: rgba(255,255,255,0.18); color: #fdf5e6; }
    .tag.matter-contract { background: rgba(59,130,246,0.2); color: #2563eb; }
    .tag.matter-labor { background: rgba(234,88,12,0.2); color: #ea580c; }
    .tag.matter-compliance { background: rgba(16,185,129,0.2); color: #059669; }
    .tag.matter-litigation { background: rgba(139,92,246,0.2); color: #7c3aed; }
    .tag.matter-general { background: rgba(107,114,128,0.2); color: #4b5563; }
    [data-theme="dark"] .tag.matter-contract { background: rgba(59,130,246,0.25); color: #60a5fa; }
    [data-theme="dark"] .tag.matter-labor { background: rgba(234,88,12,0.25); color: #fb923c; }
    [data-theme="dark"] .tag.matter-compliance { background: rgba(16,185,129,0.25); color: #34d399; }
    [data-theme="dark"] .tag.matter-litigation { background: rgba(139,92,246,0.25); color: #a78bfa; }
    [data-theme="dark"] .tag.matter-general { background: rgba(107,114,128,0.25); color: #9ca3af; }

    /* issue / basis items */
    .analysis-item {
      padding: 10px 12px;
      border: 1px solid var(--border);
      border-radius: 8px;
      margin-top: 8px;
    }
    .analysis-item:first-child { margin-top: 0; }
    .analysis-item h4 { font-size: 13px; font-weight: 600; margin-bottom: 4px; }
    .analysis-item p { font-size: 13px; color: var(--text-secondary); line-height: 1.6; }
    .analysis-item .ai-meta { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 6px; }
    .analysis-item .ai-token {
      font-size: 11px;
      font-family: "JetBrains Mono", Consolas, monospace;
      padding: 2px 6px;
      border-radius: 4px;
      background: var(--accent-light);
      color: var(--accent);
    }

    /* raw json */
    .raw-toggle {
      margin-top: 10px;
      font-size: 12px;
      color: var(--text-secondary);
      cursor: pointer;
      border: none;
      background: none;
      font: inherit;
      padding: 4px 0;
    }
    .raw-toggle:hover { color: var(--accent); }
    .raw-json {
      display: none;
      margin-top: 8px;
      padding: 12px;
      border-radius: 8px;
      background: var(--code-bg);
      overflow: auto;
      max-height: 300px;
    }
    .raw-json pre {
      font-family: "JetBrains Mono", Consolas, monospace;
      font-size: 11px;
      line-height: 1.5;
      white-space: pre-wrap;
      word-break: break-all;
      color: var(--text-secondary);
    }

    /* loading */
    .msg-loading .msg-bubble {
      display: flex;
      gap: 4px;
      padding: 16px 20px;
    }
    .msg-loading .dot {
      width: 6px; height: 6px;
      border-radius: 999px;
      background: var(--text-secondary);
      animation: dotBounce 1.4s ease-in-out infinite;
    }
    .msg-loading .dot:nth-child(2) { animation-delay: 0.2s; }
    .msg-loading .dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes dotBounce {
      0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
      40% { transform: scale(1); opacity: 1; }
    }

    /* streaming status bar */
    .st-status {
      display: flex !important;
      align-items: center;
      gap: 8px;
      padding: 10px 14px !important;
      margin-top: 8px;
      border-radius: 8px;
      background: var(--accent-light);
      font-size: 13px;
      color: var(--accent) !important;
      transition: all 0.3s ease;
    }
    .st-spinner {
      width: 14px; height: 14px;
      border: 2px solid var(--border);
      border-top-color: var(--accent);
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
      flex-shrink: 0;
    }
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
    .st-status .st-dot-bar {
      display: inline-flex;
      gap: 3px;
      margin-left: 2px;
    }
    .st-status .st-dot-bar span {
      width: 4px; height: 4px;
      border-radius: 999px;
      background: var(--accent);
      animation: dotPulse 1.4s ease-in-out infinite;
    }
    .st-status .st-dot-bar span:nth-child(2) { animation-delay: 0.2s; }
    .st-status .st-dot-bar span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes dotPulse {
      0%, 80%, 100% { transform: scale(0.5); opacity: 0.3; }
      40% { transform: scale(1.2); opacity: 1; }
    }

    /* input bar */
    .input-bar {
      padding: 14px 16px;
      border-top: 1px solid var(--border);
      background: var(--bg-chat);
    }
    .input-inner {
      max-width: 900px;
      margin: 0 auto;
      display: flex;
      gap: 10px;
      align-items: flex-end;
    }
    .input-inner textarea {
      flex: 1;
      padding: 11px 14px;
      border: 1px solid var(--border);
      border-radius: 12px;
      background: var(--bg-input);
      color: var(--text);
      font: inherit;
      font-size: 14px;
      outline: none;
      resize: none;
      min-height: 44px;
      max-height: 140px;
      line-height: 1.5;
    }
    .input-inner textarea:focus { border-color: var(--accent); }
    .send-btn {
      width: 44px; height: 44px;
      border: none;
      border-radius: 12px;
      background: var(--accent);
      color: #fff;
      font-size: 18px;
      cursor: pointer;
      flex-shrink: 0;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .send-btn:hover { opacity: 0.9; }
    .send-btn:disabled { opacity: 0.4; cursor: default; }
    .send-btn.cancel { background: var(--risk-high); }

    .copy-btn {
      margin-top: 10px;
      padding: 6px 12px;
      border: 1px solid var(--border);
      border-radius: 6px;
      background: var(--bg-card);
      color: var(--text-secondary);
      font: inherit;
      font-size: 12px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }
    .copy-btn:hover { background: var(--bg-hover); color: var(--text); }
    .copy-btn.copied { color: var(--risk-low); border-color: var(--risk-low); }

    .feedback-bar {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      margin-left: 4px;
    }
    .fb-btn {
      width: 30px; height: 30px;
      border: 1px solid var(--border);
      border-radius: 6px;
      background: var(--bg-card);
      color: var(--text-secondary);
      font-size: 14px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.15s;
    }
    .fb-btn:hover { background: var(--bg-hover); color: var(--text); }
    .fb-btn.active-up { background: var(--risk-low-bg); border-color: var(--risk-low); color: var(--risk-low); }
    .fb-btn.active-down { background: var(--risk-high-bg); border-color: var(--risk-high); color: var(--risk-high); }
    .fb-btn:disabled { opacity: 0.5; cursor: default; }
    .fb-thanks {
      font-size: 12px;
      color: var(--risk-low);
      display: none;
      margin-left: 4px;
    }

    /* scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

    /* mobile */
    .sidebar-overlay {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.4);
      z-index: 99;
    }
    @media (max-width: 768px) {
      .sidebar {
        position: fixed;
        left: -100%;
        top: 0;
        bottom: 0;
        z-index: 100;
        transition: left 0.2s;
      }
      .sidebar.open { left: 0; }
      .sidebar-overlay.open { display: block; }
      .menu-btn { display: flex; }
      .quick-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>

  <aside class="sidebar" id="sidebar">
    <div class="sidebar-head">
      <button class="new-chat-btn" id="newChatBtn">+ 新建对话</button>
    </div>
    <div class="history-list" id="historyList"></div>
    <div class="sidebar-foot">
      <input id="historyId" placeholder="输入 report_id 回查..." />
      <div class="sidebar-foot-row">
        <button id="historyBtn">加载报告</button>
        <button id="healthBtn"><span id="healthDot" class="health-dot"></span>检查状态</button>
      </div>
    </div>
  </aside>
  <div class="sidebar-overlay" id="sidebarOverlay"></div>

  <div class="main">
    <div class="main-head">
      <div style="display:flex;align-items:center;gap:8px;">
        <button class="menu-btn" id="menuBtn">☰</button>
        <h2>律智星 · LegalMind</h2>
      </div>
      <button class="theme-btn" id="themeBtn" title="切换主题">☾</button>
    </div>

    <div class="chat-area">
      <div class="chat-scroll" id="chatScroll">
        <div class="chat-container" id="chatContainer">
          <div id="welcome" class="welcome">
            <h1>律智星</h1>
            <p style="font-size:13px;color:var(--text-secondary);margin-bottom:4px;">LegalMind · 法律智能分析助手</p>
            <p>输入您遇到的法律问题，系统将自动分析风险、检索相关法条并提供初步建议。</p>
            <div class="quick-grid">
              <button class="quick-card" data-q="合同违约金约定过高，可以要求法院调减吗？" data-label="合同纠纷">
                <div class="qc-title">违约金过高怎么办？</div>
                <div class="qc-desc">了解违约金调减的法律依据和适用条件</div>
              </button>
              <button class="quick-card" data-q="公司单方面解除劳动合同，员工可以获得多少经济补偿？" data-label="劳动争议">
                <div class="qc-title">劳动解除补偿</div>
                <div class="qc-desc">计算经济补偿金的法定标准</div>
              </button>
              <button class="quick-card" data-q="合同中约定的解除条件不明确，一方想解除合同应该怎么做？" data-label="合同纠纷">
                <div class="qc-title">合同解除条件</div>
                <div class="qc-desc">解除权的行使条件和程序要求</div>
              </button>
              <button class="quick-card" data-q="企业未给员工缴纳社会保险，员工可以主张哪些权利？" data-label="合规审查">
                <div class="qc-title">社保权益维护</div>
                <div class="qc-desc">未缴社保的法律后果和维权途径</div>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="input-bar">
      <div class="input-inner">
        <textarea id="queryInput" rows="1" placeholder="描述您遇到的法律问题..."></textarea>
        <button class="send-btn" id="sendBtn" title="发送">↑</button>
      </div>
    </div>
  </div>

  <script>
    var $ = function(id) { return document.getElementById(id); };
    var el = {
      sidebar: $("sidebar"), overlay: $("sidebarOverlay"),
      menuBtn: $("menuBtn"), newChatBtn: $("newChatBtn"),
      historyList: $("historyList"), historyId: $("historyId"),
      historyBtn: $("historyBtn"), healthDot: $("healthDot"),
      healthBtn: $("healthBtn"), themeBtn: $("themeBtn"),
      chatScroll: $("chatScroll"), chatContainer: $("chatContainer"),
      welcome: $("welcome"), queryInput: $("queryInput"), sendBtn: $("sendBtn")
    };

    var sessions = [];
    var currentSession = null;
    var activeController = null;

    function esc(v) {
      return String(v == null ? "" : v).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
    }

    // theme
    function getTheme() { return localStorage.getItem("theme") || "light"; }
    function setTheme(t) {
      document.documentElement.setAttribute("data-theme", t);
      localStorage.setItem("theme", t);
      el.themeBtn.textContent = t === "dark" ? "☀" : "☾";
    }
    setTheme(getTheme());
    el.themeBtn.addEventListener("click", function() {
      setTheme(getTheme() === "dark" ? "light" : "dark");
    });

    // sidebar
    function toggleSidebar(open) {
      var isOpen = el.sidebar.classList.contains("open");
      var next = open !== undefined ? open : !isOpen;
      el.sidebar.classList.toggle("open", next);
      el.overlay.classList.toggle("open", next);
    }
    el.menuBtn.addEventListener("click", function() { toggleSidebar(); });
    el.overlay.addEventListener("click", function() { toggleSidebar(false); });

    // history
    function loadSessions() {
      try { sessions = JSON.parse(localStorage.getItem("legal_sessions") || "[]"); } catch(e) { sessions = []; }
    }
    function saveSessions() {
      localStorage.setItem("legal_sessions", JSON.stringify(sessions.slice(0, 30)));
    }
    var matterLabels = {
      contract_review: "合同纠纷", labor_dispute: "劳动争议",
      compliance_review: "合规审查", litigation_strategy: "诉讼策略",
      general_legal_consultation: "法律咨询"
    };
    function matterTag(matterType) {
      var key = matterType || "general_legal_consultation";
      var label = matterLabels[key] || key;
      var cls = "matter-" + (key.split("_")[0] || "general");
      return '<span class="tag ' + cls + '">' + esc(label) + '</span>';
    }

    function formatTime(ts) {
      if (!ts) return "";
      var d = new Date(ts);
      var pad = function(n) { return n < 10 ? "0" + n : "" + n; };
      return pad(d.getMonth()+1) + "/" + pad(d.getDate()) + " " + pad(d.getHours()) + ":" + pad(d.getMinutes());
    }

    function renderHistory() {
      el.historyList.innerHTML = sessions.map(function(s, i) {
        var cls = currentSession === i ? " active" : "";
        var time = s.createdAt ? '<span style="float:right;font-size:11px;opacity:0.6">' + formatTime(s.createdAt) + '</span>' : "";
        return '<div class="history-item' + cls + '" data-i="' + i + '">' + esc(s.title) + time + '</div>';
      }).join("");
      el.historyList.querySelectorAll(".history-item").forEach(function(item) {
        item.addEventListener("click", function() {
          switchSession(parseInt(item.getAttribute("data-i")));
        });
      });
    }
    function switchSession(index) {
      currentSession = index;
      var s = sessions[index];
      el.welcome.style.display = "none";
      el.chatContainer.innerHTML = "";
      s.messages.forEach(function(m) {
        if (m.role === "user") appendUserMsg(m.text, false);
        else appendAiMsg(m.data, false);
      });
      renderHistory();
      toggleSidebar(false);
      scrollToBottom();
    }
    function startNewChat() {
      currentSession = null;
      el.chatContainer.innerHTML = "";
      el.welcome.style.display = "";
      el.chatContainer.appendChild(el.welcome);
      renderHistory();
      toggleSidebar(false);
    }
    el.newChatBtn.addEventListener("click", startNewChat);

    // health
    async function checkHealth() {
      try {
        await fetch("/health").then(function(r) { return r.json(); });
        el.healthDot.className = "health-dot ok";
      } catch(e) {
        el.healthDot.className = "health-dot err";
      }
    }
    el.healthBtn.addEventListener("click", checkHealth);

    // report fetch
    el.historyBtn.addEventListener("click", async function() {
      var id = el.historyId.value.trim();
      if (!id) return;
      el.historyBtn.disabled = true;
      try {
        var resp = await fetch("/analysis/" + encodeURIComponent(id));
        if (!resp.ok) throw new Error((await resp.json()).detail || resp.statusText);
        var data = await resp.json();
        if (currentSession === null) {
          sessions.unshift({ title: "[回查] " + id.slice(0,8), messages: [], createdAt: Date.now() });
          currentSession = 0;
          el.welcome.style.display = "none";
          el.chatContainer.innerHTML = "";
        }
        appendAiMsg(data, true);
        saveSessions();
        renderHistory();
      } catch(e) { alert("加载失败：" + e.message); }
      finally { el.historyBtn.disabled = false; }
    });

    // textarea auto-height
    function setTextareaHeight() {
      el.queryInput.style.height = "auto";
      el.queryInput.style.height = Math.min(el.queryInput.scrollHeight, 140) + "px";
    }
    el.queryInput.addEventListener("input", setTextareaHeight);

    // send
    function appendUserMsg(text, save) {
      var div = document.createElement("div");
      div.className = "msg user";
      div.innerHTML = '<div class="msg-avatar">你</div><div class="msg-body"><div class="msg-bubble">' + esc(text) + '</div></div>';
      el.chatContainer.appendChild(div);
      if (save !== false && currentSession !== null) {
        sessions[currentSession].messages.push({ role: "user", text: text });
      }
    }

    function appendAiMsg(data, save) {
      var div = document.createElement("div");
      div.className = "msg ai";

      var opinionBlock = "";
      if (data.draft_opinion) {
        opinionBlock = '<div class="opinion-block"><div class="ob-head">' +
          '<span class="ob-title">法律意见书</span>' +
          '<span class="tag on-dark">' + esc(data.risk_level || "medium") + '</span>' +
          '<span class="tag on-dark">置信度: ' + esc(data.confidence || "-") + '</span>' +
          matterTag(data.matter_type) +
          '</div><div class="ob-text">' + formatOpinion(data.draft_opinion) + '</div></div>';
      }

      var sections = [];

      if (data.facts && data.facts.length) {
        sections.push(buildSection("关键事实 (" + data.facts.length + "项)", data.facts.map(function(f, i) {
          return '<li>' + esc(f) + '</li>';
        }).join(""), false));
      }

      if (data.issues && data.issues.length) {
        var items = data.issues.map(buildIssueItem).join("");
        sections.push(buildSection("风险分析 (" + data.issues.length + "项)", items, false));
      }

      if (data.suggested_actions && data.suggested_actions.length) {
        sections.push(buildSection("建议措施", data.suggested_actions.map(function(a) {
          return '<li>' + esc(a) + '</li>';
        }).join(""), false));
      }

      if (data.legal_basis && data.legal_basis.length) {
        var items = data.legal_basis.map(function(b) {
          return '<div class="analysis-item"><h4>' + esc(b.title || "") + '</h4><p>' + esc(b.excerpt || "") + '</p><div class="ai-meta"><span class="ai-token">' + esc(b.source_type || "") + '</span><span class="ai-token">' + esc(b.reference_id || "") + '</span>' + (b.score != null ? '<span class="ai-token">score: ' + esc(b.score) + '</span>' : '') + '</div></div>';
        }).join("");
        sections.push(buildSection("法律依据", items, false));
      }

      if (data.review_notes && data.review_notes.length) {
        sections.push(buildSection("复核意见", data.review_notes.map(function(n) {
          return '<li>' + esc(n) + '</li>';
        }).join(""), false));
      }

      var errorBlock = "";
      if (data.agent_errors && data.agent_errors.length) {
        errorBlock = data.agent_errors.map(function(e) {
          return '<div style="padding:6px 10px;margin:6px 0;border-radius:6px;background:var(--risk-high-bg);color:var(--risk-high);font-size:12px">' +
            esc(e.agent_name) + ' 步骤异常: ' + esc(e.message) + '</div>';
        }).join("");
      }

      var rawId = "raw_" + Date.now();
      var fbUpId = "fb_up_" + Date.now();
      var fbDownId = "fb_down_" + Date.now();
      var fbThanksId = "fb_thanks_" + Date.now();
      var rawBlock = '<div style="display:flex;gap:8px;align-items:center;margin-top:10px">' +
        '<div class="feedback-bar">' +
        '<button class="fb-btn" id="' + fbUpId + '" title="有帮助">👍</button>' +
        '<button class="fb-btn" id="' + fbDownId + '" title="没帮助">👎</button>' +
        '<span class="fb-thanks" id="' + fbThanksId + '">感谢反馈</span>' +
        '</div>' +
        '<button class="raw-toggle" data-raw="' + rawId + '">查看原始 JSON</button></div>' +
        '<div class="raw-json" id="' + rawId + '"><pre>' + esc(JSON.stringify(data, null, 2)) + '</pre></div>';

      div.innerHTML = '<div class="msg-avatar">⚖</div><div class="msg-body"><div class="msg-bubble">' +
        errorBlock + opinionBlock + sections.join("") + rawBlock + '</div></div>';
      el.chatContainer.appendChild(div);

      if (save !== false && currentSession !== null) {
        sessions[currentSession].messages.push({ role: "ai", data: data });
        saveSessions();
      }

      var fbUp = document.getElementById(fbUpId);
      var fbDown = document.getElementById(fbDownId);
      var fbThanks = document.getElementById(fbThanksId);
      function sendFeedback(value, clickedBtn, otherBtn) {
        fetch("/feedback", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ analysis_id: data.analysis_id, value: value })
        }).then(function() {
          clickedBtn.classList.add(value > 0 ? "active-up" : "active-down");
          clickedBtn.disabled = true;
          otherBtn.disabled = true;
          if (fbThanks) fbThanks.style.display = "inline";
        });
      }
      if (fbUp) fbUp.addEventListener("click", function() { sendFeedback(1, fbUp, fbDown); });
      if (fbDown) fbDown.addEventListener("click", function() { sendFeedback(0, fbDown, fbUp); });
    }

    function buildSection(title, bodyHtml, defaultOpen) {
      var openCls = defaultOpen ? " open" : "";
      return '<div class="report-section"><div class="rs-head' + openCls + '">' + esc(title) + '</div><div class="rs-body' + openCls + '">' + (bodyHtml.indexOf("<li>") === 0 ? '<ul>' + bodyHtml + '</ul>' : bodyHtml) + '</div></div>';
    }

    function stripMd(s) {
      return s.replace(/\*\*/g, "").replace(/__([^_]+)__/g, "$1").replace(/`([^`]+)`/g, "$1");
    }

    function formatOpinion(text) {
      if (!text) return "";
      var lines = text.split("\\n");
      var html = "";
      var inList = false;
      for (var i = 0; i < lines.length; i++) {
        var line = lines[i].trim();
        if (!line || /^---+$/.test(line)) {
          if (inList) { html += "</ul>"; inList = false; }
          continue;
        }
        line = stripMd(line);
        if (/^#{1,3}\s+/.test(line)) {
          if (inList) { html += "</ul>"; inList = false; }
          html += '<div style="font-weight:700;font-size:13px;margin:12px 0 4px;color:inherit">' + esc(line.replace(/^#{1,3}\s+/, "")) + '</div>';
        } else if (/^(一|二|三|四|五|六|七|八|九|十|【|[一二三四五六七八九十]+[、.])[）)]/.test(line) ||
            /^(案情概述|法律分析|风险提示|行动建议|结论|建议|总结)/.test(line)) {
          if (inList) { html += "</ul>"; inList = false; }
          html += '<div style="font-weight:700;font-size:13px;margin:12px 0 4px;color:inherit">' + esc(line) + '</div>';
        } else if (/^[•·\-]\s|^\d+[.、)）]/.test(line)) {
          if (!inList) { html += '<ul style="padding-left:18px;margin:4px 0">'; inList = true; }
          html += '<li style="font-size:13px;line-height:1.8;color:inherit;margin:2px 0">' + esc(line.replace(/^[•·\-]\s|^\d+[.、)）]\s*/, "")) + '</li>';
        } else if (/^⚠️/.test(line)) {
          if (inList) { html += "</ul>"; inList = false; }
          html += '<div style="padding:6px 10px;margin:6px 0;border-radius:6px;background:rgba(255,200,0,0.15);font-size:13px;line-height:1.7">' + esc(line) + '</div>';
        } else {
          if (inList) { html += "</ul>"; inList = false; }
          html += '<p style="font-size:13px;line-height:1.8;margin:4px 0;color:inherit">' + esc(line) + '</p>';
        }
      }
      if (inList) html += "</ul>";
      return html;
    }

    function buildIssueItem(iss) {
      var html = '<div class="analysis-item"><h4>' + esc(iss.title || "未命名风险") + '</h4><p>' + esc(iss.analysis || "") + '</p>';
      if (iss.citations && iss.citations.length) {
        html += '<div class="ai-meta" style="margin-top:8px">';
        iss.citations.forEach(function(c) {
          html += '<span class="ai-token" title="' + esc(c.excerpt || "") + '">' + esc(c.title || c.reference_id || "") + '</span>';
        });
        html += '</div>';
      }
      html += '<div class="ai-meta"><span class="tag ' + esc(iss.risk_level || "medium") + '">' + esc(iss.risk_level || "medium") + '</span></div></div>';
      return html;
    }

    // toggle sections + raw json
    document.addEventListener("click", function(e) {
      if (e.target.classList.contains("rs-head")) {
        e.target.classList.toggle("open");
        e.target.nextElementSibling.classList.toggle("open");
      }
      if (e.target.classList.contains("raw-toggle")) {
        var rawEl = document.getElementById(e.target.getAttribute("data-raw"));
        if (rawEl) rawEl.style.display = rawEl.style.display === "block" ? "none" : "block";
      }
    });

    function scrollToBottom() {
      el.chatScroll.scrollTop = el.chatScroll.scrollHeight;
    }
    function scrollToLatestAiMsg() {
      var msgs = el.chatContainer.querySelectorAll(".msg.ai");
      if (msgs.length) {
        var last = msgs[msgs.length - 1];
        el.chatScroll.scrollTop = last.offsetTop - el.chatContainer.offsetTop;
      }
    }

    // Streaming: create empty bubble with placeholder sections
    function createStreamingBubble() {
      var uid = "s" + Date.now();
      var div = document.createElement("div");
      div.className = "msg ai";
      div.setAttribute("data-stream-id", uid);
      div.innerHTML = '<div class="msg-avatar">⚖</div><div class="msg-body"><div class="msg-bubble">' +
        '<div class="st-matter ' + uid + '"></div>' +
        '<div class="st-opinion ' + uid + '"></div>' +
        '<div class="st-facts ' + uid + '"></div>' +
        '<div class="st-issues ' + uid + '"></div>' +
        '<div class="st-actions ' + uid + '"></div>' +
        '<div class="st-basis ' + uid + '"></div>' +
        '<div class="st-review ' + uid + '"></div>' +
        '<div class="st-status ' + uid + '">' +
          '<span class="st-spinner"></span>' +
          ' <span class="st-status-text ' + uid + '">正在分析</span>' +
          '<span class="st-dot-bar"><span></span><span></span><span></span></span></div>' +
        '</div></div>';
      el.chatContainer.appendChild(div);
      scrollToBottom();
      return { el: div, uid: uid, matter: "general_legal_consultation" };
    }

    // Streaming: update a stage as it arrives
    function renderStage(ctx, agent, data) {
      var c = ctx.el, u = ctx.uid;
      var statusText = c.querySelector(".st-status-text." + u);

      if (data.error) {
        var errHtml = '<div style="padding:6px 10px;margin:6px 0;border-radius:6px;background:var(--risk-high-bg);color:var(--risk-high);font-size:12px">' +
          esc(data.error.agent_name) + ' 步骤异常: ' + esc(data.error.message) + '</div>';
        var errTarget = c.querySelector(".st-status." + u);
        if (errTarget) errTarget.insertAdjacentHTML("beforebegin", errHtml);
      }

      if (agent === "intake_agent") {
        ctx.matter = data.matter_type || "general_legal_consultation";
        var el2 = c.querySelector(".st-matter." + u);
        if (el2) el2.innerHTML = '<div style="margin-bottom:8px">' + matterTag(ctx.matter) + '</div>';
        if (statusText) statusText.textContent = "分类完成，提取事实中";

      } else if (agent === "fact_extraction_agent") {
        var el2 = c.querySelector(".st-facts." + u);
        if (el2 && data.facts && data.facts.length) {
          el2.innerHTML = buildSection("关键事实 (" + data.facts.length + "项)", data.facts.map(function(f) {
            return '<li>' + esc(f) + '</li>';
          }).join(""), false);
        }
        if (statusText) statusText.textContent = "事实提取完成，检索法条中";

      } else if (agent === "legal_retrieval_agent") {
        var el2 = c.querySelector(".st-basis." + u);
        if (el2 && data.legal_basis && data.legal_basis.length) {
          var items = data.legal_basis.map(function(b) {
            return '<div class="analysis-item"><h4>' + esc(b.title || "") + '</h4><p>' + esc(b.excerpt || "") + '</p><div class="ai-meta"><span class="ai-token">' + esc(b.source_type || "") + '</span><span class="ai-token">' + esc(b.reference_id || "") + '</span>' + (b.score != null ? '<span class="ai-token">score: ' + esc(b.score) + '</span>' : '') + '</div></div>';
          }).join("");
          el2.innerHTML = buildSection("法律依据", items, false);
        }
        if (statusText) statusText.textContent = "法条检索完成，生成分析中";

      } else if (agent === "legal_reasoning_agent") {
        var opEl = c.querySelector(".st-opinion." + u);
        if (opEl && data.draft_opinion) {
          opEl.innerHTML = '<div class="opinion-block"><div class="ob-head">' +
            '<span class="ob-title">法律意见书</span>' +
            '<span class="tag on-dark">' + esc(data.risk_level || "medium") + '</span>' +
            matterTag(ctx.matter) +
            '</div><div class="ob-text">' + formatOpinion(data.draft_opinion) + '</div></div>';
        }
        var issEl = c.querySelector(".st-issues." + u);
        if (issEl && data.issues && data.issues.length) {
          var items = data.issues.map(buildIssueItem).join("");
          issEl.innerHTML = buildSection("风险分析 (" + data.issues.length + "项)", items, false);
        }
        var actEl = c.querySelector(".st-actions." + u);
        if (actEl && data.suggested_actions && data.suggested_actions.length) {
          actEl.innerHTML = buildSection("建议措施", data.suggested_actions.map(function(a) {
            return '<li>' + esc(a) + '</li>';
          }).join(""), false);
        }
        if (statusText) statusText.textContent = "分析完成，复核中";

      } else if (agent === "review_agent") {
        var el2 = c.querySelector(".st-review." + u);
        if (el2 && data.review_notes && data.review_notes.length) {
          el2.innerHTML = buildSection("复核意见", data.review_notes.map(function(n) {
            return '<li>' + esc(n) + '</li>';
          }).join(""), false);
        }
        if (data.confidence) {
          var opHead = c.querySelector(".ob-head");
          if (opHead) {
            opHead.innerHTML += '<span class="tag on-dark">置信度: ' + esc(data.confidence) + '</span>';
          }
        }
        if (statusText) {
          statusText.textContent = "分析完成";
          var spinner = c.querySelector(".st-spinner." + u) || c.querySelector(".st-status." + u + " .st-spinner");
          if (spinner) { spinner.style.border = "none"; spinner.textContent = "✓"; spinner.style.animation = "none"; spinner.style.color = "var(--risk-low)"; spinner.style.fontSize = "14px"; spinner.style.width = "auto"; spinner.style.height = "auto"; }
          var dotBar = c.querySelector(".st-status." + u + " .st-dot-bar");
          if (dotBar) dotBar.remove();
          var status = c.querySelector(".st-status." + u);
          if (status) { status.style.background = "var(--risk-low-bg)"; status.style.color = "var(--risk-low)"; }
        }
      }
      scrollToLatestAiMsg();
    }

    // Streaming: finalize with raw JSON and save
    function finalizeStreamingMsg(ctx, fullData) {
      var c = ctx.el, u = ctx.uid;
      var st = c.querySelector(".st-status." + u);
      if (st) st.remove();

      var copyId = "copy_" + Date.now();
      var rawId = "raw_" + Date.now();
      var fbUpId = "fb_up_" + Date.now();
      var fbDownId = "fb_down_" + Date.now();
      var fbThanksId = "fb_thanks_" + Date.now();
      var footerHtml = '<div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:10px">' +
        '<button class="copy-btn" id="' + copyId + '" data-copy="' + copyId + '">复制分析结果</button>' +
        '<div class="feedback-bar">' +
        '<button class="fb-btn" id="' + fbUpId + '" title="有帮助">👍</button>' +
        '<button class="fb-btn" id="' + fbDownId + '" title="没帮助">👎</button>' +
        '<span class="fb-thanks" id="' + fbThanksId + '">感谢反馈</span>' +
        '</div>' +
        '<button class="raw-toggle" data-raw="' + rawId + '">查看原始 JSON</button></div>' +
        '<div class="raw-json" id="' + rawId + '"><pre>' + esc(JSON.stringify(fullData, null, 2)) + '</pre></div>';
      var bubble = c.querySelector(".msg-bubble");
      if (bubble) bubble.insertAdjacentHTML("beforeend", footerHtml);

      var copyBtn = document.getElementById(copyId);
      if (copyBtn) {
        copyBtn.addEventListener("click", function() {
          var text = buildCopyText(fullData);
          navigator.clipboard.writeText(text).then(function() {
            copyBtn.textContent = "已复制";
            copyBtn.classList.add("copied");
            setTimeout(function() {
              copyBtn.textContent = "复制分析结果";
              copyBtn.classList.remove("copied");
            }, 2000);
          });
        });
      }

      var fbUp = document.getElementById(fbUpId);
      var fbDown = document.getElementById(fbDownId);
      var fbThanks = document.getElementById(fbThanksId);
      function sendFeedback(value, clickedBtn, otherBtn) {
        fetch("/feedback", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ analysis_id: fullData.analysis_id, value: value })
        }).then(function() {
          clickedBtn.classList.add(value > 0 ? "active-up" : "active-down");
          clickedBtn.disabled = true;
          otherBtn.disabled = true;
          if (fbThanks) fbThanks.style.display = "inline";
        });
      }
      if (fbUp) fbUp.addEventListener("click", function() { sendFeedback(1, fbUp, fbDown); });
      if (fbDown) fbDown.addEventListener("click", function() { sendFeedback(0, fbDown, fbUp); });

      if (currentSession !== null) {
        sessions[currentSession].messages.push({ role: "ai", data: fullData });
        saveSessions();
      }
    }

    function buildCopyText(d) {
      var parts = [];
      parts.push("【案件类型】" + (d.matter_type || "-"));
      parts.push("【风险等级】" + (d.risk_level || "-"));
      parts.push("【置信度】" + (d.confidence || "-"));
      parts.push("");
      if (d.draft_opinion) { parts.push("【核心意见】"); parts.push(d.draft_opinion); parts.push(""); }
      if (d.facts && d.facts.length) {
        parts.push("【关键事实】");
        d.facts.forEach(function(f, i) { parts.push((i+1) + ". " + f); });
        parts.push("");
      }
      if (d.issues && d.issues.length) {
        parts.push("【风险分析】");
        d.issues.forEach(function(iss) {
          parts.push("- " + (iss.title || "") + " [" + (iss.risk_level || "") + "]");
          if (iss.analysis) parts.push("  " + iss.analysis);
        });
        parts.push("");
      }
      if (d.suggested_actions && d.suggested_actions.length) {
        parts.push("【建议措施】");
        d.suggested_actions.forEach(function(a, i) { parts.push((i+1) + ". " + a); });
        parts.push("");
      }
      if (d.legal_basis && d.legal_basis.length) {
        parts.push("【法律依据】");
        d.legal_basis.forEach(function(b) { parts.push("- " + (b.title || "") + " (" + (b.reference_id || "") + ")"); });
        parts.push("");
      }
      if (d.review_notes && d.review_notes.length) {
        parts.push("【复核意见】");
        d.review_notes.forEach(function(n) { parts.push("- " + n); });
      }
      return parts.join("\\n");
    }

    function cancelAnalysis() {
      if (activeController) {
        activeController.abort();
        activeController = null;
      }
    }

    function setSendButtonState(loading) {
      if (loading) {
        el.sendBtn.disabled = false;
        el.sendBtn.classList.add("cancel");
        el.sendBtn.textContent = "✕";
        el.sendBtn.title = "取消分析";
        el.sendBtn.onclick = cancelAnalysis;
      } else {
        el.sendBtn.disabled = false;
        el.sendBtn.classList.remove("cancel");
        el.sendBtn.textContent = "↑";
        el.sendBtn.title = "发送";
        el.sendBtn.onclick = runAnalysis;
        activeController = null;
      }
    }

    async function runAnalysis() {
      var query = el.queryInput.value.trim();
      if (!query) { el.queryInput.focus(); return; }

      if (currentSession === null) {
        var sid = "sess_" + (typeof crypto !== "undefined" && crypto.randomUUID ? crypto.randomUUID() : Date.now().toString(36) + Math.random().toString(36).slice(2));
        sessions.unshift({ title: query.slice(0, 30), messages: [], createdAt: Date.now(), sessionId: sid });
        currentSession = 0;
        el.welcome.style.display = "none";
        el.chatContainer.innerHTML = "";
      }

      appendUserMsg(query, true);
      el.queryInput.value = "";
      setTextareaHeight();

      activeController = new AbortController();
      setSendButtonState(true);

      var ctx = createStreamingBubble();

      try {
        var resp = await fetch("/analysis/stream", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ user_query: query, session_id: sessions[currentSession].sessionId || null }),
          signal: activeController.signal
        });
        if (!resp.ok) {
          var errText = await resp.text();
          throw new Error(errText || resp.statusText);
        }

        var reader = resp.body.getReader();
        var decoder = new TextDecoder();
        var buffer = "";
        var fullData = null;

        while (true) {
          var result = await reader.read();
          if (result.done) break;
          buffer += decoder.decode(result.value, { stream: true });

          var lines = buffer.split("\\n");
          buffer = lines.pop();

          for (var i = 0; i < lines.length; i++) {
            var line = lines[i].trim();
            if (!line || !line.startsWith("data: ")) continue;
            var jsonStr = line.slice(6);
            try {
              var evt = JSON.parse(jsonStr);
              if (evt.event === "stage") {
                renderStage(ctx, evt.agent, evt.data);
              } else if (evt.event === "done") {
                fullData = evt.data;
              }
            } catch(e) { /* skip malformed lines */ }
          }
        }

        if (fullData) {
          finalizeStreamingMsg(ctx, fullData);
        }
        renderHistory();
      } catch(err) {
        if (err.name === "AbortError") {
          var statusEl = ctx.el.querySelector(".st-status." + ctx.uid);
          if (statusEl) statusEl.querySelector(".st-status-text").textContent = "分析已取消";
          return;
        }
        var statusEl = ctx.el.querySelector(".st-status." + ctx.uid);
        if (statusEl) statusEl.remove();
        var bubble = ctx.el.querySelector(".msg-bubble");
        if (bubble) bubble.innerHTML = '<div style="color:var(--risk-high)">分析失败：' + esc(err.message) + '</div>';
      } finally {
        setSendButtonState(false);
        scrollToLatestAiMsg();
      }
    }

    el.sendBtn.onclick = runAnalysis;
    el.queryInput.addEventListener("keydown", function(e) {
      if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); runAnalysis(); }
    });

    // quick questions
    document.querySelectorAll(".quick-card").forEach(function(card) {
      card.addEventListener("click", function() {
        el.queryInput.value = card.getAttribute("data-q");
        setTextareaHeight();
        runAnalysis();
      });
    });

    // init
    loadSessions();
    renderHistory();
    checkHealth();
  </script>
</body>
</html>"""


def render_index() -> HTMLResponse:
    return HTMLResponse(INDEX_HTML)
