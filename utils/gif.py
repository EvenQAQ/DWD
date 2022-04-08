import moviepy.editor as mpy

#视频文件的本地路径
content = mpy.VideoFileClip("/Users/even/Dev/DWD/assets/loading.mp4")
# 剪辑0分0秒到0分4秒的片段。resize为修改清晰度
c1 = content.subclip((0,0),(0,11)).resize((800,450))
# 将片段保存为gif图到python的默认路径
c1.write_gif("./assets/loading11.gif")

