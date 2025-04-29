import yt_dlp
import ffmpeg
import os
import shutil

def convert_mp4_to_gif(mp4_folder, gif_folder):
    if not os.path.exists(gif_folder):
        os.makedirs(gif_folder)
    
    for filename in os.listdir(mp4_folder):
        if filename.endswith('.mp4'):
            mp4_path = os.path.join(mp4_folder, filename)
            gif_filename = f"{os.path.splitext(filename)[0]}.gif" 
            gif_path = os.path.join(gif_folder, gif_filename)

            (
                ffmpeg
                .input(mp4_path)
                .output(gif_path, vf="fps=10,scale=320:-1:flags=lanczos")
                .run()
            )

            print(f"✔️ Converted: {gif_path}")

def to_seconds(t):
    parts = [float(p) for p in t.split(':')]
    if len(parts) == 1:
        return parts[0]
    elif len(parts) == 2:
        return parts[0] * 60 + parts[1]
    elif len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    else:
        raise ValueError(f"Invalid time format: {t}")

def _get_duration(start, end):
    return to_seconds(end) - to_seconds(start)

def cut_video(input_path, cuts, output_folder):
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i, cut in enumerate(cuts, 1):
        start = cut['start']
        end = cut['end']
        duration = _get_duration(start, end)
        output_file = os.path.join(output_folder, f"cut_{i:02d}_{start.replace(':','-')}_{end.replace(':','-')}.mp4")

        (
            ffmpeg
            .input(input_path, ss=start, t=duration)
            .output(output_file, c='copy')
            .run(overwrite_output=True)
        )

        print(f"✔️ Saved: {output_file}")

def get_YouTube_Video(url):

    temp_folder = './temp/'
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(temp_folder, '%(title)s.%(ext)s')
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(result)

def clean_folders(folder_path):

    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        
        print(f"✔️ Deleted folder: {folder_path}")
    else:
        print(f"⚠️ Folder not found: {folder_path}")

def get_Infos():
    cuts = []
    videoURL = input('Paste the YouTube video link: ')

    while True:
        start = input("Start time: ").strip()
        if start.lower() == "done":
            break

        end = input("End time: ").strip()
        if end.lower() == "done":
            break

        cuts.append({"start": start, "end": end})
        print(f"✔️ Cut added: {start} - {end}\n")
        print(f"Type 'done' at any time to finish entering cuts")

    video_path = get_YouTube_Video(videoURL)

    print("----------")
    print("\n🎬 Creating Cuts:")
    for i, cut in enumerate(cuts, 1):
        print("------")
        print(f"{i}. {cut['start']} - {cut['end']}")

    cut_video(video_path, cuts, './cuts')
    convert_mp4_to_gif('./cuts', './gifs')
    clean_folders('./temp')
    clean_folders('./cuts')

if __name__ == "__main__":
    get_Infos()

