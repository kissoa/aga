#!/usr/bin/env python3
"""Cria as 12 páginas de jogo no WordPress via wp-cli."""
import subprocess, sys

SSH = ["ssh", "aga-web"]
WPC = ["cd", "/var/www/aga-wp", "&&", "sudo", "-u", "www-data", "wp"]

jogos = {
    "civ": {
        "titulo": "FreeCiv",
        "cat": "freeciv",
        "url": "https://civ.aga.org.ao",
        "desc": "Jogo de estratégia de construção de impérios, inspirado na história da civilização humana. Joga no browser contra a IA ou com amigos.",
        "modalidades": ["Um Jogador (vs IA)", "Multijogador (2, 4, 9 jogadores)", "Jogos Longos (1 turno/dia, até 50 jogadores)"],
        "guia": "1. Cria a tua civilização → 2. Explora o mapa → 3. Constrói cidades → 4. Investiga tecnologias → 5. Cria um exército → 6. Domina o mundo!",
    },
    "xadrez": {
        "titulo": "Xadrez",
        "cat": "xadrez",
        "url": "https://xadrez.aga.org.ao",
        "desc": "Xadrez online com 50+ variantes: Xadrez Clássico, Shogi, Xiangqi, Makruk, Bughouse e muito mais. Joga contra o computador ou contra outros.",
        "modalidades": ["Jogar contra o Computador", "Multijogador online", "Puzzles táticos", "Torneios"],
        "guia": "1. Escolhe uma variante → 2. Cria uma partida → 3. Joga contra o PC ou um amigo → 4. Aprende com os puzzles → 5. Entra nos torneios!",
    },
    "ogame": {
        "titulo": "OGame",
        "cat": "ogame",
        "url": "https://ogame.aga.org.ao",
        "desc": "Jogo de estratégia espacial em tempo real. Constrói a tua base, desenvolve tecnologias e domina a galáxia.",
        "modalidades": ["Estratégia espacial", "Multijogador massivo"],
        "guia": "1. Constrói minas → 2. Desenvolve investigação → 3. Constrói a frota → 4. Ataca ou negocia → 5. Domina a galáxia!",
    },
    "travianz": {
        "titulo": "TravianZ",
        "cat": "travianz",
        "url": "https://travianz.aga.org.ao",
        "desc": "Jogo de estratégia medieval. Constrói a tua aldeia, treina tropas e forma alianças.",
        "modalidades": ["Estratégia medieval", "Multijogador"],
        "guia": "1. Constrói edifícios → 2. Treina tropas → 3. Forma alianças → 4. Conquista aldeias!",
    },
    "suroi": {
        "titulo": "Suroi",
        "cat": "suroi",
        "url": "https://suroi.aga.org.ao",
        "desc": "Jogo battle royale em 2D no browser. Salta, apanha armas e sê o último a sobreviver.",
        "modalidades": ["Battle Royale", "Multijogador"],
        "guia": "1. Salta na ilha → 2. Apanha armas → 3. Sobrevive ao círculo → 4. Elimina os adversários → 5. Sê o último!",
    },
    "kaetram": {
        "titulo": "Kaetram",
        "cat": "kaetram",
        "url": "https://kaetram.aga.org.ao",
        "desc": "MMORPG 2D de código aberto no browser. Explora o mundo, combate monstros e evolui o teu personagem.",
        "modalidades": ["MMORPG", "Multijogador"],
        "guia": "1. Cria o teu herói → 2. Explora o mundo → 3. Combate monstros → 4. Evolui → 5. Junta-te a um grupo!",
    },
    "tosios": {
        "titulo": "Tosios",
        "cat": "tosios",
        "url": "https://tosios.aga.org.ao",
        "desc": "Jogo de estratégia em tempo real com confrontos entre reinos no browser.",
        "modalidades": ["Estratégia", "Multijogador"],
        "guia": "1. Escolhe o teu reino → 2. Constrói → 3. Ataca os vizinhos → 4. Domina!",
    },
    "supernova": {
        "titulo": "Supernova",
        "cat": "supernova",
        "url": "https://supernova.aga.org.ao",
        "desc": "Jogo de estratégia espacial no browser. Explora o espaço e constrói o teu império estelar.",
        "modalidades": ["Estratégia espacial", "Multijogador"],
        "guia": "1. Explora o espaço → 2. Constrói a tua frota → 3. Coloniza planetas → 4. Expande o império!",
    },
    "ageofai": {
        "titulo": "AgeOfAI",
        "cat": "ageofai",
        "url": "https://ageofai.aga.org.ao",
        "desc": "Jogo de estratégia com inteligência artificial. Constrói a tua civilização e enfrenta a IA.",
        "modalidades": ["Estratégia", "vs IA"],
        "guia": "1. Escolhe a civilização → 2. Constrói → 3. Treina o exército → 4. Vence a IA!",
    },
    "hypersomnia": {
        "titulo": "Hypersomnia",
        "cat": "hypersomnia",
        "url": "https://hypersomnia.aga.org.ao",
        "desc": "Jogo de tiro competitivo em 2D no browser. Combates rápidos e intensos.",
        "modalidades": ["FPS 2D", "Multijogador"],
        "guia": "1. Escolhe a arma → 2. Entra no campo → 3. Domina os adversários → 4. Vence a ronda!",
    },
    "scribble": {
        "titulo": "Scribble",
        "cat": "scribble",
        "url": "https://scribble.aga.org.ao",
        "desc": "Jogo de desenho e adivinhação multijogador no browser.",
        "modalidades": ["Social", "Multijogador"],
        "guia": "1. Entra na sala → 2. Desenha a palavra → 3. Adivinha as dos outros → 4. Ganha pontos!",
    },
    "woc": {
        "titulo": "World of Craft",
        "cat": "world-of-craft",
        "url": "https://woc.aga.org.ao",
        "desc": "Jogo sandbox de construção e sobrevivência no browser, inspirado em Minecraft.",
        "modalidades": ["Sandbox", "Sobrevivência"],
        "guia": "1. Explora o mundo → 2. Recolhe recursos → 3. Constrói → 4. Sobrevive!",
    },
}

