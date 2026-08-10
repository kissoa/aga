#!/usr/bin/env python3
"""Cria o menu Jogos com os 12 jogos + adiciona ao menu Principal."""
import subprocess

def wp(*args):
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp " + " ".join(args)
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=60)
    return r.stdout.strip(), r.stderr.strip()

# IDs das páginas de jogo (criadas antes)
paginas = {
    "civ": 39, "xadrez": 40, "ogame": 41, "travianz": 42, "suroi": 43,
    "kaetram": 44, "tosios": 45, "supernova": 46, "ageofai": 47,
    "hypersomnia": 48, "scribble": 49, "woc": 50,
}
nomes = {
    "civ": "FreeCiv", "xadrez": "Xadrez", "ogame": "OGame", "travianz": "TravianZ",
    "suroi": "Suroi", "kaetram": "Kaetram", "tosios": "Tosios", "supernova": "Supernova",
    "ageofai": "AgeOfAI", "hypersomnia": "Hypersomnia", "scribble": "Scribble", "woc": "World of Craft",
}

# 1. criar menu Jogos
out, err = wp("menu", "create", '"Jogos"')
print("menu Jogos:", out, err[:40])

# 2. obter o term_id do menu Jogos
out, _ = wp("menu", "list", "--fields=term_id,name", "--format=csv")
menu_jogos = None
for linha in out.split("\n"):
    if "Jogos" in linha:
        menu_jogos = linha.split(",")[0]
print("menu Jogos ID:", menu_jogos)

# 3. adicionar as 12 páginas ao menu Jogos
if menu_jogos:
    for slug, pid in paginas.items():
        out, err = wp("menu", "item", "add", f"{menu_jogos}", f"post_type_page_{pid}")
        print(f"  {nomes[slug]}: {out[:30]} {err[:30] if err else ''}")

print("---")
print("done")
