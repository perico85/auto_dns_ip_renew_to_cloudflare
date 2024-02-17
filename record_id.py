import requests
import json

cloudflare_api = "https://api.cloudflare.com/client/v4/"
zone_id = "YOUR_ZONE_ID"
auth_key = "YOUR_API_KEY"
headers = {'Authorization': f'Bearer {auth_key}', 'Content-Type':'application/json'}

cloudflare_dns = cloudflare_api + "zones/" + zone_id + "/dns_records"   
cloudflare_dns_response = requests.get(cloudflare_dns, headers=headers)

subdomains = ['FIRST_SUBDOMIAIN', 'SECOND_SUBDOMIAIN', 'THIRD_SUBDOMIAIN'] #REMOVE SUBDOMAIN IF YOU DONT HAVE

record_ids = {}

if cloudflare_dns_response.status_code ==  200:
    dns_data = json.loads(cloudflare_dns_response.text)
    for record in dns_data['result']:
        if record['name'] in subdomains:
            record_ids[record['name']] = record['id']
            print(f"Record ID for {record['name']}: {record['id']}")
else:
    print(f"Error to obtain subdomain DNS: {cloudflare_dns_response.status_code}")

print("Record IDs founded:", record_ids)

