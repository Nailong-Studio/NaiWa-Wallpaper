using System.Runtime.InteropServices;
using SkiaSharp;

namespace NaiWaWallpaper.Services;

public static class WallpaperService
{
    private const uint SpiSetDeskWallpaper = 0x0014;
    private const uint SpifUpdateIniFile = 0x01;
    private const uint SpifSendChange = 0x02;

    public static bool IsSupported => OperatingSystem.IsWindows() || OperatingSystem.IsLinux();

    public static async Task<WallpaperResult> SetAsync(string sourcePath)
    {
        if (!IsSupported)
        {
            return new WallpaperResult(false, "设为桌面壁纸只支持 Windows 10/11 或 Linux 桌面。");
        }

        try
        {
            var prepared = await Task.Run(() => PrepareJpeg(sourcePath));

            if (OperatingSystem.IsLinux())
            {
                return await LinuxWallpaperService.SetAsync(prepared);
            }

            var ok = SystemParametersInfoW(
                SpiSetDeskWallpaper, 0, prepared,
                SpifUpdateIniFile | SpifSendChange);
            if (!ok)
            {
                return new WallpaperResult(false, $"Windows 拒绝了壁纸设置（错误 {Marshal.GetLastWin32Error()}）。");
            }
            return new WallpaperResult(true, "已设为桌面壁纸（Windows）。");
        }
        catch (Exception ex)
        {
            return new WallpaperResult(false, "设置失败：" + ex.Message);
        }
    }

    internal static string PrepareJpeg(string sourcePath)
    {
        var cacheDir = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            "NaiWaWallpaper");
        Directory.CreateDirectory(cacheDir);
        var target = Path.Combine(cacheDir, "current-wallpaper.jpg");

        using var source = SKBitmap.Decode(sourcePath)
            ?? throw new InvalidOperationException("这张图的格式无法解码。");

        using var surface = SKSurface.Create(new SKImageInfo(source.Width, source.Height));
        surface.Canvas.Clear(new SKColor(0x1A, 0x16, 0x10));
        surface.Canvas.DrawBitmap(source, 0, 0);

        using var image = surface.Snapshot();
        using var data = image.Encode(SKEncodedImageFormat.Jpeg, 93);
        using var stream = File.Open(target, FileMode.Create, FileAccess.Write, FileShare.Read);
        data.SaveTo(stream);
        return target;
    }

    [DllImport("user32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
    private static extern bool SystemParametersInfoW(
        uint uiAction, uint uiParam, string pvParam, uint fWinIni);
}

public readonly record struct WallpaperResult(bool Success, string Message);
