import tkinter as tk
from translator import translate_text_to_sign

class SignTranslatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Text to Sign Language Translator")
        self.geometry("400x250")
        self.configure(bg="#F0E8E8")

        tk.Label(self, text=" Sign Language Translator",
                 font=("Arial", 16, "bold"),
                 bg="#F0E8E8").pack(pady=10)

        self.entry = tk.Entry(self, width=40,
                              font=("Open Sans", 12))
        self.entry.pack(pady=5)

        btn_frame = tk.Frame(self, bg="#f4f4f2")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Translate",
                  font=("Open Sans", 12), bg="#4D1375",
                  fg="#F0E8E8", command=self.on_translate)\
          .grid(row=0, column=0, padx=5)

        tk.Button(btn_frame, text="Clear",
                  font=("Arial", 12), bg="#FD4516",
                  fg="#F0E8E8", command=self.clear_text)\
          .grid(row=0, column=1, padx=5)

        self.status = tk.Label(self, text="",
                               font=("Open Sans", 12),
                               bg="#F0E8E8")
        self.status.pack(pady=10)

    def on_translate(self):
        txt = self.entry.get().strip()
        if not txt:
            tk.messagebox.showwarning("Warning",
                                      "Please enter some text.")
            return
        translate_text_to_sign(txt)

    def clear_text(self):
        self.entry.delete(0, tk.END)
        self.status.config(text="")
