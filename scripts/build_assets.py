#!/usr/bin/env python3
"""生成/校验素材清单 assets.json 与 480px 缩略图 thumbs/。

用法：
  python3 scripts/build_assets.py            # 生成清单与缩略图
  python3 scripts/build_assets.py --check    # 只校验清单/缩略图是否齐全
  python3 scripts/build_assets.py --site ../NaiLoong-Universe/docs  # 同步到官网
"""
import argparse
import datetime
import json
import re
import shutil
import subprocess
import tempfile
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = 'https://nailoong-wallpaper.pages.dev/'
CATS = [
    ('classic', '圣典名画', '奶蛙主演的西方名画再创作'),
    ('laugh-gallery', '大笑藏馆', '全网搜集的大笑奶蛙变体'),
    ('emotes', '表情收藏', '表情包、官方姿态、立绘与动图'),
    ('poses', '姿势立绘', '3D 奶蛙换装立绘：职业、道具与表情'),
    ('poses-wall', '姿势壁纸', '3D 立绘合成的 1080×1920 竖屏壁纸'),
    ('pet', '桌宠动作', '桌宠动画帧与待机/大笑/倾听/躺平循环 GIF'),
    ('art', '艺术场景', 'AI 生成的生活场景与艺术脑洞'),
    ('hd', '高清壁纸', '高清表情壁纸'),
    ('4k', '4K 大图', '新标签页插件内置 4K 素材'),
    ('mobile', '手机壁纸', '1080×1936 竖屏，手机与平板'),
    ('frames', '视频帧图', '圣影抽帧与竖屏壁纸'),
    ('videos', '官方圣影', '圣殿巡行、壁纸隧道、大笑巡展与原片'),
    ('fan-videos', '同人短片', '粉丝二创的奶蛙短片与场景动画'),
    ('audio', '音效语音', '奶蛙笑声、语音与可用音效'),
    ('assets', '品牌资产', '奶蛙 logo 与品牌图'),
]
MEDIA = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.mp4', '.webm', '.mp3', '.wav', '.ogg', '.m4a'}
VIDEO = {'.mp4', '.webm'}
AUDIO = {'.mp3', '.wav', '.ogg', '.m4a'}


def title_of(stem):
    s = re.sub(r'^奶蛙[-_]?', '', stem).strip('-')
    s = s.replace('帧图-', '')
    s = re.sub(r'-(\d+s)$', r' · \1', s)
    s = re.sub(r'-(\d{2})$', r' \1', s)
    return s.replace('-', ' · ').strip() or stem


PROV = re.compile(r'^(来源|许可|版权|用途|署名|分辨率|格式)\s*[：:]')


def narrative_of(p):
    t = p.with_name(p.name + '.txt')
    if not t.exists():
        return ''
    lines = [x.strip() for x in t.read_text(encoding='utf-8', errors='ignore').splitlines() if x.strip()]
    body = []
    for line in lines[1:]:
        if PROV.match(line):
            break
        body.append(line)
    return '\n'.join(body).strip() if body else (lines[0] if lines else '')


def field_of(p, key):
    """读取同名 .txt 里 `字段：值` 形式的记录（来源 / 许可）。"""
    t = p.with_name(p.name + '.txt')
    if not t.exists():
        return ''
    m = re.search(rf'^\s*{key}\s*[：:]?\s*(.+)$', t.read_text(encoding='utf-8', errors='ignore'), re.M)
    return m.group(1).strip() if m else ''


def license_of(p):
    v = field_of(p, '许可')
    return v.split('；')[0].split(';')[0].strip() if v else '未标注'


def source_of(p):
    v = field_of(p, '来源')
    return v.split('·')[0].strip() if v else '奶蛙艺术圣殿'


