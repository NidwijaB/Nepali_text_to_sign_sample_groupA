from moviepy.editor import VideoFileClip, concatenate_videoclips

import os
from utils.clean_and_tokenize import clean_and_tokenize

CLIP_FOLDER = r"C:\Users\user\Documents\PYTHONPROJECTS\KE\text_to_sign\signvideos"

def get_clip_for_word(word):
    filename = f"{word.lower()}.mp4"
    path = os.path.join(CLIP_FOLDER, filename)
    if os.path.exists(path):
        return VideoFileClip(path)
    else:
        print(f"Clip for '{word}' not found.")
        return None

def translate_text_to_sign(prompt):
    words = clean_and_tokenize(prompt)
    clips = []

    for word in words:
        clip = get_clip_for_word(word)
        if clip:
            clips.append(clip)

    if not clips:
        print("No clips found for any of the words.")
        return

    final_clip = concatenate_videoclips(clips)
    final_clip.preview()  # plays the video

if __name__ == "__main__":
    input_text = input("Enter text to translate to sign language: ")
    translate_text_to_sign(input_text)
