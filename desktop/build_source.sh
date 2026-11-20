#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 - <<'PY'
import zipfile, pathlib
root = pathlib.Path('.')
out = pathlib.Path('dist/NaiWaWallpaper-0.0.3-source.zip')
out.parent.mkdir(parents=True, exist_ok=True)
skip_parts = {'bin','obj','dist','.git'}
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for name in ['src','assets','README.md','SOURCES.md','CHANGELOG.md','VERSION','LICENSE','build_windows.sh','build_linux.sh','build_source.sh','preview.png','.gitignore']:
        p = root / name
        if p.is_file(): z.write(p, name)
        elif p.is_dir():
            for f in sorted(p.rglob('*')):
                if not f.is_file(): continue
                if any(part in skip_parts for part in f.relative_to(root).parts): continue
                z.write(f, f.relative_to(root).as_posix())
print(out, out.stat().st_size)
PY
