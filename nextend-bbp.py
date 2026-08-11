#!/usr/bin/env python3
"""Configura o Nextend para mostrar o botão Google no bbPress e remover o formulário padrão."""
import subprocess

def wpeval(code):
    with open("/tmp/_nsl_bbp.php", "w", encoding="utf-8") as f:
        f.write("<?php\n" + code + "\n")
    subprocess.run(["scp", "-q", "/tmp/_nsl_bbp.php", "aga-web:/tmp/"], timeout=30)
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp eval-file /tmp/_nsl_bbp.php"
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=120)
    subprocess.run(["ssh", "aga-web", "rm -f /tmp/_nsl_bbp.php"], timeout=20)
    return r.stdout.strip(), r.stderr.strip()

php = r"""
global $wpdb;
// opção global do Nextend (deserializar até array)
$raw = $wpdb->get_var("SELECT option_value FROM wp_options WHERE option_name='nextend_social_login'");
$data = maybe_unserialize($raw);
$rounds = 0;
while (is_string($data) && $rounds < 5) { $data = maybe_unserialize($data); $rounds++; }

if (!is_array($data)) { echo "ERRO: opção não é array\n"; exit; }

// mostrar o botão no bbPress (em vez do formulário padrão)
$data['show_bbpress'] = 'after';   // botão depois do formulário
$data['show_login_form'] = 'show'; // login padrão do WP
// esconder o registo padrão do WP? (só Google)
// redirect após login: home
$data['redirect'] = 'https://aga.org.ao/';
$data['redirect_reg'] = 'https://aga.org.ao/';

update_option('nextend_social_login', $data, false);
echo "bbPress configurado: show_bbpress=" . $data['show_bbpress'] . "\n";
echo "redirect=" . $data['redirect'] . "\n";

// verificar
$check = get_option('nextend_social_login');
echo "verificação show_bbpress: " . ($check['show_bbpress'] ?? '?') . "\n";
"""

out, err = wpeval(php)
print(out)
print("ERR:", err[:200] if err else "")
