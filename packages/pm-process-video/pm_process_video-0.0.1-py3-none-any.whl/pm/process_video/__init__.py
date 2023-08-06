from concurrent.futures import ProcessPoolExecutor
from os import fsencode
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import sys

from ffmpeg_normalize import FFmpegNormalize
import ffmpeg
import openai
from pm.vtt2txt import vtt_to_text


openai.api_key_path = Path.home() / ".openai"


def run(command, *args, **kwargs):
    """Run subprocess and check for successful status code."""
    return subprocess.run(
        [command, *args],
        check=True,
        encoding="utf-8",
        **kwargs,
    )


def normalize_audio_for(video_path, audio_normalized_path):
    """Return audio-normalized video file saved in the given directory."""
    ffmpeg_normalize = FFmpegNormalize(audio_codec="aac", audio_bitrate="192k")
    ffmpeg_normalize.add_media_file(video_path, audio_normalized_path)
    ffmpeg_normalize.run_normalization()


def optimize_video(video_path, new_path):
    """Transcode video to optimize it."""
    # Requires npm install h265ize --global
    with TemporaryDirectory() as directory:
        run(
            "h265ize",
            "-m",
            "medium",
            "-q",
            "20",
            "-x",
            "--no-sao",
            "--aq-mode=3",
            "--normalize-level=0",
            "-d",
            directory,
            video_path,
        )
        Path(directory, video_path.name).rename(new_path)


def generate_captions(video_path, vtt_path):
    """Generate caption file out of audio track."""
    # Extracting just the audio (for whisper)
    with TemporaryDirectory() as directory:
        audio_file = Path(directory, video_path.name).with_suffix(".m4a")
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
    vtt_path.write_text(transcript)


def text_from_captions(caption_path, text_path):
    """Generate text from given captions."""
    print("Generating text transcript for", caption_path)
    plain_text = vtt_to_text(caption_path.read_text())
    text_path.write_text(plain_text)
    print("Generated", text_path)


def process_video(video_file, target_directory, optimize=False):

    # Validate input file
    input_file = video_file
    if not input_file.is_file():
        sys.exit(f"Not a file: {input_file}")
    if not target_directory.is_dir():
        sys.exit(f"Not a directory: {target_directory}")

    with TemporaryDirectory() as directory:
        directory = Path(directory)
        normalized_dir = directory / "normalized"
        encoded_dir = directory / "encoded"
        normalized_dir.mkdir()
        encoded_dir.mkdir()

        with ProcessPoolExecutor() as executor:
            # Start the normalizing and transcribing processes
            print("Normalizing audio of", input_file)
            normalized_file = normalized_dir / video_file.name
            processing = executor.submit(
                normalize_audio_for,
                input_file,
                normalized_file,
            )
            if optimize:
                # Wait on normalizing to finish
                processing.result()
                transcoded_file = encoded_dir / video_file.name
                processing = executor.submit(
                    optimize_video,
                    normalized_file,
                    transcoded_file,
                )
                normalized_file = transcoded_file
            print("Generating captions for", input_file)
            subtitles_file = directory / input_file.with_suffix(".vtt").name
            transcribing = executor.submit(
                generate_captions,
                input_file,
                subtitles_file,
            )

            # Wait on transcoding or normalizing to finish
            processing.result()
            final_video_file = target_directory / normalized_file.name
            normalized_file.rename(final_video_file)
            print("Wrote", final_video_file)

            # Wait on transcribing process to finish
            transcribing.result()
            text_file = subtitles_file.with_suffix(".txt")
            text_from_captions(subtitles_file, text_file)
            final_subtitles_file = target_directory / subtitles_file.name
            subtitles_file.rename(final_subtitles_file)
            print("Wrote", final_subtitles_file)
            final_text_file = target_directory / text_file.name
            text_file.rename(final_text_file)
            print("Wrote", final_text_file)

        print("Done.")
