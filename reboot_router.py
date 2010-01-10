import sys
import urllib
import urllib2
import getopt

def usage():
    print "python reboot_router.py --user router_user --password router_password\n"


def main(argv):
    if len(argv) == 1:
        usage()
        sys.exit(2)
    try:
        opts, args = getopt.getopt(argv[1:], "hu:p:", ["help","user","passwd"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt,value in opts:
        if opt == "-h":
            usage()
            sys.exit()
        elif opt in ("-u","--user"):
            user = value
        elif opt in ("-p","--passwd"):
            passwd = value
        else:
            print "Unknown parameter: %s/%s" % (opt,value)

    theurl = "http://192.168.100.1"
    encoded_url = theurl

    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    # this creates a password manager
    passman.add_password(None, theurl, user, passwd)
    # because we have put None at the start it will always
    # use this username/password combination for  urls
    # for which 'theurl' is a super-url

    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    # create the AuthHandler

    opener = urllib2.build_opener(authhandler)

    urllib2.install_opener(opener)
    # All calls to urllib2.urlopen will now use our handler
    # Make sure not to include the protocol in with the URL, or
    # HTTPPasswordMgrWithDefaultRealm will be very confused.
    # You must (of course) use it when fetching the page though.

    try:
        pagehandle = urllib2.urlopen(encoded_url)
        print pagehandle.read()
    except:
        pagehandle = None
    # authentication is now handled automatically for us


if __name__ == '__main__':
    main(sys.argv)


