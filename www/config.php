<?php
// ── Oracle OCI8 Connection ─────────────────────────────────────────
define('ORA_USER', getenv('ORA_USER') ?: 'AI_683380317_6');
define('ORA_PASS', getenv('ORA_PASS') ?: 'p1234');
define('ORA_HOST', getenv('ORA_HOST') ?: '10.199.8.14');
define('ORA_PORT', getenv('ORA_PORT') ?: '1726');
define('ORA_SID',  getenv('ORA_SID')  ?: 'ORCLCDB');

function getDB() {
    $dsn = '(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=' . ORA_HOST . ')(PORT=' . ORA_PORT . '))(CONNECT_DATA=(SID=' . ORA_SID . ')))';
    $conn = oci_connect(ORA_USER, ORA_PASS, $dsn);
    if (!$conn) {
        $e = oci_error();
        die('<div style="color:red;padding:20px">❌ Oracle Error: ' . htmlspecialchars($e['message']) . '</div>');
    }
    return $conn;
}

/**
 * Execute a SELECT query and return all rows as array of associative arrays.
 */
function queryAll($conn, string $sql): array {
    $stmt = oci_parse($conn, $sql);
    if (!$stmt) {
        $e = oci_error($conn);
        die('<div style="color:red;padding:20px">❌ Parse Error: ' . htmlspecialchars($e['message']) . '</div>');
    }
    if (!oci_execute($stmt, OCI_DEFAULT)) {
        $e = oci_error($stmt);
        die('<div style="color:red;padding:20px">❌ Execute Error: ' . htmlspecialchars($e['message']) . '</div>');
    }
    $rows = [];
    while ($r = oci_fetch_assoc($stmt)) {
        $rows[] = $r;
    }
    oci_free_statement($stmt);
    return $rows;
}

function num(float $n): string {
    return number_format($n, 0);
}