def wp(*args):
    cmd = " ".join(WPC + list(args))
    r = subprocess.run(SSH + [cmd], capture_output=True, text=True, timeout=60)
    return r.stdout.strip(), r.stderr.strip()

for slug, info in jogos.items():
    mods = "\n".join(f"  <li>{m}</li>" for m in info["modalidades"])
    conteudo = f"""<!-- wp:heading {{"level":2}} -->
<h2 class="wp-block-heading">🎮 {info['titulo']} — Joga no Browser</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{info['desc']}</p>
<!-- /wp:paragraph -->

<!-- wp:buttons -->
<div class="wp-block-buttons">
<!-- wp:button {{"backgroundColor":"luminous-vivid-orange","textColor":"white"}} -->
<div class="wp-block-button"><a class="wp-block-button__link has-white-color has-luminous-vivid-orange-background-color has-text-color has-background wp-element-button" href="{info['url']}" target="_blank" rel="noreferrer noopener"><strong>JOGAR AGORA</strong></a></div>
<!-- /wp:button -->
</div>
<!-- /wp:buttons -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">📋 Modalidades</h3>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list">{mods}</ul>
<!-- /wp:list -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">📖 Guia Rápido</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{info['guia']}</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">📊 Estatísticas ao Vivo</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Jogadores online, servidores e rankings atualizados em tempo real:</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<iframe src="/stats/jogo/{slug}" style="width:100%;height:320px;border:1px solid #333;border-radius:8px;" loading="lazy"></iframe>
<!-- /wp:html -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">💬 Discussão</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Tira dúvidas e partilha estratégias no <a href="/forum">fórum do jogo</a>.</p>
<!-- /wp:paragraph -->"""

    out, err = wp("post", "create",
                  "--post_type=page",
                  f"--post_title={info['titulo']}",
                  f"--post_name={slug}",
                  f"--post_content={conteudo}",
                  "--post_status=publish",
                  f"--category={info['cat']}")
    print(f"{slug}: {out[:60]} {err[:40]}")

print("---")
print("12 páginas criadas")
