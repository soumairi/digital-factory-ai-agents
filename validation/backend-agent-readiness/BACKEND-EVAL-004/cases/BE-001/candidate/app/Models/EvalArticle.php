<?php
namespace App\Models;
use Illuminate\Database\Eloquent\Model;
class EvalArticle extends Model {
    protected $table='articles'; public $timestamps=false; protected $guarded=['*'];
    public function author() { return $this->belongsTo(EvalAuthor::class,'author_id'); }
    public function category() { return $this->belongsTo(EvalCategory::class,'category_id'); }
}
