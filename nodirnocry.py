import requests
import argparse
import time
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init
from pyfiglet import Figlet


init(autoreset=True)

def print_banner():
    f = Figlet(font='slant')  # You can try 'standard', 'slant', 'block', etc.
    print(Fore.MAGENTA + f.renderText("NoDirNoCry") + Style.RESET_ALL)


def format_url(url):
    if not url.startswith(('http://', 'https://')):
        return 'http://' + url
    return url

def check_url(base_url, path):
    full_url = f"{base_url.rstrip('/')}/{path.strip()}"
    try:
        response = requests.get(full_url, timeout=5, allow_redirects=True)
        if response.status_code < 400:
            print(f"{Fore.GREEN}[+] Found: {full_url} [{response.status_code}]")
        else:
            print(f"{Fore.YELLOW}[-] Not Found: {full_url} [{response.status_code}]")
    except requests.RequestException as e:
        print(f"{Fore.RED}[!] Error: {full_url} ({e})")

def main():
    print_banner()  # <- Print ASCII banner first
    parser = argparse.ArgumentParser(description="NoDirNoCry 🕵️ - A simple Python-based directory scanner.")
    parser.add_argument("-u", "--url", required=True, help="Target URL")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to wordlist")
    parser.add_argument("-c", "--concurrency", type=int, default=10, help="Number of concurrent threads")
    parser.add_argument("--delay", type=float, default=0.0, help="Delay between requests in seconds")

    args = parser.parse_args()

    base_url = format_url(args.url)

    try:
        with open(args.wordlist, "r") as file:
            words = [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}[!] Wordlist file not found.")
        return

    print(f"{Fore.CYAN}[*] Starting scan on {base_url} with {args.concurrency} threads...")

    with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        for word in words:
            executor.submit(check_url, base_url, word)
            if args.delay:
                time.sleep(args.delay)

if __name__ == "__main__":
    main()
