import logging
import exiftool

logger  = logging.getLogger(__name__)

def read_video_exiftool(file_path: str) -> None:
    logger.info("exiftool: Read File: %s", file_path)

    files = [file_path]
    with exiftool.ExifToolHelper() as et:
        metadata: list[dict[any,any]] = et.get_metadata(files)

        for props in metadata:
            # print(d)
            for key in sorted(list(props.keys())):
                if True or "Date" in key:
                    logger.info("Key: %s, Value: %s", key, props.get(key))


def update_video_props(file_path: str, src_file_path: str) -> None:
    print()
    logger.info("exiftool: Update File: %s, Src file: %s", file_path, src_file_path)

    files = [file_path]
    with exiftool.ExifToolHelper() as et:
        src_props_list: list[dict[any,any]] = et.get_metadata(src_file_path)

        for src_props in src_props_list:
            new_tags: dict[str, str] = {}
            for key, val in src_props.items():
                if "Date" in key or "GPS" in key:
                    new_tags[key] = val

        # et.set_tags(files, {"QuickTime:CreateDate": "2023:06:23 16:01:51"})
        et.set_tags(files, new_tags)

