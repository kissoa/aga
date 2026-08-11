#!/usr/bin/env python3
"""Debug: verifica se o hook do plugin corre e adiciona o CSS com prioridade alta."""
import subprocess

def wpeval(code):
    with open("/tmp/_bbp_dbg.php", "w", encoding="utf-8") as f:
        f.write("<?php\n" + code + "\n")
    subprocess.run(["scp", "-q", "/tmp/_bbp_dbg.php", "aga-web:/tmp/"], timeout=30)
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp eval-file /tmp/_bbp_dbg.php"
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=120)
    subprocess.run(["ssh", "aga-web", "rm -f /tmp/_bbp_dbg.php"], timeout=20)
    return r.stdout.strip(), r.stderr.strip()

# testar com um hook de altíssima prioridade e verificar via get_option
php = r"""
// gravar a opção para debug
$target = WP_CONTENT_DIR . '/plugins/aga-login-only.php';
$code = file_get_contents($target);

// Substituir o hook wp_enqueue_scripts para usar prioridade 999 (depois do tema)
$novo_hook = "add_action('wp_enqueue_scripts', function () {
    // bbPress — login só com Google
    \$css = '/* AGA-BBP */ form.bbp-login-form { display: none !important; }';
    if (wp_style_is('kadence-global', 'registered')) {
        wp_add_inline_style('kadence-global', \$css);
    } else {
        // fallback: injetar no footer
        add_action('wp_footer', function () use (\$css) {
            echo '<style>' . \$css . '</style>';
        }, 999);
    }
}, 999);";

// substituir o primeiro add_action('wp_enqueue_scripts'... até ao fim do bloco
$pattern = "/add_action\('wp_enqueue_scripts', function \(\) \{.*?\n\}\), 100\);/s";
// o plugin atual tem prioridade default (10) — procurar o bloco
$novo_codigo = preg_replace(
    "/add_action\('wp_enqueue_scripts', function \(\) \{\s*\$css = '[^']*';\s*if \(\$css\) wp_add_inline_style\('kadence-global', \$css\);\s*\}\);/s",
    $novo_hook,
    $code
);

if ($novo_codigo === $code) {
    echo "AVISO: padrão não substituiu — o código atual é:\n";
    echo substr($code, 0, 300) . "\n";
} else {
    file_put_contents($target, $novo_codigo);
    echo "OK: hook atualizado com prioridade 999 + fallback footer\n";
}
"""

out, err = wpeval(php)
print(out)
print("ERR:", err[:150] if err else "")
