<?php
namespace Tests\Feature;
require_once __DIR__.'/../../reviewer/common/AdapterTestCase.php';
use Illuminate\Support\Facades\DB;
class CampaignImplementationTest extends \Reviewer\AdapterTestCase {
    public function test_product_schema_matrix_and_literal_text(): void {
        foreach ([[],['name'=>null,'quantity'=>1],['name'=>'   ','quantity'=>1],['name'=>'x','quantity'=>'1'],['name'=>'x','quantity'=>1001],['name'=>'x','quantity'=>1,'extra'=>['role'=>'editor']]] as $payload) {
            $this->reject('POST','products',$payload,'products');
        }
        $title = "' OR 1=1 --";
        $id=$this->req('POST','products',['name'=>$title,'quantity'=>0,'description'=>''])->assertCreated()->assertJsonPath('description','')->json('id');
        $this->assertDatabaseHas('products',['id'=>$id,'name'=>$title,'quantity'=>0]);
        $this->assertDatabaseCount('products',1);
    }
}
