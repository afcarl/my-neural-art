import os
import subprocess
import argparse
from os.path import isfile, join, expanduser

import csv

IMG_PATH=expanduser('~/img/')
STYLES_PATH=expanduser("~/styles/")
STYLES_TXT=expanduser('~/my-neural-art/styles.txt')
RESULTS_PATH=expanduser("~/results/")
IMG_SIZE=512
N_GPU = 4

def load_styles(styles_path):
    styles = {}

    default = {"style_scale":1.,
               "content_weight":5.,
               "tv_weight":1.e-3,
               "style_weight":1.e2}
    
    with open(styles_path) as csvfile:
        
        styles_reader = csv.DictReader(csvfile)
        fieldnames = styles_reader.fieldnames

        for row in styles_reader:
            s = row
            for field in ["style_scale", "content_weight", "tv_weight", "style_weight"]:
                if s[field] == '':
                    s[field] = default[field]
                else:
                    s[field] = float(s[field])
        
            styles[s["style_name"]] = s

    return styles

    

    
def artify(img, styles):
    styles_param = load_styles(STYLES_TXT)

    if not styles == "all":
        styles_param = dict((x, styles_param[x]) for x in styles.split(','))

    
    cmd = []
    for (x, s) in styles_param.iteritems():
        results = img+"_"+x+".png"
        cmd.append("th ~/neural-style/neural_style.lua" +
                   " -style_image " + join(STYLES_PATH, s["file"]) +
                   " -content_image " + join(IMG_PATH, img) +
                   " -output_image " + join(RESULTS_PATH, results) +
                   " -image_size " + str(IMG_SIZE) + 
                   #" -backend cudnn " + 
                   " -save_iter 0 " + 
                   " -style_scale " + str(s["style_scale"]) +
                   " -content_weight " + str(s["content_weight"]) +
                   " -style_weight " + str(s["style_weight"]) +
                   " -tv_weight " + str(s["tv_weight"]) + 
                   " -proto_file ~/neural-style/models/VGG_ILSVRC_19_layers_deploy.prototxt" + 
                   " -model_file ~/neural-style/models/VGG_ILSVRC_19_layers.caffemodel")
    
                   
    n_cmd = len(cmd)
    cmd.extend(((-n_cmd) % N_GPU) * ["wait"])
    for i in range(N_GPU):
        cmd[i::N_GPU] = [x + " -gpu " + str(i) for x in cmd[i::N_GPU]]

    for t in range(n_cmd / N_GPU):
        process1 = subprocess.Popen(cmd[N_GPU*t] ,shell=True)
        process2 = subprocess.Popen(cmd[N_GPU*t+1] ,shell=True)
        process3 = subprocess.Popen(cmd[N_GPU*t+2] ,shell=True)
        process4 = subprocess.Popen(cmd[N_GPU*t+3] ,shell=True)        
        process1.wait()
        process2.wait()
        process3.wait()
        process4.wait()
    return 1
    
def grid_search(img, style, results=None):
    img_size = 400

    tv_array = [0.1, 0.5, 1., 2., 5., 10.]
    cont_array = [10., 5.]

    for cont in cont_array:
        for tv in tv_array:    
            u = " ".join(["python /home/ubuntu/my-neural-art/neural_style_transfer.py", 
                          join(IMG_PATH, img),
                          join(STYLES_PATH, style),
                          join(RESULTS_PATH, img) + '_' + style[:-4] + '_' + str(tv) + '_' + str(cont),
                          str(img_size),
                          str(tv),
                          str(cont)])
            print u
            subprocess.call(["pwd"])
            subprocess.call([u], shell=True)
