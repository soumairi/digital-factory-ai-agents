<?php
namespace App\Actions;
use Illuminate\Support\Facades\DB;
class EvalReserve {
    public function execute(int $quantity): int {
        if($quantity<1||$quantity>1000) throw new \InvalidArgumentException('Invalid quantity');
        return DB::transaction(function() use($quantity) {
            if(DB::table('inventory')->where('id',1)->where('stock','>=',$quantity)->decrement('stock',$quantity)!==1) throw new \DomainException('Insufficient stock');
            if(app()->bound('eval.fail-between-writes')&&app('eval.fail-between-writes')===true) throw new \RuntimeException('Synthetic injected failure');
            return DB::table('reservations')->insertGetId(['inventory_id'=>1,'quantity'=>$quantity]);
        });
    }
}
