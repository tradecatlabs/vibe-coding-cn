# Ccxt - Cli

**Pages:** 1

---

## Search code, repositories, users, issues, pull requests...

**URL:** https://github.com/ccxt/ccxt/wiki/CLI

**Contents:**
- CCXT CLI (Command-Line Interface)
- Install globally
- Install
- Usage
  - Inspecting Exchange Properties
  - Calling A Unified Method By Name
  - Calling An Exchange-Specific Method By Name
- Authentication And Overrides
- Unified API vs Exchange-Specific API
  - Run with jq

CCXT includes an example that allows calling all exchange methods and properties from command line. One doesn't even have to be a programmer or write code – any user can use it!

The CLI interface is a program in CCXT that takes the exchange name and some params from the command line and executes a corresponding call from CCXT printing the output of the call back to the user. Thus, with CLI you can use CCXT out of the box, not a single line of code needed.

CCXT command line interface is very handy and useful for:

For the CCXT library users – we highly recommend to try CLI at least a few times to get a feel of it. For the CCXT library developers – CLI is more than just a recommendation, it's a must.

The best way to learn and understand CCXT CLI – is by experimentation, trial and error. Warning: CLI executes your command and does not ask for a confirmation after you launch it, so be careful with numbers, confusing amounts with prices can cause a loss of funds.

The same CLI design is implemented in all supported languages, TypeScript, JavaScript, Python and PHP – for the purposes of example code for the developers. In other words, the existing CLI contains three implementations that are in many ways identical. The code in those three CLI examples is intended to be "easily understandable".

The source code of the CLI is available here:

Clone the CCXT repository:

Change directory to the cloned repository:

Install the dependencies:

The CLI script requires at least one argument, that is, the exchange id (the list of supported exchanges and their ids). If you don't specify the exchange id, the script will print the list of all exchange ids for reference.

Upon launch, CLI will create and initialize the exchange instance and will also call exchange.loadMarkets() on that exchange. If you don't specify any other command-line arguments to CLI except the exchange id argument, then the CLI script will print out all the contents of the exchange object, including the list of all the methods and properties and all the loaded markets (the output may be extremely long in that case).

Normally, following the exchange id argument one would specify a method name to call with its arguments or an exchange property to inspect on the exchange instance.

If the only parameter you specify to CLI is the exchange id, then it will print out the contents of the exchange instance including all properties, methods, markets, currencies, etc. Warning: exchange contents are HUGE and this will dump A LOT of output to your screen!

You can specify the name of the property of the exchange to narrow the output down to a reasonable size.

You can easily view which methods are supported on the various exchanges:

Calling unified methods is easy:

Exchange specific parameters can be set in the last argument of every unified method:

Here's an example of fetching the order book on okx in sandbox mode using the implicit API and the exchange specific instId and sz parameters:

Public exchange APIs don't require authentication. You can use the CLI to call any method of a public API. The difference between public APIs and private APIs is described in the Manual, here: Public/Private API.

For private API calls, by default the CLI script will look for API keys in the keys.local.json file in the root of the repository cloned to your working directory and will also look up exchange credentials in the environment variables. More details here: Adding Exchange Credentials.

CLI supports all possible methods and properties that exist on the exchange instance.

(If the page is not being rendered for you, you can refer to the mirror at https://docs.ccxt.com/)

---
