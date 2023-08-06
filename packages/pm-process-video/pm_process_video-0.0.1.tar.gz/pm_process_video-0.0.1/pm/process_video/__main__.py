from argparse import ArgumentParser
from pathlib import Path

from . import process_video


def main():
    # Parse arguments
    parser = ArgumentParser()
    parser.add_argument("video_file", type=Path)
    parser.add_argument(
        "--target-dir",
        type=Path,
        default=Path("~/Documents/screencasts/encoded").expanduser(),
    )
    parser.add_argument("--optimize", action="store_true")
    args = parser.parse_args()
    process_video(args.video_file, args.target_dir, optimize=args.optimize)


if __name__ == "__main__":
    main()
