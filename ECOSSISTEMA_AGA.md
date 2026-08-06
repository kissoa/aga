# AGA — Angolan Gamers Association
## Documentário Técnico do Ecossistema (Exploração 2026-08-06)

> **Objetivo deste documento:** servir de contexto permanente para sessões futuras.
> Descreve o que é a AGA, a infraestrutura, cada servidor, o estado atual,
> os problemas encontrados e o que falta fazer. Explorado ao vivo via SSH
> em 2026-08-06 (manhã, fuso WAT/+1).

---

## 1. O que é a AGA

**AGA = Angolan Gamers Association (Associação de Gamers de Angola).**

- Operação de **servidores de jogos dedicados 24/7** para a comunidade gamer angolana.
- Filosofia: **"nosteam friendly — todos bem-vindos"** (os servidores Zomboid funcionam sem Steam).
- Domínio: `aga.org.ao` (DNS gerido no **Cloudflare**; NS: `betty/tosana.ns.cloudflare.com`).
- Subdomínios públicos:
  - `mc.aga.org.ao` → Minecraft
  - `terraria.aga.org.ao` → Terraria
  - `zomboid.aga.org.ao` → Project Zomboid
  - `valheim.aga.org.ao` → Valheim
  - `stats.aga.org.ao` → dashboard de monitorização (aponta para Cloudflare, mas **não está a servir nada real** — página "Default Site")
- Hosting: **homelab próprio** (rede `192.168.1.0/24`), IP público `41.63.169.132`.
- Contacto/email nos certificados: `azer.kissoa@gmail.com`.

---

## 2. Topologia da infraestrutura

```
Internet (41.63.169.132)
   │
   ├── fw  (KLB-PRD-FW-001, 192.168.1.1)   FreeBSD 14.3 + OPNsense + pf + crowdsec/fail2ban
   │      (NAT/port-forward para rp, bastion, mail e jogos — ver §8)
   │
   ├── lab (bastion SSH, 41.63.169.132:22104 → 192.168.1.104:22)  <-- entrada de admin
   │
   ├── pve (192.168.1.254)  Proxmox VE — hypervisor
   │      └── VMs:
   │          112 KLB-PRD-AGA-WEB-001      (aga-web)     DEBIAN 13  — Stats API + nginx + Postgres
   │          113 KLB-PRD-AGA-MINECRAFT-001 (aga-mc)     DEBIAN 13  — Minecraft Purpur 1.21.4
   │          114 KLB-PRD-AGA-ZOMBOID-001   (aga-zmb)    DEBIAN 13  — Project Zomboid Build 42  ⚠ OFFLINE
   │          115 KLB-PRD-AGA-TERRARIA-001  (aga-terr)   DEBIAN 13  — Terraria 1.4.4.9
   │          116 KLB-PRD-AGA-VALHEIM-001   (aga-val)    DEBIAN 13  — Valheim (online, mal monitorizado)
   │          (110 KLB-AGA-001 — APAGADA; era o "aga" principal / web antiga — ver §7)
   │
   ├── rp  (192.168.1.102)  Nginx Proxy Manager (Docker) — reverse proxy 80/81/443
   ├── pkm (192.168.1.111)  running (não AGA, mas no NPM)
   ├── mail(192.168.1.103)  STOPPED (regras pf apontam para ela — dead)
   └── pbs (192.168.1.253)  Proxmox Backup Server (backups: SÓ 101/102/104!)
```

**Acesso SSH (a partir do workspace):** todas as VMs via `ProxyJump lab` (`41.63.169.132:22104`, user `toor`).
Hosts no `~/.ssh/config`: `aga-web`, `aga-mc`, `aga-zmb`, `aga-terraria`, `aga-valheim`, `pve`, `fw`, `rp`, `pbs`, `lab`.

---

## 3. aga-web (112) — o hub do ecossistema

**VMID 112 · KLB-PRD-AGA-WEB-001 · Debian 13 (trixie) · 1 GB RAM · 30 GB disco (9% usado)**

