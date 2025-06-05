import numpy as np
import wave
import subprocess
import imageio_ffmpeg as ffmpeg
from pydub import AudioSegment
from typing import Tuple, Optional

def convert_audio_to_16bit(audio_array: np.ndarray) -> np.ndarray:
    """오디오 배열을 16-bit PCM으로 변환"""
    if audio_array.dtype != np.int16:
        return np.int16(audio_array * 32767)
    return audio_array

def create_stereo_from_mono(mono_array: np.ndarray) -> np.ndarray:
    """모노 오디오를 스테레오로 변환"""
    return np.column_stack((mono_array, mono_array))

def save_wav_file(file_path: str, audio_data: np.ndarray, sample_rate: int, channels: int) -> bool:
    """WAV 파일로 저장"""
    try:
        with wave.open(file_path, 'wb') as wav_file:
            wav_file.setnchannels(channels)
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
        return True
    except Exception:
        return False

def convert_wav_to_mp3(wav_path: str, mp3_path: str, bitrate: str, 
                      sample_rate: int, channels: int) -> Tuple[bool, str]:
    """WAV 파일을 MP3로 변환"""
    try:
        ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
        
        cmd = [
            ffmpeg_exe,
            '-i', wav_path,
            '-codec:a', 'mp3',
            '-b:a', f'{bitrate}k',
            '-ar', str(sample_rate),
            '-ac', str(channels),
            '-y',  # 덮어쓰기 허용
            mp3_path
        ]
        
        # 고품질 설정 추가
        if int(bitrate) >= 320:
            cmd.extend(['-q:a', '0'])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            return False, f"MP3 변환 실패: {result.stderr}"
        
        return True, "변환 성공"
    except Exception as e:
        return False, f"변환 중 오류: {str(e)}"

def convert_mp3_to_wav(mp3_path: str, wav_path: str) -> bool:
    """MP3 파일을 WAV로 변환 (librosa 호환성을 위해)"""
    try:
        audio = AudioSegment.from_mp3(mp3_path)
        audio.export(wav_path, format='wav')
        return True
    except Exception:
        return False

def get_audio_duration(audio_array: np.ndarray, sample_rate: int) -> float:
    """오디오 길이 계산 (초 단위)"""
    return len(audio_array) / sample_rate

def parse_sample_rate_option(option: str, original_rate: int) -> int:
    """샘플레이트 옵션 파싱"""
    if option == "원본 유지":
        return original_rate
    else:
        return int(option.split()[0])

def parse_channel_option(option: str) -> int:
    """채널 옵션 파싱"""
    return 1 if option == "모노 (Mono)" else 2