<?php

use App\Http\Controllers\ListCustomersController;
use App\Http\Middleware\AuthenticateCustomerList;
use Illuminate\Support\Facades\Route;

Route::get('/customers', ListCustomersController::class)
    ->middleware(['throttle:customer-list', AuthenticateCustomerList::class]);
