#!/usr/bin/env python3
"""Adiciona as 12 páginas de jogo ao menu Jogos (ID 18)."""
import subprocess

def wp(*args):
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp " + " ".join(args)
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=60)
    return r.stdout.strip(), r.stderr.strip()

paginas = {
    "FreeCiv": 39, "Xadrez": 40, "OGame": 41, "TravianZ": 42, "Suroi": 43,
    "Kaetram": 44, "Tosios": 45, "Supernova": 46, "AgeOfAI": 47,
    "Hypersomnia": 48, "Scribble": 49, "World of Craft": 50,
}

for nome, pid in paginas.items():
    out, err = wp("menu", "item", "add-post", "18", str(pid))
    print(f"  {nome}: {out[:40]} {err[:40] if err else ''}")
print("done")
