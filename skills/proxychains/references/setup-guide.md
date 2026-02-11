# Proxychains 安装和配置指南

## 安装 Proxychains

### Linux 系统

#### Ubuntu/Debian

```bash
# 更新包列表
sudo apt update

# 安装 proxychains4
sudo apt install proxychains4

# 验证安装
proxychains4 --version
```

#### CentOS/RHEL 7/8

```bash
# 安装 EPEL 仓库
sudo yum install epel-release

# 安装 proxychains-ng
sudo yum install proxychains-ng

# 验证安装
proxychains4 --version
```

#### Fedora

```bash
# 安装 proxychains-ng
sudo dnf install proxychains-ng

# 验证安装
proxychains4 --version
```

#### Arch Linux

```bash
# 安装 proxychains-ng
sudo pacman -S proxychains-ng

# 验证安装
proxychains4 --version
```

#### 从源码编译（通用方法）

```bash
# 安装依赖
sudo apt install build-essential git  # Debian/Ubuntu
# 或
sudo yum install gcc git make  # CentOS/RHEL

# 克隆仓库
git clone https://github.com/haad/proxychains.git
cd proxychains

# 编译安装
./configure --prefix=/usr --sysconfdir=/etc
make
sudo make install
sudo make install-config  # 安装默认配置文件

# 验证安装
proxychains4 --version
```

### macOS

```bash
# 使用 Homebrew 安装
brew install proxychains-ng

# 验证安装
proxychains4 --version
```

### WSL (Windows Subsystem for Linux)

```bash
# 在 WSL 中安装（使用 Ubuntu 示例）
sudo apt update
sudo apt install proxychains4

# 验证安装
proxychains4 --version
```

---

## 基础配置

### 配置文件位置

Proxychains 按以下顺序查找配置文件：

1. `${PROXYCHAINS_CONF_FILE}` 环境变量指定的路径
2. 命令行 `-f` 参数指定的路径
3. `./proxychains.conf` (当前目录)
4. `~/.proxychains/proxychains.conf` (用户主目录) **推荐**
5. `/etc/proxychains.conf` (系统级)

### 创建用户级配置（推荐）

```bash
# 创建配置目录
mkdir -p ~/.proxychains

# 创建配置文件（针对 127.0.0.1:9910）
cat > ~/.proxychains/proxychains.conf << 'EOF'
# Proxychains 配置文件
# 代理地址：127.0.0.1:9910

# 代理链模式
strict_chain

# 代理 DNS 请求
proxy_dns

# DNS 设置
remote_dns_subnet 224

# 超时设置（毫秒）
tcp_read_time_out 15000
tcp_connect_time_out 8000

# 代理列表
[ProxyList]
http 127.0.0.1 9910
EOF

# 设置权限
chmod 644 ~/.proxychains/proxychains.conf
```

### 创建系统级配置（可选）

```bash
# 需要 root 权限
sudo cat > /etc/proxychains.conf << 'EOF'
strict_chain
proxy_dns
remote_dns_subnet 224
tcp_read_time_out 15000
tcp_connect_time_out 8000

[ProxyList]
http 127.0.0.1 9910
EOF

# 设置权限
sudo chmod 644 /etc/proxychains.conf
```

---

## 配置详解

### 代理链模式

在配置文件中只能选择一种模式：

#### strict_chain（严格链，推荐）

```conf
# 严格按顺序使用所有代理
# 所有代理必须在线，任何一个失败则整个链失败
strict_chain
```

**适用场景：**
- 只有一个代理服务器
- 需要确保所有代理都被使用
- 对安全性要求高

#### dynamic_chain（动态链）

```conf
# 自动跳过离线代理
# 至少需要一个可用代理
dynamic_chain
```

**适用场景：**
- 有多个代理服务器
- 某些代理可能不稳定
- 需要自动故障转移

#### random_chain（随机链）

```conf
# 从列表中随机选择代理
random_chain
chain_len = 2  # 随机链长度（可选）
```

**适用场景：**
- 需要隐藏流量模式
- 有多个代理可用
- 对匿名性要求高

### DNS 设置

```conf
# 通过代理服务器解析 DNS
proxy_dns

# DNS 解析使用的虚拟子网（1-255）
remote_dns_subnet 224

# 可选：自定义 DNS 服务器（通过环境变量）
# export PROXY_DNS_SERVER=8.8.8.8
```

