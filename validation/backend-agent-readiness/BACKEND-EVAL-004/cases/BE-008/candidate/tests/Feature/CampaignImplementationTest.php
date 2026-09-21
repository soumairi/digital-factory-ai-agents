<?php
namespace Tests\Feature;
require_once __DIR__.'/../../reviewer/common/AdapterTestCase.php';
use Illuminate\Support\Facades\DB;
class CampaignImplementationTest extends \Reviewer\AdapterTestCase {
    public function test_article_relationship_visibility_and_fixed_query_growth(): void {
        foreach ([1,2] as $tenant) {
            DB::table('authors')->insert(['id'=>$tenant,'tenant_id'=>$tenant,'name'=>'Author'.$tenant]);
            DB::table('categories')->insert(['id'=>$tenant,'tenant_id'=>$tenant,'name'=>'Category'.$tenant]);
        }
        for ($i=1;$i<=55;$i++) DB::table('articles')->insert(['tenant_id'=>1,'title'=>'Article','author_id'=>1,'category_id'=>1]);
        DB::table('articles')->insert(['tenant_id'=>1,'title'=>'Foreign relation','author_id'=>2,'category_id'=>2]);
        foreach ([5,50] as $size) {
            DB::enableQueryLog(); DB::flushQueryLog();
            $r=$this->req('GET','articles?per_page='.$size)->assertOk()->assertJsonCount($size,'data');
            $queries=array_filter(DB::getQueryLog(),fn($q)=>str_contains($q['query'],'"authors"')||str_contains($q['query'],'"categories"'));
            $this->assertCount(2,$queries);
            $r->assertJsonPath('data.0.author',['id'=>1,'name'=>'Author1']);
            DB::disableQueryLog();
        }
        $this->req('GET','articles?per_page=50&page=2')->assertJsonPath('data.5.author',null)->assertJsonPath('data.5.category',null);
    }
}
