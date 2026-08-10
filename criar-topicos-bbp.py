#!/usr/bin/env python3
"""Recria os 12 tópicos via bbp_insert_topic (fluxo nativo do bbPress)."""
import subprocess

def wpeval(code):
    # escrever o PHP num ficheiro e correr wp eval-file
    with open("/tmp/_bbp_topics.php", "w", encoding="utf-8") as f:
        f.write("<?php\n" + code + "\n")
    subprocess.run(["scp", "-q", "/tmp/_bbp_topics.php", "aga-web:/tmp/"], timeout=30)
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp eval-file /tmp/_bbp_topics.php"
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=120)
    subprocess.run(["ssh", "aga-web", "rm -f /tmp/_bbp_topics.php"], timeout=20)
    return r.stdout.strip(), r.stderr.strip()

php = r"""
$forums = array(
    51 => 'FreeCiv', 52 => 'Xadrez', 53 => 'OGame', 54 => 'TravianZ', 55 => 'Suroi',
    56 => 'Kaetram', 57 => 'Tosios', 58 => 'Supernova', 59 => 'AgeOfAI', 60 => 'Hypersomnia',
    61 => 'Scribble', 62 => 'World of Craft',
);
// apagar os tópicos antigos (88-99) para recriar limpos
foreach (range(88, 99) as $old) {
    $p = get_post($old);
    if ($p && $p->post_type === 'topic') wp_delete_post($old, true);
}
// utilizador para criar os tópicos (admin)
$admin = get_users(array('role' => 'administrator', 'number' => 1));
$author = $admin ? $admin[0]->ID : 1;

foreach ($forums as $fid => $nome) {
    $args = array(
        'post_title'   => 'Bem-vindo ao fórum de ' . $nome . '!',
        'post_content' => "Bem-vindo(a) ao fórum de **$nome** da AGA!\n\nEste é o espaço para:\n- 💬 Discutir estratégias e tácticas\n- ❓ Tirar dúvidas sobre o jogo\n- 🏆 Combinar partidas e torneios\n- 📢 Anunciar novidades\n\nDivirtam-se! 🎮",
        'post_author'  => $author,
        'post_status'  => bbp_get_public_status_id(),
        'post_parent'  => $fid,
    );
    $tid = bbp_insert_topic($args, array('forum_id' => $fid));
    if (is_wp_error($tid) || !$tid) {
        echo "ERRO $nome: " . (is_wp_error($tid) ? $tid->get_error_message() : 'falhou') . "\n";
    } else {
        echo "OK $nome: tópico $tid\n";
    }
}
"""

out, err = wpeval(php)
print(out)
print("ERR:", err[:200] if err else "")
