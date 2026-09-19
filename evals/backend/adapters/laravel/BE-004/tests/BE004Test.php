<?php
namespace Reviewer;
require_once __DIR__.'/../../common/AdapterTestCase.php';
use Illuminate\Support\Facades\DB;
class BE004Test extends AdapterTestCase
{
    public function test_BE004_same_tenant_cross_tenant_nested_lists_and_unchanged_state(): void {
        for($actor=1;$actor<=4;$actor++) {
            $this->req('GET','documents',[],$actor)->assertExactJson(['data'=>[['id'=>$actor,'title'=>"Document$actor"]],'total'=>1]);
            $this->req('GET',"documents/$actor",[],$actor)->assertOk();
            $this->req('GET',"documents/$actor/attachments/$actor",[],$actor)->assertExactJson(['id'=>$actor,'name'=>"Attachment$actor"]);
            $this->req('PATCH',"documents/$actor",['title'=>"Document$actor"],$actor)->assertOk();
            foreach(array_diff([1,2,3,4],[$actor]) as $foreign) {
                $before=DB::table('documents')->get()->toJson();
                $this->req('GET',"documents/$foreign",[],$actor)->assertNotFound()->assertJsonMissingPath('title');
                $this->req('PATCH',"documents/$foreign",['title'=>'attack'],$actor)->assertNotFound();
                $this->req('GET',"documents/$actor/attachments/$foreign",[],$actor)->assertNotFound()->assertJsonMissingPath('name');
                $this->assertSame($before,DB::table('documents')->get()->toJson());
            }
        }
    }

    public function test_BE004_identifier_schema_and_protected_keys(): void {
        foreach(['0','-1','1.5','abc','999999','%5B1%5D','1%20OR%201=1'] as $id) {
            $before=$this->state('documents');
            foreach(['GET','PATCH'] as $method) $this->req($method,'documents/'.$id,['title'=>'Attack'])->assertNotFound();
            $this->assertSame($before,$this->state('documents'));
        }
        $this->reject('PATCH','documents/1',[],'documents');
        foreach($this->invalidText() as $value) $this->reject('PATCH','documents/1',['title'=>$value],'documents');
        foreach(['owner_id','tenant_id'] as $key) $this->reject('PATCH','documents/1',['title'=>'Attack',$key=>2],'documents');
        $this->req('GET','documents/1',[],null)->assertUnauthorized();
        $this->req('GET','documents/1')->assertExactJson(['id'=>1,'title'=>'Document1']);
    }
}
