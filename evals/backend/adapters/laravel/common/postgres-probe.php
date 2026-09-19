<?php
use Illuminate\Contracts\Console\Kernel;
use Illuminate\Support\Facades\DB;
require dirname(__DIR__,2).'/vendor/autoload.php';
$app=require dirname(__DIR__,2).'/bootstrap/app.php';
$app->make(Kernel::class)->bootstrap();
$root=realpath(dirname(__DIR__,3));
if(!str_starts_with($root,'/private/tmp/laravel-adapter-')||!is_file($root.'/.laravel-adapter-workspace.json'))throw new RuntimeException('Unowned workspace');
$socket=$root.'/pgsocket';
if(realpath($socket)!==$socket)throw new RuntimeException('Invalid socket path');
config(['database.default'=>'pgsql','database.connections.pgsql'=>['driver'=>'pgsql','host'=>$socket,'port'=>55432,'database'=>'adapter_fixture','username'=>'adapter_fixture','password'=>'','charset'=>'utf8','prefix'=>'','search_path'=>'public','sslmode'=>'disable']]);
DB::purge('pgsql');
DB::statement('CREATE TABLE inventory (id BIGINT PRIMARY KEY,stock INTEGER NOT NULL CHECK(stock>=0))');
DB::statement('CREATE TABLE reservations (id BIGSERIAL PRIMARY KEY,inventory_id BIGINT NOT NULL,quantity INTEGER NOT NULL)');
DB::table('inventory')->insert(['id'=>1,'stock'=>10]);
$action=app(\App\Actions\EvalReserve::class);
$action->execute(3);
app()->instance('eval.fail-between-writes',true);
try{$action->execute(2);throw new LogicException('Failure injection was not triggered');}catch(RuntimeException $e){}
if((int)DB::table('inventory')->value('stock')!==7||DB::table('reservations')->count()!==1)throw new LogicException('Rollback invariant failed');
app()->instance('eval.fail-between-writes',false);
try{$action->execute(8);throw new LogicException('Shortage was accepted');}catch(DomainException $e){}
if((int)DB::table('inventory')->value('stock')!==7)throw new LogicException('Shortage mutated stock');
echo json_encode(['engine'=>'PostgreSQL','success'=>'PASS','rollback'=>'PASS','shortage'=>'PASS','concurrency'=>'NOT EXECUTED']).PHP_EOL;
