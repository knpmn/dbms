<?php
require_once 'config.php';
$current = 'view10';
$conn = getDB();

$data = queryAll($conn, "SELECT * FROM vw_yearly_bonus_overview ORDER BY bonus_year DESC, total_bonus_score DESC");
oci_close($conn);

$avgScore = count($data) > 0 ? array_sum(array_column($data, 'YEARLY_BONUS_SCORE')) / count($data) : 0;
$maxScore = count($data) > 0 ? max(array_column($data, 'TOTAL_BONUS_SCORE')) : 1;

require 'navbar.php';
?>

<div class="card-title">Yearly Bonus Overview</div>
<div class="card-sub">Annual bonus scores per employee — View: <code style="color:var(--cyan);font-family:var(--mono);font-size:11px">vw_yearly_bonus_overview</code></div>

<!-- KPI -->
<div class="kpi-row cols-3" style="margin-bottom:28px">
  <div class="kpi-card accent-gold" data-icon="&#xF51E;">
    <div class="kpi-label">Total Records</div>
    <div class="kpi-val gold-text"><?= count($data) ?></div>
    <div class="kpi-sub">employee-year entries</div>
  </div>
  <div class="kpi-card accent-cyan" data-icon="&#xF080;">
    <div class="kpi-label">Avg Yearly Score</div>
    <div class="kpi-val cyan-text"><?= number_format($avgScore, 2) ?></div>
    <div class="kpi-sub">average score</div>
  </div>
  <div class="kpi-card accent-green" data-icon="&#xF091;">
    <div class="kpi-label">Highest Total Score</div>
    <div class="kpi-val green-text"><?= number_format($maxScore, 1) ?></div>
    <div class="kpi-sub">top performer</div>
  </div>
</div>

<div class="section-title">Yearly Bonus Records</div>
<div class="card">
  <div class="table-wrap">
  <table class="data-table">
    <thead>
      <tr>
        <th>Record ID</th>
        <th>Employee ID</th>
        <th>First Name</th>
        <th>Last Name</th>
        <th class="num">Year</th>
        <th class="num">Yearly Score</th>
        <th class="num">Total Score</th>
        <th style="min-width:160px">Progress</th>
      </tr>
    </thead>
    <tbody>
      <?php foreach ($data as $i => $row):
        $pct = $maxScore > 0 ? round($row['TOTAL_BONUS_SCORE'] / $maxScore * 100) : 0;
        $scoreColor = $row['YEARLY_BONUS_SCORE'] >= 8 ? 'green-text' : ($row['YEARLY_BONUS_SCORE'] >= 5 ? 'gold-text' : 'red-text');
      ?>
      <tr>
        <td class="muted-text" style="font-family:var(--mono)"><?= htmlspecialchars($row['YEARLY_BONUS_ID']) ?></td>
        <td class="muted-text" style="font-family:var(--mono)"><?= htmlspecialchars($row['EMPLOYEE_ID']) ?></td>
        <td style="font-weight:500"><?= htmlspecialchars($row['FIRST_NAME']) ?></td>
        <td><?= htmlspecialchars($row['LAST_NAME']) ?></td>
        <td class="num muted-text"><?= htmlspecialchars($row['BONUS_YEAR']) ?></td>
        <td class="num <?= $scoreColor ?>" style="font-weight:600"><?= number_format($row['YEARLY_BONUS_SCORE'], 2) ?></td>
        <td class="num gold-text" style="font-weight:700"><?= number_format($row['TOTAL_BONUS_SCORE'], 1) ?></td>
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
