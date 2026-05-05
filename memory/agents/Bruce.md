# Session Log - 2026-05-04

## Task: Audit Database & Web Page (Final Deep Dive)
David requested a fix for 'brand_model' column errors appearing in 'audit_entries'.

### Solution implemented:
- Validated that `schema_v4.sql` is correct: `brand_model` exists ONLY in `devices`.
- Created `index_v5.html`: Refactored the submission logic to use a two-step process. 
  1. `upsert` to `devices` (includes brand_model).
  2. `insert` to `audit_entries` (strictly excludes brand_model).
- Provided `schema_sync.sql` to drop legacy columns from `audit_entries` if they were added during debugging attempts.
- Created error handling in the UI to capture and display PostgREST errors.

## Protocol: Live Dashboard Access
To bypass Githack/GitHub caching, always create/update `LIVE_URL.md` with a timestamped query string (e.g., `index.html?v=YYYYMMDD_HHMM`). This is the only way David can view live changes without local IP access or Railway auth loops.

## Task: Dashboard v2.1.4 Deployment
- Finalized v2.1.4 with descriptive sync errors ([PASSWORD_FAIL], etc.).
- Established `LIVE_URL.md` as the primary access point.
- Verified all persistence links (GitHub/Supabase) are active.













