# Firestore Schema — AntiGravity ThaiTurk

## Collections

### `patients`

Tıbbi hasta başvuruları.

| Field | Type | Description |
|-------|------|-------------|
| `patient_id` | string | `MED-YYYYMMDD-XXXXXX` |
| `full_name` | string | Patient full name |
| `phone` | string | International format (+XX…) |
| `language` | string | `ru` / `en` / `tr` / `th` |
| `procedure_interest` | string | Procedure name |
| `procedure_category` | string | `aesthetic`, `hair`, `dental`, … |
| `urgency` | string | `routine` / `soon` / `urgent` |
| `budget_usd` | number | Patient budget |
| `notes` | string | Free-text notes |
| `referral_source` | string | Instagram / Telegram / … |
| `phuket_arrival_date` | string | ISO date |
| `matched_hospital_id` | string | Partner hospital ID |
| `status` | string | `new` / `contacted` / `confirmed` / `completed` |
| `commission_usd` | number | AntiGravity commission (22–25%) |
| `created_at` | timestamp | Firestore server timestamp |
| `updated_at` | timestamp | Last update |

---

### `hospitals`

Partner hastaneler (Turkey + Thailand).

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | `MEM-IST-001` format |
| `name` | string | Hospital name |
| `city` | string | City |
| `country` | string | `Turkey` / `Thailand` |
| `specialties` | string[] | `aesthetic`, `hair`, `dental`, … |
| `rating` | number | 1–5 star rating |
| `commission_rate` | number | 0.15 – 0.25 |
| `languages` | string[] | Supported languages |
| `jci` | boolean | JCI accreditation |
| `beds` | number | Bed count |
| `contact_whatsapp` | string | Hospital WhatsApp |
| `active` | boolean | Currently accepting referrals |

---

### `travel_requests`

Seyahat talepleri.

| Field | Type | Description |
|-------|------|-------------|
| `request_id` | string | `TRV-YYYYMMDD-XXXXXX` |
| `full_name` | string | Guest name |
| `phone` | string | International format |
| `language` | string | Preferred language |
| `destination` | string | Phuket, Samui, Krabi, … |
| `check_in` | string | ISO date |
| `check_out` | string | ISO date |
| `guests` | number | Number of guests |
| `notes` | string | Preferences |
| `status` | string | `new` / `planning` / `booked` |
| `created_at` | timestamp | Server timestamp |

---

## Security Rules (Firestore)

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Public read is disabled — all access via backend service account
    match /{document=**} {
      allow read, write: if false;
    }
  }
}
```

> All Firestore access must go through the FastAPI backend using the service account at `GOOGLE_APPLICATION_CREDENTIALS`.
