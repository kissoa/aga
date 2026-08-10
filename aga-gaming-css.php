<?php
/*
Plugin Name: AGA Gaming Theme CSS
Description: Tema escuro com cores AGA (dourado/vermelho) para o tema Kadence — portal gaming.
Version: 1.0
Author: AGA
License: GPL-2.0
*/
/* Plugin: AGA Gaming CSS — tema escuro com cores AGA para o Kadence */
add_action('wp_enqueue_scripts', 'aga_gaming_css', 100);
function aga_gaming_css() {
    $css = '
    :root {
        --bg: #0a0a10; --surface: #12121f; --border: #1e1e3a;
        --gold: #f0a500; --red: #ce1126; --green: #00e676;
        --text: #e0e0f0; --muted: #6a6a9a;
    }
    body { background: var(--bg); color: var(--text); }
    body::before {
        content:""; position: fixed; inset: 0; pointer-events: none; z-index: 0;
        background: radial-gradient(ellipse 600px 400px at 50% -10%, rgba(206,17,38,.08) 0%, transparent 70%),
                    radial-gradient(ellipse 400px 500px at 85% 70%, rgba(240,165,0,.04) 0%, transparent 60%);
    }
    .site-container, .site { position: relative; z-index: 1; }
    .site-header, .site-footer { background: var(--surface) !important; border-color: var(--border) !important; }
    .site-branding .site-title a, .site-branding .site-title { color: #fff !important; font-weight: 800; }
    .main-navigation .menu-item a, .primary-menu a { color: var(--text) !important; }
    .main-navigation .menu-item a:hover { color: var(--gold) !important; }
    .entry-title, .page-title, h1, h2, h3, h4 { color: #fff !important; }
    .wp-block-button__link { border-radius: 6px !important; font-weight: 700 !important; }
    .site-footer .footer-html { color: var(--muted) !important; }
    .site-footer .footer-html span { color: var(--gold); }
    .entry-content a, .content a { color: var(--gold); }
    .entry-content a:hover { color: #ffc23d; }
    .widget-title { color: var(--gold) !important; }
    .post, .page, .entry, article { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; }
    .site-main .post, .site-main .page { padding: 1.5rem; }
    .header-navigation .menu-item > a { padding: 0.5rem 0.8rem; border-radius: 6px; }
    .header-navigation .menu-item > a:hover { background: rgba(240,165,0,.1); }
    .site-header .header-container { max-width: 1200px; margin: 0 auto; padding: 0.8rem 1.5rem; }
    /* bbPress */
    #bbpress-forums { color: var(--text); }
    #bbpress-forums li.bbp-header, #bbpress-forums li.bbp-footer { background: var(--surface); border-color: var(--border); }
    #bbpress-forums .bbp-forum-title, #bbpress-forums .bbp-topic-title a { color: var(--gold); font-weight: 600; }
    #bbpress-forums a.bbp-forum-title:hover, #bbpress-forums .bbp-topic-title a:hover { color: #ffc23d; }
    .bbp-forum-title, .bbp-topic-title { color: var(--gold) !important; }
    /* Events */
    .tribe-events-calendar-month__day-date, .tribe-events-calendar-month__calendar-event-title { color: #fff; }
    .tribe-common--breakpoint-medium .tribe-events-calendar-month__day { background: var(--surface); }
    #tribe-events, .tribe-common { --tec-color-background-events: transparent; --tec-color-text-event-title: #fff; }
    /* inputs / forms */
    input[type=text], input[type=email], input[type=url], textarea, select { background: #0d0d16; border-color: var(--border); color: var(--text); }
    /* scrollbar */
    ::-webkit-scrollbar { width: 10px; } ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 5px; }
    ';
    wp_add_inline_style('kadence-global', $css);
}
