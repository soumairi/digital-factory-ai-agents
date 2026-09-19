<?php
namespace Reviewer;
require_once __DIR__.'/../../common/AdapterTestCase.php';
use Illuminate\Support\Facades\DB;
class BE005Test extends AdapterTestCase
{
    public function test_BE005_protected_fields_and_alternate_paths(): void {
        $this->req('PATCH','profile',['display_name'=>'Valid'])->assertExactJson(['display_name'=>'Valid']);
        foreach(['role'=>'editor','is_admin'=>true,'owner_id'=>2,'tenant_id'=>2,'profile'=>['role'=>'editor'],'attributes'=>['is_admin'=>true],'profile.role'=>'editor'] as $k=>$v) {
            $before=DB::table('profiles')->get()->toJson();
            $response=$this->req('PATCH','profile',['display_name'=>'Attack',$k=>$v]);
            $this->assertSame($before,DB::table('profiles')->get()->toJson(),'Protected state changed');
            $response->assertStatus(422)->assertExactJson(['message'=>'Invalid input.']);
        }
        $profile=\App\Models\EvalProfile::find(1); $profile->fill(['display_name'=>'Model','role'=>'editor','is_admin'=>true,'owner_id'=>2,'tenant_id'=>2]); $profile->save();
        $this->assertDatabaseHas('profiles',['id'=>1,'display_name'=>'Model','role'=>'reader','is_admin'=>false,'owner_id'=>1,'tenant_id'=>1]);
    }

    public function test_BE005_all_protected_value_shapes_and_display_boundaries(): void {
        $this->reject('PATCH','profile',[],'profiles');
        foreach($this->invalidText() as $value) $this->reject('PATCH','profile',['display_name'=>$value],'profiles');
        foreach([1,100] as $length) $this->req('PATCH','profile',['display_name'=>str_repeat('x',$length)])->assertExactJson(['display_name'=>str_repeat('x',$length)]);
        $this->reject('PATCH','profile',['display_name'=>str_repeat('x',101)],'profiles');
        foreach(['role','is_admin','owner_id','tenant_id'] as $field) foreach([null,0,false,true,2,['nested'=>true]] as $value) $this->reject('PATCH','profile',['display_name'=>'Attack',$field=>$value],'profiles');
        $this->reject('PATCH','profile',['display_name'=>'Attack','role'=>'editor','is_admin'=>true,'owner_id'=>2,'tenant_id'=>2],'profiles');
        $this->req('PATCH','profile',['display_name'=>'Denied'],null)->assertUnauthorized();
    }
}
