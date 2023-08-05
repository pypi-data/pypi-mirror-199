import json
import os
from json.decoder import JSONDecodeError
from pathlib import Path
from time import gmtime, strftime
from re import match

GREEN_START = '\033[92m'
GREY_START = '\033[90m'
RED_START = '\033[91m'
END_COLOR = '\033[0m'
spc = '  '
linesep = os.linesep
tab = '\t'


def __write_scenario_junit(scenario):
    duration = 0
    formatted_steps = ''
    try:
        for step in scenario["steps"]:
            line = os.linesep + tab + step['keyword'] + ' '  + step['name']
            if 'result' in step:
                duration += step['result']['duration']
                line += " ... " + step["result"]["status"] + " in " + str("{:.3f}s".format(step["result"]["duration"]))
            formatted_steps += line
        start = f'\n<testcase classname="{scenario["location"]}" name="{scenario["name"]}" status="{scenario["status"]}" time="{duration}">'

        if scenario['status'] == 'passed':
            failure_message = ''
        else:
            failed_step = next((s for s in scenario['steps'] if s['result']['status'] == 'failed'), scenario['steps'][-1])

            failure_message = (
                '\n<failure>\n'
                '<![CDATA[\n'
                f'Failing step: {failed_step["keyword"]} {failed_step["name"]} ... failed in {"{:.3f}s".format(failed_step["result"]["duration"])}\n'
                f'Location: {failed_step["location"]}\n'
                f'{linesep.join(failed_step["result"]["error_message"])}\n'
                ']]>\n'
                '</failure>\n'
            )

        output = (
            '\n<system-out>\n'
            '<![CDATA[]\n'
            f'@scenario.begin\n\n'
            f'{"".join(["@" + t + " " for t in scenario["tags"]])}\n'
            f'Scenario: {scenario["name"]}'
            # f'{"".join(os.linesep + tab + s["keyword"] + " " + s["name"] + " ... " + s["result"]["status"] + " in " + str("{:.3f}s".format(s["result"]["duration"])) for s in scenario["steps"])}\n'
            f'{formatted_steps}\n'
            '@scenario.end\n'
            '--------------------------------------------------------------------------------\n'
            ']]>\n'
            '</system-out>\n'
            '</testcase>\n')

        return start + failure_message + output
    except Exception as e:
        print(e)
        pass


def __get_widths(s, p, f, hide_sum, hide_passed, hide_failed, extra_width=0):
    """This does all the terrible work of finding the widths of lines for output"""
    width_p_name = max([len(line['name']) for line in p]) if p else 0
    width_p_location = max([len(line['location']) for line in p]) if p else 0
    width_f_name = max([len(line['name']) for line in f]) if f else 0
    width_f_location = max([len(line['location']) for line in f]) if f else 0
    width_s = max([len(line) for line in s])

    return (
        max(
            (width_p_name + width_p_location) * int(not hide_passed),
            (width_f_name + width_f_location) * int(not hide_failed),
            width_s * int(not hide_sum)) + extra_width,
        width_p_name,
        width_p_location,
        width_f_name,
        width_f_location,
        width_s
    )


def __get_pass_fail_details(is_passing, width, scenarios):
    dc = RED_START
    cc = GREY_START
    end = END_COLOR
    if is_passing:
        dc = GREEN_START

    return '\n'.join(
        [f'{spc}{dc}●{end}{spc}{s["name"].ljust(width)}{spc}{cc}# {s["location"]}{end}' for s in scenarios])


def write_result_aggregate(files: list, aggregate_out_file):
    agg_fp = Path(aggregate_out_file)
    aggregate = []

    for fp in files:
        try:
            with open(fp, 'r') as f:
                current_file_data = json.load(f)
        except (FileNotFoundError, JSONDecodeError):
            current_file_data = []
        aggregate += current_file_data

    with agg_fp.open('w+', encoding='utf-8') as f:
        f.write(json.dumps(aggregate))


