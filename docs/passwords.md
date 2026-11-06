# Registration PIN storage

New registrations collect a six to twelve digit PIN in the in-memory Telegram conversation context. The bot displays only masked digits and creates the customer row only after confirmation. The database stores `pbkdf2_sha256$<iterations>$<salt>$<digest>`; the salt is random for each PIN. The `customers.password_hash` column must allow at least 255 characters before deploying this change.

Existing 64-character SHA-256 hashes remain valid. When `check_password` successfully verifies one, it replaces that value with a salted PBKDF2 hash in the same database transaction. Incorrect PINs do not modify the row. Existing hashes are not upgraded until a successful verification, so old accounts that never authenticate keep the legacy hash. The current purchase flow does not call `check_password`; if PIN authentication is added to purchases, that is where lazy upgrades will occur.
