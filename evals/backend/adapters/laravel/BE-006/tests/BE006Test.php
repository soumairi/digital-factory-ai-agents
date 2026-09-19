<?php
namespace Reviewer;
require_once __DIR__.'/../../common/AdapterTestCase.php';
use Illuminate\Support\Facades\DB;
class BE006Test extends AdapterTestCase
{
    public function test_BE006_success_shortage_rollback_and_repeat(): void {
        $this->req('POST','reservations',['quantity'=>3])->assertCreated();
        $this->assertDatabaseHas('inventory',['id'=>1,'stock'=>7]); $this->assertDatabaseCount('reservations',1);
        $this->assertDatabaseHas('reservations',['inventory_id'=>1,'quantity'=>3]);
        app()->instance('eval.fail-between-writes',true);
        $response=$this->req('POST','reservations',['quantity'=>2]);
        $this->assertDatabaseHas('inventory',['id'=>1,'stock'=>7]);
        $response->assertStatus(500)->assertExactJson(['message'=>'Reservation failed.']); $this->assertDatabaseCount('reservations',1);
        app()->instance('eval.fail-between-writes',false);
        $this->req('POST','reservations',['quantity'=>8])->assertStatus(409); $this->assertDatabaseCount('reservations',1);
        $this->req('POST','reservations',['quantity'=>7])->assertCreated();
        $this->req('POST','reservations',['quantity'=>7])->assertStatus(409);
        $this->assertDatabaseHas('inventory',['id'=>1,'stock'=>0]); $this->assertDatabaseCount('reservations',2);
        $this->assertSame(10,(int)DB::table('reservations')->sum('quantity'));
        $this->assertDatabaseHas('reservations',['inventory_id'=>1,'quantity'=>7]);
    }

    public function test_BE006_quantity_normalization_and_persistence(): void {
        $before=$this->state('inventory');
        $this->reject('POST','reservations',[],'reservations');
        foreach([null,'','   ',0,-1,1001,1.5,'1',true,[],['x'=>1]] as $q) $this->reject('POST','reservations',['quantity'=>$q],'reservations');
        $this->assertSame($before,$this->state('inventory'));
        $this->req('POST','reservations',['quantity'=>1],null)->assertUnauthorized();
        $this->req('POST','reservations',['quantity'=>1000])->assertStatus(409);
    }
}
