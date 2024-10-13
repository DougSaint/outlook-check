import requests
import random
import time

def check_insta(email):
    max_tentativas = 3
    tentativa_atual = 0

    while tentativa_atual < max_tentativas:
        try:
            proxy_host = 'geo.iproyal.com'
            proxy_port = '12321'
            proxy_user = 'wVqzPNd2ZUgzrJYa'
            proxy_pass = 't65G9bgu4n1FWPBo'

            proxy_url = f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}'

            proxies = {
                'http': proxy_url,
                'https': proxy_url
            }

            app = ''.join(random.choice('1234567890') for _ in range(15))

            session = requests.Session()
            response = session.get('https://www.instagram.com/api/graphql')
            csrf = response.cookies.get_dict().get('csrftoken')

            rnd = str(random.randint(150, 999))
            android_versions = ["23/6.0", "24/7.0", "25/7.1.1", "26/8.0", "27/8.1", "28/9.0"]
            device_brands = ["SAMSUNG", "HUAWEI", "LGE/lge", "HTC", "ASUS", "ZTE", "ONEPLUS", "XIAOMI", "OPPO", "VIVO", "SONY", "REALME"]

            user_agent = f"Instagram 311.0.0.32.118 Android ({random.choice(android_versions)}; {random.randint(100, 1300)}dpi; {random.randint(200, 2000)}x{random.randint(200, 2000)}; {random.choice(device_brands)}; SM-T{rnd}; SM-T{rnd}; qcom; en_US; 545986{random.randint(111,999)})"

            common_data = {'flow': 'fxcal', 'recaptcha_challenge_field': ''}
            data = {'email_or_username': email, **common_data}

            headers = {
                'authority': 'www.instagram.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.5',
                'content-type': 'application/x-www-form-urlencoded',
                'user-agent': user_agent,
                'viewport-width': '384',
                'x-asbd-id': '129477',
                'x-csrftoken': f'{csrf}',
                'x-ig-app-id': app,
                'x-ig-www-claim': '0',
                'x-instagram-ajax': '1007832499',
                'x-requested-with': 'XMLHttpRequest'
            }

            response = requests.post('https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/', headers=headers, data=data, proxies=proxies)

            if 'error_type":"rate_limit_error' in response.text:
                tentativa_atual += 1
                time.sleep(5)
                continue

            if 'email_or_sms_sen' in response.text:
                return 'ok'
            elif 'no_account_found' in response.text:
                return 'no account'
            else:
                return 'unknown_response'

        except requests.exceptions.RequestException as e:
            tentativa_atual += 1
            time.sleep(5)

    return 'max_attempts_reached'