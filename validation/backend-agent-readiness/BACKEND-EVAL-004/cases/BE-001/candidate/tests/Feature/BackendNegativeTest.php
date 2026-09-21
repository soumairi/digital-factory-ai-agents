<?php
namespace Tests\Feature;
require_once __DIR__.'/../../reviewer/common/AdapterTestCase.php';
class BackendNegativeTest extends \Reviewer\AdapterTestCase {
    public function test_negative_unauthenticated(): void { $before=$this->state('notes');$this->req('PATCH','notes/1',['title'=>'x','body'=>'x'],null)->assertUnauthorized();$this->assertSame($before,$this->state('notes')); }
    public function test_negative_unauthorized(): void { $before=$this->state('reports');$this->req('PATCH','report/1',['title'=>'x'])->assertForbidden();$this->assertSame($before,$this->state('reports')); }
    public function test_negative_ownership(): void { $before=$this->state('notes');$r=$this->req('PATCH','notes/1',['title'=>'x','body'=>'x'],2);$this->assertSame($before,$this->state('notes'));$r->assertNotFound()->assertJsonMissingPath('title'); }
    public function test_negative_invalid(): void { $this->reject('PATCH','notes/1',[],'notes'); }
    public function test_negative_malicious(): void { $this->req('GET','notes/1%20OR%201=1')->assertNotFound()->assertDontSee('trace');$this->assertDatabaseHas('notes',['id'=>1,'title'=>'Seed1']); }
    public function test_negative_sensitive_fields(): void { $this->reject('PATCH','profile',['display_name'=>'x','is_admin'=>true],'profiles'); }
}