def media_size(src, thumb):
    """真实素材尺寸：图片读原图，视频读视频流，音频无尺寸。"""
    suf = src.suffix.lower()
    if suf in VIDEO:
        try:
            out = subprocess.check_output([
                'ffprobe', '-v', 'error', '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height', '-of', 'json', str(src)
            ])
            st = json.loads(out)['streams'][0]
            return int(st['width']), int(st['height'])
        except Exception:
            with Image.open(thumb) as im:
                return im.size
    if suf in AUDIO:
        return None, None
    with Image.open(src) as im:
        return im.size


def make_thumb(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.suffix.lower() in VIDEO:
        with tempfile.TemporaryDirectory() as td:
            frame = Path(td) / 'frame.png'
            subprocess.run(['ffmpeg', '-v', 'error', '-ss', '1', '-i', str(src), '-frames:v', '1', str(frame)], check=False)
            if not frame.exists():
                subprocess.run(['ffmpeg', '-v', 'error', '-i', str(src), '-frames:v', '1', str(frame)], check=False)
            if not frame.exists():
                return None
            im = Image.open(frame)
            im.thumbnail((480, 480), Image.LANCZOS)
            im.convert('RGB').save(dst, 'WEBP', quality=80, method=6)
            return im.size
    if src.suffix.lower() in AUDIO:
        with tempfile.TemporaryDirectory() as td:
            wave = Path(td) / 'wave.png'
            subprocess.run(['ffmpeg', '-v', 'error', '-i', str(src), '-filter_complex',
                            'showwavespic=s=960x540:colors=#FFD54F', '-frames:v', '1', str(wave)], check=False)
            if wave.exists():
                im = Image.open(wave).convert('RGB')
                im.thumbnail((480, 480), Image.LANCZOS)
                im.save(dst, 'WEBP', quality=80, method=6)
                return im.size
        return None
    im = Image.open(src)
    if getattr(im, 'is_animated', False):
        im.seek(0)
    if im.mode == 'P' and 'transparency' in im.info:
        im = im.convert('RGBA')
    else:
        im = im.convert('RGBA' if 'A' in im.getbands() else 'RGB')
    im.thumbnail((480, 480), Image.LANCZOS)
    im.save(dst, 'WEBP', quality=80, method=6)
    return im.size


def scan():
    items = []
    for cid, cname, _ in CATS:
        d = ROOT / cid
        if not d.exists():
            continue
        for p in sorted(d.iterdir(), key=lambda x: x.name):
            if not p.is_file() or p.suffix.lower() not in MEDIA:
                continue
            rel = p.relative_to(ROOT).as_posix()
            th = f'thumbs/{cid}/{p.stem}.webp'
            items.append({
                'id': rel, 'category': cid, 'categoryName': cname,
                'title': title_of(p.stem), 'file': rel,
                'raw': RAW + urllib.parse.quote(rel), 'thumb': th,
                'type': ('video' if p.suffix.lower() in VIDEO else
                         ('audio' if p.suffix.lower() in AUDIO else
                          ('gif' if p.suffix.lower() == '.gif' else 'image'))),
                'bytes': p.stat().st_size,
                'narrative': narrative_of(p),
                'license': license_of(p),
                'source': source_of(p),
                'form': ('anthro' if cid in ('poses', 'poses-wall') else 'naiwa'),
            })
    return items


def build():
    items = scan()
    for it in items:
        src = ROOT / it['file']
        dst = ROOT / it['thumb']
        if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            make_thumb(src, dst)
        it['width'], it['height'] = media_size(src, dst)
    counts = {}
    for it in items:
        counts[it['category']] = counts.get(it['category'], 0) + 1
    manifest = {
        'name': '奶蛙艺术圣殿 · 素材总清单',
        'repo': 'Nailong-Studio/NaiWa-Wallpaper',
        'sourceVersion': (ROOT / 'VERSION').read_text(encoding='utf-8').split()[0].lstrip('v')
        if (ROOT / 'VERSION').exists() else '',
        'generated': datetime.date.today().isoformat(),
        'rawBase': RAW,
        'total': len(items),
        'categories': [{'id': c, 'name': n, 'desc': d, 'count': counts.get(c, 0)} for c, n, d in CATS],
        'items': items,
    }
    (ROOT / 'assets.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'assets.json: {len(items)} items, thumbs: {len(list((ROOT / "thumbs").rglob("*.webp")))}')
    return manifest


def check(manifest):
    items = scan()
    errors = []
    if manifest.get('total') != len(items):
        errors.append(f'total {manifest.get("total")} != {len(items)}')
    ids = {x['id'] for x in items}
    m_ids = {x['id'] for x in manifest.get('items', [])}
    if ids != m_ids:
        errors.append(f'items diff: missing_in_manifest={len(ids-m_ids)} missing_on_disk={len(m_ids-ids)}')
    for it in items:
        if not (ROOT / it['thumb']).exists():
            errors.append('missing thumb: ' + it['thumb'])
    expected = {it['thumb'] for it in items}
    actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'thumbs').rglob('*.webp')}
    if actual - expected:
        errors.append(f'orphan thumbs: {len(actual - expected)}')

    for it in manifest.get('items', []):
        if not it.get('license') or it['license'] == '未标注':
            errors.append('missing license: ' + it['file'])
        if not it.get('source'):
            errors.append('missing source: ' + it['file'])
        if it.get('form') not in ('naiwa', 'anthro'):
            errors.append('bad form: ' + it['file'])
        if not it.get('narrative'):
            errors.append('empty narrative: ' + it['file'])
        if it['type'] == 'image':
            try:
                with Image.open(ROOT / it['file']) as im:
                    if im.size != (it['width'], it['height']):
                        errors.append('stale size: %s %sx%s != %sx%s' % (
                            it['file'], it['width'], it['height'], im.width, im.height))
            except Exception as exc:
                errors.append('unreadable image: %s (%s)' % (it['file'], exc))

    for it in manifest.get('items', []):
        if not it.get('license') or it['license'] == '未标注':
            errors.append('missing license: ' + it['file'])
        if not it.get('source'):
            errors.append('missing source: ' + it['file'])
        if it.get('form') not in ('naiwa', 'anthro'):
            errors.append('bad form: ' + it['file'])
        if not it.get('narrative'):
            errors.append('empty narrative: ' + it['file'])
        if it['type'] == 'image':
            try:
                with Image.open(ROOT / it['file']) as im:
                    if im.size != (it['width'], it['height']):
                        errors.append('stale size: %s %sx%s != %sx%s' % (
                            it['file'], it['width'], it['height'], im.width, im.height))
            except Exception as exc:
                errors.append('unreadable image: %s (%s)' % (it['file'], exc))

    counts = {}
    for it in items:
        counts[it['category']] = counts.get(it['category'], 0) + 1
    mc = {c['id']: c['count'] for c in manifest.get('categories', [])}
    if mc != counts:
        errors.append(f'category counts {mc} != {counts}')
    if errors:
        print('\n'.join(['FAIL'] + errors))
        raise SystemExit(1)
    print(f'OK: {len(items)} items, {len(actual)} thumbs, categories {counts}')


def sync_site(manifest, site):
    site = Path(site).resolve()
    dst_root = site / 'assets' / 'relics'
    if dst_root.exists():
        shutil.rmtree(dst_root)
    items = []
    for it in manifest['items']:
        src = ROOT / it['thumb']
        dst = dst_root / it['category'] / src.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        x = dict(it)
        x['thumb'] = f'assets/relics/{it["category"]}/{src.name}'
        items.append(x)
    out = dict(manifest, items=items)
    (site / 'data').mkdir(parents=True, exist_ok=True)
    (site / 'data' / 'assets.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'site sync: {len(items)} items -> {site}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--site')
    args = ap.parse_args()
    if args.check:
        check(json.loads((ROOT / 'assets.json').read_text(encoding='utf-8')))
        return
    manifest = build()
    if args.site:
        sync_site(manifest, args.site)


if __name__ == '__main__':
    from PIL import Image  # noqa: E402  (仅生成/校验缩略图时需要)
    main()
