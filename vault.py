import json, os
from typing import Dict

VAULT_FILENAME = "vault.json.enc"

def load_encrypted_vault(path=VAULT_FILENAME):
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_encrypted_vault(payload, path=VAULT_FILENAME):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

def ensure_vault_exists(path=VAULT_FILENAME):
    if not os.path.exists(path):
        # create empty encrypted vault with empty dict; user will provide passphrase to set
        return None
