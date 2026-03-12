<?php
require_once 'config.php';
$current = 'view9';
$conn = getDB();

$data = queryAll($conn, "SELECT * FROM vw_active_recruitment ORDER BY department_name, position_name");
oci_close($conn);

require 'navbar.php';
?>

<div class="card-title">Active Recruitment</div>
<div class="card-sub">Open positions currently being recruited — View: <code style="color:var(--cyan);font-family:var(--mono);font-size:11px">vw_active_recruitment</code></div>

<!-- KPI -->
<div class="kpi-row cols-3" style="margin-bottom:28px">
  <div class="kpi-card accent-gold" data-icon="&#xF0B1;">
    <div class="kpi-label">Open Positions</div>
    <div class="kpi-val gold-text"><?= count($data) ?></div>
    <div class="kpi-sub">active job listings</div>
  </div>
  <div class="kpi-card accent-cyan" data-icon="&#xF1AD;">
    <div class="kpi-label">Departments Hiring</div>
    <div class="kpi-val cyan-text"><?= count(array_unique(array_column($data, 'DEPARTMENT_NAME'))) ?></div>
    <div class="kpi-sub">unique departments</div>
  </div>
  <div class="kpi-card accent-green" data-icon="&#xF0E0;">
    <div class="kpi-label">Contact Points</div>
    <div class="kpi-val green-text"><?= count(array_unique(array_column($data, 'CONTACT_EMAIL'))) ?></div>
    <div class="kpi-sub">unique contact emails</div>
  </div>
</div>

<div class="section-title">Job Listings</div>
<div class="card">
  <div class="table-wrap">
  <table class="data-table">
    <thead>
      <tr>
        <th>#</th>
        <th>Department</th>
        <th>Position</th>
        <th>Contact Email</th>
      </tr>
    </thead>
    <tbody>
      <?php foreach ($data as $i => $row): ?>
      <tr>
        <td><span class="rank rank-n"><?= $i+1 ?></span></td>
        <td><span class="badge badge-cyan"><?= htmlspecialchars($row['DEPARTMENT_NAME']) ?></span></td>
        <td style="font-weight:500"><?= htmlspecialchars($row['POSITION_NAME']) ?></td>
        <td style="font-family:var(--mono);font-size:11px;color:var(--muted)"><?= htmlspecialchars($row['CONTACT_EMAIL']) ?></td>
      </tr>
      <?php endforeach; ?>
    </tbody>
  </table>
</div>

<?php require 'footer.php'; ?>
