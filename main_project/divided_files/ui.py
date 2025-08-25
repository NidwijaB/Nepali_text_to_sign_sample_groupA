import tkinter as tk
from tkinter import messagebox
from translator import translate_text_to_sign
from PIL import Image, ImageTk  # pip install pillow

class SignTranslatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Text to Sign Language Translator")
        self.geometry("450x300")
        self.configure(bg="#F0E8E8")

        tk.Label(self, text=" Sign Language Translator",
                 font=("Arial", 16, "bold"),
                 bg="#F0E8E8").pack(pady=10)

        self.entry = tk.Entry(self, width=40,
                              font=("Open Sans", 12))
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", lambda event: self.on_translate())

        btn_frame = tk.Frame(self, bg="#f4f4f2")
        btn_frame.pack(pady=10)

        # Load icons (replace paths with your actual icon file paths)
        self.icon_translate = tk.PhotoImage(file="icons/translate.png")
        self.icon_clear = tk.PhotoImage(file="icons/clear.png")
        self.icon_info = tk.PhotoImage(file="icons/info.png")
        # Load and resize icons to a consistent size (e.g., 20x20 pixels)
        self.icon_translate = ImageTk.PhotoImage(Image.open("icons/translate.png").resize((20, 20)))
        self.icon_clear = ImageTk.PhotoImage(Image.open("icons/clear.png").resize((20, 20)))
        self.icon_info = ImageTk.PhotoImage(Image.open("icons/info.png").resize((20, 20)))

        tk.Button(btn_frame, text=" Translate", image=self.icon_translate,
                  compound="left", font=("Open Sans", 12), bg="#4D1375",
                  fg="#F0E8E8", command=self.on_translate)\
          .grid(row=0, column=0, padx=5)

        tk.Button(btn_frame, text=" Clear", image=self.icon_clear,
                  compound="left", font=("Arial", 12), bg="#FD4516",
                  fg="#F0E8E8", command=self.clear_text)\
          .grid(row=0, column=1, padx=5)

        tk.Button(btn_frame, text=" Info", image=self.icon_info,
                  compound="left", font=("Arial", 12), bg="#1686FD",
                  fg="#F0E8E8", command=self.toggle_info)\
          .grid(row=0, column=2, padx=5)

        self.status = tk.Label(self, text="",
                               font=("Open Sans", 12),
                               bg="#F0E8E8")
        self.status.pack(pady=10)

        # Collapsible info label — starts hidden
        self.info_visible = False
        self.info_label = tk.Label(self, text="",
                                   font=("Open Sans", 11),
                                   bg="#F0E8E8", fg="#333")

    def on_translate(self):
        txt = self.entry.get().strip()
        if not txt:
            messagebox.showwarning("Warning", "Please enter some text.")
            return
        translate_text_to_sign(txt)

    def clear_text(self):
        self.entry.delete(0, tk.END)
        self.status.config(text="")
        self.info_label.pack_forget()
        self.info_visible = False

    def toggle_info(self):
        if self.info_visible:
            # Hide info
            self.info_label.pack_forget()
            self.info_visible = False
        else:
            # Show info
            creators = "Created by:\n- Alice Johnson\n- Bob Smith\n- Charlie Lee"
            self.info_label.config(text=creators)
            self.info_label.pack(pady=5)
            self.info_visible = True


if __name__ == "__main__":
    app = SignTranslatorApp()
    app.mainloop()
