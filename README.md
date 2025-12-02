# hum2song
Hum2Song: Humming-to-Melody Translation with Machine Learning

## 🛠️ Environment Setup (Module 1)

본 프로젝트는 **Python 3.8+** 환경에서 테스트되었습니다.
`pretty_midi` 라이브러리 설치 시 발생하는 호환성 문제를 방지하기 위해 아래 절차를 따라주세요.

### 1. 가상환경 생성 및 활성화
```bash
# 가상환경 생성 (venv)
python -m venv venv

# 활성화 (Windows)
.\venv\Scripts\activate

# 활성화 (Mac/Linux)
source venv/bin/activate
2. 라이브러리 설치 (중요!)
requirements.txt에 호환성 패치가 포함되어 있습니다. 아래 명령어로 한 번에 설치하세요.

Bash

pip install --upgrade pip
pip install -r requirements.txt
🆘 Troubleshooting (설치 에러 발생 시)
만약 pretty_midi 설치 중 metadata-generation-failed 에러가 발생한다면, 아래 명령어를 순서대로 입력하여 해결할 수 있습니다.

Bash

# 1. setuptools 버전을 강제로 낮춥니다.
pip install "setuptools<70"

# 2. 다시 requirements를 설치합니다.
pip install -r requirements.txt

---