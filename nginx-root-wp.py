#!/usr/bin/env python3
# Configura o nginx: raiz = WordPress (aga-wp), /servidores = dashboard estático (aga-static)
path = "/etc/nginx/sites-enabled/aga-stats"
with open(path, encoding="utf-8") as f:
    c = f.read()

# 1. O bloco "Static site — default" passa a apontar para o WordPress como default
#    e /servidores serve o estático
velho = """    # Static site — default
    root /var/www/aga-static;
    location / {
        try_files $uri $uri/ /index.html;
    }
}"""

novo = """    # Dashboard de servidores (site estático antigo)
    location ^~ /servidores/ {
        root /var/www/aga-static;
        try_files $uri $uri/ /index.html;
    }
    location = /servidores {
        return 301 /servidores/;
    }

    # WordPress — default (portal gaming)
    root /var/www/aga-wp;
    location / {
        try_files $uri $uri/ /index.php?$args;
    }
}"""

if velho in c:
    c = c.replace(velho, novo)
    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print("nginx: raiz = WordPress, /servidores = estático")
else:
    print("ERRO: bloco estático não encontrado")
