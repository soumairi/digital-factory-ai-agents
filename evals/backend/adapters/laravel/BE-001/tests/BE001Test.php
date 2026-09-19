<?php
namespace Reviewer;
require_once __DIR__.'/../../common/AdapterTestCase.php';
use Illuminate\Support\Facades\DB;
class BE001Test extends AdapterTestCase
{
    public function test_BE001_crud_owner_scope_and_missing_resources(): void {
        $r=$this->req('POST','notes',['title'=>'Note','body'=>'Body'])->assertCreated(); $id=$r->json('id');
        $this->assertSame(['id','title','body'],array_keys($r->json()));
        $this->assertDatabaseHas('notes',['id'=>$id,'owner_id'=>1]);
        $this->req('GET',"notes/$id")->assertExactJson(['id'=>$id,'title'=>'Note','body'=>'Body']);
        foreach(['GET','PATCH','DELETE'] as $m) $this->req($m,"notes/$id",['title'=>'Foreign','body'=>'x'],2)->assertNotFound()->assertJsonMissingPath('title');
        $this->assertDatabaseHas('notes',['id'=>$id,'title'=>'Note','owner_id'=>1]);
        $this->req('PATCH',"notes/$id",['title'=>'Updated','body'=>'New'])->assertOk();
        $this->assertDatabaseHas('notes',['id'=>$id,'title'=>'Updated','body'=>'New']);
        $this->req('DELETE',"notes/$id")->assertNoContent(); $this->assertDatabaseMissing('notes',['id'=>$id]);
        foreach(['GET','PATCH','DELETE'] as $m) $this->req($m,"notes/$id",['title'=>'x','body'=>'x'])->assertNotFound();
    }

    public function test_BE001_input_initial_state_and_regression_controls(): void {
        $this->assertDatabaseHas('notes',['id'=>1,'owner_id'=>1,'title'=>'Seed1']);
        $this->assertDatabaseHas('notes',['id'=>2,'owner_id'=>2,'title'=>'Seed2']);
        foreach(['GET','PATCH','DELETE'] as $method) {
            $before=$this->state('notes');
            $this->req($method,'notes/1',['title'=>'x','body'=>'x'],null)->assertUnauthorized();
            $this->assertSame($before,$this->state('notes'));
        }
        $this->req('POST','notes',['title'=>'x','body'=>'x'],null)->assertUnauthorized();
        foreach(['title','body'] as $field) {
            $payload=['title'=>'Valid','body'=>'Valid']; unset($payload[$field]); $this->reject('POST','notes',$payload,'notes');
            foreach($this->invalidText() as $value) $this->reject('POST','notes',array_replace(['title'=>'Valid','body'=>'Valid'],[$field=>$value]),'notes');
        }
        foreach([['owner_id'=>2],['title'=>str_repeat('x',101)],['body'=>str_repeat('x',501)]] as $extra) $this->reject('POST','notes',array_replace(['title'=>'Valid','body'=>'Valid'],$extra),'notes');
        foreach([1,100] as $length) $this->req('POST','notes',['title'=>str_repeat('x',$length),'body'=>str_repeat('b',500)])->assertCreated();
    }
}
