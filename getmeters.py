from lxml import html
from ConfigParser import SafeConfigParser
import requests
import smtplib

# Pull from IP file, must be in the same directory as the main file ("getmeters.py")
iplist_file = "iplist.txt"
body_list = []

# Main crawler file - does NOT send mail from crawled method
def crawler(url_ip):
    global eqid, counter, serial, body_list
    print "Starting Crawler Service for: " + url_ip

    url = "http://" + url_ip + "/cgi-bin/dynamic/printer/config/reports/deviceinfo.html"
    urleqid = "http://" + url_ip + "/cgi-bin/dynamic/topbar.html"
    response = requests.get(url)
    tree = html.fromstring(response.text)
    # xpath sequence should be pulled using the google source inspection
    counter = tree.xpath('//td[contains(p,"Count")]/following-sibling::td/p/text()')
    serial = tree.xpath('//td[contains(p, "Serial")]/following-sibling::td/p/text()')
    counter = counter[0].split(' ')[3]
    serial = serial[0].split(' ')[3]
    responseeqid = requests.get(urleqid)
    treeequid = html.fromstring(responseeqid.text)
    eqid = treeequid.xpath('//descendant-or-self::node()/child::b[contains(., "Location")]/text()')[1].split(' ')[-1]

    # print basic data
    print " -- equipment id found: " + eqid
    print " -- count found: " + counter
    print " -- serial found: " + serial


    body_of_email = "Equipment ID = " + eqid + "<br>Total Meter Count = " + counter + "<br>Serial Number = " + serial + "<br><br>"
    body_list.append(body_of_email)


    print "Stopping Crawler Service for: " + url_ip
    return


# -- THIS MUST BE RESET INTO A PULL FROM A CONF FILE --
# -- CHANGE THE SETTINGS TO REFLECT GENERAL INFORMATION NOT SPECIFIC TO COMPANY
def send_mail(eqid,counter,serial):

    parser = SafeConfigParser()
    parser.read("settings.conf")

    GMAIL_USERNAME = parser.get('SMTP', 'gmail_user')
    GMAIL_PASSWORD = parser.get('SMTP', 'gmail_pass')

    recipient = parser.get('SMTP', 'gmail_recipient')
    email_subject = parser.get('SMTP', 'email_subject')

    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.ehlo()
    session.starttls()
    session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

    headers = "\r\n".join(["from: " + GMAIL_USERNAME,
                        "subject: " + email_subject,
                        "to: " + recipient,
                        "mime-version: 1.0",
                        "content-type: text/html"])

    content = headers + "\r\n\r\n" + ''.join(body_list)
    session.sendmail(GMAIL_USERNAME, recipient, content)
    return

with open(iplist_file) as fp:
    for line in fp:
        crawler(line.rstrip());

send_mail(eqid,counter,serial);
