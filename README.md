<h1 align="center">
  <img src="lib/img/WAnaBRI-banner.png" alt="WAnaBRI" width="600"/></a>
  <br>
  <br>
  WAnaBRI v0.5
</h1>
<p align="center">
  <b>The Web Application Firewall (WAF) Analyzer tool for BRI</b>
</p>
<p align="center">
  <img src="lib/img/WAnaBRI-run.png" alt="WAnaBRI" width="450px"></a>
  <br>
</p>

## Features

`WAnaBRI` is a specialized tool developed by Bank Rakyat Indonesia (BRI) for the purpose of analyzing web application firewalls (WAFs). As part of BRI's commitment to cybersecurity, this tool plays a crucial role in identifying and understanding the behavior of various WAFs. `WAnaBRI` serves as an essential component in BRI's ongoing efforts to maintain the integrity and security of its web applications and services.

### `WAnaBRI` has three main feature
- Subdomain enumeration
- WAF footprinting (soon)
- WAF testing (soon)

## How does it work?

To do its magic, `WAnaBRI` does the following:

### Subdomain Enumeration

- Enumerate subdomain from target using [SubFinder](https://github.com/projectdiscovery/subfinder)
- Filter the domain by HTTP/HTTPS request response, only accept 200 OK. Code based on GO.

## Usage

```sh
python3 WAnaBRI.py -h
```
This will display help for the tool. Here are all the options it support.

```yaml
usage: WAnaBRI.py [-h] [-S] [--no-filter] [-D] [-t TARGET] [-o OUTPUT] [-V]

Web Application Firewall (WAF) Analyzer BRI - WAnaBRI

options:
  -h, --help            show this help message and exit
  -S, --subdomain-enumeration
                        Enumerate subdomains using SubFinder. Accepts only one target domain, e.g., -S bri.co.id
  --no-filter           Disable filtering of 200 HTTP/HTTPS responses using the domain_checker tool. Default is True.
  -D, --domain-checker  Filter 200 HTTP/HTTPS responses using the domain_checker tool. Accepts only a file, e.g., -D domains.txt
  -t TARGET, --target TARGET
                        Target domain or path to a .txt file containing domains, e.g., -t bri.co.id or -t domains.txt
  -o OUTPUT, --output OUTPUT
                        Name of the output file, e.g., -o output.txt
  -V, --version         Print the current version of WAnaBRI and exit.
```
## Installation

`WAnaBRI` requires **go1.20** to install dependency tools successfully. How to install go could be found [here](https://noureldinehab.medium.com/how-to-install-golang-latest-version-on-kali-linux-1afa2bd64ace).

```console
$ git clone https://github.com/Mufid1804/WAnaBRI.git
$ cd WAnaBRI
$ pip3 install -r requirements.txt
$ chmod +x install_tools.sh
$ ./install_tools.sh
```
## Running WAnaBRI
### Subdomain Enumeration

To run the subdomain enumeraton on a target, just use the following command.

```console
python3 WAnaBRI.py -S -t hackerone.com

 
 __       __   ______                       _______   _______   ______                         
/  |  _  /  | /      \                     /       \ /       \ /      |                                                                                                                                                                     
$$ | / \ $$ |/$$$$$$  | _______    ______  $$$$$$$  |$$$$$$$  |$$$$$$/       ______   __    __                                                                                                                                              
$$ |/$  \$$ |$$ |__$$ |/       \  /      \ $$ |__$$ |$$ |__$$ |  $$ |       /      \ /  |  /  |                                                                                                                                             
$$ /$$$  $$ |$$    $$ |$$$$$$$  | $$$$$$  |$$    $$< $$    $$<   $$ |      /$$$$$$  |$$ |  $$ |                                                                                                                                             
$$ $$/$$ $$ |$$$$$$$$ |$$ |  $$ | /    $$ |$$$$$$$  |$$$$$$$  |  $$ |      $$ |  $$ |$$ |  $$ |                                                                                                                                             
$$$$/  $$$$ |$$ |  $$ |$$ |  $$ |/$$$$$$$ |$$ |__$$ |$$ |  $$ | _$$ |_  __ $$ |__$$ |$$ \__$$ |                                                                                                                                             
$$$/    $$$ |$$ |  $$ |$$ |  $$ |$$    $$ |$$    $$/ $$ |  $$ |/ $$   |/  |$$    $$/ $$    $$ |                                                                                                                                             
$$/      $$/ $$/   $$/ $$/   $$/  $$$$$$$/ $$$$$$$/  $$/   $$/ $$$$$$/ $$/ $$$$$$$/   $$$$$$$ |                                                                                                                                             
                                                                           $$ |      /  \__$$ |                                                                                                                                             
Develop by Muhammad Mufid                                                  $$ |      $$    $$/                      
Copyright (c) 2023 Bank Rakyat Indonesia (Persero) Tbk.                    $$/        $$$$$$/                       
                                                                                                                    
[*] The target website is hackerone.com
[*] Starting subdomain enumeration for hackerone.com using SubFinder

[~] Done! Here's the output:

api.hackerone.com
mta-sts.hackerone.com
fwdkim1.hackerone.com
zendesk1.hackerone.com
a.ns.hackerone.com
b.ns.hackerone.com
resources.hackerone.com
links.hackerone.com
docs.hackerone.com
mta-sts.forwarding.hackerone.com
gslink.hackerone.com
mta-sts.managed.hackerone.com
go.hackerone.com
hackerone.com
events.hackerone.com
zendesk2.hackerone.com
zendesk3.hackerone.com
zendesk4.hackerone.com
www.hackerone.com
info.hackerone.com
support.hackerone.com
design.hackerone.com

[~] Subdomain enumeration finished: File output saved to log/subdomain-enumeration--2023-08-05--16-29-59.txt

[*] Filtering the subdomains using domain_checker

[          ] Failed: http://events.hackerone.com
[          ] Failed: https://events.hackerone.com
[#         ] Success: http://api.hackerone.com
[#         ] Success: https://api.hackerone.com
```
## Support

For any issues or support, please contact Muhammad Mufid at muhammad.mufid@corp.bri.co.id.

## License

Copyright (c) 2023 Bank Rakyat Indonesia (Persero) Tbk. For internal purpose use only.
