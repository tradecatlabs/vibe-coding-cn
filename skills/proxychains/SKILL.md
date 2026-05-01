---
name: proxychains
description: "proxychains4 network fallback skill: detect timeouts, DNS failures, blocked GitHub/PyPI/npm/curl/git access, configure http://127.0.0.1:9910, and retry commands through proxychains."
---

# proxychains Skill

Use this skill when network commands fail or known slow/blocked sources need a transparent TCP proxy through `proxychains4`.

## When to Use This Skill

Trigger when any of these applies:
- `curl`, `wget`, `git`, `pip`, `npm`, `yarn`, `docker pull`, or `ssh` fails with timeout, DNS, reset, refused, 403, or 451-like access errors.
- Accessing GitHub, raw GitHub content, PyPI, npm registry, Docker registries, or other known slow foreign resources.
- Configuring a local proxychains profile that points to `http://127.0.0.1:9910`.
- Diagnosing whether failure is proxy service down, proxychains config wrong, unsupported UDP/static binary behavior, or upstream blocked.

## Not For / Boundaries

- Not for bypassing legal, account, regional, or enterprise security restrictions.
- Not useful for UDP-only traffic or statically linked binaries that proxychains cannot intercept.
- Do not proxy commands that should remain on a trusted private network without checking routing and policy.
- Required inputs: failed command, full error text, target domain, proxy endpoint, OS package name, and whether the proxy service is running.
- If proxychains retry also fails, inspect proxy service health before repeating the same command.

## Quick Reference

### Common Patterns

**Install on Debian/Ubuntu**
```bash
sudo apt install proxychains4
```

**Create user config for the local proxy**
```bash
mkdir -p ~/.proxychains
cp skills/proxychains/references/proxychains.conf ~/.proxychains/proxychains.conf
```

**Test the proxy**
```bash
proxychains4 curl https://ipinfo.io/json
```

**Retry a failed curl**
```bash
proxychains4 curl https://github.com/user/repo
```

**Retry a failed git clone**
```bash
proxychains4 git clone https://github.com/user/repo.git
```

**Retry a failed pip install**
```bash
proxychains4 pip install requests
```

**Retry a failed npm install**
```bash
proxychains4 npm install package-name
```

**Retry a failed Docker pull**
```bash
proxychains4 docker pull image:tag
```

**Inspect effective config**
```bash
proxychains4 -f ~/.proxychains/proxychains.conf curl https://example.com
```

## Examples

### Example 1: GitHub Clone Timeout

- Input: `git clone` fails with a connection timeout.
- Steps:
  1. Retry with `proxychains4 git clone ...`.
  2. If it fails, run `proxychains4 curl https://github.com` to isolate Git vs network.
  3. Check local proxy service on `127.0.0.1:9910`.
- Expected output / acceptance: clone succeeds or failure is classified as proxy service/config/upstream issue.

### Example 2: PyPI Install Fails

- Input: `pip install` cannot reach PyPI.
- Steps:
  1. Retry with `proxychains4 pip install <package>`.
  2. If DNS still fails, confirm `proxy_dns` is enabled in config.
  3. Avoid writing credentials into `pip.conf` unless explicitly required.
- Expected output / acceptance: package install succeeds through proxy or produces a new non-network error.

### Example 3: Unsupported Traffic Diagnosis

- Input: proxychains retry does not affect a command.
- Steps:
  1. Confirm the command uses TCP and dynamic linking.
  2. Test the proxy with a known-good `curl`.
  3. Use application-native proxy options if proxychains cannot intercept it.
- Expected output / acceptance: unsupported mode is identified instead of repeatedly retrying.

## References

- `references/index.md`: navigation for local proxychains references.
- `references/proxychains.conf`: default config targeting `127.0.0.1:9910`.
- `references/quick-reference.md`: command snippets and common scenarios.
- `references/setup-guide.md`: installation and setup notes.
- `references/troubleshooting.md`: failure classification.
- `scripts/setup-proxy.sh`: helper script for local setup.

## Maintenance

- Sources: local proxychains reference files and config template.
- Last updated: 2026-04-28
- Known limits: proxychains relies on `LD_PRELOAD` style interception and is not universal; prefer native proxy settings when available.
