import tkinter as tk
import threading
import os

from dotenv import load_dotenv

from tkinter import filedialog, messagebox
from tkinter import ttk

from moviepy.audio.fx.volumex import volumex
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
from elevenlabs import generate, save


class ImporterGUI:
    # Constants

    ENV_PATH = './.env.local'

    FONT = 'Arial'

    VIDEO_EXTENSIONS = ['MP4', 'AVI', 'MOV']

    AUDIO_EXTENSIONS = ['MP3', 'WAV', 'ACC']

    def __init__(self):

        load_dotenv(dotenv_path=self.ENV_PATH)

        self.progress_bar = None
        self.progressLabel = None
        self.progress_window = None
        self.root = tk.Tk()
        self.root.title("Textify")
        self.root.state('zoomed')

        # Variables
        self.currentVideo = tk.StringVar()
        self.currentBackgroundAudio = tk.StringVar()
        self.checkCaption = tk.IntVar()

        # GUI structure
        self.title = tk.Label(self.root, text="Textify", font=(self.FONT, 70))
        self.title.pack(pady=30)

        self.fileLabel = tk.Label(self.root, text="Selected File: ", font=(self.FONT, 16))
        self.fileLabel.pack(side="top", anchor='w', padx=10, pady=20)

        self.selectedFileLabel = tk.Label(self.root, textvariable=self.currentVideo, font=(self.FONT, 16))
        self.selectedFileLabel.pack(side="top", anchor='w', padx=20)

        self.audioLabel = tk.Label(self.root, text="Selected Background Audio: ", font=(self.FONT, 16))
        self.audioLabel.pack(side="top", anchor='w', padx=10, pady=20)

        self.selectedAudioLabel = tk.Label(self.root, textvariable=self.currentBackgroundAudio, font=(self.FONT, 16))
        self.selectedAudioLabel.pack(side="top", anchor='w', padx=20)

        self.textLabel = tk.Label(self.root, text="Write your caption below: ", font=(self.FONT, 16))
        self.textLabel.pack(side="top", anchor='w', padx=10, pady=15)

        self.textbox = tk.Text(self.root, height=10, font=(self.FONT, 16))
        self.textbox.pack(side="top", anchor='w', padx=20, pady=5)

        self.checkbox = tk.Checkbutton(self.root, text="Compile with caption", font=(self.FONT, 16),
                                       variable=self.checkCaption)
        self.checkbox.pack(side="top", anchor='w', padx=20, pady=5)

        # Frame for buttons
        self.buttonFrame = tk.Frame(self.root)
        self.buttonFrame.pack(pady=50, padx=10)

        # Video button
        self.selectVideoButton = tk.Button(self.buttonFrame, text="Video", height=2, width=20, font=(self.FONT, 16),
                                           command=self.selectVideoFile)
        self.selectVideoButton.pack(side="left", padx=5, pady=5)

        # Audio button
        self.selectAudioButton = tk.Button(self.buttonFrame, text="Audio", height=2, width=20, font=(self.FONT, 16),
                                           command=self.selectBackgroundAudioFile)
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
                self.currentVideo.set(file_path.name)
            else:
                messagebox.showerror("Invalid File", "The selected file is not a valid video.")

    def selectBackgroundAudioFile(self):
        file_path = filedialog.askopenfile()
        if file_path:
            if self.checkAudioFormat(file_path.name):
                self.currentBackgroundAudio.set(file_path.name)
            else:
                messagebox.showerror("Invalid File", "The selected file is not a valid audio.")

    def checkVideoFormat(self, file_path):
        return file_path.upper().endswith(tuple(self.VIDEO_EXTENSIONS))

    def checkAudioFormat(self, file_path):
        return file_path.upper().endswith(tuple(self.AUDIO_EXTENSIONS))

    def generate(self):
        if self.currentVideo.get() and self.currentBackgroundAudio.get():
            # Create a pop-up window with a progress bar.
            self.progress_window = tk.Toplevel(self.root)
            self.progress_window.title("Generating Video")
            self.progressLabel = ttk.Label(self.progress_window, text="Please wait, generating video...")
            self.progressLabel.pack(pady=10)
            self.progress_bar = ttk.Progressbar(self.progress_window, orient="horizontal", length=300,
                                                mode="determinate")
            self.progress_bar.pack(padx=10, pady=20)
            self.progress_bar.start()

            threading.Thread(target=self.compose, daemon=True).start()
        else:
            messagebox.showerror("Missing Files", "Please make sure to select at least one video and one audio file.")

    def compose(self):
        try:

            video = VideoFileClip(self.currentVideo.get())
            video_duration = video.duration

            background_audio = AudioFileClip(self.currentBackgroundAudio.get())
            background_audio = volumex(background_audio, 0.5)
            audio_duration = background_audio.duration

            tts_audio = AudioFileClip("C:/Users/nelso/Documents/Projects/Textify/Storage/Results/output_caption.wav")

            if video_duration < audio_duration:
                background_audio = background_audio.set_duration(video_duration)

            combined_audio = CompositeAudioClip([background_audio, tts_audio])

            output = video.set_audio(combined_audio)

            output.write_videofile("C:/Users/nelso/Documents/Projects/Textify/Storage/Results/output_video.mp4",
                                   codec='libx264',
                                   audio_codec='aac')
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            self.progress_bar.stop()
            self.progress_window.destroy()
            messagebox.showinfo("Success", "Video was successfully generated.")

    def tts(self):
        tts = generate(api_key=os.getenv('ELEVEN_LABS_API_KEY'),
                       text="I just want you to know that if you are out there and you are being really hard on yourself right now for something that has happened ... it's normal. That is what is going to happen to you in life. No one gets through unscathed. We are all going to have a few scratches on us. Please be kind to yourselves and stand up for yourself, please",
                       voice="Adam")
        save(tts, "C:/Users/nelso/Documents/Projects/Textify/Storage/Results/output_caption.wav")
