#!/usr/bin/env python3
"""Inicializa o Nextend Social Login e configura o Google OAuth."""
import subprocess, base64

def wpeval(code):
    with open("/tmp/_nextend.php", "w", encoding="utf-8") as f:
        f.write("<?php\n" + code + "\n")
    subprocess.run(["scp", "-q", "/tmp/_nextend.php", "aga-web:/tmp/"], timeout=30)
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp eval-file /tmp/_nextend.php"
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=120)
    subprocess.run(["ssh", "aga-web", "rm -f /tmp/_nextend.php"], timeout=20)
    return r.stdout.strip(), r.stderr.strip()

# 1. inicializar o plugin (cria storage)
php1 = r"""
if (class_exists('NextendSocialLogin')) {
    // forçar instalação/storage
    if (method_exists('NextendSocialLogin', 'checkInstalled')) {
        NextendSocialLogin::checkInstalled();
        echo "checkInstalled OK\n";
    }
    if (method_exists('NextendSocialLogin', 'maybeUpgrade')) {
        NextendSocialLogin::maybeUpgrade();
        echo "maybeUpgrade OK\n";
    }
    // listar providers registados
    $providers = NextendSocialLogin::$providers ?? array();
    echo "providers: " . implode(',', array_keys($providers)) . "\n";
    if (isset($providers['google'])) {
        echo "google registado: " . ($providers['google']->isReady() ? 'PRONTO' : 'NÃO configurado') . "\n";
    }
} else {
    echo "classe não carregada\n";
}
// mostrar storage tables
global $wpdb;
$t = $wpdb->get_results("SHOW TABLES LIKE '%nextend2%'");
echo "tabelas nextend2: " . count($t) . "\n";
foreach ($t as $r) { echo "  " . implode('', (array)$r) . "\n"; }
"""

out, err = wpeval(php1)
print("=== INIT ===")
print(out)
print("ERR:", err[:200] if err else "")
