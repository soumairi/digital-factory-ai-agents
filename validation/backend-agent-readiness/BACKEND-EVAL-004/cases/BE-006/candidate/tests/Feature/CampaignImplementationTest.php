<?php
namespace Tests\Feature;
require_once __DIR__.'/../../reviewer/common/AdapterTestCase.php';
use Illuminate\Support\Facades\DB;
class CampaignImplementationTest extends \Reviewer\AdapterTestCase {
    public function test_reservation_failure_then_success_preserves_atomicity(): void {
        app()->instance('eval.fail-between-writes',true);
        $this->req('POST','reservations',['quantity'=>4])->assertStatus(500)->assertExactJson(['message'=>'Reservation failed.']);
        $this->assertDatabaseHas('inventory',['id'=>1,'stock'=>10]);
        $this->assertDatabaseCount('reservations',0);
        app()->instance('eval.fail-between-writes',false);
        $this->req('POST','reservations',['quantity'=>10])->assertCreated();
        $this->assertDatabaseHas('inventory',['id'=>1,'stock'=>0]);
        $this->assertDatabaseHas('reservations',['inventory_id'=>1,'quantity'=>10]);
        $this->req('POST','reservations',['quantity'=>1])->assertStatus(409);
        $this->assertDatabaseCount('reservations',1);
    }
}
