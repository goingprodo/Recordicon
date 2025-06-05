import librosa
import soundfile as sf
import os
import tempfile
from pydub import AudioSegment
from typing import Union, List, Tuple, Optional
import gradio as gr

from utils.file_utils import (
    create_temp_file, safe_delete_file, create_zip_file, 
    copy_file_to_directory, validate_directory
)
from utils.audio_utils import convert_mp3_to_wav

def shift_pitch(audio_file: Union[str, object], pitch_shift_semitones: float) -> str:
    """
    오디오 파일의 피치를 조정하는 함수
    
    Args:
        audio_file: 입력 오디오 파일 경로 (문자열 또는 파일 객체)
        pitch_shift_semitones: 피치 변경량 (반음 단위)
    
    Returns:
        처리된 오디오 파일 경로 또는 오류 메시지
    """
    temp_wav_path = None
    temp_output_path = None
    
    try:
        # 파일 경로 확인
        if isinstance(audio_file, str):
            file_path = audio_file
        else:
            file_path = audio_file.name
        
        # MP3 파일을 WAV로 변환 (librosa 호환성을 위해)
        if file_path.lower().endswith('.mp3'):
            temp_wav_path = create_temp_file('.wav')
            if not convert_mp3_to_wav(file_path, temp_wav_path):
                return "MP3 to WAV 변환 실패"
            audio_path = temp_wav_path
        else:
            audio_path = file_path
        
        # 오디오 로드
        y, sr = librosa.load(audio_path, sr=None)
        
        # 피치 시프트 적용
        y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=pitch_shift_semitones)
        
        # 임시 파일로 저장
        temp_output_path = create_temp_file('.wav')
        sf.write(temp_output_path, y_shifted, sr)
        
        # WAV를 MP3로 변환
        audio_output = AudioSegment.from_wav(temp_output_path)
        final_output_path = create_temp_file('.mp3')
        audio_output.export(final_output_path, format='mp3', bitrate='192k')
        
        return final_output_path
        
    except Exception as e:
        return f"오류 발생: {str(e)}"
    
    finally:
        # 임시 파일 정리
        safe_delete_file(temp_wav_path)
        safe_delete_file(temp_output_path)

def process_single_audio(audio_file: object, pitch_shift: float, 
                        output_dir: str = None) -> Tuple[Optional[str], str]:
    """
    단일 오디오 파일 처리
    """
    if audio_file is None:
        return None, "오디오 파일을 업로드해주세요."
    
    try:
        output_file = shift_pitch(audio_file, pitch_shift)
        
        if isinstance(output_file, str) and output_file.startswith("오류"):
            return None, output_file
        
        # 출력 디렉토리가 지정된 경우
        if output_dir and validate_directory(output_dir):
            original_name = os.path.splitext(os.path.basename(audio_file.name))[0]
            final_filename = f"{original_name}_pitch_{pitch_shift:+.1f}.mp3"
            final_path = copy_file_to_directory(output_file, output_dir, final_filename)
            
            # 임시 파일 삭제
            safe_delete_file(output_file)
            
            if final_path:
                return final_path, f"피치가 {pitch_shift:+.1f} 반음만큼 조정되었습니다.\n저장 위치: {final_path}"
            else:
                return None, "파일 저장 중 오류가 발생했습니다."
        
        return output_file, f"피치가 {pitch_shift:+.1f} 반음만큼 조정되었습니다."
        
    except Exception as e:
        return None, f"처리 중 오류가 발생했습니다: {str(e)}"

def process_batch_files(files: List[object], pitch_shift: float, 
                       output_dir: str = None, 
                       progress: gr.Progress = gr.Progress()) -> Tuple[Optional[str], str]:
    """
    여러 파일을 일괄 처리하는 함수
    """
    if not files:
        return None, "파일을 업로드해주세요."
    
    try:
        processed_files = []
        total_files = len(files)
        
        # 출력 디렉토리가 지정된 경우
        if output_dir and validate_directory(output_dir):
            for i, file in enumerate(files):
                progress((i + 1) / total_files, 
                        f"처리 중: {os.path.basename(file.name)} ({i+1}/{total_files})")
                
                # 개별 파일 처리
                result = shift_pitch(file.name, pitch_shift)
                
                if isinstance(result, str) and result.startswith("오류"):
                    continue  # 오류 발생한 파일은 건너뛰기
                
                # 지정된 디렉토리에 파일 저장
                original_name = os.path.splitext(os.path.basename(file.name))[0]
                new_filename = f"{original_name}_pitch_{pitch_shift:+.1f}.mp3"
                final_path = copy_file_to_directory(result, output_dir, new_filename)
                
                if final_path:
                    processed_files.append(new_filename)
                
                # 임시 결과 파일 삭제
                safe_delete_file(result)
            
            if not processed_files:
                return None, "처리할 수 있는 파일이 없습니다."
            
            return None, f"""총 {len(processed_files)}개 파일이 처리되어 {output_dir}에 저장되었습니다.

저장된 파일들:
""" + "\n".join(f"• {filename}" for filename in processed_files)
        
        # 출력 디렉토리가 지정되지 않은 경우 (ZIP 방식)
        else:
            temp_dir = tempfile.mkdtemp()
            temp_files = []
            
            for i, file in enumerate(files):
                progress((i + 1) / total_files, 
                        f"처리 중: {os.path.basename(file.name)} ({i+1}/{total_files})")
                
                # 개별 파일 처리
                result = shift_pitch(file.name, pitch_shift)
                
                if isinstance(result, str) and result.startswith("오류"):
                    continue
                
                # 처리된 파일을 임시 디렉토리에 복사
                original_name = os.path.splitext(os.path.basename(file.name))[0]
                new_filename = f"{original_name}_pitch_{pitch_shift:+.1f}.mp3"
                new_filepath = os.path.join(temp_dir, new_filename)
                
                # 파일 복사
                try:
                    with open(result, 'rb') as src, open(new_filepath, 'wb') as dst:
                        dst.write(src.read())
                    temp_files.append((new_filepath, new_filename))
                except Exception:
                    pass
                
                # 임시 결과 파일 삭제
                safe_delete_file(result)
            
            if not temp_files:
                return None, "처리할 수 있는 파일이 없습니다."
            
            # ZIP 파일 생성
            zip_path = create_temp_file('.zip')
            if create_zip_file(temp_files, zip_path):
                # 임시 디렉토리 정리
                for filepath, _ in temp_files:
                    safe_delete_file(filepath)
                os.rmdir(temp_dir)
                
                return zip_path, f"총 {len(temp_files)}개 파일이 처리되었습니다. ZIP 파일을 다운로드하세요."
            else:
                return None, "ZIP 파일 생성 중 오류가 발생했습니다."
        
    except Exception as e:
        return None, f"배치 처리 중 오류가 발생했습니다: {str(e)}"