Serviços ativos:
| Serviço | Descrição |
|---|---|
| `aga-stats-api.service` | **AGA Stats API v2** — monitorização dos 4 game servers (Python, porta 3500) |
| `nginx` | reverse proxy para `stats.aga.org.ao` → `127.0.0.1:3500/api/dashboard` |
| `postgresql@17-main` | PostgreSQL 17 (instalado; **não é usado** pela Stats API v2 — o histórico vai para SQLite) |
| `fail2ban` | proteção SSH |
| `qemu-guest-agent` | integração Proxmox |

### Stats API v2 — `/opt/aga_stats_api.py`
- Processo: `python3 /opt/aga_stats_api.py`, User `toor`, Restart=always, log em `/var/log/aga-stats-api.log`.
- **SERVERS monitorizados** (hardcoded no código):
  - `mc`: `192.168.1.113:25565` (RCON 25575, pass `agamc2026`) — usa `mcstatus` + `mcrcon`
  - `terraria`: `192.168.1.115:7777` (só teste TCP)
  - `zomboid`: `192.168.1.114:16261` (só teste UDP, **sem** RCON apesar de config ter rcon_pass)
  - `valheim`: `192.168.1.116:2456` (teste **TCP** 2456/2457/2458 — ⚠ **bug: Valheim é UDP**, daí aparecer offline)
- Ciclo de monitorização: **a cada 30 s** → grava em SQLite `/opt/aga-stats/history.db` (tabela `server_history`).
- Endpoints HTTP:
  - `GET /api/health` → `{"status":"ok"}`
  - `GET /api/servers` → estado atual de todos (JSON, usado pelo frontend)
  - `GET /api/server/<sid>` → estado + histórico 24h + pico/uptime/média
  - `GET /api/dashboard` → HTML dashboard embutido (com tabs por servidor)
  - qualquer outro path → serve `/var/www/html/index.html` (fallback)
- Dashboard HTML embutido: tema escuro, bandeira angolana (vermelho/dourado), tabs Overview/Minecraft/Terraria/Zomboid/Valheim, refresh 10 s, gráfico de barras de jogadores.

### Frontend público — `/var/www/html/index.html`
- **Mais bonito que o dashboard embutido**: tema escuro, fontes Inter + Orbitron, cards por jogo com estado online/offline, botão copiar endereço, contadores totais.
- ⚠ **Desatualizado em relação à API v2**: o JS chama `/api/mc-status` e `/api/terraria-status`, que **não existem** na API v2 (a v2 expõe `/api/servers`). Resultado: o frontend mostra Zomboid e Valheim como "Instalando" e MC/Terraria dependem de endpoints mortos.
- Subdomínios mostrados: `mc.aga.org.ao`, `terraria.aga.org.ao`, `zomboid.aga.org.ao`, `valheim.aga.org.ao`.
- Slots anunciados: MC 30, Terraria 16, Zomboid 32, Valheim 10 (valores do frontend ≠ valores da API: MC 20, Zomboid 8 — **inconsistência**).

### nginx — `/etc/nginx/sites-enabled/aga-stats`
```nginx
server_name stats.aga.org.ao;
location /     { proxy_pass http://127.0.0.1:3500/api/dashboard; ... }  # websocket upgrade
location /api/ { proxy_pass http://127.0.0.1:3500; ... }
```

### Histórico registado (SQLite, 14 492 leituras por servidor, ~30 s)
| Servidor | Última leitura | Uptime global | Estado agora |
|---|---|---|---|
| mc | 06/08 05:45 | **100,0%** | ONLINE — Purpur 1.21.4, TPS 20.0, latência 1.3 ms |
| terraria | 06/08 05:45 | **100,0%** | ONLINE — v1.4.49 |
| zomboid | 06/08 05:45 | **0,0%** (desde 30/07) | OFFLINE |
| valheim | 06/08 05:45 | **0,0%** (desde 30/07) | ONLINE de facto, marcado offline (bug TCP/UDP) |

⚠ **Aviso de segurança nos logs da API:** houve tentativas de *path traversal* contra a API
(`/api/dashboard.env`, `/api/secrets.yml`, `/api/.git/config`, `credentials.json`, `terraform.tfstate`, …),
todas devolvidas 200 pelo fallback. O fallback "serve index.html para qualquer path" é um
comportamento de enumeração — a API não expõe segredos, mas convém restringir.

---

## 4. aga-mc (113) — Minecraft

