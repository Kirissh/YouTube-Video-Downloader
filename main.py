import tkinter
import customtkinter
import yt_dlp
from PIL import Image, ImageTk
import requests
from io import BytesIO

def update_progress(bar, label, bytes_downloaded, total_size):
    percentage = bytes_downloaded / total_size * 100
    bar.set(percentage / 100)  # Update progress bar
    label.configure(text=f"{int(percentage)}%")  # Update percentage label

def on_progress(d):
    if d['status'] == 'downloading':
        total_size = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
        bytes_downloaded = d.get('downloaded_bytes', 0)
        update_progress(progressBar, pPercentage, bytes_downloaded, total_size)

def fetch_video_info(ytLink):
    try:
        with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
            info_dict = ydl.extract_info(ytLink, download=False)  # Get info without downloading
            video_title = info_dict.get('title', 'Video')
            thumbnail_url = info_dict.get('thumbnail', '')
            return video_title, thumbnail_url
    except Exception as e:
        print(f"Error fetching video info: {e}")
        return None, None

def on_url_change(event):
    ytLink = link.get().strip()
    if ytLink:
        video_title, thumbnail_url = fetch_video_info(ytLink)
        if video_title:
            title.configure(text=video_title, text_color="white")  # Set the title label
            if thumbnail_url:
                try:
                    response = requests.get(thumbnail_url)
                    img_data = Image.open(BytesIO(response.content))
                    img_data.thumbnail((150, 150))  # Resize thumbnail
                    img = ImageTk.PhotoImage(img_data)
                    thumbnail_label.configure(image=img)
                    thumbnail_label.image = img  # Keep a reference to avoid garbage collection
                except Exception as e:
                    print(f"Error loading thumbnail: {e}")
        else:
            title.configure(text="Video info not found", text_color="red")  # Error message

def startDownload():
    try:
        ytLink = link.get().strip()  # Strip any extra spaces
        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(title)s.%(ext)s',  # Save video with title as filename
            'progress_hooks': [on_progress],  # Hook for progress updates
            'quiet': True,  # Suppress verbose output
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([ytLink])  # This downloads the video

        finishLabel.configure(text="Download Complete", text_color="green")  # Success message
    except Exception as e:
        print(f"Error: {e}")
        finishLabel.configure(text="Invalid YouTube Link", text_color="red")  # Error message

# System Settings 
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

# Application Framing
app = customtkinter.CTk()
app.geometry("720x480")
app.title("YouTube Downloader")

# Center the UI elements
frame = customtkinter.CTkFrame(app)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Adding UI 
title = customtkinter.CTkLabel(frame, text="Insert YouTube Link", font=("Arial", 16))
title.pack(padx=10, pady=10)

# Link input 
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(frame, width=450, height=40, textvariable=url_var, placeholder_text="Paste YouTube link here")
link.pack(pady=10)
link.bind("<KeyRelease>", on_url_change)  # Bind key release to fetch video info

# Thumbnail display
thumbnail_label = customtkinter.CTkLabel(frame, text="")
thumbnail_label.pack(pady=10)

# Finished Downloading 
finishLabel = customtkinter.CTkLabel(frame, text="", font=("Arial", 14))
finishLabel.pack(pady=10)

# Progress percentage 
pPercentage = customtkinter.CTkLabel(frame, text="0%", font=("Arial", 14))
pPercentage.pack(pady=10)

progressBar = customtkinter.CTkProgressBar(frame, width=450)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)

# Download button 
download = customtkinter.CTkButton(frame, text="Download", command=startDownload, fg_color="#1f6aa5")
download.pack(pady=20)

# Run app by looping 
app.mainloop()
