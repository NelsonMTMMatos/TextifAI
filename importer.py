import tkinter as tk

from tkinter import filedialog, messagebox


class ImporterGUI:

    # Constants
    FONT = 'Arial'

    VIDEO_EXTENSIONS = ['MP4', 'AVI', 'MOV']

    AUDIO_EXTENSIONS = ['MP3', 'WAV', 'ACC']

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Textify")
        self.root.state('zoomed')

        # Variables
        self.currentFile = tk.StringVar()
        self.currentAudio = tk.StringVar()

        # GUI structure
        self.title = tk.Label(self.root, text="Textify", font=(self.FONT, 70))
        self.title.pack(pady=30)

        self.fileLabel = tk.Label(self.root, text="Selected file: ", font=(self.FONT, 16))
        self.fileLabel.pack(side="top", anchor='w', padx=10, pady=20)

        self.selectedFileLabel = tk.Label(self.root, textvariable=self.currentFile, font=(self.FONT, 16))
        self.selectedFileLabel.pack(side="top", anchor='w', padx=20)

        self.audioLabel = tk.Label(self.root, text="Selected Audio: ", font=(self.FONT, 16))
        self.audioLabel.pack(side="top", anchor='w', padx=10, pady=20)

        self.selectedAudioLabel = tk.Label(self.root, textvariable=self.currentAudio, font=(self.FONT, 16))
        self.selectedAudioLabel.pack(side="top", anchor='w', padx=20)

        self.textLabel = tk.Label(self.root, text="Write your caption below: ", font=(self.FONT, 16))
        self.textLabel.pack(side="top", anchor='w', padx=10, pady=10)

        self.textbox = tk.Text(self.root, height=10, font=(self.FONT, 16))
        self.textbox.pack(side="top", anchor='w', padx=20, pady=5)

        # Frame for buttons
        self.buttonFrame = tk.Frame(self.root)
        self.buttonFrame.pack(pady=50, padx=10)

        # Video button
        self.selectVideoButton = tk.Button(self.buttonFrame, text="Video", height=2, width=20, font=(self.FONT, 16),
                                           command=self.selectVideoFile)
        self.selectVideoButton.pack(side="left", padx=5, pady=5)

        # Audio button
        self.selectAudioButton = tk.Button(self.buttonFrame, text="Audio", height=2, width=20, font=(self.FONT, 16),
                                           command=self.selectAudioFile)
        self.selectAudioButton.pack(side="left", padx=5, pady=5)

        # Generate button
        self.generateButton = tk.Button(self.root, text="Generate", height=2, width=20, font=(self.FONT, 16),
                                        command=self.generate)
        self.generateButton.pack(pady=5)

        self.root.mainloop()

    def selectVideoFile(self):
        file_path = filedialog.askopenfile()
        if file_path:
            if self.checkVideoFormat(file_path.name):
                self.currentFile.set(file_path.name)
            else:
                messagebox.showerror("Invalid File", "The selected file is not a valid video.")

    def selectAudioFile(self):
        file_path = filedialog.askopenfile()
        if file_path:
            if self.checkAudioFormat(file_path.name):
                self.currentAudio.set(file_path.name)
            else:
                messagebox.showerror("Invalid File", "The selected file is not a valid audio.")

    def checkVideoFormat(self, file_path):
        return file_path.upper().endswith(tuple(self.VIDEO_EXTENSIONS))

    def checkAudioFormat(self, file_path):
        return file_path.upper().endswith(tuple(self.AUDIO_EXTENSIONS))


    def generate(self):
        pass
