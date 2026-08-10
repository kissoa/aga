#!/usr/bin/env python3
"""Corrige o link de discussão nas 12 páginas de jogo (aponta para o fórum específico)."""
import subprocess

def wp(*args):
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp " + " ".join(args)
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=60)
    return r.stdout.strip(), r.stderr.strip()

# slug da página -> slug do fórum
forums = {
    "civ": "freeciv", "xadrez": "xadrez", "ogame": "ogame", "travianz": "travianz",
    "suroi": "suroi", "kaetram": "kaetram", "tosios": "tosios", "supernova": "supernova",
    "ageofai": "ageofai", "hypersomnia": "hypersomnia", "scribble": "scribble", "woc": "world-of-craft",
}

for slug, fslug in forums.items():
    # obter o post_id da página
    out, _ = wp("post", "list", "--post_type=page", f"--name={slug}", "--field=ID", "--format=csv")
    pid = out.strip()
    if not pid:
        print(f"  {slug}: página não encontrada")
        continue
    # obter o conteúdo e substituir o link
    out, _ = wp("post", "get", pid, "--field=post_content")
    conteudo = out
    velho = '<a href="/forum">fórum do jogo</a>'
    novo = f'<a href="/forums/forum/{fslug}/">fórum do jogo</a>'
    if velho in conteudo:
        conteudo = conteudo.replace(velho, novo)
        # escrever num ficheiro e atualizar
        with open("/tmp/_page_tmp.html", "w", encoding="utf-8") as f:
            f.write(conteudo)
        subprocess.run(["scp", "-q", "/tmp/_page_tmp.html", f"aga-web:/tmp/page-{pid}.html"], timeout=30)
        wp("post", "update", pid, f"/tmp/page-{pid}.html")
        subprocess.run(["ssh", "aga-web", f"rm -f /tmp/page-{pid}.html"], timeout=20)
        print(f"  {slug} (página {pid}): link -> /forums/forum/{fslug}/")
    else:
        print(f"  {slug}: link não encontrado (verificar)")

print("done")
