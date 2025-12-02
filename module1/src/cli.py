# hum2song/module1/src/cli.py
from __future__ import annotations

import argparse
from pathlib import Path

from paths import DATA_DIR, OUTPUT_DIR
from melody_extractor import extract_melody_to_midi



def main():
    parser = argparse.ArgumentParser(
        description="Hum2Song Module1 - Humming audio to MIDI using Basic Pitch"
    )
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        required=True,
        help="입력 오디오 파일 경로 (예: data/hum1.wav)",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=str,
        default=str(OUTPUT_DIR),
        help=f"MIDI를 저장할 디렉토리 (default: {OUTPUT_DIR})",
    )
    parser.add_argument(
        "--save-notes-csv",
        action="store_true",
        help="note 이벤트 CSV도 함께 저장할지 여부",
    )

    args = parser.parse_args()

    audio_path = Path(args.input)
    midi_paths = extract_melody_to_midi(
        audio_path,
        output_dir=args.output_dir,
        save_notes_csv=args.save_notes_csv,
    )

    print("✅ Module1 done.")
    for p in midi_paths:
        print(f"   → {p}")


if __name__ == "__main__":
    main()
