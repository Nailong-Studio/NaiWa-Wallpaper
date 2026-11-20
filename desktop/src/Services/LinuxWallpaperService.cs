using System.Diagnostics;
using System.Linq;

namespace NaiWaWallpaper.Services;

/// <summary>
/// Linux desktops do not share one wallpaper API. Prefer the desktop's own
/// session tool, then a generic X11 root-pixmap setter when no desktop is known.
/// </summary>
public static class LinuxWallpaperService
{
    public static async Task<WallpaperResult> SetAsync(string jpegPath)
    {
        var desktop = GetDesktopId();

        if (desktop.Length > 0)
        {
            if (desktop.Contains("gnome") || desktop.Contains("ubuntu") || desktop.Contains("unity") ||
                desktop.Contains("budgie") || desktop.Contains("pantheon"))
            {
                return await SetGnomeLikeAsync(jpegPath, "org.gnome.desktop.background", "GNOME");
            }

            if (desktop.Contains("cinnamon"))
            {
                return await SetGnomeLikeAsync(jpegPath, "org.cinnamon.desktop.background", "Cinnamon");
            }

            if (desktop.Contains("mate"))
            {
                return await SetMateAsync(jpegPath);
            }

            if (desktop.Contains("kde") || desktop.Contains("plasma"))
            {
                return await SetKdeAsync(jpegPath);
            }

            if (desktop.Contains("xfce"))
            {
                return await SetXfceAsync(jpegPath);
            }

            if (desktop.Contains("sway"))
            {
                return await SetSwayAsync(jpegPath);
            }

            if (desktop.Contains("hyprland"))
            {
                return await SetHyprlandAsync(jpegPath);
            }
        }

        return await SetGenericX11Async(jpegPath);
    }

    private static async Task<WallpaperResult> SetGnomeLikeAsync(string jpegPath, string schema, string name)
    {
        var gsettings = Find("gsettings");
        if (gsettings is null)
        {
            return Fail($"你的 {name} 桌面缺少 gsettings，无法设置壁纸。");
        }

        var uri = new Uri(jpegPath).AbsoluteUri;
        var result = await RunAsync(gsettings, "set", schema, "picture-uri", uri);
        if (!result.Ok)
        {
            return Fail($"gsettings 设置失败：{result.Output}");
        }

        // GNOME uses a separate key for the dark appearance. It is optional on
        // Cinnamon and older GNOME builds, so its failure is not fatal.
        _ = await RunAsync(gsettings, "set", schema, "picture-uri-dark", uri);
        return new WallpaperResult(true, $"已设为桌面壁纸（Linux · {name}）。");
    }

    private static async Task<WallpaperResult> SetMateAsync(string jpegPath)
    {
        var gsettings = Find("gsettings");
        if (gsettings is null)
        {
            return Fail("你的 MATE 桌面缺少 gsettings，无法设置壁纸。");
        }

        var result = await RunAsync(
            gsettings, "set", "org.mate.background", "picture-filename", jpegPath);
        return result.Ok
            ? new WallpaperResult(true, "已设为桌面壁纸（Linux · MATE）。")
            : Fail($"MATE 设置失败：{result.Output}");
    }

    private static async Task<WallpaperResult> SetKdeAsync(string jpegPath)
    {
        var apply = Find("plasma-apply-wallpaperimage");
        if (apply is not null)
        {
            var applied = await RunAsync(apply, jpegPath);
            if (applied.Ok)
            {
                return new WallpaperResult(true, "已设为桌面壁纸（Linux · KDE Plasma）。");
            }
        }

        // Plasma 5/6 also expose a small scripting bridge through qdbus.
        var qdbus = Find("qdbus6") ?? Find("qdbus");
        if (qdbus is not null)
        {
            var uri = new Uri(jpegPath).AbsoluteUri;
            var script =
                "var ds = desktops(); " +
                "for (var i = 0; i < ds.length; i++) { " +
                "var d = ds[i]; " +
                "d.wallpaperPlugin = 'org.kde.image'; " +
                "d.currentConfigGroup = new Array('Wallpaper', 'org.kde.image', 'General'); " +
                $"d.writeConfig('Image', '{EscapeJs(uri)}'); " +
                "}";
            var result = await RunAsync(
                qdbus, "org.kde.plasmashell", "/PlasmaShell",
                "org.kde.PlasmaShell.evaluateScript", script);
            if (result.Ok)
            {
                return new WallpaperResult(true, "已设为桌面壁纸（Linux · KDE Plasma）。");
            }
        }

        return Fail("KDE Plasma 没有找到 plasma-apply-wallpaperimage 或可用的 qdbus。");
    }

    private static async Task<WallpaperResult> SetXfceAsync(string jpegPath)
    {
        var xfconf = Find("xfconf-query");
        if (xfconf is null)
        {
            return Fail("你的 XFCE 桌面缺少 xfconf-query，无法设置壁纸。");
        }

        var list = await RunAsync(xfconf, "-c", "xfce4-desktop", "-l");
        if (!list.Ok)
        {
            return Fail($"读取 XFCE 壁纸属性失败：{list.Output}");
        }

        var properties = list.Output
            .Split('\n', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)
            .Where(x => x.EndsWith("/last-image", StringComparison.OrdinalIgnoreCase))
            .ToList();

        if (properties.Count == 0)
        {
            return Fail("XFCE 没有找到 last-image 属性，无法设置壁纸。");
        }

        var updated = 0;
        foreach (var property in properties)
        {
            var result = await RunAsync(
                xfconf, "-c", "xfce4-desktop", "-p", property, "-s", jpegPath);
            if (result.Ok) updated++;
        }

        return updated > 0
            ? new WallpaperResult(true, "已设为桌面壁纸（Linux · XFCE）。")
            : Fail("XFCE 的 last-image 属性写入失败。");
    }

