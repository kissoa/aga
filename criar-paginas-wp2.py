#!/usr/bin/env python3
"""Cria as 12 páginas de jogo no WordPress via wp-cli — conteúdo via stdin (sem aspas no shell)."""
import subprocess

SSH = ["ssh", "aga-web"]
JOGOS = {
    "civ": ("FreeCiv", "freeciv", "https://civ.aga.org.ao",
            "Jogo de estratégia de construção de impérios, inspirado na história da civilização humana. Joga no browser contra a IA ou com amigos.",
            ["Um Jogador (vs IA)", "Multijogador (2, 4, 9 jogadores)", "Jogos Longos (1 turno/dia, até 50 jogadores)"],
            "1. Cria a tua civilização → 2. Explora o mapa → 3. Constrói cidades → 4. Investiga tecnologias → 5. Cria um exército → 6. Domina o mundo!"),
    "xadrez": ("Xadrez", "xadrez", "https://xadrez.aga.org.ao",
               "Xadrez online com 50+ variantes: Xadrez Clássico, Shogi, Xiangqi, Makruk, Bughouse e muito mais. Joga contra o computador ou contra outros.",
               ["Jogar contra o Computador", "Multijogador online", "Puzzles táticos", "Torneios"],
               "1. Escolhe uma variante → 2. Cria uma partida → 3. Joga contra o PC ou um amigo → 4. Aprende com os puzzles → 5. Entra nos torneios!"),
    "ogame": ("OGame", "ogame", "https://ogame.aga.org.ao",
              "Jogo de estratégia espacial em tempo real. Constrói a tua base, desenvolve tecnologias e domina a galáxia.",
              ["Estratégia espacial", "Multijogador massivo"],
              "1. Constrói minas → 2. Desenvolve investigação → 3. Constrói a frota → 4. Ataca ou negocia → 5. Domina a galáxia!"),
    "travianz": ("TravianZ", "travianz", "https://travianz.aga.org.ao",
                 "Jogo de estratégia medieval. Constrói a tua aldeia, treina tropas e forma alianças.",
                 ["Estratégia medieval", "Multijogador"],
                 "1. Constrói edifícios → 2. Treina tropas → 3. Forma alianças → 4. Conquista aldeias!"),
    "suroi": ("Suroi", "suroi", "https://suroi.aga.org.ao",
              "Jogo battle royale em 2D no browser. Salta, apanha armas e sê o último a sobreviver.",
              ["Battle Royale", "Multijogador"],
              "1. Salta na ilha → 2. Apanha armas → 3. Sobrevive ao círculo → 4. Elimina os adversários → 5. Sê o último!"),
    "kaetram": ("Kaetram", "kaetram", "https://kaetram.aga.org.ao",
                "MMORPG 2D de código aberto no browser. Explora o mundo, combate monstros e evolui o teu personagem.",
                ["MMORPG", "Multijogador"],
                "1. Cria o teu herói → 2. Explora o mundo → 3. Combate monstros → 4. Evolui → 5. Junta-te a um grupo!"),
    "tosios": ("Tosios", "tosios", "https://tosios.aga.org.ao",
               "Jogo de estratégia em tempo real com confrontos entre reinos no browser.",
               ["Estratégia", "Multijogador"],
               "1. Escolhe o teu reino → 2. Constrói → 3. Ataca os vizinhos → 4. Domina!"),
    "supernova": ("Supernova", "supernova", "https://supernova.aga.org.ao",
                  "Jogo de estratégia espacial no browser. Explora o espaço e constrói o teu império estelar.",
                  ["Estratégia espacial", "Multijogador"],
                  "1. Explora o espaço → 2. Constrói a tua frota → 3. Coloniza planetas → 4. Expande o império!"),
    "ageofai": ("AgeOfAI", "ageofai", "https://ageofai.aga.org.ao",
                "Jogo de estratégia com inteligência artificial. Constrói a tua civilização e enfrenta a IA.",
                ["Estratégia", "vs IA"],
                "1. Escolhe a civilização → 2. Constrói → 3. Treina o exército → 4. Vence a IA!"),
    "hypersomnia": ("Hypersomnia", "hypersomnia", "https://hypersomnia.aga.org.ao",
                    "Jogo de tiro competitivo em 2D no browser. Combates rápidos e intensos.",
                    ["FPS 2D", "Multijogador"],
                    "1. Escolhe a arma → 2. Entra no campo → 3. Domina os adversários → 4. Vence a ronda!"),
    "scribble": ("Scribble", "scribble", "https://scribble.aga.org.ao",
                 "Jogo de desenho e adivinhação multijogador no browser.",
                 ["Social", "Multijogador"],
                 "1. Entra na sala → 2. Desenha a palavra → 3. Adivinha as dos outros → 4. Ganha pontos!"),
    "woc": ("World of Craft", "world-of-craft", "https://woc.aga.org.ao",
            "Jogo sandbox de construção e sobrevivência no browser, inspirado em Minecraft.",
            ["Sandbox", "Sobrevivência"],
            "1. Explora o mundo → 2. Recolhe recursos → 3. Constrói → 4. Sobrevive!"),
}

def criar_pagina(slug, titulo, cat, url, desc, mods, guia):
    """Cria página com conteúdo via stdin (evita problemas de aspas no shell)."""
    mods_html = "".join(f"<li>{m}</li>" for m in mods)
    conteudo = f"""<h2>🎮 {titulo} — Joga no Browser</h2>
<p>{desc}</p>
<p><a href="{url}" target="_blank" rel="noopener"><strong style="background:#f59e0b;color:#fff;padding:10px 20px;border-radius:6px;text-decoration:none;">JOGAR AGORA</strong></a></p>
<h3>📋 Modalidades</h3>
<ul>{mods_html}</ul>
<h3>📖 Guia Rápido</h3>
<p>{guia}</p>
<h3>📊 Estatísticas ao Vivo</h3>
<p>Jogadores online, servidores e rankings atualizados em tempo real:</p>
<iframe src="/stats/jogo/{slug}" style="width:100%;height:320px;border:1px solid #333;border-radius:8px;" loading="lazy"></iframe>
<h3>💬 Discussão</h3>
<p>Tira dúvidas e partilha estratégias no <a href="/forum">fórum do jogo</a>.</p>"""

    # escrever conteúdo num ficheiro temporário no servidor
    tmp = f"/tmp/wp-page-{slug}.html"
    with open("/tmp/_conteudo_tmp.html", "w", encoding="utf-8") as f:
        f.write(conteudo)
    subprocess.run(["scp", "-q", "/tmp/_conteudo_tmp.html", f"aga-web:{tmp}"], timeout=30)
    cmd = (f"cd /var/www/aga-wp && sudo -u www-data wp post create {tmp} "
           f"--post_type=page --post_title='{titulo}' --post_name='{slug}' "
           f"--post_status=publish --post_category='{cat}' --porcelain")
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=60)
    # limpar tmp
    subprocess.run(["ssh", "aga-web", f"rm -f {tmp}"], timeout=20)
    return r.stdout.strip(), r.stderr.strip()

for slug, (titulo, cat, url, desc, mods, guia) in JOGOS.items():
    out, err = criar_pagina(slug, titulo, cat, url, desc, mods, guia)
    print(f"{slug}: {'OK ID=' + out if out else err[:60]}")

print("---")
print("done")
