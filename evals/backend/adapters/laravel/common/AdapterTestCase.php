<?php
namespace Reviewer;

use App\Models\User;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;
use Tests\TestCase;

abstract class AdapterTestCase extends TestCase
{
    protected array $actors = [];
    protected string $password;
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
        $this->password='adapter-synthetic-password-not-a-credential';
        for ($i=1;$i<=4;$i++) {
            $u=new User; $u->name='Synthetic '.$i; $u->email="actor$i@example.test"; $u->password=$this->password;
            $u->tenant_id=$i<=2?1:2; $u->role=$i===2?'editor':'reader'; $u->save(); $this->actors[$i]=$u;
            DB::table('documents')->insert(['id'=>$i,'owner_id'=>$i,'tenant_id'=>$u->tenant_id,'title'=>"Document$i"]);
            DB::table('attachments')->insert(['id'=>$i,'document_id'=>$i,'name'=>"Attachment$i"]);
            DB::table('profiles')->insert(['id'=>$i,'owner_id'=>$i,'tenant_id'=>$u->tenant_id,'display_name'=>"Profile$i",'role'=>$u->role,'is_admin'=>false]);
        }
        DB::table('reports')->insert(['id'=>1,'title'=>'Report']);
        DB::table('inventory')->insert(['id'=>1,'stock'=>10]);
        foreach ([1,2] as $owner) DB::table('notes')->insert(['id'=>$owner,'owner_id'=>$owner,'title'=>'Seed'.$owner,'body'=>'Synthetic seed']);
    }
    protected function req(string $method,string $path,array $data=[],?int $actor=1) {
        // Forget guard state to exercise real Basic authentication on every request.
        app('auth')->forgetGuards();
        $headers=$actor===null?[]:['PHP_AUTH_USER'=>$this->actors[$actor]->email,'PHP_AUTH_PW'=>$this->password];
        return $this->json($method,'/api/eval/'.$path,$data,$headers);
    }
    protected function state(string $table): string { return DB::table($table)->orderBy('id')->get()->toJson(); }
    protected function reject(string $method,string $path,array $payload,string $table,?int $actor=1): void {
        $before=$this->state($table);
        $response=$this->req($method,$path,$payload,$actor);
        $this->assertSame($before,$this->state($table),'Rejected request changed persisted state');
        $response->assertStatus(422)->assertExactJson(['message'=>'Invalid input.']);
    }
    protected function invalidText(): array { return [null,'','   ',0,-1,[],['nested'=>'x'],true]; }
}
