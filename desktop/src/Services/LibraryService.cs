using System.Text.Json;
using NaiWaWallpaper.Models;

namespace NaiWaWallpaper.Services;

public sealed class LibraryService
{
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNameCaseInsensitive = true
    };

    public string Root { get; private init; } = "";
    public string ListPath { get; private init; } = "";
    public IReadOnlyList<WallpaperItem> Items { get; private init; } = [];

    public static LibraryService Load()
    {
        var listPath = FindListPath();
        if (listPath is null)
        {
            throw new FileNotFoundException(
                "找不到 assets/wallpapers/list.json。请把 assets 文件夹放在 NaiWaWallpaper.exe 或 NaiWaWallpaper 旁边。");
        }

        var root = Path.GetDirectoryName(Path.GetDirectoryName(listPath))!;
        var entries = JsonSerializer.Deserialize<List<WallpaperListEntry>>(
            File.ReadAllText(listPath), JsonOptions) ?? [];

        var items = entries
            .Select(entry =>
            {
                var filePath = Path.Combine(root, entry.File);
                var thumbPath = Path.Combine(root, entry.Thumb);
                return new WallpaperItem
                {
                    Key = entry.File,
                    Title = string.IsNullOrWhiteSpace(entry.Title) ? Path.GetFileNameWithoutExtension(entry.File) : entry.Title,
                    Category = entry.Category,
                    CategoryLabel = CategoryLabels.Of(entry.Category),
                    Source = entry.Source,
                    FilePath = filePath,
                    ThumbPath = thumbPath,
                    Width = entry.W,
                    Height = entry.H
                };
            })
            .Where(x => File.Exists(x.FilePath))
            .Where(x => File.Exists(x.ThumbPath))
            .ToList();

        if (items.Count == 0)
        {
            throw new InvalidOperationException("素材清单是空的，或所有图片都缺失。");
        }

        return new LibraryService
        {
            Root = root,
            ListPath = listPath,
            Items = items
        };
    }

    private static string? FindListPath()
    {
        var candidates = new List<string>();
        var processDir = Path.GetDirectoryName(Environment.ProcessPath);
        if (!string.IsNullOrEmpty(processDir))
        {
            candidates.Add(Path.Combine(processDir, "assets", "wallpapers", "list.json"));
            candidates.Add(Path.Combine(processDir, "assets", "list.json"));
        }

        candidates.AddRange(new[]
        {
            Path.Combine(AppContext.BaseDirectory, "assets", "wallpapers", "list.json"),
            Path.Combine(AppContext.BaseDirectory, "assets", "list.json"),
            Path.Combine(Directory.GetCurrentDirectory(), "assets", "wallpapers", "list.json"),
            Path.Combine(Directory.GetCurrentDirectory(), "assets", "list.json")
        });

        // Dev convenience: run from src/bin/... and reach the sibling pack.
        var dir = new DirectoryInfo(AppContext.BaseDirectory);
        for (var i = 0; i < 6 && dir is not null; i++, dir = dir.Parent)
        {
            candidates.Add(Path.Combine(dir.FullName, "assets", "wallpapers", "list.json"));
        }

        return candidates.FirstOrDefault(File.Exists);
    }
}
