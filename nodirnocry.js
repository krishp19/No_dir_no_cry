const { Command } = require('commander');
const axios = require('axios');
const chalk = require('chalk');
const fs = require('fs');
const path = require('path');

const program = new Command();

program
  .option('-u, --url <urls>', 'target URL(s)', (val) => val.split(','))
  .option('-w, --wordlist <file>', 'path to wordlist')
  .parse();  // No need to pass process.argv, commander does this automatically

const options = program.opts();

// Ensure URLs are correctly formatted (add http:// if not present)
function formatUrl(url) {
  if (!/^https?:\/\//i.test(url)) {
    url = 'http://' + url;
  }
  return url;
}

// Function to check a URL with a word from the wordlist
async function checkURL(baseURL, word) {
  const formattedURL = formatUrl(baseURL);
  try {
    const response = await axios.get(`${formattedURL}/${word}`, {
      maxRedirects: 5, // Follow up to 5 redirects
      validateStatus: (status) => status >= 200 && status < 400, // Handle 2xx and 3xx status codes
    });

    // If we get a 2xx or 3xx status, the route exists (valid)
    if (response.status >= 200 && response.status < 400) {
      console.log(chalk.green(`Found: ${formattedURL}/${word} (Status: ${response.status})`));
    } else {
      // If we get a 4xx or 5xx status, consider it a failure
      console.log(chalk.yellow(`Not Found: ${formattedURL}/${word} (Status: ${response.status})`));
    }
  } catch (error) {
    // Handle other types of errors like network errors, etc.
    if (error.response) {
      // If we get a response with an error status
      console.log(chalk.red(`Error: ${formattedURL}/${word} - Status: ${error.response.status}`));
    } else {
      console.log(chalk.red(`Error: ${formattedURL}/${word} - Network issue or timeout`));
    }
  }
}

// Function to start scanning for each URL
async function startScan(urls, wordlist) {
  for (const url of urls) {
    console.log(chalk.blue(`Starting scan on: ${url}`));
    const words = fs.readFileSync(wordlist, 'utf-8').split('\n').map(line => line.trim()).filter(line => line.length > 0);

    if (words.length === 0) {
      console.log(chalk.yellow('Warning: Wordlist is empty.'));
      return;
    }

    // Loop through each word in the wordlist and check
    for (const word of words) {
      await checkURL(url, word);
    }
  }
}

// Validate if URLs and wordlist are provided
if (!options.url || !options.wordlist) {
  console.log(chalk.red('Error: URL(s) and wordlist are required.'));
  process.exit(1);
}

// Start the scan
startScan(options.url, options.wordlist);
