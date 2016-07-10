from lxml import html
import requests
from render import Render


class EventsParser(object):
    url = ''
    render = False  # render the page before parsing (i.e. b/c javascript)

    def __init__(self, *args, **kwargs):
        pass

    def get_page(self, url=None):
        if url is None:
            url = self.url
        page = requests.get(url)
        return page.content

    def render_page(self, url=None):
        if url is None:
            url = self.url
        r = Render(url)
        result = r.frame.toHtml()
        formatted_result = str(result.toAscii())
        return formatted_result
    
    def get_tree(self, url=None, render=False):
        if url is None:
            url = self.url
        if render or self.render:
            content = self.render_page(url=url)
        else:
            content = self.get_page(url=url)
        tree = html.fromstring(content)
        return tree
    
    def get_events(self):
        return []
        

class GosuGamersParser(EventsParser):
    url = 'http://www.gosugamers.net/overwatch/tournaments/upcoming' \
          '?box=true&itemCount=12'
    render = True

    def get_events(self):
        tree = self.get_tree()
        table = tree.get_element_by_id('tournament-box')
        if table is None:
            raise RuntimeError('Failed to find #tournament-box')
        
        event_tuples = []
        for row in table.findall('.//tr'):
            event = row.find('.//a')
            if event is None:
                raise RuntimeError('Failed to find event link')
            name = event.find('span')
            if name is None:
                raise RuntimeError('Failed to find event name in <span>')
            event_name = name.text
            event_url = event.attrib.get('href')
            event_tuples.append((event_name, event_url))

        # Fetch each events page and parse info
        events = []
        for name, url in event_tuples:
            data = {'Name': name}
            page = requests.get('http://www.gosugamers.net'+url)
            tree = html.fromstring(page.content)

            # Find the table with info
            tournament_div = tree.cssselect('div.tournament')
            if len(tournament_div):
                tournament_div = tournament_div[0]
            else:
                print "Failed to find tournament div element for '{}'".format(name)
                continue
            table = tournament_div.find('.//table')
            if table is None:
                print "Failed to find tournament table for '{}'".format(name)
                continue
            for row in table.findall('.//tr'):
                heading = None
                text = None

                # Find the info heading
                th = row.find('th')
                if th is not None:
                    heading = th.text
                
                # Find the info
                content = row.find('td')
                if content is not None:
                    a_link = content.find('a')
                    if a_link is not None:
                        text = a_link.text
                    else:
                        text = content.text
                    # Clean up the string
                    text = text.lstrip()
                    text = text.rstrip()
                
                if heading is not None:
                    data[heading] = text
            
            # Add event data to list
            events.append(data)
        
        return events


class RedditParser(EventsParser):
    url = 'https://reddit.com/r/overwatch'
    render = False

    def get_events(self):
        tree = self.get_tree()
        # Find the esports calendar h1
        h1_list = tree.findall('.//h1')
        esports_h1 = None
        for h1 in h1_list:
            if h1.text == 'Esports Calendar':
                esports_h1 = h1
                break
        if esports_h1 is None:
            raise RuntimeError('Failed to find Esports Calendar H1 element')
        # The first sibling should be a blockquote with all the events
        block = esports_h1.getnext()
        if block is None or block.tag != 'blockquote':
            raise RuntimeError('Failed to find blockquote sibling of '
                            'Esports Calendar')
        # Each event is in a blockquote child
        event_blocks = block.findall('blockquote')
        # Each event name is inside an H2
        events = []
        for event in event_blocks:
            data = {}
            event_name = None
            h2 = event.find('h2')
            if h2 is not None:
                # Find the event name in the <a> tag
                a_tag = h2.find('a')
                if a_tag is not None:
                    data['Name'] = a_tag.text
                    for p in event.findall('p'):
                        data['Info'] = p.text_content()
            if data.get('Name'):
                events.append(data)
            else:
                print "Failed to find event name H2"
        return events
