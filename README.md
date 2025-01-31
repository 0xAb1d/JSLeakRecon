# **JSLeakRecon** 

**JSLeakRecon** is an ultimate JavaScript scanning tool designed for **offensive security professionals**, **defensive security analysts**, **penetration testers**, **bug hunters**, and **developers**. This tool helps to detect **potential credential leaks**, hardcoded sensitive information (like API keys, tokens, secrets), and other security vulnerabilities in JavaScript files. With features like **real-time URL scanning**, **multithreading**, and **stealth user-agent rotation**, JSLeakRecon is crucial for both proactive identification of security flaws before production (for defensive use) and effective reconnaissance in offensive security contexts.

![IMG_2065 JPEG](https://github.com/user-attachments/assets/9aab6b2d-8e0d-4e55-99da-8513dfc05e23)

![IMG_2066 JPEG](https://github.com/user-attachments/assets/0e5ee960-66d9-4823-9a94-34ed6b6d5417)

![IMG_2067 JPEG](https://github.com/user-attachments/assets/83db0610-b153-4c91-b2dc-5c68f046db5b)


## **Table of Contents**
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Customization](#customization)
- [License](#license)

---

## **Features**
- **Real-time scanning of JavaScript files** from URLs or Local filesystem.
- Detects **hardcoded credentials** like passwords, API keys, tokens, and other secrets.
- Supports **multithreaded scanning** for faster results.
- **Stealth scanning** with random **user-agent rotation** for web anonymity.
- Customizable regex patterns through `regex.yaml` for specific leak detection.
- Generates reports in **HTML**, **TXT**, and **log file** formats.
- Supports scanning of both local `.js` files and web-based JavaScript files.

---

## **Installation**

To get started with JSLeakRecon, you'll need to have **Python 3.x** installed. You can install the required dependencies by following the steps below:

1. Clone the repository:
   ```bash
   git clone https://github.com/0xAb1d/JSLeakRecon.git
   cd JSLeakRecon
   ```


2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## **Usage**
JSLeakRecon allows you to scan JavaScript files either from URLs or from a local folder. You can also customize the number of threads for multithreaded scanning and specify an output format.

```
➜ python3 jsleakrecon.py


      _ ____  _               _    ____
     | / ___|| |    ___  __ _| | _|  _ \ ___  ___ ___  _ __
  _  | \___ \| |   / _ \/ _` | |/ / |_) / _ \/ __/ _ \| '_ \
 | |_| |___) | |__|  __/ (_| |   <|  _ <  __/ (_| (_) | | | |
  \___/|____/|_____\___|\__,_|_|\_\_| \_\___|\___\___/|_| |_|
                                                    v1.4

          By Abid Ahmad [0xAb1d]

usage: jsleakrecon.py [-h] [-l LIST] [-f FOLDER] [-o OUTPUT] [-t THREADS]

JSLeakRecon - Scanning Potential Leaks in JavaScript Files.

options:
  -h, --help            show this help message and exit
  -l LIST, --list LIST  Path to the list of JavaScript files or URLs (e.g.,
                        jslist.txt)
  -f FOLDER, --folder FOLDER
                        Path to a folder containing JavaScript files to scan
  -o OUTPUT, --output OUTPUT
                        Output file for results (e.g., output.txt or
                        output.html)
  -t THREADS, --threads THREADS
                        Number of threads to use (default: 10)

```

Command-Line Arguments:
- `-l`, `--list`: Path to the list of JavaScript files or URLs (e.g., jslist.txt).
- `-f`, `--folder`: Path to a folder containing JavaScript files to scan.
- `-o`, `--output`: Output file for results (output.txt or output.html).
- `-t`, `--threads`: Number of threads to use (default: 10).

Example Usage
Scan a list of URLs from a file:
```
python3 jsleakrecon.py -l jslist.txt
```

Scan a folder of local JavaScript files:
```
python3 jsleakrecon.py -f /path/to/js/files
```

Save results to an HTML file:
```
python3 jsleakrecon.py -l jslist.txt -o results.html
```

Multithreaded scanning (20 threads):
```
python3 jsleakrecon.py -l jslist.txt -t 20 -o output.html
```

Output Formats
- **HTML Report**: A HTML report with structured results.
- **TXT Report**: Simple text format that contains the cleaned result values.
- **Log File**: Automatically generated log file with details about the scan.

## **Customization**
You can modify the regex patterns used by JSLeakRecon by editing the regex.yaml file. This allows you to add or update patterns to detect new types of sensitive data.

Example regex.yaml file format:
```
patterns:
  # Generic password patterns with length enforcement (min 5 characters)
  generic_password_patterns:
    - "(?i)\\b(pass|password|passwd|pwd|passcode|passphrase|pin)\\b\\s*[:=]\\s*['\"]?([a-zA-Z0-9@#$_%&*!+-]{8,})['\"]?"  # Enforcing at least 5 characters

  # Generic username patterns with length enforcement (min 3 characters)
  generic_username_patterns:
    - "(?i)\\b(user|username|login|usr|uid|userid|uname|admin_user|root_user|db_user|email)\\b\\s*[:=]\\s*['\"]?([a-zA-Z0-9-_@.]{5,})['\"]?"

  # Generic secret patterns (API keys, tokens, etc.) with length enforcement (min 8 characters)
  generic_secret_patterns:
    - "(?i)\\b(secret|token|auth_token|api_key|apiKey|access_token|session_token|jwt_token|encryption_key|ssh_key|crypt_key|access_key)\\b\\s*[:=]\\s*['\"]?([a-zA-Z0-9-_]{8,})['\"]?"

  # Patterns for comments that might contain sensitive data
  comments_patterns:
    - "(?i)(?:#|\\/\\/|\\/\\*|<!--)\\s*(pass|password|passwd|pwd|user|username|secret|token|auth_token|api_key|apiKey|access_key)\\s*[:=]\\s*['\"]?([a-zA-Z0-9@#$_%&*!+-]{5,})['\"]?"

```

## **License**
JSLeakRecon is licensed under the [MIT License](https://github.com/0xAb1d/JSLeakRecon/blob/main/LICENSE). You are free to use, modify, and distribute this tool under the terms of the license.


