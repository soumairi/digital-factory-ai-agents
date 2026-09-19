<?php

use Illuminate\Contracts\Console\Kernel;
use Illuminate\Foundation\Application;

require __DIR__.'/../vendor/autoload.php';
$app = require __DIR__.'/../bootstrap/app.php';
$app->make(Kernel::class)->bootstrap();
$keys = ['app.env', 'app.debug', 'database.default', 'database.connections.sqlite.database', 'database.connections.sqlite.url', 'cache.default', 'session.driver', 'mail.default', 'queue.default', 'queue.failed.driver', 'filesystems.default', 'filesystems.disks.local.root', 'logging.default', 'auth.defaults.guard', 'auth.guards.web.driver', 'auth.providers.users.driver'];
$out = ['php' => PHP_VERSION, 'laravel' => Application::VERSION, 'pdo_drivers' => PDO::getAvailableDrivers(), 'configuration_cached' => $app->configurationIsCached()];
foreach ($keys as $key) {
    $out[$key] = config($key);
}
if ($out['database.default'] !== 'sqlite' || $out['database.connections.sqlite.database'] !== ':memory:' || ! empty($out['database.connections.sqlite.url'])) {
    throw new RuntimeException('Unsafe database target');
}
$out['database_probe'] = $app->make('db')->connection()->select('PRAGMA database_list');
$out['database_tables'] = $app->make('db')->connection()->select("SELECT name FROM sqlite_master WHERE type='table'");
echo json_encode($out, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES).PHP_EOL;
