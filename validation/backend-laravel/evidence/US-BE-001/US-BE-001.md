# US-BE-001: List customers with secure pagination
As an authenticated administrator I want a paginated customer list for safe browsing.
AC1 GET /api/customers. AC2 authentication and authorization. AC3 deny inappropriate access. AC4 paginate. AC5 safe maximum page size. AC6 only id/name/email/created_at. AC7 no sensitive/internal fields. AC8 server validation. AC9 invalid inputs rejected. AC10 positive/negative automated tests. AC11 installed security rules. AC12 no production resources.
Full acceptance criteria originate in the requesting user’s validation task. Human final acceptance pending.
