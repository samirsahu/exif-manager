from contextlib import closing
import os
import subprocess
import logging
from video_exiftool import update_video_props

logger = logging.getLogger(__name__)
cli_logger = logging.getLogger(f"{__name__}_cli")

HANDBRAKECLI = "HandBrakeCLI"
def fix_video_exif(base_dir: str) -> None:
    logger.info("Fix videos in %s directory", base_dir)
    for dir_path, dir_names, file_names in os.walk(base_dir): #pylint: disable=unused-variable
        file_names_set = set(file_names)
        for f in file_names:
            inp_file_name, inp_file_ext = os.path.splitext(f)
            if inp_file_ext in (".MOV", ".mov"):
                logger.info("======================================================")
                try:
                    inp_file_path = os.path.join(dir_path,f)
                    logger.info("File: %s", inp_file_path)


                    if f"{inp_file_name}.mp4" in file_names_set:
                        logger.info("MP4 already exists. Skip")
                        continue

                    out_file_path = os.path.join(dir_path, f"{inp_file_name}.mp4")

                    logger.info("Encode %s to %s", inp_file_path, out_file_path)

                    encode_rc: int = process_command([
                        HANDBRAKECLI,
                        "-i", 
                        inp_file_path,
                        "-o", 
                        out_file_path,
                    ])

                    if encode_rc != 0:
                        raise RuntimeError(f"Error trying to encode file. RC: {encode_rc}")

                    logger.info("Update EXIF")
                    update_video_props(out_file_path, inp_file_path)

                    logger.info("Update timestamps")
                    touch_rc = process_command(["touch", "-r", inp_file_path, out_file_path])

                    if touch_rc != 0:
                        raise RuntimeError(f"Error trying to touch file. RC: {touch_rc}")

                    logger.info("Delete _original file created by EXIF Tool")
                    os.remove(os.path.join(dir_path, f"{out_file_path}_original"))
                    logger.info("File encoded to %s", out_file_path)
                except Exception as exc: #pylint: disable=broad-exception-caught
                    logger.exception(exc)
                    with closing(open(f"{inp_file_path}_error", "w", encoding="UTF-8")) as err_file:
                        err_file.write(str(exc))


def process_command(command: list[str]) -> int:
    proc: subprocess.Popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def monitor_process_output(proc: subprocess.Popen):
        while True:
            assert proc.stdout
            output = proc.stdout.readline().decode()
            if output:
                cli_logger.debug(output)
            else:
                break

    while proc.poll() is None:
        monitor_process_output(proc)

    return_code = proc.wait()
    return return_code
