# import os
# import cv2
# import easyocr
# import subprocess
# import yt_dlp
# import json
# import csv
# from youtubesearchpython import VideosSearch
# import yt_dlp as youtube_dl
# import re




# # cookies generator
# def get_youtube_cookies():
#     browsers = [
#         ('firefox', None, None, None),
#         ('chrome', None, None, None),
#         ('chromium', None, None, None),
#         ('opera', None, None, None),
#         ('brave', None, None, None),
#     ]

#     for browser_spec in browsers:
#         try:
#             print(f"Attempting to retrieve cookies from {browser_spec[0]}...")
#             return browser_spec
#         except Exception as e:
#             print(f"Could not get cookies from {browser_spec[0]}: {str(e)}")
    
#     print("No valid cookies found in any supported browser.")
#     return None

# """Search for YouTube video links based on a query using regex."""
# def get_video_links(query, limit=5):
#     videosSearch = VideosSearch(query, limit=limit*2)  # Fetch more results initially
#     results = videosSearch.result()

#     video_links = []
#     query_lower = query.lower()
#     query_pattern = re.compile(re.escape(query_lower), re.IGNORECASE)

#     for video in results['result']:
#         title = video['title'].lower()
#         if query_pattern.search(title):
#             video_links.append(video['link'])
#             video_links.append(video['title'])

#         if len(video_links) >= limit*2:
#             break

#     return video_links[:limit*2]



# def convert_to_mp4(input_file, output_file):
#     command = [
#         'ffmpeg',
#         '-i', input_file,
#         '-c:v', 'libx264',
#         '-c:a', 'aac',
#         output_file
#     ]
   
#     try:
#         subprocess.run(command, check=True, capture_output=True, text=True)
#         print(f"Successfully converted {input_file} to {output_file}")
#     except subprocess.CalledProcessError as e:
#         print(f"An error occurred during conversion: {e}")
#         print(f"FFmpeg output: {e.output}")    



# def download_youtube_video(url, download_folder):

#     if not os.path.exists(download_folder):
#     # Create the directory if it does not exist
#        os.makedirs(download_folder)
#        print(f"Directory {download_folder} created.")
#     else:
#        print(f"Directory {download_folder} already exists.")

#     browser_spec = get_youtube_cookies()
#     if not browser_spec:
#         print("No cookies found. Attempting download without authentication.")
#         ydl_opts = {}
#     else:    
#         ydl_opts = {
#             'cookiesfrombrowser': browser_spec,
#             'outtmpl': os.path.join(download_folder, 'video.%(ext)s'),
#             'writesubtitles': True,
#             'subtitlesformat': 'vtt',
#             'subtitleslangs': ['en'],
#             'writeautomaticsub': True
#         }
#     try:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info_dict = ydl.extract_info(url, download=True)
#             video_title = info_dict.get('title', None)
#             print(f"Title: {video_title}")
#     except Exception as e:
#         print(f"An error occurred during download: {str(e)}")

#     files = os.listdir(download_folder)
#     if files[0].endswith('.mp4'):
#        input_file=os.path.join(download_folder, files[0])
#        return input_file
    
#     video_path = os.path.join(download_folder, 'video.mp4')
#     input_file=os.path.join(download_folder, files[0])
#     convert_to_mp4(input_file=input_file,output_file=video_path)
#     os.remove(input_file)
#     return video_path


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


# def convert_subtitles_to_srt(vtt_file):
#     srt_file = vtt_file.replace('.vtt', '.srt')
#     try:
#         subprocess.run(['ffmpeg', '-i', vtt_file, srt_file], check=True)
#         return srt_file
#     except subprocess.CalledProcessError as e:
#         print(f"Error converting subtitles: {e}")
#         return None

# def extract_text_from_srt(srt_file, subtitle_dir):
#     text = []
#     with open(srt_file, 'a+', encoding='utf-8') as file:
#         for line in file:
#             line = line.strip()
#             if line and not line.isdigit() and not line.startswith('00:'):
#                 text.append(line)
#     subtitle_text = '\n'.join(text)

#     if not os.path.exists(subtitle_dir):
#         os.makedirs(subtitle_dir)

#     subtitle_filename = os.path.join(subtitle_dir, os.path.basename(srt_file).replace('.srt', '.txt'))
#     with open(subtitle_filename, 'a+', encoding='utf-8') as file:
#         file.write(subtitle_text)

#     return subtitle_filename


