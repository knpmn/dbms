<?php
require_once 'config.php';
$current = 'view10';
$conn = getDB();

$data = queryAll($conn, "SELECT * FROM vw_yearly_bonus_overview ORDER BY bonus_year DESC, total_bonus_score DESC");
oci_close($conn);

$fullYear = count(array_filter($data, fn($r) => $r['TOTAL_BONUS_SCORE'] >= 120));
$topScore = count($data) > 0 ? max(array_column($data, 'TOTAL_BONUS_SCORE')) : 0;

require 'navbar.php';
?>

<div class="card-title">Yearly Bonus Overview</div>
<div class="card-sub">Annual bonus eligibility based on hitting 10 pts every month (max 120) — View: <code style="color:var(--cyan);font-family:var(--mono);font-size:11px">vw_yearly_bonus_overview</code></div>

<!-- KPI -->
<div class="kpi-row cols-3" style="margin-bottom:28px">
  <div class="kpi-card accent-gold" data-icon="&#xF51E;">
    <div class="kpi-label">Total Records</div>
    <div class="kpi-val gold-text"><?= count($data) ?></div>
    <div class="kpi-sub">employee-year entries</div>
  </div>
  <div class="kpi-card accent-cyan" data-icon="&#xF080;">
    <div class="kpi-label">Top Score</div>
    <div class="kpi-val cyan-text"><?= number_format($topScore, 1) ?></div>
    <div class="kpi-sub">out of 120</div>
  </div>
  <div class="kpi-card accent-green" data-icon="&#xF091;">
    <div class="kpi-label">Full Year Achievers</div>
    <div class="kpi-val green-text"><?= $fullYear ?></div>
    <div class="kpi-sub">hit 120 pts (full bonus)</div>
  </div>
</div>

<div class="section-title">Yearly Bonus Records</div>
<div class="card">
  <div class="table-wrap">
  <table class="data-table" style="text-align:center">
    <thead>
      <tr>
        <th>Record ID</th>
        <th>Employee ID</th>
        <th>First Name</th>
        <th>Last Name</th>
        <th>Year</th>
        <th>Total Score (/ 120)</th>
        <th style="min-width:160px">Progress</th>
      </tr>
    </thead>
    <tbody>
      <?php foreach ($data as $row):
        $total    = (float)$row['TOTAL_BONUS_SCORE'];
        $pct      = min(round($total / 120 * 100), 100);
        $barColor = $pct >= 100 ? 'fill-green' : ($pct >= 50 ? 'fill-gold' : 'fill-red');
      ?>
      <tr>
        <td class="muted-text" style="font-family:var(--mono)"><?= htmlspecialchars($row['YEARLY_BONUS_ID']) ?></td>
        <td class="muted-text" style="font-family:var(--mono)"><?= htmlspecialchars($row['EMPLOYEE_ID']) ?></td>
        <td style="font-weight:500"><?= htmlspecialchars($row['FIRST_NAME']) ?></td>
        <td><?= htmlspecialchars($row['LAST_NAME']) ?></td>
        <td class="muted-text"><?= htmlspecialchars($row['BONUS_YEAR']) ?></td>
        <td class="gold-text" style="font-weight:700"><?= number_format($total, 1) ?> / 120</td>
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