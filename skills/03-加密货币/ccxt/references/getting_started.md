# Ccxt - Getting Started

**Pages:** 1

---

## Search code, repositories, users, issues, pull requests...

**URL:** https://github.com/ccxt/ccxt/wiki/Install

**Contents:**
- Install
  - JavaScript (NPM)
  - JavaScript (for use with the <script> tag):
  - Custom JavaScript Builds
  - Python
  - PHP
  - .net/C#
  - Docker
- Proxy

The easiest way to install the ccxt library is to use builtin package managers:

This library is shipped as an all-in-one module implementation with minimalistic dependencies and requirements:

You can also clone it into your project directory from ccxt GitHub repository and copy files manually into your working directory with language extension appropriate for your environment.

An alternative way of installing this library is to build a custom bundle from source. Choose exchanges you need in exchanges.cfg.

JavaScript version of ccxt works both in Node and web browsers. Requires ES6 and async/await syntax support (Node 15+). When compiling with Webpack and Babel, make sure it is not excluded in your babel-loader config.

ccxt crypto trading library in npm

All-in-one browser bundle (dependencies included), served from a CDN of your choice:

You can obtain a live-updated version of the bundle by removing the version number from the URL (the @a.b.c thing) or the /latest/ on our cdn — however, we do not recommend to do that, as it may break your app eventually. Also, please keep in mind that we are not responsible for the correct operation of those CDN servers.

We also provide webpack minified and tree-shaken versions of the library starting from version 3.0.35 - Visit https://cdn.ccxt.com to browse the prebundled versions we distribute.

Note: the file sizes are subject to change.

Here is an example using a custom bybit bundle from our cdn in the browser

The default entry point for the browser is window.ccxt and it creates a global ccxt object:

It takes time to load all scripts and resources. The problem with in-browser usage is that the entire CCXT library weighs a few megabytes which is a lot for a web application. Sometimes it is also critical for a Node app. Therefore to lower the loading time you might want to make your own custom build of CCXT for your app with just the exchanges you need. CCXT uses webpack to remove dead code paths to make the package smaller.

ccxt algotrading library in PyPI

The library supports concurrent asynchronous mode with asyncio and async/await in Python 3.5.3+

The autoloadable version of ccxt can be installed with Packagist/Composer (PHP 8.1+).

It can also be installed from the source code: ccxt.php

It requires common PHP modules:

The library supports concurrent asynchronous mode using tools from ReactPHP in PHP 8.1+. Read the Manual for more details.

ccxt in C# with Nugget (netstandard 2.0 and netstandard 2.1)

You can get CCXT installed in a container along with all the supported languages and dependencies. This may be useful if you want to contribute to CCXT (e.g. run the build scripts and tests — please see the Contributing document for the details on that).

You don't need the Docker image if you're not going to develop CCXT. If you just want to use CCXT – just install it as a regular package into your project.

Using docker-compose (in the cloned CCXT repository):

If you are unable to obtain data from exchanges due to location restrictions read the proxy section.

(If the page is not being rendered for you, you can refer to the mirror at https://docs.ccxt.com/)

---
