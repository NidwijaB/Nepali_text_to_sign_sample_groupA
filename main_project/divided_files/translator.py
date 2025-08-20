import os
import json
import string
from moviepy.editor import VideoFileClip
from tkinter import messagebox
from player import play_clips_with_subtitles

CLIP_FOLDER = r"D:\data"
SYN_FILE    = r"C:\Users\user\Documents\PYTHONPROJECTS\Nepali_text_to_sign_sample_groupA\main_project\divided_files\synonyms.json"

print("Using synonyms file:", os.path.abspath(SYN_FILE), "\n")

try:
    with open(SYN_FILE, encoding="utf-8-sig") as f:
        raw = f.read()
    # print("Raw file head:", repr(raw[:100]), "\n")
    data = json.loads(raw)
except Exception as e:
    print("Failed loading synonyms.json:", e)
    data = {}

# print("Loaded keys (raw):", repr(list(data.keys())), "\n")

SYNONYMS = {k.strip().lower(): v for k, v in data.items()}
# print("Normalized keys:", repr(list(SYNONYMS.keys())), "\n")
# print("'khanchu' in SYNONYMS?", "khanchu" in SYNONYMS, "\n")


EXTS = (".m4v", ".mp4", ".wmv")

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
    raw_key  = word
    norm_key = normalize(word)

    if norm_key in SYNONYMS:
        mapped = SYNONYMS[norm_key]
        return mapped

    if norm_key in ALL_KEYS:
        print(f"  ↳ found directly in ALL_KEYS")
        return norm_key

    print(f"  ↳ fallback to norm_key itself")
    return norm_key

def clean_text(text: str) -> list[str]:
    return text.lower().replace(".", "").replace(",", "").split()

def load_clips(words, folder=CLIP_FOLDER):
    clips = []
    exts  = [".m4v", ".wmv", ".mp4"]

    for word in words:
        key  = resolve_clip_key(word)
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
        two = f"{words[i]} {words[i+1]}" if i+1 < len(words) else None
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
