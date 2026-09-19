<?php

namespace App\Http\Requests;

use Illuminate\Contracts\Validation\Validator;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Http\Exceptions\HttpResponseException;
use Illuminate\Support\Facades\Gate;
use Illuminate\Support\Facades\Log;

class ListCustomersRequest extends FormRequest
{
    public function authorize(): bool
    {
        if (Gate::allows('list-customers')) {
            return true;
        }

        Log::warning('customers.authorization_denied');

        return false;
    }

    public function rules(): array
    {
        return [
            'page' => ['sometimes', 'required', 'integer', 'min:1', 'max:1000'],
            'per_page' => ['sometimes', 'required', 'integer', 'min:1', 'max:100'],
        ];
    }

    public function after(): array
    {
        return [function (Validator $validator): void {
            if (array_diff(array_keys($this->all()), ['page', 'per_page']) !== []) {
                $validator->errors()->add('pagination', 'Unsupported parameter.');
            }

            foreach (['page', 'per_page'] as $key) {
                $value = $this->input($key);
                if ($this->exists($key) && (! is_string($value) || ! preg_match('/\A[1-9][0-9]{0,3}\z/D', $value))) {
                    $validator->errors()->add($key, 'Invalid pagination.');
                }
            }

            if ($this->getContent() !== '') {
                $validator->errors()->add('pagination', 'Request body is not supported.');
            }
        }];
    }

    protected function failedValidation(Validator $validator): void
    {
        throw new HttpResponseException(response()->json(['message' => 'Invalid pagination parameters.'], 422)
            ->header('Cache-Control', 'no-store'));
    }
}
