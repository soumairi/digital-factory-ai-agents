<?php
namespace Tests\Feature;
require_once __DIR__.'/../../reviewer/common/AdapterTestCase.php';
use Illuminate\Support\Facades\DB;
class CampaignImplementationTest extends \Reviewer\AdapterTestCase {
    public function test_owner_scoped_ordered_pages_and_invalid_sizes(): void {
        for ($i=1;$i<=42;$i++) DB::table('records')->insert(['id'=>$i,'owner_id'=>$i%2?1:2,'title'=>'Same']);
        $this->req('GET','records')->assertJsonCount(20,'data')->assertJsonPath('total',21);
        $r=$this->req('GET','records?page=2&per_page=10')->assertOk()->assertJsonPath('total',21);
        $this->assertSame(range(21,39,2),array_column($r->json('data'),'id'));
        foreach (['per_page=101','per_page=','page=0','page[]=1'] as $query) $this->req('GET','records?'.$query)->assertStatus(422);
        $this->assertDatabaseCount('records',42);
    }
}
