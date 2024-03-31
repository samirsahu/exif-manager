import subprocess
import logging
import sys
import os
from contextlib import closing
from typing import Any
import exiftool
from moviepy.editor import VideoFileClip


logger = logging.getLogger(__name__)


def read_video_exif_exiftool(file_path: str) -> None:
    logger.info("read_video_exif_exiftool: Read File: %s", file_path)

    files = [file_path]
    with exiftool.ExifToolHelper() as et:
        metadata: list[dict[any, any]] = et.get_metadata(files)

        for props in metadata:
            for key in sorted(list(props.keys())):
                if True or "Date" in key:
                    logger.info("Key: %s, Value: %s", key, props.get(key))


def read_video_exif_moviepy(file_path: str) -> None:
    logger.info("read_video_exif_moviepy: File: %s", file_path)
    with closing(VideoFileClip(file_path)) as video:
        logger.info("Duration: %s", video.duration)
        logger.info("Size: %s", video.size)


def update_video_exif(file_path: str, src_file_path: str) -> None:
    logger.info("update_video_exif: Update File: %s, Src file: %s", file_path, src_file_path)

    files = [file_path]
    with exiftool.ExifToolHelper() as et:
        src_props_list: list[dict[str, Any]] = et.get_metadata(src_file_path)

        for src_props in src_props_list:
            new_tags: dict[str, str] = {}
            for key, val in src_props.items():
                if "Date" in key or "GPS" in key:
                    new_tags[key] = val

        et.set_tags(files, new_tags)


HANDBRAKE_CLI = "HandBrakeCLI"

# pylint: disable=too-many-locals
def encode_videos(base_dir: str, *, max_files: int = sys.maxsize) -> None:
    logger.info("Fix videos in %s directory. max_files: %d", base_dir, max_files)

    video_file_num: int = 0
    encoded_num: int = 0
    failed_num: int = 0
    skipped_num: int = 0

    for dir_path, dir_names, file_names in os.walk(base_dir): # pylint: disable=unused-variable

        dir_name = os.path.basename(dir_path)
        if dir_name.startswith("@") or dir_name.startswith("."):
            logger.info("Skip directory: %s", dir_path)
            continue

        file_names_set = set(file_names)
        for inp_file_name in file_names:
            inp_file_name_only, inp_file_ext = os.path.splitext(inp_file_name)

            if inp_file_ext.lower() == ".mov":
                logger.info("======================================================")
                try:
                    video_file_num += 1

                    inp_file_path = os.path.join(dir_path, inp_file_name)
                    logger.info("%d. Checking File: %s", video_file_num, inp_file_path)

                    if f"{inp_file_name_only}.mp4" in file_names_set:
                        logger.info("MP4 already exists. Skip")
                        skipped_num += 1
                        continue

                    if f"{inp_file_name}_err" in file_names_set:
                        logger.info("Error file exists. Skip")
                        skipped_num += 1
                        continue
                    
                    out_file_path = encode_video(dir_path, inp_file_name)

                    encoded_num += 1

                    logger.info("Encoding done")
                except IOError:
                    logger.exception("IO Error during processing file %s", inp_file_path)
                    return
                except Exception as exc:  # pylint: disable=broad-exception-caught
                    failed_num += 1
                    logger.exception(exc)
                    if out_file_path:
                        os.remove(out_file_path)
                    with closing(open(f"{inp_file_path}_err", "a", encoding="UTF-8")) as err_file:
                        err_file.write(str(exc))

            if encoded_num >= max_files:
                break

        if encoded_num >= max_files:
            break

    logger.info("Encode status: Success=%d, Failed=%d, Skipped=%d",encoded_num, failed_num, skipped_num)

def encode_video(dir_path: str, inp_file_name: str) -> str:

    inp_file_path = os.path.join(dir_path, inp_file_name)
    inp_file_name_only, inp_file_ext = os.path.splitext(inp_file_name)

    with closing(open(f"{inp_file_path}_wip", "a", encoding="UTF-8")) as wip_file:
        wip_file.write("Working")

    out_file_path = os.path.join(dir_path, f"{inp_file_name_only}.mp4")

    logger.info("Encode %s to %s", inp_file_path, out_file_path)
    encode_rc: int = process_command([
        HANDBRAKE_CLI,
        "-i",
        inp_file_path,
        "-o",
        out_file_path,
    ])
    if encode_rc != 0:
        raise RuntimeError(f"Error trying to encode file. RC: {encode_rc}")

    logger.info("Update EXIF")
    update_video_exif(out_file_path, inp_file_path)

    logger.info("Delete _original file created by EXIF Tool")
    os.remove(os.path.join(dir_path, f"{out_file_path}_original"))
    logger.info("File encoded to %s", out_file_path)

    logger.info("Update timestamps as source file")
    touch_rc = process_command(["touch", "-r", inp_file_path, out_file_path])
    if touch_rc != 0:
        raise RuntimeError(f"Error trying to touch file. RC: {touch_rc}")

    logger.info("Remove WIP file")
    os.remove(f"{inp_file_path}_wip")

    return out_file_path


def process_command(command: list[str]) -> int:
    proc: subprocess.Popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def monitor_process_output(proc: subprocess.Popen):
        while True:
            assert proc.stdout
            output = proc.stdout.readline().decode()
            if output:
                logger.debug(output)
            else:
                break

    while proc.poll() is None:
        monitor_process_output(proc)

    return_code = proc.wait()
    return return_code
