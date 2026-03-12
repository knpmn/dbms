<?php
require_once 'config.php';
$current = 'view1';
$conn = getDB();

$data = queryAll($conn, "SELECT * FROM vw_department_headcount ORDER BY department_id");
oci_close($conn);

$totalEmployees = array_sum(array_column($data, 'TOTAL_EMPLOYEES'));

require 'navbar.php';
?>

<div class="card-title">Department Headcount</div>
<div class="card-sub">Total employees per department — View: <code style="color:var(--cyan);font-family:var(--mono);font-size:11px">vw_department_headcount</code></div>

<!-- KPI -->
<div class="kpi-row cols-3" style="margin-bottom:28px">
  <div class="kpi-card accent-gold" data-icon="&#xF1AD;">
    <div class="kpi-label">Total Departments</div>
    <div class="kpi-val gold-text"><?= count($data) ?></div>
    <div class="kpi-sub">departments</div>
  </div>
  <div class="kpi-card accent-cyan" data-icon="&#xF0C0;">
    <div class="kpi-label">Total Employees</div>
    <div class="kpi-val cyan-text"><?= $totalEmployees ?></div>
    <div class="kpi-sub">across all departments</div>
  </div>
  <div class="kpi-card accent-green" data-icon="&#xF080;">
    <div class="kpi-label">Avg per Dept</div>
    <div class="kpi-val green-text"><?= count($data) > 0 ? number_format($totalEmployees / count($data), 1) : 0 ?></div>
    <div class="kpi-sub">employees / dept</div>
  </div>
</div>

<div class="section-title">Department Breakdown</div>
<?php
$maxEmp = max(array_column($data, 'TOTAL_EMPLOYEES') ?: [1]) ?: 1;
$colors = ['fill-gold','fill-cyan','fill-green','fill-blue','fill-red'];
?>
<div class="card">
  <div class="table-wrap">
  <table class="data-table">
    <thead>
      <tr>
        <th>#</th>
        <th>Department ID</th>
        <th>Department Name</th>
        <th class="num">Total Employees</th>
        <th style="min-width:180px">Distribution</th>
      </tr>
    </thead>
    <tbody>
      <?php foreach ($data as $i => $row):
        $pct = $maxEmp > 0 ? round($row['TOTAL_EMPLOYEES'] / $maxEmp * 100) : 0;
        $color = $colors[$i % count($colors)];
      ?>
      <tr>
        <td><span class="rank rank-<?= $i < 3 ? ($i+1) : 'n' ?>"><?= $i+1 ?></span></td>
        <td class="muted-text" style="font-family:var(--mono)"><?= htmlspecialchars($row['DEPARTMENT_ID']) ?></td>
        <td style="font-weight:500"><?= htmlspecialchars($row['DEPARTMENT_NAME']) ?></td>
        <td class="num cyan-text"><?= htmlspecialchars($row['TOTAL_EMPLOYEES']) ?></td>
        <td style="padding-right:20px">
          <div style="display:flex;align-items:center;gap:8px">
            <div class="bar-track" style="flex:1">
              <div class="bar-fill <?= $color ?>" style="width:<?= $pct ?>%"></div>
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