### 超时设置

```conf
# TCP 读取超时（毫秒）
tcp_read_time_out 15000  # 15秒

# TCP 连接超时（毫秒）
tcp_connect_time_out 8000  # 8秒
```

**调优建议：**
- 慢速网络：增加到 30000 和 15000
- 快速网络：减少到 10000 和 5000
- 本地代理：可以设置为 5000 和 3000

### 日志设置

```conf
# 静默模式（不输出代理链信息）
quiet_mode
```

**注意：** 调试时应注释掉此选项以查看详细输出。

---

## 代理列表配置

### 基本格式

```conf
[ProxyList]
# 格式：type host port [username password]
```

### HTTP 代理

```conf
# 不需要认证
http 127.0.0.1 9910

# 需要认证
http 127.0.0.1 8080 username password
```

### SOCKS4 代理

```conf
# 不需要认证
socks4 127.0.0.1 1080

# SOCKS4 不支持用户认证
```

### SOCKS5 代理

```conf
# 不需要认证
socks5 127.0.0.1 1080

# 需要认证
socks5 127.0.0.1 1080 username password
```

### 多代理配置

```conf
[ProxyList]
# 主代理
http 127.0.0.1 9910

# 备用代理（strict_chain 模式下会按顺序使用）
# 取消注释以启用
#http 127.0.0.1 8080
#socks5 127.0.0.1 1080
```

### 代理链示例

```conf
# 多级代理（流量经过多个代理）
strict_chain

[ProxyList]
http 127.0.0.1 9910
socks5 proxy2.example.com 1080
http proxy3.example.com 8080
```

---

## 高级配置

### 使用环境变量

```bash
# SOCKS5 代理（简化配置）
export PROXYCHAINS_SOCKS5_HOST=127.0.0.1
export PROXYCHAINS_SOCKS5_PORT=9910
proxychains4 curl https://github.com

# 指定配置文件
export PROXYCHAINS_CONF_FILE=~/.proxychains/custom.conf
proxychains4 command

# 自定义 DNS 服务器
export PROXY_DNS_SERVER=8.8.8.8
proxychains4 curl https://example.com
```

### 多配置文件管理

```bash
# 为不同场景创建不同配置文件
mkdir -p ~/.proxychains

# 国内代理配置
cat > ~/.proxychains/cn.conf << 'EOF'
strict_chain
proxy_dns
[ProxyList]
http 127.0.0.1 9910
EOF

# 国外代理配置
cat > ~/.proxychains/intl.conf << 'EOF'
strict_chain
proxy_dns
[ProxyList]
socks5 proxy.example.com 1080
EOF

# 使用特定配置
proxychains4 -f ~/.proxychains/cn.conf curl https://github.com
proxychains4 -f ~/.proxychains/intl.conf curl https://google.com
```

### 创建 Shell 别名

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
cat >> ~/.bashrc << 'EOF'

# Proxychains 别名
alias pc='proxychains4'
alias pccn='proxychains4 -f ~/.proxychains/cn.conf'
alias pcintl='proxychains4 -f ~/.proxychains/intl.conf'

# 常用命令别名
alias pcgit='proxychains4 git'
alias pcpip='proxychains4 pip'
alias pcnpm='proxychains4 npm'
alias pccurl='proxychains4 curl'
alias pcwget='proxychains4 wget'
alias pcssh='proxychains4 ssh'

EOF

# 重新加载配置
source ~/.bashrc
```

---

## 测试配置

### 基本连接测试

```bash
# 测试 proxychains 是否工作
proxychains4 curl https://ipinfo.io/json

# 应该显示代理服务器的 IP 地址，而不是本机 IP
```

### 对比测试

```bash
# 不使用代理的 IP
curl https://ipinfo.io/json

# 使用代理的 IP（应该不同）
proxychains4 curl https://ipinfo.io/json
```

### DNS 测试

```bash
# 测试 DNS 解析
proxychains4 nslookup google.com
proxychains4 dig github.com

# 使用 proxyresolv 工具
proxyresolv google.com
```

### 完整功能测试

```bash
# HTTP 请求
proxychains4 curl -I https://github.com

# HTTPS 请求
proxychains4 curl https://www.google.com

# SSH 连接（如果有测试服务器）
proxychains4 ssh user@example.com

