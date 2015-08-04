#!/usr/bin/env python3
import sys, json, os
from string import Template
from os.path import join
from subprocess import call

script_path = os.path.dirname(os.path.realpath(__file__))
data_resources_folder = os.path.join(script_path, 'data')

def wrapInDoubleQuotes(s):
    return '"{}"'.format(s)

def main():
    args = sys.argv[1:]
    config_path = args[0]
    config = json.load(open(config_path))


    project_path = \
        os.path.abspath(join(script_path, os.pardir))
    model_path = join(project_path, 'models')
    results_path = join(project_path, 'results', config['resultsFolder'])
    sphinx_config_path = join(script_path, 'sphinx/config')
    default_config_path = join(sphinx_config_path, 'default.config.xml')
    interpolated_config_path = join(sphinx_config_path, 'interpolated.config.xml')
    interpolated_config_template = open(interpolated_config_path).read()
    # print(interpolated_config_string)


    def model(path): return os.path.join(model_path, path)
    def result(path): return os.path.join(results_path, path)

    languageModelPath = model(config['languageModelPath'])
    acousticModelPath = model(config['acousticModelPath'])
    dictionaryPath    = model(config['dictionaryPath'])
    g2pModelPath      = model(config['g2pModelPath'])

    if 'keywordModelPath' in config:
        keywordModelPath = result(config['keywordModelPath'])
        new_config = interpolated_config_template.replace(
                '{{keywordLm}}', keywordModelPath)
        new_config = new_config.replace(
                '{{lm}}', languageModelPath)
        sphinx_config_file_path = '/tmp/interpolated.config.json'
        open(sphinx_config_file_path, 'w').write(new_config)
        # interpolated_sphinx_config = os.path.join
    else:
        sphinx_config_file_path = default_config_path

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
        outFilePathTimes,
        sphinx_config_file_path
    ]))

    call('touch "{}"'.format(outFilePathTranscription), shell=True)
    call('touch "{}"'.format(outFilePathTimes), shell=True)

    gigs = 4 # 4GB heap
    cmd = 'java -Xmx{}G -jar Hotwords.jar {}'.format(gigs, sphinx_arguments)
    wd = os.path.join(script_path, 'sphinx')
    call(cmd, cwd=wd, shell=True)

main()


