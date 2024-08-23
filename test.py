import ffmpeg
import subprocess
import os
import yt_dlp
import cv2
import easyocr
import csv
from openai import OpenAI
import instaloader




class InstaLoader():
  def __init__(self):
    self.L = instaloader.Instaloader()

  def login_and_save_session(self,username, password):
    self.L.login(username, password)
    self.L.save_session_to_file()

  def load_session_file(self,username):
      self.L = instaloader.Instaloader()
      self.L.load_session_from_file(username)

  def get_video(self,url):
    shortcode = url.split('/')[-2]

    # Load the post using the shortcode
    post = instaloader.Post.from_shortcode(self.L.context, shortcode)

    # Download the video(s) from the post
    if post.is_video:
        print(f"Downloading video from {url}")
        self.L.download_post(post, target=f'videos/{shortcode}')

    else:
        print("The post does not contain a video.")

    print("Download completed!")

loader = InstaLoader()
# loader.login_and_save_session('shubhchaturvedi63', 'shubh2006')
loader.load_session_file('aakashkhamaru')


import shutil

def get_description(url, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Directory {output_folder} created.")
    else:
        print(f"Directory {output_folder} already exists.")

    # Extract the shortcode from the URL
    shortcode = url.split('/')[-2]
    folder = f'videos/{shortcode}'

    try:
        # Attempt to download the video
        loader.get_video(url)
    except Exception as e:
        print(f"Error downloading video: {e}")
        print("Proceeding without video download.")

    # Define the path for the combined output file
    output_file_path = os.path.join(output_folder, 'combined_output.txt')

    # Check if the video folder exists
    if not os.path.exists(folder):
        print(f"Warning: Directory {folder} does not exist. There may be no video content.")
        return

    with open(output_file_path, 'a', encoding='utf-8') as output_file:
        try:
            for filename in os.listdir(folder):
                if filename.endswith('.txt'):
                    file_path = os.path.join(folder, filename)
                    with open(file_path, 'r', encoding='utf-8') as txt_file:
                        # Read the content of the file
                        content = txt_file.read()
                        # Write content to the output file
                        output_file.write(f"--- Start of {filename} ---\n")
                        output_file.write(content + '\n')
                        output_file.write(f"--- End of {filename} ---\n\n")
        except FileNotFoundError:
            print(f"Error: Could not find or access the directory {folder}")
        except Exception as e:
            print(f"An error occurred while processing files: {e}")

    print("Description extraction completed.")

    # Optional: Clean up the videos folder if it exists
    if os.path.exists(folder):
        shutil.rmtree(folder)
        print(f"Cleaned up temporary folder: {folder}")

# Example usage
# url = 'https://example.com/video-url'  # Replace with your video URL
# output_folder = '/content/videos/output'  # Replace with your desired output folder
# get_description(url, output_folder)

    
# def correct_food_ingredients(api_key, user_prompt):
#     client = OpenAI(api_key=api_key)
#     system_prompt = (
#         "You are an advanced language model specialized in food ingredients. "
#         "Your task is to process and correct food ingredient names. "
#         "1. If a word is a broken English or misspelled food ingredient, correct it to the proper name. "
#         "2. If a word is already correct, pass it through as is. "
#         "3. Ensure that no word is repeated in the output. "
#         "4. ignore those word which is not repleted to food ingredient "
#         "Provide the corrected list of unique food ingredients."
#     )

#     completion = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {
#                 "role": "system",
#                 "content": system_prompt,
#             },
#             {
#                 "role": "user",
#                 "content": user_prompt,
#             }
#         ]
#     )

#     ret = completion.choices[0].message.content
#     print(ret)
#     return ' '.join(ret.split('\n'))

def correct_food_ingredients(api_key, user_prompt):
    client = OpenAI(api_key=api_key)
    system_prompt = (
        "You are an AI specialized in correcting and formatting food ingredient names. "
        "1. Correct any misspelled or broken English food ingredient names. "
        "2. Preserve correct food ingredient names or words which are relarted to food preparation as they are. "
        "3. Do not repeat word. "

    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            }
        ]
    )

    ret = completion.choices[0].message.content
    print(ret)
    return ' '.join(ret.split('\n'))




def get_youtube_cookies():
    browsers = [
        ('firefox', None, None, None),
        ('chrome', None, None, None),
        ('chromium', None, None, None),
        ('opera', None, None, None),
        ('brave', None, None, None),
    ]

    for browser_spec in browsers:
        try:
            print(f"Attempting to retrieve cookies from {browser_spec[0]}...")
            return browser_spec
        except Exception as e:
            print(f"Could not get cookies from {browser_spec[0]}: {str(e)}")
    
    print("No valid cookies found in any supported browser.")
    return None


def convert_to_mp4(input_file, output_file):
    command = [
        'ffmpeg',
        '-i', input_file,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        output_file
    ]
   
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Successfully converted {input_file} to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during conversion: {e}")
        print(f"FFmpeg output: {e.output}")    

def download_youtube_video(url, download_folder):

    if not os.path.exists(download_folder):
    # Create the directory if it does not exist
       os.makedirs(download_folder)
       print(f"Directory {download_folder} created.")
    else:
       print(f"Directory {download_folder} already exists.")

    browser_spec = get_youtube_cookies()
    if not browser_spec:
        print("No cookies found. Attempting download without authentication.")
        ydl_opts = {}
    else:    
        ydl_opts = {
            'cookiesfrombrowser': browser_spec,
            'outtmpl': os.path.join(download_folder, 'video.%(ext)s'),
            'writesubtitles': True,
            'subtitlesformat': 'vtt',
            'subtitleslangs': ['en'],
            'writeautomaticsub': True
        }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', None)
            print(f"Title: {video_title}")
    except Exception as e:
        print(f"An error occurred during download: {str(e)}")

    files = os.listdir(download_folder)
    if files[0].endswith('.mp4'):
       input_file=os.path.join(download_folder, files[0])
       print("hello")
       return input_file
    
    video_path = os.path.join(download_folder, 'video.mp4')
    input_file=os.path.join(download_folder, files[0])
    convert_to_mp4(input_file=input_file,output_file=video_path)
    os.remove(input_file)
    print("heloo2")
    return video_path

