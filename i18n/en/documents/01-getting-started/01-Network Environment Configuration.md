# Network Environment Configuration

> Vibe Coding Prerequisite: Ensure normal access to services like GitHub, Google, and Claude.

---

## Method One: AI-Guided Configuration (Recommended)

Copy the following prompt and paste it into any AI chat box (ChatGPT, Claude, Gemini web version, etc.):

```
You are a patient network environment configuration assistant. I need to configure a network proxy to access foreign services such as GitHub, Google, and Claude.

My situation:
- Operating system: [Please tell me if you are using Windows/macOS/Linux/Android]
- I already have a proxy service subscription link (airport subscription)

Please guide me through configuring the network proxy using the FlClash client:
1. How to download and install FlClash (GitHub: https://github.com/chen08209/FlClash/releases)
2. How to import my subscription link
3. How to enable TUN mode (virtual network card) to achieve global proxy
4. How to enable system proxy
5. How to verify if the configuration is successful

Requirements:
- Each step should be explained in detail, with illustrations describing button locations.
- If I encounter problems, help me analyze the cause and provide solutions.
- After completing each step, ask me if it was successful before proceeding to the next.

Let's start now by asking me what operating system I am using.
```

---

## Method Two: Manual Configuration

### You will need

1.  **Network Service Subscription** - A provider of proxy nodes
2.  **FlClash** - A cross-platform network configuration client

### Step One: Purchase Network Service

Visit the service provider: https://xn--9kqz23b19z.com/#/register?code=35BcnKzl

-   Register an account
-   Select a plan (starting from about 6 RMB/month)
-   After payment, find the **subscription link** in the user panel and copy it for later use.

### Step Two: Download FlClash

GitHub Download: https://github.com/chen08209/FlClash/releases

Choose according to your system:
-   Windows: `FlClash-x.x.x-windows-setup.exe`
-   macOS: `FlClash-x.x.x-macos.dmg`
-   Linux: `FlClash-x.x.x-linux-amd64.AppImage`
-   Android: `FlClash-x.x.x-android.apk`

### Step Three: Import Subscription

1.  Open FlClash
2.  Click **Configuration** → **Add**
3.  Select **URL Import**
4.  Paste the subscription link copied in step one
5.  Click confirm and wait for nodes to load

### Step Four: Enable Proxy

Set the following three items in order:

| Setting           | Operation                         |
|:------------------|:----------------------------------|
| **Virtual NIC (TUN)** | Enable - Achieve global traffic proxy |
| **System Proxy**  | Enable - Allow system applications to use the proxy |
| **Proxy Mode**    | Select **Global Mode**            |

After setting up, the FlClash main interface should show "Connected".

### Verification

```bash
# Test Google connectivity
curl -I https://www.google.com

# Test GitHub connectivity
curl -I https://github.com
```

Returning `HTTP/2 200` indicates successful configuration.

---

## Common Issues

**Q: Nodes cannot connect?**
A: Try switching to another node, or check if the subscription has expired.

**Q: Some applications don't use the proxy?**
A: Ensure TUN mode (virtual NIC) is enabled.

**Q: Want the terminal to also use the proxy?**
A: The terminal automatically uses the proxy when TUN mode is enabled; or manually set:
```bash
export https_proxy=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890
```

---

## Next Steps

After network configuration is complete, continue reading [02-Development Environment Setup](./02-Development%20Environment%20Setup.md).
