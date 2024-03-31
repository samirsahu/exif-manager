import logging
from exif import Image

logger = logging.getLogger(__name__)

def read_image_exif(file_path: str) -> None:
    logger.info("read_image_exif: File: %s", file_path)

    with open(file_path, "rb") as img_file_reader:
        img_file: Image = Image(img_file_reader)

        if img_file.has_exif:
            print(f"Exif version: {img_file.exif_version}")
            exif_data = dir(img_file)
            for key in exif_data:
                val = img_file.get(key)
                val = len(val) if key in ["_segments"] else val

                logger.info("%s: %s", key, val)
        else:
            logger.info("No exif found")
