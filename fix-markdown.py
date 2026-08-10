#!/usr/bin/env python3
"""Substitui markdown ** por HTML <strong> nos 12 tópicos (IDs 112-123)."""
import subprocess

def wpeval(code):
    with open("/tmp/_bbp_fix.php", "w", encoding="utf-8") as f:
        f.write("<?php\n" + code + "\n")
    subprocess.run(["scp", "-q", "/tmp/_bbp_fix.php", "aga-web:/tmp/"], timeout=30)
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp eval-file /tmp/_bbp_fix.php"
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=120)
    subprocess.run(["ssh", "aga-web", "rm -f /tmp/_bbp_fix.php"], timeout=20)
    return r.stdout.strip(), r.stderr.strip()

php = r"""
foreach (range(112, 123) as $tid) {
    $p = get_post($tid);
    if (!$p || $p->post_type !== 'topic') { echo "skip $tid\n"; continue; }
    $novo = str_replace('**', '<strong>', $p->post_content);
    // fechar o strong: **X** -> <strong>X</strong>
    $novo = preg_replace('/<strong>([^<]+)<strong>/', '<strong>$1</strong>', $novo);
    // se ainda houver abertos sem fecho, fechar no fim
    $abertos = substr_count($novo, '<strong>');
    $fechados = substr_count($novo, '</strong>');
    $novo .= str_repeat('</strong>', max(0, $abertos - $fechados));
    wp_update_post(array('ID' => $tid, 'post_content' => $novo));
    echo "fixed $tid\n";
}
// limpar cache
wp_cache_flush();
"""

out, err = wpeval(php)
print(out)
print("ERR:", err[:200] if err else "")
