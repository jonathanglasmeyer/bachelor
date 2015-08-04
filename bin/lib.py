import os

script_path = os.path.dirname(os.path.realpath(__file__))
data_resources_folder = os.path.join(script_path, 'data')

top5000_fname = os.path.join(data_resources_folder, 'top5000.txt')
top5000words = open(top5000_fname).read().split('\n')[:-1]
def top_x_words(x): return top5000words[:x]

