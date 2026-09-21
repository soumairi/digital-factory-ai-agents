<?php
namespace App\Http\Middleware;
use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
class EvalAuthenticate {
    public function handle(Request $request, Closure $next) {
        Auth::forgetGuards();
        $failure=Auth::guard('web')->onceBasic();
        return $failure ?: $next($request);
    }
}
