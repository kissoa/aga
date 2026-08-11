#!/usr/bin/env python3
"""Ativa o provider Google na lista 'enabled' do Nextend."""
import subprocess

def wpeval(code):
    with open("/tmp/_nsl_enable.php", "w", encoding="utf-8") as f:
        f.write("<?php\n" + code + "\n")
    subprocess.run(["scp", "-q", "/tmp/_nsl_enable.php", "aga-web:/tmp/"], timeout=30)
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp eval-file /tmp/_nsl_enable.php"
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=120)
    subprocess.run(["ssh", "aga-web", "rm -f /tmp/_nsl_enable.php"], timeout=20)
    return r.stdout.strip(), r.stderr.strip()

php = r"""
// Ver a opção global 'enabled'
$settings = NextendSocialLogin::$settings;
$enabled = $settings->get('enabled');
echo "enabled atual: " . (is_array($enabled) ? implode(',', $enabled) : var_export($enabled, true)) . "\n";

// Adicionar 'google'
if (!is_array($enabled)) $enabled = array();
if (!in_array('google', $enabled)) {
    $enabled[] = 'google';
    $settings->set('enabled', $enabled);
    // forçar store
    global $wpdb;
    $all = $settings->getAll('final');
    $wpdb->update(
        $wpdb->prefix . 'options',
        array('option_value' => serialize($all)),
        array('option_name' => NextendSocialLogin::$settings->getOptionKey())
    );
    echo "google adicionado ao enabled\n";
} else {
    echo "google já estava no enabled\n";
}

// verificar estado do provider
$provider = NextendSocialLogin::$providers['google'] ?? null;
if ($provider) {
    echo "getState: " . $provider->getState() . "\n";
}
"""

out, err = wpeval(php)
print(out)
print("ERR:", err[:200] if err else "")
