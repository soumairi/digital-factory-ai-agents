<?php

use App\Models\User;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;

final class SecurityBoundaryTest extends Tests\TestCase
{
    private string $secret;
    protected function setUp(): void
    {
        parent::setUp();
        $this->assertSame(':memory:', config('database.connections.sqlite.database'));
        $this->assertEmpty(config('database.connections.sqlite.url'));
        $this->artisan('migrate', ['--force' => true])->assertSuccessful();
        $this->secret = bin2hex(random_bytes(24));
        foreach ([false, true] as $admin) {
            $u = new User;
            $u->name = 'Synthetic';
            $u->email = ($admin ? 'admin' : 'reader').'@example.test';
            $u->password = Hash::make($this->secret);
            $u->is_admin = $admin;
            $u->save();
        }
        DB::table('customers')->insert(['name'=>'Synthetic', 'email'=>'synthetic@example.test', 'internal_notes'=>'PRIVATE_TEST_MARKER', 'created_at'=>'2026-09-17 00:00:00']);
    }
    private function credentials(string $name): void
    {
        $this->withServerVariables(['PHP_AUTH_USER'=>$name.'@example.test', 'PHP_AUTH_PW'=>$this->secret]);
    }
    public function test_head_enforces_role_boundary(): void
    {
        $this->call('HEAD','/api/customers')->assertUnauthorized();
        $this->credentials('reader');
        $this->call('HEAD','/api/customers')->assertForbidden();
        $this->credentials('admin');
        $this->call('HEAD','/api/customers')->assertOk();
        $this->assertDatabaseCount('customers',1);
    }
    public function test_all_write_methods_reject_admin_and_preserve_state(): void
    {
        $this->credentials('admin');
        $before=DB::table('customers')->get()->toJson();
        foreach (['POST','PUT','PATCH','DELETE'] as $method) {
            $this->json($method,'/api/customers',['is_admin'=>true])->assertStatus(405);
        }
        $this->assertSame($before,DB::table('customers')->get()->toJson());
        $this->assertFalse(User::where('email','reader@example.test')->first()->is_admin);
    }
    public function test_forwarded_headers_do_not_bypass_loopback_throttle(): void
    {
        for ($i=0;$i<60;$i++) {
            $this->withHeaders(['X-Forwarded-For'=>'192.0.2.'.($i+1),'Forwarded'=>'for=192.0.2.'.($i+1)])
                ->getJson('/api/customers')->assertUnauthorized();
        }
        $this->withHeader('X-Forwarded-For','198.51.100.1')->getJson('/api/customers')->assertTooManyRequests();
        $this->assertDatabaseCount('customers',1);
    }
    public function test_get_json_body_cannot_override_limits_or_grant_role(): void
    {
        $this->credentials('reader');
        $this->json('GET','/api/customers',['is_admin'=>true])->assertForbidden()->assertJsonMissingPath('data');
        $this->credentials('admin');
        $this->json('GET','/api/customers?per_page=1',['per_page'=>101])->assertUnprocessable();
        $this->json('GET','/api/customers',['tenant_id'=>2])->assertUnprocessable();
        $this->assertFalse(User::where('email','reader@example.test')->first()->is_admin);
        $this->assertDatabaseCount('customers',1);
    }
    public function test_database_exception_is_redacted(): void
    {
        $this->credentials('admin');
        DB::listen(function ($query) {
            if (str_contains($query->sql,'customers')) {
                throw new RuntimeException('SYNTHETIC_SQL_SECRET_MARKER');
            }
        });
        $this->getJson('/api/customers')->assertStatus(500)->assertJsonMissingPath('trace')
            ->assertDontSee('SYNTHETIC_SQL_SECRET_MARKER')->assertDontSee('PRIVATE_TEST_MARKER');
    }
}