# def merge_text_files(subtitle_text_path, frame_text_path, output_folder):
#     if not os.path.exists(subtitle_text_path) and not os.path.exists(frame_text_path):
#         return None

#     merged_texts = []
#     if os.path.exists(subtitle_text_path):
#         with open(subtitle_text_path, 'r+', encoding='utf-8') as file:
#             merged_texts.append(file.read())



#     if os.path.exists(frame_text_path):
#         with open(frame_text_path, 'r+', encoding='utf-8') as file:
#             merged_texts.append(file.read())



#     output_path1 = os.path.join(output_folder,"main_json.json")
#     output_path2 = os.path.join(output_folder,"main_csv.csv")


#     # Save to JSON file
#     json_data = {'texts': merged_texts}
#     with open(output_path1, 'a+', encoding='utf-8') as json_file:
#         json.dump(json_data, json_file, indent=4)

#     # Save to CSV file
#     with open(output_path2, "a+", newline='', encoding='utf-8') as csv_file:
#         writer = csv.writer(csv_file)
#         for text in merged_texts:
#             writer.writerow([text])

#     os.remove(subtitle_text_path)
#     os.remove(frame_text_path)

#     return output_path1, output_path2



# def main(query, limit=3,output_folder='./output',subtitle_dir = './sub_title',frame_text_output_dir = './frame_text'):


#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

#     video_links = get_video_links(query, limit)
#     if not video_links:
#         print(f"No close matches found for '{query}'")
#         return

#     for i in range(0, len(video_links), 4):
#         chunk = video_links[i:i+4]
#         for index in range(0, len(chunk), 2):
#             video_url = chunk[index]
#             video_title = chunk[index + 1]
#             print(f"Processing video URL: {video_url}")
#             print(f"Video Title: {video_title}")

#             video_path = download_youtube_video(video_url, output_folder)

#             print("video path where video saved", video_path)


#             print(os.listdir(output_folder))
#             vtt_files = [f for f in os.listdir(output_folder) if f.endswith('.vtt')]

#             if not vtt_files:
#                print(f"No VTT file found for video: {video_links}")
#                continue

#             vtt_file = os.path.join(output_folder, vtt_files[0])

#             srt_file = convert_subtitles_to_srt(vtt_file)

#             if not srt_file:
#                 continue

#             subtitle_text_path = extract_text_from_srt(srt_file, subtitle_dir)
#             if not subtitle_text_path:
#                 print(f"Failed to extract text from subtitles for video: {video_links}")

#             frame_text_path = extract_text_from_video_frames(video_path, frame_text_output_dir)

#             json_path ,csv_path = merge_text_files(subtitle_text_path, frame_text_path, output_folder)
#             if json_path and csv_path:
#                 print(f"Merged text saved to {json_path} {csv_path}")

#             os.remove(vtt_file)
#             os.remove(srt_file)
#             os.remove(video_path)
#             print("video is deleted after successful processing of vid to text :))")





# if __name__ == '__main__':
#     query = 'chicken masala'
#     main(query = 'chicken masala',limit=8,output_folder = './output',subtitle_dir = './sub_title',frame_text_output_dir = './frame_text')
import os
import cv2
import easyocr
import subprocess
import yt_dlp
import json
import csv
from youtubesearchpython import VideosSearch
import re

# cookies generator
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

def get_video_links(query, limit=5):
    videosSearch = VideosSearch(query, limit=limit*2)
    results = videosSearch.result()

    video_links = []
    query_lower = query.lower()
    query_pattern = re.compile(re.escape(query_lower), re.IGNORECASE)

    for video in results['result']:
        title = video['title'].lower()
        if query_pattern.search(title):
            video_links.append(video['link'])
            video_links.append(video['title'])

        if len(video_links) >= limit*2:
            break

    return video_links[:limit*2]

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
    video_extensions = [
     '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm', '.m4v', '.3gp', 
    '.mpeg', '.mpg', '.m2v', '.ogv', '.mxf', '.ts', '.vob', '.divx', '.rm', 
    '.rmvb', '.asf'
]
    if not os.path.exists(download_folder):
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
    mp4_files = [file for file in files if file.lower().endswith('.mp4')]
    mp4_files=str(mp4_files).strip("['] ")
    print(mp4_files)

    if mp4_files:
       input_file=os.path.join(download_folder, mp4_files)
       return input_file
    
    video_files = [file for file in files if any(file.lower().endswith(ext) for ext in video_extensions)]
    video_file=str(video_files).strip("['] ")
    video_path = os.path.join(download_folder, 'video.mp4')
    input_file=os.path.join(download_folder, video_file)
    convert_to_mp4(input_file=input_file,output_file=video_path)
    os.remove(input_file)
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
                if confidence >= 0.10 and text not in video_texts:
                    video_texts.append(text)
                    print(f"Frame {frame_index} - Extracted Text: {text} (Confidence: {confidence})")

        frame_index += 1

    video.release()
   
    if video_texts:
        if not os.path.exists(text_output_dir):
            os.makedirs(text_output_dir)

        video_text_file = os.path.join(text_output_dir, os.path.basename(video_path).replace('.mp4', '_frames.txt'))
        with open(video_text_file, 'a+', encoding='utf-8') as file:
            file.write('\n'.join(video_texts))

        return video_text_file
    return None

