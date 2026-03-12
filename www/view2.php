<?php
require_once 'config.php';
$current = 'view2';
$conn = getDB();

$data = queryAll($conn, "SELECT * FROM vw_monthly_bonus_summary ORDER BY bonus_year DESC, bonus_month DESC, employee_id");
oci_close($conn);

$totalPoints = array_sum(array_column($data, 'TOTAL_MONTHLY_POINTS'));
$totalRecords = count($data);

require 'navbar.php';
?>

<div class="card-title">Monthly Bonus Summary</div>
<div class="card-sub">Employee bonus points grouped by month/year — View: <code style="color:var(--cyan);font-family:var(--mono);font-size:11px">vw_monthly_bonus_summary</code></div>

<!-- KPI -->
<div class="kpi-row cols-3" style="margin-bottom:28px">
  <div class="kpi-card accent-gold" data-icon="&#xF06B;">
    <div class="kpi-label">Total Points Awarded</div>
    <div class="kpi-val gold-text"><?= number_format($totalPoints) ?></div>
    <div class="kpi-sub">all-time points</div>
  </div>
  <div class="kpi-card accent-cyan" data-icon="&#xF03A;">
    <div class="kpi-label">Records</div>
    <div class="kpi-val cyan-text"><?= $totalRecords ?></div>
    <div class="kpi-sub">employee-month entries</div>
  </div>
  <div class="kpi-card accent-green" data-icon="&#xF080;">
    <div class="kpi-label">Avg Points / Entry</div>
    <div class="kpi-val green-text"><?= $totalRecords > 0 ? number_format($totalPoints / $totalRecords, 1) : 0 ?></div>
    <div class="kpi-sub">points per record</div>
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
        <th class="num">Total Points</th>
      </tr>
    </thead>
    <tbody>
      <?php foreach ($data as $row): ?>
      <tr>
        <td class="muted-text" style="font-family:var(--mono)"><?= htmlspecialchars($row['EMPLOYEE_ID']) ?></td>
        <td style="font-weight:500"><?= htmlspecialchars($row['FIRST_NAME']) ?></td>
        <td><?= htmlspecialchars($row['LAST_NAME']) ?></td>
        <td class="num muted-text"><?= htmlspecialchars($row['BONUS_YEAR']) ?></td>
        <td class="num muted-text"><?= htmlspecialchars($row['BONUS_MONTH']) ?></td>
        <td class="num gold-text" style="font-weight:600"><?= number_format($row['TOTAL_MONTHLY_POINTS']) ?></td>
      </tr>
      <?php endforeach; ?>
    </tbody>
  </table>
</div>

<?php require 'footer.php'; ?>
