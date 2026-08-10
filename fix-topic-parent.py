#!/usr/bin/env python3
"""Corrige post_parent dos 12 tópicos (bbPress lista tópicos pelo post_parent)."""
import subprocess

def wp(*args):
    cmd = "cd /var/www/aga-wp && sudo -u www-data wp " + " ".join(args)
    r = subprocess.run(["ssh", "aga-web", cmd], capture_output=True, text=True, timeout=60)
    return r.stdout.strip(), r.stderr.strip()

# topico -> forum
pares = {
    88: 51, 89: 52, 90: 53, 91: 54, 92: 55, 93: 56,
    94: 57, 95: 58, 96: 59, 97: 60, 98: 61, 99: 62,
}

for tid, fid in pares.items():
    out, err = wp("post", "update", str(tid), f"--post_parent={fid}")
    print(f"  tópico {tid} -> fórum {fid}: {out[:40]} {err[:40] if err else ''}")

# limpar cache do WP
wp("cache", "flush")
print("cache flushed")
print("done")
