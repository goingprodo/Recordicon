# 🎵 Recodicon - 통합 오디오 처리기

**Recodicon**은 마이크 녹음과 피치 조정 기능을 제공하는 Gradio 기반 웹 애플리케이션입니다.

> **Record + Icon = Recodicon** 🎙️✨

## ✨ 주요 기능

### 🎙️ 마이크 녹음
- 실시간 마이크 녹음
- 다양한 품질 설정 (비트레이트, 채널, 샘플링 레이트)
- 고품질 MP3 출력
- FFmpeg 기반 압축

### 🎵 피치 조정
- 단일 파일 및 배치 처리
- -12 ~ +12 반음 범위 조정
- 다양한 오디오 형식 지원 (MP3, WAV, M4A)
- librosa 기반 고품질 피치 시프팅

## 📁 프로젝트 구조

```
Recodicon/
├── main.py                 # 메인 실행 파일
├── make_venv.bat          # 가상환경 생성 및 패키지 설치 (Windows)
├── run_gpu.bat            # 애플리케이션 실행 (Windows)
├── requirements.txt        # 필요한 라이브러리
├── README.md              # 이 파일
├── config/
│   └── settings.py        # 앱 설정
├── modules/
│   ├── __init__.py       
│   ├── recorder.py       # 녹음 기능
│   └── pitch_shifter.py  # 피치 조정 기능
└── utils/
    ├── __init__.py       
    ├── audio_utils.py    # 오디오 처리 유틸리티
    └── file_utils.py     # 파일 처리 유틸리티
```

## 🚀 빠른 시작 (Windows 사용자)

