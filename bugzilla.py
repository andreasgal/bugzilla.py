import sys, urllib, urllib2, json, time

server = 'https://api-dev.bugzilla.mozilla.org/1.3/'

# fetch a url and parse the result as JSON
def fetch(url):
    return json.loads(urllib2.urlopen(url).read())

# convert a UTC date/time string to a local time string
def localtime(str):
    parsed = str.split('Z')[0].split('T')
    strtime = parsed[1].replace(':', '')
    strdate = parsed[0].replace('-', '')
    t = time.strptime(strdate + strtime, '%Y%m%d%H%M%S')
    t = time.mktime(t) + time.timezone
    t = time.gmtime(t)
    return time.strftime('%Y-%m-%d %H:%M %Z', t)

# check whether a number is a string
def isnumber(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

# get a bug from bugzilla
def getbug(number):
    bug = fetch(server + 'bug/' + str(number))
    bug['number'] = number;
    return bug;

# check whether a bug has a flag set (such as 'needinfo')
def hasflag(bug, status, name):
    if 'flags' in bug:
        flags = bug['flags']
        for flag in flags:
            if flag['status'] == status and flag['name'] == name:
                return True
    return False

# print the description of a bug
def printbug(bug):
    print 'Bug', bug['number'], '-', bug['summary']
    print 'Status:', bug['status'], '[NEEDINFO]' if hasflag(bug, '?', 'needinfo') else ''
    if 'whiteboard' in bug:
        print 'Whiteboard:', bug['whiteboard']
    if 'keywords' in bug:
        print 'Keywords:', bug['keywords']
    print 'Assigned to:', bug['assigned_to']['real_name']
    print 'Modified:', localtime(bug['last_change_time'])
    for field in bug:
        if field[0:3] == 'cf_' and not bug[field] == '---':
            name = field[3:].replace('_', '-')
            print name + ':', bug[field]

# initialize timezone processing
time.tzset()

# process command line arguments
argv = sys.argv
argc = len(argv)

if (argc > 1):
    if isnumber(argv[1]):
        printbug(getbug(argv[1]))
        exit(0)
    print 'not supported:', argv[1]
    exit(0)

print "bug number"
