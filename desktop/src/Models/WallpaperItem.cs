using System.ComponentModel;
using System.Runtime.CompilerServices;
using Avalonia.Media.Imaging;

namespace NaiWaWallpaper.Models;

public sealed class WallpaperItem : INotifyPropertyChanged
{
    private Bitmap? _thumb;
    private Bitmap? _preview;
    private bool _isFavorite;

    public required string Key { get; init; }
    public required string Title { get; init; }
    public required string Category { get; init; }
    public required string CategoryLabel { get; init; }
    public required string Source { get; init; }
    public required string FilePath { get; init; }
    public required string ThumbPath { get; init; }
    public int Width { get; init; }
    public int Height { get; init; }

    public string DisplayTitle => Title.StartsWith("奶蛙-", StringComparison.Ordinal)
        ? Title[3..]
        : Title;

    public string MetaLine => $"{Width} × {Height} · {CategoryLabel}";

    public string Orientation => Width >= Height * 1.5 ? "横屏"
        : Height >= Width * 1.5 ? "竖屏"
        : "近方形";

    public string DetailMeta => $"{Width} × {Height} · {Orientation} · {CategoryLabel}";

    public bool IsFavorite
    {
        get => _isFavorite;
        set
        {
            if (_isFavorite == value) return;
            _isFavorite = value;
            OnPropertyChanged();
            OnPropertyChanged(nameof(FavoriteGlyph));
        }
    }

    public string FavoriteGlyph => IsFavorite ? "★ 已收藏" : "☆ 收藏";

    public Bitmap? Thumb
    {
        get => _thumb;
        set
        {
            _thumb = value;
            OnPropertyChanged();
        }
    }

    public Bitmap? Preview
    {
        get => _preview;
        set
        {
            _preview = value;
            OnPropertyChanged();
        }
    }

    public event PropertyChangedEventHandler? PropertyChanged;

    private void OnPropertyChanged([CallerMemberName] string? name = null)
        => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
}
