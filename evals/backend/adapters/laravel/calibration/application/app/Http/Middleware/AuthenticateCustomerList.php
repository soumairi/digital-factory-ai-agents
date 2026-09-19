<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Log;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpKernel\Exception\UnauthorizedHttpException;

class AuthenticateCustomerList
{
    public function handle(Request $request, Closure $next): Response
    {
        try {
            Auth::guard('web')->onceBasic();
        } catch (UnauthorizedHttpException $exception) {
            Log::warning('customers.authentication_denied');

            throw $exception;
        }

        return $next($request);
    }
}
