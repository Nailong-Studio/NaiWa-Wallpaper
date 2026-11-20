namespace NaiWaWallpaper.Models;

public sealed class WallpaperListEntry
{
    public string File { get; set; } = "";
    public string Title { get; set; } = "";
    public string Category { get; set; } = "";
    public int W { get; set; }
    public int H { get; set; }
    public string Source { get; set; } = "";
    public string Thumb { get; set; } = "";
}
