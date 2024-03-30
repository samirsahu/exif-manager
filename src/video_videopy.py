from contextlib import closing
from moviepy.editor import VideoFileClip


def read_video_moviepy(file_path: str) -> None:
    print()
    print(f"Moviepy: File: {file_path}")
    with closing(VideoFileClip(file_path)) as video:
        print(video.duration)
        print(video.size)

