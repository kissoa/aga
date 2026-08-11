#!/usr/bin/env python3
"""Corrige a dupla serialização da opção nextend_social_login."""
import subprocess

def wpeval(code):
    with open("/tmp/_nsl_en5.php", "w", encoding="utf-8") as f:
        f.write("<?php\n" + code + "\n")
    subprocess.run(["scp", "-q", "/tmp/_nsl_en5.php", "aga-web:/tmp/"], timeout=30)
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp eval-file /tmp/_nsl_en5.php"
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=120)
    subprocess.run(["ssh", "aga-web", "rm -f /tmp/_nsl_en5.php"], timeout=20)
    return r.stdout.strip(), r.stderr.strip()

php = r"""
global $wpdb;
$raw = $wpdb->get_var("SELECT option_value FROM wp_options WHERE option_name='nextend_social_login'");

// deserializar até chegar ao array
$data = maybe_unserialize($raw);
$rounds = 0;
while (is_string($data) && $rounds < 5) {
    $data = maybe_unserialize($data);
    $rounds++;
}
echo "rounds de deserialização: $rounds\n";
echo "tipo final: " . gettype($data) . "\n";

if (is_array($data)) {
    // garantir enabled com google
    if (!is_array($data['enabled'] ?? null)) $data['enabled'] = array();
    if (!in_array('google', $data['enabled'])) $data['enabled'][] = 'google';
    echo "enabled: " . implode(',', $data['enabled']) . "\n";

    // gravar SEM dupla serialização (update_option serializa uma vez)
    update_option('nextend_social_login', $data, false);
    echo "gravado correctamente\n";

    // verificar
    $check = get_option('nextend_social_login');
    echo "verificação: " . gettype($check) . ", enabled=" . (is_array($check['enabled'] ?? null) ? implode(',', $check['enabled']) : '?') . "\n";
}
"""

out, err = wpeval(php)
print(out)
print("ERR:", err[:200] if err else "")
