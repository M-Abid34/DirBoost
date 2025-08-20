import requests
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

def banner(target, wordlist, threads):
    print(rf"""
=============================================
   D I R B O O S T  —  Directory Bruteforcer
=============================================
 Target   : {target}
 Wordlist : {wordlist}
 Threads  : {threads}
=============================================
""")

parser = argparse.ArgumentParser(description="Directory Brute Forcer")
parser.add_argument("url", help="The target URL")
parser.add_argument("wordlist", help="Path to the wordlist file")
parser.add_argument("-t", "--threads", type=int, default=4, help="Number of concurrent threads")
args = parser.parse_args()

def check_directory(url, directory):
    """Check a single directory path and return if found."""
    full_url = f"{url.rstrip('/')}/{directory}"
    try:
        response = requests.get(full_url, timeout=5)
        if response.status_code == 200:
            return f'/{directory}'
    except requests.RequestException:
        pass
    return None

def brute_force_directories(url, wordlist, threads):
    with open(wordlist, 'r') as file:
        directories = [line.strip() for line in file if line.strip()]

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(check_directory, url, d): d for d in directories}
        for future in as_completed(futures):
            result = future.result()
            if result:
                print(f"[+] Found directory: {result}")

if __name__ == "__main__":
    if not args.url.startswith("http://") and not args.url.startswith("https://"):
        print("Please provide a valid URL starting with http:// or https://")
    else:
        banner(args.url, args.wordlist, args.threads)
        brute_force_directories(args.url, args.wordlist, args.threads)
