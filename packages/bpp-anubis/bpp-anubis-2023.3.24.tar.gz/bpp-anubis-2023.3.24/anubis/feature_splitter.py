import glob
import subprocess
from random import shuffle
from re import search
from os.path import join


def get_test_paths(unit, feature_dir, processes, accounts=None):
    paths = __get_paths(feature_dir, unit)
    result = __get_path_groups(paths, processes, accounts)
    return result


def __get_path_groups(paths, num_split, accounts=None, section=None):
    # split as evenly as possible
    inc = -(-len(paths) // num_split)

    if paths:
        # group the paths
        path_groups = [paths[i:i + inc] for i in range(0, len(paths), inc)]
        shuffle(path_groups)

        if accounts:
            return list(zip(accounts, path_groups))
        return list(zip(list(range(len(path_groups))), path_groups))
    return []


def __get_paths(feature_dir, unit):
    feature_paths = glob.glob(f'{feature_dir}/**/*.feature', recursive=True)

    if unit.lower() == 'scenario':
        # get all "Scenarios"
        scenario_paths = subprocess.run(
            [f'grep -irn "Scenario:" {" ".join(feature_paths)} | sed s/": .*"/""/'],
            shell=True,
            capture_output=True
        ).stdout.decode('utf-8').split('\n')

        # get all "Examples" and remove the first one to prevent duplicates
        example_paths = subprocess.run(
            [f'grep -rin "Examples\||" {" ".join(feature_paths)}'],
            shell=True,
            capture_output=True
        ).stdout.decode('utf-8').split('\n')

        # remove commented example lines
        example_paths = [path for path in example_paths if not search(r'.*:\d+:#.*', path) and len(path) != 0]

        # remove first occurrence of a file path to prevent duplicate examples
        example_paths_filtered = []
        i = 0
        while i < len(example_paths):
            if 'Examples' in example_paths[i]:
                i += 2
            else:
                example_paths_filtered.append(example_paths[i].split(': ')[0])
                i += 1

        if '' in scenario_paths:
            scenario_paths.remove('')
        if '' in example_paths_filtered:
            example_paths_filtered.remove('')
        return scenario_paths + example_paths_filtered
    return feature_paths


def get_feature_paths(feature_dir):
    return glob.glob(join(feature_dir, '**', '*.feature'), recursive=True)


def get_tags_match(grep_output, list_of_tags):
    desired_tags = [tag for tag in list_of_tags if not tag.startswith('~')]
    undesired_tags = [tag.replace('~', '') for tag in list_of_tags if tag.startswith('~')]
    test_path_details = {'tests_to_run': [], 'tests_not_to_run': []}
    for line in grep_output:
        path, line_number, tags = line.split(':')
        if all([tag in tags for tag in desired_tags]) and not any([tag in tags for tag in undesired_tags]):
            test_path_details['tests_to_run'].append(path + ':' + line_number)
            continue
        test_path_details['tests_not_to_run'].append(path + ':' + line_number)
    return test_path_details


def __get_paths_to_matching_tags(args_known):
    feature_paths = glob.glob(f'{args_known.feature_dir}/**/*.feature', recursive=True)
    tag_details = subprocess.run(
        [f'grep -rn @ {" ".join(feature_paths)} | sed -nre "s/ //gp"'],
        shell=True,
        capture_output=True
    ).stdout.decode('utf-8').split('\n')
    tag_details.remove('')  # the last entry is just '' because it's the newline at the end of grep output
    return get_tags_match(tag_details, args_known.tags)


def get_paths_by_tags_and_gherkin(tags, parsed_gherkin):
    desired_tags = [tag for tag in tags if not tag.startswith('~')] if tags else []
    undesired_tags = [tag.replace('~', '') for tag in tags if tag.startswith('~')] if tags else []

    # parsed_gherkin is nested, flatten it
    scenarios = [test for feature in parsed_gherkin for test in feature.tests if test.keyword.startswith('scenario')]
    matching_tests = []

    for gb in scenarios:
        if all([tag in gb.tags for tag in desired_tags]) and not any([tag in gb.tags for tag in undesired_tags]):
            matching_tests.extend([ex[1] for ex in gb.examples]) if gb.examples else matching_tests.append(gb.location)

    return matching_tests
