# Installation

## Standard Installation

```bash
pip install twscrape
```

## Development Version

Install the latest development version directly from GitHub:

```bash
pip install git+https://github.com/vladkens/twscrape.git
```

## Requirements

- Python 3.7+
- asyncio support
- Internet connection for Twitter/X access

## Dependencies

The library automatically installs required dependencies:
- `httpx` - Async HTTP client
- `aiosqlite` - Async SQLite database
- Additional dependencies as specified in setup.py

## Verification

Verify installation:

```bash
# Check CLI is available
twscrape --help

# Check Python import works
python -c "from twscrape import API; print('OK')"
```

## Upgrading

```bash
pip install --upgrade twscrape
```

## Uninstallation

```bash
pip uninstall twscrape
```

## Database Location

By default, twscrape creates `accounts.db` in your current working directory. You can specify a custom location:

```python
api = API("path/to/custom.db")
```

Or via CLI:

```bash
twscrape --db path/to/custom.db <command>
```
