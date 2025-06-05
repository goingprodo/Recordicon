# 🎵 통합 오디오 처리기

마이크 녹음과 피치 조정 기능을 제공하는 Gradio 기반 웹 애플리케이션입니다.

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
audio_processor/
├── main.py                 # 메인 실행 파일
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

## 🚀 설치 및 실행

### 1. 저장소 클론 또는 파일 다운로드
```bash
# 모든 파일을 audio_processor 폴더에 저장하세요
```

### 2. 필요한 라이브러리 설치
```bash
cd audio_processor
pip install -r requirements.txt
```

### 3. FFmpeg 설치 (필수)

**Windows:**
- https://ffmpeg.org/download.html 에서 다운로드
- 환경변수 PATH에 추가

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

### 4. 애플리케이션 실행
```bash
python main.py
```

### 5. 웹 브라우저에서 접속
- 로컬: http://localhost:7860
- 공유 링크도 자동으로 생성됩니다

## 🎯 사용법

### 마이크 녹음
1. 브라우저에서 마이크 권한 허용
2. 품질 설정 선택
3. 녹음 버튼으로 녹음 시작/중지
4. "녹음 처리" 버튼으로 MP3 변환
5. 다운로드

### 피치 조정
1. 오디오 파일 업로드
2. 피치 조정값 설정 (-12 ~ +12 반음)
3. 출력 폴더 설정 (선택사항)
4. 처리 실행
5. 결과 다운로드

## ⚙️ 설정 커스터마이징

`config/settings.py` 파일에서 다음 설정들을 변경할 수 있습니다:

- 서버 포트 및 주소
- 기본 비트레이트 및 품질 옵션
- 피치 조정 범위
- UI 텍스트

## 🛠️ 문제 해결

### 일반적인 오류

**ModuleNotFoundError:**
```bash
pip install --upgrade -r requirements.txt
```

**FFmpeg 관련 오류:**
- FFmpeg가 올바르게 설치되고 PATH에 추가되었는지 확인

**마이크 접근 안됨:**
- 브라우저에서 마이크 권한 허용
- HTTPS 환경에서 실행 권장

**메모리 부족:**
- 큰 파일 처리 시 충분한 RAM 확보
- 배치 처리 시 파일 개수 제한

## 📋 요구사항

- Python 3.7+
- FFmpeg
- 충분한 디스크 공간 (임시 파일용)
- 마이크 접근 권한

## 🔧 개발자를 위한 정보

### 새로운 기능 추가
1. `modules/` 폴더에 새 모듈 생성
2. `utils/` 폴더에 공통 함수 추가
3. `main.py`에서 인터페이스 연결
4. `config/settings.py`에 설정 추가

### 코드 구조
- **modules**: 핵심 기능 모듈
- **utils**: 재사용 가능한 유틸리티 함수
- **config**: 설정 및 상수

## 📜 라이선스

이 프로젝트는 개인 및 교육 목적으로 자유롭게 사용할 수 있습니다.

## 🤝 기여

버그 리포트나 기능 제안은 언제든 환영합니다!

---

**개발**: AI Assistant  
**기술 스택**: Python, Gradio, librosa, FFmpeg, Pydub