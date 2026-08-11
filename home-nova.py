#!/usr/bin/env python3
"""Reconstrói a página Início (5) com design limpo e profissional."""
import subprocess

def wp(*args):
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp " + " ".join(args)
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=60)
    return r.stdout.strip(), r.stderr.strip()

jogos = [
    ("🌍", "FreeCiv", "/civ/", "Estratégia de impérios"),
    ("♟️", "Xadrez", "/xadrez/", "50+ variantes"),
    ("🚀", "OGame", "/ogame/", "Estratégia espacial"),
    ("🏰", "TravianZ", "/travianz/", "Estratégia medieval"),
    ("🎯", "Suroi", "/suroi/", "Battle Royale 2D"),
    ("⚔️", "Kaetram", "/kaetram/", "MMORPG 2D"),
    ("👑", "Tosios", "/tosios/", "Reinos em guerra"),
    ("✨", "Supernova", "/supernova/", "Império estelar"),
    ("🤖", "AgeOfAI", "/ageofai/", "Estratégia vs IA"),
    ("🔫", "Hypersomnia", "/hypersomnia/", "FPS 2D"),
    ("✏️", "Scribble", "/scribble/", "Desenho e adivinha"),
    ("⛏️", "World of Craft", "/woc/", "Sandbox"),
]

cards = "".join(
    f'<a href="{url}" class="aga-jogo-card">'
    f'<span class="aga-jogo-emoji">{emoji}</span>'
    f'<span class="aga-jogo-nome">{nome}</span>'
    f'<span class="aga-jogo-desc">{desc}</span>'
    f'<span class="aga-jogo-jogar">Jogar →</span>'
    f'</a>'
    for emoji, nome, url, desc in jogos
)

conteudo = f"""<!-- wp:html -->
<div class="aga-hero">
  <div class="aga-hero-badge">🇦🇴 COMUNIDADE GAMING DE ANGOLA</div>
  <h1>Joga grátis, <span class="aga-gold">no browser</span>.</h1>
  <p>12 jogos 100% grátis, 100% web, 100% open source. Sem download, sem pagar — só abrir e jogar.</p>
  <div class="aga-hero-cta">
    <a href="#jogos" class="aga-btn-primary">🎮 Explorar Jogos</a>
    <a href="/forum/" class="aga-btn-secondary">💬 Comunidade</a>
  </div>
</div>
<!-- /wp:html -->

<!-- wp:heading {{"level":2,"className":"aga-secao-titulo"}} -->
<h2 class="wp-block-heading aga-secao-titulo" id="jogos">🎮 Jogos de Browser</h2>
<!-- /wp:heading -->

<!-- wp:paragraph {{"className":"aga-secao-sub"}} -->
<p class="aga-secao-sub">Escolhe o teu jogo e entra já:</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div class="aga-grade-jogos">{cards}</div>
<!-- /wp:html -->

<!-- wp:heading {{"level":2,"className":"aga-secao-titulo"}} -->
<h2 class="wp-block-heading aga-secao-titulo">🖥️ Servidores Dedicados</h2>
<!-- /wp:heading -->

<!-- wp:paragraph {{"className":"aga-secao-sub"}} -->
<p class="aga-secao-sub">Servidores 24/7 para a comunidade — estado em tempo real:</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div class="aga-servidores">
  <a href="/servidores/" class="aga-servidor-card">
    <span class="aga-servidor-nome">⛏️ Minecraft</span>
    <span class="aga-servidor-meta">Survival · Purpur 1.21.4</span>
    <span class="aga-servidor-btn">Ver estado →</span>
  </a>
  <a href="/servidores/" class="aga-servidor-card">
    <span class="aga-servidor-nome">🌿 Terraria</span>
    <span class="aga-servidor-meta">Cooperativo · 1.4.4.9</span>
    <span class="aga-servidor-btn">Ver estado →</span>
  </a>
  <a href="/servidores/" class="aga-servidor-card">
    <span class="aga-servidor-nome">🧟 Project Zomboid</span>
    <span class="aga-servidor-meta">Hardcore · Build 42</span>
    <span class="aga-servidor-btn">Ver estado →</span>
  </a>
  <a href="/servidores/" class="aga-servidor-card">
    <span class="aga-servidor-nome">⛵ Valheim</span>
    <span class="aga-servidor-meta">Viking Survival · v0.219</span>
    <span class="aga-servidor-btn">Ver estado →</span>
  </a>
</div>
<!-- /wp:html -->

<!-- wp:html -->
<div class="aga-cta-fim">
  <h3>Pronto para jogar?</h3>
  <p>Entra no fórum, combina partidas e participa nos torneios.</p>
  <a href="/forum/" class="aga-btn-primary">💬 Ir para o Fórum</a>
  <a href="/eventos/" class="aga-btn-secondary">🏆 Ver Eventos</a>
</div>
<!-- /wp:html -->"""

with open("/tmp/_home_nova.html", "w", encoding="utf-8") as f:
    f.write(conteudo)
subprocess.run(["scp", "-q", "/tmp/_home_nova.html", "aga-web:/tmp/home-nova.html"], timeout=30)
out, err = wp("post", "update", "5", "/tmp/home-nova.html")
subprocess.run(["ssh", "aga-web", "rm -f /tmp/home-nova.html"], timeout=20)
print(out[:60], err[:60] if err else "")
print("done")
