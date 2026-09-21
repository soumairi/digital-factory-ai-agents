<?php

use App\Http\Controllers\ListCustomersController;
use App\Http\Middleware\AuthenticateCustomerList;
use Illuminate\Support\Facades\Route;

Route::get('/customers', ListCustomersController::class)
    ->middleware(['throttle:customer-list', AuthenticateCustomerList::class]);

Route::prefix('eval')->middleware([\App\Http\Middleware\EvalAuthenticate::class])->group(function() {
    $c=\App\Http\Controllers\EvalController::class;
    Route::post('notes',[$c,'noteCreate']);
    Route::match(['GET','PATCH','DELETE'],'notes/{id}',[$c,'note'])->whereNumber('id');
    Route::post('products',[$c,'product']);
    Route::match(['GET','PATCH'],'report/{id}',[$c,'report'])->whereNumber('id');
    Route::get('documents',[$c,'documentList']);
    Route::match(['GET','PATCH'],'documents/{id}',[$c,'document'])->whereNumber('id');
    Route::get('documents/{id}/attachments/{child}',[$c,'attachment'])->whereNumber(['id','child']);
    Route::patch('profile',[$c,'profile']);
    Route::post('reservations',[$c,'reserve']);
    Route::get('records',[$c,'records']);
    Route::get('articles',[$c,'articles']);
});
