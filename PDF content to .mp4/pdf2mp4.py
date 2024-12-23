
from PIL import Image
import pytesseract
from mutagen.mp3 import MP3
from moviepy.editor import VideoFileClip
import moviepy.editor as mpe
from gtts import gTTS
from pdf2image import convert_from_path
import os
import sys

def pdf2text(PDF_file):
    """Extract text from a PDF file."""
    try:
        
        pages = convert_from_path(PDF_file, 300)  
        image_counter = 1
        text = ""

        print("Converting PDF pages to images...")
        for page in pages:
            filename = f"page_{image_counter}.jpg"
            page.save(filename, 'JPEG')
            image_counter += 1

        print("Extracting text from images...")
        for i in range(1, image_counter):
            filename = f"page_{i}.jpg"
            text += pytesseract.image_to_string(Image.open(filename))
            os.remove(filename)  
        text = text.replace('-\n', '')  
        return text

    except Exception as e:
        print(f"Error processing PDF: {e}")
        sys.exit(1)

def text2video(mtext, video_file, pdf_file_name):
    """Combine extracted text as audio with a video."""
    if not mtext.strip():
        print("Error: No text found in the PDF.")
        sys.exit(1)

    try:
        language = 'en'
        print("Converting text to speech...")
        myobj = gTTS(text=mtext, lang=language, slow=False)
        audio_file = "output.mp3"
        myobj.save(audio_file)

        audio = MP3(audio_file)
        audio_length = int(audio.info.length)

        print("Processing the video file...")
        videoclip = VideoFileClip(video_file)

        if int(videoclip.duration) > audio_length:
            videoclip = videoclip.subclip(0, audio_length)

        background_music = mpe.AudioFileClip(audio_file)
        new_clip = videoclip.set_audio(background_music)

        output_video_name = pdf_file_name.split(".pdf")[0] + "(video).mp4"
        new_clip.write_videofile(output_video_name, codec='libx264', audio_codec='aac')

        print(f"Video saved as: {output_video_name}")
        os.remove(audio_file)  # Clean up temporary audio file

    except Exception as e:
        print(f"Error creating video: {e}")
        sys.exit(1)

if __name__ == "__main__":

    PDF_file = input("Enter the name of PDF file with extension (e.g., file.pdf): ")

    if not os.path.exists(PDF_file) or not PDF_file.lower().endswith('.pdf'):
        print(f"Error: File '{PDF_file}' does not exist or is not a PDF.")
        sys.exit(1)

    
    video_file = input("Enter the name of video file with extension (e.g., file.mp4): ")

    if not os.path.exists(video_file) or not video_file.lower().endswith(('.mp4', '.mov', '.avi')):
        print(f"Error: File '{video_file}' does not exist or is not a valid video format.")
        sys.exit(1)

    
    text = pdf2text(PDF_file)

    
    text2video(text, video_file, PDF_file)

