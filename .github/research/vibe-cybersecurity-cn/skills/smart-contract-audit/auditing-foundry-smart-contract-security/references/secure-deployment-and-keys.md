# Secure Deployment & Key Hygiene

The contract code can be flawless and you still lose everything if a **private key
leaks** or you sign a malicious transaction. This is the part most smart-contract
guides skip. Treat keys as the highest-severity asset.

## Golden rules

1. **A real private key or seed phrase NEVER touches a file, env var, shell history, or git.**
2. Plaintext `PRIVATE_KEY=0x...` in `.env` is the #1 leak vector — use an **encrypted keystore** instead.
3. **Separate wallets**: a throwaway dev wallet (testnet only) ≠ the mainnet deployer ≠ your personal MetaMask with real funds.
4. **Hardware wallet (Ledger/Trezor) for any mainnet deploy or admin action** that controls funds.
5. Simulate before broadcasting; verify after.

## Foundry encrypted keystore (`cast wallet`)

Import the key once into an encrypted, password-protected keystore — then reference
it by name. The raw key never appears in commands or files again.

```bash
# Import interactively (key is typed, not in argv/history), set a strong password
cast wallet import deployer --interactive

# Or generate a fresh dev key directly into the keystore
cast wallet new

# List / inspect (addresses only)
cast wallet list
```

Deploy by **account name**, never by `--private-key`:

```bash
# Testnet first — simulate (no --broadcast) then broadcast + verify
forge script script/Deploy.s.sol --account deployer --rpc-url <testnet_rpc>
forge script script/Deploy.s.sol --account deployer --rpc-url <testnet_rpc> --broadcast --verify

# Mainnet (prefer a Ledger):
forge script script/Deploy.s.sol --ledger --hd-paths "m/44'/60'/0'/0/0" --rpc-url <mainnet_rpc> --broadcast --verify
```

In deploy scripts, use `vm.startBroadcast()` with **no argument** (it uses the
`--account`/`--ledger` signer). Avoid `vm.envUint("PRIVATE_KEY")`.

## Anti-leak controls (wire into the project)

```bash
# 1. .gitignore the usual suspects
printf '.env\n.env.*\n*.key\nkeystore/\nbroadcast/\n' >> .gitignore

# 2. Scan history + working tree for secrets (see the implementing-secret-scanning-with-gitleaks skill)
gitleaks detect --no-banner
gitleaks detect --no-banner --log-opts="--all"   # full git history

# 3. Confirm nothing sensitive is tracked
git ls-files | grep -E '\.env$|\.key$|keystore' && echo "REMOVE THESE FROM GIT"
```

If a key was ever committed (even and then deleted): **consider it compromised** —
generate a new one, move funds, and purge history (BFG / `git filter-repo`).

## MetaMask / wallet operational security

- Dedicated browser profile for Web3; review every signature — **read what you sign**.
- Beware **blind signing** and `eth_sign`/`personal_sign` phishing; reject opaque hex.
- Token **approval hygiene**: avoid unlimited `approve`; periodically revoke (revoke.cash); prefer `permit` with deadlines.
- Verify the **contract address and chain id** before interacting; bookmark dApps, don't follow links.
- Add networks/RPCs only from trusted sources — a malicious RPC can lie about state and simulate fake balances.

## RPC & dependency trust

- Pin a reputable RPC (your own node, or a known provider); a hostile RPC can feed false data to scripts and frontends.
- Pin dependency versions (`forge install` with a tag/commit; lock OpenZeppelin version). Re-audit on bumps.
- Verify deployed bytecode matches source on the explorer (`forge verify-contract` / `--verify`).

## Post-deploy checklist

- [ ] Source verified on the block explorer.
- [ ] Ownership/admin transferred to a **multisig** (Safe), not an EOA, for anything controlling funds.
- [ ] Timelock on privileged upgrades/parameter changes.
- [ ] Monitoring/alerting on critical events (large withdrawals, ownership changes, pause).
- [ ] Emergency runbook: pause + emergency-withdraw path tested on testnet.
- [ ] Deploy key rotated/retired if it ever touched a less-trusted machine.

## References
- Foundry deploying guide: https://getfoundry.sh/guides/deploying
- `cast wallet`: https://getfoundry.sh/cast/reference/wallet
- OpenZeppelin Contracts: https://docs.openzeppelin.com/contracts
- Safe (multisig): https://safe.global/
- revoke.cash (approval management): https://revoke.cash/
