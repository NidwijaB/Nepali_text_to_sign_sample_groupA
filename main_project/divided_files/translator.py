import os
import sys
import json
import string
from moviepy.editor import VideoFileClip
from tkinter import messagebox
from player import play_clips_with_subtitles

# Helper to make resources work both in IDE and in PyInstaller exe
def resource_path(relative_path):
    """ Get absolute path to resource (works for dev and for PyInstaller exe) """
    try:
        # PyInstaller extracts files into a temporary folder _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Use relative paths so PyInstaller can bundle them
CLIP_FOLDER = resource_path("data")
SYN_FILE    = resource_path("synonyms.json")

print("Using synonyms file:", os.path.abspath(SYN_FILE), "\n")

# Load synonyms
try:
    with open(SYN_FILE, encoding="utf-8-sig") as f:
        raw = f.read()
    data = json.loads(raw)
except Exception as e:
    print("Failed loading synonyms.json:", e)
    data = {}

SYNONYMS = {k.strip().lower(): v for k, v in data.items()}

# Video extensions
EXTS = (".m4v", ".mp4", ".wmv")

# Collect all available keys
ALL_KEYS = {
    os.path.splitext(fname)[0]
    for fname in os.listdir(CLIP_FOLDER)
    if fname.lower().endswith(EXTS)
}
ALL_KEYS.update(SYNONYMS.values())

print("ALL_KEYS sample:", list(ALL_KEYS)[:10], "\n")


def normalize(word: str) -> str:
    return word.lower().strip(string.punctuation)


def resolve_clip_key(word: str) -> str:
    norm_key = normalize(word)

    if norm_key in SYNONYMS:
        return SYNONYMS[norm_key]

    if norm_key in ALL_KEYS:
        print(f"  ↳ found directly in ALL_KEYS")
        return norm_key

    print(f"  ↳ fallback to norm_key itself")
    return norm_key


def clean_text(text: str) -> list[str]:
    return text.lower().replace(".", "").replace(",", "").split()


def load_clips(words, folder=CLIP_FOLDER):
    clips = []
    exts = [".m4v", ".wmv", ".mp4"]

    for word in words:
        key = resolve_clip_key(word)
        clip = None

        for ext in exts:
            path = os.path.join(folder, f"{key}{ext}")
            if not os.path.exists(path):
                continue

            try:
                clip = VideoFileClip(path).without_audio()
                print(f"Loaded clip: {path}\n")
                break
            except OSError as e:
                print(f"Failed loading {path}: {e}")

        if clip:
            clips.append(clip)
        else:
            print(f"Clip not found for '{word}' → '{key}'\n")

    return clips


def translate_text_to_sign(text: str):
    words = clean_text(text)

    # Merge two-word phrases if defined in synonyms
    merged, i = [], 0
    while i < len(words):
        two = f"{words[i]} {words[i+1]}" if i + 1 < len(words) else None
        if two and two in SYNONYMS:
            merged.append(two)
            i += 2
        else:
            merged.append(words[i])
            i += 1

    clips = load_clips(merged)
    pairs = list(zip(merged, clips))

    if pairs:
        play_clips_with_subtitles(pairs, window_size=(800, 450))
    else:
        messagebox.showerror("Error", "No matching sign clips found.")
