#!/usr/bin/env python3
"""Verifica e ativa a exibição do botão Google no login do Nextend."""
import subprocess

def wpeval(code):
    with open("/tmp/_nsl_show.php", "w", encoding="utf-8") as f:
        f.write("<?php\n" + code + "\n")
    subprocess.run(["scp", "-q", "/tmp/_nsl_show.php", "aga-web:/tmp/"], timeout=30)
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp eval-file /tmp/_nsl_show.php"
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=120)
    subprocess.run(["ssh", "aga-web", "rm -f /tmp/_nsl_show.php"], timeout=20)
    return r.stdout.strip(), r.stderr.strip()

php = r"""
// Opções globais do Nextend: onde mostrar os botões
$settings = NextendSocialLogin::$settings;
echo "=== opções globais atuais ===\n";
foreach ($settings->getAll('stored') as $k => $v) {
    $val = is_array($v) ? implode(',', $v) : (string)$v;
    if (strlen($val) < 80) echo "  $k = $val\n";
}
echo "\n=== opções relevantes para exibição ===\n";
$opts = array('show_login_form', 'show_register_form', 'show_bbpress', 'show_comment_form', 'redirect', 'redirect_reg');
foreach ($opts as $o) {
    echo "  $o = " . $settings->get($o) . "\n";
}
"""

out, err = wpeval(php)
print(out)
print("ERR:", err[:200] if err else "")
