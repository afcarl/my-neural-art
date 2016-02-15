import os
import subprocess
import argparse
from os.path import isfile, join

import csv

IMG_PATH='img/'
STYLES_PATH="styles/"
STYLES_TXT="styles.txt"
RESULTS_PATH="results"
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
                    print "coucou"
                    s[field] = [float(x) for x in s[field].split(',')]
        
            styles[s["style_name"]] = s

    return styles

    

    
def artify(img, styles):
    styles_param = load_styles(STYLES_TXT)

    if not styles == "all":
        styles_param = dict((x, styles_param[x]) for x in styles.split(','))

    

    for (x, s) in styles_param.iteritems():
        style_path = 
        results = img+"_"+x+".png"
        subprocess.call(["th neural_style.lua" +
                         " -style_image " + join(STYLES_PATH, s["file"]) +
                         " -content_image " + join(IMG_PATH, img) +
                         " -output_image " + join(RESULTS_PATH, results) 
                         " -gpu 0 " +
                         " -style_scale " + str(s["style_scale"]) +
                         " -content_weight " + str(s["content_weight"]) +
                         " -style_weight " + str(s["style_weight"]) +
                         " -tv_weight " + str(s["tv_weight"])
                         , shell=True])

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
