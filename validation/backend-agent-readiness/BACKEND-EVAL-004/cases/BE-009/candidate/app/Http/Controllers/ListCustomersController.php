<?php

namespace App\Http\Controllers;

use App\Http\Requests\ListCustomersRequest;
use App\Http\Resources\CustomerResource;
use App\Models\Customer;
use Illuminate\Http\JsonResponse;

class ListCustomersController extends Controller
{
    public function __invoke(ListCustomersRequest $request): JsonResponse
    {
        $input = $request->validated();
        $customers = Customer::query()
            ->select(['id', 'name', 'email', 'created_at'])
            ->orderBy('id')
            ->paginate((int) ($input['per_page'] ?? 20), ['*'], 'page', (int) ($input['page'] ?? 1));
        $customers->appends(['per_page' => $customers->perPage()]);

        return CustomerResource::collection($customers)->response()
            ->header('Cache-Control', 'no-store');
    }
}
