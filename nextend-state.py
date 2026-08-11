#!/usr/bin/env python3
"""Verifica o estado real do provider Google e o que o get() devolve."""
import subprocess

def wpeval(code):
    with open("/tmp/_nsl_state.php", "w", encoding="utf-8") as f:
        f.write("<?php\n" + code + "\n")
    subprocess.run(["scp", "-q", "/tmp/_nsl_state.php", "aga-web:/tmp/"], timeout=30)
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp eval-file /tmp/_nsl_state.php"
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=120)
    subprocess.run(["ssh", "aga-web", "rm -f /tmp/_nsl_state.php"], timeout=20)
    return r.stdout.strip(), r.stderr.strip()

php = r"""
$provider = NextendSocialLogin::$providers['google'] ?? null;
if (!$provider) { echo "ERRO: sem provider google\n"; exit; }

echo "=== opção bruta ===\n";
global $wpdb;
$raw = $wpdb->get_var("SELECT option_value FROM wp_options WHERE option_name='nsl_google'");
echo "bytes: " . strlen($raw) . "\n";
echo "primeiros 200: " . substr($raw, 0, 200) . "\n";

echo "\n=== get() do provider ===\n";
echo "client_id: " . substr($provider->settings->get('client_id'), 0, 15) . "...\n";
echo "client_secret: " . substr($provider->settings->get('client_secret'), 0, 10) . "...\n";
echo "tested: " . $provider->settings->get('tested') . "\n";
echo "settings_saved: " . $provider->settings->get('settings_saved') . "\n";

echo "\n=== required fields ===\n";
foreach ($provider->getRequiredFields() as $k => $label) {
    $v = $provider->settings->get($k);
    echo "  $k ($label): " . (empty($v) ? 'VAZIO!' : 'ok (' . substr($v, 0, 10) . '...)') . "\n";
}

echo "\n=== getState ===\n";
echo $provider->getState() . "\n";
"""

out, err = wpeval(php)
print(out)
print("ERR:", err[:200] if err else "")
