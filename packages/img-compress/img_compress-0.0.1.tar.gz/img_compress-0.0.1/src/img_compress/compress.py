import sys
import tinify
from pathlib import Path

tinify.key = "" # 请在 https://tinify.cn/developers 申请密匙 key

def hint(func):
    count = 1
    def call_func(source, total, width, height):
        nonlocal count
        print(f"({count}/{total})图片<{source}>正在压缩处理中，请稍后...")
        func(source, width, height)
        count += 1
        if count-1 == total:
            print("全部处理完成~")
    return call_func

@hint
def compress(source, width, height): 
    optimize = tinify.from_file(source)

    if width and height:
        optimize = optimize.resize(method="fit", width=width, height=height)
    if width and not height:
        optimize = optimize.resize(method="scale", width=width)
    if not width and height:
        optimize = optimize.resize(method="scale", height=height)
    
    optimize.to_file("opt_" + source.split('\\')[-1])

if __name__ == "__main__":
    if sys.argv[1:]:
        sources = sys.argv[1:]
    else:
        sources = input("请输入需要压缩的图片名称（回车优化当前文件夹）：").split()
        print("开始优化当前文件夹下所有的jpg/png/webp图片")

    size = input("请输入尺寸（宽度 高度）：")
    if size:
        width, height = size.split()
        width, height = int(width), int(height)
    else:
        width = 0
        height = 0
    
    if not sources:
        p = Path('.')
        jpgs = list(p.glob("*.jpg")) + list(p.glob("*.jpeg"))
        pngs = list(p.glob("*.png"))
        webps = list(p.glob("*.webp"))
        for each in jpgs + pngs + webps:
            sources.append(str(each))

    total = len(sources)
    for each in sources:
        compress(each, total, width, height)


