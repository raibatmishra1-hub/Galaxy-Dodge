"""Convert .wav files to .ogg (Ogg Vorbis) for the web build.

Browsers (and pygbag) handle .ogg far better than .wav, and .ogg files are
roughly 10x smaller, so the game loads quickly on phones.

Requires ffmpeg on PATH (https://ffmpeg.org). Uses only the standard library.

Usage (from anywhere):
    python scripts/convert_audio.py              # convert all .wav in audio/
    python scripts/convert_audio.py --force      # re-convert even if .ogg exists
    python scripts/convert_audio.py --quality 3  # Vorbis quality 0-10 (default 4)
    python scripts/convert_audio.py --src some/dir
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = REPO_ROOT / 'audio'

def convert(wav_path, quality, force):
    ogg_path = wav_path.with_suffix('.ogg')

    if ogg_path.exists() and not force:
        print(f"skip     {wav_path.name} (already has {ogg_path.name})")
        return True

    command = [
        'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
        '-i', str(wav_path),
        '-c:a', 'libvorbis', '-q:a', str(quality),
        str(ogg_path),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FAILED   {wav_path.name}: {result.stderr.strip()}")
        return False

    wav_kb = wav_path.stat().st_size / 1024
    ogg_kb = ogg_path.stat().st_size / 1024
    print(f"convert  {wav_path.name} -> {ogg_path.name}  ({wav_kb:,.0f} KB -> {ogg_kb:,.0f} KB)")
    return True


def main():
    parser = argparse.ArgumentParser(description='Convert .wav files to .ogg using ffmpeg.')
    parser.add_argument('--src', type=Path, default=AUDIO_DIR,
                        help='folder containing .wav files (default: audio/)')
    parser.add_argument('--quality', type=int, default=4, choices=range(0, 11), metavar='0-10',
                        help='Vorbis quality, higher is better/larger (default: 4)')
    parser.add_argument('--force', action='store_true',
                        help='overwrite existing .ogg files')
    args = parser.parse_args()

    if shutil.which('ffmpeg') is None:
        sys.exit("ffmpeg not found on PATH. Install it from https://ffmpeg.org and try again.")

    src = args.src.resolve()
    wav_files = sorted(src.glob('*.wav'))
    if not wav_files:
        sys.exit(f"No .wav files found in {src}")

    results = [convert(wav, args.quality, args.force) for wav in wav_files]
    failed = results.count(False)
    print(f"\n{len(results) - failed}/{len(results)} files OK in {src}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()