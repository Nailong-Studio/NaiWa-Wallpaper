#!/usr/bin/env python3
"""奶蛙世界的内页生成器。

首页只留地图和入口；聚落、今日、藏品滩、取货口各自成页。
"""
import json
from html import escape


def js_json(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


def esc(s):
    return escape(str(s or ''), quote=True)


SYMBOLS = r'''<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="i-frame" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="1" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M6 16l4-5 3 3 2-2 3 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></symbol>
  <symbol id="i-laugh" viewBox="0 0 24 24"><path d="M4 12c0 5 3.6 8 8 8s8-3 8-8" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M8 9h.01M16 9h.01" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></symbol>
  <symbol id="i-sticker" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M8 14c1.4 1.6 2.8 2.4 4 2.4s2.6-.8 4-2.4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M9 9h.01M15 9h.01" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></symbol>
  <symbol id="i-pose" viewBox="0 0 24 24"><circle cx="12" cy="7" r="3" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M12 10v6m0 0l-3 5m3-5l3 5M7 12h10" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></symbol>
  <symbol id="i-paw" viewBox="0 0 24 24"><ellipse cx="12" cy="15" rx="5" ry="4" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="7" cy="9" r="2" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="7" r="2" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="17" cy="9" r="2" fill="none" stroke="currentColor" stroke-width="1.6"/></symbol>
  <symbol id="i-spark" viewBox="0 0 24 24"><path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8L12 3Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></symbol>
  <symbol id="i-wave" viewBox="0 0 24 24"><path d="M3 13c2-2.4 4-2.4 6 0s4 2.4 6 0 4-2.4 6 0M3 18c2-2.4 4-2.4 6 0s4 2.4 6 0 4-2.4 6 0" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></symbol>
  <symbol id="i-film" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="1" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M10 9l5 3-5 3V9Z" fill="currentColor"/><path d="M3 9h2M19 9h2M3 15h2M19 15h2" stroke="currentColor" stroke-width="1.6"/></symbol>
  <symbol id="i-box" viewBox="0 0 24 24"><path d="M4 8l8-4 8 4v9l-8 4-8-4V8Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M4 8l8 4 8-4M12 12v9" fill="none" stroke="currentColor" stroke-width="1.6"/></symbol>
  <symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="6" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M16 16l4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></symbol>
  <symbol id="i-close" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></symbol>
  <symbol id="i-sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.5 1.5M17.5 17.5L19 19M19 5l-1.5 1.5M6.5 17.5L5 19" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></symbol>
  <symbol id="i-moon" viewBox="0 0 24 24"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.4 6.4 0 0 0 10.5 10.5Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></symbol>
  <symbol id="i-arrow" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  <symbol id="i-naiwa" viewBox="0 0 64 64"><path d="M32 8c12 0 21 8 21 20 0 11-9 18-21 18S11 39 11 20C11 8 20 2 32 2Z" fill="#FFD54F"/><circle cx="23" cy="23" r="7" fill="#66BB6A"/><circle cx="41" cy="23" r="7" fill="#66BB6A"/><circle cx="23" cy="23" r="3" fill="#14120c"/><circle cx="41" cy="23" r="3" fill="#14120c"/><ellipse cx="32" cy="43" rx="13" ry="10" fill="#F2E3BE"/><path d="M8 54c8-4 16-5 24-2s16 2 24-1" fill="none" stroke="#FFD54F" stroke-width="3" stroke-linecap="round"/></symbol>
</svg>'''

SUB_CSS = r'''
@font-face{font-family:"ZCOOL KuaiLe";src:url("fonts/zcool-kuaile-display.woff2?v=__VERSION__") format("woff2");font-weight:400;font-style:normal;font-display:swap}
:root{
  --bg:#0d0c09;--bg2:#13110c;--panel:#191610;--panel2:#211c13;
  --ink:#efe5cf;--muted:#a79b82;--line:#342b1d;--dim:#7f735d;
  --gold:#f1c24d;--green:#7cc36a;
  --shadow:0 22px 60px rgba(0,0,0,.45);
  --display:"ZCOOL KuaiLe","STKaiti","KaiTi","PingFang SC","Microsoft YaHei",sans-serif;
  --body:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans CJK SC",sans-serif;
  color-scheme:dark;
}
html[data-theme="light"]{
  --bg:#f6efdd;--bg2:#efe4cb;--panel:#fffaf0;--panel2:#f7ecd6;
  --ink:#2d2618;--muted:#74684f;--line:#d8c7a4;--dim:#9b8a6a;
  --gold:#a86f0d;--green:#4c8a3b;
  --shadow:0 20px 44px rgba(88,68,30,.16);
  color-scheme:light;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--ink);font:16px/1.75 var(--body);-webkit-font-smoothing:antialiased}
img{display:block;max-width:100%}
a{color:inherit}
button,input{font:inherit;color:inherit}
::selection{background:var(--gold);color:var(--bg)}
:focus-visible{outline:2px solid var(--gold);outline-offset:3px}
.skip{position:absolute;left:-999px;top:8px;z-index:20;background:var(--gold);color:var(--bg);padding:8px 14px}
.skip:focus{left:8px}
.wrap{width:min(1240px,92vw);margin:0 auto}

/* ===== 顶栏 ===== */
.top{position:sticky;top:0;z-index:10;background:color-mix(in srgb,var(--bg) 86%,transparent);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.top__in{width:min(1240px,92vw);margin:0 auto;display:flex;align-items:center;gap:28px;height:66px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;font-family:var(--display);font-size:21px;letter-spacing:.04em;white-space:nowrap}
.brand svg{width:30px;height:30px;flex:none}
.brand b{font-weight:400}
.nav{display:flex;gap:22px;margin-left:auto;font-size:13px;letter-spacing:.06em;color:var(--muted)}
.nav a{text-decoration:none;position:relative;padding:6px 0}
.nav a::after{content:"";position:absolute;left:0;right:100%;bottom:0;height:1px;background:var(--gold);transition:right .25s}
.nav a:hover{color:var(--ink)}
.nav a:hover::after,.nav a[aria-current="page"]::after{right:0}
.nav a[aria-current="page"]{color:var(--ink)}
.theme{flex:none;margin-left:auto;width:38px;height:38px;border:1px solid var(--line);background:transparent;display:grid;place-items:center;cursor:pointer;color:var(--muted)}
.theme:hover{color:var(--gold);border-color:var(--gold)}
.theme svg{width:18px;height:18px}
.theme .moon{display:none}
html[data-theme="light"] .theme .moon{display:block}
html[data-theme="light"] .theme .sun{display:none}
.menu{flex:none;display:none;width:38px;height:38px;border:1px solid var(--line);background:transparent;place-items:center;align-content:center;cursor:pointer;color:var(--muted)}
.menu:hover{color:var(--gold);border-color:var(--gold)}
.menu span{display:block;width:15px;height:1px;background:currentColor;margin:2px 0;transition:transform .2s,opacity .2s}
.menu[aria-expanded="true"] span:nth-child(1){transform:translateY(3px) rotate(45deg)}
.menu[aria-expanded="true"] span:nth-child(2){opacity:0}
.menu[aria-expanded="true"] span:nth-child(3){transform:translateY(-3px) rotate(-45deg)}
.mobile-menu{display:none;border-top:1px solid var(--line);background:var(--bg)}
.mobile-menu nav{width:min(1240px,92vw);margin:0 auto;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:24px}
.mobile-menu a{padding:13px 2px;border-bottom:1px solid var(--line);font-size:13px;letter-spacing:.04em;color:var(--muted);text-decoration:none}
.mobile-menu a:hover{color:var(--gold)}
.mobile-menu a[aria-current="page"]{color:var(--ink)}

/* ===== 内页门头 ===== */
.page-hero{padding:clamp(40px,6vw,72px) 0 clamp(28px,4vw,44px);border-bottom:1px solid var(--line);position:relative;overflow:hidden}
.crumbs{display:flex;flex-wrap:wrap;align-items:center;gap:8px;font-size:11px;letter-spacing:.04em;color:var(--dim);margin-bottom:22px}
.crumbs a{text-decoration:none;color:var(--muted)}
.crumbs a:hover{color:var(--gold)}
.kicker{display:flex;align-items:center;gap:10px;font-size:11px;letter-spacing:.22em;color:var(--muted);margin-bottom:16px}
.kicker::before{content:"";width:34px;height:1px;background:var(--gold)}
.page-hero h1{font-family:var(--display);font-weight:400;font-size:clamp(48px,7.4vw,92px);line-height:.98;letter-spacing:.01em;color:var(--ink)}
.page-hero h1 em{font-style:normal;color:var(--gold);white-space:nowrap}
.page-hero .lede{max-width:44em;margin-top:20px;color:var(--muted);font-size:clamp(14px,1.5vw,16px);line-height:1.85}
.page-hero .hero-meta{display:flex;flex-wrap:wrap;gap:10px 24px;align-items:center;margin-top:24px;font-size:12px}
.page-hero .hero-meta a{color:var(--gold);text-decoration:none;border-bottom:1px solid var(--gold);padding-bottom:2px}
.section{padding:clamp(36px,6vw,64px) 0;border-bottom:1px solid var(--line)}
.page-foot{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:18px 28px;padding-top:28px;margin-top:12px;font-size:12px;color:var(--muted)}
.page-foot p{max-width:40ch;line-height:1.8}
.btn{display:inline-flex;align-items:center;gap:10px;background:var(--gold);color:var(--bg);text-decoration:none;padding:11px 18px;font-size:13px;font-weight:500;letter-spacing:.04em;border:1px solid var(--gold);transition:transform .2s,background .2s}
.btn:hover{transform:translateY(-2px);background:var(--ink);border-color:var(--ink);color:var(--bg)}
.link{font-size:13px;color:var(--muted);text-decoration:none;border-bottom:1px solid var(--line);padding-bottom:3px}
.link:hover{color:var(--gold);border-color:var(--gold)}

/* ===== 聚落目录 ===== */
.zone-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;background:var(--line);border:1px solid var(--line)}
.zone{display:grid;grid-template-columns:104px minmax(0,1fr) 20px;gap:18px;align-items:center;background:var(--bg2);padding:18px;text-decoration:none;position:relative;transition:background .2s}
.zone:hover{background:var(--panel)}
.zone:hover .zone__cover img{transform:scale(1.04)}
.zone__cover{width:104px;height:104px;overflow:hidden;background:var(--panel);border:1px solid var(--line)}
.zone__cover img{width:100%;height:100%;object-fit:cover;transition:transform .35s}
.zone__meta{min-width:0}
.zone__meta small{display:block;font-size:10px;color:var(--dim);letter-spacing:.12em}
.zone__meta h3{font-family:var(--display);font-weight:400;font-size:22px;line-height:1.2;margin:4px 0 5px;color:var(--ink)}
.zone__meta p{font-size:12px;color:var(--muted);line-height:1.65}
.zone__count{font-size:12px;color:var(--gold);margin-top:6px;display:block}
.zone__go{font-size:14px;color:var(--gold);text-align:right;white-space:nowrap}
.zone__go::after{content:" →";font-size:11px}

/* ===== 今日三件 ===== */
.today-grid{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:clamp(20px,3vw,40px);align-items:start}
.today-main{position:relative}
.today-main figure{aspect-ratio:4/3;overflow:hidden;background:var(--panel);border:1px solid var(--line)}
.today-main img{width:100%;height:100%;object-fit:cover;transition:transform .5s}
.today-main:hover img{transform:scale(1.03)}
.today-main h3{font-family:var(--display);font-weight:400;font-size:clamp(26px,3vw,38px);line-height:1.15;margin:18px 0 8px}
.today-main p{color:var(--muted);font-size:14px;line-height:1.85;max-width:42em}
.today-main a{display:inline-block;margin-top:12px;font-size:12px;color:var(--gold);text-decoration:none;border-bottom:1px solid var(--gold)}
.today-side{display:grid;gap:1px;background:var(--line);border:1px solid var(--line)}
.today-mini{display:grid;grid-template-columns:132px minmax(0,1fr);gap:16px;align-items:center;background:var(--bg2);padding:14px;text-decoration:none;transition:background .2s}
.today-mini:hover{background:var(--panel)}
.today-mini figure{width:132px;height:100px;overflow:hidden;background:var(--panel)}
.today-mini img{width:100%;height:100%;object-fit:cover}
.today-mini h4{font-family:var(--display);font-weight:400;font-size:19px;line-height:1.25;margin-bottom:4px}
.today-mini p{font-size:12px;color:var(--muted);line-height:1.6;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}

/* ===== 藏品滩 ===== */
.collection-page{padding:clamp(28px,5vw,52px) 0 clamp(50px,7vw,86px)}
.collection-bar{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;border-bottom:1px solid var(--line);padding-bottom:14px;margin-bottom:20px}
.count{font-size:12px;color:var(--muted);letter-spacing:.04em}
.filters{display:grid;gap:15px;margin-bottom:26px}
.search{display:flex;align-items:center;gap:10px;border-bottom:1px solid var(--line);padding:8px 2px;max-width:620px;transition:border-color .2s}
.search:focus-within{border-color:var(--gold)}
.search:focus-within svg{color:var(--gold)}
.search svg{width:18px;height:18px;color:var(--muted);flex:none}
.search input{width:100%;min-width:0;background:none;border:0;outline:0;font-size:14px;color:var(--ink);padding:4px 0}
.search input::placeholder{color:var(--dim)}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{border:1px solid var(--line);background:transparent;color:var(--muted);font-size:11px;padding:6px 10px;cursor:pointer;letter-spacing:.03em}
.chip[aria-pressed="true"]{background:var(--gold);border-color:var(--gold);color:var(--bg)}
.chip:hover{border-color:var(--gold);color:var(--ink)}
.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.card{background:var(--panel);border:1px solid var(--line);text-align:left;cursor:pointer;padding:0;display:flex;flex-direction:column;transition:border-color .2s,transform .2s;overflow:hidden}
.card:hover{border-color:var(--gold);transform:translateY(-3px)}
.card figure{width:100%;aspect-ratio:4/3;background:var(--bg);display:grid;place-items:center;overflow:hidden}
.card figure img{width:100%;height:100%;object-fit:contain}
.card__body{padding:10px 12px 13px;border-top:1px solid var(--line)}
.card__cat{font-size:10px;letter-spacing:.1em;color:var(--gold)}
.card__title{font-size:13px;line-height:1.4;margin-top:3px;color:var(--ink);display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.card__dim{font-size:10px;color:var(--dim);margin-top:5px}
.more{display:flex;justify-content:center;margin-top:34px}
.more button{border:1px solid var(--line);background:transparent;color:var(--muted);padding:11px 26px;font-size:13px;letter-spacing:.06em;cursor:pointer}
.more button:hover{border-color:var(--gold);color:var(--gold)}
.more button[hidden]{display:none}
.empty{border:1px solid var(--line);background:var(--panel);padding:34px 20px;margin-top:26px;text-align:center}
.empty p{color:var(--muted);font-size:13px;line-height:1.8}
.empty button{margin-top:14px;border:1px solid var(--gold);background:transparent;color:var(--gold);padding:9px 18px;font-size:12px;cursor:pointer}
.empty button:hover{background:var(--gold);color:var(--bg)}

/* ===== 取货口 ===== */
.take-page{padding:clamp(32px,5vw,56px) 0 clamp(54px,7vw,86px)}
.take-panel{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:clamp(24px,4vw,44px);border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:clamp(24px,4vw,38px) 0}
.take-copy,.take-links{min-width:0}
.take-copy h2{font-family:var(--display);font-weight:400;font-size:clamp(26px,3vw,36px);line-height:1.15;margin-bottom:10px}
.take-copy p{font-size:13px;line-height:1.8;color:var(--muted);max-width:38em}
.take-copy p + p{margin-top:8px}
.take-pre{background:var(--panel);border:1px solid var(--line);padding:18px;overflow-x:auto;max-width:100%;font-size:12px;line-height:1.9;color:var(--muted);margin-top:20px}
.take-pre b{color:var(--gold);font-weight:400}
.take-list{border-top:1px solid var(--line)}
.take-list a{display:grid;grid-template-columns:minmax(0,1fr) 18px;gap:12px;align-items:center;text-decoration:none;padding:13px 0;border-bottom:1px solid var(--line);color:var(--muted);font-size:13px;transition:color .2s,padding .2s}
.take-list a:hover{color:var(--gold);padding-left:8px}
.take-list a small{display:block;color:var(--dim);font-size:11px;margin-top:2px;line-height:1.5}
.take-list a span{color:var(--gold);text-align:right}
.take-note{margin-top:20px;font-size:12px;line-height:1.8;color:var(--dim)}

/* ===== 页脚 ===== */
footer{border-top:1px solid var(--line);padding:26px 0 34px;font-size:12px;color:var(--muted)}
.foot{display:flex;justify-content:space-between;gap:28px;align-items:flex-start}
.foot p{max-width:62ch;line-height:1.8}
.foot a{color:var(--gold);text-decoration:none}
.foot__meta{text-align:right;white-space:nowrap;font-size:11px;line-height:1.8}

/* ===== Star 引导 ===== */
.star-callout{display:flex;align-items:center;justify-content:space-between;gap:20px;background:var(--panel);border:1px solid var(--line);padding:18px 20px;margin:0 auto 24px}
.star-callout__copy{display:flex;align-items:center;gap:12px;min-width:0}
.star-callout__mark{color:var(--gold);font-size:22px;line-height:1;flex:none}
.star-callout__copy strong{display:block;color:var(--ink);font-size:14px;line-height:1.5}
.star-callout__copy small{display:block;color:var(--muted);font-size:11px;line-height:1.6;margin-top:3px}
.star-callout__links{display:flex;flex-wrap:wrap;gap:8px;flex:none}
.star-callout__links a{border:1px solid var(--line);border-radius:999px;color:var(--gold);font-size:11px;line-height:1;padding:9px 11px;text-decoration:none;white-space:nowrap;transition:border-color .2s,background .2s}
.star-callout__links a:hover{border-color:var(--gold);background:var(--bg2)}

/* ===== 灯箱 ===== */
dialog{border:1px solid var(--line);background:var(--panel);color:var(--ink);padding:0;width:min(1080px,94vw);max-height:90vh;margin:auto;box-shadow:var(--shadow)}
dialog::backdrop{background:rgba(0,0,0,.72);backdrop-filter:blur(4px)}
.lb{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,.75fr);min-height:420px}
.lb figure{background:var(--bg);display:grid;place-items:center;padding:18px;max-height:84vh;overflow:hidden}
.lb figure img{max-height:78vh;width:auto;max-width:100%;object-fit:contain}
.lb figure img[hidden]{display:none}
.lb figure video{display:block;width:100%;height:auto;max-height:78vh;background:#000}
.lb figure video[hidden]{display:none}
.lb audio{display:block;width:100%;margin:14px 0 2px}
.lb audio[hidden]{display:none}
.lb__copy{padding:clamp(22px,3vw,38px);overflow-y:auto;max-height:84vh;border-left:1px solid var(--line)}
.lb__cat{font-size:11px;letter-spacing:.12em;color:var(--gold)}
.lb h3{font-family:var(--display);font-weight:400;font-size:clamp(26px,3vw,34px);line-height:1.15;margin:8px 0 14px}
.lb p{font-size:13px;line-height:1.9;color:var(--muted)}
.lb dl{display:grid;grid-template-columns:64px minmax(0,1fr);gap:7px 12px;margin:20px 0;font-size:12px;border-top:1px solid var(--line);padding-top:16px}
.lb dt{color:var(--dim)}
.lb dd{color:var(--ink);word-break:break-word}
.lb a{display:inline-block;margin-top:6px;font-size:12px;color:var(--gold);text-decoration:none;border-bottom:1px solid var(--gold)}
.lb__close{position:absolute;right:10px;top:10px;width:36px;height:36px;border:1px solid var(--line);background:var(--panel);color:var(--muted);cursor:pointer;display:grid;place-items:center}
.lb__close:hover{color:var(--gold);border-color:var(--gold)}
.lb__close svg{width:16px;height:16px}

/* ===== 响应 ===== */
@media (max-width:1080px){
  .zone-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
  .grid{grid-template-columns:repeat(3,minmax(0,1fr))}
  .today-grid{grid-template-columns:1fr}
  .today-side{grid-template-columns:repeat(2,minmax(0,1fr))}
  .take-panel{grid-template-columns:1fr}
}
@media (max-width:760px){
  .top__in{gap:12px;height:58px}
  .brand{font-size:18px}
  .brand svg{width:26px;height:26px}
  .nav{display:none}
  .star-callout{flex-direction:column;align-items:flex-start;gap:12px}
  .menu{display:grid}
  .mobile-menu:not([hidden]){display:block}
  .page-hero h1{font-size:clamp(42px,13vw,64px)}
  .zone-grid{grid-template-columns:1fr}
  .zone{grid-template-columns:82px minmax(0,1fr) 16px;gap:13px;padding:14px}
  .zone__cover{width:82px;height:82px}
  .zone__meta h3{font-size:20px}
  .zone__go{font-size:12px}
  .grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
  .card__title{font-size:12px}
  .today-side{grid-template-columns:1fr}
  .today-mini{grid-template-columns:104px minmax(0,1fr)}
  .today-mini figure{width:104px;height:92px}
  .collection-bar{display:block}
  .collection-bar .link{display:inline-block;margin-top:8px}
  .lb{grid-template-columns:1fr}
  .lb__copy{border-left:0;border-top:1px solid var(--line);max-height:none}
  .lb figure{max-height:48vh;padding:10px}
  .lb figure img{max-height:44vh}
  .lb figure video{max-height:44vh}
  .foot{flex-direction:column}
  .foot__meta{text-align:left;white-space:normal}
}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  *,*::before,*::after{animation:none!important;transition:none!important}
}
'''

SUB_HTML = r'''<!DOCTYPE html>
<html lang="zh-CN" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
<meta name="theme-color" content="#0d0c09" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#f6efdd" media="(prefers-color-scheme: light)">
<link rel="canonical" href="__CANONICAL__">
<meta property="og:type" content="website">
<meta property="og:title" content="__TITLE__">
<meta property="og:description" content="__DESC__">
<meta property="og:url" content="__CANONICAL__">
<meta property="og:image" content="__OG_IMAGE__">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="__FAVICON__">
<link rel="preload" href="fonts/zcool-kuaile-display.woff2?v=__VERSION__" as="font" type="font/woff2" crossorigin>
<script>
(function(){try{var t=localStorage.getItem('naiwa-world-theme');if(!t)t=matchMedia('(prefers-color-scheme: light)').matches?'light':'dark';document.documentElement.dataset.theme=t;}catch(e){}})();
</script>
<style>__SUB_CSS__</style>
</head>
<body>
<a class="skip" href="#main">跳到正文</a>
__SYMBOLS__
__HEADER__
<main id="main">
__BODY__
</main>
__FOOTER__
__DIALOG__
<script>
__COMMON_JS__
</script>
<script>
__PAGE_JS__
</script>
</body>
</html>
'''

COMMON_JS = r'''(function(){
  var root=document.documentElement;
  var themeBtn=document.getElementById('theme');
  function setTheme(t){
    root.dataset.theme=t;
    if(themeBtn) themeBtn.setAttribute('aria-pressed',t==='light'?'true':'false');
    try{localStorage.setItem('naiwa-world-theme',t);}catch(e){}
  }
  setTheme(root.dataset.theme||(matchMedia('(prefers-color-scheme: light)').matches?'light':'dark'));
  if(themeBtn) themeBtn.addEventListener('click',function(){setTheme(root.dataset.theme==='light'?'dark':'light');});

  var menuBtn=document.getElementById('menu');
  var mobileNav=document.getElementById('mobileNav');
  function setMenu(open){
    if(!menuBtn||!mobileNav) return;
    mobileNav.hidden=!open;
    menuBtn.setAttribute('aria-expanded',open?'true':'false');
    menuBtn.setAttribute('aria-label',open?'收起导航':'展开导航');
  }
  if(menuBtn&&mobileNav){
    menuBtn.addEventListener('click',function(){setMenu(mobileNav.hidden);});
    mobileNav.addEventListener('click',function(e){if(e.target.closest('a')) setMenu(false);});
    document.addEventListener('click',function(e){
      if(mobileNav.hidden) return;
      if(!e.target.closest('#mobileNav')&&!e.target.closest('#menu')) setMenu(false);
    });
    document.addEventListener('keydown',function(e){
      if(e.key==='Escape'&&!mobileNav.hidden){setMenu(false);menuBtn.focus();}
    });
  }
})();'''

LIGHTBOX = r'''<dialog id="lightbox" aria-label="藏品详情">
  <button class="lb__close" id="lbClose" type="button" aria-label="关闭"><svg><use href="#i-close" xlink:href="#i-close"/></svg></button>
  <div class="lb">
    <figure>
      <img id="lbImg" alt="">
      <video id="lbVideo" controls playsinline preload="metadata" hidden></video>
    </figure>
    <div class="lb__copy">
      <div class="lb__cat" id="lbCat"></div>
      <h3 id="lbTitle"></h3>
      <p id="lbNarr"></p>
      <audio id="lbAudio" controls preload="metadata" hidden></audio>
      <dl>
        <dt>尺寸</dt><dd id="lbDim">—</dd>
        <dt>许可</dt><dd id="lbLicense">—</dd>
        <dt>来源</dt><dd id="lbSource">—</dd>
      </dl>
      <a id="lbRaw" href="#" target="_blank" rel="noopener">打开原件 ↗</a>
    </div>
  </div>
</dialog>'''


def header(active):
    links = [
        ('zones', 'zones.html', '聚落'),
        ('history', 'history.html', '简史'),
        ('today', 'today.html', '今日'),
        ('collection', 'collection.html', '藏品滩'),
        ('take', 'take.html', '取货口'),
    ]
    nav = []
    mobile = []
    for key, href, label in links:
        cur = ' aria-current="page"' if key == active else ''
        nav.append('<a href="%s"%s>%s</a>' % (href, cur, label))
        mobile.append('<a href="%s"%s>%s</a>' % (href, cur, label))
    external = '<a href="https://github.com/Nailong-Studio/NaiWa-Wallpaper" target="_blank" rel="noopener">★ Star</a>\n        <a href="https://nailoong-universe.pages.dev/" target="_blank" rel="noopener">艺术圣殿 ↗</a>'
    nav.append(external)
    mobile.append(external)
    return '''<header class="top">
  <div class="top__in">
    <a class="brand" href="index.html"><svg><use href="#i-naiwa" xlink:href="#i-naiwa"/></svg><b>奶蛙世界</b></a>
    <nav class="nav" aria-label="主导航">%s</nav>
    <button class="theme" id="theme" type="button" aria-label="切换明暗主题" aria-pressed="false">
      <svg class="sun"><use href="#i-sun" xlink:href="#i-sun"/></svg>
      <svg class="moon"><use href="#i-moon" xlink:href="#i-moon"/></svg>
    </button>
    <button class="menu" id="menu" type="button" aria-label="展开导航" aria-expanded="false" aria-controls="mobileNav">
      <span></span><span></span><span></span>
    </button>
  </div>
  <div class="mobile-menu" id="mobileNav" hidden>
    <nav aria-label="手机导航">%s</nav>
  </div>
</header>''' % ('\n      '.join(nav), '\n      '.join(mobile))


FOOTER = r'''<footer>
<div class="wrap star-callout" aria-label="给项目点 Star">
  <div class="star-callout__copy">
    <span class="star-callout__mark" aria-hidden="true">★</span>
    <div>
      <strong>如果这些奶蛙让你笑了一下，去 GitHub 给五个项目各点一颗 Star。</strong>
      <small>Star 是公开的收藏，不用打赏，也不用注册新账号。</small>
    </div>
  </div>
  <div class="star-callout__links">
    <a href="https://github.com/Nailong-Studio/NaiWa-Wallpaper" target="_blank" rel="noopener">素材仓库 ↗</a>
    <a href="https://github.com/Nailong-Studio/NaiWa-NewTab" target="_blank" rel="noopener">新标签页扩展 ↗</a>
    <a href="https://github.com/Nailong-Studio/NaiLoong-Universe" target="_blank" rel="noopener">艺术圣殿 ↗</a>
    <a href="https://github.com/Nailong-Studio/naiwa" target="_blank" rel="noopener">像素游戏 ↗</a>
    <a href="https://github.com/Nailong-Studio/naiwa-pixel-stickers" target="_blank" rel="noopener">像素表情技能 ↗</a>
  </div>
</div>
  <div class="wrap foot">
    <p>奶蛙是民间二创形象，角色原型权利归原权利人。本库只收录许可允许再分发的素材，逐件来源与许可见同名 <code>.txt</code>。若你是权利人并认为某件不宜收录，请开 <a href="https://github.com/Nailong-Studio/NaiWa-Wallpaper/issues">Issue</a>，核实后下架。</p>
    <div class="foot__meta">__TOTAL__ 件藏品 · v__VERSION__ · __DATE__<br><a href="index.html">奶蛙世界</a> / <a href="history.html">奶蛙简史</a> / NAIWA WORLD</div>
  </div>
</footer>'''

COLLECTION_JS = r'''(function(){
  const ZONES = __ZONES_JSON__;
  const ITEMS = __ITEMS_JSON__;
  const grid = document.getElementById('grid');
  const chips = document.getElementById('chips');
  const countEl = document.getElementById('count');
  const moreBtn = document.getElementById('more');
  const empty = document.getElementById('empty');
  const q = document.getElementById('q');
  const params = new URLSearchParams(location.search);
  const initialZone = ZONES.some(function(z){return z.id===params.get('zone');}) ? params.get('zone') : 'all';
  const state = { zone: initialZone, q: params.get('q') || '', shown: 24 };

  function zoneOf(id){ return ZONES.find(function(z){return z.id===id;}); }
  function zoneNameOf(it){
    const z = ZONES.find(function(z){return z.cats.indexOf(it.c)>-1;});
    return z ? z.name : '';
  }
  function inZone(it){
    if(state.zone==='all') return true;
    const z = zoneOf(state.zone);
    return z ? z.cats.indexOf(it.c)>-1 : true;
  }
  function filtered(){
    const needle = state.q.trim().toLowerCase();
    return ITEMS.filter(function(it){
      if(!inZone(it)) return false;
      if(!needle) return true;
      return (it.t+' '+it.n+' '+it.s+' '+it.cn+' '+zoneNameOf(it)).toLowerCase().indexOf(needle)>-1;
    });
  }
  function card(it, idx){
    const dim = it.w && it.h ? it.w+' × '+it.h : (it.ty==='video' ? '影像' : '音频');
    const eager = idx<4;
    const dims = (it.ty==='image' && it.w && it.h) ? ' width="'+it.w+'" height="'+it.h+'"' : '';
    return '<button class="card" type="button" data-idx="'+idx+'">'+
      '<figure><img src="'+esc(it.th)+'" alt="'+esc(it.t)+'"'+dims+' loading="'+(eager?'eager':'lazy')+'"'+(eager?' fetchpriority="high"':'')+' decoding="async"></figure>'+
      '<div class="card__body"><div class="card__cat">'+esc(it.cn)+'</div>'+
      '<div class="card__title">'+esc(it.t)+'</div>'+
      '<div class="card__dim">'+dim+'</div></div></button>';
  }
  function render(){
    const list = filtered();
    const slice = list.slice(0, state.shown);
    grid.innerHTML = slice.map(card).join('');
    countEl.textContent = '滩上 '+list.length+' 件 · 已铺开 '+slice.length+' 件';
    moreBtn.hidden = slice.length>=list.length;
    moreBtn.textContent = '再拾 '+Math.min(24,list.length-slice.length)+' 件';
    empty.hidden = list.length!==0;
  }
  function syncUrl(){
    const p = new URLSearchParams();
    if(state.zone!=='all') p.set('zone',state.zone);
    if(state.q.trim()) p.set('q',state.q);
    const s = p.toString();
    try{history.replaceState(null,'',location.pathname+(s?'?'+s:''));}catch(e){}
  }
  function setZone(id, resetSearch){
    state.zone = id;
    state.shown = 24;
    if(resetSearch){state.q='';q.value='';}
    Array.from(chips.children).forEach(function(b){
      b.setAttribute('aria-pressed', b.dataset.zone===id?'true':'false');
    });
    render(); syncUrl();
  }
  function buildChips(){
    const all = document.createElement('button');
    all.className='chip'; all.type='button'; all.dataset.zone='all';
    all.textContent='全部 '+ITEMS.length; all.setAttribute('aria-pressed','true');
    chips.appendChild(all);
    ZONES.forEach(function(z){
      const b=document.createElement('button');
      b.className='chip'; b.type='button'; b.dataset.zone=z.id;
      b.textContent=z.name+' '+z.count; b.setAttribute('aria-pressed','false');
      chips.appendChild(b);
    });
    chips.addEventListener('click',function(e){
      const b=e.target.closest('.chip');
      if(b) setZone(b.dataset.zone);
    });
  }

  function esc(s){
    return String(s==null?'':s).replace(/[&<>"']/g,function(c){
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
    });
  }

  const lb=document.getElementById('lightbox');
  const lbImg=document.getElementById('lbImg');
  const lbVideo=document.getElementById('lbVideo');
  const lbAudio=document.getElementById('lbAudio');
  const lbCat=document.getElementById('lbCat');
  const lbTitle=document.getElementById('lbTitle');
  const lbNarr=document.getElementById('lbNarr');
  const lbDim=document.getElementById('lbDim');
  const lbLicense=document.getElementById('lbLicense');
  const lbSource=document.getElementById('lbSource');
  const lbRaw=document.getElementById('lbRaw');
  function openItem(it){
    const isVideo=it.ty==='video';
    const isAudio=it.ty==='audio';
    lbVideo.pause(); lbAudio.pause();
    lbImg.hidden=isVideo;
    lbVideo.hidden=!isVideo;
    lbAudio.hidden=!isAudio;
    if(isVideo){lbVideo.poster=it.th;lbVideo.src=it.r;lbVideo.load();}
    else{lbVideo.removeAttribute('src');lbVideo.load();}
    if(isAudio){lbAudio.src=it.r;lbAudio.load();}
    else{lbAudio.removeAttribute('src');lbAudio.load();}
    lbCat.textContent=it.cn;
    lbTitle.textContent=it.t;
    lbNarr.textContent=it.n||'这件还没有展签。';
    lbDim.textContent=(it.w&&it.h)?it.w+' × '+it.h:(isVideo?'影像':'音频');
    lbLicense.textContent=it.l||'见同名 .txt';
    lbSource.textContent=it.s||'—';
    lbRaw.href=it.r||'#';
    lbImg.alt=it.t;
    lbImg.dataset.full=it.r||'';
    lbImg.src=it.th;
    if(!isVideo&&!isAudio&&it.r&&it.r!==it.th){
      const full=new Image();
      full.onload=function(){if(lb.open&&lbImg.dataset.full===it.r) lbImg.src=it.r;};
      full.src=it.r;
    }
    lb.showModal();
  }
  grid.addEventListener('click',function(e){
    const b=e.target.closest('.card');
    if(!b) return;
    const list=filtered();
    const it=list[Number(b.dataset.idx)];
    if(it) openItem(it);
  });
  document.getElementById('lbClose').addEventListener('click',function(){lb.close();});
  lb.addEventListener('close',function(){lbVideo.pause();lbAudio.pause();});
  lb.addEventListener('click',function(e){if(e.target===lb) lb.close();});
  document.addEventListener('keydown',function(e){
    if(e.key==='Escape'&&lb.open) lb.close();
  });
  document.getElementById('emptyReset').addEventListener('click',function(){
    setZone('all',true); q.focus();
  });
  q.addEventListener('input',function(){state.q=q.value;state.shown=24;render();syncUrl();});
  moreBtn.addEventListener('click',function(){state.shown+=24;render();});

  buildChips();
  q.value=state.q;
  setZone(state.zone,false);
})();'''

TODAY_JS = r'''(function(){
  const POOL = __TODAY_POOL__;
  const grid = document.getElementById('todayGrid');
  const date = new Date();
  const seed = date.getFullYear()*372 + (date.getMonth()+1)*31 + date.getDate();
  const picked = [];
  if(POOL.length){
    for(let k=0;k<3;k++){
      let idx=(seed*7+k*137)%POOL.length;
      let guard=0;
      while(picked.indexOf(POOL[idx])>-1 && guard<POOL.length){idx=(idx+1)%POOL.length;guard++;}
      picked.push(POOL[idx]);
    }
  }
  function esc(s){
    return String(s==null?'':s).replace(/[&<>"']/g,function(c){
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
    });
  }
  if(!picked.length){
    grid.innerHTML='<p class="empty">今天没有可铺的图。</p>';
  }else{
    const main=picked[0];
    const mainHtml='<article class="today-main">'+
      '<figure><img src="'+esc(main.th)+'" alt="'+esc(main.t)+'" loading="eager" decoding="async"></figure>'+
      '<h3>'+esc(main.t)+'</h3><p>'+esc(main.n)+'</p>'+
      '<a href="#lightbox" data-today="'+esc(main.i)+'">看这一件</a></article>';
    const sideHtml='<div class="today-side">'+picked.slice(1).map(function(it){
      return '<a class="today-mini" href="#lightbox" data-today="'+esc(it.i)+'">'+
        '<figure><img src="'+esc(it.th)+'" alt="'+esc(it.t)+'" loading="lazy" decoding="async"></figure>'+
        '<div><h4>'+esc(it.t)+'</h4><p>'+esc(it.n)+'</p></div></a>';
    }).join('')+'</div>';
    grid.innerHTML=mainHtml+sideHtml;
  }
  grid.addEventListener('click',function(e){
    const a=e.target.closest('[data-today]');
    if(!a) return;
    e.preventDefault();
    const it=POOL.find(function(x){return x.i===a.dataset.today;});
    if(it) openItem(it);
  });

  const lb=document.getElementById('lightbox');
  const lbImg=document.getElementById('lbImg');
  const lbVideo=document.getElementById('lbVideo');
  const lbAudio=document.getElementById('lbAudio');
  const lbCat=document.getElementById('lbCat');
  const lbTitle=document.getElementById('lbTitle');
  const lbNarr=document.getElementById('lbNarr');
  const lbDim=document.getElementById('lbDim');
  const lbLicense=document.getElementById('lbLicense');
  const lbSource=document.getElementById('lbSource');
  const lbRaw=document.getElementById('lbRaw');
  function openItem(it){
    const isVideo=it.ty==='video';
    const isAudio=it.ty==='audio';
    lbVideo.pause();lbAudio.pause();
    lbImg.hidden=isVideo;
    lbVideo.hidden=!isVideo;
    lbAudio.hidden=!isAudio;
    if(isVideo){lbVideo.poster=it.th;lbVideo.src=it.r;lbVideo.load();}
    else{lbVideo.removeAttribute('src');lbVideo.load();}
    if(isAudio){lbAudio.src=it.r;lbAudio.load();}
    else{lbAudio.removeAttribute('src');lbAudio.load();}
    lbCat.textContent=it.cn;
    lbTitle.textContent=it.t;
    lbNarr.textContent=it.n||'这件还没有展签。';
    lbDim.textContent=(it.w&&it.h)?it.w+' × '+it.h:(isVideo?'影像':'音频');
    lbLicense.textContent=it.l||'见同名 .txt';
    lbSource.textContent=it.s||'—';
    lbRaw.href=it.r||'#';
    lbImg.alt=it.t;
    lbImg.dataset.full=it.r||'';
    lbImg.src=it.th;
    if(!isVideo&&!isAudio&&it.r&&it.r!==it.th){
      const full=new Image();
      full.onload=function(){if(lb.open&&lbImg.dataset.full===it.r) lbImg.src=it.r;};
      full.src=it.r;
    }
    lb.showModal();
  }
  document.getElementById('lbClose').addEventListener('click',function(){lb.close();});
  lb.addEventListener('close',function(){lbVideo.pause();lbAudio.pause();});
  lb.addEventListener('click',function(e){if(e.target===lb) lb.close();});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&lb.open) lb.close();});
})();'''


def page(title, desc, canonical, body, css='', script='', dialog='', active='home', og_image='', version='', total='', date='', favicon=''):
    html = SUB_HTML
    html = html.replace('__TITLE__', title)
    html = html.replace('__DESC__', desc)
    html = html.replace('__CANONICAL__', canonical)
    html = html.replace('__OG_IMAGE__', og_image)
    html = html.replace('__FAVICON__', favicon)
    html = html.replace('__SUB_CSS__', SUB_CSS + css)
    html = html.replace('__SYMBOLS__', SYMBOLS)
    html = html.replace('__HEADER__', header(active))
    html = html.replace('__BODY__', body)
    html = html.replace('__FOOTER__', FOOTER)
    html = html.replace('__DIALOG__', dialog)
    html = html.replace('__COMMON_JS__', COMMON_JS)
    html = html.replace('__PAGE_JS__', script)
    html = html.replace('__TOTAL__', str(total))
    html = html.replace('__VERSION__', str(version))
    html = html.replace('__DATE__', str(date))
    return html


def zone_cards(zones):
    out = []
    for idx, z in enumerate(zones, 1):
        out.append(
            '<a class="zone" href="collection.html?zone=%s">'
            '<div class="zone__cover"><img src="%s" alt="%s" loading="lazy" decoding="async"></div>'
            '<div class="zone__meta"><small>ZONE %02d</small><h3>%s</h3><p>%s</p>'
            '<span class="zone__count">%d 件 · %s</span></div>'
            '<span class="zone__go">进入</span></a>'
            % (z['id'], esc(z['cover']), esc(z['coverAlt']), idx, esc(z['name']), esc(z['desc']), z['count'], kb(z['bytes']))
        )
    return '\n'.join(out)


def kb(n):
    return '%.0f KB' % (n / 1024) if n < 1024 * 1024 else '%.1f MB' % (n / 1048576)


def build_pages(manifest, zones, slim, favicon, raw_base, cat_count, ext_count):
    version = manifest['sourceVersion']
    date = manifest['generated']
    total = manifest['total']
    base = 'https://nailoong-wallpaper.pages.dev'
    og = base + '/classic/%E5%A5%B6%E8%9B%99-%E4%B8%98%E6%AF%94%E7%89%B9%E4%B8%8E%E6%99%AE%E7%BB%AA%E5%85%8B.jpg'
    pages = {}

    zones_body = '''<section class="page-hero">
  <div class="wrap">
    <div class="crumbs"><a href="index.html">奶蛙世界</a><span>/</span><span>九座聚落</span></div>
    <div class="kicker">THE NINE / 九座聚落</div>
    <h1>先认路，<em>再挑滩。</em></h1>
    <p class="lede">九座聚落各管一类。点任意一座，直接落到筛好的藏品滩；不想挑，就从第一座开始走。地图留在首页，目录在这里。</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="zone-grid">%s</div>
    <div class="page-foot"><p>每座聚落只负责一个方向，进去之后再用搜索和分类慢慢收窄。</p><a class="btn" href="collection.html">直接去藏品滩 <svg width="14" height="14" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-arrow" xlink:href="#i-arrow"/></svg></a></div>
  </div>
</section>''' % zone_cards(zones)
    pages['zones.html'] = page(
        '九座聚落 · 奶蛙世界',
        '奶蛙世界的九座聚落目录：名画、大笑、表情、姿势、桌宠、奇想、壁纸、圣影与档案馆。点一座，直接进入筛好的藏品滩。',
        base + '/zones', zones_body, active='zones', og_image=og,
        version=version, total=total, date=date, favicon=favicon,
    )

    today_body = '''<section class="page-hero">
  <div class="wrap">
    <div class="crumbs"><a href="index.html">奶蛙世界</a><span>/</span><span>今日三件</span></div>
    <div class="kicker">THREE TODAY / 今日三件</div>
    <h1>今天轮到<em>这三件。</em></h1>
    <p class="lede">按日期轮换，不按热度，也不做推荐榜。看完就关门，想看更多再去藏品滩。</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="today-grid" id="todayGrid"></div>
    <div class="page-foot"><p>这三件只负责今天。明天再进来，会换成另外三件。</p><a class="btn" href="collection.html">去藏品滩看全部 <svg width="14" height="14" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-arrow" xlink:href="#i-arrow"/></svg></a></div>
  </div>
</section>'''
    today_pool = [it for it in slim if it['ty'] == 'image' and (it.get('w') or 0) >= 900 and len(it.get('n') or '') > 16]
    today_js = TODAY_JS.replace('__TODAY_POOL__', js_json(today_pool))
    pages['today.html'] = page(
        '今日三件 · 奶蛙世界',
        '奶蛙世界今天轮到的三件藏品。每天按日期更换，看完可以从这里去藏品滩。',
        base + '/today', today_body, script=today_js, dialog=LIGHTBOX, active='today', og_image=og,
        version=version, total=total, date=date, favicon=favicon,
    )

    collection_body = '''<section class="page-hero">
  <div class="wrap">
    <div class="crumbs"><a href="index.html">奶蛙世界</a><span>/</span><span>藏品滩</span></div>
    <div class="kicker">THE SHORE / 藏品滩</div>
    <h1>%d 件，<em>慢慢翻。</em></h1>
    <p class="lede">全部藏品都在这一页。按聚落、分类或关键词找；一次只铺 24 件，找到想看的再打开。首页不放这张长清单。</p>
    <div class="hero-meta"><a href="zones.html">← 回九座聚落</a><a href="today.html">先看今日三件</a></div>
  </div>
</section>
<section class="collection-page">
  <div class="wrap">
    <div class="collection-bar">
      <p class="count" id="count" aria-live="polite">正在数藏品……</p>
      <a class="link" href="zones.html">按聚落走</a>
    </div>
    <div class="filters">
      <label class="search">
        <svg><use href="#i-search" xlink:href="#i-search"/></svg>
        <input id="q" type="search" placeholder="搜标题、展签、来源" aria-label="搜索藏品" autocomplete="off">
      </label>
      <div class="chips" id="chips" role="group" aria-label="按聚落筛选"></div>
    </div>
    <div class="grid" id="grid"></div>
    <div class="empty" id="empty" hidden>
      <p>滩上没找到这一件。换个词，或者把筛子倒空。</p>
      <button id="emptyReset" type="button">清空搜索和聚落</button>
    </div>
    <div class="more"><button id="more" type="button">再拾 24 件</button></div>
  </div>
</section>''' % total
    collection_js = COLLECTION_JS.replace('__ZONES_JSON__', js_json(zones)).replace('__ITEMS_JSON__', js_json(slim))
    pages['collection.html'] = page(
        '藏品滩 · %d 件藏品 · 奶蛙世界' % total,
        '奶蛙世界全部 %d 件藏品。按九座聚落、分类和关键词筛选，一次铺开 24 件。' % total,
        base + '/collection', collection_body, script=collection_js, dialog=LIGHTBOX, active='collection', og_image=og,
        version=version, total=total, date=date, favicon=favicon,
    )

    take_body = '''<section class="page-hero">
  <div class="wrap">
    <div class="crumbs"><a href="index.html">奶蛙世界</a><span>/</span><span>取货口</span></div>
    <div class="kicker">THE BACK DOOR / 取货口</div>
    <h1>给要拿去用的人，<em>留一扇侧门。</em></h1>
    <p class="lede">这里不放展签，只放取用方式：单件直链、全量清单、打包下载和两个外站。看完就可以走。</p>
  </div>
</section>
<section class="take-page">
  <div class="wrap">
    <div class="take-panel">
      <div class="take-copy">
        <h2>三种取法</h2>
        <p>单件可以直接拼 GitHub raw 路径；也可以走 Cloudflare 图床，开 CORS；要整批就拿 assets.json。</p>
        <pre class="take-pre"># 单件直链（GitHub raw，跟随改名跳转）
https://raw.githubusercontent.com/Nailong-Studio/NaiWa-Wallpaper/main/&lt;分类&gt;/&lt;文件名&gt;

# 或走 Cloudflare 图床（开 CORS，可直接当壁纸 URL）
__RAW_BASE__&lt;分类&gt;/&lt;文件名&gt;

# 按清单程序化取用
curl -s https://raw.githubusercontent.com/Nailong-Studio/NaiWa-Wallpaper/main/assets.json</pre>
      </div>
      <div class="take-links">
        <div class="take-list">
          <a href="assets.json"><div>assets.json · __TOTAL__ 件全量清单<small>标题 / 尺寸 / 展签 / 许可 / 来源</small></div><span>↗</span></a>
          <a href="https://github.com/Nailong-Studio/NaiWa-Wallpaper" target="_blank" rel="noopener"><div>GitHub 仓库<small>Nailong-Studio/NaiWa-Wallpaper</small></div><span>↗</span></a>
          <a href="https://github.com/Nailong-Studio/NaiWa-Wallpaper/releases" target="_blank" rel="noopener"><div>打包下载<small>Release 附件</small></div><span>↗</span></a>
          <a href="https://naiwa-wallpaper.pages.dev/" target="_blank" rel="noopener"><div>奶蛙壁纸扩展<small>新标签页内置 __EXT_COUNT__ 张</small></div><span>↗</span></a>
          <a href="https://nailoong-universe.pages.dev/" target="_blank" rel="noopener"><div>奶蛙艺术圣殿<small>策展过的成品展厅</small></div><span>↗</span></a>
        </div>
        <p class="take-note">许可和来源写在每件同名的 .txt 里。拿去做壁纸、桌面宠物或二创，先看那一行。</p>
      </div>
    </div>
    <div class="page-foot"><p>这页是给开发者和批量取用的人准备的；普通浏览回藏品滩就够了。</p><a class="link" href="collection.html">回藏品滩</a></div>
  </div>
</section>'''
    take_body = take_body.replace('__RAW_BASE__', raw_base).replace('__TOTAL__', str(total)).replace('__EXT_COUNT__', str(ext_count))
    pages['take.html'] = page(
        '取货口 · 给开发者 · 奶蛙世界',
        '奶蛙世界的取货口：单件直链、全量 assets.json、打包下载、壁纸扩展和艺术圣殿入口。',
        base + '/take', take_body, active='take', og_image=og,
        version=version, total=total, date=date, favicon=favicon,
    )
    return pages
