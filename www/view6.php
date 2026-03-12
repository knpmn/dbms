<?php
require_once 'config.php';
$current = 'view6';
$conn = getDB();

$data = queryAll($conn, "SELECT * FROM vw_penalty_history ORDER BY penalty_date DESC");
oci_close($conn);

$levelCounts = array_count_values(array_column($data, 'PENALTY_LEVEL'));

require 'navbar.php';
?>

<div class="card-title">Penalty History</div>
<div class="card-sub">Employee disciplinary records — View: <code style="color:var(--cyan);font-family:var(--mono);font-size:11px">vw_penalty_history</code></div>

<!-- KPI -->
<div class="kpi-row cols-3" style="margin-bottom:28px">
  <div class="kpi-card accent-red" data-icon="&#xF071;">
    <div class="kpi-label">Total Penalties</div>
    <div class="kpi-val red-text"><?= count($data) ?></div>
    <div class="kpi-sub">all records</div>
  </div>
  <div class="kpi-card accent-gold" data-icon="&#xF0C0;">
    <div class="kpi-label">Employees Penalized</div>
    <div class="kpi-val gold-text"><?= count(array_unique(array_column($data, 'EMPLOYEE_ID'))) ?></div>
    <div class="kpi-sub">unique employees</div>
  </div>
  <div class="kpi-card accent-cyan" data-icon="&#xF03A;">
    <div class="kpi-label">Penalty Types</div>
    <div class="kpi-val cyan-text"><?= count($levelCounts) ?></div>
    <div class="kpi-sub">distinct levels</div>
  </div>
</div>

<div class="section-title">Penalty Records</div>
<div class="card">
  <div class="table-wrap">
  <table class="data-table">
    <thead>
      <tr>
        <th>Penalty ID</th>
        <th>Employee ID</th>
        <th>First Name</th>
        <th>Last Name</th>
        <th>Penalty Date</th>
        <th>Level</th>
      </tr>
    </thead>
    <tbody>
      <?php foreach ($data as $row):
        $level = strtolower($row['PENALTY_LEVEL']);
        $badgeClass = str_contains($level, 'warning') ? 'badge-gold'
                    : (str_contains($level, 'terminat') ? 'badge-red'
                    : (str_contains($level, 'suspension') ? 'badge-red'
                    : (str_contains($level, 'salary') ? 'badge-cyan'
                    : 'badge-muted')));
      ?>
      <tr>
        <td class="muted-text" style="font-family:var(--mono)"><?= htmlspecialchars($row['PENALTY_ID']) ?></td>
        <td class="muted-text" style="font-family:var(--mono)"><?= htmlspecialchars($row['EMPLOYEE_ID']) ?></td>
        <td style="font-weight:500"><?= htmlspecialchars($row['FIRST_NAME']) ?></td>
        <td><?= htmlspecialchars($row['LAST_NAME']) ?></td>
        <td style="font-family:var(--mono);font-size:12px"><?= htmlspecialchars($row['PENALTY_DATE']) ?></td>
        <td><span class="badge <?= $badgeClass ?>"><?= htmlspecialchars($row['PENALTY_LEVEL']) ?></span></td>
      </tr>
      <?php endforeach; ?>
    </tbody>
  </table>
</div>

<?php require 'footer.php'; ?>
