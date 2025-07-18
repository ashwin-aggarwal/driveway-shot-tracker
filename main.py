import os
import argparse
from utils.ffmpeg_utils import clean_video  
from detector import run_detection


def main():
    parser = argparse.ArgumentParser(description="Basketball Shot Detector Pipeline")
    parser.add_argument("--input", required=True, help="Path to input video file")
    parser.add_argument("--output", help="Path to save cleaned video (optional)")
    args = parser.parse_args()

    input_path = args.input

    # If no output path provided, auto-generate it
    if args.output:
        output_path = args.output
    else:
        directory, filename = os.path.split(input_path)
        cleaned_name = "cleaned_" + filename
        output_path = os.path.join(directory, cleaned_name)

    # Step 1: Clean the input video using FFmpeg
    print("🔄 Cleaning video...")
    clean_video(input_path, output_path)

    # Step 2: Run detection on the cleaned video
    print("🏀 Running basketball shot detection...")
    run_detection(output_path)

if __name__ == "__main__":
    main()