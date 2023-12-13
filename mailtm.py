import requests
import time
import json

MAILTM_HEADERS = {   
    "Accept": "application/json",
    "Content-Type": "application/json" 
}

class MailTmError(Exception):
    pass

def _make_mailtm_request(request_fn, timeout = 600):
    tstart = time.monotonic()
    error = None
    status_code = None
    while time.monotonic() - tstart < timeout:
        try:
            r = request_fn()
            status_code = r.status_code
            if status_code == 200 or status_code == 201:
                return r.json()
            if status_code != 429:
                break
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            error = e
        time.sleep(1.0)
    
    if error is not None:
        raise MailTmError(error) from error
    if status_code is not None:
        raise MailTmError(f"Status code: {status_code}")
    if time.monotonic() - tstart >= timeout:
        raise MailTmError("timeout")
    raise MailTmError("unknown error")

def get_mailtm_domains():
    def _domain_req():
        return requests.get("https://api.mail.tm/domains", headers = MAILTM_HEADERS)
    
    r = _make_mailtm_request(_domain_req)

    return [ x['domain'] for x in r ]

def create_mailtm_account(address, password):
    account = json.dumps({"address": address, "password": password})   
    def _acc_req():
        return requests.post("https://api.mail.tm/accounts", data=account, headers=MAILTM_HEADERS)

    r = _make_mailtm_request(_acc_req)
    assert len(r['id']) > 0

#functon to list mail headers
def list_headers():
	def head_req():
		return requests.head("https://api.mail.tm/accounts", data=account)
	res = _make_mailtm_request(head_req)
	return [i['accounts'] for i in res]

#function to handle pagination
def pagination():
	def parser():
		return requests.get("https://api.mail.tm/accounts", data=account, headers=list_headers())
	res = _make_mailtm_request(parser)
	for i in res:
		print(res[i], i)


#function to read an email
def read_mail():
	def fetch_mail():
		return request.get("https://api.mail.tm/messages" data=account, header=MAILTM_HEADERS)
	resp = _make_mailtm_request(fetch_mail)
	return [i['messages'] for i in resp]


def main():
	#call create a new account function
	try:
		new_account = create_mailtm_account("kariukiallan850@gmail.com", 1234)
	except error:
		print("Account creation unsuccessful")
	
	#call list headers of newly created account function
	list_headers()
	#call pagination of headers function
	pagination()
	#call read mail functon
	mail_content = read_mail().time()
	#loop through mail content to check if new mail arrived and update server
	for i in mail_content:
		if mail_content != read_mail().time:
			json.dump(read_mail().time)

if __name__ == "main":
	main()

