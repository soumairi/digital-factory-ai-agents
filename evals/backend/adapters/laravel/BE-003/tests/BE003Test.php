<?php
namespace Reviewer;
require_once __DIR__.'/../../common/AdapterTestCase.php';
use Illuminate\Support\Facades\DB;
class BE003Test extends AdapterTestCase
{
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

    public function test_BE003_credential_and_editor_title_matrix(): void {
        foreach([null,'','   ','invalid'] as $password) {
            app('auth')->forgetGuards();$before=$this->state('reports');
            $headers=['PHP_AUTH_USER'=>$this->actors[2]->email];if($password!==null)$headers['PHP_AUTH_PW']=$password;
            $this->json('PATCH','/api/eval/report/1',['title'=>'Denied'],$headers)->assertUnauthorized()->assertDontSee('trace');
            $this->assertSame($before,$this->state('reports'));
        }
        $this->req('GET','report/1')->assertExactJson(['id'=>1,'title'=>'Report']);
        $this->reject('PATCH','report/1',[],'reports',2);
        foreach($this->invalidText() as $value) $this->reject('PATCH','report/1',['title'=>$value],'reports',2);
        $this->req('PATCH','report/1',[])->assertForbidden();
    }
}
