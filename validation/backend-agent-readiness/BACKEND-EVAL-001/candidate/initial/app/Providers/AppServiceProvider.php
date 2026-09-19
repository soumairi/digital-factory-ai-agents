<?php

namespace App\Providers;

use App\Models\User;
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        //
    }

    public function boot(): void
    {
        Gate::define('eval-read-report', fn (User $user): bool => in_array($user->role, ['reader', 'editor'], true));
        Gate::define('eval-edit-report', fn (User $user): bool => $user->role === 'editor');
        Gate::define('list-customers', fn (User $user): bool => $user->is_admin === true);
        RateLimiter::for('customer-list', fn (Request $request) => Limit::perMinute(60)->by($request->ip()));
    }
}
