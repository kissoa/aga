#!/usr/bin/env python3
"""Verifica a estrutura da opção nsl_google e o redirect URI."""
import subprocess

def wpeval(code):
    with open("/tmp/_nsl_check.php", "w", encoding="utf-8") as f:
        f.write("<?php\n" + code + "\n")
    subprocess.run(["scp", "-q", "/tmp/_nsl_check.php", "aga-web:/tmp/"], timeout=30)
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp eval-file /tmp/_nsl_check.php"
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=120)
    subprocess.run(["ssh", "aga-web", "rm -f /tmp/_nsl_check.php"], timeout=20)
    return r.stdout.strip(), r.stderr.strip()

php = r"""
global $wpdb;
$opt = $wpdb->get_var("SELECT option_value FROM wp_options WHERE option_name='nsl_google'");
$data = maybe_unserialize($opt);
echo "=== chaves da opção ===\n";
foreach ($data as $k => $v) {
    $val = is_array($v) ? json_encode($v) : (string)$v;
    echo "  $k = " . substr($val, 0, 40) . "\n";
}
echo "\n=== redirect URI que o plugin usa ===\n";
$provider = NextendSocialLogin::$providers['google'] ?? null;
if ($provider) {
    echo "login url: " . $provider->getLoginUrl() . "\n";
    echo "redirect: " . $provider->getRedirectUriForLoginFlow() . "\n";
}
echo "\n=== estado do provider ===\n";
echo "isReady: " . (method_exists($provider, 'isReady') ? ($provider->isReady() ? 'SIM' : 'NAO') : 'metodo nao existe') . "\n";
"""

out, err = wpeval(php)
print(out)
print("ERR:", err[:200] if err else "")
