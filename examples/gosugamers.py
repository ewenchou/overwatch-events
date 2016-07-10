from overwatch_events.parsers import GosuGamersParser


def main():
    parser = GosuGamersParser()
    events = parser.get_events()
    for data in events:
        print 
        print u"Name: {}".format(data['Name'])
        for k, v in data.iteritems():
            if k != 'Name':
                print u"{}: {}".format(k, v)


if __name__ == '__main__':
    main()