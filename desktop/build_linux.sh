#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
dotnet publish src/NaiWaWallpaper.csproj -c Release -r linux-x64 --self-contained true \
  -p:PublishSingleFile=true -p:IncludeNativeLibrariesForSelfExtract=true \
  -p:DebugType=None -o dist/linux-x64
rm -rf "dist/NaiWaWallpaper-0.0.3-linux-x64"
mkdir -p "dist/NaiWaWallpaper-0.0.3-linux-x64/assets"
cp dist/linux-x64/NaiWaWallpaper "dist/NaiWaWallpaper-0.0.3-linux-x64/"
chmod +x "dist/NaiWaWallpaper-0.0.3-linux-x64/NaiWaWallpaper"
cp -a assets/wallpapers "dist/NaiWaWallpaper-0.0.3-linux-x64/assets/"
cp README.md SOURCES.md LICENSE CHANGELOG.md preview.png "dist/NaiWaWallpaper-0.0.3-linux-x64/"
cp README.md "dist/NaiWaWallpaper-0.0.3-linux-x64/README.txt"
python3 - <<'PY'
import zipfile, pathlib
root = pathlib.Path('dist/NaiWaWallpaper-0.0.3-linux-x64')
zip_path = pathlib.Path('dist/NaiWaWallpaper-0.0.3-linux-x64.zip')
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for p in sorted(root.rglob('*')):
        if p.is_file():
            z.write(p, p.relative_to(root).as_posix())
print(zip_path, zip_path.stat().st_size)
PY
