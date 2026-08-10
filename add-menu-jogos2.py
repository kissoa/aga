#!/usr/bin/env python3
"""Adiciona o menu Jogos (18) como item (com submenu) no menu Principal (5)."""
import subprocess

def wp(*args):
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp " + " ".join(args)
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=60)
    return r.stdout.strip(), r.stderr.strip()

# adicionar um item "Jogos" (custom link para # ou página) ao menu Principal
# para o submenu funcionar, o item pai precisa de ser um item com children.
# O wp-cli não cria submenus diretamente; o melhor: adicionar o item como custom
# e depois usar o wp post para setar o parent... na verdade, o padrão é:
# adicionar todas as páginas ao MESMO menu e organizar por parent.

# Abordagem mais simples: adicionar o menu Jogos como item do menu Principal via custom
out, err = wp("menu", "item", "add-custom", "5", '"Jogos"', "#")
print("item Jogos:", out[:40], err[:40] if err else '')

# ver o db_id do item criado
out, _ = wp("menu", "item", "list", "5", "--fields=db_id,title,type,object")
print(out)
