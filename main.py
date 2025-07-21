import os
from utils.ffmpeg_utils import clean_video
from detector import run_detection
from visualizer import plot_make_miss_stats

def main():
    input_path = input("🎥 Enter path to your input video: ").strip()

    # Ensure the input file exists
    if not os.path.exists(input_path):
        print(f"❌ File not found: {input_path}")
        return

    # Generate cleaned output path
    base_name = os.path.basename(input_path)
    cleaned_path = os.path.join("testvideos", "cleaned_" + base_name)

    # Make sure outputs directory exists
    os.makedirs("testvideos", exist_ok=True)

    # Step 1: Clean video using ffmpeg
    clean_video(input_path, cleaned_path)

    # Step 2: Run detection
    makes, misses = run_detection(cleaned_path)

    #Step 3: Visualize results
    plot_make_miss_stats(makes, misses)
    print("✅ Detection and visualization complete!")


if __name__ == "__main__":
    main()