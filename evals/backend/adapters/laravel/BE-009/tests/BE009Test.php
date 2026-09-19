<?php
namespace Reviewer;
require_once __DIR__.'/../../common/AdapterTestCase.php';
use Illuminate\Support\Facades\DB;
class BE009Test extends AdapterTestCase
{
    public function test_BE009_six_negative_categories_and_methods(): void {
        $id=$this->req('POST','notes',['title'=>'Safe','body'=>'Body'])->assertCreated()->json('id');
        foreach(['GET','PATCH','DELETE'] as $m) {
            $this->req($m,"notes/$id",['title'=>'x','body'=>'x'],null)->assertUnauthorized();
            $this->req($m,"notes/$id",['title'=>'x','body'=>'x'],2)->assertNotFound();
        }
        $this->req('PATCH','report/1',['title'=>'Attack'])->assertForbidden();
        foreach([[],['title'=>[],'body'=>'x'],['title'=>'x','body'=>str_repeat('x',501)],['title'=>'x','body'=>'x','owner_id'=>2],['title'=>'x','body'=>'x','role'=>'editor']] as $payload) $this->req('PATCH',"notes/$id",$payload)->assertStatus(422);
        $this->req('GET','notes/1%20OR%201=1')->assertNotFound();
        $this->req('PUT',"notes/$id",['title'=>'Attack'])->assertStatus(405);
        $this->assertDatabaseHas('notes',['id'=>$id,'title'=>'Safe','body'=>'Body','owner_id'=>1]);
        $this->assertDatabaseHas('reports',['id'=>1,'title'=>'Report']);
        $this->assertDatabaseCount('notes',3);
    }
    public function test_BE009_sensitive_privilege_side_effects_and_excessive_resources(): void {
        $before=$this->state('profiles');
        $response=$this->req('PATCH','profile',['display_name'=>'Attack','is_admin'=>true]);
        $this->assertSame($before,$this->state('profiles'),'Protected state changed');
        $response->assertStatus(422);
        foreach($this->invalidText() as $v) $this->reject('PATCH','notes/1',['title'=>$v,'body'=>'Body'],'notes');
        foreach(['owner_id'=>2,'role'=>'editor','is_admin'=>true] as $k=>$v) $this->reject('PATCH','notes/1',['title'=>'x','body'=>'x',$k=>$v],'notes');
        $this->req('GET','records?per_page=1000000')->assertStatus(422);
        $this->req('GET','records?page=1%20OR%201=1')->assertStatus(422);
        $this->assertDatabaseHas('notes',['id'=>1,'owner_id'=>1,'title'=>'Seed1']);
    }
}
