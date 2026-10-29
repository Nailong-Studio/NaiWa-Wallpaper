#!/usr/bin/env python3
"""生成库房公开索引页（index.html），供 Cloudflare Pages / GitHub Pages 直接托管。

定位：这是**素材仓库的取货窗口**，不是展馆。只列目录、件数、体积、格式与取用方式，
不铺大图墙——展示交给奶蛙艺术圣殿（NaiLoong-Universe）。

用法：python3 scripts/build_site.py
"""
import html
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
manifest = json.loads((ROOT / 'assets.json').read_text(encoding='utf-8'))

by_cat = {}
for it in manifest['items']:
    by_cat.setdefault(it['category'], []).append(it)


def kb(n):
    return '%.0f KB' % (n / 1024) if n < 1024 * 1024 else '%.1f MB' % (n / 1048576)


rows = []
for c in manifest['categories']:
    sub = by_cat.get(c['id'], [])
    if not sub:
        continue
    exts = {}
    for x in sub:
        ext = os.path.splitext(x['file'])[1].lower().lstrip('.')
        exts[ext] = exts.get(ext, 0) + 1
    ext_txt = ' / '.join('%s×%d' % (k, v) for k, v in sorted(exts.items(), key=lambda kv: -kv[1]))
    rows.append(
        '<tr><td><code>%s/</code></td><td>%s</td><td>%d</td><td>%s</td><td>%s</td><td>%s</td></tr>'
        % (c['id'], html.escape(c['name']), len(sub), kb(sum(x['bytes'] for x in sub)),
           ext_txt, html.escape(c['desc']))
    )

rows_txt = '\n'.join(rows)
cat_count = len([c for c in manifest['categories'] if c['count']])

page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>奶蛙素材库 · 取货窗口</title>
<meta name="description" content="奶蛙素材仓库索引：{manifest['total']} 件素材、{cat_count} 个分类，附分类表、目录结构与机器可读清单。">
<style>
:root{{--bg:#0d0b09;--fg:#e8e0cf;--gold:#d9b45b;--dim:#8a7f68;--line:#2a231a}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--fg);font:15px/1.7 "Noto Sans SC",-apple-system,"Segoe UI",sans-serif;padding:clamp(20px,4vw,56px)}}
.wrap{{max-width:980px;margin:0 auto}}
h1{{font-size:clamp(1.4rem,3vw,2rem);letter-spacing:.06em;color:var(--gold);font-weight:600;margin-bottom:6px}}
.sub{{color:var(--dim);font-size:.8rem;letter-spacing:.14em;margin-bottom:24px}}
p.lead{{color:#c3b9a4;font-size:.92rem;max-width:72ch;margin-bottom:24px}}
.links{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:32px}}
.links a{{color:var(--gold);text-decoration:none;border:1px solid var(--line);padding:6px 12px;font-size:.78rem}}
.links a:hover{{border-color:var(--gold)}}
h2{{font-size:.78rem;letter-spacing:.2em;color:var(--dim);margin:30px 0 12px;font-weight:500}}
table{{width:100%;border-collapse:collapse;font-size:.82rem}}
th{{text-align:left;color:var(--dim);font-weight:500;font-size:.7rem;letter-spacing:.1em;padding:6px 10px 6px 0;border-bottom:1px solid var(--line)}}
td{{padding:9px 10px 9px 0;border-bottom:1px solid rgba(42,35,26,.6);vertical-align:top}}
td code{{color:var(--gold);font-size:.8rem}}
td:nth-child(3),td:nth-child(4){{white-space:nowrap;color:var(--dim)}}
td:last-child{{color:#a99f8c;font-size:.78rem}}
pre{{background:#141109;border:1px solid var(--line);padding:16px;overflow-x:auto;font-size:.76rem;line-height:1.7;color:#b8ad95}}
footer{{margin-top:38px;padding-top:16px;border-top:1px solid var(--line);color:var(--dim);font-size:.74rem}}
footer a{{color:var(--gold)}}
</style>
</head>
<body>
<div class="wrap">
  <h1>奶蛙素材库</h1>
  <div class="sub">NAIWA ASSET VAULT · 取货窗口</div>
  <p class="lead">这里是<b>素材仓库</b>，不是展厅：{manifest['total']} 件素材按分类平铺存放，每件配同名 <code>.txt</code> 档案（叙事 / 来源 / 许可）。
  看策展过的成品，请去 <a href="https://nailoong-universe.pages.dev/" style="color:var(--gold)">奶蛙艺术圣殿</a>。</p>

  <div class="links">
    <a href="assets.json">assets.json · 机器可读清单</a>
    <a href="https://github.com/Nailong-Studio/wallpaper" target="_blank" rel="noopener">GitHub 仓库</a>
    <a href="https://naiwa-wallpaper.pages.dev/" target="_blank" rel="noopener">壁纸扩展</a>
    <a href="https://github.com/Nailong-Studio/wallpaper/releases" target="_blank" rel="noopener">打包下载</a>
  </div>

  <h2>分类一览</h2>
  <table>
    <thead><tr><th>目录</th><th>分类</th><th>件数</th><th>体积</th><th>格式</th><th>说明</th></tr></thead>
    <tbody>
{rows_txt}
    </tbody>
  </table>

  <h2>取用方式</h2>
  <pre># 单件直链（GitHub raw，跟随改名跳转）
https://raw.githubusercontent.com/Nailong-Studio/wallpaper/main/&lt;分类&gt;/&lt;文件名&gt;

# 或走 Cloudflare 图床（开 CORS，可直接当壁纸 URL）
{manifest['rawBase']}&lt;分类&gt;/&lt;文件名&gt;

# 按清单程序化取用
curl -s https://raw.githubusercontent.com/Nailong-Studio/wallpaper/main/assets.json
</pre>

  <footer>
    素材 {manifest['total']} 件 · 版本 {manifest['sourceVersion']} · 更新于 {manifest['generated']}。
    奶蛙为民间二创形象，角色原型权利归原权利人；本库只收录许可允许再分发的素材，逐件来源见同名 <code>.txt</code>。
    若你是权利人并认为某件不宜收录，请开 <a href="https://github.com/Nailong-Studio/wallpaper/issues">Issue</a>，核实后下架。
  </footer>
</div>
</body>
</html>
"""
(ROOT / 'index.html').write_text(page, encoding='utf-8')
print('index.html written: %d items, %d categories' % (manifest['total'], cat_count))
