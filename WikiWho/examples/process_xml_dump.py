from mwxml import Dump
from mwtypes.files import reader

from WikiWho.wikiwho import Wikiwho


def process_xml_dump(xml_file_path):
    """
    Link to xml dumps: https://dumps.wikimedia.org/enwiki/

    Example usage:

    from WikiWho.examples.process_xml_dump import process_xml_dump

    xml_file_path = '/home/kenan/Downloads/enwiki-20180101-pages-meta-history1.xml-p5753p7728.7z'
    wikiwho_obj = process_xml_dump(xml_file_path)
    print(wikiwho_obj.title)
    print(wikiwho_obj.ordered_revisions)

    :param xml_file_path:
    :return: WikiWho object.
    """
    # more info about reading xml dumps: https://github.com/mediawiki-utilities/python-mwxml
    dump = Dump.from_file(reader(xml_file_path))
    for page in dump:
        wikiwho = Wikiwho(page.title)
        wikiwho.analyse_article_from_xml_dump(page)
        break  # process only first page
    return wikiwho

def iter_rev_tokens_and_text(last_rev):
    curr_pos = 0
    ltext = last_rev.text.lower()
    for token in iter_rev_tokens(last_rev):
        next_pos = ltext.index(token.value, curr_pos)
        if next_pos > curr_pos:
            yield None, last_rev.text[curr_pos:next_pos]
        yield token, last_rev.text[next_pos:next_pos + len(token.value)]
        curr_pos = next_pos + len(token.value)

if __name__ == "__main__":
    import sys

    from WikiWho.utils import iter_rev_tokens

    from termcolor import colored

    path = sys.argv[1]
    wikiwho_obj = process_xml_dump(path)

    colors = ('cyan', 'yellow', 'red', 'blue', 'green', 'magenta')
    color = 0
    prev_rev_id = None
    last_rev = wikiwho_obj.revisions[wikiwho_obj.ordered_revisions[-1]]

    for token, text in iter_rev_tokens_and_text(last_rev):
        if token:
            # token.origin_rev_id
            color_index = token.origin_rev_id % len(colors)
            print(colored(text, colors[(color_index+1)%len(colors)], 'on_' + colors[color_index]), end="")

            prev_rev_id = token.origin_rev_id
        else:
            print(text, end="")
    print()