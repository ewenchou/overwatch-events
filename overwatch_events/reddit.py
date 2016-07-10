from lxml import html
import requests


def main():
    # Get the page
    page = requests.get('https://reddit.com/r/overwatch')
    # Parse the page content
    tree = html.fromstring(page.content)
    # Find the esports calendar h1
    h1_list = tree.findall('.//h1')
    esports_h1 = None
    for h1 in h1_list:
        if h1.text == 'Esports Calendar':
            esports_h1 = h1
            break
    if esports_h1 is None:
        print h1_list
        raise RuntimeError('Failed to find Esports Calendar H1 element')
    # The first sibling should be a blockquote with all the events
    block = esports_h1.getnext()
    if block is None or block.tag != 'blockquote':
        raise RuntimeError('Failed to find blockquote sibling of '
                           'Esports Calendar')
    # Each event is in a blockquote child
    event_blocks = block.findall('blockquote')
    # Each event name is inside an H2
    event_data = []
    for event in event_blocks:
        h2 = event.find('h2')
        if h2 is not None:
            # Find the event name in the <a> tag
            a_tag = h2.find('a')
            if a_tag is not None:
                print a_tag.text
                for p in event.findall('p'):
                    print p.text_content()


if __name__ == '__main__':
    main()