**VMID 113 · KLB-PRD-AGA-MINECRAFT-001 · Debian 13 · 3 GB RAM · 30 GB (7%)**

- **Servidor:** Purpur 1.21.4 (fork de Paper) — `java -Xms1G -Xmx2G -G1GC -jar purpur.jar --nogui`
- **Serviço:** `aga-minecraft.service` (enabled, active desde 03/08, ~1.6 GB RAM)
- **Portas:** 25565 (jogo) · 25575 (RCON, pass `agamc2026`)
- **Config relevante** (`server.properties`):
  - `gamemode=survival`, `difficulty=hard`, `allow-flight=true`
  - `enable-rcon=true`, `enforce-whitelist=false` (whitelist vazia)
  - `entity-activation-range=32`, `generate-structures=true`, Nether + End ativos
- **Plugins:** `bStats`, `spark` (profiler/performance) — sem plugins de jogo (sem Essentials/Geyser apesar do frontend prometer `/tpa /home /kit /warp` e "Java + Bedrock")
- **Mundos:** `world`, `world_nether`, `world_the_end` — level.dat de ~1,5 KB (mundo **muito jovem/recém-criado**, 03/08)
- **Jogadores:** `usercache.json` vazio → **ninguém entrou ainda**; `whitelist.json`/`ops.json` vazios
- **Estado:** ONLINE, 0 jogadores, TPS 20, uptime 100%.

---

## 5. aga-terraria (115) — Terraria

**VMID 115 · KLB-PRD-AGA-TERRARIA-001 · Debian 13 · 1 GB RAM · 30 GB (6%)**

- **Servidor:** Terraria 1.4.4.9 (build 1449, `TerrariaServer.bin.x86_64`) — `-config /opt/terraria/serverconfig.txt`
- **Serviço:** `aga-terraria.service` (active desde 02/08; ~700 MB RAM)
- **Porta:** 7777 (TCP)
- **Config** (`/opt/terraria/serverconfig.txt`):
  - Mundo: `/opt/terraria/worlds/AGA_Terraria.wld`, `autocreate=3` (grande), `worldname=AGA_Terraria`
  - `difficulty=1` (Expert), `maxplayers=16`, **sem password**, `secure=0`
  - MOTD: *"AGA Terraria — Associação de Gamers de Angola"*
- **Estado:** ONLINE, 0 jogadores; **CPU a 99,8%** desde o arranque (~4 dias de CPU = 4d3h37m!) — o processo usa 100% de um core continuamente; load ~1.9. (Possível busy-loop do servidor mono/.NET em idle — vale investigar.)
- Logs mostram conexões de `192.168.1.112` (a Stats API) a cada ~40 s — normal.

---

## 6. aga-zmb (114) — Project Zomboid ⚠ OFFLINE (crash)

**VMID 114 · KLB-PRD-AGA-ZOMBOID-001 · Debian 13 · 2 GB RAM · 30 GB (34% — o mais usado)**

- **Servidor:** Project Zomboid Build 42 (`ProjectZomboid64`, `-nosteam -servername AGA_Zomboid -adminpassword agazomboid2026 -MaxPlayers 8`)
- **Serviço:** `aga-zomboid.service` — systemd diz "active (running)" mas **o jogo está morto desde 02/08 03:03**.
- **Causa raiz (confirmada nos logs):**
  - `java.lang.OutOfMemoryError: Java heap space` durante `LOADING ASSETS: START` (animação `Turkey_Poult`).
  - Config JVM `/opt/zomboid/ProjectZomboid64.json`: **`-Xmx512m -Xms384m` — heap ridiculamente baixo** para o Build 42 (que precisa de 2–4 GB).
  - 4 ficheiros `hs_err_pid*.log` (30/07) = crashes JVM repetidos antes do arranque atual.
- **Sintoma atual:** processo 726 vivo (772 MB RSS, 20 threads, `futex_wait`) mas **sem portas UDP/TCP abertas** (16261/27015 não escutam), log `server-console.txt` parado desde 02/08 03:03.
- **Mundo/saves:** `/home/toor/Zomboid/` (server-console, backups, Logs, Crafting). Já existiu pelo menos 1 arranque OK a 30/07 08:14 (UPnP not found → port-forward manual necessário).
- **Fix provável:** parar o serviço, subir `-Xmx` (ex.: `-Xmx3g -Xms1g`) no `ProjectZomboid64.json`, reiniciar, e adicionar regras pf (ver §8). Com 2 GB de RAM na VM, heap 3g não cabe — **a VM precisa de mais RAM** (Proxmox) ou heap ~1.5g + ajustar `MaxPlayers`.

