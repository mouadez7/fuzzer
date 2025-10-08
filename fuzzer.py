#!/usr/bin/python3

import sys
import getopt
import requests

target_url = ""
wordlist_file = ""
filter_status = ""
filter_size = ""


def usage():
    print("Simple Directory Fuzzer")
    print("Usage: python3 fuzzer.py -u URL -w WORDLIST [options]")
    print()
    print("Required Arguments:")
    print("  -u, --url        Target URL")
    print("  -w, --wordlist   Path to wordlist file")
    print()
    print("Filters:")
    print("  -s, --status     Hide these status codes (ex: 401,404)")
    print("  -z, --size       Hide these sizes (ex: 1235,6755)")
    print()
    print("Examples:")
    print("  python3 fuzzer.py -u http://example.com -w wordlist.txt")
    print("  python3 fuzzer.py -u http://example.com -w wordlist.txt -s 404")
    print("  python3 fuzzer.py -u http://example.com -w wordlist.txt -z 6755")
    sys.exit(0)


def parse_status_filter(status_str):
    status_list = []

    if ',' in status_str:
        for status in status_str.split(','):
            status_list.append(int(status))
    else:
        status_list.append(int(status_str))

    return status_list


def parse_size_filter(size_str):
    size_list = []

    if ',' in size_str:
        for size in size_str.split(','):
            size_list.append(int(size))
    else:
        size_list.append(int(size_str))

    return size_list


def main():
    global target_url, wordlist_file, filter_status, filter_size

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hu:w:s:z:",
                                   ["help", "url=", "wordlist=", "status=", "size="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-u", "--url"):
            target_url = a
        elif o in ("-w", "--wordlist"):
            wordlist_file = a
        elif o in ("-s", "--status"):
            filter_status = a
        elif o in ("-z", "--size"):
            filter_size = a
        else:
            print("flag provided but not defined: " + o)
            usage()

    if not target_url or not wordlist_file:
        print("[-] URL and wordlist are required")
        usage()

    status_list = []
    size_list = []

    if filter_status:
        status_list = parse_status_filter(filter_status)

    if filter_size:
        size_list = parse_size_filter(filter_size)

    print("[*] Starting fuzz for: " + target_url)
    print("[*] Wordlist: " + wordlist_file)

    if status_list:
        print("[*] Hiding status codes: " + str(status_list))
    if size_list:
        print("[*] Hiding sizes: " + str(size_list))

    print("=" * 100)

    try:
        with open(wordlist_file, 'r') as f:
            words = f.read().splitlines()
    except:
        print("[-] Cannot read wordlist file")
        sys.exit(1)

    found_count = 0

    for word in words:
        if word.strip():
            test_url = target_url.rstrip('/') + '/' + word.strip()

            try:
                response = requests.get(test_url, timeout=5)
                status = response.status_code
                size = len(response.content)

                show_result = True

                if status_list and status in status_list:
                    show_result = False

                if size_list and size in size_list:
                    show_result = False

                if show_result:
                    print("[+] " + test_url + " - Status: " + str(status) + " - Size: " + str(size))
                    found_count += 1

            except:
                pass

    print("=" * 100)
    print("[*] Fuzzing completed.")


if __name__ == "__main__":
    main()