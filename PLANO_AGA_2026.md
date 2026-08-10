# 🎮 AGA TVCABO ANGOLA — PLANO MASTER (2026-08-07)

> **Documento único para continuar em qualquer sessão futura.**
> Estado verificado ao vivo em 2026-08-07 ~18:00 WAT.
> Complementos: `ECOSSISTEMA_AGA.md` (topologia base) · `ESTADO_2026-08-07.md` (handoff anterior)

---

## 0. MISSÃO & REGRAS DO USER (não negociáveis)

**Objectivo: 10 jogos, todos 100% WEB (browser), 100% GRÁTIS, 100% OPEN SOURCE.**

- ❌ Sem clientes instaláveis (só browser)
- ❌ Sem jogos pagos (Terraria/Zomboid/Valheim foram removidos)
- ❌ Sem API de AI com custos (Wolfcha foi removido por isso)
- ❌ Sem Docker se possível (user prefere nativo — excepção: World of Claudecraft)
- ✅ Testar SEMPRE no browser real (não só curl)
- ✅ Idioma PT/PT-BR quando disponível
- ✅ Nome: **"AGA TVCABO ANGOLA"**
- ✅ Regra de ouro: auditar antes de prometer; nunca prometer suporte humano sem staff

**Decisões do user nesta sessão:**
- Remover Wolfcha (usa LLM/API) → substituir por **TravianZ + OGame**
- Remover SuperNova (a pedido)
- Manter só jogos web (foram desligadas VMs de jogos dedicados: Luanti, Veloren, Mindustry, etc.)

---

## 1. ESTADO ACTUAL — VERIFICADO (HTTP 200 em tudo abaixo)

### ✅ LIVE E ACESSÍVEIS PUBLICAMENTE (9)

| # | Jogo | URL | VM | IP | Porta | HTTP |
|---|------|-----|-----|-----|-------|------|
| 1 | 🏰 Age of AI | https://ageofai.aga.org.ao | 117 | .117 | 8080 | ✅ 200 |
| 2 | ⚔️ Kaetram | https://kaetram.aga.org.ao | 118 | .118 | 9001 | ✅ 200 |
| 3 | 🔫 Hypersomnia | https://hypersomnia.aga.org.ao | 119 | .119 | UDP 8412 + :80 | ✅ 200 |
| 4 | 🎯 Suroi | https://suroi.aga.org.ao | 120 | .120 | 3000 | ✅ 200 |
| 5 | ♟️ Lichess | https://lichess.aga.org.ao | 121 | .121 | 9663 (nginx:80) | ✅ 200 |
| 6 | 🏰 TravianZ | https://travianz.aga.org.ao | 122 | .122 | 80 | ✅ 200 |
| 7 | ✏️ Scribble.rs | https://scribble.aga.org.ao | 113 | .113 | 8080 | ✅ 200 |
| 8 | 🔫 TOSIOS | https://tosios.aga.org.ao | 115 | .115 | 3001 | ✅ 200 |
| 9 | 🛸 OGame | https://ogame.aga.org.ao | 116 | .116 | 80 | ✅ 200 (admin legor/aga2026admin) |

> **World of Claudecraft removido** (2026-08-07): containers Docker apagados, NPM proxy removido, DNS Cloudflare removido, card removido do site. VM .114 livre para uso futuro.

---

## 2. INFRA — VMs (Proxmox @ pve 192.168.1.254)

| VM | Nome (hostname) | IP | RAM | Jogo actual | Estado |
|----|-----------------|-----|-----|-------------|--------|
| 112 | KLB-PRD-AGA-WEB-001 | .112 | 2 GB | Site WP + stats | ✅ running |
| 113 | KLB-PRD-AGA-SCRIBBLE-001 | .113 | 3 GB | **Scribble.rs** | ✅ running |
| 114 | KLB-PRD-AGA-WOC-001 | .114 | 6 GB | **World of Claudecraft** | 🔄 building |
| 115 | KLB-PRD-AGA-TOSIOS-001 | .115 | 2 GB | **TOSIOS** | ✅ running |
| 116 | KLB-PRD-AGA-OGAME-001 | .116 | 3 GB | **OGame** 🆕 | ✅ running |
| 117 | KLB-PRD-AGA-AGEOFAI-001 | .117 | 1 GB | Age of AI | ✅ running |
| 118 | KLB-PRD-AGA-KAETRAM-001 | .118 | 3 GB | Kaetram | ✅ running |
| 119 | KLB-PRD-AGA-HYPERSOMNIA-001 | .119 | 2 GB | Hypersomnia | ✅ running |
| 120 | KLB-PRD-AGA-SUROI-001 | .120 | 3 GB | Suroi | ✅ running |
| 121 | KLB-PRD-AGA-LICHESS-001 | .121 | 4 GB | Lichess | ✅ running |
| 122 | KLB-PRD-AGA-TRAVIANZ-001 | .122 | 2 GB | **TravianZ** | ✅ running |

