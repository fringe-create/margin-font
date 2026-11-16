# Margin 1.000

A personal monospaced font family for Margin contributors's apps.

## Quick start for web apps

Copy the `web` directory to your app's public assets. Load `margin.css`:

```html
<link rel="stylesheet" href="/fonts/margin/margin.css">
```

```css
body {
  font-family: 'Margin', ui-monospace, monospace;
  font-weight: 400;
  font-size: 16px;
  line-height: 1.6;
  font-synthesis: none;
}
h1, h2 { font-weight: 500; letter-spacing: -0.025em; }
button, input, textarea, select { font: inherit; }
em { font-style: italic; }
strong { font-weight: 700; }
```

Use standard `font-weight` values between 200 and 900. Use `font-style: italic` for the separately drawn italic. Do not load both the variable files and static files as duplicate faces.

## Included styles

| Weight | Name | Upright | Italic |
|---|---|---|---|
| 200 | ExtraLight | Yes | Yes |
| 300 | Light | Yes | Yes |
| 400 | Regular | Yes | Yes |
| 500 | Medium | Yes | Yes |
| 600 | SemiBold | Yes | Yes |
| 700 | Bold | Yes | Yes |
| 800 | ExtraBold | Yes | Yes |
| 900 | Black | Yes | Yes |

There is no Thin 100 style. The supported range is 200 to 900.

- `web/`: Two variable WOFF2 files and CSS. Use for web apps.
- `fonts/variable/`: Two variable TTF files. Use when your platform supports variable fonts.
- `fonts/static/`: Sixteen static TTF files. Use for native apps, design tools, or platforms that require individual styles.
- `preview.html`: Offline specimen with a size control, weight control, upright and italic choice, and all sixteen styles.
- `source/`: Build script and original font inputs.
- `validation.json`: Build and rendering checks.

## Native apps

For iOS, add the selected static TTF files to the app target and list their filenames in `UIAppFonts`. Select them with their PostScript names, for example `Margin-Regular`, `Margin-Medium`, `Margin-Bold`, and `Margin-Italic`. In SwiftUI: `.font(.custom("Margin-Regular", size: 16))`. Use explicit names for each desired style. For Android, place static files in `res/font` with lowercase underscore filenames and declare weight/style in a font-family XML resource. For React Native or Expo, load each selected static face and map it to the corresponding weight/style in your app's font setup.

Desktop menus may group intermediate static weights as separate legacy families, such as Margin Medium. Typographic family metadata groups them as Margin in applications that support it.

## Design

The Precise direction informed this build. Margin uses a 564-unit cell, compared with the upstream font's 600-unit cell. The outlines are 6% narrower. The dot has a chamfered shape, which also affects punctuation built from it. The R has a small outward extension on its lower leg. Original dotted-zero and character distinctions remain. Italics come from original italic masters, rather than a simulated slant. All text weights are interpolated from the upstream designed weight range, rather than generated with an outline stroke.

This is a customized derivative of Adobe Source Code Pro, not a typeface drawn entirely from scratch and not a modification of Fragment Mono. Its eight weights and italic masters provide the foundation for a usable first version of Margin. Test it in your app's actual layouts before release, particularly narrow controls, multiline text, and small labels. Monospaced text takes more horizontal room than proportional text.

## Characters

The font retains the upstream character set and OpenType layout tables. It includes English and Spanish, Latin extensions, Greek, and Cyrillic. It is not a universal-script font. Use platform fallbacks for unsupported scripts and emoji. Combining marks have zero advance by design. Most ordinary characters share the fixed advance.

## License

Margin is distributed under the SIL Open Font License 1.1. Keep `OFL.txt` and `NOTICE.txt` with redistributed font files. You can embed it in commercial apps. Your app code does not become subject to the font license. The font itself remains under the OFL. The font may not be sold on its own.

## Rebuild

Install Python dependencies: `pip install 'fonttools[woff]' brotli`. From this directory run `python source/build.py`. The bundled upstream inputs allow offline rebuilding. See `NOTICE.txt` for provenance.
