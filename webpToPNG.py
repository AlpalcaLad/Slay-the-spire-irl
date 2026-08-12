#!/usr/bin/python3
# Usage: webp_to_png <filename>


def arg_chk(args):
    if len(args) != 2:
        print("Script takes exactly one argument")
        quit()


def exist_chk(img):
    from os.path import exists
    if not exists(img):
        print("File not found")
        quit()


def img_ext(img):
    from os.path import splitext
    ext = splitext(img)[1]
    if ext != ".webp":
        print("Only .WEBP files are accepted")
        quit()


def ext_to_png(img):
    from os.path import splitext
    path, ext = splitext(img)
    new_img = f"{path}.png"
    return new_img


def img_conv(img):
    from PIL import Image
    png_file = ext_to_png(img)
    png = Image.open(img).convert("RGBA")
    png.save(png_file, "png")
    print(f"Saved to {png_file}")



if __name__ == "__main__":
    from sys import argv
    # arg_chk(argv)
    # exist_chk(argv[1])
    # img_ext(argv[1])
    # img_conv(argv[1])
    import os
    for f in os.listdir(argv[1]):
        if f[-1] != "p":
            continue
        if os.path.isfile(argv[1]+"/"+f.replace("webp","png")):
            os.remove(argv[1]+"/"+f.replace("webp","png"))
        img_conv(argv[1]+"/"+f)
        os.remove(argv[1]+"/"+f)