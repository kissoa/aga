#!/usr/bin/env python3
"""Cria tópico de boas-vindas em cada um dos 12 fóruns bbPress."""
import subprocess

def wp(*args):
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp " + " ".join(args)
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=60)
    return r.stdout.strip(), r.stderr.strip()

# IDs dos fóruns bbPress (criados antes: 51-62)
# FreeCiv=51, Xadrez=52, OGame=53, TravianZ=54, Suroi=55, Kaetram=56,
# Tosios=57, Supernova=58, AgeOfAI=59, Hypersomnia=60, Scribble=61, WorldOfCraft=62
forums = {
    51: "FreeCiv",
    52: "Xadrez",
    53: "OGame",
    54: "TravianZ",
    55: "Suroi",
    56: "Kaetram",
    57: "Tosios",
    58: "Supernova",
    59: "AgeOfAI",
    60: "Hypersomnia",
    61: "Scribble",
    62: "World of Craft",
}

for fid, nome in forums.items():
    conteudo = f"""Bem-vindo(a) ao fórum de **{nome}** da AGA!

Este é o espaço para:
- 💬 Discutir estratégias e tácticas
- ❓ Tirar dúvidas sobre o jogo
- 🏆 Combinar partidas e torneios
- 📢 Anunciar novidades

Para jogares agora: acede à página do jogo no menu **Jogos** ou pelo link direto.

Divirtam-se e boa sorte! 🎮"""

    # escrever conteúdo num ficheiro temporário
    tmp = f"/tmp/topic-{fid}.md"
    with open("/tmp/_topic_tmp.md", "w", encoding="utf-8") as f:
        f.write(conteudo)
    subprocess.run(["scp", "-q", "/tmp/_topic_tmp.md", f"aga-web:{tmp}"], timeout=30)
    out, err = wp("post", "create", tmp,
                  "--post_type=topic",
                  f"--post_title=Bem-vindo ao fórum de {nome}!",
                  "--post_status=publish",
                  "--porcelain")
    # associar o tópico ao fórum via meta
    if out.strip():
        tid = out.strip()
        wp("post", "meta", "update", tid, "_bbp_forum_id", str(fid))
        print(f"  {nome} (forum {fid}): tópico {tid}")
    else:
        print(f"  {nome}: ERRO {err[:60]}")
    subprocess.run(["ssh", "aga-web", f"rm -f {tmp}"], timeout=20)

print("done")
