<?php
namespace Reviewer;
require_once __DIR__.'/../../common/AdapterTestCase.php';
use Illuminate\Support\Facades\DB;
class BE008Test extends AdapterTestCase
{
    public function test_BE008_relationship_query_budget_and_correct_serialization(): void {
        foreach([1,2] as $tenant) {
            DB::table('authors')->insert(['id'=>$tenant,'tenant_id'=>$tenant,'name'=>"Author$tenant"]);
            DB::table('categories')->insert(['id'=>$tenant,'tenant_id'=>$tenant,'name'=>"Category$tenant"]);
            for($i=0;$i<55;$i++) DB::table('articles')->insert(['tenant_id'=>$tenant,'title'=>"Article$i",'author_id'=>$tenant,'category_id'=>$tenant]);
        }
        // Same-tenant article must never disclose a foreign relation.
        DB::table('articles')->insert(['tenant_id'=>1,'title'=>'Mismatch','author_id'=>2,'category_id'=>2]);
        $this->req('GET','articles')->assertOk()->assertJsonCount(20,'data');
        foreach([5,50] as $size) {
            DB::enableQueryLog(); DB::flushQueryLog();
            $r=$this->req('GET',"articles?per_page=$size")->assertOk()->assertJsonCount($size,'data')->assertJsonPath('total',56);
            $queries=array_filter(DB::getQueryLog(),fn($q)=>str_starts_with(strtolower($q['query']),'select')&&!str_contains($q['query'],'"users"'));
            $rel=array_filter($queries,fn($q)=>str_contains($q['query'],'"authors"')||str_contains($q['query'],'"categories"'));
            $this->assertLessThanOrEqual(4,count($queries)); $this->assertLessThanOrEqual(2,count($rel));
            foreach($r->json('data') as $a) { $this->assertSame(['id','title','author','category'],array_keys($a)); $this->assertSame(['id'=>1,'name'=>'Author1'],$a['author']); $this->assertSame(['id'=>1,'name'=>'Category1'],$a['category']); }
            fwrite(STDOUT,"\nQUERY_EVIDENCE size=$size domain=".count($queries).' relationships='.count($rel)."\n");
        }
        $this->req('GET','articles?page=2&per_page=50')->assertJsonPath('data.5.author',null)->assertJsonPath('data.5.category',null);
        $this->req('GET','articles?per_page=101')->assertStatus(422);
    }

    public function test_BE008_pagination_types_and_query_limit(): void {
        foreach(['page','per_page'] as $key) foreach([null,'','   ',0,-1,[],['x'=>1]] as $value) {
            app('auth')->forgetGuards();$before=$this->state('articles');
            $res=$this->call('GET','/api/eval/articles',[$key=>$value],[],[],['HTTP_ACCEPT'=>'application/json','PHP_AUTH_USER'=>$this->actors[1]->email,'PHP_AUTH_PW'=>$this->password]);
            $res->assertStatus(422);$this->assertSame($before,$this->state('articles'));
        }
        $this->req('GET','articles',[],null)->assertUnauthorized();
        $this->req('GET','articles?per_page=101')->assertStatus(422);
    }
}
