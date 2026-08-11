#!/usr/bin/env python3
"""Remove o formulário de username/senha — autenticação só via Google OAuth."""
import subprocess

def wpeval(code):
    with open("/tmp/_nsl_only.php", "w", encoding="utf-8") as f:
        f.write("<?php\n" + code + "\n")
    subprocess.run(["scp", "-q", "/tmp/_nsl_only.php", "aga-web:/tmp/"], timeout=30)
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp eval-file /tmp/_nsl_only.php"
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=120)
    subprocess.run(["ssh", "aga-web", "rm -f /tmp/_nsl_only.php"], timeout=20)
    return r.stdout.strip(), r.stderr.strip()

# 1. Esconder o formulário padrão do wp-login via CSS (mantém o botão Google)
php1 = r"""
$css = "
/* Login só com Google — esconder formulário padrão */
body.login #loginform { display: none !important; }
body.login #nav { display: none !important; }
body.login #backtoblog { display: none !important; }
body.login h1 { margin-bottom: 2rem !important; }
#nsl-custom-login-form-vertical, #login .nsl-container { margin-top: 1.5rem !important; }
";
update_option('aga_login_css', $css);
echo "CSS login salvo: " . strlen($css) . " bytes\n";
"""

out, err = wpeval(php1)
print(out)
print("ERR1:", err[:100] if err else "")

# 2. Criar/actualizar o plugin que injeta o CSS + bloqueia o registo normal
php2 = r"""
// verificar se já existe um mu-plugin ou plugin de custom login
$target = WP_CONTENT_DIR . '/plugins/aga-login-only.php';
$code = <<<'PHP'
<?php
/*
Plugin Name: AGA Login Only Google
Description: Autenticação apenas via Google OAuth — esconde formulário de senha.
Version: 1.0
*/
add_action('login_enqueue_scripts', function () {
    $css = get_option('aga_login_css', '');
    if ($css) wp_add_inline_style('login', $css);
});
// Bloquear o login por senha (só Google)
add_filter('authenticate', function ($user, $username, $password) {
    // permite o fluxo do Nextend (que não passa por aqui como user/pass normal)
    if (!is_wp_error($user) && $user instanceof WP_User && isset($_POST['log']) && isset($_POST['pwd'])) {
        // só bloqueia se o utilizador existe E veio do formulário normal
        if ($username) return new WP_Error('login_social_only', 'A autenticação é apenas via Google.');
    }
    return $user;
}, 30, 3);
// Esconder o formulário do bbPress (login widget)
add_filter('bbp_get_template_part', function ($templates, $slug, $name) {
    return $templates;
}, 10, 3);
PHP;
file_put_contents($target, $code);
echo "plugin criado: $target\n";
"""

out2, err2 = wpeval(php2)
print(out2)
print("ERR2:", err2[:100] if err2 else "")

# 3. activar o plugin
r = subprocess.run(["ssh", "aga-web", "cd /var/www/aga-wp && sudo chown www-data:www-data wp-content/plugins/aga-login-only.php && sudo -u www-data wp plugin activate aga-login-only"], capture_output=True, text=True, timeout=60)
print(r.stdout.strip()[:100])
print(r.stderr.strip()[:100] if r.stderr.strip() else "")
