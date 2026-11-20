using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using Avalonia.Media.Imaging;
using Avalonia.Threading;
using NaiWaWallpaper.Models;
using NaiWaWallpaper.Services;

namespace NaiWaWallpaper.ViewModels;

public sealed class MainViewModel : INotifyPropertyChanged
{
    private readonly StateStore _store;
    private readonly AppState _state;
    private string _search;
    private string _category;
    private bool _favoritesOnly;
    private WallpaperItem? _selected;
    private string _status;
    private CancellationTokenSource? _previewCts;

    public MainViewModel(LibraryService library, StateStore store, AppState state)
    {
        Library = library;
        _store = store;
        _state = state;
        _search = state.Search;
        _category = state.Category;
        _status = "本地素材 · 离线可用";

        AllItems = library.Items.ToList();
        foreach (var item in AllItems)
        {
            item.IsFavorite = state.Favorites.Contains(item.Key);
        }

        Visible = [];
        Refresh();
        if (Selected is null && Visible.Count > 0) Selected = Visible[0];
    }

    public LibraryService Library { get; }
    public IReadOnlyList<WallpaperItem> AllItems { get; }
    public ObservableCollection<WallpaperItem> Visible { get; }

    public string Search
    {
        get => _search;
        set
        {
            if (_search == value) return;
            _search = value ?? "";
            _state.Search = _search;
            OnPropertyChanged();
            Refresh();
        }
    }

    public string Category
    {
        get => _category;
        set
        {
            if (_category == value) return;
            _category = value;
            _state.Category = _category;
            OnPropertyChanged();
            Refresh();
        }
    }

    public bool FavoritesOnly
    {
        get => _favoritesOnly;
        set
        {
            if (_favoritesOnly == value) return;
            _favoritesOnly = value;
            OnPropertyChanged();
            Refresh();
        }
    }

    public WallpaperItem? Selected
    {
        get => _selected;
        set
        {
            if (ReferenceEquals(_selected, value)) return;
            if (_selected is not null) _selected.Preview = null;
            _selected = value;
            _state.CurrentKey = value?.Key;
            OnPropertyChanged();
            OnPropertyChanged(nameof(HasSelection));
            OnPropertyChanged(nameof(FavoriteButtonText));
            _ = LoadPreviewAsync(value);
        }
    }

    public bool HasSelection => Selected is not null;

    public string FavoriteButtonText => Selected?.FavoriteGlyph ?? "☆ 收藏";

    public string Status
    {
        get => _status;
        set
        {
            if (_status == value) return;
            _status = value;
            OnPropertyChanged();
        }
    }

    public string CountText => $"{Visible.Count} / {AllItems.Count} 张";

    public string LibraryName => "奶蛙壁纸库";

    public int FavoriteCount => AllItems.Count(x => x.IsFavorite);

    public int CountOf(string category) => category switch
    {
        "all" => AllItems.Count,
        "favorites" => FavoriteCount,
        _ => AllItems.Count(x => x.Category == category)
    };

    public bool IsEmpty => Visible.Count == 0;

    public string EmptyTitle => FavoritesOnly ? "还没有收藏" : "没有匹配的壁纸";

    public string EmptyBody => FavoritesOnly
        ? "在任意一张壁纸上点“收藏”，它就会留在这里。"
        : "换一个关键词，或回到“全部壁纸”。";

    public async Task LoadThumbnailsAsync()
    {
        using var gate = new SemaphoreSlim(6);
        var tasks = AllItems.Select(async item =>
        {
            await gate.WaitAsync();
            try
            {
                var bmp = await Task.Run(() => new Bitmap(item.ThumbPath));
                await Dispatcher.UIThread.InvokeAsync(() => item.Thumb = bmp);
            }
            catch
            {
                // A missing thumbnail must not stop the rest of the grid.
            }
            finally
            {
                gate.Release();
            }
        });

        await Task.WhenAll(tasks);
    }

