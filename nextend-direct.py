#!/usr/bin/env python3
"""Grava a config do Google directamente na opção nsl_google com a estrutura completa."""
import subprocess

def wpeval(code):
    with open("/tmp/_nsl_direct.php", "w", encoding="utf-8") as f:
        f.write("<?php\n" + code + "\n")
    subprocess.run(["scp", "-q", "/tmp/_nsl_direct.php", "aga-web:/tmp/"], timeout=30)
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp eval-file /tmp/_nsl_direct.php"
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=120)
    subprocess.run(["ssh", "aga-web", "rm -f /tmp/_nsl_direct.php"], timeout=20)
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

// ver os defaults do provider (o que o plugin espera)
$defaults = $provider->settings->getDefaults();
echo "=== defaults do provider ===\n";
foreach ($defaults as $k => $v) {{
    $val = is_array($v) ? 'array' : (string)$v;
    echo "  $k = " . substr($val, 0, 40) . "\n";
}}

// montar a opção com defaults + stored
$stored = array(
    'settings_saved' => '1',
    'client_id' => '{client_id}',
    'client_secret' => '{client_secret}',
    'tested' => '1',
    'login_label' => 'Continuar com Google',
    'register_label' => 'Continuar com Google',
);
$option = array(
    'default' => $defaults,
    'stored'  => $stored,
);
update_option('nsl_google', $option);

// verificar
$opt = get_option('nsl_google');
echo "=== verificação ===\n";
echo "stored client_id: " . substr($opt['stored']['client_id'] ?? '', 0, 15) . "...\n";
echo "stored settings_saved: " . ($opt['stored']['settings_saved'] ?? '?') . "\n";
echo "stored tested: " . ($opt['stored']['tested'] ?? '?') . "\n";
echo "isReady: " . ($provider->isReady() ? 'SIM' : 'NAO') . "\n";
"""

out, err = wpeval(php)
print(out)
print("ERR:", err[:200] if err else "")