def convert_subtitles_to_srt(vtt_file):
    srt_file = vtt_file.replace('.vtt', '.srt')
    try:
        subprocess.run(['ffmpeg', '-i', vtt_file, srt_file, '-y'], check=True)  # Add '-y' to force overwrite
        return srt_file
    except subprocess.CalledProcessError as e:
        print(f"Error converting subtitles: {e}")
        return None

def extract_text_from_srt(srt_file, subtitle_dir):
    text = []
    with open(srt_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line and not line.isdigit() and not line.startswith('00:'):
                text.append(line)
    subtitle_text = '\n'.join(text)

    if not os.path.exists(subtitle_dir):
        os.makedirs(subtitle_dir)

    subtitle_filename = os.path.join(subtitle_dir, os.path.basename(srt_file).replace('.srt', '.txt'))
    with open(subtitle_filename, 'w', encoding='utf-8') as file:
        file.write(subtitle_text)

    return subtitle_filename

def merge_text_files(subtitle_text_path, frame_text_path, output_folder):
    if not os.path.exists(subtitle_text_path) and not os.path.exists(frame_text_path):
        return None

    merged_texts = []
    if os.path.exists(subtitle_text_path):
        with open(subtitle_text_path, 'r', encoding='utf-8') as file:
            merged_texts.append(file.read())

    if os.path.exists(frame_text_path):
        with open(frame_text_path, 'r', encoding='utf-8') as file:
            merged_texts.append(file.read())

    output_path1 = os.path.join(output_folder, "main_json.json")
    output_path2 = os.path.join(output_folder, "main_csv.csv")

    # Save to JSON file
    json_data = {'texts': merged_texts}
    with open(output_path1, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, indent=4)

    # Save to CSV file
    with open(output_path2, "w", newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for text in merged_texts:
            writer.writerow([text])

    if os.path.exists(subtitle_text_path):
        os.remove(subtitle_text_path)
    if os.path.exists(frame_text_path):
        os.remove(frame_text_path)

    return output_path1, output_path2

def main(query, limit=3, output_folder='./output', subtitle_dir='./sub_title', frame_text_output_dir='./frame_text'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video_links = get_video_links(query, limit)
    if not video_links:
        print(f"No close matches found for '{query}'")
        return

    for i in range(0, len(video_links), 2):
        video_url = video_links[i]
        video_title = video_links[i + 1]
        print(f"Processing video URL: {video_url}")
        print(f"Video Title: {video_title}")

        video_path = download_youtube_video(video_url, output_folder)
        print("Video path where video saved:", video_path)

        print(os.listdir(output_folder))
        vtt_files = [f for f in os.listdir(output_folder) if f.endswith('.vtt')]

        if not vtt_files:
            print(f"No VTT file found for video: {video_links}")
            continue

        vtt_file = vtt_files[0]
        vtt_file_path = os.path.join(output_folder, vtt_file)
        srt_file_path = convert_subtitles_to_srt(vtt_file_path)

        frame_text_path = extract_text_from_video_frames(video_path, frame_text_output_dir)
        subtitle_text_path = extract_text_from_srt(srt_file_path, subtitle_dir)

        if frame_text_path and subtitle_text_path:
            output_json_path, output_csv_path = merge_text_files(subtitle_text_path, frame_text_path, output_folder)
            print(f"Merged text file created at: {output_json_path}")
            print(f"Merged CSV file created at: {output_csv_path}")
        else:
            print("No texts extracted from video frames or subtitles.")

if __name__ == "__main__":
    query = "Chicken Masala"
    main(query)

