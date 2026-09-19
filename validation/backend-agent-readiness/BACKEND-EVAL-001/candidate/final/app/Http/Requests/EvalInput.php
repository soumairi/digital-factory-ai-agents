<?php
namespace App\Http\Requests;
use Illuminate\Http\Request;
use Illuminate\Http\Exceptions\HttpResponseException;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Contracts\Validation\Validator;
class EvalInput extends FormRequest {
    private array $schema=[];
    public function authorize(): bool { return true; } // Real route authentication and resource/action checks run before fields().
    public function rules(): array { return $this->schema; }
    protected function failedValidation(Validator $validator): never { self::invalid(); }
    public static function invalid(): never { throw new HttpResponseException(response()->json(['message'=>'Invalid input.'],422)); }
    public static function fields(Request $r,array $rules,array $integers=[]): array {
        $data=$r->all();
        if(array_diff(array_keys($data),array_keys($rules))) self::invalid();
        foreach($integers as $k) if(isset($data[$k])&&!is_int($data[$k])) self::invalid();
        $form=self::createFrom($r);
        $form->schema=$rules;
        $form->setContainer(app());
        $form->validateResolved();
        return $form->validated();
    }
    public static function page(Request $r): array {
        if(array_diff(array_keys($r->query()),['page','per_page'])) self::invalid();
        $out=[];
        foreach(['page'=>[1,1000000],'per_page'=>[20,100]] as $key=>[$default,$max]) {
            $query=$r->query();
            $value=array_key_exists($key,$query)?$query[$key]:(string)$default;
            if(!is_string($value)||!preg_match('/^[1-9][0-9]*$/D',$value)||strlen($value)>7||(int)$value>$max) self::invalid();
            $out[]=(int)$value;
        }
        return $out;
    }
}
