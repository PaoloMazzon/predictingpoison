from zlib import compress
from PIL import Image
import numpy as np
from math import sqrt
from os import listdir
from os.path import isfile, join
import json

def get_png_bytes(file_path):
    img = Image.open(file_path).convert("RGB")
    return np.array(img).tobytes()

def get_png_array(file_path):
    img = Image.open(file_path).convert("RGB")
    return np.array(img)

# Returns a number from 0-1 representing entropy using the zip method
def zip_entropy(file_path):
    byte_array = get_png_bytes(file_path)
    compressed_bytes = compress(byte_array, level = 1)
    return len(compressed_bytes) / len(byte_array)

# Returns a number from 0-1 representing entropy using the luminance method
def luminance_entropy(file_path):
    def rgb_luminance(r, g, b):
        return sqrt( 0.299 * (float(r / 255) ** 2) + 0.587 * (float(g / 255) ** 2) + 0.114 * (float(b / 255) ** 2))
    ia = get_png_array(file_path)
    image_luminance = []
    for y in range(len(ia)):
        image_luminance.append([])
        for x in range(len(ia[y])):
            image_luminance[y] += [rgb_luminance(ia[y][x][0], ia[y][x][1], ia[y][x][2])]
    luminance_differentials = []
    for y in range(1, len(ia) - 1):
        for x in range(1, len(ia[y]) - 1):
            luminance_differentials += [abs(image_luminance[y - 1][x] - image_luminance[y][x])]
            luminance_differentials += [abs(image_luminance[y + 1][x] - image_luminance[y][x])]
            luminance_differentials += [abs(image_luminance[y][x - 1] - image_luminance[y][x])]
            luminance_differentials += [abs(image_luminance[y][x + 1] - image_luminance[y][x])]
    return (sum(luminance_differentials) / len(luminance_differentials)) * 2

# Loads an image and returns a map of 
# {
#   "fname": "xxx.jpg", 
#   "width": 500, 
#   "height": 500, 
#   "zip_entropy": 0.54, 
#   "luminance_entropy": 0.21
# }
def get_image_profile(fname):
    out = {}
    out["fname"] = fname.split("/")[-1]
    with Image.open(fname) as img:
        out["width"], out["height"] = img.size
    out["zip_entropy"] = zip_entropy(fname)
    out["luminance_entropy"] = luminance_entropy(fname)
    return out

# Processes the data for every image and returns the dictionary containing them all
# {
#   "poisoned_images": 
#   [
#       {"fname": "xxx.jpg", "width": 500, "height": 500, "zip_entropy": 0.54, "luminance_entropy": 0.21}
#       {"fname": "xxx.jpg", "width": 500, "height": 500, "zip_entropy": 0.54, "luminance_entropy": 0.21}
#       {"fname": "xxx.jpg", "width": 500, "height": 500, "zip_entropy": 0.54, "luminance_entropy": 0.21}
#   ], 
#   "clean_images": 
#   [
#       {"fname": "xxx.jpg", "width": 500, "height": 500, "zip_entropy": 0.54, "luminance_entropy": 0.21}
#       {"fname": "xxx.jpg", "width": 500, "height": 500, "zip_entropy": 0.54, "luminance_entropy": 0.21}
#       {"fname": "xxx.jpg", "width": 500, "height": 500, "zip_entropy": 0.54, "luminance_entropy": 0.21}
#   ]
# }
def get_image_profiles(force_update=False):
    if (isfile("processed_images.json")):
        return json.loads("processed_images.json")
    poisoned_files = [f for f in listdir("poisoned_images/scaled/") if isfile(join("poisoned_images/scaled/", f))]
    clean_files = [f for f in listdir("images/scaled/") if isfile(join("images/scaled/", f))]
    pi = []
    ci = []
    print("Poisoned images starting...")
    for i in range(len(poisoned_files)):
        pi += [get_image_profile("poisoned_images/scaled/" + poisoned_files[i])]
        print(f"Poisoned image {i + 1}/{len(poisoned_files)} done.")
    print("Poisoned images complete.")
    print("Clean images starting...")
    for i in range(len(clean_files)):
        ci += [get_image_profile("images/scaled/" + clean_files[i])]
        print(f"Clean image {i + 1}/{len(clean_files)} done.")
    print("Clean images complete.")
    profiles = {
        "poisoned_images": pi,#[get_image_profile("poisoned_images/" + x) for x in poisoned_files], 
        "clean_images": ci#[get_image_profile("images/" + x) for x in clean_files]
    }
    with open("processed_images.json", "w") as f:
        f.write(json.dumps(profiles))
    return profiles

if __name__ == "__main__":
    get_image_profiles(True)