import argparse
import hashlib
import subprocess
import time
import os
import json


DOCKER_IMG_LOGPATH = '/nlc2cmd/logs/'


def _get_hash(prefix):
    hash = hashlib.sha1()
    hash.update(str(time.time()).encode())
    return f'{prefix}_{hash.hexdigest()}'


def start_evaluation_process(submission_image, annotation_folder, annotation_filename, params_folder,
                             params_filename, grammar_folder, grammar_filename, log_folder):

    grammar_filepath = os.path.join('/grammar_folder', grammar_filename)
    container_name = _get_hash('nlc2cmd')
    stdout_file = open(os.path.join(log_folder, 'stdout.data.txt'), 'w')
    stderr_file = open(os.path.join(log_folder, 'stderr.data.txt'), 'w')

    process = subprocess.Popen([
        "docker", 
        "run", 
        "--rm", 
        "--name", 
            f"{container_name}",
        "--network=none",
        "-v", 
            f"{annotation_folder}:/annotation_folder",
        "-v",
            f"{params_folder}:/params_folder",
        "-v",
            f"{grammar_folder}:/grammar_folder",
        "-v", 
            f"{log_folder}:{DOCKER_IMG_LOGPATH}",
        "-e",
            f"GRAMMAR_FILEPATH={grammar_filepath}",
        "-t", 
        f"{submission_image}", 
        "/bin/bash", 
        "-c",
        f"python3 /nlc2cmd/src/evaluate.py " + 
            f"--annotation_filepath /annotation_folder/{annotation_filename} " +
            f"--params_filepath /params_folder/{params_filename} " +
            f"--output_folderpath {DOCKER_IMG_LOGPATH} " + 
            f"--mode eval"
    ], stdout=stdout_file, stderr=stderr_file)

    return process, container_name


def kill_docker_container(container_name):
    
    subprocess.call(
        ["docker", "rm", "--force", f"{container_name}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def get_docker_logs(container_name):
    """ Get logs of docker container. """
    p = subprocess.run(
        ["docker", "logs", container_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return p.stdout.decode()


def read_result_file(folderpath):
    with open(os.path.join(folderpath, 'result.json'), 'r') as f:
        result = json.load(f)
    return result


def main(submission_image, annotation_filepath, params_filepath, grammar_filepath, log_folder):

    try:
        log_folder = os.path.abspath(log_folder)
        os.makedirs(log_folder, exist_ok=True)

        annotation_folder, annotation_filename = os.path.split(os.path.abspath(annotation_filepath))
        params_folder, params_filename = os.path.split(os.path.abspath(params_filepath))
        grammar_folder, grammar_filename = os.path.split(os.path.abspath(grammar_filepath))

        print('Starting evaluation')
        print(f'Check folder "{args.log_folder}" for progress')

        submission_proc, container_name = start_evaluation_process(
            submission_image, annotation_folder, annotation_filename,
            params_folder, params_filename, grammar_folder, grammar_filename, log_folder
        )

        submission_proc.communicate()

    except Exception as err:
        print(err)

    finally:
        kill_docker_container(container_name)
        result = read_result_file(log_folder)
    
    return result


if __name__ == "__main__":

    linesep = "="*100

    default_img = "nlc2cmd-challenge"
    default_annotation_filepath = os.path.join(os.path.dirname(__file__), 'configs', 'annotations', 'local_eval_annotations.json')
    default_params_filepath = os.path.join(os.path.dirname(__file__), 'configs', 'core', 'evaluation_params.json')
    default_grammar_filepath = os.path.join(os.path.dirname(__file__), 'configs', 'core', 'grammar.txt')
    default_logfolder = os.path.join(os.path.dirname(__file__), "logs")

    parser = argparse.ArgumentParser()
    parser.add_argument('--img', type=str, required=False, default=default_img, help="Submission docker image name")
    parser.add_argument('--annotation_filepath', type=str, required=False, default=default_annotation_filepath, help="Annotation filepath")
    parser.add_argument('--params_filepath', type=str, required=False, default=default_params_filepath, help="Parameters filepath")
    parser.add_argument('--grammar_filepath', type=str, required=False, default=default_grammar_filepath, help="Grammar filepath")
    parser.add_argument('--log_folder', type=str, required=False, default=default_logfolder, help="Output log folder path")

    args = parser.parse_args()

    print(linesep)
    print(' '*30 + 'Evaluating nlc2cmd submission locally')
    print(linesep)

    print('Parameters: ')
    for arg in vars(args):
        print('\t {} : {}'.format(arg, getattr(args, arg)))
    print(linesep + '\n')

    result = main(args.img, args.annotation_filepath, args.params_filepath, args.grammar_filepath, args.log_folder)

    print(linesep)
    print('Result:')
    for key, val in result.items():
        print(f'\t{key}: {val}')
    print(linesep)
