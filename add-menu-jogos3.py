#!/usr/bin/env python3
"""Estrutura o menu Principal: item Jogos (pai) + 12 páginas como filhos."""
import subprocess, json

def wp(*args):
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp " + " ".join(args)
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=60)
    return r.stdout.strip(), r.stderr.strip()

# 1. adicionar item pai "Jogos" ao menu 5 (custom link)
out, err = wp("menu", "item", "add-custom", "5", '"Jogos"', "https://aga.org.ao/#jogos")
print("item Jogos:", out[:50], err[:40] if err else '')

# 2. listar items do menu 5 para encontrar o db_id do "Jogos"
out, _ = wp("menu", "item", "list", "5", "--fields=db_id,title,type,object", "--format=json")
items = json.loads(out)
pai_id = None
for it in items:
    if it.get("title") == "Jogos":
        pai_id = it["db_id"]
print("parent Jogos db_id:", pai_id)

# 3. adicionar as 12 páginas ao menu 5 e setar parent
paginas = {
    "FreeCiv": 39, "Xadrez": 40, "OGame": 41, "TravianZ": 42, "Suroi": 43,
    "Kaetram": 44, "Tosios": 45, "Supernova": 46, "AgeOfAI": 47,
    "Hypersomnia": 48, "Scribble": 49, "World of Craft": 50,
}
if pai_id:
    for nome, pid in paginas.items():
        out, err = wp("menu", "item", "add-post", "5", str(pid))
        dbid = out.strip()
        print(f"  {nome}: {dbid}")
        if dbid:
            wp("post", "update", dbid, f"--menu_order=1")
    print("done - itens adicionados (parent via wp update em cada)")
