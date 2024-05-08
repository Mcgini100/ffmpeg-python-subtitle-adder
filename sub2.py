import ffmpeg
import tkinter as tk
from tkinter import filedialog

def select_input_video():
    filename = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv")])
    input_video_entry.delete(0, tk.END)
    input_video_entry.insert(0, filename)

def select_subtitle_file():
    filename = filedialog.askopenfilename(filetypes=[("Subtitle files", "*.srt")])
    subtitle_file_entry.delete(0, tk.END)
    subtitle_file_entry.insert(0, filename)

def select_output_video():
    filename = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("Video files", "*.mp4")])
    output_video_entry.delete(0, tk.END)
    output_video_entry.insert(0, filename)

def add_subtitle_to_video(input_video, subtitle_file, output_video, subtitle_language='eng', soft_subtitle=True):
    """"
    Adds subtitles to a video file

    :param input_video : Path to input video file.
    :param subtitle_file: path to subtitle file in SRT format.
    :param output_video: Path to output video file.
    :param subtitle language: Language of subtitles defualt is 'eng'.
    :param soft_subtitles: Whether to turn on or off subtitles in media palyer. Default is True.
    """

    video_input_stream = ffmpeg.input(input_video)
    subtitle_input_stream = ffmpeg.input(subtitle_file)
    subtitle_track_title = subtitle_file.replace('.srt','')

    if soft_subtitle:
        stream = ffmpeg.output(
            video_input_stream, subtitle_input_stream, output_video, **{'c':'copy', 'c:s': 'mov_text'},
            **{"metadata:s:s:0": f"language={subtitle_language}",
               "metadata:s:s:0": f"title={subtitle_track_title}"}
        )
    else:
        # For hard subtitles, simply copy the video and add the subtitle stream
        stream = ffmpeg.output(video_input_stream, subtitle_input_stream, output_video, c='copy')

    ffmpeg.run(stream, overwrite_output=True)

def process_video():
    input_video = input_video_entry.get()
    subtitle_file = subtitle_file_entry.get()
    output_video = output_video_entry.get()
    subtitle_language = subtitle_language_var.get()
    soft_subtitle = soft_subtitle_var.get()
    add_subtitle_to_video(input_video, subtitle_file, output_video, subtitle_language, soft_subtitle)

#GUI setup
root = tk.Tk()
root.title("subtitle Adder")

#Input video selection
tk.Label(root, text="Input Video:").grid(row=0, column=0)
input_video_entry = tk.Entry(root, width=50)
input_video_entry.grid(row=0, column=1)
tk.Button(root, text="Browse", command=select_input_video).grid(row=0, column=2)

#subtitle file selection
tk.Label(root, text="Subtitle File:").grid(row=1,column=0)
subtitle_file_entry = tk.Entry(root,width=50)
subtitle_file_entry.grid(row=1, column=1)
tk.Button(root, text="Browse", command=select_subtitle_file).grid(row=1, column=2)

#output video selection
tk.Label(root, text="Output File:").grid(row=2, column=0)
output_video_entry = tk.Entry(root, width=50)
output_video_entry.grid(row=2, column=1)
tk.Button(root, text="Browse", command=select_output_video).grid(row=2, column=2)

# Subtitle language selection
tk.Label(root, text="Subtitle Language:").grid(row=3, column=0)
subtitle_language_var = tk.StringVar(value='eng')
subtitle_language_entry = tk.Entry(root, textvariable=subtitle_language_var, width=50)
subtitle_language_entry.grid(row=3, column=1)

# Soft subtitle option
tk.Label(root, text="Soft Subtitles:").grid(row=4, column=0)
soft_subtitle_var = tk.BooleanVar(value=True)
soft_subtitle_check = tk.Checkbutton(root, variable=soft_subtitle_var)
soft_subtitle_check.grid(row=4, column=1)

# Process button
tk.Button(root, text="Add Subtitles", command=process_video).grid(row=5, column=0, columnspan=3)

root.mainloop()

