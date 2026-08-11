#!/usr/bin/env python3
"""Configura o Google OAuth no Nextend Social Login (lê credenciais do pychess)."""
import subprocess

def wpeval(code):
    with open("/tmp/_nsl_cfg.php", "w", encoding="utf-8") as f:
        f.write("<?php\n" + code + "\n")
    subprocess.run(["scp", "-q", "/tmp/_nsl_cfg.php", "aga-web:/tmp/"], timeout=30)
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp eval-file /tmp/_nsl_cfg.php"
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=120)
    subprocess.run(["ssh", "aga-web", "rm -f /tmp/_nsl_cfg.php"], timeout=20)
    return r.stdout.strip(), r.stderr.strip()

# ler as credenciais do pychess (no aga-lichess) e gerar o PHP com elas
r = subprocess.run(["ssh", "aga-lichess", "sudo cat /etc/pychess.env | grep -E 'GOOGLE_CLIENT_ID|GOOGLE_CLIENT_SECRET'"], capture_output=True, text=True, timeout=30)
creds = {}
for linha in r.stdout.strip().split("\n"):
    if "=" in linha:
        k, v = linha.split("=", 1)
        creds[k.strip()] = v.strip()
print("credenciais lidas:", {k: v[:10] + "..." for k, v in creds.items()})

client_id = creds.get("GOOGLE_CLIENT_ID", "")
client_secret = creds.get("GOOGLE_CLIENT_SECRET", "")

php = f"""
// Configurar o provider Google no Nextend
$provider = NextendSocialLogin::$providers['google'] ?? null;
if (!$provider) {{ echo "ERRO: provider google nao encontrado\n"; exit; }}

$settings = $provider->settings;
$values = array(
    'settings_saved' => '1',
    'client_id' => '{client_id}',
    'client_secret' => '{client_secret}',
    'tested' => '1',
    'login_label' => 'Continuar com Google',
    'register_label' => 'Continuar com Google',
);
foreach ($values as $k => $v) {{
    $settings->update($k, $v);
}}
// também via array update (alguns campos são em grupo)
$settings->update(array(
    'client_id' => '{client_id}',
    'client_secret' => '{client_secret}',
    'settings_saved' => '1',
    'tested' => '1',
));
echo "Google configurado no Nextend\n";

// verificar o que ficou gravado
global $wpdb;
$opt = $wpdb->get_var("SELECT option_value FROM wp_options WHERE option_name='nsl_google'");
echo "opcao nsl_google: " . (strlen($opt) . " bytes") . "\n";
if ($opt) {{
    $data = maybe_unserialize($opt);
    echo "client_id gravado: " . substr($data['client_id'] ?? '', 0, 12) . "...\n";
    echo "settings_saved: " . ($data['settings_saved'] ?? '?') . "\n";
    echo "tested: " . ($data['tested'] ?? '?') . "\n";
}}
"""

out, err = wpeval(php)
print(out)
print("ERR:", err[:200] if err else "")
