<?php
$current = $current ?? '';

$navItems = [
    'view1'  => ['icon' => 'fa-building',           'label' => 'Dept Headcount',      'file' => 'view1.php'],
    'view2'  => ['icon' => 'fa-gift',                'label' => 'Monthly Bonus',        'file' => 'view2.php'],
    'view3'  => ['icon' => 'fa-trophy',              'label' => 'Top Performance',      'file' => 'view3.php'],
    'view4'  => ['icon' => 'fa-users',               'label' => 'Employee Directory',   'file' => 'view4.php'],
    'view5'  => ['icon' => 'fa-file-contract',       'label' => 'Contract Expiry',      'file' => 'view5.php'],
    'view6'  => ['icon' => 'fa-triangle-exclamation','label' => 'Penalty History',      'file' => 'view6.php'],
    'view7'  => ['icon' => 'fa-calendar-check',      'label' => "Today's Attendance",  'file' => 'view7.php'],
    'view8'  => ['icon' => 'fa-chart-bar',           'label' => 'Monthly Attendance',  'file' => 'view8.php'],
    'view9'  => ['icon' => 'fa-briefcase',           'label' => 'Active Recruitment',  'file' => 'view9.php'],
    'view10' => ['icon' => 'fa-coins',               'label' => 'Yearly Bonus',        'file' => 'view10.php'],
];
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>HR Oracle Dashboard</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <style>
    /* ═══════ RESET & VARS ═══════ */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      /* ── Light mode ── */
      --bg:        #f0f5ff;
      --surface:   #ffffff;
      --surface2:  #f5f8ff;
      --border:    #dbe4ff;
      --text:      #1e2a45;
      --muted:     #8898b8;
      --sidebar-header-bg: linear-gradient(135deg,#1d4ed8,#2563eb);
      --sidebar-logo-text: #ffffff;
      --sidebar-logo-sub:  rgba(255,255,255,.6);

      /* ── Brand palette ── */
      --primary:  #2563eb;
      --sky:      #0ea5e9;
      --indigo:   #6366f1;
      --green:    #059669;
      --red:      #dc2626;

      /* legacy aliases */
      --gold: var(--primary);
      --cyan: var(--sky);
      --blue: var(--indigo);

      --nav-w:      232px;
      --mono:       'JetBrains Mono', monospace;
      --sans:       'Inter', sans-serif;
      --shadow-sm:  0 1px 3px rgba(37,99,235,.07);
      --shadow:     0 4px 20px rgba(37,99,235,.12);
      --transition: .18s ease;
    }

    /* ═══════ DARK MODE ═══════ */
    [data-theme="dark"] {
      --bg:        #0d1526;
      --surface:   #152036;
      --surface2:  #1a2942;
      --border:    #243556;
      --text:      #cdd9f0;
      --muted:     #5a7299;
      --sidebar-header-bg: linear-gradient(135deg,#1a3a8f,#1d4ed8);
      --sidebar-logo-text: #e2eaff;
      --sidebar-logo-sub:  rgba(180,200,255,.5);
      --shadow-sm:  0 1px 4px rgba(0,0,0,.35);
      --shadow:     0 4px 24px rgba(0,0,0,.45);
    }

    /* ═══════ BASE ═══════ */
    body {
      font-family: var(--sans);
      background: var(--bg);
      color: var(--text);
      display: flex;
      min-height: 100vh;
      transition: background var(--transition), color var(--transition);
    }

    /* ═══════ OVERLAY (mobile) ═══════ */
    .sidebar-overlay {
      display: none;
      position: fixed; inset: 0;
      background: rgba(0,0,0,.45);
      z-index: 99;
      opacity: 0;
      transition: opacity var(--transition);
    }
    body.sidebar-open .sidebar-overlay {
      display: block;
      opacity: 1;
    }

    /* ═══════ SIDEBAR ═══════ */
    .sidebar {
      width: var(--nav-w);
      min-height: 100vh;
      background: var(--surface);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      position: fixed;
      left: 0; top: 0;
      z-index: 100;
      box-shadow: var(--shadow);
      transition: transform var(--transition), background var(--transition), border-color var(--transition);
    }

    .sidebar-logo {
      padding: 20px 16px 18px;
      border-bottom: 1px solid rgba(255,255,255,.12);
      background: var(--sidebar-header-bg);
    }
    .sidebar-logo .logo-icon {
      width: 36px; height: 36px;
      background: rgba(255,255,255,.15);
      border-radius: 8px;
      display: flex; align-items: center; justify-content: center;
      font-size: 16px; margin-bottom: 10px;
      color: #fff;
      border: 1px solid rgba(255,255,255,.2);
    }
    .sidebar-logo h1 { font-size: 14px; font-weight: 700; color: var(--sidebar-logo-text); }
    .sidebar-logo span {
      font-family: var(--mono); font-size: 9px;
      color: var(--sidebar-logo-sub);
      letter-spacing: 1.5px; text-transform: uppercase;
    }

    /* Nav close btn (mobile only) */
    .sidebar-close {
      display: none;
      position: absolute; top: 14px; right: 12px;
      background: rgba(255,255,255,.15); border: none; cursor: pointer;
      width: 28px; height: 28px; border-radius: 6px;
      color: #fff; font-size: 13px;
      align-items: center; justify-content: center;
    }

    .nav-section {
      padding: 14px 12px 6px;
      font-family: var(--mono); font-size: 9px;
      letter-spacing: 2px; text-transform: uppercase;
      color: var(--muted);
    }

    .nav-item {
      display: flex; align-items: center; gap: 9px;
      padding: 8px 10px; margin: 1px 6px;
      border-radius: 7px; text-decoration: none;
      color: var(--muted); font-size: 12.5px; font-weight: 500;
      transition: background var(--transition), color var(--transition);
      position: relative;
    }
    .nav-item:hover { background: var(--surface2); color: var(--text); }
    .nav-item.active { background: rgba(37,99,235,.1); color: var(--primary); }
    .nav-item.active::before {
      content: '';
      position: absolute; left: -6px; top: 50%;
      transform: translateY(-50%);
      width: 3px; height: 18px;
      background: var(--primary); border-radius: 0 3px 3px 0;
    }
    .nav-item .nav-icon {
      width: 28px; height: 28px;
      display: flex; align-items: center; justify-content: center;
      border-radius: 6px; background: var(--surface2);
      font-size: 12px; color: var(--muted); flex-shrink: 0;
      transition: background var(--transition), color var(--transition);
    }
    .nav-item:hover .nav-icon  { background: var(--border); color: var(--text); }
    .nav-item.active .nav-icon { background: rgba(37,99,235,.12); color: var(--primary); }
    .nav-item .nav-label { flex: 1; }
    .nav-item .nav-badge {
      font-family: var(--mono); font-size: 8.5px;
      background: var(--surface2); color: var(--muted);
      padding: 2px 5px; border-radius: 4px; border: 1px solid var(--border);
    }
    .nav-item.active .nav-badge {
      background: rgba(37,99,235,.1); color: var(--primary);
      border-color: rgba(37,99,235,.2);
    }

    .sidebar-footer {
      margin-top: auto; padding: 12px 14px;
      border-top: 1px solid var(--border);
      font-family: var(--mono); font-size: 10px; color: var(--muted);
      background: var(--surface2);
      transition: background var(--transition);
    }
    .db-status { display: flex; align-items: center; gap: 6px; margin-bottom: 3px; }
    .dot {
      width: 6px; height: 6px; border-radius: 50%;
      background: var(--green); box-shadow: 0 0 6px rgba(5,150,105,.5);
      animation: blink 2s infinite;
    }
    @keyframes blink { 0%,100%{opacity:1} 50%{opacity:.4} }

    /* ═══════ MAIN ═══════ */
    .main { margin-left: var(--nav-w); flex:1; display:flex; flex-direction:column; min-height:100vh; }

    /* ═══════ TOPBAR ═══════ */
    .topbar {
      padding: 10px 24px; border-bottom: 1px solid var(--border);
      background: var(--surface);
      display: flex; align-items: center; justify-content: space-between;
      position: sticky; top: 0; z-index: 50;
      box-shadow: var(--shadow-sm);
      gap: 12px;
      transition: background var(--transition), border-color var(--transition);
    }
    .topbar-left {
      display: flex; align-items: center; gap: 8px;
      font-size: 12.5px; color: var(--muted); min-width: 0;
    }
    .topbar-left .brand { white-space: nowrap; }
    .topbar-left .sep { color: var(--border); font-size: 16px; }
    .topbar-left .page-name {
      color: var(--text); font-weight: 600;
      display: flex; align-items: center; gap: 7px;
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    .topbar-left .page-name i { color: var(--primary); font-size: 13px; flex-shrink:0; }

    .topbar-right {
      display: flex; align-items: center; gap: 8px;
      font-family: var(--mono); font-size: 11px; color: var(--muted);
      flex-shrink: 0;
    }
    .topbar-pill {
      background: rgba(37,99,235,.08); color: var(--primary);
      border: 1px solid rgba(37,99,235,.18); border-radius: 5px;
      padding: 2px 8px; font-size: 10.5px;
      white-space: nowrap;
    }
    .topbar-date { white-space: nowrap; }

    /* Hamburger button (mobile only) */
    .menu-toggle {
      display: none;
      background: var(--surface2); border: 1px solid var(--border);
      border-radius: 7px; cursor: pointer;
      width: 34px; height: 34px; flex-shrink: 0;
      align-items: center; justify-content: center;
      color: var(--text); font-size: 14px;
      transition: background var(--transition);
    }
    .menu-toggle:hover { background: var(--border); }

    /* Dark mode toggle */
    .theme-toggle {
      background: var(--surface2); border: 1px solid var(--border);
      border-radius: 7px; cursor: pointer;
      width: 34px; height: 34px; flex-shrink: 0;
      display: flex; align-items: center; justify-content: center;
      color: var(--muted); font-size: 14px;
      transition: background var(--transition), color var(--transition), border-color var(--transition);
    }
    .theme-toggle:hover { background: var(--border); color: var(--text); }

    /* ═══════ PAGE CONTENT ═══════ */
    .page-content { padding: 20px 24px; flex: 1; }

    /* ═══════ SECTION TITLE ═══════ */
    .section-title {
      font-family: var(--mono); font-size: 9.5px;
      letter-spacing: 2px; text-transform: uppercase;
      color: var(--muted); margin-bottom: 12px;
      display: flex; align-items: center; gap: 10px;
    }
    .section-title::after { content:''; flex:1; height:1px; background:var(--border); }

    /* ═══════ CARD ═══════ */
    .card {
      background: var(--surface); border: 1px solid var(--border);
      border-radius: 10px; padding: 18px 20px;
      box-shadow: var(--shadow-sm);
      transition: background var(--transition), border-color var(--transition);
    }
    .card-title { font-size: 16px; font-weight: 700; color: var(--text); margin-bottom: 3px; }
    .card-sub   { font-size: 11.5px; color: var(--muted); margin-bottom: 18px; }

    /* ═══════ TABLE ═══════ */
    .table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; }
    .data-table { width: 100%; border-collapse: collapse; font-size: 12.5px; min-width: 540px; }
    .data-table thead th {
      font-family: var(--mono); font-size: 9.5px;
      letter-spacing: 1px; text-transform: uppercase;
      color: var(--muted); padding: 9px 12px;
      text-align: left; border-bottom: 1px solid var(--border);
      white-space: nowrap; background: var(--surface2);
      transition: background var(--transition);
    }
    .data-table thead th:first-child { border-radius: 8px 0 0 0; }
    .data-table thead th:last-child  { border-radius: 0 8px 0 0; }
    .data-table tbody tr { transition: background .12s; }
    .data-table tbody tr:hover { background: var(--surface2); }
    .data-table tbody td { padding: 9px 12px; border-bottom: 1px solid var(--border); color: var(--text); }
    .data-table tbody tr:last-child td { border-bottom: none; }
    .data-table tfoot td { padding: 9px 12px; }
    .num { text-align: right; font-family: var(--mono); font-size: 12px; }
    .gold-text  { color: var(--primary); }
    .cyan-text  { color: var(--sky); }
    .green-text { color: var(--green); }
    .red-text   { color: var(--red); }
    .muted-text { color: var(--muted); }

    /* ═══════ BADGES ═══════ */
    .badge {
      display: inline-flex; align-items: center; gap: 4px;
      padding: 3px 9px; border-radius: 20px; font-size: 11px; font-weight: 600;
    }
    .badge-green { background:rgba(5,150,105,.08);  color:var(--green);   border:1px solid rgba(5,150,105,.2); }
    .badge-gold  { background:rgba(37,99,235,.08);  color:var(--primary); border:1px solid rgba(37,99,235,.2); }
    .badge-red   { background:rgba(220,38,38,.08);  color:var(--red);     border:1px solid rgba(220,38,38,.2); }
    .badge-cyan  { background:rgba(14,165,233,.09); color:var(--sky);     border:1px solid rgba(14,165,233,.2); }
    .badge-blue  { background:rgba(99,102,241,.09); color:var(--indigo);  border:1px solid rgba(99,102,241,.2); }
    .badge-muted { background:rgba(136,152,184,.1); color:var(--muted);   border:1px solid rgba(136,152,184,.2); }

    /* ═══════ RANK ═══════ */
    .rank {
      display:inline-flex; align-items:center; justify-content:center;
      width:24px; height:24px; border-radius:6px;
      font-family:var(--mono); font-size:11px; font-weight:700;
    }
    .rank-1 { background:rgba(37,99,235,.15);  color:var(--primary); }
    .rank-2 { background:rgba(99,102,241,.13); color:var(--indigo); }
    .rank-3 { background:rgba(14,165,233,.13); color:var(--sky); }
    .rank-n { background:var(--surface2); color:var(--muted); }

    /* ═══════ KPI ROW ═══════ */
    .kpi-row { display:grid; gap:14px; margin-bottom:20px; }
    .kpi-row.cols-2 { grid-template-columns:repeat(2,1fr); }
    .kpi-row.cols-3 { grid-template-columns:repeat(3,1fr); }
    .kpi-row.cols-4 { grid-template-columns:repeat(4,1fr); }
    .kpi-card {
      background:var(--surface); border:1px solid var(--border);
      border-radius:10px; padding:16px 18px;
      position:relative; overflow:hidden;
      box-shadow:var(--shadow-sm);
      transition:box-shadow .2s, transform .2s, background var(--transition), border-color var(--transition);
    }
    .kpi-card:hover { box-shadow:var(--shadow); transform:translateY(-2px); }
    .kpi-card::after {
      font-family: "Font Awesome 6 Free";
      font-weight: 900;
      content: attr(data-icon);
      position:absolute; right:16px; top:50%; transform:translateY(-50%);
      font-size:46px; opacity:.18; pointer-events:none;
    }
    .kpi-card .kpi-label { font-size:9.5px; font-family:var(--mono); letter-spacing:1px; text-transform:uppercase; color:var(--muted); margin-bottom:7px; }
    .kpi-card .kpi-val   { font-family:var(--mono); font-size:24px; font-weight:700; }
    .kpi-card .kpi-sub   { font-size:11px; color:var(--muted); margin-top:4px; }
    .kpi-card.accent-gold  { border-top:3px solid var(--primary); }
    .kpi-card.accent-cyan  { border-top:3px solid var(--sky); }
    .kpi-card.accent-green { border-top:3px solid var(--green); }
    .kpi-card.accent-blue  { border-top:3px solid var(--indigo); }
    .kpi-card.accent-red   { border-top:3px solid var(--red); }

    /* ═══════ BARS ═══════ */
    .bar-track { height:7px; background:var(--surface2); border-radius:4px; overflow:hidden; border:1px solid var(--border); }
    .bar-fill  { height:100%; border-radius:4px; animation:grow 1s ease forwards; }
    @keyframes grow { from{width:0} }
    .fill-gold  { background:linear-gradient(90deg,var(--primary),#3b82f6); }
    .fill-cyan  { background:linear-gradient(90deg,var(--sky),#38bdf8); }
    .fill-green { background:linear-gradient(90deg,var(--green),#10b981); }
    .fill-blue  { background:linear-gradient(90deg,var(--indigo),#818cf8); }
    .fill-red   { background:linear-gradient(90deg,var(--red),#ef4444); }

    /* ═══════ RESPONSIVE ═══════ */
    @media (max-width: 768px) {
      /* Sidebar slides off-screen; toggle pushes it back */
      .sidebar {
        transform: translateX(-100%);
      }
      body.sidebar-open .sidebar {
        transform: translateX(0);
      }
      .sidebar-close { display: flex; }

      /* Main fills full width */
      .main { margin-left: 0; }

      /* Show hamburger in topbar */
      .menu-toggle { display: flex; }

      /* Hide brand text to save room */
      .topbar-left .brand,
      .topbar-left .sep { display: none; }

      /* Hide date on very small screens */
      .topbar-date { display: none; }

      /* KPI grids collapse */
      .kpi-row.cols-4,
      .kpi-row.cols-3 { grid-template-columns: repeat(2, 1fr); }
      .kpi-row.cols-2 { grid-template-columns: 1fr; }

      /* Tighter page padding */
      .page-content { padding: 14px 12px; }
      .topbar { padding: 8px 14px; }
    }

    @media (max-width: 420px) {
      .kpi-row.cols-4,
      .kpi-row.cols-3,
      .kpi-row.cols-2 { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>

<!-- Overlay for mobile -->
<div class="sidebar-overlay" id="sidebarOverlay"></div>

<!-- ═══ SIDEBAR ═══ -->
<aside class="sidebar" id="sidebar">
  <button class="sidebar-close" id="sidebarClose" aria-label="Close menu">
    <i class="fa-solid fa-xmark"></i>
  </button>
  <div class="sidebar-logo">
    <div class="logo-icon"><i class="fa-solid fa-database"></i></div>
    <h1>HR Dashboard</h1>
    <span>Oracle Analytics</span>
  </div>

  <div class="nav-section">Views</div>

  <?php foreach($navItems as $key => $item): ?>
  <a href="<?= $item['file'] ?>" class="nav-item <?= $current === $key ? 'active' : '' ?>">
    <span class="nav-icon"><i class="fa-solid <?= $item['icon'] ?>"></i></span>
    <span class="nav-label"><?= $item['label'] ?></span>
    <span class="nav-badge"><?= strtoupper($key) ?></span>
  </a>
  <?php endforeach; ?>

  <div class="sidebar-footer">
    <div class="db-status"><div class="dot"></div> Oracle Connected</div>
    <div><?= ORA_SID ?></div>
  </div>
</aside>

<!-- ═══ MAIN ═══ -->
<main class="main">
  <div class="topbar">
    <!-- Left: hamburger + breadcrumb -->
    <div class="topbar-left">
      <button class="menu-toggle" id="menuToggle" aria-label="Open menu">
        <i class="fa-solid fa-bars"></i>
      </button>
      <span class="brand">HR Dashboard</span>
      <span class="sep">›</span>
      <span class="page-name">
        <i class="fa-solid <?= $navItems[$current]['icon'] ?? 'fa-chart-bar' ?>"></i>
        <?= $navItems[$current]['label'] ?? 'Dashboard' ?>
      </span>
    </div>

    <!-- Right: SID pill + date + dark toggle -->
    <div class="topbar-right">
      <span class="topbar-pill">
        <i class="fa-solid fa-server" style="margin-right:4px"></i><?= ORA_SID ?>
      </span>
      <span class="topbar-date"><?= date('d M Y') ?></span>
      <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode">
        <i class="fa-solid fa-moon" id="themeIcon"></i>
      </button>
    </div>
  </div>

  <div class="page-content">

<script>
  /* ── Dark mode ───────────────────────────────────────────────── */
  (function () {
    const root   = document.documentElement;
    const btn    = document.getElementById('themeToggle');
    const icon   = document.getElementById('themeIcon');
    const DARK   = 'dark';
    const stored = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    function setTheme(dark) {
      root.setAttribute('data-theme', dark ? DARK : 'light');
      icon.className = dark ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
      localStorage.setItem('theme', dark ? DARK : 'light');
    }

    // Apply on load (before paint to avoid flash)
    setTheme(stored ? stored === DARK : prefersDark);

    btn.addEventListener('click', function () {
      setTheme(root.getAttribute('data-theme') !== DARK);
    });
  })();

  /* ── Mobile sidebar ──────────────────────────────────────────── */
  (function () {
    const toggle  = document.getElementById('menuToggle');
    const close   = document.getElementById('sidebarClose');
    const overlay = document.getElementById('sidebarOverlay');
    const body    = document.body;

    function open()  { body.classList.add('sidebar-open'); }
    function close_() { body.classList.remove('sidebar-open'); }

    toggle.addEventListener('click', open);
    close.addEventListener('click', close_);
    overlay.addEventListener('click', close_);

    // Close sidebar when a nav link is clicked (navigates away)
    document.querySelectorAll('.nav-item').forEach(function (a) {
      a.addEventListener('click', close_);
    });
  })();
</script>