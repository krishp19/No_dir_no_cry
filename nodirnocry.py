import requests
import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init
from pyfiglet import Figlet
from tqdm import tqdm

init(autoreset=True)

def print_banner():
    f = Figlet(font='slant')
    print(Fore.MAGENTA + f.renderText("NoDirNoCry") + Style.RESET_ALL)

def format_url(url):
    if not url.startswith(('http://', 'https://')):
        return 'http://' + url
    return url

def get_session(proxy=None):
    session = requests.Session()
    if proxy:
        session.proxies = {
            "http": proxy,
            "https": proxy,
        }
    return session

def check_url(base_url, path, session):
    full_url = f"{base_url.rstrip('/')}/{path.strip()}"
    try:
        response = session.get(full_url, timeout=5, allow_redirects=True)
        return (full_url, response.status_code, None)
    except requests.RequestException as e:
        return (full_url, None, str(e))

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="NoDirNoCry 🕵️ - A simple Python-based directory scanner.")
    parser.add_argument("-u", "--url", required=True, help="Target URL")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to wordlist")
    parser.add_argument("-c", "--concurrency", type=int, default=10, help="Number of concurrent threads")
    parser.add_argument("--delay", type=float, default=0.0, help="Delay between requests in seconds")
    parser.add_argument("--proxy", help="Use proxy for requests (format: http://proxy:port)")

    args = parser.parse_args()
    base_url = format_url(args.url)

    # Get session with proxy support if provided
    session = get_session(args.proxy)

    try:
        with open(args.wordlist, "r") as file:
            words = [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}[!] Wordlist file not found.")
        return

    print(f"{Fore.CYAN}[*] Starting scan on {base_url} with {args.concurrency} threads...\n")

    found = 0
    errors = 0
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        futures = [executor.submit(check_url, base_url, word, session) for word in words]

        with tqdm(total=len(futures), desc="Progress", ncols=75, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed} < {remaining}, {rate_fmt}]") as pbar:
            for future in as_completed(futures):
                url, status_code, error = future.result()

                if status_code is not None:
                    if status_code < 400:
                        found += 1
                        tqdm.write(f"{Fore.GREEN}[+] Found: {url} [{status_code}]")
                    else:
                        tqdm.write(f"{Fore.YELLOW}[-] Not Found: {url} [{status_code}]")
                else:
                    errors += 1
                    tqdm.write(f"{Fore.RED}[!] Error: {url} ({error})")

                pbar.update(1)

                if args.delay:
                    time.sleep(args.delay)

        elapsed = time.time() - start_time
        rps = len(futures) / elapsed if elapsed else 0

        print(f"\n{Fore.CYAN} Scan Complete:")
        print(f"{Fore.GREEN} Total Found: {found}")
        print(f"{Fore.RED} Total Errors: {errors}")
        print(f"{Fore.YELLOW} Requests/sec: {rps:.2f}")
        print(f"{Fore.BLUE} Time Taken: {elapsed:.2f}s\n")

if __name__ == "__main__":
    main()
