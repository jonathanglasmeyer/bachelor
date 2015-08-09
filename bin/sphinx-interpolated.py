#!/usr/bin/env python3
import sys, json, os
from string import Template
from os.path import join
from subprocess import call

script_path = os.path.dirname(os.path.realpath(__file__))
data_resources_folder = os.path.join(script_path, 'data')

def wrapInDoubleQuotes(s):
    return '"{}"'.format(s)

def main(INTERPOLATED):
    args = sys.argv[1:]
    config_path = args[0]
    if INTERPOLATED:
        print('INTERPOLATE MODE\n')
    else:
        print('BASELINE MODE\n')

    config = json.load(open(config_path))

    project_path = os.path.abspath(join(script_path, os.pardir))
    model_path = join(project_path, 'models')
    results_path = join(project_path, 'results', config['resultsFolder'])
    sphinx_config_path = join(script_path, 'sphinx/config', config.get('sphinxConfigSetName', ''))
    default_config_path = join(sphinx_config_path, 'default.config.xml')
    interpolated_config_path = join(sphinx_config_path, 'interpolated.config.xml')
    interpolated_config_template = open(interpolated_config_path).read()
    # print(interpolated_config_string)


    def makeModelPath(path): return os.path.join(model_path, path)
    def makeResultPath(path): return os.path.join(results_path, path)

    languageModelPath = makeModelPath(config['languageModelPath'])
    acousticModelPath = makeModelPath(config['acousticModelPath'])
    dictionaryPath    = makeModelPath(config['dictionaryPath'])
    g2pModelPath      = makeModelPath(config['g2pModelPath'])

    if 'keywordModelPath' in config and INTERPOLATED:
        keywordModelPath = makeResultPath(config['keywordModelPath'])

        new_config = interpolated_config_template.replace( '{{keywordLm}}', keywordModelPath)
        new_config = new_config.replace( '{{lm}}', languageModelPath)

        sphinx_config_file_path = '/tmp/interpolated.config.json'
        open(sphinx_config_file_path, 'w').write(new_config)

        outFilePathTranscription = makeResultPath('sphinx_result_interpolated.txt')
        outFilePathTimes = makeResultPath('sphinx_word_times_interpolated.txt')
    else:
        sphinx_config_file_path = default_config_path

        outFilePathTranscription = makeResultPath('sphinx_result_baseline.txt')
        outFilePathTimes = makeResultPath('sphinx_word_times_baseline.txt')

    log_file = makeResultPath('sphinx_log_interpolated.txt' if INTERPOLATED else 'sphinx_log_baseline.txt')

    inputWaveFilepath = makeResultPath('resources/audio.wav')

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
    cmd = 'java -Xmx{}G -jar Hotwords.jar {} 2>&1 | tee -a "{}"'.format(gigs, sphinx_arguments, log_file)
    wd = join(script_path, 'sphinx')
    call(cmd, cwd=wd, shell=True)

main(INTERPOLATED=False)
# main(INTERPOLATED=True)


