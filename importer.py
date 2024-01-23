import tkinter as tk

from tkinter import filedialog


class ImporterGUI:

    def init(self):

        self.root = tk.Tk()
        self.root.title("Textify")
        self.root.geometry("800x500")

        # Variables
        self.currentFile = tk.StringVar()

        # GUI structure

        self.title = tk.Label(self.root, text="Textify", font=('Arial', 40))
        self.title.pack(pady=30)

        self.fileLabel = tk.Label(self.root, text="Selected file: ", font=('Arial', 16))
        self.fileLabel.pack(side="top", anchor='w', padx=10, pady=5)

        self.selectedFileLabel = tk.Label(self.root, textvariable=self.currentFile, font=('Arial', 16))
        self.selectedFileLabel.pack(side="top", anchor='w', padx=10)

        self.root.mainloop()


ImporterGUI()