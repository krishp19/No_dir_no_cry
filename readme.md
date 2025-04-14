# 🕵️‍♂️ nodirnocry

**`nodirnocry`** is a humorous yet powerful directory and file brute-force scanner written in Node.js. It's like `dirhunt`, but with *more sass and fewer chills* 😎.

---

## ⚙️ Features

- 🔍 Brute-force scan hidden directories and files
- 🌐 Support multiple URLs at once
- 📁 Custom wordlist support
- 🐢 Optional delay between each request (for stealthy scanning)
- ✅ Status detection (2xx/3xx → Found, 4xx/5xx → Not Found or Error)
- 🎨 Color-coded console output (thanks to Chalk)
- 🪶 Lightweight and easy to use

---

## 📦 Installation

```bash
git clone https://github.com/your-username/nodirnocry.git
cd nodirnocry
npm install
🚀 Usage

node nodirnocry.js [options]
🔧 Options:
Flag	Description	Example
-u, --url	Target URL(s), comma-separated	-u https://example.com,https://test.com
-w, --wordlist	Path to the wordlist file	-w wordlist.txt
-d, --delay	Delay between requests (in ms)	-d 1000 (1 second)
-h, --help	Show help	node nodirnocry.js --help
🧪 Examples

Basic scan:
node nodirnocry.js -u https://example.com -w wordlist.txt

Multiple URLs:
node nodirnocry.js -u https://site1.com,https://site2.com -w paths.txt

Stealth mode (1 sec delay):
node nodirnocry.js -u https://mysite.com -w wordlist.txt -d 1000

📁 Wordlist Format
Just one directory or filename per line:

txt

admin
login
config
uploads
images
index.html
robots.txt
✨ Sample Output

Starting scan on: https://example.com
✅ Found: https://example.com/admin (Status: 200)
⚠️ Not Found: https://example.com/uploads (Status: 404)
❌ Error: https://example.com/config - Network issue or timeout
🧠 Future Enhancements (PRs welcome!)
📄 Save results to output file

🎭 Random User-Agent support

🌍 Proxy support

🔀 Wordlist shuffling or random scan order

🧬 Heuristics for deeper scans

🤓 Author
Krish Prasad
Passionate about dev tools, cyber-humor, and clean code.

🪦 Disclaimer
This tool is for educational and authorized testing only.
Don’t be a script kiddie — scan responsibly! ⚠️

