#!/usr/bin/env python3
"""Mostra o redirect URI exacto que o Nextend envia ao Google."""
import subprocess

def wpeval(code):
    with open("/tmp/_nsl_uri.php", "w", encoding="utf-8") as f:
        f.write("<?php\n" + code + "\n")
    subprocess.run(["scp", "-q", "/tmp/_nsl_uri.php", "aga-web:/tmp/"], timeout=30)
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp eval-file /tmp/_nsl_uri.php"
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=120)
    subprocess.run(["ssh", "aga-web", "rm -f /tmp/_nsl_uri.php"], timeout=20)
    return r.stdout.strip(), r.stderr.strip()

php = r"""
$provider = NextendSocialLogin::$providers['google'] ?? null;
if (!$provider) { echo "sem provider\n"; exit; }

// o redirect URI que o plugin envia ao Google
$redirect = $provider->getRedirectUriForAuthFlow();
echo "redirect_uri: " . $redirect . "\n";

// o login url
echo "login_url: " . $provider->getLoginUrl() . "\n";

// a base redirect (a que o Google espera em app creation)
if (method_exists($provider, 'getBaseRedirectUriForAppCreation')) {
    echo "base_redirect: " . $provider->getBaseRedirectUriForAppCreation() . "\n";
}
"""

out, err = wpeval(php)
print(out)
print("ERR:", err[:200] if err else "")
