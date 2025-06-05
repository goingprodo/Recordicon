# 앱 설정 파일

# 서버 설정
SERVER_CONFIG = {
    "server_name": "0.0.0.0",
    "server_port": 7860,
    "share": True,
    "debug": True
}

# 녹음 설정
RECORDING_CONFIG = {
    "bitrate_options": ["64", "96", "128", "160", "192", "224", "256", "320"],
    "default_bitrate": "192",
    "channel_options": ["모노 (Mono)", "스테레오 (Stereo)"],
    "default_channel": "모노 (Mono)",
    "sample_rate_options": [
        "원본 유지",
        "22050 Hz (FM 라디오 수준)",
        "44100 Hz (CD 품질)",
        "48000 Hz (DVD 품질)"
    ],
    "default_sample_rate": "원본 유지"
}

# 피치 조정 설정
PITCH_CONFIG = {
    "min_pitch": -12,
    "max_pitch": 12,
    "default_pitch": 2,
    "step": 0.5,
    "supported_formats": [".mp3", ".wav", ".m4a"]
}

# UI 텍스트
UI_TEXT = {
    "app_title": "🎵 통합 오디오 처리기",
    "app_description": "마이크 녹음과 피치 조정 기능을 제공하는 통합 오디오 처리 도구입니다.",
    "recorder_tab": "🎙️ 마이크 녹음",
    "pitch_tab": "🎵 피치 조정",
    "single_pitch_tab": "단일 파일 처리",
    "batch_pitch_tab": "배치 처리"
}