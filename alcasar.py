import urllib.request
import urllib.parse
import sys
import getopt
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

username = ""
password = ""

cert = dir_path + "/alcasar.crt"

argv = sys.argv[1:]

try:
    opts, args = getopt.getopt(argv, "hu:p:", ["username=", "password="])
except getopt.GetoptError:
    print('alcasar.py -u <username> -p <password>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print('alcasar.py -u <username> -p <password>')
        sys.exit()
    elif opt in ("-u", "--username"):
        username = arg
    elif opt in ("-p", "--password"):
        password = arg

if username == "" or password == "":
    print('alcasar.py -u <username> -p <password>')
    sys.exit(2)


def get_challenge(s: str):
    return s.split('input type="hidden" name="challenge" value="')[1][:32]


def get_logon_url(s: str):
    return s.split('http-equiv="refresh" content="0;url=')[1].split("userurl=http://google.com/")[0]


request = urllib.request.urlopen("http://google.com", cafile=cert)

response = request.read().decode()
challenge = get_challenge(response)

data = {"Password": password,
        "UserName": username,
        "button": "Authentication",
        "challenge": challenge,
        "uamip": "172.16.112.1",
        "uamport": "3990",
        "userurl": "http://google.com/"}

headers = {
    'origin': "https://alcasar",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0",
    'content-type': "application/x-www-form-urlencoded",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'referer': "https://alcasar/intercept.php?res=notyet&uamip=172.16.112.1&uamport=3990&challenge=" + challenge,
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "en-US,en;q=0.8,fr-FR;q=0.6,fr;q=0.4"
}

bin_data = urllib.parse.urlencode(data).encode()
request = urllib.request.Request("https://alcasar/intercept.php", bin_data, headers, method="POST")
response = urllib.request.urlopen(request, cafile=cert).read().decode()
urllib.request.urlopen(get_logon_url(response), cafile=cert)

print("Success")
