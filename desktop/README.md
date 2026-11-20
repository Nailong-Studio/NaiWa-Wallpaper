# NaiWa Wallpaper · 奶蛙壁纸

一个只做壁纸的桌面客户端。支持 Windows 10/11 和 Linux 桌面。不是浏览器扩展，也不是网页版的换皮。

## 它做什么

- 内置 205 张奶蛙壁纸，离线可用，不联网。
- 按桌面横屏 / 手机竖屏 / 方形 / 4K / 姿势分类筛选，支持标题和来源搜索。
- 选中即看大图；一键设为当前桌面壁纸。
- 收藏、随机一张、下一张、定时自动轮换。
- 素材在本地解码，设置时转成高质量 JPG；不上传、不统计、不登录。

## 运行

### Windows 10/11

解压后双击 `NaiWaWallpaper.exe`。

### Linux 桌面

解压后执行：

```bash
chmod +x NaiWaWallpaper
./NaiWaWallpaper
```

Linux 没有统一的壁纸 API，程序按当前桌面环境选择后端：

| 桌面 | 使用的方式 |
| --- | --- |
| GNOME / Ubuntu / Budgie / Pantheon | `gsettings` |
| Cinnamon | `gsettings` |
| MATE | `gsettings` |
| KDE Plasma | `plasma-apply-wallpaperimage`，找不到时用 `qdbus` / `qdbus6` |
| XFCE | `xfconf-query` |
| Sway | `swaymsg` |
| Hyprland | `hyprctl` + `hyprpaper` |
| 通用 X11 | `feh` 或 `xwallpaper` |

通用 X11 的兜底工具不是系统自带的，Ubuntu 可以装：

```bash
sudo apt install feh
```

纯服务器、容器、没有图形桌面会话的环境只能浏览素材，不能设置壁纸。程序会直接说明缺少哪个后端，不会假装成功。

### 便携包结构

```
NaiWaWallpaper.exe        # Windows
NaiWaWallpaper            # Linux
assets/
  wallpapers/
    list.json
    *.webp
    thumbs/*.webp
README.txt
```

`assets` 必须和可执行文件放在同一层；找不到素材时程序会给出提示，不会静默白屏。

## 开发

需要 .NET 8 SDK：

```bash
cd src
dotnet run
dotnet build -c Release
```

Windows 单文件发布：

```bash
dotnet publish src/NaiWaWallpaper.csproj -c Release -r win-x64 --self-contained true \
  -p:PublishSingleFile=true -p:IncludeNativeLibrariesForSelfExtract=true \
  -p:DebugType=None -o dist/win-x64
```

Linux x64 单文件发布：

```bash
dotnet publish src/NaiWaWallpaper.csproj -c Release -r linux-x64 --self-contained true \
  -p:PublishSingleFile=true -p:IncludeNativeLibrariesForSelfExtract=true \
  -p:DebugType=None -o dist/linux-x64
```

或直接用仓库里的 `build_windows.sh` / `build_linux.sh` 打包。

## 当前范围

- Windows 10/11 与 Linux x64 桌面；单张桌面壁纸模式。
- Linux 按桌面环境适配；通用 X11 需要 `feh` 或 `xwallpaper`。
- 自动轮换需要程序保持运行；关闭程序后停止轮换。
- 素材包是精选 205 张，不包含表情包、视频、音频和低分辨率小图。
- 没有安装器、数字签名、开机自启和托盘常驻；便携包直接运行。

## 测试范围

- Windows 版已完成 x64 交叉编译；界面在 Linux 虚拟显示器实测。
- Linux 版已完成 Ubuntu 22.04 x64 构建；通用 X11 后端在 Xvfb + feh 下验证。
- GNOME / KDE / XFCE / Sway / Hyprland 的后端命令按各桌面标准接口实现，仍需在对应真实桌面会话点一次“设为桌面壁纸”确认。
- Windows 的 `SystemParametersInfoW` 和 Linux 各桌面后端的真实桌面效果，均建议首次运行时人工确认。

## 版本

`v0.0.3`

## 素材与许可

程序代码 MIT。205 张壁纸来自 `Nailong-Studio/NaiWa-Wallpaper` 素材仓，逐件来源和许可见该仓同名 `.txt` 记录。奶蛙是二创角色，原角色权利归其权利人。

## 说明

这是未签名的便携版，首次运行 Windows SmartScreen 可能提示“更多信息”。程序不请求管理员权限，不写系统目录；壁纸缓存只写到当前用户目录：

- Windows：`%LocalAppData%\NaiWaWallpaper`
- Linux：`~/.local/share/NaiWaWallpaper`

## 给五个奶蛙项目点 Star

如果奶蛙桌面帮你省了找壁纸的时间，去 GitHub 给五个项目各点一颗 Star：[素材仓库](https://github.com/Nailong-Studio/NaiWa-Wallpaper)、[艺术圣殿](https://github.com/Nailong-Studio/NaiLoong-Universe)、[新标签页扩展](https://github.com/Nailong-Studio/NaiWa-NewTab)、[像素游戏](https://github.com/Nailong-Studio/naiwa)、[像素表情技能](https://github.com/Nailong-Studio/naiwa-pixel-stickers)。桌面端源码也在素材仓库的 `desktop/` 目录。
