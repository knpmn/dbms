<?php
require_once 'config.php';
$current = 'view3';
$conn = getDB();

$data = queryAll($conn, "SELECT * FROM vw_top_performance_bonus ORDER BY total_accumulated_points DESC");
oci_close($conn);

$totalPoints = array_sum(array_column($data, 'TOTAL_ACCUMULATED_POINTS'));
$maxPoints   = count($data) > 0 ? max(array_column($data, 'TOTAL_ACCUMULATED_POINTS')) : 1;

require 'navbar.php';
?>

<div class="card-title">Top Performance Bonus</div>
<div class="card-sub">Employees ranked by total accumulated bonus points — View: <code style="color:var(--cyan);font-family:var(--mono);font-size:11px">vw_top_performance_bonus</code></div>

<!-- KPI -->
<div class="kpi-row cols-3" style="margin-bottom:28px">
  <div class="kpi-card accent-gold" data-icon="&#xF091;">
    <div class="kpi-label">Total Points (All)</div>
    <div class="kpi-val gold-text"><?= number_format($totalPoints) ?></div>
    <div class="kpi-sub">accumulated points</div>
  </div>
  <div class="kpi-card accent-cyan" data-icon="&#xF0C0;">
    <div class="kpi-label">Employees Ranked</div>
    <div class="kpi-val cyan-text"><?= count($data) ?></div>
    <div class="kpi-sub">with bonus records</div>
  </div>
  <div class="kpi-card accent-green" data-icon="&#xF005;">
    <div class="kpi-label">Top Score</div>
    <div class="kpi-val green-text"><?= $maxPoints ?></div>
    <div class="kpi-sub">highest accumulated pts</div>
  </div>
</div>

<div class="section-title">Performance Ranking</div>
<div class="card">
  <div class="table-wrap">
  <table class="data-table">
    <thead>
      <tr>
        <th>Rank</th>
        <th>Employee ID</th>
        <th>First Name</th>
        <th>Last Name</th>
        <th class="num">Total Points</th>
        <th style="min-width:200px">Progress</th>
      </tr>
    </thead>
    <tbody>
      <?php foreach ($data as $i => $row):
        $pct = $maxPoints > 0 ? round($row['TOTAL_ACCUMULATED_POINTS'] / $maxPoints * 100) : 0;
      ?>
      <tr>
        <td><span class="rank rank-<?= $i < 3 ? ($i+1) : 'n' ?>"><?= $i+1 ?></span></td>
        <td class="muted-text" style="font-family:var(--mono)"><?= htmlspecialchars($row['EMPLOYEE_ID']) ?></td>
        <td style="font-weight:500"><?= htmlspecialchars($row['FIRST_NAME']) ?></td>
        <td><?= htmlspecialchars($row['LAST_NAME']) ?></td>
        <td class="num gold-text" style="font-weight:700"><?= number_format($row['TOTAL_ACCUMULATED_POINTS']) ?></td>
        <td style="padding-right:20px">
          <div style="display:flex;align-items:center;gap:8px">
            <div class="bar-track" style="flex:1">
              <div class="bar-fill fill-gold" style="width:<?= $pct ?>%"></div>
            </div>
            <span style="font-family:var(--mono);font-size:11px;color:var(--muted);width:32px;text-align:right"><?= $pct ?>%</span>
          </div>
        </td>
      </tr>
      <?php endforeach; ?>
    </tbody>
  </table>
</div>

<?php require 'footer.php'; ?>
