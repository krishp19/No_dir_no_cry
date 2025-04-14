const { Command } = require('commander');
const axios = require('axios');
const chalk = require('chalk');
const fs = require('fs');
const pLimit = require('p-limit').default;

const program = new Command();

program
  .option('-u, --url <urls>', 'target URL(s)', (val) => val.split(','))
  .option('-w, --wordlist <file>', 'path to wordlist')
  .option('-c, --concurrency <number>', 'number of parallel requests', '5')
  .parse();

const options = program.opts();
const concurrency = parseInt(options.concurrency) || 5;

// Ensure URL is properly formatted
function formatUrl(url) {
  if (!/^https?:\/\//i.test(url)) {
    url = 'http://' + url;
  }
  return url;
}

// Function to check if a specific path exists
async function checkURL(baseURL, word) {
  const formattedURL = formatUrl(baseURL);
  const target = `${formattedURL}/${word}`;

  try {
    const response = await axios.get(target, {
      maxRedirects: 5,
      validateStatus: (status) => status >= 200 && status < 400, // Treat 2xx and 3xx as valid
    });

    if (response.status >= 200 && response.status < 400) {
      console.log(chalk.green(`✔ Found: ${target} (Status: ${response.status})`));
    } else {
      console.log(chalk.yellow(`✖ Not Found: ${target} (Status: ${response.status})`));
    }
  } catch (error) {
    if (error.response) {
      console.log(chalk.red(`⚠ Error: ${target} - Status: ${error.response.status}`));
    } else {
      console.log(chalk.red(`⚠ Error: ${target} - Network issue or timeout`));
    }
  }
}

// Main scan function
async function startScan(urls, wordlistPath) {
  const words = fs.readFileSync(wordlistPath, 'utf-8')
    .split('\n')
    .map(line => line.trim())
    .filter(line => line.length > 0);

  if (words.length === 0) {
    console.log(chalk.yellow('⚠ Wordlist is empty.'));
    return;
  }

  const limit = pLimit(concurrency);

  for (const url of urls) {
    console.log(chalk.blue(`\n🔍 Starting scan on: ${url}`));

    const tasks = words.map(word => limit(() => checkURL(url, word)));

    await Promise.all(tasks);
  }

  console.log(chalk.cyan('\n✅ Scan completed.'));
}

// Validation
if (!options.url || !options.wordlist) {
  console.log(chalk.red('❌ Error: Please provide both URL(s) and wordlist.'));
  program.help();
  process.exit(1);
}

// Start the scan
startScan(options.url, options.wordlist);