# Git 克隆
proxychains4 git clone https://github.com/haad/proxychains.git /tmp/test-repo
```

---

## 与代理软件集成

### V2Ray

```bash
# 假设 V2Ray HTTP 代理端口是 10809
# 更新 proxychains 配置
cat > ~/.proxychains/proxychains.conf << 'EOF'
strict_chain
proxy_dns
[ProxyList]
http 127.0.0.1 10809
EOF
```

### Clash

```bash
# 假设 Clash HTTP 代理端口是 7890
# 更新 proxychains 配置
cat > ~/.proxychains/proxychains.conf << 'EOF'
strict_chain
proxy_dns
[ProxyList]
http 127.0.0.1 7890
EOF
```

### Shadowsocks

```bash
# 假设 Shadowsocks SOCKS5 端口是 1080
# 更新 proxychains 配置
cat > ~/.proxychains/proxychains.conf << 'EOF'
strict_chain
proxy_dns
[ProxyList]
socks5 127.0.0.1 1080
EOF
```

### SSH 动态端口转发

```bash
# 创建 SSH 动态端口转发（SOCKS5）
ssh -fN -D 1080 user@remote-server

# 配置 proxychains 使用 SSH 隧道
cat > ~/.proxychains/proxychains.conf << 'EOF'
strict_chain
proxy_dns
[ProxyList]
socks5 127.0.0.1 1080
EOF

# 使用
proxychains4 curl https://example.com
```

---

## 常见配置模板

### 模板 1: 单个 HTTP 代理（默认）

```conf
strict_chain
proxy_dns
remote_dns_subnet 224
tcp_read_time_out 15000
tcp_connect_time_out 8000

[ProxyList]
http 127.0.0.1 9910
```

### 模板 2: 单个 SOCKS5 代理

```conf
strict_chain
proxy_dns
remote_dns_subnet 224
tcp_read_time_out 15000
tcp_connect_time_out 8000

[ProxyList]
socks5 127.0.0.1 1080
```

### 模板 3: 多代理动态链（自动故障转移）

```conf
dynamic_chain
proxy_dns
remote_dns_subnet 224
tcp_read_time_out 15000
tcp_connect_time_out 8000

[ProxyList]
http 127.0.0.1 9910
http 127.0.0.1 8080
socks5 127.0.0.1 1080
```

### 模板 4: 低延迟优化

```conf
strict_chain
proxy_dns
remote_dns_subnet 224
tcp_read_time_out 10000
tcp_connect_time_out 5000
quiet_mode

[ProxyList]
http 127.0.0.1 9910
```

---

## 持久化配置

### 系统启动时自动使用代理

**不推荐全局使用，仅对特定用户/命令使用**

```bash
# 创建启动脚本（示例）
cat > ~/start-with-proxy.sh << 'EOF'
#!/bin/bash
proxychains4 bash
EOF

chmod +x ~/start-with-proxy.sh
```

### 为特定应用创建包装脚本

```bash
# Git 包装脚本
cat > ~/bin/git-proxy << 'EOF'
#!/bin/bash
proxychains4 git "$@"
EOF

chmod +x ~/bin/git-proxy

# 使用
git-proxy clone https://github.com/user/repo.git
```

---

## 故障排除配置

如果遇到问题，使用此配置进行调试：

```conf
# 调试配置
strict_chain
proxy_dns
remote_dns_subnet 224
tcp_read_time_out 30000
tcp_connect_time_out 15000
# 注释掉 quiet_mode 以查看详细输出

[ProxyList]
http 127.0.0.1 9910
```

---

## 安全建议

1. **配置文件权限**
   ```bash
   chmod 644 ~/.proxychains/proxychains.conf
   ```

2. **不要在配置文件中明文存储密码**
   - 如果必须使用认证，确保配置文件权限正确
   - 考虑使用环境变量

3. **定期更新 proxychains**
   ```bash
   sudo apt update && sudo apt upgrade proxychains4
   ```

4. **验证代理服务器可信度**
   - 只使用信任的代理服务器
   - 避免使用公共免费代理

---

## 下一步

配置完成后：

1. 阅读 `quick-reference.md` 了解常用命令
2. 阅读 `troubleshooting.md` 了解问题解决
3. 开始使用 proxychains4！

---

**提示：** 配置文件修改后立即生效，无需重启服务。
