<?php
require_once 'config.php';
$current = 'view8';
$conn = getDB();

$data = queryAll($conn, "SELECT * FROM vw_monthly_attendance_summary ORDER BY attendance_year DESC, attendance_month DESC, employee_id");
oci_close($conn);

$totalPresent = array_sum(array_column($data, 'TOTAL_PRESENT'));
$totalAbsent  = array_sum(array_column($data, 'TOTAL_ABSENT'));
$totalLeave   = array_sum(array_column($data, 'TOTAL_LEAVE'));

require 'navbar.php';
?>

<div class="card-title">Monthly Attendance Summary</div>
<div class="card-sub">Monthly attendance breakdown per employee — View: <code style="color:var(--cyan);font-family:var(--mono);font-size:11px">vw_monthly_attendance_summary</code></div>

<!-- KPI -->
<div class="kpi-row cols-3" style="margin-bottom:28px">
  <div class="kpi-card accent-green" data-icon="&#xF058;">
    <div class="kpi-label">Total Present Days</div>
    <div class="kpi-val green-text"><?= $totalPresent ?></div>
    <div class="kpi-sub">across all employees & months</div>
  </div>
  <div class="kpi-card accent-red" data-icon="&#xF057;">
    <div class="kpi-label">Total Absent Days</div>
    <div class="kpi-val red-text"><?= $totalAbsent ?></div>
    <div class="kpi-sub">across all employees & months</div>
  </div>
  <div class="kpi-card accent-gold" data-icon="&#xF5CA;">
    <div class="kpi-label">Total Leave Days</div>
    <div class="kpi-val gold-text"><?= $totalLeave ?></div>
    <div class="kpi-sub">day off across all records</div>
  </div>
</div>

<div class="section-title">Monthly Breakdown</div>
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
        <th class="num">Present</th>
        <th class="num">Absent</th>
        <th class="num">Leave</th>
      </tr>
    </thead>
    <tbody>
      <?php foreach ($data as $row): ?>
      <tr>
        <td class="muted-text" style="font-family:var(--mono)"><?= htmlspecialchars($row['EMPLOYEE_ID']) ?></td>
        <td style="font-weight:500"><?= htmlspecialchars($row['FIRST_NAME']) ?></td>
        <td><?= htmlspecialchars($row['LAST_NAME']) ?></td>
        <td class="num muted-text"><?= htmlspecialchars($row['ATTENDANCE_YEAR']) ?></td>
        <td class="num muted-text"><?= htmlspecialchars($row['ATTENDANCE_MONTH']) ?></td>
        <td class="num green-text" style="font-weight:600"><?= htmlspecialchars($row['TOTAL_PRESENT']) ?></td>
        <td class="num red-text"><?= htmlspecialchars($row['TOTAL_ABSENT']) ?></td>
        <td class="num gold-text"><?= htmlspecialchars($row['TOTAL_LEAVE']) ?></td>
      </tr>
      <?php endforeach; ?>
    </tbody>
  </table>
</div>

<?php require 'footer.php'; ?>
