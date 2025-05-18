import dns.resolver
import requests
import argparse

def get_nameservers(domain):
    try:
        answers = dns.resolver.resolve(domain, 'NS')
        return sorted([str(rdata).strip('.') for rdata in answers])
    except Exception as e:
        print(f'[!] Error fetching NS for {domain}: {e}')
        return []

def is_cloudflare_ns(ns_list):
    return any(ns.lower().endswith('.ns.cloudflare.com') for ns in ns_list)

def reverse_whois(ns_list, api_key):
    api_url = 'https://reverse-whois.whoisxmlapi.com/api/v2'
    payload = {
        'apiKey': api_key,
        'searchType': 'current',
        'mode': 'purchase',
        'advancedSearchTerms': [
            {'field': 'NameServers', 'term': ns} for ns in ns_list
        ]
    }

    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            return response.json().get('domainsList', [])
        else:
            print(f'[!] API Error {response.status_code}: {response.text}')
            return []
    except Exception as e:
        print(f'[!] API request failed: {e}')
        return []

def filter_domains(domains, keyword):
    return [d for d in domains if keyword.lower() in d.lower()]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('domain', help='The target domain to search for.')
    parser.add_argument('--apikey', help='Your WhoisXML API key.')
    parser.add_argument('--keyword', help='A keyword filter to match domains.', default=None)
    args = parser.parse_args()

    ns_list = get_nameservers(args.domain)
    if not ns_list or not is_cloudflare_ns(ns_list):
        print('[!] Nameservers are not Cloudflare.')
        return

    domains = reverse_whois(ns_list, args.apikey)
    if args.keyword:
        domains = filter_domains(domains, args.keyword)

    for domain in domains:
        print(domain)

if __name__ == '__main__':
    main()
