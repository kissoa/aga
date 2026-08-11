#!/usr/bin/env python3
"""Ativa o provider Google na opção enabled (direto na BD)."""
import subprocess

def wpeval(code):
    with open("/tmp/_nsl_en2.php", "w", encoding="utf-8") as f:
        f.write("<?php\n" + code + "\n")
    subprocess.run(["scp", "-q", "/tmp/_nsl_en2.php", "aga-web:/tmp/"], timeout=30)
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp eval-file /tmp/_nsl_en2.php"
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=120)
    subprocess.run(["ssh", "aga-web", "rm -f /tmp/_nsl_en2.php"], timeout=20)
    return r.stdout.strip(), r.stderr.strip()

php = r"""
global $wpdb;
// encontrar a opção de config global do Nextend
$opt = $wpdb->get_row("SELECT option_name, option_value FROM wp_options WHERE option_name LIKE '%nsl%config%' OR option_name LIKE 'nsl%' LIMIT 5");
echo "opção global: " . ($opt->option_name ?? 'nenhuma') . "\n";

// a opção global do Nextend Social Login é 'nsl_config' normalmente
$rows = $wpdb->get_results("SELECT option_name FROM wp_options WHERE option_name LIKE 'nsl%'");
foreach ($rows as $r) { echo "  " . $r->option_name . "\n"; }
"""

out, err = wpeval(php)
print(out)
print("ERR:", err[:200] if err else "")
