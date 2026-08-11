#!/usr/bin/env python3
"""Verifica todas as opções de exibição do Nextend (login pages)."""
import subprocess

def wpeval(code):
    with open("/tmp/_nsl_all.php", "w", encoding="utf-8") as f:
        f.write("<?php\n" + code + "\n")
    subprocess.run(["scp", "-q", "/tmp/_nsl_all.php", "aga-web:/tmp/"], timeout=30)
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp eval-file /tmp/_nsl_all.php"
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=120)
    subprocess.run(["ssh", "aga-web", "rm -f /tmp/_nsl_all.php"], timeout=20)
    return r.stdout.strip(), r.stderr.strip()

php = r"""
$settings = NextendSocialLogin::$settings;
$all = $settings->getAll('stored');
echo "=== TODAS as opções (login-related) ===\n";
foreach ($all as $k => $v) {
    if (stripos($k, 'login') !== false || stripos($k, 'wp_') !== false || stripos($k, 'woocommerce') !== false || stripos($k, 'bbpress') !== false || stripos($k, 'redirect') !== false) {
        $val = is_array($v) ? implode(',', $v) : (string)$v;
        echo "  $k = " . substr($val, 0, 60) . "\n";
    }
}
"""

out, err = wpeval(php)
print(out)
print("ERR:", err[:200] if err else "")
