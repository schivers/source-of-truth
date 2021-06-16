import requests 
import json
from datetime import datetime, date

def _url(path):
    return 'https://api.ciscospark.com/v1' + path

def _fix_at(at):
    at_prefix = 'Bearer '
    if at_prefix not in at:
        return 'Bearer ' + at
    else:
        return at

def post_message_markdown(at, roomId, markdown, toPersonId='', toPersonEmail=''):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json; charset=utf-8'}
    payload = {'roomId': roomId, 'markdown': markdown}
    if toPersonId:
        payload['toPersonId'] = toPersonId
    if toPersonEmail:
        payload['toPersonEmail'] = toPersonEmail
    resp = requests.post(url=_url('/messages'), json=payload, headers=headers)
    message_dict = json.loads(resp.text)
    message_dict['statuscode'] = str(resp.status_code)
    #print(message_dict)
    print("Message sent")
    return message_dict


if __name__ == "__main__":
    url = "http://10.2.84.2:8000/api/extras/object-changes/"
    headers= {'Authorization': "Token 0123456789abcdef0123456789abcdef01234567" }
    response = requests.get("http://10.2.84.2:8000/api/extras/object-changes/")
    
    #Netbox Bot Webex
    at= "OGI2NWYyZWEtNDU1Ny00ZGZmLThhMDYtZTQ0ZDUyODY2MjExOTBmZjM4MTMtMmY3_PF84_0198f08a-3880-4871-b55e-4863ccf723d5"
    roomId="Y2lzY29zcGFyazovL3VzL1JPT00vZjY1MGZhYzAtY2VhNS0xMWViLTg2ODUtYjMzYTEwY2ZjZGVj"

    r= requests.get(url,headers=headers)

    result= r.json()
    result= result['results']
    today = date.today()
    d_string= today.strftime("%Y-%m-%d")

    res= [i for i in result if d_string in i["time"]]

    #print(res)

    a=[("* _%s_ ID: **%s** Action: **%s** Object: %s Link: http://10.2.84.2:8000/extras/changelog/%s/  \n"%(item['time'],item['user_name'],item['action']['label'],item['object_data']['name'],item['id'])) for item in res]

    changelog = ''.join(a)
    output=("## Netbox Change Log {0} \n".format(str(d_string))+changelog)
    
    post_message_markdown(at,roomId,output)