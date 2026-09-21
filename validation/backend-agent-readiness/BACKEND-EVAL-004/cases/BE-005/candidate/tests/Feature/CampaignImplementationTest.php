<?php
namespace Tests\Feature;
require_once __DIR__.'/../../reviewer/common/AdapterTestCase.php';
use Illuminate\Support\Facades\DB;
class CampaignImplementationTest extends \Reviewer\AdapterTestCase {
    public function test_profile_allowlist_keeps_every_protected_value(): void {
        $this->req('PATCH','profile',['display_name'=>'Campaign'])->assertExactJson(['display_name'=>'Campaign']);
        foreach (['role'=>'editor','is_admin'=>true,'owner_id'=>2,'tenant_id'=>2,'profile'=>['is_admin'=>true]] as $key=>$value) {
            $this->reject('PATCH','profile',['display_name'=>'Denied',$key=>$value],'profiles');
        }
        $this->assertDatabaseHas('profiles',['id'=>1,'display_name'=>'Campaign','role'=>'reader','is_admin'=>false,'owner_id'=>1,'tenant_id'=>1]);
    }
}
