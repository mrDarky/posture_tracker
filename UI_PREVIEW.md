# UI Design

## Design System

The app uses a modern dark theme with density-independent sizing (`dp`/`sp` units) for consistent cross-platform rendering on Windows, macOS, and Linux.

### Color Palette

| Role        | Value (RGBA)               | Usage                             |
|-------------|----------------------------|-----------------------------------|
| Background  | `(0.12, 0.12, 0.14, 1)`   | Window & tab backgrounds          |
| Surface     | `(0.17, 0.17, 0.20, 1)`   | Card containers                   |
| Input       | `(0.22, 0.22, 0.26, 1)`   | Text fields, spinners, list rows  |
| Accent      | `(0.25, 0.56, 1.0, 1)`    | Primary buttons                   |
| Good        | `(0.18, 0.80, 0.44, 1)`   | Good-posture status, start button |
| Bad         | `(0.91, 0.30, 0.24, 1)`   | Bad-posture status, stop button   |
| Scanning    | `(1.0, 0.76, 0.03, 1)`    | In-progress indicators            |
| Text        | `(0.93, 0.93, 0.95, 1)`   | Primary text                      |
| Text Muted  | `(0.55, 0.55, 0.60, 1)`   | Labels, descriptions              |

### Reusable Widget Classes

Defined in `posture_tracker.kv`:

- **`Card`** — rounded `dp(12)` container with surface background
- **`ModernButton`** — rounded `dp(10)` button with accent color
- **`AccentButton`** — green variant for positive actions
- **`DangerButton`** — red variant for stop/danger actions
- **`ModernSpinner`** — styled dropdown on dark input surface
- **`ModernTextInput`** — styled text field on dark input surface

### Adaptive Layout

- **Minimum window**: 480 × 400 px — prevents layout collapse
- **Default window**: 800 × 600 px
- All sizing uses `dp()` / `sp()` units for DPI-aware rendering
- Cards and buttons scale with window size via `size_hint`
- Scrollable camera list adapts to available space

## Camera Tab

```
┌──────────────────────────────────────────────────────┐
│  [ Camera ]  [ Settings ]                            │
├──────────────────────────────────────────────────────┤
│  ╭──────────────────────────────────────────────╮    │
│  │ Camera:   [ Camera 0              ▾ ]        │    │
│  ╰──────────────────────────────────────────────╯    │
│                                                      │
│  ╭──────────────────────────────────────────────╮    │
│  │                                              │    │
│  │          (live camera feed area)             │    │
│  │                                              │    │
│  │  Tilt:  12.3°              Good Posture      │    │
│  ╰──────────────────────────────────────────────╯    │
│                                                      │
│  [ ● Start Tracking ]    [ ■ Stop Tracking ]         │
│    (green, rounded)        (red, rounded)            │
└──────────────────────────────────────────────────────┘
```

## Settings Tab

```
┌──────────────────────────────────────────────────────┐
│  [ Camera ]  [ Settings ]                            │
├──────────────────────────────────────────────────────┤
│  Settings                                            │
│                                                      │
│  ╭──────────────────────────────────────────────╮    │
│  │  Tilt Threshold                              │    │
│  │  Degrees:  [ 15.0                  ]         │    │
│  │  Lower = stricter · Higher = lenient         │    │
│  │  Recommended: 10–20 degrees                  │    │
│  ╰──────────────────────────────────────────────╯    │
│                                                      │
│  ╭──────────────────────────────────────────────╮    │
│  │  Camera Management                           │    │
│  │  [ Refresh Cameras ]  Found 2 camera(s)      │    │
│  │  ┌──────────────────────────────────────┐    │    │
│  │  │ ● Camera 0 ★ — 640×480  [Test][Def] │    │    │
│  │  │ ● Camera 1   — 1280×720 [Test][Def] │    │    │
│  │  │ ○ Camera 2   — unavail  [   ][   ]  │    │    │
│  │  └──────────────────────────────────────┘    │    │
│  ╰──────────────────────────────────────────────╯    │
│                                                      │
│  [ Save Settings ]                                   │
│  Settings saved! Threshold: 15.0°                    │
└──────────────────────────────────────────────────────┘
```

## Status Indicators

| Symbol | Meaning                                 |
|--------|-----------------------------------------|
| `●`    | Camera available and working             |
| `○`    | Camera unavailable                       |
| `★`    | Default camera                           |
| Green  | Good posture / success                   |
| Red    | Bad posture / error                      |
| Yellow | Scanning / in-progress                   |

## Cross-Platform Notes

- Uses Kivy framework — runs natively on Windows, macOS, and Linux
- `dp()` and `sp()` units adapt to screen DPI automatically
- Minimum window size prevents broken layouts on small screens
- No platform-specific fonts or assets required
