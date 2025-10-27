import click, getpass, json, os
from .core import encrypt_json_obj, decrypt_json_payload
from .vault import load_encrypted_vault, save_encrypted_vault, VAULT_FILENAME

def _read_passphrase(prompt='Passphrase: '):
    return getpass.getpass(prompt=prompt)

@click.group()
@click.option('--vault', default=VAULT_FILENAME, help='Vault file path (encrypted)')
@click.pass_context
def cli(ctx, vault):
    ctx.ensure_object(dict)
    ctx.obj['vault'] = vault

@cli.command('set')
@click.argument('namespace')
@click.argument('key')
@click.argument('value')
@click.pass_context
def set_secret(ctx, namespace, key, value):
    vault_path = ctx.obj['vault']
    passphrase = _read_passphrase()
    payload = load_encrypted_vault(vault_path)
    if payload:
        try:
            data = decrypt_json_payload(payload, passphrase)
        except Exception as e:
            click.echo('ERROR: wrong passphrase or corrupted vault')
            raise SystemExit(1)
    else:
        data = {}

    # set nested namespace.key
    ns = data.setdefault(namespace, {})
    ns[key] = value
    new_payload = encrypt_json_obj(data, passphrase)
    save_encrypted_vault(new_payload, vault_path)
    click.echo(f'Saved {namespace}.{key} into {vault_path}')

@cli.command('get')
@click.argument('namespace')
@click.argument('key')
@click.pass_context
def get_secret(ctx, namespace, key):
    vault_path = ctx.obj['vault']
    passphrase = _read_passphrase()
    payload = load_encrypted_vault(vault_path)
    if not payload:
        click.echo('Vault not found or empty.')
        raise SystemExit(1)
    try:
        data = decrypt_json_payload(payload, passphrase)
    except Exception as e:
        click.echo('ERROR: wrong passphrase or corrupted vault')
        raise SystemExit(1)
    ns = data.get(namespace, {})
    if key in ns:
        click.echo(ns[key])
    else:
        click.echo('Key not found.')

@cli.command('list')
@click.pass_context
def list_all(ctx):
    vault_path = ctx.obj['vault']
    passphrase = _read_passphrase()
    payload = load_encrypted_vault(vault_path)
    if not payload:
        click.echo('Vault not found or empty.')
        raise SystemExit(1)
    try:
        data = decrypt_json_payload(payload, passphrase)
    except Exception:
        click.echo('ERROR: wrong passphrase or corrupted vault')
        raise SystemExit(1)
    for ns, kv in data.items():
        click.echo(f'[{ns}]')
        for k in kv:
            click.echo(f' - {k}')

@cli.command('delete')
@click.argument('namespace')
@click.argument('key')
@click.pass_context
def delete_secret(ctx, namespace, key):
    vault_path = ctx.obj['vault']
    passphrase = _read_passphrase()
    payload = load_encrypted_vault(vault_path)
    if not payload:
        click.echo('Vault not found or empty.')
        raise SystemExit(1)
    try:
        data = decrypt_json_payload(payload, passphrase)
    except Exception:
        click.echo('ERROR: wrong passphrase or corrupted vault')
        raise SystemExit(1)
    ns = data.get(namespace, {})
    if key in ns:
        del ns[key]
        new_payload = encrypt_json_obj(data, passphrase)
        save_encrypted_vault(new_payload, vault_path)
        click.echo(f'Deleted {namespace}.{key}')
    else:
        click.echo('Key not found.')

@cli.command('export')
@click.option('--out', default='vault_decrypted.json', help='Output JSON file (decrypted)')
@click.pass_context
def export_vault(ctx, out):
    vault_path = ctx.obj['vault']
    passphrase = _read_passphrase()
    payload = load_encrypted_vault(vault_path)
    if not payload:
        click.echo('Vault not found or empty.')
        raise SystemExit(1)
    try:
        data = decrypt_json_payload(payload, passphrase)
    except Exception:
        click.echo('ERROR: wrong passphrase or corrupted vault')
        raise SystemExit(1)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    click.echo('Exported decrypted vault to ' + out)

def main():
    cli()

if __name__ == '__main__':
    main()
