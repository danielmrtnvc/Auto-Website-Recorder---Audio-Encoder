import os
import subprocess

# Define input and output directories
recordings_folder = r"C:\Users\danie\OneDrive\Desktop\FFmpeg Automation\Recordings"
final_folder = r"C:\Users\danie\OneDrive\Desktop\FFmpeg Automation\Final"
audio_file = r"C:\Users\danie\OneDrive\Desktop\FFmpeg Automation\audio.m4a"  # Update with your actual audio file name

# Ensure the Final folder exists
os.makedirs(final_folder, exist_ok=True)

# Loop through all video files in the Recordings folder
for filename in os.listdir(recordings_folder):
    if filename.endswith((".mp4", ".mkv", ".avi")):  # Add more formats if needed
        input_video = os.path.join(recordings_folder, filename)
        output_video = os.path.join(final_folder, filename)

        # FFmpeg command to attach audio
        ffmpeg_cmd = [
            r"C:\ffmpeg\bin\ffmpeg.exe", "-i", input_video, "-i", audio_file,  
            "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", output_video
        ]

        print(f"Processing: {filename} → {output_video}")
        subprocess.run(ffmpeg_cmd, check=True)

print("✅ All videos have been processed and saved to the 'Final' folder!")
