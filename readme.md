# 🕵️‍♂️ NoDirNoCry (Python Edition)

**`NoDirNoCry`** is a humorous yet powerful CLI-based directory and file brute-force scanner written in Python. Think of it as the Python cousin of `dirhunt`, but with more sass, ASCII vibes, and stealth mode 🐍🎩

---

## ⚙️ Features

- 🔍 Brute-force scan hidden directories and files  
- 🌐 Support for multiple URLs at once  
- 📁 Custom wordlist support  
- 🐢 Optional delay between each request (for stealth or rate-limited targets)  
- ⚡ Concurrency with adjustable threads  
- ✅ Smart status detection (2xx/3xx → Found, 4xx/5xx → Not Found or Error)  
- 🎨 Colored terminal output with `colorama`  
- 🔤 ASCII banner support using `pyfiglet`

---

## 📦 Installation

```bash
git clone https://github.com/your-username/nodirnocry-python.git
cd nodirnocry-python
pip install -r requirements.txt
```

> Requirements: `requests`, `colorama`, `pyfiglet`

---

## 🚀 Usage

```bash
python nodirnocry.py [options]
```

---

## 🔧 Options

| Flag                  | Description                            | Example                                      |
|-----------------------|----------------------------------------|----------------------------------------------|
| `-u`, `--url`         | Target URL(s), comma-separated         | `-u https://example.com,https://test.com`    |
| `-w`, `--wordlist`    | Path to the wordlist file              | `-w wordlist.txt`                            |
| `-d`, `--delay`       | Delay between requests in milliseconds | `-d 1000` (1 second)                         |
| `-c`, `--concurrency` | Number of concurrent requests          | `-c 10`                                      |
| `-h`, `--help`        | Show help                              | `python nodirnocry.py --help`                |
| `--proxy`             | Proxy to use for the requests          | `--proxy http://proxy.com:8080`              |

## 🧪 Examples

**Basic scan:**
```bash
python nodirnocry.py -u https://example.com -w wordlist.txt
```

**Multiple URLs:**
```bash
python nodirnocry.py -u https://site1.com,https://site2.com -w paths.txt
```

**Stealth mode with delay:**
```bash
python nodirnocry.py -u https://mysite.com -w wordlist.txt -d 1000
```

**Aggressive scan with concurrency:**
```bash
python nodirnocry.py -u https://secure.net -w topdirs.txt -c 20
```
**Using Proxy:**
```bash
python nodirnocry.py -u https://example.com -w wordlist.txt --proxy http://proxy.com:8080
```

---

## 📁 Wordlist Format

Just one directory or filename per line:

```
admin
login
config
uploads
images
index.html
robots.txt
```

---

## ✨ Sample Output

```
Starting scan on: https://example.com
✅ Found: https://example.com/admin (Status: 200)
⚠️ Not Found: https://example.com/uploads (Status: 404)
❌ Error: https://example.com/config - Network issue or timeout
```

---

## 🎨 ASCII Banner

When the scan starts, you'll be greeted with a slick **ASCII banner** like this:

```
    _   __      ____  _      _   __      ______
   / | / /___  / __ \(_)____/ | / /___  / ____/______  __
  /  |/ / __ \/ / / / / ___/  |/ / __ \/ /   / ___/ / / /
 / /|  / /_/ / /_/ / / /  / /|  / /_/ / /___/ /  / /_/ /
/_/ |_/\____/_____/_/_/  /_/ |_/\____/\____/_/   \__, /
```

---

## 🧠 Future Enhancements (PRs welcome!)

- 📄 Save results to output file  
- 🎭 Random User-Agent support  
- 🌍 Proxy support  
- 🔀 Wordlist shuffling or random scan order  
- 🧬 Heuristics or AI-based scan suggestions  
- 🧪 Unit tests for core modules  

---

## 🤓 Author

**Krish Prasad**  
Passionate about dev tools, cyber-humor, clean code, and caffeinated late-night debugging ☕🧠

---

## 🪦 Disclaimer

This tool is intended for **educational** and **authorized testing** only.  
**Don’t be a script kiddie — scan responsibly!** ⚠️
