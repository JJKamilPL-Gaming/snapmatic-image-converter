
import os
from argparse import ArgumentParser
from glob import glob

parser = ArgumentParser(description = "This tool allows you to convert GTA 5's in-game snapshots (taken using Snapmatic app in your protagonist's cellphone) to JPEG images. It also extracts the image's metadata and saves it in JSON format. ")
parser.add_argument("-i", help = "Folder containing ingame screenshots", required = True)
parser.add_argument("-o", help = "Folder where to save converted images", required = True)
args = parser.parse_args()

print("")

for path in glob(args.i + "/*"):
    
    print("Processing file: ", path, "...", end = " ")
    
    directory, filename = path.split("/")
    photo = open(path, "rb")

    image_data = bytearray()

    for i in range(292, os.path.getsize(path)):
        photo.seek(i)
        image_data += photo.read(1)
    
    out_photo = open(args.o + "/" + filename + ".jpg", "wb")
    out_photo = out_photo.write(image_data)
    photo.close()
    print("Done")

    json_data = bytearray()
    photo = open(path, "rb")

    photo.seek(os.path.getsize(path) - 3604)
    
    for j in range(((os.path.getsize(path) - 3604) + 1), ((os.path.getsize(path) - 3604) + 2000)):
        current_char = photo.read(1)
        next_char = photo.read(1)
        cc = str(current_char)
        nc = str(next_char)
        if(cc == "b'\\x00'" and nc == "b'\\x00'"):
            break
        else:
            json_data += current_char
            photo.seek(j)
    
    out_json = open(args.o + "/" + filename + ".json", "wb")
    out_json = out_json.write(json_data)
    photo.close()
    
print("")
print("All files successfully converted")