from os import listdir
import shutil, os
import subprocess
from os.path import isfile

# Download ffmpeg essentials (do not use master build)


# def convert_and_move(path, new_folder, path_to_ffmpeg, new_sound_file_type):
#     f_names = [f_name for f_name in listdir(path)]
#     new_folder = path + "/" + new_folder
#     try:
#         os.mkdir(new_folder)
#     except:
#         pass
#     for filename in f_names:
#         file = path + '/' + filename
#         if file.endswith('webm') and isfile(file):
#             command = ['ffmpeg', '-i', file, (new_folder + '/' + filename).replace('webm', new_sound_file_type)]
#             subprocess.Popen(command, env={'PATH': path_to_ffmpeg}, shell=True)
#         elif isfile(file):
#             shutil.copyfile(file, new_folder + "/" + filename)

def convert_to_wav(path, new_folder, path_to_ffmpeg):
    f_names = [f_name for f_name in listdir(path)]
    new_folder = path + "/" + new_folder
    try:
        os.mkdir(new_folder)
    except:
        pass
    for index, filename in enumerate(f_names):
        print(index, "   file: ", filename)
        file = path + '/' + filename
        if isfile(file):
            f = file.split('.')
            command = ['ffmpeg', '-i', file, (new_folder + '/' + filename).replace(f[2], 'wav')]
            print(command)
            subprocess.Popen(command, env={'PATH': path_to_ffmpeg}, shell=True)


# convert_to_wav("./data/covid", 'wav', 'C:/ffmpeg_essentials_build/bin')
# convert_to_wav("./data/symptomatic", 'wav', 'C:/ffmpeg_essentials_build/bin')
convert_to_wav("./data/healthy", 'wav', 'C:/ffmpeg_essentials_build/bin')
print("done")

