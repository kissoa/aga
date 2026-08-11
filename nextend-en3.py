#!/usr/bin/env python3
"""Ativa o provider Google na opção global nextend_social_login."""
import subprocess

def wpeval(code):
    with open("/tmp/_nsl_en3.php", "w", encoding="utf-8") as f:
        f.write("<?php\n" + code + "\n")
    subprocess.run(["scp", "-q", "/tmp/_nsl_en3.php", "aga-web:/tmp/"], timeout=30)
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp eval-file /tmp/_nsl_en3.php"
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=120)
    subprocess.run(["ssh", "aga-web", "rm -f /tmp/_nsl_en3.php"], timeout=20)
    return r.stdout.strip(), r.stderr.strip()

php = r"""
global $wpdb;
$opt = $wpdb->get_row("SELECT option_value FROM wp_options WHERE option_name='nextend_social_login'");
if ($opt) {
    $data = maybe_unserialize($opt->option_value);
    echo "existe, enabled atual: " . (is_array($data['enabled'] ?? null) ? implode(',', $data['enabled']) : 'vazio') . "\n";
} else {
    $data = array();
    echo "não existe — criar\n";
}

// adicionar google ao enabled
if (!is_array($data['enabled'] ?? null)) $data['enabled'] = array();
if (!in_array('google', $data['enabled'])) {
    $data['enabled'][] = 'google';
}
// garantir ordering com google
if (isset($data['ordering']) && is_array($data['ordering']) && !in_array('google', $data['ordering'])) {
    $data['ordering'][] = 'google';
}

if ($opt) {
    $wpdb->update($wpdb->prefix . 'options', array('option_value' => serialize($data)), array('option_name' => 'nextend_social_login'));
} else {
    add_option('nextend_social_login', $data);
}
echo "enabled agora: " . implode(',', $data['enabled']) . "\n";

// limpar cache de objectos
wp_cache_flush();

// verificar estado do provider
$provider = NextendSocialLogin::$providers['google'] ?? null;
if ($provider) {
    echo "getState: " . $provider->getState() . "\n";
}
"""

out, err = wpeval(php)
print(out)
print("ERR:", err[:200] if err else "")
