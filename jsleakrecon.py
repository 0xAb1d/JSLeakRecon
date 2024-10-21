import re
import yaml
import argparse
import requests
from concurrent.futures import ThreadPoolExecutor
import os
import random
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from colorama import Fore, Style, init
import time

init(autoreset=True)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Mobile/15E148 Safari/604.1"
]

def print_banner():
    banner = r"""

      _ ____  _               _    ____                      
     | / ___|| |    ___  __ _| | _|  _ \ ___  ___ ___  _ __  
  _  | \___ \| |   / _ \/ _` | |/ / |_) / _ \/ __/ _ \| '_ \ 
 | |_| |___) | |__|  __/ (_| |   <|  _ <  __/ (_| (_) | | | |
  \___/|____/|_____\___|\__,_|_|\_\_| \_\___|\___\___/|_| |_|
                                                    v1.4        
    """
    print(f"{Fore.WHITE}{banner}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}          By Abid Ahmad [0xAb1d]{Style.RESET_ALL}\n")

def print_result(category, identified_value, js_file):
    colored_result = (
        f"{Fore.RED}[{category}]{Style.RESET_ALL} "
        f"{Fore.GREEN}[{identified_value}]{Style.RESET_ALL} "
        f"{Fore.WHITE}[{js_file}]{Style.RESET_ALL}\n"
    )
    print(colored_result, end='')

def print_message(message):
    print(f"\n    >> {message}\n")

def load_regex_patterns(yaml_file):
    with open(yaml_file, 'r') as file:
        patterns = yaml.safe_load(file)
        return patterns

def is_url(path):
    return path.startswith("http://") or path.startswith("https://")

def fetch_url_content(url):
    try:
        user_agent = random.choice(USER_AGENTS)  
        headers = {'User-Agent': user_agent}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None

def scan_file(js_file, patterns, results):
    try:
        if is_url(js_file):
            content = fetch_url_content(js_file)
            if content is None:
                return
        else:
            with open(js_file, 'r', encoding='utf-8') as file:
                content = file.read()

        for category, regex_list in patterns['patterns'].items():
            for regex in regex_list:
                matches = re.finditer(regex, content)
                for match in matches:
                    identified_value = match.group(0)
                    print_result(category, identified_value, js_file)
                    results.append({'pattern': category, 'value': identified_value, 'file_path': js_file})
    except Exception as e:
        print(f"Error processing file {js_file}: {e}")

def scan_files(js_files, patterns, max_threads):
    results = []
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(scan_file, js_file, patterns, results) for js_file in js_files]
        for future in futures:
            future.result()
    return results

def generate_html_report(results, output_file, total_files, total_leaks, scan_duration):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.html')
    rendered_html = template.render(
        total_files=total_files,
        total_leaks=total_leaks,
        scan_duration=scan_duration,
        results=results
    )
    with open(output_file, 'w') as f:
        f.write(rendered_html)

def generate_clean_text_report(results, output_file):
    with open(output_file, 'w') as f:
        for result in results:
            f.write(f"{result['value']}\n")

def generate_log_file(results, input_path):
    random_number = random.randint(1, 1000)
    log_filename = f"{Path(input_path).stem}_{random_number}.log"
    with open(log_filename, 'w') as log_file:
        for result in results:
            log_file.write(f"[{result['pattern']}] [{result['value']}] [{result['file_path']}]\n")
    return log_filename

def main():
    parser = argparse.ArgumentParser(description='JSLeakRecon - Scanning Potential Leaks in JavaScript Files.')
    parser.add_argument('-l', '--list', help='Path to the list of JavaScript files or URLs (e.g., jslist.txt)')
    parser.add_argument('-f', '--folder', help='Path to a folder containing JavaScript files to scan')
    parser.add_argument('-o', '--output', help='Output file for results (e.g., output.txt or output.html)')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Number of threads to use (default: 10)')
    args = parser.parse_args()

    print_banner()

    patterns = load_regex_patterns('regex.yaml')

    js_files = []
    if args.list:
        input_file = Path(args.list)
        with open(input_file, 'r') as file:
            js_files = [line.strip() for line in file if line.strip()]
    elif args.folder:
        folder_path = Path(args.folder)
        js_files = [str(p) for p in Path(folder_path).rglob('*.js')]
    else:
        print("Please provide either a list of files/URLs using -l or a folder path using -f.")
        return

    start_time = time.time()
    results = scan_files(js_files, patterns, args.threads)
    end_time = time.time()

    scan_duration = time.strftime("%H:%M:%S", time.gmtime(end_time - start_time))

    log_filename = generate_log_file(results, args.list if args.list else args.folder)

    if args.output:
        output_file = args.output
        extension = os.path.splitext(output_file)[1].lower()
        total_files = len(js_files)
        total_leaks = len(results)

        if extension == ".html":
            generate_html_report(results, output_file, total_files, total_leaks, scan_duration)
        elif extension == ".txt":
            generate_clean_text_report(results, output_file)
        else:
            print("Unsupported file format. Please use .txt or .html.")
            return
        
        print_message(f"Results saved in {output_file}")
    else:
        print_message("No output file specified. Results saved only in the log file.")
    
    print_message(f"Log file saved as {log_filename}")

if __name__ == "__main__":
    main()
