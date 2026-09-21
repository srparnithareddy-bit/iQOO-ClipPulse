# iQOO ClipPulse 🎮⚡

iQOO ClipPulse is an AI-powered automated video editing engine built for gamers. It uses Audio Peak Analysis and Screen Text Recognition (OCR) to detect key gameplay moments (Kills, Victories, Headshots) and generates vertical 9:16 reels instantly.

## 🚀 Key Features
- **Dual Intelligence Detection:** Combines volume decibel peaks with OpenCV + EasyOCR keyword detection.
- **Auto-Cropping Engine:** Converts standard landscape 16:9 gameplay footage into 9:16 short vertical reels using FFmpeg.
- **Seamless Integration Setup:** Designed for iQOO Ultra Game Mode / Monster Mode overlay triggers.

## 🛠️ Tech Stack
- **AI Backend:** Python 3, SciPy, NumPy, OpenCV, EasyOCR
- **Media Engine:** FFmpeg
- **Mobile Architecture:** Android Kotlin (MediaProjection API + Foreground Service)

## 💻 How to Run Locally

### 1. Prerequisites
Ensure you have **FFmpeg** installed on your system.

### 2. Install Dependencies
```bash
pip install scipy numpy opencv-python easyocr