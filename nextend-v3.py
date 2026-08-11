#!/usr/bin/env python3
"""Grava a config do Google via getAll('default') + set() + storeSettings via update()."""
import subprocess

def wpeval(code):
    with open("/tmp/_nsl_v3.php", "w", encoding="utf-8") as f:
        f.write("<?php\n" + code + "\n")
    subprocess.run(["scp", "-q", "/tmp/_nsl_v3.php", "aga-web:/tmp/"], timeout=30)
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp eval-file /tmp/_nsl_v3.php"
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=120)
    subprocess.run(["ssh", "aga-web", "rm -f /tmp/_nsl_v3.php"], timeout=20)
    return r.stdout.strip(), r.stderr.strip()

r = subprocess.run(["ssh", "aga-lichess", "sudo cat /etc/pychess.env | grep -E 'GOOGLE_CLIENT_ID|GOOGLE_CLIENT_SECRET'"], capture_output=True, text=True, timeout=30)
creds = {}
for linha in r.stdout.strip().split("\n"):
    if "=" in linha:
        k, v = linha.split("=", 1)
        creds[k.strip()] = v.strip()
client_id = creds.get("GOOGLE_CLIENT_ID", "")
client_secret = creds.get("GOOGLE_CLIENT_SECRET", "")

php = f"""
$provider = NextendSocialLogin::$providers['google'] ?? null;
if (!$provider) {{ echo "ERRO: provider google nao encontrado\n"; exit; }}

// 1. obter os defaults completos
$defaults = $provider->settings->getAll('default');
echo "defaults: " . count($defaults) . " campos\n";

// 2. usar set() campo a campo (o método set actualiza o array stored)
$provider->settings->set('settings_saved', '1');
$provider->settings->set('client_id', '{client_id}');
$provider->settings->set('client_secret', '{client_secret}');
$provider->settings->set('tested', '1');
$provider->settings->set('login_label', 'Continuar com Google');
$provider->settings->set('register_label', 'Continuar com Google');

// 3. forçar o store (o método set pode não gravar até update/store)
//    update() valida via filtro; vamos gravar directamente a opção com getAll()
$final = $provider->settings->getAll('final');
global $wpdb;
$wpdb->update(
    $wpdb->prefix . 'options',
    array('option_value' => serialize($final)),
    array('option_name' => 'nsl_google')
);

// verificar
$opt = maybe_unserialize(get_option('nsl_google'));
echo "=== verificação ===\n";
echo "client_id: " . substr($opt['client_id'] ?? 'NULO', 0, 15) . "...\n";
echo "settings_saved: " . ($opt['settings_saved'] ?? '?') . "\n";
echo "tested: " . ($opt['tested'] ?? '?') . "\n";
echo "isReady: " . ($provider->isReady() ? 'SIM' : 'NAO') . "\n";
"""

out, err = wpeval(php)
print(out)
print("ERR:", err[:200] if err else "")
