import argparse
from datetime import datetime, timezone, tzinfo
import logging
from logging.handlers import RotatingFileHandler
import sys
import image_utils
import video_utils

logging.basicConfig(
    handlers=[RotatingFileHandler(
        filename="service-{:%Y-%m-%dT%H-%M-%S}.log".format(datetime.now()),
        backupCount=10,
        maxBytes=10*1024*1024 # 10MB
    )],
    encoding='utf-8', level=logging.INFO,
    format='%(asctime)s: %(levelname)s: %(name)s: L%(lineno)d: %(message)s',
)

logger = logging.getLogger(__name__)

# base_dir: str = "/app/data" # Run in Docker container
base_dir: str = "/app/mount" # Run in Docker container

# base_dir: str = "/Users/sam/Work/CodeProjects/exif-manager/data" # Run in macos directy
# base_dir: str = "/Volumes/Sam/Pictures/Camera Roll/iPhone Photos"

def main(args: list[str]) -> None:
    parser = setup_args_parser()
    parsed_args = parser.parse_args(args)

    mode = parsed_args.mode
    logger.info("Mode: %s", mode)

    if "read-image-exif" == mode:
        for f in parsed_args.files:
            image_utils.read_image_exif(f"{base_dir}/data/2023-06-23 19.25.30.jpg")
    elif "read-video-exif" == mode:
        video_utils.read_video_exif_moviepy(f"{base_dir}/data/2023-07-05 10.25.15.MOV")
        video_utils.read_video_exif_exiftool(f"{base_dir}/data/2023-07-05 10.25.15.MOV")
    elif "encode-videos" == mode:
        video_utils.encode_videos(base_dir)
    elif "temp" == mode:
        # video_utils.encode_videos(base_dir, max_files=1)
        logger.info(video_utils.encode_video(f"{base_dir}/2015/iPhone 5S", "IMG_0398.MOV"))
        pass
    else:
        raise ValueError("Invalid command")

def setup_args_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="exif-manager",
        description="Bunch of utilities that can be performed on Audio/Video files."
    )
    mode_parser = parser.add_subparsers(dest="mode", required=True)

    sub_parser = mode_parser.add_parser("read-image-exif", help="Read EXIF data for the list of Pictures." )
    sub_parser.add_argument("files", type=str, nargs="+")

    sub_parser = mode_parser.add_parser("read-video-exif", help="Read EXIF data for the list of Videos." )
    sub_parser.add_argument("files", type=str, nargs="+")

    sub_parser = mode_parser.add_parser("encode-videos", help="Encodes all the .MOV videos to .MP4 in the mounted directory recursively" )

    sub_parser = mode_parser.add_parser("temp", help="Some temporary command")
    return parser

if __name__ == "__main__":
    main(sys.argv[1:])
