import os
import logging
from logging.handlers import RotatingFileHandler
from image_exif import read_image
from video_videopy import read_video_moviepy
from video_exiftool import read_video_exiftool, update_video_props
from video_fixer import fix_video_exif

logging.basicConfig(
    handlers=[RotatingFileHandler(
        filename="service.log",
        backupCount=5,
        maxBytes=10*1024*1024 # 10MB
    )],
    encoding='utf-8', level=logging.INFO, 
    format='%(asctime)s: %(levelname)s: %(name)s: %(message)s',
)

base_dir: str = "/app" # Run in Docker container
# base_dir: str = "/Users/sam/Work/CodeProjects/exif-reader" # Run in macos directy


def main() -> None:
    # read_image(f"{base_dir}/data/2023-06-23 19.25.30.jpg")
    # read_video_moviepy(f"{base_dir}/data/2023-07-05 10.25.15.MOV")
    # read_video(f"{base_dir}/data/2023-07-05 10.25.15-fhd.mp4")
    # read_video(f"{base_dir}/data/2023-07-05 10.25.15-4k-hevc.mp4")

    # read_video_exiftool(f"{base_dir}/data/2023-07-05 10.25.15.MOV")
    # read_video_exiftool(f"{base_dir}/data/2023-07-05 10.25.15.mp4")
    # update_video_props(f"{base_dir}/data/2023-07-05 10.25.15.mp4", f"{base_dir}/data/2023-07-05 10.25.15.MOV")
    # print("AFTER UPDATE====")
    # read_video_exiftool(f"{base_dir}/data/2023-07-05 10.25.15.mp4")

    fix_video_exif(os.path.join(base_dir, "data"))


if __name__ == "__main__":
    main()
