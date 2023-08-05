# __main__.py
import multiprocessing
import os
import sys
import shutil
from datetime import datetime
from random import choice
from anubis import feature_file_parser
from anubis import arg_parser_main
from anubis import feature_splitter
from anubis import results
from anubis.parallelizer import command_generator
from anubis.copy import art


def main():
    # Misc Setup ---------------------------------------------------------------------------------
    start = datetime.now()
    args_known, args_unknown = arg_parser_main.parse_arguments()

    if args_known.verbose:
        print(choice(art) + '\nRunning tests with Anubis  -- powered by love  Σ>―(〃°ω°〃)♡→)')

    #
    # Set up output dirs and files ---------------------------------------------------------------------------------
    # create a directory that will contain results and be exported
    if args_known.verbose:
        print(f'--- SETTING UP OUTPUT\n\tSending output to <{args_known.output}>')

    if not os.path.isdir(args_known.output):
        os.makedirs(args_known.output, exist_ok=True)
    else:
        errors = []
        for filename in os.listdir(args_known.output):
            file_path = os.path.join(args_known.output, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                errors.append(e)
    with open(args_known.junit, 'w'):
        pass

    #
    # Group features and tests ---------------------------------------------------------------------------------
    if args_known.verbose:
        print('\n--- GROUPING FEATURES')
        print(f'\tfeature dir: <{args_known.feature_dir}>')
        print(f'\ttags: <{",".join([t for t in args_known.tags]) if args_known.tags else "n/a"}>')

    # split the features and store as list
    feature_paths = feature_splitter.get_feature_paths(args_known.feature_dir)
    parsed_gherkin = feature_file_parser.get_parsed_gherkin(feature_paths)
    test_paths = feature_splitter.get_paths_by_tags_and_gherkin(args_known.tags, parsed_gherkin)
    tests_to_run = feature_splitter.__get_path_groups(test_paths, args_known.processes)

    #
    # Run the tests ---------------------------------------------------------------------------------
    # run all the processes and save the locations of the result files
    num_groups = len(tests_to_run)
    passed, failed, total = 0, 0, 0

    if args_known.verbose:
        print(f'\n--- RUNNING IN <{num_groups}> PROCESS{"ES" * int(num_groups > 1)}\n')

    if tests_to_run:
        # set up the multiple processes
        pool = multiprocessing.Pool(args_known.processes)
        result_files = pool.map(command_generator, tests_to_run)
        results.write_result_aggregate(files=result_files, aggregate_out_file=args_known.aggregate)

        # do the math to print out the results summary
        results.write_junit(args_known.aggregate, args_known.junit)
        passed, failed, total = results.get_result_values(args_known.aggregate)
        end = datetime.now()
        results.print_result_summary(args_known, args_known.D, start, end, passed, failed)

    if args_known.output.endswith('.tempoutput'):
        shutil.rmtree(args_known.output)

    # exit correctly
    if args_known.pass_with_no_tests or not tests_to_run or total == 0:
        print('𓃥 no tests found --> this run passes by default')
        return 0
    return 0 if passed/total >= args_known.pass_threshold else 1


if __name__ == '__main__':
    # run everything
    sys.exit(main())
