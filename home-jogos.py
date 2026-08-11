#!/usr/bin/env python3
"""Adiciona à página Início (5) uma secção com os 12 jogos em destaque."""
import subprocess

def wp(*args):
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp " + " ".join(args)
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=60)
    return r.stdout.strip(), r.stderr.strip()

# obter conteúdo atual da página Início
out, _ = wp("post", "get", "5", "--field=post_content")
conteudo = out

# secção de jogos (cards com emoji + nome + descrição curta)
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
    f'<div style="background:#12121f;border:1px solid #1e1e3a;border-radius:12px;padding:1rem;text-align:center;">'
    f'<div style="font-size:2rem">{emoji}</div>'
    f'<div style="font-weight:700;color:#fff;margin:.4rem 0">{nome}</div>'
    f'<div style="font-size:.8rem;color:#6a6a9a">{desc}</div>'
    f'<a href="{url}" style="display:inline-block;margin-top:.6rem;background:#f0a500;color:#0a0a10;padding:.3rem 1rem;border-radius:6px;text-decoration:none;font-weight:700;font-size:.85rem;">Jogar</a>'
    f'</div>'
    for emoji, nome, url, desc in jogos
)

secao = f"""<!-- wp:heading {{"level":2}} -->
<h2 class="wp-block-heading" style="text-align:center">🎮 Jogos de Browser — 100% Grátis</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p style="text-align:center;color:#6a6a9a">12 jogos 100% GRÁTIS, 100% WEB, 100% OPEN SOURCE. Escolhe o teu e joga agora!</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1rem;margin:1.5rem 0">
{cards}
</div>
<!-- /wp:html -->
"""

# inserir a secção antes do separador de Redes Sociais (ou no fim do hero)
# vamos inserir logo a seguir ao hero (após o "VER SERVIDORES ONLINE" / botões)
marca = '<!-- wp:separator -->'
if marca in conteudo:
    conteudo = conteudo.replace(marca, secao + "\n" + marca, 1)
else:
    conteudo = conteudo + "\n" + secao

# atualizar
with open("/tmp/_home_tmp.html", "w", encoding="utf-8") as f:
    f.write(conteudo)
subprocess.run(["scp", "-q", "/tmp/_home_tmp.html", "aga-web:/tmp/home.html"], timeout=30)
out, err = wp("post", "update", "5", "/tmp/home.html")
subprocess.run(["ssh", "aga-web", "rm -f /tmp/home.html"], timeout=20)
print(out[:60], err[:60] if err else "")
print("done")
