import requests
import json

CONFIG = {
    'api_token': 'YOUR_API_KEY',
    'zone_id': 'YOUR_ZONE_ID',
    'records': [
        {
            'name': 'FIRST_SUBDOMAIN',
            'record_id': 'FIRST_RECORD_ID_SUBDOMAIN'
        },
        {
            'name': 'SECOND_SUBDOMAIN',
            'record_id': 'FIRST_RECORD_ID_SUBDOMAIN'
        },
        {
            'name': 'THIRD_SUBDOMAIN',
            'record_id': 'THIRD_RECORD_ID_SUBDOMAIN'
        }
    ]
}

public_ip = requests.get('https://icanhazip.com').text.strip()

try:
    with open('last_ip.txt', 'r') as ip_file:
        last_ip = ip_file.read().strip()
except FileNotFoundError:
    last_ip = None

if public_ip != last_ip:
    for record in CONFIG['records']:
        url = f'https://api.cloudflare.com/client/v4/zones/{CONFIG["zone_id"]}/dns_records/{record["record_id"]}'

        headers = {
            'Authorization': f'Bearer {CONFIG["api_token"]}',
            'Content-Type': 'application/json'
        }

        data = {
            'type': 'A',
            'name': record['name'],
            'content': public_ip,
            'ttl':   120,
            'proxied': False
        }

        response = requests.put(url, headers=headers, json=data)

       if response.status_code ==   200:
            print(f'DNS record for {record["name"]} actualizado exitosamente.')
        else:
            print(f'Error updating the DNS record for {record["name"]}: {response.content}')

    with open('last_ip.txt', 'w') as ip_file:
        ip_file.write(public_ip)
else:
    print('The IP hasn't changed, no need to update the DNS records.')

