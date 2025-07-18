#  ffmpeg -i "videos/testvideos/testingvideowithdad.mp4"\
#   -c:v libx264 -preset fast \
#   -c:a aac \
#   -movflags +faststart \
#   -r 30 \
#   -pix_fmt yuv420p \
#   outputs/splitclips_from_timestamps/cleaned_testing_video_withdad.mp4



#   #put this terminal with absolute path to phone video
#   #change the output to whatever u want
#   #it does take a while ~ around the amount of time the video itself is


#    ffmpeg -i "filename"\
#   -c:v libx264 -preset fast \
#   -c:a aac \
#   -movflags +faststart \
#   -r 30 \
#   -pix_fmt yuv420p \
#   outputpath
import subprocess

def clean_video(input_path: str, output_path: str):
    """
    Uses FFmpeg to re-encode a video with settings optimized for OpenCV and YOLO inference.

    Args:
        input_path (str): Path to the input video file.
        output_path (str): Path where the cleaned video will be saved.
    """
    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-c:v", "libx264",
        "-preset", "fast",
        "-c:a", "aac",
        "-movflags", "+faststart",
        "-r", "30",
        "-pix_fmt", "yuv420p",
        output_path
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"✅ FFmpeg: Cleaned video saved to: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg failed: {e}")
