#!/usr/bin/env python3
"""Corrige a config do Google no Nextend — grava o array completo de uma vez."""
import subprocess

def wpeval(code):
    with open("/tmp/_nsl_fix.php", "w", encoding="utf-8") as f:
        f.write("<?php\n" + code + "\n")
    subprocess.run(["scp", "-q", "/tmp/_nsl_fix.php", "aga-web:/tmp/"], timeout=30)
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp eval-file /tmp/_nsl_fix.php"
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=120)
    subprocess.run(["ssh", "aga-web", "rm -f /tmp/_nsl_fix.php"], timeout=20)
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

// limpar a opcao atual e gravar o array completo
global $wpdb;
$wpdb->delete($wpdb->prefix . 'options', array('option_name' => 'nsl_google'));

$values = array(
    'settings_saved' => '1',
    'client_id' => '{client_id}',
    'client_secret' => '{client_secret}',
    'tested' => '1',
    'login_label' => 'Continuar com Google',
    'register_label' => 'Continuar com Google',
);
// usar o metodo do provider (grava serializado)
$provider->settings->update($values);

// verificar
$opt = $wpdb->get_var("SELECT option_value FROM wp_options WHERE option_name='nsl_google'");
$data = maybe_unserialize($opt);
echo "tipo: " . gettype($data) . "\n";
if (is_array($data)) {{
    echo "client_id: " . substr($data['client_id'] ?? '', 0, 15) . "...\n";
    echo "settings_saved: " . ($data['settings_saved'] ?? '?') . "\n";
    echo "tested: " . ($data['tested'] ?? '?') . "\n";
    echo "login_label: " . ($data['login_label'] ?? '?') . "\n";
}}
echo "redirect: " . $provider->getRedirectUriForLoginFlow() . "\n";
"""

out, err = wpeval(php)
print(out)
print("ERR:", err[:200] if err else "")
