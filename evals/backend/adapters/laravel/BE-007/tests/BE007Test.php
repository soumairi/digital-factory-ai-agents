<?php
namespace Reviewer;
require_once __DIR__.'/../../common/AdapterTestCase.php';
use Illuminate\Support\Facades\DB;
class BE007Test extends AdapterTestCase
{
    public function test_BE007_pagination_traversal_scope_and_resource_limits(): void {
        for($i=1;$i<=250;$i++) DB::table('records')->insert(['id'=>$i,'owner_id'=>$i%2?1:2,'title'=>'Duplicate']);
        $this->req('GET','records')->assertOk()->assertJsonCount(20,'data')->assertJsonPath('total',125);
        $this->req('GET','records?per_page=100')->assertOk()->assertJsonCount(100,'data');
        $ids=[];
        for($page=1;$page<=7;$page++) $ids=array_merge($ids,array_column($this->req('GET',"records?page=$page")->assertOk()->json('data'),'id'));
        $this->assertSame(range(1,249,2),$ids);
        $this->req('GET','records?page=1000000')->assertOk()->assertJsonCount(0,'data')->assertJsonPath('total',125);
        $this->req('GET','records',[],2)->assertJsonPath('total',125)->assertJsonPath('data.0.id',2);
        foreach(['page=0','page=-1','page=1.5','page[]=1','page=01','page=1000001','per_page=101','per_page=0','per_page=1000000000000','per_page=1e2','per_page=abc','per_page=','owner_id=2'] as $q) $this->req('GET',"records?$q")->assertStatus(422);
        $this->assertDatabaseCount('records',250);
    }

    public function test_BE007_raw_null_whitespace_types_and_metadata(): void {
        for($i=1;$i<=250;$i++) DB::table('records')->insert(['id'=>$i,'owner_id'=>$i%2?1:2,'title'=>'Duplicate']);
        $response=$this->req('GET','records')->assertOk()->assertJsonPath('page',1)->assertJsonPath('per_page',20)->assertJsonPath('total',125);
        $this->assertSame(['data','total','page','per_page'],array_keys($response->json()));
        foreach($response->json('data') as $item) $this->assertSame(['id','title'],array_keys($item));
        $this->req('GET','records?per_page=7&page=2')->assertJsonCount(7,'data')->assertJsonPath('page',2)->assertJsonPath('per_page',7)->assertJsonPath('data.0.id',15);
        foreach(['page','per_page'] as $key) foreach([null,'','   ',0,-1,'1.5',[],['x'=>1]] as $value) {
            app('auth')->forgetGuards();$before=$this->state('records');
            $res=$this->call('GET','/api/eval/records',[$key=>$value],[],[],['HTTP_ACCEPT'=>'application/json','PHP_AUTH_USER'=>$this->actors[1]->email,'PHP_AUTH_PW'=>$this->password]);
            $res->assertStatus(422)->assertExactJson(['message'=>'Invalid input.']);$this->assertSame($before,$this->state('records'));
        }
        $this->req('GET','records',[],null)->assertUnauthorized();
    }
}
