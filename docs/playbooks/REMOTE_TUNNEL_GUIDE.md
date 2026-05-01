# VS Code Remote Tunnel（WSL 侧）快速指南

面向场景：在 WSL 内开通 VS Code Tunnel，供 Mac/任意客户端通过 Remote - Tunnels 或 vscode.dev 访问。

## 前置条件
- WSL 已开启 systemd（`/etc/wsl.conf` 有 `[boot] systemd=true`，然后 `wsl --shutdown` 重进）。
- 网络可直连或通过本机代理 127.0.0.1:9910（本指南示例端口）。

## 安装 VS Code CLI（WSL 内）
```bash
sudo apt-get update
sudo apt-get install -y wget gpg apt-transport-https
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | sudo tee /etc/apt/keyrings/packages.microsoft.gpg >/dev/null
echo "deb [arch=amd64,arm64 signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" | sudo tee /etc/apt/sources.list.d/vscode.list
sudo apt-get update
sudo apt-get install -y code
which code   # 应为 /usr/local/bin/code 或 /usr/bin/code
```

## 一次性登录
```bash
/usr/local/bin/code tunnel user login
# 浏览器打开提示的 device code 完成 GitHub 授权
```

## 配置代理（可选，示例 127.0.0.1:9910）
创建 drop-in：
```bash
mkdir -p ~/.config/systemd/user/code-tunnel.service.d
cat > ~/.config/systemd/user/code-tunnel.service.d/proxy.conf <<'EOF'
[Service]
Environment=HTTP_PROXY=http://127.0.0.1:9910
Environment=HTTPS_PROXY=http://127.0.0.1:9910
Environment=NO_PROXY=localhost,127.0.0.1,::1
EOF
systemctl --user daemon-reload
```

## 安装并开机自启隧道服务
```bash
/usr/local/bin/code tunnel service install --accept-server-license-terms --name wsl-lenovo
systemctl --user enable code-tunnel.service
systemctl --user restart code-tunnel.service
```

## 验证
```bash
/usr/local/bin/code tunnel status        # tunnel: Connected 且 service_installed:true
systemctl --user status code-tunnel.service --no-pager
```

## 客户端连接
- VS Code 桌面：安装 “Remote - Tunnels”，用同一 GitHub 账号登录，Remote Explorer 选择 `wsl-lenovo`。
- 纯浏览器：访问 `https://vscode.dev/tunnel/wsl-lenovo`，同账号登录即可。

## 日志与维护
```bash
/usr/local/bin/code tunnel service log --log info   # 查看服务日志
/usr/local/bin/code tunnel rename <new-name>        # 重命名隧道
/usr/local/bin/code tunnel kill                     # 停止当前隧道进程
/usr/local/bin/code tunnel service uninstall        # 移除自启服务
```

## 常见故障排查
- 仍显示 Disconnected：确认代理可用，`curl https://api.github.com` 能通；或暂时 `unset HTTP_PROXY HTTPS_PROXY` 再试。
- 路径错误 (`\\wsl.localhost\\...`)：不要在 `terminal.integrated.cwd` 写 UNC，删除该项或用 POSIX 路径。
- 未启用 systemd：检查 `/etc/wsl.conf`，修改后 `wsl --shutdown` 重新进入。
