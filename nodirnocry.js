const { Command } = require('commander');
const axios = require('axios');
const chalk = require('chalk');
const fs = require('fs');
const path = require('path');

// Utility to pause execution
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

const program = new Command();

program
  .option('-u, --url <urls>', 'target URL(s)', val => val.split(','))
  .option('-w, --wordlist <file>', 'path to wordlist')
  .option('-d, --delay <ms>', 'delay between requests in milliseconds', parseInt)
  .parse();

const options = program.opts();

function formatUrl(url) {
  if (!/^https?:\/\//i.test(url)) {
    url = 'http://' + url;
  }
  return url;
}

async function checkURL(baseURL, word) {
  const formattedURL = formatUrl(baseURL);
  try {
    const response = await axios.get(`${formattedURL}/${word}`, {
      maxRedirects: 5,
      validateStatus: (status) => status >= 200 && status < 400,
    });

    if (response.status >= 200 && response.status < 400) {
      console.log(chalk.green(`Found: ${formattedURL}/${word} (Status: ${response.status})`));
    } else {
      console.log(chalk.yellow(`Not Found: ${formattedURL}/${word} (Status: ${response.status})`));
    }
  } catch (error) {
    if (error.response) {
      console.log(chalk.red(`Error: ${formattedURL}/${word} - Status: ${error.response.status}`));
    } else {
      console.log(chalk.red(`Error: ${formattedURL}/${word} - Network issue or timeout`));
    }
  }
}

async function startScan(urls, wordlist, delay = 0) {
  for (const url of urls) {
    console.log(chalk.blue(`Starting scan on: ${url}`));
    const words = fs.readFileSync(wordlist, 'utf-8')
      .split('\n')
      .map(line => line.trim())
      .filter(line => line.length > 0);

    if (words.length === 0) {
      console.log(chalk.yellow('Warning: Wordlist is empty.'));
      return;
    }

    for (const word of words) {
      await checkURL(url, word);
      if (delay) await sleep(delay);
    }
  }
}

if (!options.url || !options.wordlist) {
  console.log(chalk.red('Error: URL(s) and wordlist are required.'));
  process.exit(1);
}

const scanDelay = options.delay || 0;
startScan(options.url, options.wordlist, scanDelay);
