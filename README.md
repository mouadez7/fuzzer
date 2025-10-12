# fuzzer.py

Simple Directory Fuzzer

Description
-----------
A lightweight directory and file fuzzer built using Python and the `requests` library. Useful for discovering hidden paths and resources on a web server.

Usage
-----
Usage: python3 fuzzer.py -u URL -w WORDLIST [options]

Required Arguments:
  -u, --url        Target URL
  -w, --wordlist   Path to wordlist file

Options:
  -s, --status     Hide these status codes (ex: 401,404)
  -z, --size       Hide these sizes (ex: 1235,6755)
  -t, --threads    Number of threads (default: 5, max: 20)

Examples:
  python3 fuzzer.py -u https://example.com -w wordlist.txt
  python3 fuzzer.py -u https://example.com -w wordlist.txt -s 404 -t 10
  python3 fuzzer.py -u https://example.com -w wordlist.txt -z 6755
