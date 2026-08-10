#!/usr/bin/env python3
# Adiciona location /stats/ ao vhost do nginx (passa para o WordPress via PHP)
path = "/etc/nginx/sites-enabled/aga-stats"
with open(path, encoding="utf-8") as f:
    c = f.read()

velho = """    # Static site — default
    root /var/www/aga-static;"""

novo = """    # Stats pages — WordPress (AGA Stats Pages plugin)
    location ~ ^/stats/ {
        root /var/www/aga-wp;
        try_files $uri $uri/ /index.php?$args;
    }

    # Static site — default
    root /var/www/aga-static;"""

if velho in c:
    c = c.replace(velho, novo)
    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print("nginx: location /stats/ adicionado")
else:
    print("ERRO: bloco não encontrado")
