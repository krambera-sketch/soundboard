# Party soundboard

A soundboard website. Your audio files live in the `sounds/` folder, and GitHub Pages turns the repository into a link anyone can open.

## What's in this folder

| File | What it does |
| --- | --- |
| `index.html` | The soundboard page |
| `sounds/` | **Your audio files go here** |
| `board.json` | Optional: title, section order, per-sound tweaks |
| `build_manifest.py` | Builds `sounds.json` (the list of sounds) from the folders |
| `.github/workflows/pages.yml` | Rebuilds and publishes the site whenever you push |

## How your sounds become the board

Folders become sections, files become pads:

```
sounds/
  01 Intros/
    01 airhorn.mp3        -> section "Intros", pad "airhorn"
    02 walk-in.wav
  02 Insults/
    boo.mp3
  laugh.mp3               -> section "Sounds" (files outside a folder)
```

Numbers at the start of a name control the order and are hidden on the page.
MP3, WAV, M4A, OGG, AAC and FLAC all work.

## Put it online (GitHub Pages)

1. Create a GitHub account if you need one, then make a **new public repository** (for example `soundboard`). Free GitHub Pages needs a public repo.
2. Add this folder's contents to the repository. The two easiest ways:
   - **GitHub Desktop** (no command line): add the folder as a local repository, commit, and publish.
   - **Terminal:** from inside this folder run
     ```
     git init -b main
     git add .
     git commit -m "Soundboard"
     git remote add origin https://github.com/YOUR-NAME/soundboard.git
     git push -u origin main
     ```
   Uploading through the GitHub website also works, but hidden folders such as `.github` are easy to miss. If you use it, create the workflow by hand: **Add file > Create new file**, name it `.github/workflows/pages.yml` and paste in the contents of that file.
3. In the repository go to **Settings > Pages** and set **Source** to **GitHub Actions**.
4. Open the **Actions** tab. When "Publish soundboard" finishes (about a minute), your site is at
   `https://YOUR-NAME.github.io/soundboard/`

## Adding or changing sounds later

Drop files into `sounds/` (or a folder inside it) and commit. On the GitHub website: open the `sounds` folder, then **Add file > Upload files**. The site rebuilds itself within a minute or two.
If a replaced file still sounds old, do a hard refresh (Ctrl/Cmd + Shift + R).

## board.json (optional)

```json
{
  "title": "Dave's 40th",
  "sectionOrder": ["Songs", "Intros"],
  "collapsed": ["Insults"],
  "sounds": {
    "Songs/walk-in.mp3": { "name": "Walk-in song", "loop": true, "gain": 0.8, "color": "#ff7ad9" }
  }
}
```

- `sounds` keys are paths inside the `sounds/` folder, exactly as the files are named.
- `gain` is volume for that sound (1 is normal). Without it the page levels each sound automatically.
- `loop` makes a pad repeat until you pause it.
- `color` is any hex color.

## Preview on your laptop

Browsers block a page opened by double-click from reading your audio files, so use a tiny local server:

```
python3 build_manifest.py
python3 -m http.server 8000
```

(on Windows use `py` instead of `python3`), then open http://localhost:8000

## Using the board

- **Click or tap** a pad to play it. Tap it again to pause, tap once more to resume. The "Tap again" menu can switch that to restart or layer instead.
- **W A S D** or the arrow keys move the highlight, **Space** plays or pauses, **Q / E** jump between sections, **P** pauses everything, **Esc** stops everything.
- **Stop all**, **One at a time** and the volume slider are in the top bar. Your volume, theme and which sections are collapsed are remembered on each device.

## Good to know

- The published site is read-only. Changes happen by changing the files in the repository.
- Anyone with the link can open it and hear the sounds. Only upload clips you're comfortable sharing.
- GitHub's website uploader accepts files up to 25 MB; git accepts up to 100 MB. Keep the repository under about 1 GB. Short clips are best, since every sound is loaded when the page opens.
- On iPhone and iPad, switch off the silent switch or you will hear nothing.

## If something looks wrong

- **The page shows "Add your first sound" and upload buttons:** `sounds.json` wasn't found, so the page is running as a personal editor. Check that the Actions run succeeded, or run `build_manifest.py` and commit `sounds.json`.
- **A pad is dimmed with a line through its name:** that file didn't load. Check that it's in `sounds/` and is a normal audio file.
- **"No sounds yet":** the sounds folder is empty or has no supported audio files.
- **Actions run failed:** open the run in the Actions tab and read the red step. A missing `sounds` folder or a typo in `board.json` are the usual causes.
