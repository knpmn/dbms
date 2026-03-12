<?php
require_once 'config.php';
$current = 'view4';
$conn = getDB();

$data = queryAll($conn, "SELECT * FROM vw_employee_directory ORDER BY employee_id");
oci_close($conn);

require 'navbar.php';
?>

<div class="card-title">Employee Directory</div>
<div class="card-sub">Full employee listing with department and position — View: <code style="color:var(--cyan);font-family:var(--mono);font-size:11px">vw_employee_directory</code></div>

<!-- KPI -->
<div class="kpi-row cols-3" style="margin-bottom:28px">
  <div class="kpi-card accent-gold" data-icon="&#xF0C0;">
    <div class="kpi-label">Total Employees</div>
    <div class="kpi-val gold-text"><?= count($data) ?></div>
    <div class="kpi-sub">in system</div>
  </div>
  <div class="kpi-card accent-cyan" data-icon="&#xF1AD;">
    <div class="kpi-label">Departments</div>
    <div class="kpi-val cyan-text"><?= count(array_unique(array_column($data, 'DEPARTMENT_NAME'))) ?></div>
    <div class="kpi-sub">active departments</div>
  </div>
  <div class="kpi-card accent-green" data-icon="&#xF0B1;">
    <div class="kpi-label">Avg Base Salary</div>
    <div class="kpi-val green-text" style="font-size:20px">
      <?= count($data) > 0 ? number_format(array_sum(array_column($data,'BASE_SALARY')) / count($data), 0) : 0 ?>
    </div>
    <div class="kpi-sub">THB / month</div>
  </div>
</div>

<div class="section-title">Employee List</div>
<div class="card">
  <div class="table-wrap">
  <table class="data-table">
    <thead>
      <tr>
        <th>ID</th>
        <th>First Name</th>
        <th>Last Name</th>
        <th>Email</th>
        <th>Department</th>
        <th>Position</th>
        <th class="num">Base Salary</th>
      </tr>
    </thead>
    <tbody>
      <?php foreach ($data as $row): ?>
      <tr>
        <td class="muted-text" style="font-family:var(--mono)"><?= htmlspecialchars($row['EMPLOYEE_ID']) ?></td>
        <td style="font-weight:500"><?= htmlspecialchars($row['FIRST_NAME']) ?></td>
        <td><?= htmlspecialchars($row['LAST_NAME']) ?></td>
        <td style="font-family:var(--mono);font-size:11px;color:var(--muted)"><?= htmlspecialchars($row['EMAIL']) ?></td>
        <td><span class="badge badge-cyan"><?= htmlspecialchars($row['DEPARTMENT_NAME'] ?? '-') ?></span></td>
        <td><?= htmlspecialchars($row['POSITION_NAME'] ?? '-') ?></td>
        <td class="num gold-text"><?= number_format($row['BASE_SALARY'] ?? 0) ?></td>
      </tr>
      <?php endforeach; ?>
    </tbody>
  </table>
</div>

<?php require 'footer.php'; ?>
