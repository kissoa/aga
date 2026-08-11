<?php
/*
Plugin Name: AGA Gaming Theme CSS
Description: Tema escuro profissional com cores AGA para o portal gaming (Kadence).
Version: 2.0
Author: AGA
License: GPL-2.0
*/
/* Plugin: AGA Gaming CSS — tema escuro com cores AGA para o Kadence */
add_action('wp_enqueue_scripts', 'aga_gaming_css', 100);
function aga_gaming_css() {
    $css = '
    :root {
        --bg: #0a0a10; --surface: #12121f; --surface2: #171728; --border: #1e1e3a;
        --gold: #f0a500; --gold2: #ffc23d; --red: #ce1126; --green: #00e676;
        --text: #e0e0f0; --muted: #8a8ab0;
    }
    body { background: var(--bg) !important; color: var(--text) !important; }
    body::before {
        content:""; position: fixed; inset: 0; pointer-events: none; z-index: 0;
        background:
            radial-gradient(ellipse 700px 450px at 50% -10%, rgba(206,17,38,.10) 0%, transparent 70%),
            radial-gradient(ellipse 500px 600px at 90% 40%, rgba(240,165,0,.05) 0%, transparent 60%),
            radial-gradient(ellipse 400px 500px at 5% 80%, rgba(240,165,0,.04) 0%, transparent 60%);
    }
    .site-container, .site, #main, .content-area, .site-main { position: relative; z-index: 1; }
    .site-header, .site-footer { background: var(--surface) !important; border-color: var(--border) !important; }
    .site-header { border-bottom: 1px solid var(--border); }
    .site-branding .site-title a, .site-branding .site-title { color: #fff !important; font-weight: 800; font-size: 1.4rem; }
    .main-navigation .menu-item a, .primary-menu a, .header-navigation a { color: var(--text) !important; font-weight: 500; }
    .main-navigation .menu-item a:hover { color: var(--gold) !important; }
    .header-navigation .menu-item > a { padding: .5rem .85rem !important; border-radius: 8px; }
    .header-navigation .menu-item > a:hover { background: rgba(240,165,0,.12) !important; }
    .header-navigation .sub-menu { background: var(--surface2) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; padding: .4rem !important; }
    .header-navigation .sub-menu a { color: var(--text) !important; border-radius: 6px; }
    .header-navigation .sub-menu a:hover { background: rgba(240,165,0,.1) !important; color: var(--gold) !important; }
    .entry-title, .page-title, h1, h2, h3, h4, h5 { color: #fff !important; }
    .entry, .page, article { background: transparent !important; border: none !important; }
    .entry-content { color: var(--text); }
    .entry-content a:not(.aga-btn-primary):not(.aga-btn-secondary):not(.aga-jogo-card):not(.aga-servidor-card) { color: var(--gold); }
    .entry-content a:hover { color: var(--gold2); }

    /* ===== HERO ===== */
    .aga-hero { text-align: center; padding: 4rem 1rem 3rem; max-width: 900px; margin: 0 auto; }
    .aga-hero-badge { display: inline-block; background: linear-gradient(135deg, rgba(240,165,0,.15), rgba(206,17,38,.12)); border: 1px solid rgba(240,165,0,.3); color: var(--gold); padding: .35rem 1.1rem; border-radius: 30px; font-size: .72rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 1.4rem; }
    .aga-hero h1 { font-size: clamp(2.2rem, 5vw, 3.6rem); font-weight: 900; line-height: 1.1; margin: 0 0 1rem; }
    .aga-gold { color: var(--gold); }
    .aga-hero p { color: var(--muted); font-size: 1.1rem; max-width: 600px; margin: 0 auto 2rem; }
    .aga-hero-cta { display: flex; gap: .8rem; justify-content: center; flex-wrap: wrap; }

    /* ===== BOTÕES ===== */
    .aga-btn-primary, .aga-btn-secondary { display: inline-block; padding: .8rem 1.8rem; border-radius: 10px; font-weight: 700; font-size: .95rem; text-decoration: none !important; transition: .2s; }
    .aga-btn-primary { background: linear-gradient(135deg, var(--gold), #d98f00); color: #0a0a10 !important; }
    .aga-btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(240,165,0,.25); }
    .aga-btn-secondary { background: var(--surface2); color: var(--text) !important; border: 1px solid var(--border); }
    .aga-btn-secondary:hover { border-color: var(--gold); color: var(--gold) !important; }

    /* ===== SECÇÕES ===== */
    .aga-secao-titulo { text-align: center; font-size: 2rem; font-weight: 800; margin: 3.5rem 0 .3rem !important; }
    .aga-secao-sub { text-align: center; color: var(--muted); margin: 0 0 2rem !important; }

    /* ===== GRADE DE JOGOS ===== */
    .aga-grade-jogos { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; max-width: 1100px; margin: 0 auto; }
    .aga-jogo-card { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 1.4rem 1rem; text-align: center; text-decoration: none !important; transition: .2s; display: flex; flex-direction: column; align-items: center; gap: .3rem; }
    .aga-jogo-card:hover { transform: translateY(-4px); border-color: rgba(240,165,0,.5); box-shadow: 0 10px 30px rgba(240,165,0,.08); }
    .aga-jogo-emoji { font-size: 2.4rem; line-height: 1; }
    .aga-jogo-nome { color: #fff; font-weight: 700; font-size: 1.05rem; }
    .aga-jogo-desc { color: var(--muted); font-size: .8rem; }
    .aga-jogo-jogar { color: var(--gold); font-size: .85rem; font-weight: 700; margin-top: .5rem; }
    .aga-jogo-card:hover .aga-jogo-jogar { color: var(--gold2); }

    /* ===== SERVIDORES ===== */
    .aga-servidores { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 1rem; max-width: 1100px; margin: 0 auto; }
    .aga-servidor-card { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 1.2rem; text-decoration: none !important; transition: .2s; display: flex; flex-direction: column; gap: .3rem; }
    .aga-servidor-card:hover { transform: translateY(-2px); border-color: rgba(240,165,0,.4); }
    .aga-servidor-nome { color: #fff; font-weight: 700; font-size: 1.05rem; }
    .aga-servidor-meta { color: var(--muted); font-size: .82rem; }
    .aga-servidor-btn { color: var(--gold); font-size: .85rem; font-weight: 600; margin-top: .4rem; }

    /* ===== CTA FINAL ===== */
    .aga-cta-fim { text-align: center; background: linear-gradient(135deg, rgba(240,165,0,.08), rgba(206,17,38,.06)); border: 1px solid rgba(240,165,0,.2); border-radius: 16px; padding: 2.5rem 1.5rem; margin: 3.5rem auto 1rem; max-width: 900px; }
    .aga-cta-fim h3 { font-size: 1.6rem; margin: 0 0 .5rem; }
    .aga-cta-fim p { color: var(--muted); margin: 0 0 1.4rem; }
    .aga-cta-fim .aga-btn-primary, .aga-cta-fim .aga-btn-secondary { margin: 0 .3rem; }

    /* ===== FOOTER ===== */
    .site-footer .footer-html { color: var(--muted) !important; }
    .site-footer .footer-html span { color: var(--gold); }

    /* ===== bbPress ===== */
    #bbpress-forums { color: var(--text); }
    #bbpress-forums li.bbp-header, #bbpress-forums li.bbp-footer { background: var(--surface) !important; border-color: var(--border) !important; color: #fff; }
    #bbpress-forums .bbp-forum-title, #bbpress-forums .bbp-topic-title a { color: var(--gold) !important; font-weight: 600; }
    #bbpress-forums .bbp-forum-title:hover, #bbpress-forums .bbp-topic-title a:hover { color: var(--gold2) !important; }
    #bbpress-forums .bbp-body { background: var(--surface); }
    #bbpress-forums .bbp-body .bbp-forum, #bbpress-forums .bbp-body .bbp-topic { border-color: var(--border) !important; }
    .bbp-template-notice { background: var(--surface2) !important; border-color: var(--border) !important; border-radius: 8px; }
    .bbp-login-form input[type=text], .bbp-login-form input[type=password] { background: #0d0d16; border-color: var(--border); color: var(--text); }

    /* ===== EVENTS ===== */
    .tribe-events-calendar-month__day { background: var(--surface) !important; }
    .tribe-common--breakpoint-medium .tribe-events-calendar-month__day { background: var(--surface) !important; }
    .tribe-events-calendar-month__day-date { color: #fff !important; }
    .tribe-events-calendar-month__calendar-event-title { color: var(--gold) !important; }
    #tribe-events { --tec-color-background-events: transparent; }

    /* ===== FORMS ===== */
    input[type=text], input[type=email], input[type=url], input[type=password], textarea, select { background: #0d0d16 !important; border-color: var(--border) !important; color: var(--text) !important; border-radius: 8px; }
    input:focus, textarea:focus { border-color: var(--gold) !important; outline: none; }

    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 5px; }
    ';
    wp_add_inline_style('kadence-global', $css);
}
