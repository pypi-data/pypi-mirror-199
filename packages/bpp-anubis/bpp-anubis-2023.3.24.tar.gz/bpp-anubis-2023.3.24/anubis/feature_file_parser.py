class GherkinFeature:
    def __init__(self, name='', background=None, location='', tags=None, tests=None):
        self.name = name
        self.location = location
        self.background = background if background is not None else None
        self.tags = tags if tags is not None else []
        self.tests = tests if tests is not None else []


class GherkinBlock:
    def __init__(self, name='', location='', keyword='', tags=None, steps=None, examples=None):
        self.name = name
        self.location = location
        self.keyword = keyword
        self.tags = tags if tags is not None else []
        self.steps = steps if steps is not None else []
        self.examples = examples if examples is not None else []
        self.blocks = []


def gherkin_parser(fp):
    with open(fp, 'r') as f:
        lines = [line.lstrip().lower().replace('\n', '') for line in f.readlines()]
        lines.reverse()

    gherkin_block_keywords = ['scenario', 'scenario outline']  # these keywords indicate new gherkin block
    test_step_keywords = ['given', 'when', 'then', 'and', '*', 'but']  # these keywords indicate steps

    feature = GherkinFeature()
    current_block = GherkinBlock()

    for i, line in enumerate(lines):
        location = fp + f':{len(lines) - i}'
        if any([line.startswith(kw) for kw in gherkin_block_keywords]):
            current_block.name = line.split(':')[-1].lstrip()
            if current_block.examples:
                current_block.examples.pop(-1)
                current_block.examples.reverse()
            current_block.keyword = line.split(':')[0]
            current_block.steps.reverse()
            current_block.blocks.reverse()
            current_block.name = line.split(':')[-1]
            current_block.location = location

            if lines[i + 1].startswith('@'):
                current_block.tags.extend([tag.replace('@', '') for tag in lines[i + 1].split()])

            feature.tests.append(current_block)
            current_block = GherkinBlock()
        elif any(line.startswith(kw) for kw in test_step_keywords):
            current_block.steps.append(line)
        # elif line.startswith('@'):
        #     current_block.tags.extend([tag.replace('@', '') for tag in line.split()])
        elif line.startswith('|'):
            current_block.examples.append((line, location))
        elif line.startswith('feature'):
            feature.name = line.split('feature:')[-1]
            feature.location = fp
            feature.tests.reverse()
            if i != len(lines) - 1 and lines[i + 1].startswith('@'):
                feature.tags.extend([tag.replace('@', '') for tag in lines[i + 1].split()])
        elif line.startswith('background'):
            current_block.name = line.split('background:')[-1]
            current_block.keyword = 'background'
            current_block.location = fp
            current_block.blocks.reverse()
            feature.background = current_block
    # feature.tests.reverse()

    for test in feature.tests:
        test.tags.extend(feature.tags)

    return feature


def get_parsed_gherkin(fp):
    if type(fp) is list:
        parsed_gherkin = []
        for path in fp:
            parsed_gherkin.append(gherkin_parser(path))
        return parsed_gherkin
    else:
        return [gherkin_parser(fp)].reverse()