def get_result_values(aggregate_file):
    try:
        with open(aggregate_file) as f:
            res = json.load(f)
    except FileNotFoundError:
        return 0, 0, 0

    statuses = []
    for feature in res:
        if 'elements' in feature:
            for scenario in feature['elements']:
                if scenario['type'] != 'background':
                    statuses.append(scenario['status'])

    passed = statuses.count('passed')
    failed = statuses.count('failed')
    total = passed + failed
    return passed, failed, total


def print_result_summary(args_known, user_defs, start, end, num_passed, num_failed):
    # set up a bunch of variables
    total = num_passed + num_failed
    pass_rate = f'{num_passed / total * 100:.2f}%' if total > 0 else 'n/a'
    fail_rate = f'{num_failed / total * 100:.2f}%' if total > 0 else 'n/a'
    env_txt = f'{spc}Env:     <{next((a.split("=")[1] for a in user_defs if match("env=(.*)", a)), "n/a")}>'
    tag_txt = f'{spc}Tags:    <{", ".join(tag for tag in args_known.tags) if args_known.tags else ""}>'
    res_txt = f'{spc}Output:  <{args_known.output}>'
    pass_txt = f'{spc}Passed:  <{num_passed}, {pass_rate}>'
    fail_txt = f'{spc}Failed:  <{num_failed}, {fail_rate}>'
    run_txt = f'{spc}Runtime: <{strftime("%Hh %Mm %Ss", gmtime((end - start).total_seconds()))}>'

    with open(args_known.aggregate) as f:
        res = json.load(f)

    summary = [pass_rate, fail_rate, env_txt, tag_txt, res_txt, pass_txt, fail_txt, run_txt]
    passed = []
    failed = []
    for feature in res:
        if 'elements' in feature:
            for element in feature['elements']:
                if element['type'] != 'background' and element['status'].lower() == 'passed':
                    passed.append(element)
                if element['type'] != 'background' and element['status'].lower() == 'failed':
                    failed.append(element)

    width, width_pn, width_pl, width_fn, width_fl, width_sum = __get_widths(
        summary, passed, failed, args_known.hide_passed, args_known.hide_failed, args_known.hide_summary, 4 * len(spc))

    if not args_known.hide_passed and num_passed:
        passing_details = __get_pass_fail_details(True, width_pn, passed)
        print(f'--- Passing scenarios '.ljust(width, '-') + '\n' + passing_details + '\n')
    if not args_known.hide_failed and num_failed:
        failing_details = __get_pass_fail_details(False, width_fn, failed)
        print(f'--- Failing scenarios '.ljust(width, '-') + '\n' + failing_details + '\n')
    if not args_known.hide_summary:
        print('--- ♡𓃥♡ SUMMARY ♡𓃥♡ '.ljust(width, '-'))
        print(env_txt)
        print(res_txt)
        print(tag_txt)
        print(pass_txt)
        print(fail_txt)
        print(run_txt, '\n')


def write_junit(json_aggregate, output_file):
    with open(json_aggregate) as f:
        res = json.load(f)

    statuses = []
    for feature in res:
        if 'elements' in feature:
            for scenario in feature['elements']:
                if scenario['type'] != 'background':
                    statuses.append(scenario['status'])

    passed = statuses.count('passed')
    failed = statuses.count('failed')
    total = passed + failed

    start = ('<?xml version="1.0" encoding="UTF-8" ?>\n'
             f'<testsuite name="Test Run" tests="{total}" failures="{failed}">')

    scenarios = []
    for feature in res:
        if 'elements' in feature:
            for scenario in feature['elements']:
                bg_steps = [] if scenario['type'].lower() != 'background' else scenario['steps']

                if scenario['type'].lower() != 'background':
                    bg_steps += scenario['steps']
                    scenario['steps'] = bg_steps
                    scenarios.append(scenario)

    try:  # todo - make all of this more stable; logging
        junit_res = [__write_scenario_junit(scen) for scen in scenarios]
        end = '\n</testsuite>'
        final = start + "".join(junit_res) + end

        with open(output_file, 'w+') as f:
            f.writelines(final)
    except Exception as e:
        print('!!something went wrong writing to the junit out file!!')
        print('this is the error\n', e)
