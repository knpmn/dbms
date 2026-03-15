<?php
require_once 'config.php';
$current = 'view2';
$conn = getDB();

$data = queryAll($conn, "SELECT * FROM vw_monthly_bonus_summary ORDER BY total_monthly_points DESC");
oci_close($conn);

$totalPoints  = array_sum(array_column($data, 'TOTAL_MONTHLY_POINTS'));
$totalRecords = count($data);
$fullMonths   = count(array_filter($data, fn($r) => $r['TOTAL_MONTHLY_POINTS'] >= 10));

require 'navbar.php';
?>

<div class="card-title">Monthly Bonus Summary</div>
<div class="card-sub">Employee bonus points grouped by month/year (max 10 pts/month) — View: <code style="color:var(--cyan);font-family:var(--mono);font-size:11px">vw_monthly_bonus_summary</code></div>

<!-- KPI -->
<div class="kpi-row cols-3" style="margin-bottom:28px">
  <div class="kpi-card accent-gold" data-icon="&#xF06B;">
    <div class="kpi-label">Total Points Awarded</div>
    <div class="kpi-val gold-text"><?= number_format($totalPoints) ?></div>
    <div class="kpi-sub">all-time capped points</div>
  </div>
  <div class="kpi-card accent-cyan" data-icon="&#xF03A;">
    <div class="kpi-label">Records</div>
    <div class="kpi-val cyan-text"><?= $totalRecords ?></div>
    <div class="kpi-sub">employee-month entries</div>
  </div>
  <div class="kpi-card accent-green" data-icon="&#xF091;">
    <div class="kpi-label">Perfect Months</div>
    <div class="kpi-val green-text"><?= $fullMonths ?></div>
    <div class="kpi-sub">entries hitting 10 pts</div>
  </div>
</div>

<div class="section-title">Monthly Bonus Records</div>
<div class="card">
  <div class="table-wrap">
  <table class="data-table">
    <thead>
      <tr>
        <th>Employee ID</th>
        <th>First Name</th>
        <th>Last Name</th>
        <th class="num">Year</th>
        <th class="num">Month</th>
        <th class="num">Points</th>
        <th style="min-width:160px">Progress (/ 10)</th>
      </tr>
    </thead>
    <tbody>
      <?php foreach ($data as $row):
        $pts = (float)$row['TOTAL_MONTHLY_POINTS'];
        $pct = min(round($pts / 10 * 100), 100);
        $barColor  = $pct >= 100 ? 'fill-green' : ($pct >= 50 ? 'fill-gold' : 'fill-red');
        $textColor = $pct >= 100 ? 'green-text' : ($pct >= 50 ? 'gold-text' : 'red-text');
      ?>
      <tr>
        <td class="muted-text" style="font-family:var(--mono)"><?= htmlspecialchars($row['EMPLOYEE_ID']) ?></td>
        <td style="font-weight:500"><?= htmlspecialchars($row['FIRST_NAME']) ?></td>
        <td><?= htmlspecialchars($row['LAST_NAME']) ?></td>
        <td class="num muted-text"><?= htmlspecialchars($row['BONUS_YEAR']) ?></td>
        <td class="num muted-text"><?= htmlspecialchars($row['BONUS_MONTH']) ?></td>
        <td class="num <?= $textColor ?>" style="font-weight:600"><?= number_format($pts, 1) ?> / 10</td>
        <td style="padding-right:20px">
          <div style="display:flex;align-items:center;gap:8px">
            <div class="bar-track" style="flex:1">
              <div class="bar-fill <?= $barColor ?>" style="width:<?= $pct ?>%"></div>
            </div>
            <span style="font-family:var(--mono);font-size:11px;color:var(--muted);width:36px;text-align:right"><?= $pct ?>%</span>
          </div>
        </td>
      </tr>
      <?php endforeach; ?>
    </tbody>
  </table>
  </div>
</div>

<?php require 'footer.php'; ?>