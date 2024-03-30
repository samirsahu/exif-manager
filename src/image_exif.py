from exif import Image

def read_image(file_path: str) -> None:
    print()
    print(f"exif: File: {file_path}")
    with open(file_path, "rb") as img_file:
        img_file: Image = Image(img_file)

        if img_file.has_exif:
            print(f"Exif version: {img_file.exif_version}")
            exif_data = dir(img_file)
            for key in exif_data:
                val = img_file.get(key)
                val = len(val) if key in ["_segments"] else val

                # print(f"{key}: {type(val)}")
                print(f"{key}: {val}")
        else:
            print("No exif found")
