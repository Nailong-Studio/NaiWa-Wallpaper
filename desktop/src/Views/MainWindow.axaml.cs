using System.Diagnostics;
using System.IO;
using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Markup.Xaml;
using Avalonia.Media;
using Avalonia.Threading;
using NaiWaWallpaper.Models;
using NaiWaWallpaper.Services;
using NaiWaWallpaper.ViewModels;

namespace NaiWaWallpaper.Views;

public sealed partial class MainWindow : Window
{
    private readonly DispatcherTimer _timer = new();
    private MainViewModel? _vm;
    private AppState? _state;
    private bool _ready;

    public MainWindow()
    {
        InitializeComponent();
        _timer.Tick += OnTimerTick;
        Closing += OnClosing;

        try
        {
            var library = LibraryService.Load();
            var store = new StateStore();
            _state = store.Load();
            _vm = new MainViewModel(library, store, _state);
            DataContext = _vm;
            _ready = true;

            UpdateCounts();
            UpdateCategorySelection();
            UpdateEmpty();

            this.FindControl<TextBox>("SearchBox")!.Text = _vm.Search;
            this.FindControl<ComboBox>("AutoBox")!.SelectedIndex = _state.AutoMinutes switch
            {
                >= 1440 => 3,
                >= 60 => 2,
                >= 30 => 1,
                _ => 0
            };
            ApplyAutoTimer();

            Opened += async (_, _) =>
            {
                await _vm.LoadThumbnailsAsync();
                UpdateCounts();
                UpdateEmpty();
            };
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine(ex);
            _ready = false;
            Content = BuildError(ex);
        }
    }

    private void InitializeComponent() => AvaloniaXamlLoader.Load(this);

    private void OnCategoryClick(object? sender, RoutedEventArgs e)
    {
        if (!_ready || _vm is null || sender is not Button button) return;
        var tag = button.Tag?.ToString() ?? "all";

        if (tag == "favorites")
        {
            _vm.FavoritesOnly = true;
        }
        else
        {
            _vm.FavoritesOnly = false;
            _vm.Category = tag;
        }

        UpdateCategorySelection();
        UpdateEmpty();
    }

    private void OnSearchChanged(object? sender, TextChangedEventArgs e)
    {
        if (!_ready || _vm is null) return;
        _vm.Search = (sender as TextBox)?.Text ?? "";
        UpdateEmpty();
    }

    private void OnSelectionChanged(object? sender, SelectionChangedEventArgs e)
    {
        if (!_ready || _vm is null) return;
        if (this.FindControl<ListBox>("WallList")?.SelectedItem is WallpaperItem item)
        {
            _vm.Selected = item;
            _vm.Status = "已选中 · " + item.DisplayTitle;
        }
        UpdateEmpty();
    }

    private async void OnSetClick(object? sender, RoutedEventArgs e)
    {
        if (_vm is null) return;
        var setButton = this.FindControl<Button>("SetButton");
        if (setButton is not null) setButton.IsEnabled = false;
        try
        {
            await _vm.SetWallpaperAsync();
        }
        finally
        {
            if (setButton is not null) setButton.IsEnabled = true;
        }
    }

    private void OnFavoriteClick(object? sender, RoutedEventArgs e)
    {
        if (_vm is null) return;
        _vm.ToggleFavorite();
        UpdateCounts();
        UpdateCategorySelection();
        UpdateEmpty();
    }

    private void OnRandomClick(object? sender, RoutedEventArgs e)
    {
        if (_vm is null) return;
        var item = _vm.SelectRandom();
        ScrollTo(item);
    }

    private void OnNextClick(object? sender, RoutedEventArgs e)
    {
        if (_vm is null) return;
        var item = _vm.SelectNext();
        ScrollTo(item);
    }

    private void OnAutoChanged(object? sender, SelectionChangedEventArgs e)
    {
        if (!_ready || _vm is null || _state is null) return;
        var autoBox = this.FindControl<ComboBox>("AutoBox");
        _state.AutoMinutes = new[] { 0, 30, 60, 1440 }[Math.Max(0, autoBox?.SelectedIndex ?? 0)];
        _vm.SaveState();
        ApplyAutoTimer();
    }

    private void ApplyAutoTimer()
    {
        _timer.Stop();
        if (_state is null || _state.AutoMinutes <= 0) return;
        _timer.Interval = TimeSpan.FromMinutes(_state.AutoMinutes);
        _timer.Start();
    }

    private async void OnTimerTick(object? sender, EventArgs e)
    {
        if (_vm is null) return;
        var item = _vm.SelectRandom();
        ScrollTo(item);
        await _vm.SetWallpaperAsync();
    }

