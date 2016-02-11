import os
import subprocess
import argparse
from os.path import isfile, join

# parser = argparse.ArgumentParser(description='Neural style transfer with Keras.')

# parser.add_argument('base_image_path', metavar='base', type=str,
#                     help='Path to the img directory.')
# parser.add_argument('style_reference_image_path', metavar='ref', type=str,
#                     help='Path to the styles directory.')
# parser.add_argument('result_prefix', metavar='res_prefix', type=str,
#                     help='Path for the results directory.')

def multiple_img():
    tv = 1.
    cont = 0.025
    img_size = 800
    img_path = 'img/'
    styles_path = 'styles/'
    results_path = 'results/'
    
    for img in [f for f in os.listdir(img_path) if isfile(join(img_path, f))]:
        for style in [g for g in os.listdir(styles_path) if isfile(join(styles_path, g))]:
                
            subprocess.call(["python neural_style_transfer",
                             join(img_path, img),
                             join(styles_path, style),
                             join(results_path, img + '_' + style[:-4]),
                             str(800),
                             str(tv),
                             str(cont)])

def grid_search():
    img_path = '/home/ubuntu/img/'
    img = 'comp-einstein.jpg'
    styles_path = '/home/ubuntu/styles/abstract/'
    style = 'comp-vasarely1.jpg'
    results_path = '/home/ubuntu/results/'
    
    tv_array = [0.1, 0.5, 1., 2., 5., 10.]
    cont_array = [0.001, 0.01, 0.02, 0.05, 0.1, 0.5, 1.]
    for tv in tv_array:
        for cont in cont_array:
            u = " ".join(["python /home/ubuntu/my-neural-art/neural_style_transfer.py", 
                          join(img_path, img),
                          join(styles_path, style),
                          join(results_path, img) + '_' + style[:-4],
                          str(800),
                          str(tv),
                          str(cont)])
            print u
            subprocess.call([)])


if __name__ == '__main__':
    grid_search()
