<?php
namespace Tests\Feature;
require_once __DIR__.'/../../reviewer/common/AdapterTestCase.php';
use Illuminate\Support\Facades\DB;
class CampaignImplementationTest extends \Reviewer\AdapterTestCase {
    public function test_document_persistence_and_nested_boundary(): void {
        $foreign=$this->state('documents');
        foreach ([2,3,4] as $actor) {
            $this->req('PATCH','documents/1',['title'=>'Denied'],$actor)->assertNotFound();
            $this->assertSame($foreign,$this->state('documents'));
        }
        $this->req('PATCH','documents/1',['title'=>'Durable'])->assertExactJson(['id'=>1,'title'=>'Durable']);
        $this->assertDatabaseHas('documents',['id'=>1,'title'=>'Durable','owner_id'=>1,'tenant_id'=>1]);
        $this->req('GET','documents/1')->assertJsonPath('title','Durable');
        $this->req('GET','documents/1/attachments/2')->assertNotFound()->assertJsonMissingPath('name');
        $this->req('GET','documents')->assertExactJson(['data'=>[['id'=>1,'title'=>'Durable']],'total'=>1]);
    }
}
