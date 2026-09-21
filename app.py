import os
import subprocess
import numpy as np
from scipy.io import wavfile
import cv2
import easyocr

# Initialize OCR Reader (English)
reader = easyocr.Reader(['en'], gpu=False)

def detect_highlight_timestamp(video_path):
    print("🔍 Step 1: Audio Peak & Screen Text OCR Analysis combinedly running...")
    
    # 1. Extract Audio
    temp_audio = "temp_audio.wav"
    subprocess.run([
        'ffmpeg', '-y', '-i', video_path, 
        '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '1', temp_audio
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    sample_rate, data = wavfile.read(temp_audio)
    chunk_size = sample_rate
    num_chunks = len(data) // chunk_size
    chunk_volumes = []
    
    for i in range(num_chunks):
        chunk = data[i * chunk_size : (i + 1) * chunk_size]
        volume = np.max(np.abs(chunk)) if len(chunk) > 0 else 0
        chunk_volumes.append(volume)
        
    audio_peak_second = int(np.argmax(chunk_volumes))
    
    if os.path.exists(temp_audio):
        os.remove(temp_audio)

    # 2. OCR Text Analysis (Checking for KILL/VICTORY/HEADSHOT keywords)
    print("🎯 Step 2: Game Screen Frame OCR Scan running...")
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_sec = frame_count // fps
    
    keywords = ["KILL", "VICTORY", "HEADSHOT", "KNOCKED", "ELIMINATED", "WINNER"]
    ocr_detected_second = None
    
    # Every 2 seconds frame capture & scan
    for sec in range(0, duration_sec, 2):
        cap.set(cv2.CAP_PROP_POS_FRAMES, sec * fps)
        ret, frame = cap.read()
        if not ret:
            continue
            
        results = reader.readtext(frame, detail=0)
        detected_text = " ".join(results).upper()
        
        for kw in keywords:
            if kw in detected_text:
                print(f"🔥 OCR Text Detected Keyword '{kw}' at {sec} seconds mark!")
                ocr_detected_second = sec
                break
        if ocr_detected_second:
            break
            
    cap.release()
    
    # Decision Engine: Give priority to OCR, fallback to Audio Peak
    final_highlight = ocr_detected_second if ocr_detected_second is not None else audio_peak_second
    print(f"🏆 Final AI Target Highlight Time: {final_highlight} seconds!")
    return final_highlight

def generate_vertical_reel(video_path, best_second, output_reel_path):
    print("✂️ Step 3: Highlighting reel cropping (9:16 format)...")
    
    start_time = max(0, best_second - 4)
    duration = 8  # 8-second Reel
    
    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-ss', str(start_time),
        '-i', video_path,
        '-t', str(duration),
        '-vf', 'crop=ih*(9/16):ih',
        '-c:a', 'copy',
        output_reel_path
    ]
    
    subprocess.run(ffmpeg_cmd)
    print(f"✅ Enhanced AI Reel Generated Successfully: {output_reel_path}")

if __name__ == "__main__":
    input_video = "sample_gameplay.mp4" 
    output_reel = "iQOO_ClipPulse_Reel.mp4"
    
    if os.path.exists(input_video):
        peak_second = detect_highlight_timestamp(input_video)
        generate_vertical_reel(input_video, peak_second, output_reel)
    else:
        print("⚠️ Folder lo 'sample_gameplay.mp4' file kanipinchaledhu!")