#!/usr/bin/env python3
"""Estrutura o menu Principal (5): cria pai 'Jogos' + filhos via meta _menu_item_menu_item_parent."""
import subprocess, json

def wp(*args):
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp " + " ".join(args)
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=60)
    return r.stdout.strip(), r.stderr.strip()

def sql(q):
    return wp("db", "query", f'"{q}"')

# 1. o item pai "Jogos" já existe (adicionado antes)? verificar
out, _ = wp("menu", "item", "list", "5", "--fields=db_id,title,type,object", "--format=json")
items = json.loads(out)
pai_id = None
for it in items:
    if it.get("title") == "Jogos":
        pai_id = it["db_id"]
print("pai Jogos:", pai_id)

if not pai_id:
    out, _ = wp("menu", "item", "add-custom", "5", '"Jogos"', "https://aga.org.ao/#jogos")
    print("criado:", out)
    out, _ = wp("menu", "item", "list", "5", "--fields=db_id,title,type,object", "--format=json")
    items = json.loads(out)
    for it in items:
        if it.get("title") == "Jogos":
            pai_id = it["db_id"]
    print("pai agora:", pai_id)

# 2. adicionar as 12 páginas ao menu 5 (se ainda não estiverem)
paginas = {
    "FreeCiv": 39, "Xadrez": 40, "OGame": 41, "TravianZ": 42, "Suroi": 43,
    "Kaetram": 44, "Tosios": 45, "Supernova": 46, "AgeOfAI": 47,
    "Hypersomnia": 48, "Scribble": 49, "World of Craft": 50,
}
# ids já no menu (do menu Jogos 18 — mas vamos ao menu 5)
for nome, pid in paginas.items():
    out, err = wp("menu", "item", "add-post", "5", str(pid))
    print(f"  {nome}: {out.strip()}")

# 3. listar os novos items do menu 5 (páginas) e setar parent = pai_id
out, _ = wp("menu", "item", "list", "5", "--fields=db_id,title,type,object", "--format=json")
items = json.loads(out)
for it in items:
    t = it.get("title", "")
    if t in paginas:
        did = it["db_id"]
        sql(f"UPDATE wp_postmeta SET meta_value={pai_id} WHERE post_id={did} AND meta_key='_menu_item_menu_item_parent'")
        print(f"  parent set: {t} (item {did})")

print("done")
