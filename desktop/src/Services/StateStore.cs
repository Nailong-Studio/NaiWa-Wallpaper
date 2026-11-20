using System.Text.Json;

namespace NaiWaWallpaper.Services;

public sealed class AppState
{
    public List<string> Favorites { get; set; } = [];
    public string Category { get; set; } = "all";
    public string Search { get; set; } = "";
    public int AutoMinutes { get; set; }
    public string? CurrentKey { get; set; }
}

public sealed class StateStore
{
    private static readonly JsonSerializerOptions JsonOptions = new() { WriteIndented = true };
    private readonly string _path;

    public StateStore()
    {
        var dir = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            "NaiWaWallpaper");
        Directory.CreateDirectory(dir);
        _path = Path.Combine(dir, "state.json");
    }

    public AppState Load()
    {
        try
        {
            if (!File.Exists(_path)) return new AppState();
            return JsonSerializer.Deserialize<AppState>(File.ReadAllText(_path), JsonOptions)
                   ?? new AppState();
        }
        catch
        {
            return new AppState();
        }
    }

    public void Save(AppState state)
    {
        try
        {
            File.WriteAllText(_path, JsonSerializer.Serialize(state, JsonOptions));
        }
        catch
        {
            // Preferences are a convenience, never a hard failure.
        }
    }
}
