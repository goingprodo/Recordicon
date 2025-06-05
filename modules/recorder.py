import numpy as np
import tempfile
from typing import Tuple, Optional, Any
from utils.audio_utils import (
    convert_audio_to_16bit, create_stereo_from_mono, save_wav_file,
    convert_wav_to_mp3, get_audio_duration, parse_sample_rate_option,
    parse_channel_option
)
from utils.file_utils import generate_filename, get_file_size_mb, safe_delete_file

def process_recording(audio_data: Any, bitrate: str, channels: str, 
                     sample_rate_option: str) -> Tuple[Optional[str], str]:
    """
    오디오 데이터를 받아서 MP3로 변환하는 함수
    
    Args:
        audio_data: Gradio에서 받은 오디오 데이터 (sample_rate, audio_array)
        bitrate: 출력 비트레이트
        channels: 채널 설정 ("모노 (Mono)" 또는 "스테레오 (Stereo)")
        sample_rate_option: 샘플레이트 설정
    
    Returns:
        (mp3_file_path, status_message)
    """
    if audio_data is None:
        return None, "녹음된 오디오가 없습니다."
    
    temp_wav_path = None
    
    try:
        # Gradio에서 받은 오디오 데이터 처리
        original_sample_rate, audio_array = audio_data
        
        # 샘플레이트 설정
        target_sample_rate = parse_sample_rate_option(sample_rate_option, original_sample_rate)
        
        # 채널 설정
        channels_num = parse_channel_option(channels)
        
        # 16-bit PCM으로 변환
        audio_array = convert_audio_to_16bit(audio_array)
        
        # 임시 WAV 파일 생성
        temp_wav_path = tempfile.mktemp(suffix=".wav")
        
        # 스테레오 변환 (필요한 경우)
        if channels == "스테레오 (Stereo)" and len(audio_array.shape) == 1:
            audio_array = create_stereo_from_mono(audio_array)
        
        # WAV 파일로 저장
        if not save_wav_file(temp_wav_path, audio_array, target_sample_rate, channels_num):
            return None, "WAV 파일 저장 실패"
        
        # MP3 파일명 생성
        mp3_filename = generate_filename(
            "recording",
            f"{bitrate}kbps_{channels.split()[0]}_{target_sample_rate}Hz"
        )
        
        # MP3로 변환
        success, message = convert_wav_to_mp3(
            temp_wav_path, mp3_filename, bitrate, target_sample_rate, channels_num
        )
        
        if not success:
            return None, message
        
        # 파일 정보 계산
        file_size = get_file_size_mb(mp3_filename)
        duration = get_audio_duration(audio_array, target_sample_rate)
        
        status_msg = f"""✅ 녹음 완료!
📁 파일명: {mp3_filename}
🎵 비트레이트: {bitrate}kbps
📊 채널: {channels}
🔊 샘플레이트: {target_sample_rate} Hz
⏱️ 길이: {duration:.1f}초
💾 파일크기: {file_size:.2f}MB
🎼 형식: MP3 (고품질 압축)"""
        
        return mp3_filename, status_msg
    
    except Exception as e:
        return None, f"오류가 발생했습니다: {str(e)}"
    
    finally:
        # 임시 파일 정리
        safe_delete_file(temp_wav_path)

def clear_recording() -> Tuple[None, str]:
    """녹음 초기화"""
    return None, "새로운 녹음을 시작할 수 있습니다."