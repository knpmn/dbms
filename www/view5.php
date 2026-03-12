<?php
require_once 'config.php';
$current = 'view5';
$conn = getDB();

$data = queryAll($conn, "SELECT * FROM vw_contract_expiry_alert ORDER BY days_remaining ASC");
oci_close($conn);

$expiredCount  = count(array_filter($data, fn($r) => $r['DAYS_REMAINING'] <= 0));
$urgentCount   = count(array_filter($data, fn($r) => $r['DAYS_REMAINING'] > 0 && $r['DAYS_REMAINING'] <= 30));
$activeCount   = count(array_filter($data, fn($r) => $r['DAYS_REMAINING'] > 30));

require 'navbar.php';
?>

<div class="card-title">Contract Expiry Alert</div>
<div class="card-sub">Track employee contract end dates and days remaining — View: <code style="color:var(--cyan);font-family:var(--mono);font-size:11px">vw_contract_expiry_alert</code></div>

<!-- KPI -->
<div class="kpi-row cols-3" style="margin-bottom:28px">
  <div class="kpi-card accent-red" data-icon="&#xF06A;">
    <div class="kpi-label">Expired / Overdue</div>
    <div class="kpi-val red-text"><?= $expiredCount ?></div>
    <div class="kpi-sub">contracts past end date</div>
  </div>
  <div class="kpi-card accent-gold" data-icon="&#xF071;">
    <div class="kpi-label">Expiring Soon (&le;30d)</div>
    <div class="kpi-val gold-text"><?= $urgentCount ?></div>
    <div class="kpi-sub">need urgent renewal</div>
  </div>
  <div class="kpi-card accent-green" data-icon="&#xF058;">
    <div class="kpi-label">Active (&gt;30d)</div>
    <div class="kpi-val green-text"><?= $activeCount ?></div>
    <div class="kpi-sub">contracts healthy</div>
  </div>
</div>

<div class="section-title">Contract Details</div>
<div class="card">
  <div class="table-wrap">
  <table class="data-table">
    <thead>
      <tr>
        <th>Contract ID</th>
        <th>Employee ID</th>
        <th>First Name</th>
        <th>Last Name</th>
        <th>Type</th>
        <th>End Date</th>
        <th class="num">Days Remaining</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
      <?php foreach ($data as $row):
        $days = (int)$row['DAYS_REMAINING'];
        if ($days <= 0) {
            $statusBadge = 'badge-red'; $statusLabel = 'Expired';
        } elseif ($days <= 30) {
            $statusBadge = 'badge-gold'; $statusLabel = 'Urgent';
        } else {
            $statusBadge = 'badge-green'; $statusLabel = 'Active';
        }
      ?>
      <tr>
        <td class="muted-text" style="font-family:var(--mono)"><?= htmlspecialchars($row['CONTRACT_ID']) ?></td>
        <td class="muted-text" style="font-family:var(--mono)"><?= htmlspecialchars($row['EMPLOYEE_ID']) ?></td>
        <td style="font-weight:500"><?= htmlspecialchars($row['FIRST_NAME']) ?></td>
        <td><?= htmlspecialchars($row['LAST_NAME']) ?></td>
        <td><?= htmlspecialchars($row['CONTRACT_TYPE']) ?></td>
        <td style="font-family:var(--mono);font-size:12px"><?= htmlspecialchars($row['END_DATE']) ?></td>
        <td class="num <?= $days <= 0 ? 'red-text' : ($days <= 30 ? 'gold-text' : 'green-text') ?>" style="font-weight:600"><?= $days ?></td>
        <td><span class="badge <?= $statusBadge ?>"><?= $statusLabel ?></span></td>
      </tr>
      <?php endforeach; ?>
    </tbody>
  </table>
</div>

<?php require 'footer.php'; ?>
