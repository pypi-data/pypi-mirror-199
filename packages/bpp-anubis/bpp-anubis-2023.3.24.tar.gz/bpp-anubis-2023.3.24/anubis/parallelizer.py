from .arg_parser_main import parse_arguments
from os.path import join
from subprocess import call, STDOUT, DEVNULL


def command_generator(test_paths) -> str:
    """
    Use args, accounts, and features to construct behave command
    :param test_paths: [(int, list), ... ]
    :return:
    """
    # get arguments and construct the behave command
    args, args_unknown = parse_arguments()
    pgi = test_paths[0]  # pgi is the "parallel group index," basically to keep track of which subprocess this is
    if args.index_start > 0:
        pgi += args.index_start
    results_json_file = join(args.output, f'{pgi}.json')
    user_defs = ' '.join('-D "{}"'.format(arg) for arg in args.D) if args.D else ''
    args_unknown = ' '.join(arg for arg in args_unknown) if args_unknown else ''
    tags = ' '.join('--tags="{}"'.format(tags) for tags in args.tags) if args.tags else ''
    paths = ' '.join("{}".format(path) for path in test_paths[1])
    output = f'-f json -o "{join(args.output, str(pgi))}.json"'
    command = rf'behave -D parallel -D pgi="{pgi}" {args_unknown} {user_defs} {tags} {output} {paths}'

    if args.verbose:
        print(command)
        call(command, shell=True)
    else:
        call(command, shell=True, stdout=DEVNULL, stderr=STDOUT)
    return results_json_file
