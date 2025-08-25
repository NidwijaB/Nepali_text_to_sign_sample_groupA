import os
import tkinter as tk
from tkinter import ttk
from moviepy.editor import VideoFileClip, concatenate_videoclips
from PIL import Image, ImageTk

CLIP_FOLDER = r"D:\data"


def clean_text(text):
    return text.lower().strip().replace(".", "").replace(",", "").split()


def load_clips(words, folder=CLIP_FOLDER):
    clips = []
    for word in words:
        path = os.path.join(folder, f"{word}.m4v")
        if os.path.exists(path):
            clips.append((word, VideoFileClip(path).without_audio()))
        else:
            print(f"⚠️ Clip not found for word: {word}")
    return clips


def play_video_sequence(clips, video_label, text_label):
    """Play clips one after another in the Tkinter window, updating the text."""

    if not clips:
        return

    word, clip = clips[0]  # First clip
    fps = clip.fps
    delay = int(1000 / fps)

    # Show the word under the video
    text_label.config(text=word.capitalize())

    def update_frame(frame_gen, remaining_clips):
        try:
            frame = next(frame_gen)
            img = Image.fromarray(frame)
            img = img.resize((400, 250))  # Resize for Tkinter
            img_tk = ImageTk.PhotoImage(img)
            video_label.config(image=img_tk)
            video_label.image = img_tk
            video_label.after(delay, update_frame, frame_gen, remaining_clips)
        except StopIteration:
            # Move to next clip
            if remaining_clips:
                next_word, next_clip = remaining_clips[0]
                text_label.config(text=next_word.capitalize())
                next_gen = next_clip.iter_frames(fps=next_clip.fps, dtype="uint8")
                video_label.after(delay, update_frame, next_gen, remaining_clips[1:])
            else:
                video_label.config(image='')
                video_label.image = None
                text_label.config(text="")

    frame_gen = clip.iter_frames(fps=fps, dtype="uint8")
    update_frame(frame_gen, clips[1:])


def translate_text_to_sign():
    text = entry.get()
    words = clean_text(text)
    clips = load_clips(words)
    play_video_sequence(clips, video_label, word_label)


# Tkinter GUI
root = tk.Tk()
root.title("Sign Language Translator")
root.geometry("500x450")

entry = ttk.Entry(root, width=40)
entry.pack(pady=10)

translate_btn = ttk.Button(root, text="Translate", command=translate_text_to_sign)
translate_btn.pack(pady=5)

video_label = ttk.Label(root)
video_label.pack(pady=10)

word_label = ttk.Label(root, font=("Arial", 16), foreground="blue")
word_label.pack(pady=5)

root.mainloop()
