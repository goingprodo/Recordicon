import gradio as gr
from config.settings import SERVER_CONFIG, RECORDING_CONFIG, PITCH_CONFIG, UI_TEXT
from modules.recorder import process_recording, clear_recording
from modules.pitch_shifter import process_single_audio, process_batch_files

def create_recorder_interface():
    """마이크 녹음 인터페이스 생성"""
    with gr.Column():
        gr.HTML("""
        <div style="text-align: center; padding: 20px;">
            <h2>🎙️ 마이크 녹음기</h2>
            <p>녹음 버튼을 눌러 음성을 녹음하고 고품질 MP3 파일로 저장하세요!</p>
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                # 마이크 입력 컴포넌트
                microphone = gr.Audio(
                    sources=["microphone"],
                    type="numpy",
                    label="마이크 녹음",
                    interactive=True
                )
                
                with gr.Row():
                    record_btn = gr.Button("🎙️ 녹음 처리", variant="primary", size="lg")
                    clear_btn = gr.Button("🗑️ 초기화", variant="secondary")
            
            with gr.Column(scale=1):
                # 품질 설정
                gr.HTML("<h3>🔧 품질 설정</h3>")
                
                bitrate = gr.Dropdown(
                    choices=RECORDING_CONFIG["bitrate_options"],
                    value=RECORDING_CONFIG["default_bitrate"],
                    label="비트레이트 (kbps)",
                    info="높을수록 고품질 (파일 크기 증가)"
                )
                
                channels = gr.Radio(
                    choices=RECORDING_CONFIG["channel_options"],
                    value=RECORDING_CONFIG["default_channel"],
                    label="채널 설정",
                    info="스테레오는 파일 크기가 2배"
                )
                
                sample_rate_option = gr.Dropdown(
                    choices=RECORDING_CONFIG["sample_rate_options"],
                    value=RECORDING_CONFIG["default_sample_rate"],
                    label="샘플링 레이트",
                    info="높을수록 고품질"
                )
                
                # 품질 가이드
                with gr.Accordion("💡 품질 가이드", open=False):
                    gr.HTML("""
                    <div style="font-size: 12px; line-height: 1.4;">
                        <strong>비트레이트 가이드:</strong><br>
                        • 64kbps: 음성 녹음 (최소 품질)<br>
                        • 128kbps: 일반 음악 (표준)<br>
                        • 192kbps: 고품질 음악 (권장)<br>
                        • 256kbps: 매우 고품질<br>
                        • 320kbps: 최고 품질 (CD 수준)<br><br>
                        
                        <strong>용량 참고:</strong><br>
                        • 1분 음성: 64kbps ≈ 0.48MB<br>
                        • 1분 음악: 192kbps ≈ 1.44MB<br>
                        • 1분 최고품질: 320kbps ≈ 2.4MB
                    </div>
                    """)
        
        with gr.Row():
            with gr.Column():
                # 결과 표시
                output_file = gr.File(label="📥 다운로드 MP3 파일", interactive=False)
                status_text = gr.Textbox(
                    label="📊 변환 상태", 
                    interactive=False,
                    placeholder="녹음 상태와 파일 정보가 여기에 표시됩니다.",
                    lines=8
                )
        
        # 이벤트 핸들러
        record_btn.click(
            fn=process_recording,
            inputs=[microphone, bitrate, channels, sample_rate_option],
            outputs=[output_file, status_text]
        )
        
        clear_btn.click(
            fn=clear_recording,
            outputs=[microphone, status_text]
        )

def create_pitch_shifter_interface():
    """피치 조정 인터페이스 생성"""
    with gr.Column():
        gr.HTML("""
        <div style="text-align: center; padding: 20px;">
            <h2>🎵 피치 조정기</h2>
            <p>MP3 파일의 피치를 올리거나 내릴 수 있습니다.</p>
        </div>
        """)
        
        with gr.Tabs():
            # 단일 파일 처리 탭
            with gr.TabItem("단일 파일 처리"):
                with gr.Row():
                    with gr.Column():
                        # 단일 파일 입력 컴포넌트
                        audio_input = gr.Audio(
                            label="MP3 파일 업로드",
                            type="filepath",
                            format="mp3"
                        )
                        
                        pitch_slider_single = gr.Slider(
                            minimum=PITCH_CONFIG["min_pitch"],
                            maximum=PITCH_CONFIG["max_pitch"],
                            value=PITCH_CONFIG["default_pitch"],
                            step=PITCH_CONFIG["step"],
                            label="피치 조정 (반음)",
                            info="양수: 높게, 음수: 낮게 (-12 ~ +12 반음)"
                        )
                        
                        output_dir_single = gr.Textbox(
                            label="출력 폴더 경로 (선택사항)",
                            placeholder="예: C:\\Users\\사용자\\Music\\출력폴더 (비워두면 다운로드로 제공)",
                            info="폴더 경로를 입력하면 해당 위치에 직접 저장됩니다"
                        )
                        
                        process_btn_single = gr.Button("피치 조정하기", variant="primary")
                    
                    with gr.Column():
                        # 단일 파일 출력 컴포넌트
                        audio_output = gr.Audio(
                            label="조정된 오디오",
                            type="filepath"
                        )
                        
                        status_text_single = gr.Textbox(
                            label="처리 상태",
                            interactive=False
                        )
            
            # 배치 처리 탭
            with gr.TabItem("배치 처리 (여러 파일)"):
                with gr.Row():
                    with gr.Column():
                        # 배치 파일 입력 컴포넌트
                        files_input = gr.File(
                            label="MP3 파일들 업로드 (여러 파일 선택 가능)",
                            file_count="multiple",
                            file_types=PITCH_CONFIG["supported_formats"]
                        )
                        
                        pitch_slider_batch = gr.Slider(
                            minimum=PITCH_CONFIG["min_pitch"],
                            maximum=PITCH_CONFIG["max_pitch"],
                            value=PITCH_CONFIG["default_pitch"],
                            step=PITCH_CONFIG["step"],
                            label="피치 조정 (반음)",
                            info="양수: 높게, 음수: 낮게 (-12 ~ +12 반음)"
                        )
                        
                        output_dir_batch = gr.Textbox(
                            label="출력 폴더 경로 (선택사항)",
                            placeholder="예: C:\\Users\\사용자\\Music\\출력폴더 (비워두면 ZIP으로 다운로드)",
                            info="폴더 경로를 입력하면 해당 위치에 직접 저장됩니다"
                        )
                        
                        process_btn_batch = gr.Button("일괄 처리하기", variant="primary")
                    
                    with gr.Column():
                        # 배치 처리 출력 컴포넌트
                        batch_output = gr.File(
                            label="처리된 파일들 (ZIP)",
                            type="filepath"
                        )
                        
                        status_text_batch = gr.Textbox(
                            label="처리 상태",
                            interactive=False
                        )
        
        # 이벤트 바인딩
        process_btn_single.click(
            fn=process_single_audio,
            inputs=[audio_input, pitch_slider_single, output_dir_single],
            outputs=[audio_output, status_text_single]
        )
        
        process_btn_batch.click(
            fn=process_batch_files,
            inputs=[files_input, pitch_slider_batch, output_dir_batch],
            outputs=[batch_output, status_text_batch]
        )

def create_usage_guide():
    """사용법 가이드 생성"""
    with gr.Accordion("📖 사용법 및 팁", open=False):
        gr.Markdown("""
        ## 🎙️ 마이크 녹음 사용법:
        1. **마이크 권한 허용**: 브라우저에서 마이크 접근 권한을 허용해주세요
        2. **품질 설정**: 원하는 비트레이트, 채널, 샘플링 레이트를 선택하세요
        3. **녹음 시작**: 마이크 영역의 녹음 버튼을 클릭하여 녹음을 시작합니다
        4. **녹음 중지**: 다시 버튼을 클릭하여 녹음을 중지합니다
        5. **MP3 변환**: "녹음 처리" 버튼을 클릭하여 설정된 품질로 MP3 파일을 생성합니다
        
        ## 🎵 피치 조정 사용법:
        
        **단일 파일 처리:**
        1. MP3 파일을 업로드하세요
        2. 피치 조정값을 설정하세요
        3. (선택사항) 출력 폴더 경로를 입력하세요
        4. "피치 조정하기" 버튼을 클릭하세요
        
        **배치 처리 (여러 파일):**
        1. 여러 MP3 파일을 한 번에 선택해서 업로드하세요
        2. 피치 조정값을 설정하세요 (모든 파일에 동일하게 적용)
        3. (선택사항) 출력 폴더 경로를 입력하세요
        4. "일괄 처리하기" 버튼을 클릭하세요
        
        ## 💡 품질 설정 팁:
        - **음성 녹음**: 64-128kbps, 모노, 22kHz면 충분
        - **음악 녹음**: 192-256kbps, 스테레오, 44.1kHz 권장
        - **최고 품질**: 320kbps, 스테레오, 48kHz (용량 큼)
        
        ## 🎼 피치 조정 팁:
        - 1 반음 = 1 semitone (12반음 = 1옥타브)
        - 보컬 피치 올리기: +1 ~ +4 반음 추천
        - 지원 형식: MP3, WAV, M4A
        
        ## ⚙️ 출력 위치 설정:
        - **출력 폴더 경로를 입력한 경우**: 해당 폴더에 직접 저장됩니다
        - **출력 폴더를 비워둔 경우**: 웹에서 다운로드하거나 ZIP 파일로 제공됩니다
        - **경로 예시**: `C:\\Users\\사용자이름\\Music\\PitchShifted`
        
        ## ⚠️ 주의사항:
        - 마이크 접근 권한이 필요합니다
        - 높은 비트레이트는 파일 크기가 커집니다
        - 스테레오는 모노보다 약 2배 용량을 차지합니다
        - 배치 처리 시 진행률이 표시됩니다
        """)

def main():
    """메인 애플리케이션"""
    # 필요한 라이브러리 설치 안내
    install_info = """
이 프로그램을 실행하기 전에 다음 명령어로 라이브러리를 설치해주세요:

pip install -r requirements.txt

추가로 FFmpeg가 필요할 수 있습니다:
- Windows: https://ffmpeg.org/download.html
- macOS: brew install ffmpeg  
- Linux: sudo apt install ffmpeg
"""
    
    print(install_info)
    print("\n🎵 통합 오디오 처리기를 시작합니다...")
    
    # Gradio 인터페이스 생성
    with gr.Blocks(title=UI_TEXT["app_title"], theme=gr.themes.Soft()) as app:
        # 헤더
        gr.HTML(f"""
        <div style="text-align: center; padding: 20px; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 20px;">
            <h1 style="margin: 0; font-size: 2.5em;">{UI_TEXT["app_title"]}</h1>
            <p style="margin: 10px 0 0 0; font-size: 1.2em;">{UI_TEXT["app_description"]}</p>
        </div>
        """)
        
        # 메인 탭
        with gr.Tabs():
            # 마이크 녹음 탭
            with gr.TabItem(UI_TEXT["recorder_tab"]):
                create_recorder_interface()
            
            # 피치 조정 탭
            with gr.TabItem(UI_TEXT["pitch_tab"]):
                create_pitch_shifter_interface()
        
        # 사용법 가이드
        create_usage_guide()
        
        # 푸터
        gr.HTML("""
        <div style="text-align: center; padding: 20px; margin-top: 30px; border-top: 1px solid #eee; color: #666;">
            <p>🎵 <strong>통합 오디오 처리기</strong> | 고품질 오디오 녹음 및 피치 조정 도구</p>
            <p style="font-size: 0.9em;">imageio-ffmpeg & librosa 기반 | 개발: AI Assistant</p>
        </div>
        """)
    
    # 앱 실행
    app.launch(**SERVER_CONFIG)

if __name__ == "__main__":
    main()