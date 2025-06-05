@echo off
echo ================================================
echo    🎵 Recodicon - 오디오 처리기 설치 중...
echo ================================================
echo.

REM Python 버전 확인
py -3.10 --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 3.10이 설치되지 않았습니다.
    echo 📥 https://python.org 에서 Python 3.10을 다운로드하여 설치해주세요.
    pause
    exit /b 1
)

echo ✅ Python 3.10 발견됨
echo 📦 Recodicon 가상환경 생성 중...

REM Python 가상환경 생성 및 활성화
py -3.10 -m venv venv
if errorlevel 1 (
    echo ❌ 가상환경 생성 실패
    pause
    exit /b 1
)

echo ✅ 가상환경 생성 완료
echo 🔧 가상환경 활성화 중...

call venv\Scripts\activate
if errorlevel 1 (
    echo ❌ 가상환경 활성화 실패
    pause
    exit /b 1
)

echo ✅ 가상환경 활성화 완료
echo 📚 필요한 패키지 설치 중... (약 2-3분 소요)

REM pip 업그레이드
python -m pip install --upgrade pip

REM 필요한 패키지 설치
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 패키지 설치 실패
    echo 💡 인터넷 연결을 확인하고 다시 시도해주세요.
    pause
    exit /b 1
)

echo.
echo ================================================
echo    🎉 Recodicon 설치 완료!
echo ================================================
echo.
echo 📋 다음 단계:
echo    1. FFmpeg 설치 확인 (https://ffmpeg.org)
echo    2. run_gpu.bat 실행하여 Recodicon 시작
echo.
echo 💡 팁: FFmpeg가 설치되지 않으면 오디오 변환이 작동하지 않습니다.
echo.

pause