#!/usr/bin/env python3
"""Ajusta o CSS: esconde só os campos do formulário, mantém o botão Google."""
import subprocess

def wpeval(code):
    with open("/tmp/_login_css2.php", "w", encoding="utf-8") as f:
        f.write("<?php\n" + code + "\n")
    subprocess.run(["scp", "-q", "/tmp/_login_css2.php", "aga-web:/tmp/"], timeout=30)
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp eval-file /tmp/_login_css2.php"
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=120)
    subprocess.run(["ssh", "aga-web", "rm -f /tmp/_login_css2.php"], timeout=20)
    return r.stdout.strip(), r.stderr.strip()

php = r"""
$css = "
/* Login só com Google — esconder os CAMPOS do formulário, não o container */
body.login #loginform p { display: none !important; }
body.login #loginform .submit { display: none !important; }
body.login #nav { display: none !important; }
body.login #backtoblog { display: none !important; }
body.login h1 { margin-bottom: 1.5rem !important; }
#nsl-custom-login-form-main, #login .nsl-container { margin-top: 1.2rem !important; }
body.login #login { padding-top: 2rem !important; }
/* mensagem de boas-vindas */
body.login::before {
    content: 'Entra com a tua conta Google para acederes ao fórum e à comunidade.';
    display: block;
    text-align: center;
    color: #8a8ab0;
    font-size: .9rem;
    max-width: 320px;
    margin: 1rem auto -1rem;
    line-height: 1.5;
}
";
update_option('aga_login_css', $css);
echo "CSS atualizado\n";
"""

out, err = wpeval(php)
print(out)
print("ERR:", err[:100] if err else "")
