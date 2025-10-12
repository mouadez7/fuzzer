#!/usr/bin/python3

import sys
import getopt
import requests
import concurrent.futures

target_url = ""
wordlist_file = ""
filter_status = ""
filter_size = ""
threads = 5


def usage():
    print("Simple Directory Fuzzer")
    print("Usage: python3 fuzzer.py -u URL -w WORDLIST [options]")
    print()
    print("Required Arguments:")
    print("  -u, --url        Target URL")
    print("  -w, --wordlist   Path to wordlist file")
    print()
    print("Options:")
    print("  -s, --status     Hide these status codes (ex: 401,404)")
    print("  -z, --size       Hide these sizes (ex: 1235,6755)")
    print("  -t, --threads    Number of threads (default: 5, max: 20)")
    print()
    print("Examples:")
    print("  python3 fuzzer.py -u https://example.com -w wordlist.txt")
    print("  python3 fuzzer.py -u https://example.com -w wordlist.txt -s 404 -t 10")
    print("  python3 fuzzer.py -u https://example.com -w wordlist.txt -z 6755")
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


def fuzz_word(word_data):
    word, target_url, status_list, size_list = word_data

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

        except:
            pass

    return None, False


def main():
    global target_url, wordlist_file, filter_status, filter_size, threads

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hu:w:s:z:t:",
                                   ["help", "url=", "wordlist=", "status=", "size=", "threads="])
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
        elif o in ("-t", "--threads"):
            threads = int(a)
            if threads > 20:
                print("[!] Maximum threads for fuzzing is 20")
                threads = 20
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
    print("[*] Threads: " + str(threads))

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

    word_data = [(word, target_url, status_list, size_list) for word in words]

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(fuzz_word, word_data)

    print("=" * 100)
    print("[*] Fuzzing completed.")


if __name__ == "__main__":
    main()
