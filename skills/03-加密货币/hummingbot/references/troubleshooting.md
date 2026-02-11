# Hummingbot - Troubleshooting

**Pages:** 1

---

## Troubleshooting - Hummingbot

**URL:** https://hummingbot.org/troubleshooting/

**Contents:**
- Troubleshooting
- Installation¶
  - Docker: Permission denied error¶
  - Source: conda command not found¶
  - Source: ./install: line 40 ... Killed¶
  - Source: Could not find conda environment: hummingbot¶
  - Source: unable to execute gcc: No such file or directory¶
- Dashboard¶
  - Failed to connect MQTT Bridge:¶
  - Docker is not running. Please start Docker and refresh the page.¶

The error message above indicates a permission issue while trying to access the Docker daemon socket. This is a common problem when trying to run Docker commands as a non-root user. To add your user to the docker group, use the following command:

Ensure Anaconda, Miniconda, or Miniforge (for arm64 systems) is installed. If you've just installed it, restart your terminal to refresh the command line environment.

Collecting package metadata (repodata.json): / ./install: line 40: 14981 Killed... This error shows up during installation, typically on systems with 2GB RAM or less. Increase your system's RAM to at least 4GB, or consider adding a swap file if upgrading hardware is not feasible.

This is related to the issue above. Check if there are any errors after running the ./install script. If there are, you'll need to solve those first otherwise creating the hummingbot conda environment will fail.

If getting this error you'll need to install the build-essential package. Run the command below to install -

If you get this error, this usually means the Hummingbot Broker is not running, start the Broker from the Instances page and then restart all Hummingbot client instances.

Make sure you have Docker installed. On Windows and MacOS machines make sure you have Docker Desktop running in the background.

Note: The name of the missing module could be something else like st_pages etc. If you get this message this means the environment wasn't installed properly. Run the following steps in a terminal to reinstall -

By default the authentication system is disabled.

Find the variable AUTH_SYSTEM_ENABLED in the CONFIG.py file and set it to True to enable the authentication page.

If you are getting this error on Kraken, or a similar error on a different exchange this is because the exchange connector doesn't currently support market orders which the PositionExecutor needs to close the position.

If you get this error make sure that when you created the API keys you also checked the Access Websockets API option.

You'll need to approve tokens that you are trading. See below for an example if you are trading WETH on Ethereum mainnet

When approving tokens, if you get a "Token not Supported" error, please make sure to add the token address in the tokenlist manually. The token list can be found in the ./conf/list folder

Use the following command to display token balances for different networks.

This error comes up because CTRL + V doesn't work in Hummingbot. Try any of the following shortcuts below to paste.

Press CTRL + X if you want to cancel out of the configuration

If one or more tokens is showing 0 Total in ($), use the command below to change your rate oracle source. By default, the rate_oracle_source is set to Binance and if the token is not available in Binance then the Total in ($) will show 0.

**Examples:**

Example 1 (unknown):
```unknown
docker: Got permission denied while trying to connect to the Docker daemon socket at
unix:///var/run/docker.sock...
```

Example 2 (unknown):
```unknown
sudo usermod -aG docker $USER

# Restart the terminal after running the command above, if it still doesn't work try the command below

sudo chmod 666 /var/run/docker.sock
```

Example 3 (unknown):
```unknown
$ conda
-bash: conda: command not found
```

Example 4 (unknown):
```unknown
Collecting package metadata (repodata.json): / ./install: line 40: 14981 Killed...
```

---