    public void Refresh()
    {
        var keyword = (_search ?? "").Trim();
        IEnumerable<WallpaperItem> query = AllItems;

        if (_category != "all")
        {
            query = query.Where(x => x.Category == _category);
        }

        if (FavoritesOnly)
        {
            query = query.Where(x => x.IsFavorite);
        }

        if (keyword.Length > 0)
        {
            query = query.Where(x =>
                x.Title.Contains(keyword, StringComparison.OrdinalIgnoreCase) ||
                x.CategoryLabel.Contains(keyword, StringComparison.OrdinalIgnoreCase) ||
                x.Source.Contains(keyword, StringComparison.OrdinalIgnoreCase));
        }

        var ordered = query.ToList();
        Visible.Clear();
        foreach (var item in ordered) Visible.Add(item);

        OnPropertyChanged(nameof(CountText));
        OnPropertyChanged(nameof(FavoriteCount));
        OnPropertyChanged(nameof(IsEmpty));
        OnPropertyChanged(nameof(EmptyTitle));
        OnPropertyChanged(nameof(EmptyBody));

        if (Visible.Count == 0) Status = "没有匹配的壁纸。";

        if (Selected is not null && !Visible.Contains(Selected))
        {
            Selected = Visible.FirstOrDefault();
        }
        else if (Selected is null && Visible.Count > 0)
        {
            Selected = Visible[0];
        }
    }

    public void ToggleFavorite()
    {
        if (Selected is null) return;
        Selected.IsFavorite = !Selected.IsFavorite;
        if (Selected.IsFavorite)
        {
            if (!_state.Favorites.Contains(Selected.Key)) _state.Favorites.Add(Selected.Key);
            Status = "已收藏。";
        }
        else
        {
            _state.Favorites.Remove(Selected.Key);
            Status = "已取消收藏。";
        }

        OnPropertyChanged(nameof(FavoriteButtonText));
        OnPropertyChanged(nameof(FavoriteCount));
        if (FavoritesOnly) Refresh();
        _store.Save(_state);
    }

    public WallpaperItem? SelectRandom()
    {
        if (Visible.Count == 0) return null;
        var next = Visible[Random.Shared.Next(Visible.Count)];
        Selected = next;
        return next;
    }

    public WallpaperItem? SelectNext()
    {
        if (Visible.Count == 0) return null;
        var index = Selected is null ? -1 : Visible.IndexOf(Selected);
        var next = Visible[(index + 1 + Visible.Count) % Visible.Count];
        Selected = next;
        return next;
    }

    public async Task SetWallpaperAsync()
    {
        if (Selected is null)
        {
            Status = "先选一张壁纸。";
            return;
        }

        Status = "正在处理图片…";
        var result = await WallpaperService.SetAsync(Selected.FilePath);
        Status = result.Message;
        if (result.Success)
        {
            _state.CurrentKey = Selected.Key;
            _store.Save(_state);
        }
    }

    public void SaveState() => _store.Save(_state);

    private async Task LoadPreviewAsync(WallpaperItem? item)
    {
        _previewCts?.Cancel();
        _previewCts = new CancellationTokenSource();
        var token = _previewCts.Token;
        if (item is null) return;

        // Show the small image immediately, then replace with the original.
        item.Preview ??= item.Thumb;
        try
        {
            var full = await Task.Run(() => new Bitmap(item.FilePath), token);
            if (token.IsCancellationRequested || !ReferenceEquals(Selected, item)) return;
            await Dispatcher.UIThread.InvokeAsync(() => item.Preview = full);
        }
        catch (OperationCanceledException)
        {
        }
        catch
        {
            // Keep the thumbnail if the original cannot be decoded.
        }
    }

    public event PropertyChangedEventHandler? PropertyChanged;

    private void OnPropertyChanged([CallerMemberName] string? name = null)
        => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
}
