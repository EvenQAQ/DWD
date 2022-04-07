import PIL.Image as Image

src_dir = "/Users/even/Dev/DWD/assets/feedback/"
chart_dir = "/Users/even/Dev/DWD/assets/chart/"

flag = "T"
for i in range(0, 6):
    print(i)
    layer1 = Image.open(src_dir + str(i) + ".png").convert('RGBA')   # 底图背景
    for j in range(1, 101):
        if j < 10:
            layer2 = Image.open(chart_dir + flag + "-0" + str(j) + ".png").convert('RGBA')    # mask
        else:
            layer2 = Image.open(chart_dir + flag + "-" + str(j) + ".png").convert('RGBA')    # mask

        # layer1和layer2要相同大小，否则需resize
        final = Image.new("RGBA", layer1.size)             # 合成的image
        final = Image.alpha_composite(final, layer1)
        final = Image.alpha_composite(final, layer2)

        final=final.convert('RGB')
        save_path = src_dir + "/" + str(i) + "/" + flag + str(j) + ".png"
        final.save(save_path)

