#!/usr/bin/env python3
import sys, json, os
from subprocess import call

script_path = os.path.dirname(os.path.realpath(__file__))
data_resources_folder = os.path.join(script_path, 'data')

def wrapInDoubleQuotes(s):
    return '"{}"'.format(s)

def main():
    args = sys.argv[1:]
    config_path = args[0]
    config = json.load(open(config_path))

    # -Xmx4G

    project_path = \
        os.path.abspath(os.path.join(script_path, os.pardir))
    model_path = os.path.join(project_path, 'models')
    results_path = os.path.join(project_path, 'results', config['resultsFolder'])

    def model(path): return os.path.join(model_path, path)
    def result(path): return os.path.join(results_path, path)

    languageModelPath = model(config['languageModelPath'])
    acousticModelPath = model(config['acousticModelPath'])
    dictionaryPath    = model(config['dictionaryPath'])
    g2pModelPath      = model(config['g2pModelPath'])

    inputWaveFilepath = result('resources/audio.wav')
    outFilePathTranscription = result('sphinx_result.txt')
    outFilePathTimes = result('sphinx_word_times.txt')

    sphinx_arguments = ' '.join(map(wrapInDoubleQuotes, [
        acousticModelPath,
        dictionaryPath,
        languageModelPath,
        g2pModelPath,
        inputWaveFilepath,
        outFilePathTranscription,
        outFilePathTimes]))

    call('touch "{}"'.format(outFilePathTranscription), shell=True)
    call('touch "{}"'.format(outFilePathTimes), shell=True)

    cmd = 'java -jar Hotwords.jar {}'.format(sphinx_arguments)
    wd = os.path.join(script_path, 'sphinx')
    call(cmd, cwd=wd, shell=True)

main()


