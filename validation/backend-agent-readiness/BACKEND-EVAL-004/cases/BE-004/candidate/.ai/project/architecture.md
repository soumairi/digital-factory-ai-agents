# Observed architecture
bootstrap/app.php configures routes/web.php, routes/console.php and /up; JSON error rendering for api/* configured in scaffold. AppServiceProvider register/boot are empty. app/Models/User.php is the standard authenticated Eloquent user. No Customer model, customer endpoint, API route file, controller or customer-specific authorization exists.
Root web route renders welcome view. Tests contain one basic unit example and one internal HTTP root-route example. No database reset trait is active in these tests.
US-BE-001 domain behavior: NOT YET IMPLEMENTED. Standard Laravel FormRequest, Gate/Policy and API Resource mechanisms are planned per installed profile; no new architecture or package is mandated.
