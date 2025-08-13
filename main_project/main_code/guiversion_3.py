import os
import json
import string
import tkinter as tk
from tkinter import messagebox

import pygame
from moviepy.editor import VideoFileClip

# --- CONFIG ---
CLIP_FOLDER = r"D:\data"
SYN_FILE = "synonyms.json"

# Load synonyms
if os.path.exists(SYN_FILE):
    with open(SYN_FILE, "r", encoding="utf-8") as f:
        SYNONYMS = json.load(f)
else:
    SYNONYMS = {}

# Build set of valid clip names from folder + synonym targets
ALL_KEYS = {os.path.splitext(f)[0] for f in os.listdir(CLIP_FOLDER) if f.endswith(".m4v")}
ALL_KEYS.update(SYNONYMS.values())

def normalize(word: str) -> str:
    return word.lower().strip(string.punctuation)

def resolve_clip_key(word: str) -> str:
    """Map token to actual clip filename stem via synonyms or exact match."""
    token = normalize(word)

    #Synonym map
    if token in SYNONYMS:
        return SYNONYMS[token]

    #Exact match
    if token in ALL_KEYS:
        return token

    #No match
    return token

def clean_text(text):
    return text.lower().strip().replace(".", "").replace(",", "").split()

def load_clips(words, folder=CLIP_FOLDER):
    clips = []
    for word in words:
        key = resolve_clip_key(word)

        path = os.path.join(folder, f"{key}.m4v")

        if os.path.exists(path):
            clips.append(VideoFileClip(path).without_audio())
        else:
            try:
                path = os.path.join(folder, f"{key}.wmv")
                clips.append(VideoFileClip(path).without_audio())
            except:
                print(f"Clip not found for '{word}' (resolved as '{key}')")
    return clips

def play_clips_with_subtitles(clip_word_pairs, window_size=(640, 360)):
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(window_size)
    clock = pygame.time.Clock()

    font = pygame.font.SysFont('Arial', 28, bold=True)
    text_color = (255, 231, 255)
    bg_color = (0, 0, 0)

    for word, clip in clip_word_pairs:
        fps = clip.fps
        frame_gen = clip.iter_frames(fps=fps, dtype="uint8")
        for frame in frame_gen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    return
            surf = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            surf = pygame.transform.scale(surf, window_size)
            screen.blit(surf, (0, 0))

            subtitle_surface = font.render(word.capitalize(), True, text_color)
            subtitle_bg = pygame.Surface((subtitle_surface.get_width() + 20, subtitle_surface.get_height() + 10))
            subtitle_bg.fill(bg_color)
            subtitle_bg.set_alpha(150)

            x = (window_size[0] - subtitle_surface.get_width()) // 2
            y = window_size[1] - subtitle_surface.get_height() - 20

            screen.blit(subtitle_bg, (x - 10, y - 5))
            screen.blit(subtitle_surface, (x, y))

            pygame.display.flip()
            clock.tick(fps)

    pygame.quit()

def translate_text_to_sign(text):
    words = clean_text(text)

    # merge two-word phrases if in synonyms
    merged = []
    i = 0
    while i < len(words):
        two = f"{words[i]} {words[i+1]}" if i+1 < len(words) else None
        if two and two in SYNONYMS:
            merged.append(two)
            i += 2
        else:
            merged.append(words[i])
            i += 1

    clips = load_clips(merged)
    clip_word_pairs = list(zip(merged, clips))
    if clip_word_pairs:
        play_clips_with_subtitles(clip_word_pairs, window_size=(800, 450))
    else:
        messagebox.showerror("Error", "No matching sign clips found.")

def on_translate():
    text = entry.get()
    if not text.strip():
        messagebox.showwarning("Warning", "Please enter some text.")
        return
    translate_text_to_sign(text)

def clear_text():
    entry.delete(0, tk.END)
    status_label.config(text="")

# UI
root = tk.Tk()
root.title("Text to Sign Language Translator")
root.geometry("400x250")
root.configure(bg="#f4f4f4")

title_label = tk.Label(root, text=" Sign Language Translator", font=("Arial", 16, "bold"), bg="#f4f4f4")
title_label.pack(pady=10)

entry = tk.Entry(root, width=40, font=("Arial", 12))
entry.pack(pady=5)

btn_frame = tk.Frame(root, bg="#f4f4f4")
btn_frame.pack(pady=10)

translate_btn = tk.Button(btn_frame, text="Translate", font=("Arial", 12), bg="#4CAF50", fg="white", command=on_translate)
translate_btn.grid(row=0, column=0, padx=5)

clear_btn = tk.Button(btn_frame, text="Clear", font=("Arial", 12), bg="#f44336", fg="white", command=clear_text)
clear_btn.grid(row=0, column=1, padx=5)

status_label = tk.Label(root, text="", font=("Arial", 12), bg="#f4f4f4")
status_label.pack(pady=10)

root.mainloop()