**Nota:** hostnames renomeados em /etc/hostname (113=SCRIBBLE, 114=WOC, 115=TOSIOS, 116=OGAME, 122=TRAVIANZ). Restantes (117-121) mantiveram nomes originais.

### SSH aliases (`/root/.ssh/config`)
```
aga-ageofai(.117)  aga-kaetram(.118)  aga-hypersomnia(.119)
aga-suroi(.120)    aga-lichess(.121)  aga-mc(.113=scribble)
aga-terraria(.115=TOSIOS)  aga-mindustry(.122=TravianZ)
aga-woc(.114)      aga-valheim(.116)
```
- Chave SSH correcta: `ssh-ed25519 ...KNudMmw3 agente`
- ProxyJump: `lab` (bastion 41.63.169.132:22104 → 192.168.1.104)

---

## 3. INFRA — NPM (reverse proxy @ rp = VM 102)

- **Proxies existentes**: ageofai, kaetram, hypersomnia, suroi, lichess, travianz
- **FALTAM**: scribble.aga.org.ao → .113:8080 · tosios.aga.org.ao → .115:3001 · (claudecraft quando pronto)
- ⚠️ **CRÍTICO**: NPM **NÃO regenera** configs do SQLite! Para adicionar proxy:
  1. Criar ficheiro `/data/nginx/proxy_host/<nome>.conf` no container `toor-app-1` (formato: server blocks com listen 80/443, ssl_certificate /data/custom_ssl/npm-99/..., include conf.d/include/proxy.conf)
  2. `docker exec toor-app-1 nginx -t && nginx -s reload`
  - Modelo pronto: `/tmp/npm-travianz.conf` no VPS (usar como template)

### SSL (Let's Encrypt)
- Cert SAN **6 domínios**: ageofai, kaetram, hypersomnia, suroi, lichess, travianz (.aga.org.ao)
- Local: `/etc/letsencrypt/live/ageofai.aga.org.ao/` no host rp
- Copiado para NPM: `/home/toor/data/custom_ssl/npm-99/`
- **Renovar/emitir** = certbot DNS-01 com plugin cloudflare:
  ```bash
  # no rp: precisa do ficheiro /etc/letsencrypt/cloudflare.ini com dns_cloudflare_api_token
  certbot certonly --dns-cloudflare --dns-cloudflare-credentials /etc/letsencrypt/cloudflare.ini \
    -d domínio1.aga.org.ao ... --non-interactive --agree-tos --register-unsafely-without-email
  # depois copiar fullchain.pem + privkey.pem para /home/toor/data/custom_ssl/npm-99/ + docker cp + reload
  ```
- Script pronto: `/tmp/dns-cert2.sh` (inclui copiar creds) — recrear se /tmp limpo

### DNS Cloudflare (zone `80f180a676804f98740964ec9a75779c`)
- API token: `cfut_...` em `/root/workspace/AGA/CREDENCIAIS.md`
- Registos A **proxied:false** → 41.63.169.132: ageofai, kaetram, hypersomnia, suroi, lichess, travianz
- **FALTAM**: scribble, tosios (+ claudecraft)

---

## 4. CREDENCIAIS

| Sistema | User | Senha | URL/Notas |
|---------|------|-------|-----------|
| TravianZ admin | admin | aga2026admin | travianz.aga.org.ao (email azer.kissoa@gmail.com) |
| TravianZ sistema | Multihunter/Support | aga2026 | contas de moderação |
| TravianZ MySQL | travianz | travianz2026 | db: travianz, host localhost |
| OGame MySQL | ogame | ogame2026 | db: ogame, host localhost |
| OGame admin (legor) | legor | aga2026admin | ogame.aga.org.ao, universo 1 |
| Cloudflare API | cfut_... | — | zone 80f180a676804f98740964ec9a75779c |
| SSH VMs | toor | chave agente | sudo NOPASSWD |

---

## 5. PENDENTES — PRÓXIMA SESSÃO (ordem recomendada)

### 🔥 1. World of Claudecraft — aguardar `docker compose up -d --build` (VM 114)
- Estado: 🔄 build em background (`proc_59486f9a2fbf`). Repo clonado (2.7GB, --depth 1). Docker 26.1.5 + docker-compose 2.26.1 instalados. 
- .env criado com POSTGRES_PASSWORD aleatório.
- Verificar: `ssh aga-woc 'sudo docker ps'` e `curl -s https://claudecraft.aga.org.ao/`
- Se build falhar: verificar logs, considerar build nativo (sem Docker) com PostgreSQL + pnpm

### ✅ 2. OGame — INSTALADO (VM 116)
- Wizard completo: Master DB + Universo 1. Admin legor/aga2026admin funcional.
- Wizard pode ser reexecutado se necessário em /game/install.php (password: aga2026admin)

### ✅ 3. Scribble.rs + TOSIOS — EXPOSTOS PUBLICAMENTE
- Proxies NPM: scribble.conf (→ .113:8080), tosios.conf (→ .115:3001) + DNS A + cert SAN (9 domínios).
- HTTPS 200 verificado para ambos.