---

## 7. aga-valheim (116) — Valheim

**VMID 116 · KLB-PRD-AGA-VALHEIM-001 · Debian 13 · 2 GB RAM · 30 GB (12%)**

- **Servidor:** `valheim_server.x86_64` — `-name 'AGA Valheim' -world AGA_Valheim -port 2456 -password agavalheim2026 -public 0`
- **Serviço:** `aga-valheim.service` (active desde 03/08; ~1.2 GB RAM)
- **Portas:** **UDP 2456 e 2457 abertas** (o Valheim é UDP!) + TCP 127.0.0.1:40695 (local).
- **Estado real: ONLINE e saudável** — log `/var/log/aga-valheim.log` mostra saves automáticos a cada 10 min, 81 ZDOs, backups auto a cada 2 h, sem erros.
- **Porque aparece OFFLINE na Stats API:** a API testa **TCP** nas portas 2456–2458; o Valheim só responde **UDP**. Bug de monitorização, não do servidor.
- **Mundos:** `/opt/valheim/worlds/worlds_local/` + listas `adminlist.txt`, `bannedlist.txt`, `permittedlist.txt`.
- `-public 0` = não aparece na lista pública do Steam (acesso direto por IP/domínio).

---

## 8. Rede pública, DNS e firewall ⚠ (problemas principais)

### DNS (Cloudflare)
| Domínio | Aponta para | Servido por |
|---|---|---|
| `mc/terraria/zomboid/valheim.aga.org.ao` | **41.63.169.132** (IP do lab) | direto (sem Cloudflare proxy) |
| `stats.aga.org.ao` | 104.21.69.179 / 172.67.211.3 (Cloudflare) | **página "Default Site"** — NPM/origin não configurado |
| `aga.org.ao` | Cloudflare | página "Default Site" |

### Reverse proxy (rp — 192.168.1.102, Nginx Proxy Manager em Docker)
Container `toor-app-1` (`jc21/nginx-proxy-manager`), portas 80/81/443.
Proxy hosts na BD do NPM (`/home/toor/data/database.sqlite`):
- `klb-prd-{rp,pve,pbs,fw,jmp}.lab.it.ao` → painéis internos (NPM, Proxmox 8006, PBS 8007, fw 443, jmp 9090)
- `klb-dev-wfl-001` → 192.168.1.105:5678 · `klb-dev-cms-001` → 192.168.1.107:80 · `klb-prd-pwm-001` → 192.168.1.108:8080 · `pkm.lab.it.ao` → 192.168.1.111:80
- `ai.lab.it.ao` → 192.168.1.109:8787 · `agent.lab.it.ao` → 192.168.1.109:3001 (WebUI/agente Hermes!)
- ⚠ `aga.org.ao` → **192.168.1.110:80** (host 17, ativo) e `condo.ao`/`www.condo.ao` → **192.168.1.110:3001** (hosts 18/19) — **todos apontam para a VM 110 que foi APAGADA** → dead.
- ❌ **Não existe proxy host para `stats.aga.org.ao`** — por isso o dashboard não aparece publicamente.

### Firewall (fw — 192.168.1.1, FreeBSD 14.3 OPNsense, pf + crowdsec + fail2ban)
Regras **rdr (NAT)** existentes para jogos:
- `25565 tcp → 192.168.1.113` (MC) ✅ rdr existe
- `7777  tcp → 192.168.1.115` (Terraria) ✅ rdr existe
- `16261 udp → 192.168.1.114` (Zomboid) ✅ rdr existe
- Valheim (2456/2457 UDP) ❌ **sem rdr, sem pass** — não exposto

⚠⚠ **MAS faltam as regras `pass in` correspondentes!** O pf só tem pass-in no WAN (vtnet0) para:
- `80/81/443 → 192.168.1.102` (NPM/rp)
- `22104 → 192.168.1.104:22` (bastion)
- `smtps/submission/imaps/pop3s → 192.168.1.103` (mail, que está STOPPED — dead)

