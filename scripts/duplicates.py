#!/usr/bin/env python3
"""列出近似重复素材，供人工判定。

对 assets.json 里的静态图计算 64 位 dHash，汉明距离 ≤ 阈值即归为一组；
另做 SHA-256 精确比对。只读，不修改任何文件。

用法：python3 scripts/duplicates.py [--threshold 5]

基线见 DUPLICATES.md：38 组、98 张，均为有意派生。
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent


def dhash(path):
    with Image.open(path) as im:
        g = ImageOps.grayscale(im).resize((9, 8))
    px = list(g.getdata())
    bits = k = 0
    for r in range(8):
        for c in range(8):
            if px[r * 9 + c] > px[r * 9 + c + 1]:
                bits |= 1 << k
            k += 1
    return bits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--threshold', type=int, default=5)
    args = ap.parse_args()

    manifest = json.loads((ROOT / 'assets.json').read_text(encoding='utf-8'))
    items = [i for i in manifest['items'] if i['type'] == 'image']

    exact = collections.defaultdict(list)
    for it in items:
        exact[hashlib.sha256((ROOT / it['file']).read_bytes()).hexdigest()].append(it['title'])
    exact_groups = [v for v in exact.values() if len(v) > 1]

    print('静态图 %d 张' % len(items))
    print('精确重复（SHA-256）：%d 组' % len(exact_groups))
    for g in exact_groups:
        print('  ' + ' / '.join(g))

    hashes = [(it, dhash(ROOT / it['file'])) for it in items]
    seen, groups = set(), []
    for i in range(len(hashes)):
        if i in seen:
            continue
        group = [hashes[i]]
        seen.add(i)
        for j in range(i + 1, len(hashes)):
            if j in seen:
                continue
            if bin(hashes[i][1] ^ hashes[j][1]).count('1') <= args.threshold:
                group.append(hashes[j])
                seen.add(j)
        if len(group) > 1:
            groups.append(group)

    print('近似重复（dHash ≤ %d）：%d 组、%d 张' % (args.threshold, len(groups), sum(map(len, groups))))
    for n, group in enumerate(groups, 1):
        cats = '/'.join(sorted({it['category'] for it, _ in group}))
        print('%2d. [%s] %s' % (n, cats, '、'.join(it['title'] for it, _ in group)))


if __name__ == '__main__':
    main()
