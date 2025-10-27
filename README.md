# Secure Secret Store 🔐

A small CLI tool to **store, retrieve, list and delete secrets** in an encrypted local vault (AES-256 via Fernet).  
Designed for developers and small teams who need a simple, safe local secret store that can be committed (encrypted) into git safely.

## Features
- Encrypts secrets with a passphrase-derived key (PBKDF2HMAC + Fernet)
- CLI: `set`, `get`, `delete`, `list`, `export` (encrypted JSON vault)
- Safe to commit `vault.json.enc` to Git
- No external server — offline, privacy-focused
- Minimal dependencies (`cryptography` & `click`)

## Install (local)
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Usage examples
```bash
# create or update a secret
secret-store set my/service API_KEY "sk_test_1234"

# retrieve a secret (asks passphrase interactively)
secret-store get my/service API_KEY

# list secrets
secret-store list

# delete a secret
secret-store delete my/service API_KEY

# export decrypted vault to JSON (useful for migration)
secret-store export --out vault_decrypted.json
```

Vault file (default): `vault.json.enc`
Passphrase: you will be prompted; passphrase is not saved.

## Security notes
- Uses PBKDF2 with many iterations and AES (Fernet) — suitable for local protection.
- Do **not** share passphrases. If you lose the passphrase, vault cannot be recovered.
- For team-sharing, agree on a shared passphrase or distribute per-user keys securely.

## Sponsor
If this tool helps your workflow, consider sponsoring development on GitHub Sponsors ❤️

## License
MIT
