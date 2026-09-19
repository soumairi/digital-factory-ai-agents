<?php
// Disposable SQLite process race. No external service or customer data.
use Illuminate\Contracts\Console\Kernel;
use Illuminate\Support\Facades\DB;
require __DIR__.'/../vendor/autoload.php';
$app=require __DIR__.'/../bootstrap/app.php';
$app->make(Kernel::class)->bootstrap();
if (!str_starts_with(realpath(__DIR__.'/../..'), '/private/tmp/backend-eval-001-')) throw new RuntimeException('Wrong sandbox');
$mode=$argv[1]??'parent';
if($mode==='worker') {
    $db=$argv[2]; $slot=$argv[3];
    if(dirname($db)!==realpath(__DIR__.'/../..') || !str_starts_with(basename($db),'race-')) throw new RuntimeException('Wrong database');
    config(['database.connections.sqlite.database'=>$db]); DB::purge('sqlite'); DB::statement('PRAGMA busy_timeout = 5000');
    touch($db.'.ready-'.$slot);
    $deadline=microtime(true)+10;
    while(!file_exists($db.'.go')) { if(microtime(true)>$deadline) throw new RuntimeException('Barrier timed out'); usleep(1000); }
    try { $id=app(\App\Actions\EvalReserve::class)->execute(7); echo json_encode(['status'=>201,'id'=>$id]); }
    catch(DomainException $e) { echo json_encode(['status'=>409]); }
    exit;
}
$results=[];
for($round=0;$round<5;$round++) {
    $db=realpath(__DIR__.'/../..').'/race-'.bin2hex(random_bytes(8)).'.sqlite';
    $pdo=new PDO('sqlite:'.$db);
    $pdo->exec('CREATE TABLE inventory (id INTEGER PRIMARY KEY, stock INTEGER NOT NULL CHECK(stock >= 0)); CREATE TABLE reservations (id INTEGER PRIMARY KEY, inventory_id INTEGER NOT NULL, quantity INTEGER NOT NULL); INSERT INTO inventory VALUES(1,10)');
    $children=[];
    foreach([1,2] as $slot) {
        $pipes=[];
        $process=proc_open([PHP_BINARY,'-n',__FILE__,'worker',$db,(string)$slot],[0=>['pipe','r'],1=>['pipe','w'],2=>['pipe','w']],$pipes,dirname(__DIR__));
        fclose($pipes[0]); $children[]=[$process,$pipes];
    }
    $deadline=microtime(true)+10;
    while(!file_exists($db.'.ready-1')||!file_exists($db.'.ready-2')) { if(microtime(true)>$deadline) throw new RuntimeException('Workers not ready'); usleep(1000); }
    touch($db.'.go'); $statuses=[];
    foreach($children as [$process,$pipes]) {
        $out=stream_get_contents($pipes[1]);$err=stream_get_contents($pipes[2]);fclose($pipes[1]);fclose($pipes[2]);$code=proc_close($process);
        if($code!==0||$err!=='') throw new RuntimeException('Worker failure');
        $statuses[]=json_decode($out,true,512,JSON_THROW_ON_ERROR)['status'];
    }
    sort($statuses);$stock=(int)$pdo->query('SELECT stock FROM inventory')->fetchColumn();$count=(int)$pdo->query('SELECT COUNT(*) FROM reservations')->fetchColumn();
    if($statuses!==[201,409]||$stock!==3||$count!==1) throw new RuntimeException('Concurrency invariant failed');
    $results[]=['round'=>$round+1,'statuses'=>$statuses,'stock'=>$stock,'reservation_count'=>$count];
}
echo json_encode(['engine'=>'SQLite','competing_processes'=>2,'barrier'=>'Both workers ready before release','results'=>$results],JSON_PRETTY_PRINT).PHP_EOL;
