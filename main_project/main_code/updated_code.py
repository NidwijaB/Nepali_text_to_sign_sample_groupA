from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
from utils.clean_and_tokenize import clean_and_tokenize

#
# def clean_text(text):
#     return text.lower().strip().replace(".", "").replace(",", "").split()

def load_clips(words, folder=r"C:\Users\user\Documents\PYTHONPROJECTS\Nepali_text_to_sign_sample_groupA\signvideos"):
    clips = []
    for word in words:
        path = os.path.join(folder, f"{word}.mp4")
        if os.path.exists(path):
            clips.append(VideoFileClip(path).without_audio())
        else:
            print(f"Clip not found for word: {word}")
    return clips

def translate_text_to_sign(text):
    words = clean_and_tokenize(prompt)
    # words = clean_text(text)
    clips = load_clips(words)
    if clips:
        final = concatenate_videoclips(clips)
        final.preview()

if __name__ == "__main__":
    prompt = input("Enter text to translate to sign language: ")
    translate_text_to_sign(prompt)
