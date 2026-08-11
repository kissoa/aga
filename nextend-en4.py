#!/usr/bin/env python3
"""Inspeciona e corrige a opção global nextend_social_login."""
import subprocess

def wpeval(code):
    with open("/tmp/_nsl_en4.php", "w", encoding="utf-8") as f:
        f.write("<?php\n" + code + "\n")
    subprocess.run(["scp", "-q", "/tmp/_nsl_en4.php", "aga-web:/tmp/"], timeout=30)
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp eval-file /tmp/_nsl_en4.php"
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=120)
    subprocess.run(["ssh", "aga-web", "rm -f /tmp/_nsl_en4.php"], timeout=20)
    return r.stdout.strip(), r.stderr.strip()

php = r"""
global $wpdb;
$raw = $wpdb->get_var("SELECT option_value FROM wp_options WHERE option_name='nextend_social_login'");
echo "raw (primeiros 300): " . substr($raw, 0, 300) . "\n";
echo "\ntype: " . gettype(maybe_unserialize($raw)) . "\n";
"""

out, err = wpeval(php)
print(out)
print("ERR:", err[:200] if err else "")