### 1️⃣ 준비사항
- **Python 3.10** 설치 필요 ([python.org](https://python.org)에서 다운로드)
- **FFmpeg** 설치 필요 ([ffmpeg.org](https://ffmpeg.org/download.html)에서 다운로드 후 PATH 추가)

### 2️⃣ Recodicon 설치
1. 모든 파일을 `Recodicon` 폴더에 다운로드
2. **`make_venv.bat`** 더블클릭 → 가상환경 생성 및 패키지 자동 설치
3. 설치 완료까지 기다리기 (약 2-3분)

### 3️⃣ Recodicon 실행
- **`run_gpu.bat`** 더블클릭 → 애플리케이션 자동 실행
- 웹 브라우저가 자동으로 열리거나 콘솔에 표시된 주소로 접속

### 🎯 완료!
브라우저에서 http://localhost:7860 또는 공유 링크로 접속하여 Recodicon을 사용하세요!

---

## 🐧 Linux/macOS 사용자

### Recodicon 설치
```bash
# 1. Recodicon 폴더로 이동
cd Recodicon

# 2. 가상환경 생성
python3 -m venv venv
source venv/bin/activate  # Linux/macOS

# 3. 패키지 설치
pip install -r requirements.txt

# 4. FFmpeg 설치
# macOS:
brew install ffmpeg

# Ubuntu/Debian:
sudo apt update && sudo apt install ffmpeg
```

### Recodicon 실행
```bash
cd Recodicon
source venv/bin/activate
python main.py
```

---

## 🎯 Recodicon 사용법

### 🎙️ 마이크 녹음
1. **마이크 권한 허용**: 브라우저에서 마이크 접근 권한 허용
2. **품질 설정**: 비트레이트, 채널, 샘플링 레이트 선택
3. **녹음**: 마이크 버튼으로 녹음 시작/중지
4. **변환**: "녹음 처리" 버튼으로 MP3 변환
5. **다운로드**: 생성된 파일 다운로드

### 🎵 피치 조정

#### 단일 파일 처리
1. MP3/WAV/M4A 파일 업로드
2. 피치 조정값 설정 (-12 ~ +12 반음)
3. 출력 폴더 설정 (선택사항)
4. "피치 조정하기" 클릭
5. 결과 다운로드

#### 배치 처리 (여러 파일)
1. 여러 파일 한 번에 업로드
2. 피치 조정값 설정 (모든 파일에 동일 적용)
3. 출력 폴더 설정 또는 ZIP 다운로드 선택
4. "일괄 처리하기" 클릭
5. 진행률 확인 후 결과 다운로드

---

## ⚙️ Recodicon 고급 설정

### 품질 설정 가이드
| 용도 | 비트레이트 | 채널 | 샘플링 레이트 |
|------|------------|------|--------------|
| 음성 녹음 | 64-128kbps | 모노 | 22kHz |
| 일반 음악 | 192kbps | 스테레오 | 44.1kHz |
| 고품질 음악 | 256-320kbps | 스테레오 | 48kHz |

### 피치 조정 팁
- **1 반음** = 1 semitone (12반음 = 1옥타브)
- **보컬 높이기**: +1 ~ +4 반음 권장
- **음악 키 변경**: ±1 ~ ±6 반음 일반적
- **극한 효과**: ±7 ~ ±12 반음 (로봇 목소리 등)

### 출력 설정
- **폴더 지정**: `C:\Users\사용자\Music\Recodicon_Output` 형식으로 입력
- **비워두기**: 웹에서 직접 다운로드 또는 ZIP 파일 제공

---

## 🔧 Recodicon 커스터마이징

`config/settings.py` 파일에서 다음을 수정할 수 있습니다:

```python
# 서버 설정
SERVER_CONFIG = {
    "server_port": 7860,    # 포트 변경
    "share": True,          # 공유 링크 생성 여부
}

# 기본값 변경
RECORDING_CONFIG = {
    "default_bitrate": "192",  # 기본 비트레이트
    "default_channel": "모노 (Mono)",  # 기본 채널
}

# UI 텍스트 커스터마이징
UI_TEXT = {
    "app_title": "🎵 Recodicon - 나만의 오디오 처리기",
    "app_description": "당신만의 오디오 처리 솔루션",
}
```

---

## 🛠️ 문제 해결

### 자주 발생하는 문제

**1. Python을 찾을 수 없음**
```
해결: Python 3.10을 설치하고 PATH에 추가
확인: 명령 프롬프트에서 'py -3.10 --version' 실행
```

**2. FFmpeg 관련 오류**
```
해결: FFmpeg 설치 후 환경변수 PATH에 추가
확인: 명령 프롬프트에서 'ffmpeg -version' 실행
```

**3. make_venv.bat 실행 오류**
```
해결: PowerShell 실행 정책 변경
명령: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
또는: 관리자 권한으로 명령 프롬프트 실행
```

**4. run_gpu.bat 실행 안됨**
```
해결: make_venv.bat을 먼저 실행했는지 확인
확인: Recodicon 폴더에 venv 폴더가 생성되었는지 확인
```

**5. 마이크 접근 안됨**
```
해결: 브라우저에서 마이크 권한 허용
팁: Chrome에서 주소창 옆 자물쇠 아이콘 클릭
```

**6. 메모리 부족**
```
해결: 큰 파일 처리 시 파일 크기 줄이기
팁: 배치 처리 시 한 번에 5-10개 파일만 처리
```

### Recodicon 재설치 방법
1. `Recodicon` 폴더 내 `venv` 폴더 삭제
2. `make_venv.bat` 다시 실행
3. 완료 후 `run_gpu.bat`으로 실행

---

## 📋 시스템 요구사항

### 최소 사양
- **OS**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.7 이상 (3.10 권장)
- **RAM**: 4GB 이상
- **저장공간**: 2GB 이상 (임시 파일용)

### 권장 사양 (최적의 Recodicon 성능을 위해)
- **Python**: 3.10 또는 3.11
- **RAM**: 8GB 이상 (대용량 파일 처리용)
- **SSD**: 빠른 파일 처리
- **CPU**: 멀티코어 프로세서 (배치 처리 성능 향상)

---

## 🎵 Recodicon 배치 파일 상세

### `make_venv.bat`
```batch
@echo off
REM Recodicon 가상환경 생성 및 패키지 설치
py -3.10 -m venv venv
call venv/Scripts/activate
python -m pip install -r requirements.txt
echo Recodicon installation completed! You can now run using run_gpu.bat
pause
```

### `run_gpu.bat`
```batch
@echo off
REM Recodicon 실행
call venv\Scripts\activate
python main.py
pause
```

---

## 🔧 개발자 정보

### Recodicon 아키텍처
- **프론트엔드**: Gradio (웹 인터페이스)
- **오디오 처리**: librosa, Pydub, FFmpeg
- **백엔드**: Python, NumPy, SciPy

### Recodicon 확장 가이드
1. `modules/` 폴더에 새 모듈 생성
2. `utils/` 폴더에 공통 함수 추가  
3. `main.py`에서 인터페이스 연결
4. `config/settings.py`에 설정 추가

### 코드 구조
- **modules**: 핵심 기능 (녹음, 피치 조정)
- **utils**: 재사용 가능한 유틸리티
- **config**: 중앙 집중식 설정 관리

---

## 📞 Recodicon 지원

### 버그 리포트
다음 정보와 함께 리포트해주세요:
- 발생한 오류의 스크린샷
- 사용한 파일 형식 및 크기
- 운영체제 및 Python 버전
- Recodicon 실행 환경

### 기능 제안
Recodicon의 새로운 기능 아이디어나 개선사항 제안 환영합니다!

---

## 📄 라이선스

**Recodicon**은 개인 및 교육 목적으로 자유롭게 사용할 수 있습니다.

---

**🎵 Recodicon** - *Your Audio Processing Companion*  
**개발**: AI Assistant  
**기술 스택**: Python, Gradio, librosa, FFmpeg, Pydub
