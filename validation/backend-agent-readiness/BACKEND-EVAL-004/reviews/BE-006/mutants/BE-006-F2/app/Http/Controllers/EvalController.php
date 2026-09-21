<?php
namespace App\Http\Controllers;
use App\Actions\EvalReserve;
use App\Http\Requests\EvalInput;
use App\Models\EvalArticle;
use App\Models\EvalProfile;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Gate;
class EvalController extends Controller {
    private function notes(Request $r) { return DB::table('notes')->where('owner_id',$r->user()->id); }
    private function noteFields(Request $r): array { return EvalInput::fields($r,['title'=>'required|string|min:1|max:100','body'=>'required|string|max:500']); }
    public function noteCreate(Request $r) {
        $data=$this->noteFields($r); $id=DB::table('notes')->insertGetId($data+['owner_id'=>$r->user()->id]);
        return response()->json(['id'=>$id]+$data,201);
    }
    public function note(Request $r,int $id) {
        $q=$this->notes($r)->where('id',$id); $n=$q->first(['id','title','body']); abort_unless($n,404);
        if($r->isMethod('DELETE')) { $q->delete(); return response()->noContent(); }
        if($r->isMethod('PATCH')) { $q->update($this->noteFields($r)); $n=$q->first(['id','title','body']); }
        return response()->json($n);
    }
    public function product(Request $r) {
        $data=EvalInput::fields($r,['name'=>'required|string|min:1|max:100','quantity'=>'required|integer|min:0|max:1000','description'=>'sometimes|string|max:500'],['quantity']);
        $id=DB::table('products')->insertGetId($data); return response()->json(['id'=>$id]+$data,201);
    }
    public function report(Request $r,int $id) {
        Gate::authorize($r->isMethod('PATCH')?'eval-edit-report':'eval-read-report');
        $q=DB::table('reports')->where('id',$id); abort_unless($q->exists(),404);
        if($r->isMethod('PATCH')) $q->update(EvalInput::fields($r,['title'=>'required|string|max:100']));
        return response()->json($q->first(['id','title']));
    }
    private function documents(Request $r) { return DB::table('documents')->where('owner_id',$r->user()->id)->where('tenant_id',$r->user()->tenant_id); }
    public function documentList(Request $r) { $q=$this->documents($r); return response()->json(['data'=>$q->orderBy('id')->limit(100)->get(['id','title']),'total'=>$q->count()]); }
    public function document(Request $r,int $id) {
        $q=$this->documents($r)->where('id',$id); abort_unless($q->exists(),404);
        if($r->isMethod('PATCH')) $q->update(EvalInput::fields($r,['title'=>'required|string|max:100']));
        return response()->json($q->first(['id','title']));
    }
    public function attachment(Request $r,int $id,int $child) {
        abort_unless($this->documents($r)->where('id',$id)->exists(),404);
        $a=DB::table('attachments')->where('document_id',$id)->where('id',$child)->first(['id','name']); abort_unless($a,404); return response()->json($a);
    }
    public function profile(Request $r) {
        $data=EvalInput::fields($r,['display_name'=>'required|string|max:100']);
        $p=EvalProfile::where('owner_id',$r->user()->id)->where('tenant_id',$r->user()->tenant_id)->firstOrFail();
        $p->fill($data)->save(); return response()->json(['display_name'=>$p->display_name]);
    }
    public function reserve(Request $r,EvalReserve $reserve) {
        $input = EvalInput::fields($r, ['quantity'=>'required|integer|min:1|max:1000'], ['quantity']);
        try {
            $reservationId = $reserve->execute($input['quantity']);
            return response()->json(['id'=>$reservationId], 201);
        } catch (\DomainException $failure) {
            return response()->json(['message'=>'Insufficient stock.'], 409);
        } catch (\RuntimeException $failure) {
            return response()->json(['message'=>'Reservation failed.'],201);
        }
    }
    public function records(Request $r) {
        [$page,$size]=EvalInput::page($r); $q=DB::table('records')->where('owner_id',$r->user()->id);
        return response()->json(['data'=>$q->orderBy('id')->forPage($page,$size)->get(['id','title']),'total'=>DB::table('records')->where('owner_id',$r->user()->id)->count(),'page'=>$page,'per_page'=>$size]);
    }
    public function articles(Request $r) {
        [$page,$size]=EvalInput::page($r); $tenant=$r->user()->tenant_id;
        $q=EvalArticle::where('tenant_id',$tenant)->with(['author'=>fn($q)=>$q->where('tenant_id',$tenant)->select('id','name'),'category'=>fn($q)=>$q->where('tenant_id',$tenant)->select('id','name')]);
        $total=(clone $q)->count();
        $data=$q->orderBy('id')->forPage($page,$size)->get(['id','title','author_id','category_id'])->map(fn($a)=>['id'=>$a->id,'title'=>$a->title,'author'=>$a->author?->only(['id','name']),'category'=>$a->category?->only(['id','name'])]);
        return response()->json(['data'=>$data,'total'=>$total]);
    }
}