    private static async Task<WallpaperResult> SetSwayAsync(string jpegPath)
    {
        var swaymsg = Find("swaymsg");
        if (swaymsg is null)
        {
            return Fail("Sway 缺少 swaymsg，无法设置壁纸。");
        }

        var result = await RunAsync(swaymsg, "output", "*", "bg", jpegPath, "fill");
        return result.Ok
            ? new WallpaperResult(true, "已设为桌面壁纸（Linux · Sway）。")
            : Fail($"Sway 设置失败：{result.Output}");
    }

    private static async Task<WallpaperResult> SetHyprlandAsync(string jpegPath)
    {
        var hyprctl = Find("hyprctl");
        if (hyprctl is null)
        {
            return Fail("Hyprland 缺少 hyprctl，无法设置壁纸。");
        }

        // hyprpaper accepts wallpaper spec as ",path"; it is normally running
        // alongside Hyprland. If it is not, the command returns a clear error.
        var result = await RunAsync(hyprctl, "hyprpaper", "wallpaper", "," + jpegPath);
        return result.Ok
            ? new WallpaperResult(true, "已设为桌面壁纸（Linux · Hyprland）。")
            : Fail($"Hyprland/hyprpaper 设置失败：{result.Output}");
    }

    private static async Task<WallpaperResult> SetGenericX11Async(string jpegPath)
    {
        if (Environment.GetEnvironmentVariable("DISPLAY") is null)
        {
            return Fail("当前没有图形桌面会话（DISPLAY/WAYLAND_DISPLAY 未设置），只能浏览，不能设置壁纸。");
        }

        var feh = Find("feh");
        if (feh is not null)
        {
            var result = await RunAsync(feh, "--bg-fill", jpegPath);
            if (result.Ok)
            {
                return new WallpaperResult(true, "已设为桌面壁纸（Linux · 通用 X11 / feh）。");
            }
        }

        var xwallpaper = Find("xwallpaper");
        if (xwallpaper is not null)
        {
            var result = await RunAsync(xwallpaper, "--zoom", jpegPath);
            if (result.Ok)
            {
                return new WallpaperResult(true, "已设为桌面壁纸（Linux · 通用 X11 / xwallpaper）。");
            }
        }

        return Fail(
            "没有检测到可用的 Linux 壁纸后端。请确认已登录桌面；" +
            "通用 X11 需要安装 feh 或 xwallpaper（Ubuntu: sudo apt install feh）。");
    }

    private static string GetDesktopId()
    {
        var values = new[]
        {
            Environment.GetEnvironmentVariable("XDG_CURRENT_DESKTOP"),
            Environment.GetEnvironmentVariable("XDG_SESSION_DESKTOP"),
            Environment.GetEnvironmentVariable("DESKTOP_SESSION"),
            Environment.GetEnvironmentVariable("GDMSESSION")
        };

        return string.Join(" ", values
            .Where(x => !string.IsNullOrWhiteSpace(x))
            .Select(x => x!.Trim()))
            .ToLowerInvariant();
    }

    private static string? Find(string name)
    {
        var path = Environment.GetEnvironmentVariable("PATH");
        if (string.IsNullOrWhiteSpace(path)) return null;

        foreach (var directory in path.Split(Path.PathSeparator, StringSplitOptions.RemoveEmptyEntries))
        {
            var candidate = Path.Combine(directory, name);
            if (File.Exists(candidate)) return candidate;
        }

        return null;
    }

    private static async Task<CommandResult> RunAsync(string executable, params string[] arguments)
    {
        var startInfo = new ProcessStartInfo
        {
            FileName = executable,
            UseShellExecute = false,
            CreateNoWindow = true,
            RedirectStandardOutput = true,
            RedirectStandardError = true
        };
        foreach (var argument in arguments) startInfo.ArgumentList.Add(argument);

        using var process = new Process { StartInfo = startInfo };
        try
        {
            process.Start();
            var stdoutTask = process.StandardOutput.ReadToEndAsync();
            var stderrTask = process.StandardError.ReadToEndAsync();

            using var timeout = new CancellationTokenSource(TimeSpan.FromSeconds(10));
            try
            {
                await process.WaitForExitAsync(timeout.Token);
            }
            catch (OperationCanceledException)
            {
                try { process.Kill(true); } catch { }
                await process.WaitForExitAsync();
                return new CommandResult(false, "命令超时。");
            }

            var output = ((await stdoutTask) + "\n" + (await stderrTask)).Trim();
            return new CommandResult(process.ExitCode == 0, output);
        }
        catch (Exception ex)
        {
            return new CommandResult(false, ex.Message);
        }
    }

    private static string EscapeJs(string value)
        => value.Replace("\\", "\\\\").Replace("'", "\\'");

    private static WallpaperResult Fail(string message)
        => new WallpaperResult(false, message);

    private readonly record struct CommandResult(bool Ok, string Output);
}
