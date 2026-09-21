<?php
namespace Tests\Feature;
require_once __DIR__.'/../../reviewer/common/AdapterTestCase.php';
use Illuminate\Support\Facades\DB;
class CampaignImplementationTest extends \Reviewer\AdapterTestCase {
    public function test_report_permissions_are_server_owned_and_durable(): void {
        $before=$this->state('reports');
        $this->req('PATCH','report/1',['title'=>'Denied'],null)->assertUnauthorized();
        $this->req('PATCH','report/1',['title'=>'Denied','role'=>'editor'])->assertForbidden();
        $this->assertSame($before,$this->state('reports'));
        $this->req('GET','report/1')->assertExactJson(['id'=>1,'title'=>'Report']);
        $this->req('PATCH','report/1',['title'=>'Campaign edit'],2)->assertExactJson(['id'=>1,'title'=>'Campaign edit']);
        $this->assertDatabaseHas('reports',['id'=>1,'title'=>'Campaign edit']);
        $this->req('GET','report/1')->assertJsonPath('title','Campaign edit');
    }
}
