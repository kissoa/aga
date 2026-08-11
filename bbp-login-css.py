#!/usr/bin/env python3
"""Esconde o formulário de login do bbPress (fica só o botão Google)."""
import subprocess

def wpeval(code):
    with open("/tmp/_bbp_css.php", "w", encoding="utf-8") as f:
        f.write("<?php\n" + code + "\n")
    subprocess.run(["scp", "-q", "/tmp/_bbp_css.php", "aga-web:/tmp/"], timeout=30)
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp eval-file /tmp/_bbp_css.php"
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=120)
    subprocess.run(["ssh", "aga-web", "rm -f /tmp/_bbp_css.php"], timeout=20)
    return r.stdout.strip(), r.stderr.strip()

# adicionar ao CSS do plugin AGA Gaming (ou criar regra no aga-login-only)
php = r"""
$target = WP_CONTENT_DIR . '/plugins/aga-login-only.php';
$code = file_get_contents($target);

// adicionar CSS para esconder o formulário do bbPress
$css_bbp = "
/* bbPress — login só com Google (esconder formulário de senha) */
form.bbp-login-form { display: none !important; }
#bbpress-forums .bbp-logged-in { display: block !important; }
";

// injetar o CSS no plugin (na função de enqueue)
$code = str_replace(
    "add_action('login_enqueue_scripts', function () {",
    "add_action('wp_enqueue_scripts', function () {
    \$css = '" . addslashes($css_bbp) . "';
    if (\$css) wp_add_inline_style('kadence-global', \$css);
});
add_action('login_enqueue_scripts', function () {",
    $code
);

file_put_contents($target, $code);
echo "CSS bbPress adicionado ao plugin\n";
"""

out, err = wpeval(php)
print(out)
print("ERR:", err[:150] if err else "")