### ✅ 4. Site AGA (aga.org.ao)
- Página estática reescrita: "AGA TVCABO ANGOLA — Jogos de Browser", 10 cards (9 "Jogar Agora" + WoC "Em Breve"), links Discord/WhatsApp/Telegram.
- Ficheiro: `/var/www/aga-static/index.html` na VM 112 (servido via nginx → NPM).

### 5. Idioma PT (verificação)
- ✅ Age of AI, Kaetram, Suroi (PT-BR 86%), WoC (PT-BR 22 locales)
- ❌ TravianZ, Scribble.rs, TOSIOS, OGame — sem PT
- ⚠️ Hypersomnia (cliente web remoto), Lichess (híbrido CDN com UI quebrada)

### 6. Limpezas / Ops
- Hostnames: ✅ renomeados (113=SCRIBBLE, 114=WOC, 115=TOSIOS, 116=OGAME, 122=TRAVIANZ)
- Stats API: ❌ ainda aponta para jogos antigos (MC/Terraria/Zomboid/Valheim) — precisa reconfigurar
- Backups PBS: ❌ VMs AGA (112-122) continuam sem backup
- agamap.md (skill): ✅ atualizado com hostnames e novos proxies
- Cert SAN: 9 domínios; após WoC LIVE, reemitir com 10 (adicionar claudecraft.aga.org.ao)

---

## 6. COMANDOS ÚTEIS POR JOGO

| Jogo | Start/Status | Porta | Notas |
|------|-------------|-------|-------|
| Age of AI | `systemctl status aga-ageofai` | 8080 | Node, repo /opt/age-of-ai |
| Kaetram | `systemctl status aga-kaetram` | 9001 | yarn start, /opt/kaetram, HOST=0.0.0.0 no .env |
| Hypersomnia | `systemctl status aga-hypersomnia` | UDP 8412 + nginx:80 | AppImage + landing page |
| Suroi | `systemctl status aga-suroi` | 3000 | bun start + nginx serve dist |
| Lichess | `systemctl status aga-lichess` | 9663 (nginx:80) | lila stage; assets CDN lichess.org (híbrido) |
| TravianZ | apache2 | 80 | PHP/MySQL; /var/www/html; admin/aga2026admin |
| Scribble.rs | `systemctl status aga-scribble` | 8080 | /opt/scribblers/scribblers --port 8080 --host 0.0.0.0 |
| TOSIOS | `systemctl status aga-tosios` | 3001 | node packages/server/dist/index.js; build=npm run build |
| WoC | docker compose | 8787 | /opt/world-of-claudecraft (a reinstalar) |
| OGame | apache2 | 80 | /var/www/html (a instalar) |

---

## 7. LIÇÕES APRENDIDAS (evitar repetir)

1. **NPM não regenera configs do SQLite** → criar .conf manualmente em /data/nginx/proxy_host/ e reload
2. **certbot standalone falha** (porta 80 ocupada) → usar **DNS-01** com plugin dns-cloudflare
3. **Chave SSH correcta** = `...CQFSyYK3XSY8KNudMmw3 agente` (a outra que usava antes estava errada)
4. **VM 122 SSH** resolveu reescrevendo authorized_keys com a chave certa via PVE agent
5. **TravianZ** instalado via wizard web em /install (6 passos); SQL em var/db/struct.sql + datagen-world-data.sql; REMOVER /install após instalação + chmod 755 GameEngine, 777 Prevention/Notes/var/log
6. **Scribble.rs** binary 14MB; cuidado com "Text file busy" ao substituir binário em uso → parar serviço primeiro
7. **TOSIOS** porta 3001 (não 3000); start via node dist, não npm start
8. **Kaetram** hub precisa HOST=0.0.0.0 no .env para expor cliente web; nginx serve client static + proxy API
9. **Lichess híbrido**: net.asset.domain=lichess.org no local.conf → assets do CDN oficial, lógica local (funciona mas não 100% self-hosted)
10. **World of Claudecraft**: exigente (Docker+Postgres+pnpm) — dar VM com 6GB e tempo; background pode falhar silenciosamente

---

## 8. SESSÃO ANTERIOR — RESUMO FEITO (contexto)

- Criadas 5 VMs web (117-121) como linked clones da VM 200 (template Debian)
- Instalados e LIVE: Age of AI, Kaetram, Hypersomnia, Suroi, Lichess
- SSL Let's Encrypt + NPM proxies + DNS Cloudflare directo (proxied:false)
- Hoje: Scribble.rs (.113), TOSIOS (.115), TravianZ (.122) instalados e LIVE
- Removidos/desligados: Minecraft, Terraria, Zomboid, Valheim, Luanti, Veloren, Mindustry (jogos pagos ou dedicados)
- Removidos da lista: Wolfcha (AI paga), SuperNova (pedido user)