**Testes externos confirmam:** TCP 25565/7777/16261 **fechadas** de fora; UDP 2456 sem resposta fiável; HTTP 41.63.169.132:80 responde 200 (página default do NPM). Ou seja: **os jogos estão inacessíveis da Internet apesar do DNS e do NAT**, porque o pf bloqueia (default drop) — só o reverse proxy e o bastion passam.

### Backups (PBS — 192.168.1.253)
- Job único (`/etc/pve/jobs.cfg`, 02:00 diário): **apenas VMs 101, 102, 104**.
- ❌ **As VMs AGA (112–116) NÃO têm backup.** O PBS tem espaço (401 GB livres) e guarda 101/102 religiosamente.
- Storage `local` do pve a 94% (38.5 GB) — limpeza recomendada; `local-lvm` a 0% (não usado); `pve-storage` a 45%.

---

## 9. VM 110 apagada (era o "aga")

- Não existe no `qm list` (apagada antes de 06/08).
- O `~/.ssh/config` tinha `Host aga → 192.168.1.110` — **removido na exploração de 06/08** (backup: `config.bak.20260806`).
- Ainda referenciada em: NPM (`aga.org.ao`, `condo.ao`), o que explica o site morto.
- O workspace `/root/workspace/condo/` existe mas está **vazio** — o projeto condo (app na 3001) vivia na VM 110 e perdeu-se com ela, salvo se houver backup no PBS (não está no job…).

---

## 10. Estado atual — resumo executivo (06/08/2026 06:40 WAT)

| Servidor | Processo | Portas | Jogável de fora? | Monitorização |
|---|---|---|---|---|
| Minecraft (113) | ✅ running | ✅ 25565 | ❌ pf bloqueia | ✅ online, 0 jog |
| Terraria (115) | ✅ running | ✅ 7777 | ❌ pf bloqueia | ✅ online (CPU 100% ⚠) |
| Zomboid (114) | ⚠ processo preso | ❌ nenhuma | ❌ | ❌ offline (OOM heap 512m) |
| Valheim (116) | ✅ running | ✅ UDP 2456/2457 | ❌ sem rdr/pass | ⚠ marcado offline (bug TCP) |
| Stats API (112) | ✅ running | ✅ 3500 (interno) | ❌ sem proxy host no NPM | — |
| Site `aga.org.ao` | ❌ origin morto | — | ❌ "Default Site" | — |

**Conclusão:** nenhum jogo é atualmente acessível a partir da Internet.
Os servidores correm, mas firewall (pass-in), reverse proxy (NPM), monitorização
(UDP vs TCP) e o crash do Zomboid bloqueiam o serviço público.

---

## 11. Problemas detetados (checklist para a próxima sessão)

1. **Zomboid offline por OOM** — heap 512 MB insuficiente; subir para ≥2 GB e dar mais RAM à VM 114 (2 GB → 4 GB) no Proxmox; parar/reiniciar o serviço.
2. **Valheim marcado offline** — corrigir `query_server()` na Stats API: testar UDP (socket SOCK_DGRAM) em vez de TCP.
3. **Portas de jogos bloqueadas no pf** — adicionar `pass in` no OPNsense para 25565→113, 7777→115, 16261→114, 2456/2457→116 (e rdr para valheim).
4. **`stats.aga.org.ao` e `aga.org.ao` mortos** — criar proxy host no NPM para `stats.aga.org.ao → 192.168.1.112:3500` (ou 80/nginx); limpar/redirecionar hosts apontando para 192.168.1.110 (aga.org.ao, condo.ao).
5. **Frontend `/var/www/html/index.html` desatualizado** — endpoints `/api/mc-status`/`/api/terraria-status` não existem; ligar à v2 (`/api/servers`) ou alinhar valores (slots MC 20 vs 30, Zomboid 8 vs 32).
6. **Backups: VMs AGA sem backup** — adicionar 112–116 ao job do PBS.
7. **Terraria CPU 100%** — investigar busy-loop (versão mono do servidor Terraria em idle consome 1 core?).
8. **Limpeza de referências mortas** — `mail` (103) STOPPED mas com rdr/pass; storage `local` do pve a 94%; proxy hosts NPM para a 110.
9. **Segurança** — RCON/admin passwords em texto claro em ficheiros e na API (agamc2026, agazomboid2026, agavalheim2026); fallback da API que devolve index.html para qualquer path (enumeração); considerar rate-limit/ACL no nginx para `/api/`.

