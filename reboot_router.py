import sys
import urllib
import urllib2
import getopt
import re

def usage():
    print "python reboot_router.py --user router_user --password router_password\n"


def main(argv):
    # Make sure that we have arguments
    if len(argv) == 1:
        usage()
        sys.exit(2)

    # TODO: check optparse. It might be more intuitive
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

    # Cable Modem config page
    theurl = "http://192.168.100.1/configdata.html"

    # I've used Wireshark to see which values where used to restart the modem
    headers = {'Host': '192.168.100.1',
               'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.6) Gecko/20091223 Gentoo Firefox/3.5.6',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language': 'en-us,en;q=0.5',
               'Accept-Encoding': 'gzip,deflate',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
               'Keep-Alive': '300',
               'Connection': 'keep-alive',
               'Referer': 'http://192.168.100.1/configdata.html',
               'Content-Type': 'application/x-www-form-urlencoded'}
    # 'Content-Length': '113' # This is automatically calculated by urllib2
    post_values = {'FREQ_PLAN':'NORTH_AMERICA',
                   'US_CHANNEL_ID':'39',
                   'FREQUENCY_MHZ':'573000000',
                   'DHCP_SERVER':'YES',
                   'BUTTON_INPUT':'Restart Cable Modem'}
    encoded_post_values = urllib.urlencode(post_values)

    request = urllib2.Request(theurl, encoded_post_values, headers)
    try:
        response = urllib2.urlopen(request)
        command_answer = response.read()
    except Exception,e:
        print "Modem page could not be retrieved\nCause: %s\n" % e
        command_answer = None

    if command_answer is not None:
        m = re.search("Your Cable Modem is rebooting in 10 Seconds",command_answer)
        if m == None:
            print "Text not matched"
            print False
        else:
            print "The Modem is rebooting in 10 Seconds"
            print True
    else:
        print False



if __name__ == '__main__':
    main(sys.argv)


#   passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    # this creates a password manager
#   passman.add_password(None, theurl, user, passwd)
    # because we have put None at the start it will always
    # use this username/password combination for  urls
    # for which 'theurl' is a super-url

#   authhandler = urllib2.HTTPBasicAuthHandler(passman)
    # create the AuthHandler

#   opener = urllib2.build_opener(authhandler)

#   urllib2.install_opener(opener)
    # All calls to urllib2.urlopen will now use our handler
    # Make sure not to include the protocol in with the URL, or
    # HTTPPasswordMgrWithDefaultRealm will be very confused.
    # You must (of course) use it when fetching the page though.
