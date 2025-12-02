# hum2song/module1/src/paths.py
from pathlib import Path

# module1 폴더 기준 루트
BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

# 편의상 디렉토리 없으면 만들어 두기
DATA_DIR.mkdir(exist_ok=True, parents=True)
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
