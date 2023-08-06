import os
import sys
import argparse
import json
from pathlib import Path
import subprocess
import urllib3

from template_generator import template
from template_generator import template_test
from template_generator import ffmpeg

parser = argparse.ArgumentParser()
parser.add_argument("--test", type=str, default=None, help="测试")
parser.add_argument("--transcoding", type=str, default=None, help="转码")
parser.add_argument("--input", type=str, default=None, help="输入资源")

def testTemplate():
    template_test.test()
    
def configTemplate():
    input = sys.argv[2]

    inputFiles = []
    template_path = None
    params = {}
    output_path = None
    try:
        if os.path.isfile(input):
            with open(input, 'r') as f:
                data = json.load(f)
        inputFiles = data["input"]
        template_path = data["template"]
        params = data["params"]
        output_path = data["output"]
    except:
        inputFiles = [sys.argv[2]]
        template_path = sys.argv[3]
        params = json.loads(sys.argv[4])
        output_path = sys.argv[5]

    if inputFiles == None or len(inputFiles) == 0 or template_path == None or output_path == None:
        print("args fail!")
        return
    for it in inputFiles:
        if os.path.exists(it) == False:
            print(f"file {it} not found!")
            return
    if os.path.exists(template_path) == False:
        print(f"template {template_path} not found!")
        return
    template.executeTemplate(inputFiles, template_path, params, output_path)

def autoTemplate():
    file = sys.argv[2]
    if os.path.exists(file) == False:
        print("auto process video file not exist")
        return
    template.autoTemplate(file)
    
def transcoding():
    file = sys.argv[2]
    if os.path.exists(file) == False:
        print("transcoding file not exist")
        return
    
    w,h,bitrate,fps = ffmpeg.videoInfo(file)
    if w <= 0 or h <= 0 or bitrate <= 0 or fps <= 0:
        print("file is not video")
        return
    niceBitrate = min(bitrate, (w * h) * (fps / 30.0) / (540.0 * 960.0 / 4000))

    tmpPath = f"{file}.mp4"
    args_moov = "-movflags faststart"
    args_h264 = "-c:v libx264 -pix_fmt yuv420p"
    args_bitrate = f"-b:v {niceBitrate}k -bufsize {niceBitrate}k"
    command = f'-i {file} {args_moov} {args_h264} {args_bitrate} -y {tmpPath}'
    if ffmpeg.process(command):
        os.remove(file)
        os.rename(tmpPath, file)

def doFfmpeg():
    cmd = sys.argv[2]
    if os.path.exists(cmd) == False:
        print("please set command")
        return
    
    if ffmpeg.process(cmd):
        print("=== success")
    else:
        print("=== fail")

module_func = {
    "--test": testTemplate,
    "--input": configTemplate,
    "--auto": autoTemplate,
    "--transcoding": transcoding,
    "--ffmpeg": doFfmpeg
}

def main():
    if len(sys.argv) < 2:
        return
    urllib3.disable_warnings()
    try:
        module = sys.argv[1]
        if module in module_func:
            module_func[module]()
        else:
            print("Unknown command:", module)
            sys.exit(0)
    except Exception as e:
        print(f"uncatch Exception:{e}")
        return
        
if __name__ == '__main__':
        main()
