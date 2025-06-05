@echo off
echo ================================================
echo    🎵 Recodicon - 오디오 처리기 시작 중...
echo ================================================
echo.

REM 가상환경 존재 확인
if not exist "venv\Scripts\activate.bat" (
    echo ❌ 가상환경이 없습니다.
    echo 💡 먼저 make_venv.bat을 실행하여 설치해주세요.
    echo.
    pause
    exit /b 1
)

echo 🔧 가상환경 활성화 중...
call venv\Scripts\activate

REM FFmpeg 설치 확인
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  경고: FFmpeg가 설치되지 않았거나 PATH에 없습니다.
    echo 💡 오디오 변환 기능이 제한될 수 있습니다.
    echo 📥 https://ffmpeg.org 에서 다운로드하여 설치해주세요.
    echo.
)

REM Python 파일 존재 확인
if not exist "main.py" (
    echo ❌ main.py 파일을 찾을 수 없습니다.
    echo 💡 Recodicon 폴더에서 실행하고 있는지 확인해주세요.
    echo.
    pause
    exit /b 1
)

echo ✅ 가상환경 활성화 완료
echo 🚀 Recodicon 시작 중...
echo.
echo 📱 브라우저에서 다음 주소로 접속하세요:
echo    🔗 http://localhost:7860
echo.
echo 💡 종료하려면 Ctrl+C를 누르거나 이 창을 닫으세요.
echo.

REM Recodicon 실행
python main.py

echo.
echo 🔚 Recodicon이 종료되었습니다.
pause