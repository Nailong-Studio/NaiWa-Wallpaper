#!/usr/bin/env python3
"""生成库房公开首页（index.html），供 Cloudflare Pages / GitHub Pages 直接托管。

用法：python3 scripts/build_site.py
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
manifest = json.loads((ROOT / 'assets.json').read_text(encoding='utf-8'))

cards = []
for c in manifest['categories']:
    items = [i for i in manifest['items'] if i['category'] == c['id']]
    if not items:
        continue
    cover = items[0]['thumb']
    cards.append(
        f'<a class="card" href="https://github.com/Nailong-Studio/wallpaper/tree/main/{c["id"]}" target="_blank" rel="noopener">'
        f'<img loading="lazy" src="{cover}" alt="{html.escape(c["name"])}">'
        f'<span class="card__body"><b>{html.escape(c["name"])}</b><i>{html.escape(c["desc"])}</i></span></a>'
    )

template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>奶蛙艺术圣殿 · 库房</title>
<meta name="description" content="奶蛙艺术圣殿的公开库房：素材清单、缩略图与原图直链，取用请自便。">
<style>
:root{--void:#0B0806;--gold:#D9B45B;--gold2:#FFD54F;--ivory:#EDE4D0;--dim:#B8A175;--line:rgba(217,180,91,.28)}
*{box-sizing:border-box;margin:0;padding:0}
body{background:radial-gradient(120% 80% at 50% 0,#1a1209 0,var(--void) 55%);color:var(--ivory);
font-family:"Noto Serif SC","Songti SC",serif;line-height:1.9;min-height:100vh;padding:clamp(24px,5vw,64px)}
.wrap{max-width:1120px;margin:0 auto}
.kicker{color:var(--gold);letter-spacing:.5em;font-size:.74rem;text-indent:.5em}
h1{font-size:clamp(1.6rem,4vw,2.6rem);letter-spacing:.16em;color:var(--gold2);font-weight:600;margin:14px 0 10px}
.lead{color:rgba(237,228,208,.8);font-size:.88rem;max-width:62ch}
.nav{display:flex;flex-wrap:wrap;gap:10px;margin:24px 0 34px}
.nav a{color:var(--gold2);text-decoration:none;border:1px solid var(--line);padding:7px 14px;border-radius:999px;font-size:.76rem;letter-spacing:.06em}
.nav a:hover{border-color:var(--gold)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px}
.card{display:flex;flex-direction:column;border:1px solid var(--line);border-radius:2px;overflow:hidden;text-decoration:none;color:inherit;
background:linear-gradient(165deg,rgba(217,180,91,.06),rgba(11,8,6,.5));transition:transform .3s,border-color .3s}
.card:hover{transform:translateY(-3px);border-color:var(--gold)}
.card img{width:100%;aspect-ratio:16/10;object-fit:cover;background:#1a140d}
.card__body{padding:12px 14px 14px;display:flex;flex-direction:column;gap:4px}
.card__body b{color:var(--gold2);font-size:.9rem;letter-spacing:.08em;font-weight:500}
.card__body i{font-style:normal;color:var(--dim);font-size:.72rem;line-height:1.7}
footer{margin-top:44px;padding-top:18px;border-top:1px solid var(--line);color:var(--dim);font-size:.72rem;letter-spacing:.05em}
footer a{color:var(--gold)}
</style>
</head>
<body>
<div class="wrap">
  <p class="kicker">NAIWA RELIQUARY</p>
  <h1>奶蛙艺术圣殿 · 库房</h1>
  <p class="lead">本页是库房的公开窗口。所有素材均按厅登记在册，配来源、许可与档案；取用请自便，转载请先读许可。<br>
  库房不设门禁，也不提供讲解员——每件素材的档案就是讲解员。</p>
  <nav class="nav">
    <a href="assets.json">机器可读清单 · assets.json</a>
    <a href="thumbs/" target="_blank" rel="noopener">缩略图库</a>
    <a href="https://github.com/Nailong-Studio/wallpaper" target="_blank" rel="noopener">GitHub 库房</a>
    <a href="https://nailoong-universe.pages.dev/" target="_blank" rel="noopener">返回圣殿</a>
  </nav>
  <main class="grid">
__CARDS__
  </main>
  <footer>
    原图直链遵循 <code>assets.json</code> 中的 <code>raw</code> 字段。奶蛙为民间二创形象，角色原型权利归原权利人；
    若你是权利人并认为某件不宜收录，请开 Issue，我们会核实后下架。本库房不做商业用途。
  </footer>
</div>
</body>
</html>
""".replace('__CARDS__', '\n'.join(cards))

(ROOT / 'index.html').write_text(template, encoding='utf-8')
print('index.html written:', len(cards), 'categories')
