#!/usr/bin/env python3
"""
Scans the sounds/ folder and writes sounds.json, the list the website reads.

  sounds/Intros/airhorn.mp3   ->  section "Intros", pad "airhorn"
  sounds/laugh.wav            ->  section "Sounds" (files outside any folder)

Tips
  * Numbers at the start of a name set the order and are hidden:
    "01 Intros" shows as "Intros", "03 big airhorn.mp3" shows as "big airhorn".
  * board.json (optional) sets the title, section order and per-sound tweaks.

Run it yourself with:  python3 build_manifest.py   (use "py" on Windows)
The GitHub workflow runs it automatically on every push.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOUNDS = ROOT / "sounds"
EXTS = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".flac", ".webm", ".opus"}
PALETTE = ["#39ff14", "#a80000", "#ff9f00", "#1b1b1e"]  # toxic green, blood red, pumpkin, black
DEFAULT_SECTION = "Sounds"


def pick_color(placed):
    """Pick a color unlike the pad to the left and, as far as possible, the pads above it.

    The board shows 3 to 6 pads per row depending on screen width, so the pad above
    is 3, 4, 5 or 6 places back.
    """
    i = len(placed)
    left = placed[i - 1] if i else None
    above = [placed[i - k] for k in (3, 4, 5, 6) if i - k >= 0]

    def clashes(color):
        return (10 if color == left else 0) + above.count(color)

    return min(PALETTE, key=lambda c: (clashes(c), (PALETTE.index(c) - i) % len(PALETTE)))


def tidy(name, fallback):
    """'03 big airhorn' -> 'big airhorn' (leading numbers are only for ordering)."""
    cleaned = re.sub(r"^\d+[\s._-]+", "", name).strip()
    return cleaned or name.strip() or fallback


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "x"


def sort_key(text):
    return [int(p) if p.isdigit() else p.lower() for p in re.split(r"(\d+)", text)]


def main():
    board = {}
    board_path = ROOT / "board.json"
    if board_path.exists():
        try:
            board = json.loads(board_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as err:
            sys.exit(f"board.json isn't valid JSON: {err}")
    overrides = board.get("sounds", {})
    collapsed_names = set(board.get("collapsed", []))

    found = []  # (section raw folder or None, rel path, file path)
    if SOUNDS.is_dir():
        for path in SOUNDS.rglob("*"):
            rel = path.relative_to(SOUNDS)
            if not path.is_file() or path.suffix.lower() not in EXTS:
                continue
            if any(part.startswith(".") for part in rel.parts):
                continue
            folder = rel.parts[0] if len(rel.parts) > 1 else None
            found.append((folder, rel, path))
    found.sort(key=lambda f: (f[0] is not None, sort_key(f[0] or ""), sort_key("/".join(f[1].parts[1:] if f[0] else f[1].parts))))

    sections, pads, used_ids = [], [], set()
    by_name = {}
    colors_in = {}  # section name -> colors used so far, in board order
    for folder, rel, path in found:
        sec_name = tidy(folder, DEFAULT_SECTION) if folder else DEFAULT_SECTION
        if sec_name not in by_name:
            sec_id = "s-" + slug(sec_name)
            while sec_id in used_ids:
                sec_id += "x"
            used_ids.add(sec_id)
            by_name[sec_name] = {"id": sec_id, "name": sec_name, "collapsed": sec_name in collapsed_names}
            sections.append(by_name[sec_name])
        rel_posix = rel.as_posix()
        ov = overrides.get(rel_posix, {})
        placed = colors_in.setdefault(sec_name, [])
        color = ov.get("color") or pick_color(placed)
        placed.append(color)
        pad = {
            "id": "f-" + slug(rel_posix)[:40] + "-" + hashlib.md5(rel_posix.encode()).hexdigest()[:4],
            "name": ov.get("name") or tidy(path.stem, "Sound"),
            "color": color,
            "sec": by_name[sec_name]["id"],
            "file": "sounds/" + rel_posix,
            "loop": bool(ov.get("loop", False)),
        }
        if "gain" in ov:
            pad["gain"] = float(ov["gain"])  # otherwise the page levels each sound automatically
        pads.append(pad)

    order = board.get("sectionOrder", [])
    if order:
        sections.sort(key=lambda s: (order.index(s["name"]) if s["name"] in order else len(order)))

    manifest = {"title": board.get("title", "Soundboard"), "sections": sections, "pads": pads}
    (ROOT / "sounds.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"sounds.json written: {len(pads)} sounds in {len(sections)} sections")
    if not pads:
        print("No audio files found yet. Add some to the sounds/ folder.")


if __name__ == "__main__":
    main()
