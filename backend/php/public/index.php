<?php

declare(strict_types=1);

$host = getenv('DB_HOST') ?: '127.0.0.1';
$port = (int) (getenv('DB_PORT') ?: 3306);
$database = getenv('DB_NAME') ?: 'led_test';
$user = getenv('DB_USER') ?: 'led_user';
$password = getenv('DB_PASSWORD') ?: 'led_password';
$databaseStatus = 'connected';

try {
    $pdo = new PDO(
        "mysql:host={$host};port={$port};dbname={$database};charset=utf8mb4",
        $user,
        $password,
        [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION],
    );
    $pdo->query('SELECT 1');
} catch (Throwable $error) {
    $databaseStatus = 'unavailable';
}
?>
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>LED Test Web Stack</title>
</head>
<body>
    <h1>LED Test Web Stack</h1>
    <p>Apache and PHP are running.</p>
    <p>MariaDB: <strong><?= htmlspecialchars($databaseStatus) ?></strong></p>
</body>
</html>
