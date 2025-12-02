# hum2song/module1/src/melody_extractor.py
from __future__ import annotations

from pathlib import Path
from typing import List

from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH
from paths import OUTPUT_DIR
from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH


def extract_melody_to_midi(
    audio_path: str | Path,
    output_dir: str | Path | None = None,
    save_notes_csv: bool = False,
) -> List[Path]:
    """
    Basic Pitch를 이용해 audio 파일을 MIDI로 변환한다.

    Parameters
    ----------
    audio_path : str or Path
        허밍 오디오 파일 경로 (.wav, .mp3 등)
    output_dir : str or Path, optional
        결과를 저장할 디렉토리. None이면 module1/output 사용.
    save_notes_csv : bool
        True면 note event CSV도 함께 저장.

    Returns
    -------
    List[Path]
        생성된 MIDI 파일 경로 리스트.
        (현재는 audio 1개만 넣으므로 길이 1일 것)
    """
    audio_path = Path(audio_path)
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    out_dir = Path(output_dir) if output_dir is not None else OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    # Basic Pitch는 input 경로 리스트, output 디렉토리, 저장 옵션들을 인자로 받음
    predict_and_save(
        [str(audio_path)],     # input-audio-path-list
        str(out_dir),          # output-directory
        save_midi=True,        # MIDI 저장
        sonify_midi=False,     # MIDI를 wav로 렌더링은 안 함
        save_model_outputs=False,
        save_notes=save_notes_csv,
    )

    # output 디렉토리 안에서 방금 파일 이름(stem)으로 시작하는 .mid 찾기
    stem = audio_path.stem
    midi_files = sorted(out_dir.glob(f"{stem}*.mid"))

    if not midi_files:
        raise RuntimeError(
            f"No MIDI file was generated for input {audio_path} in {out_dir}"
        )

    return midi_files
