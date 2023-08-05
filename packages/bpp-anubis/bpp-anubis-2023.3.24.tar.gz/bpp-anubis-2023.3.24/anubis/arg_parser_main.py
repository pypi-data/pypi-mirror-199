import argparse
import os
from subprocess import run
from re import match


def parse_arguments():
    parser = argparse.ArgumentParser('Running in parallel mode')
    # anubis-specific stuff
    parser.add_argument('--processes', required=False, default=10, type=int)
    parser.add_argument('--feature_dir', required=False, default='features')
    parser.add_argument('--output', required=False, default='default')
    parser.add_argument('--aggregate', required=False, default='.tempres.json')
    parser.add_argument('--pass-threshold', required=False, type=float, default=1.0)
    parser.add_argument('--index-start', required=False, type=int, default=0)
    parser.add_argument('--env', required=True, type=str)
    parser.add_argument('--junit', required=False, type=str, default='results.xml')

    # flags
    parser.add_argument('--pass-with-no-tests', required=False, action='store_true')
    parser.add_argument('--hide-passed', required=False, action='store_true')
    parser.add_argument('--hide-failed', required=False, action='store_true')
    parser.add_argument('--hide-summary', required=False, action='store_true')
    parser.add_argument('--verbose', required=False, action='store_true')

    # sent directly to behave
    parser.add_argument('--tags', required=False, nargs='+', action='append')
    parser.add_argument('-D', required=False, nargs='+', action='append')

    # format anything that needs to be formatted
    known, unknown = parser.parse_known_args()

    # output files
    known.output = os.path.join(os.getcwd(), '.tempoutput' if known.output == 'default' else known.output)
    known.aggregate = os.path.join(known.output, known.aggregate)
    known.junit = os.path.join(known.output, known.junit)

    # tags
    if known.tags:
        known.tags = [tag.replace('@', '').replace('"', "'") for group in known.tags for tag in group]

        # try to look for a jira ticket at the start of the branch name and add it to the tags list
        if 'this-branch' in known.tags:
            try:
                res = run(
                    ['git rev-parse --abbrev-ref HEAD'],
                    shell=True,
                    capture_output=True
                ).stdout.decode('utf-8').split('\n')[0]
                branch_name = match(r'^(?P<ticket_identifier>\w+-\d+).*$', res)
                if branch_name:
                    known.tags.append(branch_name.groupdict()['ticket_identifier'])
                    known.tags.remove('this-branch')
            except:
                pass

    # user definitions
    known.D = [arg for group in known.D for arg in group] if known.D else []
    known.D.append(f'env={known.env}')

    return known, unknown
