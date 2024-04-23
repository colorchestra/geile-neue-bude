Scrapes a well-known german website for new apartment offers (or anything else) so you'll be the first to know about it. Also notifies you about it, currently implemented to fit a Discord webhook.

## Usage
- Install `beautifulsoup4` and `requests`, e.g. via pip
- Specify your search parameters in Ebay Kleinanzeigen and copy the URL from the address bar
- Copy `config.py.example` to `config.py` and enter your data
- Running `main.py` runs the search once. To do it continuously, use a cronjob, systemd timer or similar, or use `run.sh`. 