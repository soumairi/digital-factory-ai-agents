<?php
namespace Tests\Feature;
require_once __DIR__.'/../../reviewer/common/AdapterTestCase.php';
use Illuminate\Support\Facades\DB;
class CampaignImplementationTest extends \Reviewer\AdapterTestCase {
    public function test_created_note_is_owned_private_and_deletable(): void {
        $created = $this->req('POST','notes',['title'=>'Campaign note','body'=>'Body'])->assertCreated();
        $id = $created->json('id');
        $this->assertDatabaseHas('notes',['id'=>$id,'owner_id'=>1,'title'=>'Campaign note']);
        $before = $this->state('notes');
        $this->req('DELETE',"notes/$id",[],2)->assertNotFound()->assertJsonMissingPath('title');
        $this->assertSame($before,$this->state('notes'));
        $this->req('PATCH',"notes/$id",['title'=>'Revised','body'=>'New'])->assertExactJson(['id'=>$id,'title'=>'Revised','body'=>'New']);
        $this->req('GET',"notes/$id")->assertJsonMissingPath('owner_id')->assertJsonPath('title','Revised');
        $this->req('DELETE',"notes/$id")->assertNoContent();
        $this->assertDatabaseMissing('notes',['id'=>$id]);
        $this->req('GET',"notes/$id")->assertNotFound();
    }
}
