# Acceptance Criteria — US-BE-001

| ID | Required outcome |
| --- | --- |
| AC1 | Provide GET /api/customers. |
| AC2 | Only authenticated and authorized users may access the endpoint. |
| AC3 | Unauthorized users receive an appropriate response. |
| AC4 | Return paginated results. |
| AC5 | Enforce a safe maximum page size. |
| AC6 | Each customer contains only id, name, email and created_at. |
| AC7 | Do not expose internal or sensitive fields. |
| AC8 | Validate request parameters server-side. |
| AC9 | Reject or safely normalize invalid pagination values according to project conventions. |
| AC10 | Automated tests cover authorized, unauthenticated and unauthorized access; pagination and maximum size; response schema; invalid inputs. |
| AC11 | Follow installed Foundation security rules, including independent review gates. |
| AC12 | Use no production resources. |

Source: original user-supplied US-BE-001 validation instruction; prior [recorded story](../../../backend-laravel/evidence/US-BE-001/US-BE-001.md). These are requirements, not Security/Audit findings. Sandbox conventions appear in the frozen context; they do not redefine the Foundation's owner/tenant evaluation fixtures.
