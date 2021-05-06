# api tester
import requests

def main():
    endpoint = 'users?userId=abc123'
    url = 'http://127.0.0.1:5000'+'/'+endpoint

    # is not relevant for all types of calls
    data = {'userId':'abc123'}
    
    resp = requests.get(url, data=data)
    
    resp = resp.json()

    print(resp)
    

if __name__ == '__main__':
    main()