    private async void OnOpenFolder(object? sender, RoutedEventArgs e)
    {
        if (_vm is null) return;
        try
        {
            var path = _vm.Library.Root;
            if (OperatingSystem.IsWindows())
            {
                await Task.Run(() => Process.Start(new ProcessStartInfo("explorer.exe", path) { UseShellExecute = true }));
            }
            else
            {
                await Task.Run(() => Process.Start(new ProcessStartInfo("xdg-open", path) { UseShellExecute = true }));
            }
        }
        catch (Exception ex)
        {
            _vm.Status = "打不开目录：" + ex.Message;
        }
    }

    private void ScrollTo(WallpaperItem? item)
    {
        if (item is null) return;
        var list = this.FindControl<ListBox>("WallList");
        if (list is null) return;
        list.SelectedItem = item;
        list.ScrollIntoView(item);
    }

    private void UpdateCounts()
    {
        if (_vm is null) return;
        var catAll = this.FindControl<Button>("CatAll");
        var catDesktop = this.FindControl<Button>("CatDesktop");
        var catVertical = this.FindControl<Button>("CatVertical");
        var catSquare = this.FindControl<Button>("CatSquare");
        var cat4k = this.FindControl<Button>("Cat4k");
        var catPoses = this.FindControl<Button>("CatPoses");
        var catFav = this.FindControl<Button>("CatFav");
        if (catAll is null || catDesktop is null || catVertical is null || catSquare is null ||
            cat4k is null || catPoses is null || catFav is null)
        {
            return;
        }
        catAll.Content = $"全部壁纸  ·  {_vm.CountOf("all")}";
        catDesktop.Content = $"桌面横屏  ·  {_vm.CountOf("desktop")}";
        catVertical.Content = $"手机竖屏  ·  {_vm.CountOf("vertical")}";
        catSquare.Content = $"方形大图  ·  {_vm.CountOf("square")}";
        cat4k.Content = $"4K 巨幕  ·  {_vm.CountOf("4k")}";
        catPoses.Content = $"姿势壁纸  ·  {_vm.CountOf("poses")}";
        catFav.Content = $"我的收藏  ·  {_vm.FavoriteCount}";
    }

    private void UpdateCategorySelection()
    {
        if (_vm is null) return;
        var favorites = _vm.FavoritesOnly;
        SetClass("CatFav", favorites);
        SetClass("CatAll", !favorites && _vm.Category == "all");
        SetClass("CatDesktop", !favorites && _vm.Category == "desktop");
        SetClass("CatVertical", !favorites && _vm.Category == "vertical");
        SetClass("CatSquare", !favorites && _vm.Category == "square");
        SetClass("Cat4k", !favorites && _vm.Category == "4k");
        SetClass("CatPoses", !favorites && _vm.Category == "poses");
    }

    private void SetClass(string name, bool selected)
    {
        var button = this.FindControl<Button>(name);
        if (button is null) return;
        if (selected) button.Classes.Add("selected");
        else button.Classes.Remove("selected");
    }

    private void UpdateEmpty()
    {
        if (_vm is null) return;
        var emptyPanel = this.FindControl<StackPanel>("EmptyPanel");
        var emptyTitle = this.FindControl<TextBlock>("EmptyTitle");
        var emptyBody = this.FindControl<TextBlock>("EmptyBody");
        var detailPanel = this.FindControl<Border>("DetailPanel");
        if (emptyPanel is null || emptyTitle is null || emptyBody is null || detailPanel is null) return;
        emptyPanel.IsVisible = _vm.IsEmpty;
        detailPanel.IsVisible = _vm.HasSelection;
        emptyTitle.Text = _vm.EmptyTitle;
        emptyBody.Text = _vm.EmptyBody;
    }

    private void OnClosing(object? sender, WindowClosingEventArgs e)
    {
        _vm?.SaveState();
    }

    private Control BuildError(Exception ex)
    {
        var title = new TextBlock
        {
            Text = "素材库没有找到",
            FontSize = 28,
            FontWeight = FontWeight.Black,
            Foreground = Brushes.White
        };
        var body = new TextBlock
        {
            Text = ex.Message + "\n\n请把 assets 文件夹放在 NaiWaWallpaper.exe 或 NaiWaWallpaper 旁边。",
            FontSize = 14,
            Foreground = Brushes.White,
            TextWrapping = TextWrapping.Wrap,
            MaxWidth = 520
        };
        var panel = new StackPanel { Spacing = 12, Margin = new Avalonia.Thickness(40) };
        panel.Children.Add(title);
        panel.Children.Add(body);
        return new Border
        {
            Background = new SolidColorBrush(Color.Parse("#1B1610")),
            Child = panel
        };
    }
}
