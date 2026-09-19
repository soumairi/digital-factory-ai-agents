<?php
namespace Reviewer;
require_once __DIR__.'/../../common/AdapterTestCase.php';
use Illuminate\Support\Facades\DB;
class BE002Test extends AdapterTestCase
{
    public function test_BE002_strict_boundaries_unknown_nested_hostile_and_no_writes(): void {
        foreach ([['name'=>'x','quantity'=>0],['name'=>str_repeat('x',100),'quantity'=>1000,'description'=>str_repeat('d',500)]] as $v) $this->req('POST','products',$v)->assertCreated();
        $valid=['name'=>'x','quantity'=>1];
        $bad=[[],['name'=>'x'],['quantity'=>1],['name'=>'','quantity'=>1],['name'=>123,'quantity'=>1],['name'=>str_repeat('x',101),'quantity'=>1]];
        foreach([-1,1001,1.5,'1',true,null,[],"1 OR 1=1",'<script>'] as $q) $bad[]=['name'=>'x','quantity'=>$q];
        foreach([['description'=>str_repeat('d',501)],['description'=>['nested'=>'x']],['extra'=>1],['name'=>['nested'=>'x']],['quantity'=>['value'=>1]],['role'=>'admin']] as $extra) $bad[]=array_merge($valid,$extra);
        foreach($bad as $payload) {
            $before=DB::table('products')->get()->toJson();
            $this->req('POST','products',$payload)->assertStatus(422)->assertExactJson(['message'=>'Invalid input.']);
            $this->assertSame($before,DB::table('products')->get()->toJson());
        }
        $this->req('POST','products',['name'=>"' OR 1=1 -- <script>",'quantity'=>1])->assertCreated();
        $this->assertDatabaseCount('products',3);
        app('auth')->forgetGuards();
        $this->call('POST','/api/eval/products',[],[],[],['CONTENT_TYPE'=>'application/json','HTTP_ACCEPT'=>'application/json','PHP_AUTH_USER'=>$this->actors[1]->email,'PHP_AUTH_PW'=>$this->password],'{broken')->assertStatus(422)->assertDontSee('trace');
        $this->assertDatabaseCount('products',3);
    }

    public function test_BE002_complete_normalization_matrix_and_state(): void {
        foreach(['name','quantity'] as $field) {
            $payload=['name'=>'Valid','quantity'=>1];unset($payload[$field]);$this->reject('POST','products',$payload,'products');
            $values=$field==='name'?$this->invalidText():[null,'','   ',-1,1001,1.5,'1',true,[],['x'=>1]];
            foreach($values as $value) $this->reject('POST','products',array_replace(['name'=>'Valid','quantity'=>1],[$field=>$value]),'products');
        }
        foreach([null,[],['x'=>1],str_repeat('x',501)] as $value) $this->reject('POST','products',['name'=>'Valid','quantity'=>1,'description'=>$value],'products');
        foreach(['extra'=>1,'nested'=>['x'=>1],'attributes.role'=>'editor'] as $key=>$value) $this->reject('POST','products',['name'=>'Valid','quantity'=>1,$key=>$value],'products');
        foreach(['','   ',str_repeat('x',500)] as $description) {
            $response=$this->req('POST','products',['name'=>'Valid','quantity'=>0,'description'=>$description])->assertCreated();
            $this->assertSame(['id','name','quantity','description'],array_keys($response->json()));
            $response->assertJsonPath('description',trim($description));
            $this->assertDatabaseHas('products',['id'=>$response->json('id'),'quantity'=>0,'description'=>trim($description)]);
        }
        $this->req('POST','products',['name'=>'Valid','quantity'=>1],null)->assertUnauthorized();
    }
}