def extract_text_from_video_frames(video_path, text_output_dir):
    video = cv2.VideoCapture(video_path)
    reader = easyocr.Reader(['en'])

    if not video.isOpened():
        print("PATH IS ", video_path)
        raise ValueError("Error opening video stream or file")

    frame_index = 0
    video_texts = []
   
    while True:
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = video.read()
        if not ret:
            break

        output = reader.readtext(frame)
        for item in output:
            if len(item) == 3:
                bbox, text, confidence = item
                if confidence >= 0.90 and text not in  video_texts:
                    video_texts.append(text)
                    print(f"Frame {frame_index} - Extracted Text: {text} (Confidence: {confidence})")

        frame_index += 1

    video.release()
   

    if video_texts:
        if not os.path.exists(text_output_dir):
            os.makedirs(text_output_dir)

        video_texts = '\n'.join(video_texts)    
        corrected_video_text = correct_food_ingredients(api_key,video_texts)
        print(corrected_video_text)
        video_text_file = os.path.join(text_output_dir, os.path.basename(video_path).replace('.mp4', '_frames.txt'))
        with open(video_text_file, 'a+', encoding='utf-8') as file:
            file.write(' '.join(corrected_video_text))

        return video_text_file
    return None



if __name__ == '__main__':

    insta_link_file_path = '/root/youtubetxtextract/instagram.csv'
    urls = []
    with open(insta_link_file_path, 'r') as file:
        csv_reader = csv.reader(file)  # Corrected to `csv.reader`
        for row in csv_reader:
            # Assuming the URLs are in the first column of the CSV
            urls.append(row[0])
    
    for url in urls:
        print(url)
        get_description(url,"/root/youtubetxtextract/descr_output")
        x=download_youtube_video(url,"/root/youtubetxtextract/test_output")
        print(x)
        extract_text_from_video_frames(video_path=x,text_output_dir="/root/youtubetxtextract/test_output")  
    




# def extract_text_from_video_frames(video_path, text_output_dir):
#     video = cv2.VideoCapture(video_path)
#     reader = easyocr.Reader(['en'])

#     if not video.isOpened():
#         print("PATH IS ", video_path)
#         raise ValueError("Error opening video stream or file")

#     frame_index = 0
#     video_texts = []
   
#     while True:
#         video.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
#         ret, frame = video.read()
#         if not ret:
#             break

#         output = reader.readtext(frame)
#         for item in output:
#             if len(item) == 3:
#                 bbox, text, confidence = item
#                 if confidence >= 0.10 and text not in  video_texts:
#                     video_texts.append(text)
#                     print(f"Frame {frame_index} - Extracted Text: {text} (Confidence: {confidence})")

#         frame_index += 1

#     video.release()
   

#     if video_texts:
#         if not os.path.exists(text_output_dir):
#             os.makedirs(text_output_dir)

#         video_text_file = os.path.join(text_output_dir, os.path.basename(video_path).replace('.mp4', '_frames.txt'))
#         with open(video_text_file, 'a+', encoding='utf-8') as file:
#             file.write('\n'.join(video_texts))

#         return video_text_file
#     return None








# def video_to_frames_url_auto(url, folder):
#     """Extract frames from a video URL."""
#     if not os.path.exists(folder):
#         os.makedirs(folder)

#     video_path = download_youtube_video(url, folder)
#     if video_path is None:
#         print("Error: Video file not downloaded or path is None.")
#         return

#     print(f"Video Path: {video_path}")

#     video = cv2.VideoCapture(video_path)
#     if not video.isOpened():
#         raise ValueError(f"Error opening video stream or file. Path: {video_path}")

#     frame_index = 0
#     while True:
#         ret, frame = video.read()
#         if not ret:
#             print(f"No more frames to read or error at frame index {frame_index}.")
#             break

#         frame_filename = os.path.join(folder, f'frame_{frame_index:04d}.jpg')
#         cv2.imwrite(frame_filename, frame)
#         print(f"Frame {frame_index} saved.")
#         frame_index += 1

#     video.release()
#     print(f"Extracted {frame_index} frames to '{folder}'")

# def extract_text_from_images(folder_path, output_text_folder):
#     """Extract text from images using OCR and associate it with frame numbers."""
#     images = sorted([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])

#     seen_texts = set()
#     output_file_path = os.path.join(output_text_folder, "extracted_text.txt")

#     with open(output_file_path, "w", encoding="utf-8") as f:  # Open file once for writing
#         for image in images:
#             image_path = os.path.join(folder_path, image)
#             if image_path.lower().endswith((".jpg", ".jpeg", ".png")):
#                 frame_number = image.split('_')[1].split('.')[0]  # Extract frame number from filename
#                 output = reader.readtext(image_path)
#                 for item in output:
#                         if len(item) == 3:
#                             bbox, text, confidence = item
#                             if confidence >= 0.10 and text not in seen_texts:
#                                 seen_texts.add(text)
#                                 f.write(f"Frame {frame_number}: {text} (Confidence: {confidence})\n")
#                                 print(f"Frame {frame_number} - Extracted Text: {text} (Confidence: {confidence})")