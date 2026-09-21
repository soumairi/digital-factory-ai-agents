<?php
namespace App\Models;
use Illuminate\Database\Eloquent\Model;
class EvalProfile extends Model {
    protected $table='profiles';
    public $timestamps=false;
    protected $fillable=['display_name'];
}
