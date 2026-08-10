#!/usr/bin/env python3
# Adiciona index index.php ao server block do nginx
path = "/etc/nginx/sites-enabled/aga-stats"
with open(path, encoding="utf-8") as f:
    c = f.read()

if "index index.php" not in c:
    velho = "    server_name aga.org.ao stats.aga.org.ao;"
    novo = "    server_name aga.org.ao stats.aga.org.ao;\n    index index.php index.html;"
    if velho in c:
        c = c.replace(velho, novo)
        with open(path, "w", encoding="utf-8") as f:
            f.write(c)
        print("index index.php adicionado")
    else:
        print("ERRO: server_name não encontrado")
else:
    print("já existe")
