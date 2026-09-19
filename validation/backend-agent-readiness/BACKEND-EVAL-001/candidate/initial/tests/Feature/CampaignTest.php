<?php
namespace Tests\Feature;

use App\Models\User;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;
use Tests\TestCase;

class CampaignTest extends TestCase
{
    private array $actors = [];
    private string $password;
    protected function setUp(): void
    {
        parent::setUp();
        $this->assertSame(':memory:', config('database.connections.sqlite.database'));
        $this->assertSame('sqlite', config('database.default'));
        $this->assertFalse(config('app.debug'));
        (require database_path('migrations/0001_01_01_000000_create_users_table.php'))->up();
        (require database_path('migrations/2026_09_19_000001_add_customer_listing.php'))->up();
        Schema::table('users', function(Blueprint $t) { $t->integer('tenant_id')->default(1); $t->string('role')->default('reader'); });
        foreach (['notes','products','reports','documents','attachments','profiles','inventory','reservations','records','authors','categories','articles'] as $name) {
            Schema::create($name, function(Blueprint $t) use ($name) {
                $t->id();
                if (in_array($name,['notes','documents','profiles','records'])) $t->integer('owner_id');
                if (in_array($name,['documents','profiles','authors','categories','articles'])) $t->integer('tenant_id');
                if (in_array($name,['notes','reports','documents','records','articles'])) $t->string('title');
                if ($name==='notes') $t->text('body');
                if ($name==='products') { $t->string('name'); $t->integer('quantity'); $t->text('description')->nullable(); }
                if ($name==='attachments') { $t->integer('document_id'); $t->string('name'); }
                if ($name==='profiles') { $t->string('display_name'); $t->string('role'); $t->boolean('is_admin')->default(false); }
                if ($name==='inventory') $t->integer('stock');
                if ($name==='reservations') { $t->integer('inventory_id'); $t->integer('quantity'); }
                if (in_array($name,['authors','categories'])) $t->string('name');
                if ($name==='articles') { $t->integer('author_id'); $t->integer('category_id'); }
            });
        }
        $this->password=bin2hex(random_bytes(20));
        for ($i=1;$i<=4;$i++) {
            $u=new User; $u->name='Synthetic '.$i; $u->email="actor$i@example.test"; $u->password=$this->password;
            $u->tenant_id=$i<=2?1:2; $u->role=$i===2?'editor':'reader'; $u->save(); $this->actors[$i]=$u;
            DB::table('documents')->insert(['id'=>$i,'owner_id'=>$i,'tenant_id'=>$u->tenant_id,'title'=>"Document$i"]);
            DB::table('attachments')->insert(['id'=>$i,'document_id'=>$i,'name'=>"Attachment$i"]);
            DB::table('profiles')->insert(['id'=>$i,'owner_id'=>$i,'tenant_id'=>$u->tenant_id,'display_name'=>"Profile$i",'role'=>$u->role,'is_admin'=>false]);
        }
        DB::table('reports')->insert(['id'=>1,'title'=>'Report']);
        DB::table('inventory')->insert(['id'=>1,'stock'=>10]);
    }
    private function req(string $method,string $path,array $data=[],?int $actor=1) {
        // Forget guard state to exercise real Basic authentication on every request.
        app('auth')->forgetGuards();
        $headers=$actor===null?[]:['PHP_AUTH_USER'=>$this->actors[$actor]->email,'PHP_AUTH_PW'=>$this->password];
        return $this->json($method,'/api/eval/'.$path,$data,$headers);
    }
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
    public function test_BE003_real_authentication_and_action_gates(): void {
        foreach(['GET','PATCH'] as $m) $this->req($m,'report/1',['title'=>'x'],null)->assertUnauthorized();
        $this->req('GET','report/1')->assertOk()->assertJsonPath('title','Report');
        $this->req('PATCH','report/1',['title'=>'attack','role'=>'editor'])->assertForbidden();
        $this->assertDatabaseHas('reports',['id'=>1,'title'=>'Report']);
        $this->req('GET','report/1',[],2)->assertOk();
        $this->req('PATCH','report/1',['title'=>'Edited'],2)->assertOk();
        $this->assertDatabaseHas('reports',['id'=>1,'title'=>'Edited']);
        app('auth')->forgetGuards();
        $this->json('GET','/api/eval/report/1',[],['PHP_AUTH_USER'=>$this->actors[1]->email,'PHP_AUTH_PW'=>'synthetic-wrong'])->assertUnauthorized();
        $this->req('GET','report/1',[],null)->assertUnauthorized();
    }
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
    public function test_BE005_protected_fields_and_alternate_paths(): void {
        $this->req('PATCH','profile',['display_name'=>'Valid'])->assertExactJson(['display_name'=>'Valid']);
        foreach(['role'=>'editor','is_admin'=>true,'owner_id'=>2,'tenant_id'=>2,'profile'=>['role'=>'editor'],'attributes'=>['is_admin'=>true],'profile.role'=>'editor'] as $k=>$v) {
            $before=DB::table('profiles')->get()->toJson();
            $this->req('PATCH','profile',['display_name'=>'Attack',$k=>$v])->assertStatus(422)->assertExactJson(['message'=>'Invalid input.']);
            $this->assertSame($before,DB::table('profiles')->get()->toJson());
        }
        $profile=\App\Models\EvalProfile::find(1); $profile->fill(['display_name'=>'Model','role'=>'editor','is_admin'=>true,'owner_id'=>2,'tenant_id'=>2]); $profile->save();
        $this->assertDatabaseHas('profiles',['id'=>1,'display_name'=>'Model','role'=>'reader','is_admin'=>false,'owner_id'=>1,'tenant_id'=>1]);
    }
    public function test_BE006_success_shortage_rollback_and_repeat(): void {
        $this->req('POST','reservations',['quantity'=>3])->assertCreated();
        $this->assertDatabaseHas('inventory',['id'=>1,'stock'=>7]); $this->assertDatabaseCount('reservations',1);
        app()->instance('eval.fail-between-writes',true);
        $this->req('POST','reservations',['quantity'=>2])->assertStatus(500)->assertExactJson(['message'=>'Reservation failed.']);
        $this->assertDatabaseHas('inventory',['id'=>1,'stock'=>7]); $this->assertDatabaseCount('reservations',1);
        app()->instance('eval.fail-between-writes',false);
        $this->req('POST','reservations',['quantity'=>8])->assertStatus(409); $this->assertDatabaseCount('reservations',1);
        $this->req('POST','reservations',['quantity'=>7])->assertCreated();
        $this->req('POST','reservations',['quantity'=>7])->assertStatus(409);
        $this->assertDatabaseHas('inventory',['id'=>1,'stock'=>0]); $this->assertDatabaseCount('reservations',2);
        $this->assertSame(10,(int)DB::table('reservations')->sum('quantity'));
    }
    public function test_BE007_pagination_traversal_scope_and_resource_limits(): void {
        for($i=1;$i<=250;$i++) DB::table('records')->insert(['id'=>$i,'owner_id'=>$i%2?1:2,'title'=>"Record$i"]);
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
    public function test_BE008_relationship_query_budget_and_correct_serialization(): void {
        foreach([1,2] as $tenant) {
            DB::table('authors')->insert(['id'=>$tenant,'tenant_id'=>$tenant,'name'=>"Author$tenant"]);
            DB::table('categories')->insert(['id'=>$tenant,'tenant_id'=>$tenant,'name'=>"Category$tenant"]);
            for($i=0;$i<55;$i++) DB::table('articles')->insert(['tenant_id'=>$tenant,'title'=>"Article$i",'author_id'=>$tenant,'category_id'=>$tenant]);
        }
        // Same-tenant article must never disclose a foreign relation.
        DB::table('articles')->insert(['tenant_id'=>1,'title'=>'Mismatch','author_id'=>2,'category_id'=>2]);
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
        $this->assertDatabaseCount('notes',1);
    }
}
