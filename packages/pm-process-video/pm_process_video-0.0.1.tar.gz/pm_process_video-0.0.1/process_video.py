from argparse import ArgumentParser
from concurrent.futures import ProcessPoolExecutor
from os import fsencode
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import sys

from ffmpeg_normalize import FFmpegNormalize
import ffmpeg
import openai


openai.api_key_path = Path.home() / ".openai"


def run(command, *args, **kwargs):
    return subprocess.run(
        [command, *args],
        check=True,
        encoding="utf-8",
        **kwargs,
    )


def normalize_audio_for(video_path, normalized_dir):
    normalized_file = normalized_dir / video_path.name
    ffmpeg_normalize = FFmpegNormalize(audio_codec="aac", audio_bitrate="192k")
    ffmpeg_normalize.add_media_file(video_path, normalized_file)
    ffmpeg_normalize.run_normalization()
    return normalized_file


def generate_captions(video_path, output_directory):
    # Extracting just the audio (for whisper)
    audio_file = output_directory / video_path.with_suffix(".m4a").name
    (
        ffmpeg.input(fsencode(video_path))
        .audio
        .output(fsencode(audio_file), acodec="copy")
        .run()
    )
    with audio_file.open(mode="rb") as binary_audio_file:
        transcript = openai.Audio.transcribe(
            "whisper-1",
            binary_audio_file,
            response_format="vtt",
            language="en",
        )
    subtitles_file = output_directory / video_path.with_suffix(".vtt")
    subtitles_file.write_text(transcript)
    return subtitles_file


def text_from_captions(caption_path):
    print("Generating text transcript for", caption_path)
    # Requires pipx install pm-vtt2txt
    process = run("vtt2txt", caption_path, capture_output=True)
    plain_text = process.stdout

    final_txt_file = caption_path.with_suffix(".txt")
    final_txt_file.write_text(plain_text)
    print("Generated", final_txt_file)
    return final_txt_file


def main():
    # Parse arguments
    parser = ArgumentParser()
    parser.add_argument("video_file", type=Path)
    parser.add_argument(
        "--encoded-dir",
        type=Path,
        default=Path("~/Documents/screencasts/encoded").expanduser(),
    )
    args = parser.parse_args()

    # Validate input file
    input_file = args.video_file
    if not input_file.is_file():
        sys.exit(f"Not a file: {input_file}")
    if not args.encoded_dir.is_dir():
        sys.exit(f"Not a directory: {args.encoded_dir}")

    with TemporaryDirectory() as directory:
        directory = Path(directory)
        normalized_dir = directory / "normalized"
        encoded_dir = directory / "encoded"
        normalized_dir.mkdir()
        encoded_dir.mkdir()

        with ProcessPoolExecutor() as executor:
            # Start the normalizing and transcribing processes
            print("Normalizing audio of", input_file)
            normalizing = executor.submit(normalize_audio_for, input_file, normalized_dir)
            print("Generating captions for", input_file)
            transcribing = executor.submit(generate_captions, input_file, directory)

            # Wait on transcoding to finish
            normalized_file = normalizing.result()
            final_video_file = args.encoded_dir / normalized_file.name
            normalized_file.rename(final_video_file)
            print("Wrote", final_video_file)

            # Wait on transcribing process to finish
            subtitles_file = transcribing.result()
            text_file = text_from_captions(subtitles_file)
            final_subtitles_file = args.encoded_dir / subtitles_file.name
            subtitles_file.rename(final_subtitles_file)
            print("Wrote", final_subtitles_file)
            final_text_file = args.encoded_dir / text_file.name
            text_file.rename(final_text_file)
            print("Wrote", final_text_file)

        print("Done.")


if __name__ == "__main__":
    main()
