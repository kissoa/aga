#!/usr/bin/env python3
"""Corrige o CSS do bbPress: esconde só os campos, mantém o botão Google visível."""
import subprocess

def wpeval(code):
    with open("/tmp/_bbp_v3.php", "w", encoding="utf-8") as f:
        f.write("<?php\n" + code + "\n")
    subprocess.run(["scp", "-q", "/tmp/_bbp_v3.php", "aga-web:/tmp/"], timeout=30)
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp eval-file /tmp/_bbp_v3.php"
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=120)
    subprocess.run(["ssh", "aga-web", "rm -f /tmp/_bbp_v3.php"], timeout=20)
    return r.stdout.strip(), r.stderr.strip()

php = r"""
$target = WP_CONTENT_DIR . '/plugins/aga-login-only.php';
$code = <<<'PHP'
<?php
/*
Plugin Name: AGA Login Only Google
Description: Autenticação apenas via Google OAuth — esconde formulário de senha.
Version: 1.2
*/

// CSS frontend (bbPress etc.) — esconde CAMPOS, mantém botão Google
add_action('wp_enqueue_scripts', function () {
    $css = "/* AGA-BBP — esconder campos do form, manter botão Google */
form.bbp-login-form .bbp-username { display: none !important; }
form.bbp-login-form .bbp-password { display: none !important; }
form.bbp-login-form .bbp-remember-me { display: none !important; }
form.bbp-login-form .bbp-submit-wrapper { display: none !important; }
form.bbp-login-form p { margin: 0 !important; }
#bbpress-forums .nsl-container { margin-top: .5rem !important; }
#bbpress-forums .bbp-logged-in { display: block !important; }
";
    if (wp_style_is('kadence-global', 'registered')) {
        wp_add_inline_style('kadence-global', $css);
    } else {
        add_action('wp_footer', function () use ($css) {
            echo '<style>' . $css . '</style>';
        }, 999);
    }
}, 999);

// CSS do login do WP — só Google
add_action('login_enqueue_scripts', function () {
    $css = get_option('aga_login_css', '');
    if ($css) wp_add_inline_style('login', $css);
});

// Bloquear o login por senha (só Google)
add_filter('authenticate', function ($user, $username, $password) {
    if (!is_wp_error($user) && $user instanceof WP_User && isset($_POST['log']) && isset($_POST['pwd'])) {
        if ($username) return new WP_Error('login_social_only', 'A autenticação é apenas via Google.');
    }
    return $user;
}, 30, 3);
PHP;

file_put_contents($target, $code);
echo "plugin atualizado (campos bbPress escondidos, botão mantido)\n";
echo shell_exec('php -l ' . escapeshellarg($target)) ?: '';
"""

out, err = wpeval(php)
print(out)
print("ERR:", err[:150] if err else "")
