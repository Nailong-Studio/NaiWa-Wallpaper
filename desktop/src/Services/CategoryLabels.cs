namespace NaiWaWallpaper.Services;

public static class CategoryLabels
{
    public static string Of(string category) => category switch
    {
        "desktop" => "桌面横屏",
        "vertical" => "手机竖屏",
        "square" => "方形大图",
        "4k" => "4K 巨幕",
        "poses" => "姿势壁纸",
        _ => category
    };
}
