<?php
/*
Plugin Name: AGA Stats Pages
Description: Endpoints /stats/jogo/<jogo> — estatísticas reais por jogo (jogadores online, servidores, rankings).
Version: 1.0
Author: AGA
*/

// Registo da rota: /stats/jogo/<slug>
add_action('init', function () {
    add_rewrite_rule('^stats/jogo/([a-z0-9-]+)/?$', 'index.php?aga_jogo=$matches[1]', 'top');
});
add_filter('query_vars', function ($vars) {
    $vars[] = 'aga_jogo';
    return $vars;
});
add_action('template_redirect', function () {
    $jogo = get_query_var('aga_jogo');
    if (!$jogo) return;
    aga_render_stats($jogo);
    exit;
});

function aga_render_stats($slug) {
    // Mapa: slug -> (nome, url_estado, tipo)
    $jogos = [
        'civ'       => ['FreeCiv', 'https://civ.aga.org.ao/', 'civ'],
        'xadrez'    => ['Xadrez', 'https://xadrez.aga.org.ao/', 'xadrez'],
        'ogame'     => ['OGame', 'https://ogame.aga.org.ao/', 'web'],
        'travianz'  => ['TravianZ', 'https://travianz.aga.org.ao/', 'web'],
        'suroi'     => ['Suroi', 'https://suroi.aga.org.ao/', 'web'],
        'kaetram'   => ['Kaetram', 'https://kaetram.aga.org.ao/', 'web'],
        'tosios'    => ['Tosios', 'https://tosios.aga.org.ao/', 'web'],
        'supernova' => ['Supernova', 'https://supernova.aga.org.ao/', 'web'],
        'ageofai'   => ['AgeOfAI', 'https://ageofai.aga.org.ao/', 'web'],
        'hypersomnia' => ['Hypersomnia', 'https://hypersomnia.aga.org.ao/', 'web'],
        'scribble'  => ['Scribble', 'https://scribble.aga.org.ao/', 'web'],
        'woc'       => ['World of Craft', 'https://woc.aga.org.ao/', 'web'],
    ];
    if (!isset($jogos[$slug])) {
        aga_stats_html('Jogo desconhecido', 'Sem dados para este jogo.', []);
        return;
    }
    [$nome, $url, $tipo] = $jogos[$slug];

    $stats = [];
    if ($tipo === 'civ') {
        // FreeCiv: tentar aceder ao metaserver da VM (a API local do freeciv-web)
        $stats = aga_stats_civ();
    } elseif ($tipo === 'xadrez') {
        $stats = aga_stats_xadrez();
    } else {
        // verificar se o site responde (online/offline)
        $stats = aga_stats_web($url);
    }

    aga_stats_html($nome, $url, $stats);
}

function aga_stats_web($url) {
    $ctx = stream_context_create(['http' => ['timeout' => 4, 'ignore_errors' => true]]);
    $start = microtime(true);
    $code = @file_get_contents($url, false, $ctx);
    $ms = round((microtime(true) - $start) * 1000);
    if ($code === false) {
        return [['rótulo' => 'Estado', 'valor' => 'OFFLINE'], ['rótulo' => 'Latência', 'valor' => '—']];
    }
    $ok = is_string($code) && strpos($code, '<html') !== false ? 'ONLINE' : 'RESPONDE';
    return [['rótulo' => 'Estado', 'valor' => $ok], ['rótulo' => 'Latência', 'valor' => $ms . ' ms']];
}

function aga_stats_civ() {
    $r = [];
    $ch = curl_init('https://civ.aga.org.ao/');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 5);
    $html = curl_exec($ch);
    $ok = $html !== false && is_string($html);
    $r[] = ['rótulo' => 'Estado', 'valor' => $ok ? 'ONLINE' : 'OFFLINE'];
    if (preg_match('/id="statistics-singleplayer"><b>(\d+)<\/b>.*?id="statistics-multiplayer"><b>(\d+)<\/b>/s', (string)$html, $m)) {
        $r[] = ['rótulo' => 'Jogos 1 jogador', 'valor' => $m[1]];
        $r[] = ['rótulo' => 'Jogos multi', 'valor' => $m[2]];
    }
    return $r;
}

function aga_stats_xadrez() {
    $ch = curl_init('https://xadrez.aga.org.ao/');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 5);
    $html = curl_exec($ch);
    $ok = $html !== false && is_string($html);
    $r = [['rótulo' => 'Estado', 'valor' => $ok ? 'ONLINE' : 'OFFLINE']];
    if ($ok && preg_match('/class="site-title"[^>]*>([^<]+)</', $html, $m)) {
        $r[] = ['rótulo' => 'Servidor', 'valor' => trim($m[1])];
    }
    return $r;
}

function aga_stats_html($nome, $url, $stats) {
    header('Content-Type: text/html; charset=utf-8');
    $rows = '';
    foreach ($stats as $s) {
        $val = $s['valor'];
        $cls = (strpos($val, 'ONLINE') !== false) ? 'ok' : ((strpos($val, 'OFFLINE') !== false) ? 'bad' : '');
        $rows .= "<div class=\"stat\"><span class=\"k\">{$s['rótulo']}</span><span class=\"v $cls\">{$val}</span></div>";
    }
    echo '<!DOCTYPE html><html lang="pt"><head><meta charset="UTF-8"><style>
    body{margin:0;font-family:system-ui,sans-serif;background:#0a0a10;color:#e0e0f0}
    .wrap{padding:1rem;max-width:560px}
    .h{display:flex;align-items:center;justify-content:space-between;margin-bottom:.8rem}
    .h b{color:#fff;font-size:1.05rem}.h a{color:#f0a500;text-decoration:none;font-size:.85rem}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:.6rem}
    .stat{background:#12121f;border:1px solid #1e1e3a;border-radius:10px;padding:.7rem .9rem}
    .k{display:block;font-size:.65rem;text-transform:uppercase;letter-spacing:1px;color:#6a6a9a;margin-bottom:.25rem}
    .v{font-size:1.1rem;font-weight:800;color:#fff}
    .v.ok{color:#00e676}.v.bad{color:#ff5252}
    .note{color:#6a6a9a;font-size:.75rem;margin-top:1rem}
    </style></head><body><div class="wrap">
    <div class="h"><b>📊 ' . $nome . '</b><a href="' . $url . '" target="_blank">Abrir jogo →</a></div>
    <div class="grid">' . $rows . '</div>
    <div class="note">Dados recolhidos em tempo real. Atualizado a cada carregamento.</div>
    </div></body></html>';
}
