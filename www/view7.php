<?php
require_once 'config.php';
$current = 'view7';
$conn = getDB();

$data = queryAll($conn, "SELECT * FROM vw_today_attendance_status ORDER BY employee_id");
oci_close($conn);

$presentCount = count(array_filter($data, fn($r) => strtolower($r['STATUS']) === 'present'));
$absentCount  = count(array_filter($data, fn($r) => strtolower($r['STATUS']) === 'absent'));
$leaveCount   = count($data) - $presentCount - $absentCount;

require 'navbar.php';
?>

<div class="card-title">Today's Attendance Status</div>
<div class="card-sub">Live attendance snapshot for today — View: <code style="color:var(--cyan);font-family:var(--mono);font-size:11px">vw_today_attendance_status</code></div>

<!-- KPI -->
<div class="kpi-row cols-3" style="margin-bottom:28px">
  <div class="kpi-card accent-green" data-icon="&#xF058;">
    <div class="kpi-label">Present</div>
    <div class="kpi-val green-text"><?= $presentCount ?></div>
    <div class="kpi-sub">checked in today</div>
  </div>
  <div class="kpi-card accent-red" data-icon="&#xF057;">
    <div class="kpi-label">Absent</div>
    <div class="kpi-val red-text"><?= $absentCount ?></div>
    <div class="kpi-sub">not in today</div>
  </div>
  <div class="kpi-card accent-gold" data-icon="&#xF5CA;">
    <div class="kpi-label">On Leave / Other</div>
    <div class="kpi-val gold-text"><?= $leaveCount ?></div>
    <div class="kpi-sub">day off / other</div>
  </div>
</div>

<div class="section-title">Attendance List — <?= date('d M Y') ?></div>
<div class="card">
  <div class="table-wrap">
  <table class="data-table">
    <thead>
      <tr>
        <th>Employee ID</th>
        <th>First Name</th>
        <th>Last Name</th>
        <th>Date</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
      <?php foreach ($data as $row):
        $s = strtolower($row['STATUS']);
        $badgeClass = $s === 'present'      ? 'badge-green'
                    : ($s === 'absent'      ? 'badge-red'
                    : 'badge-gold');
      ?>
      <tr>
        <td class="muted-text" style="font-family:var(--mono)"><?= htmlspecialchars($row['EMPLOYEE_ID']) ?></td>
        <td style="font-weight:500"><?= htmlspecialchars($row['FIRST_NAME']) ?></td>
        <td><?= htmlspecialchars($row['LAST_NAME']) ?></td>
        <td style="font-family:var(--mono);font-size:12px"><?= htmlspecialchars($row['ATTENDANCE_DATE']) ?></td>
        <td><span class="badge <?= $badgeClass ?>"><?= htmlspecialchars($row['STATUS']) ?></span></td>
      </tr>
      <?php endforeach; ?>
    </tbody>
  </table>
</div>

<?php require 'footer.php'; ?>
