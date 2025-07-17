import os
import subprocess
from datetime import datetime, timedelta

def split_video(input_file, timestamp_list, output_dir):
    """
    Args:
        input_file (str): Path to the input video.
        timestamp_list (list of str): List of start times as "HH:MM:SS".
        output_dir (str): Directory to save clips.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, start in enumerate(timestamp_list):
        # Calculate end time by adding 1.5 seconds to start time
        start_time = datetime.strptime(start, "%H:%M:%S")
        end_time = start_time + timedelta(seconds=2)
        end = end_time.strftime("%H:%M:%S")

        output_path = os.path.join(output_dir, f"clip_{i+1:03}.mp4")

        # FFmpeg command
        command = [
            "ffmpeg",
            "-y",
            "-ss", str(start),
            "-to", str(end),
            "-i", input_file,
            "-c:v", "libx264",
            "-preset", "fast",
            "-c:a", "aac",
            "-movflags", "+faststart",
            "-r", "30",
            "-pix_fmt", "yuv420p",
            output_path
        ]

        print(f"🎬 Cutting and encoding clip {i+1}: {start} to {end}")
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# ========= Example Usage =========
if __name__ == "__main__":
    input_video = "videos/shots-collection-zoomed.mp4"  # Replace with your video file path

    timestamps = [
    # ✅ MAKES FIRST
    "00:00:53",  # make
    "00:01:58",  # make
    "00:02:09",  # make
    "00:03:41",  # make
    "00:03:47",  # make
    "00:03:54",  # make
    "00:04:02",  # make
    "00:04:42",  # make
    "00:04:49",  # make

    # ❌ MISSES AFTER
    "00:00:10",  # miss
    "00:00:18",  # miss
    "00:00:28",  # miss
    "00:00:38",  # miss
    "00:01:03",  # miss
    "00:01:10",  # miss
    "00:01:19",  # miss
    "00:01:37",  # miss
    "00:01:47",  # miss
    "00:02:26",  # miss
    "00:02:33",  # miss
    "00:02:43",  # miss
    "00:02:53",  # miss
    "00:03:05",  # miss
    "00:03:14",  # miss
    "00:03:24",  # miss
    "00:03:31",  # miss
    "00:04:12",  # miss
    "00:04:21",  # miss
    "00:04:36",  # miss
    "00:04:56",  # miss
    "00:05:05",  # miss
    "00:05:14",  # miss
]


    output_directory = "outputs/splitclips_from_timestamps/batch2"  # Replace with your desired output directory
    split_video(input_video, timestamps, output_directory)