---

## 12. Credenciais e segredos

> ⚠ As credenciais reais estão no ficheiro local `CREDENCIAIS.md` (não commitado — `.gitignore`).
> Abaixo apenas referências. Os valores estão hardcoded nos scripts da infraestrutura e devem ser rotacionados.

| Recurso | Localização do segredo |
|---|---|
| Cloudflare DNS API token (`aga.org.ao`) | `CREDENCIAIS.md` — testado 06/08/2026: válido e ativo |
| Cloudflare Zone ID | `80f180a676804f98740964ec9a75779c` (não é secreto) |
| MC RCON (113) | `CREDENCIAIS.md` |
| Zomboid admin (114) | `CREDENCIAIS.md` |
| Valheim password (116) | `CREDENCIAIS.md` |
| Stats API (112) | RCON pass MC/Zomboid hardcoded em `/opt/aga_stats_api.py` |
| OPNsense API Key | `CREDENCIAIS.md` |

### Registo DNS da zona aga.org.ao (via API, 06/08/2026 — 8 registos)

| Tipo | Nome | Conteúdo | Nota |
|---|---|---|---|
| A | `aga.org.ao` | 41.63.169.132 | proxied (Cloudflare) |
| A | `cs.aga.org.ao` | 41.63.169.132 | ⚠ servidor Counter-Strike? não documentado |
| A | `mc.aga.org.ao` | 41.63.169.132 | direto |
| A | `terraria.aga.org.ao` | 41.63.169.132 | direto |
| A | `valheim.aga.org.ao` | 41.63.169.132 | direto |
| A | `zomboid.aga.org.ao` | 41.63.169.132 | direto |
| CNAME | `*.aga.org.ao` | aga.org.ao | wildcard → raiz |
| CNAME | `www.aga.org.ao` | aga.org.ao | |

> Nota: `stats.aga.org.ao` **não tem registo próprio** — resolve via wildcard `*` → `aga.org.ao` (proxied). Para servir o dashboard é preciso registo A próprio ou configurar origin no Cloudflare/NPM.

---

## 13. Comandos úteis

```bash
# Acesso (ProxyJump lab configurado no ~/.ssh/config)
ssh aga-web    # Stats API + nginx + postgres (112)
ssh aga-mc     # Minecraft (113)
ssh aga-zmb    # Zomboid (114)
ssh aga-terraria  # Terraria (115)
ssh aga-valheim   # Valheim (116)
ssh pve        # Proxmox (192.168.1.254)
ssh fw         # firewall OPNsense (FreeBSD/csh — sem 2>/dev/null!)
ssh rp         # NPM docker (192.168.1.102)
ssh pbs        # backup server (192.168.1.253)

# Estado dos jogos
ssh aga-web 'curl -s http://127.0.0.1:3500/api/servers | python3 -m json.tool'
ssh aga-web 'python3 -c "import sqlite3;c=sqlite3.connect(\"/opt/aga-stats/history.db\");print(list(c.execute(\"SELECT server,SUM(online)*100.0/COUNT(*),MAX(datetime(ts,\\\"unixepoch\\\")) FROM server_history GROUP BY server\")))"'

# Logs
ssh aga-zmb 'tail -50 /home/toor/Zomboid/server-console.txt'          # crash OOM
ssh aga-valheim 'tail -30 /var/log/aga-valheim.log'                    # saves saudáveis
ssh aga-web 'tail -20 /var/log/aga-stats-api.log'                      # path traversal no log

# Firewall (OPNsense — shell csh; NÃO usar redirecionamento 2>/dev/null)
ssh fw 'pfctl -s nat'
ssh fw 'pfctl -s rules'
ssh fw 'pfctl -s Anchors'
```

---

*Documento gerado pela exploração ao vivo de 2026-08-06. Estado capturado às ~06:45 WAT.
Próxima sessão: começar pelo checklist da §11, ordem sugerida: 3 (rede) → 1 (Zomboid) → 2 (monitorização) → 4/5 (web) → 6 (backups).*
