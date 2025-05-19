# 🕵️‍♂️ ReconFlare

**ReconFlare** is a reconnaissance tool that helps you uncover domains associated with the same Cloudflare account as a given target domain by leveraging the fact that each cloudflare account has a pair of nameservers assigned to it and reverse whois.

## ⚙️ Installation

```bash
git clone https://github.com/pe-4/reconflare.git
cd reconflare
pip install requests dnspython
```

## 🔑 Prerequisite: WhoisXML API Key

Get a free API key at https://reverse-whois.whoisxmlapi.com. The free tier allows 500 queries/month.

# Example
`python reconflare.py medium.com --keyword medium --apikey yourapikeyhere`

