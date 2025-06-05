import os
import tempfile
import zipfile
from typing import List, Tuple, Optional

def create_temp_file(suffix: str = ".mp3") -> str:
    """임시 파일 경로 생성"""
    return tempfile.mktemp(suffix=suffix)

def safe_delete_file(file_path: str) -> None:
    """안전하게 파일 삭제"""
    try:
        if file_path and os.path.exists(file_path):
            os.unlink(file_path)
    except Exception:
        pass  # 삭제 실패해도 무시

def get_file_size_mb(file_path: str) -> float:
    """파일 크기를 MB 단위로 반환"""
    try:
        return os.path.getsize(file_path) / (1024 * 1024)
    except Exception:
        return 0.0

def generate_filename(base_name: str, suffix: str, extension: str = "mp3") -> str:
    """파일명 생성"""
    import numpy as np
    random_id = np.random.randint(1000, 9999)
    return f"{base_name}_{suffix}_{random_id}.{extension}"

def create_zip_file(files: List[Tuple[str, str]], zip_path: str) -> bool:
    """여러 파일을 ZIP으로 압축"""
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filepath, filename in files:
                if os.path.exists(filepath):
                    zipf.write(filepath, filename)
        return True
    except Exception:
        return False

def copy_file_to_directory(src_path: str, dst_dir: str, new_filename: str) -> Optional[str]:
    """파일을 지정된 디렉토리로 복사"""
    try:
        if not os.path.exists(dst_dir):
            return None
        
        dst_path = os.path.join(dst_dir, new_filename)
        with open(src_path, 'rb') as src, open(dst_path, 'wb') as dst:
            dst.write(src.read())
        return dst_path
    except Exception:
        return None

def validate_directory(dir_path: str) -> bool:
    """디렉토리 경로 유효성 검사"""
    return dir_path and os.path.exists(dir_path) and os.path.isdir(dir_path)