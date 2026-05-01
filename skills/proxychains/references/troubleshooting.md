# Proxychains 故障排除指南

## 常见错误及解决方案

### 错误 1: "proxychains: command not found"

**症状：**
```bash
$ proxychains4 curl https://github.com
bash: proxychains4: command not found
```

**原因：** proxychains 未安装

**解决方案：**

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install proxychains4

# CentOS/RHEL
sudo yum install epel-release
sudo yum install proxychains-ng

# Fedora
sudo dnf install proxychains-ng

# macOS
brew install proxychains-ng

# Arch Linux
sudo pacman -S proxychains-ng

# 验证安装
proxychains4 --version
```

---

### 错误 2: "can't read configuration file"

**症状：**
```bash
$ proxychains4 curl https://github.com
[proxychains] can't read configuration file /etc/proxychains.conf
```

**原因：** 配置文件不存在或路径错误

**解决方案：**

```bash
# 方法 1: 创建用户级配置文件
mkdir -p ~/.proxychains
cat > ~/.proxychains/proxychains.conf << 'EOF'
strict_chain
proxy_dns
[ProxyList]
http 127.0.0.1 9910
EOF

# 方法 2: 复制系统配置模板
sudo cp /usr/share/doc/proxychains*/proxychains.conf /etc/
# 或
sudo cp /usr/local/etc/proxychains.conf /etc/

# 方法 3: 指定配置文件路径
proxychains4 -f /path/to/proxychains.conf curl https://github.com

# 验证配置文件
cat ~/.proxychains/proxychains.conf
```

---

### 错误 3: "timeout"

**症状：**
```bash
$ proxychains4 curl https://github.com
[proxychains] Strict chain ... 127.0.0.1:9910 ... github.com:443 ... timeout
curl: (28) Connection timed out after 10000 milliseconds
```

**原因：** 代理服务未运行、端口错误或防火墙阻止

**解决方案：**

```bash
# 1. 检查代理服务是否运行
netstat -tunlp | grep 9910
ss -tunlp | grep 9910
lsof -i :9910

# 2. 测试代理服务直接连接
curl -x http://127.0.0.1:9910 https://www.google.com

# 3. 检查防火墙规则
sudo iptables -L -n | grep 9910
sudo ufw status

# 4. 确认代理配置正确
cat ~/.proxychains/proxychains.conf | grep -A 2 "\[ProxyList\]"

# 5. 增加超时时间（编辑配置文件）
tcp_connect_time_out 15000
tcp_read_time_out 30000

# 6. 如果代理服务未运行，启动代理服务
# （根据你的代理软件，例如：）
# v2ray、clash、shadowsocks 等
```

---

### 错误 4: "connection refused"

**症状：**
```bash
$ proxychains4 curl https://github.com
[proxychains] Strict chain ... 127.0.0.1:9910 ... connect refused
curl: (7) Failed to connect to 127.0.0.1 port 9910: Connection refused
```

**原因：** 代理端口未监听或代理服务未启动

**解决方案：**

```bash
# 1. 确认代理服务状态
# 检查你的代理软件是否运行（v2ray、clash、shadowsocks 等）

# 2. 验证代理端口
netstat -tunlp | grep 9910
# 如果没有输出，说明端口未监听

# 3. 检查代理软件配置
# 确认代理软件监听的端口是 9910

# 4. 尝试其他可能的代理端口
# 常见端口：1080 (SOCKS), 7890 (HTTP), 8080 (HTTP)
netstat -tunlp | grep -E '1080|7890|8080|9910'

# 5. 更新 proxychains 配置为正确端口
nano ~/.proxychains/proxychains.conf
# 修改 [ProxyList] 部分：
# http 127.0.0.1 [正确的端口]

# 6. 重启代理服务
# 根据你的代理软件执行相应命令
```

---

### 错误 5: "DNS request timed out"

**症状：**
```bash
$ proxychains4 curl https://github.com
[proxychains] DNS request timed out
curl: (6) Could not resolve host: github.com
```

**原因：** DNS 解析失败或 proxy_dns 配置问题

**解决方案：**

```bash
# 1. 检查配置文件中的 proxy_dns 设置
cat ~/.proxychains/proxychains.conf | grep proxy_dns
# 应该有：proxy_dns

# 2. 如果没有，添加 proxy_dns
nano ~/.proxychains/proxychains.conf
# 添加：
proxy_dns
remote_dns_subnet 224

# 3. 测试 DNS 解析
proxychains4 nslookup github.com
proxychains4 dig github.com

# 4. 使用自定义 DNS 服务器
export PROXY_DNS_SERVER=8.8.8.8
proxychains4 curl https://github.com

# 5. 或者使用 IP 地址直接访问（跳过 DNS）
proxychains4 curl https://140.82.114.4  # GitHub IP

# 6. 检查 /etc/resolv.conf
cat /etc/resolv.conf
# 确保有有效的 nameserver
```

---

### 错误 6: "Program not supported"

**症状：**
```bash
$ proxychains4 ./static-binary
[proxychains] Program not supported
```

**原因：** 程序是静态链接的，proxychains 只支持动态链接程序

**解决方案：**

```bash
# 1. 检查程序是否静态链接
ldd ./program
# 如果输出 "not a dynamic executable"，则为静态链接

# 2. 对于静态链接程序，需要其他方案：
# - 使用系统级代理（iptables 转发）
# - 使用 VPN
# - 使用容器级代理

# 3. Go 程序示例（通常是静态链接）
# 设置环境变量而不是用 proxychains
export HTTP_PROXY=http://127.0.0.1:9910
export HTTPS_PROXY=http://127.0.0.1:9910
./go-program

# 4. 对于可重新编译的程序
# 编译为动态链接版本
```

---

### 错误 7: "strict chain ... all proxy servers are down"

**症状：**
```bash
$ proxychains4 curl https://github.com
[proxychains] strict chain ... all proxy servers are down!
curl: (97) Failure in receiving network data
```

**原因：** strict_chain 模式下所有代理都不可用

**解决方案：**

```bash
# 1. 测试代理列表中的每个代理
cat ~/.proxychains/proxychains.conf | grep -A 10 "\[ProxyList\]"

# 逐个测试
curl -x http://127.0.0.1:9910 https://www.google.com
curl -x http://127.0.0.1:8080 https://www.google.com

# 2. 切换到 dynamic_chain 模式（自动跳过死代理）
nano ~/.proxychains/proxychains.conf
# 注释掉：#strict_chain
# 启用：dynamic_chain

# 3. 或者移除不可用的代理
nano ~/.proxychains/proxychains.conf
# 只保留可用的代理在 [ProxyList] 中

# 4. 重新测试
proxychains4 curl https://ipinfo.io/json
```

---

### 错误 8: "Permission denied"

**症状：**
```bash
$ proxychains4 curl https://github.com
[proxychains] Permission denied
```

**原因：** 配置文件或 proxychains 可执行文件权限问题

**解决方案：**

```bash
# 1. 检查配置文件权限
ls -la ~/.proxychains/proxychains.conf

# 2. 修复权限
chmod 644 ~/.proxychains/proxychains.conf

# 3. 检查目录权限
ls -la ~/.proxychains/

# 4. 修复目录权限
chmod 755 ~/.proxychains/

# 5. 检查 proxychains 可执行文件权限
ls -la $(which proxychains4)

# 6. 如果是系统级配置文件
sudo chmod 644 /etc/proxychains.conf
```

---

## 高级故障排除

### 调试模式

```bash
# 启用详细输出
# 编辑配置文件，注释掉 quiet_mode
nano ~/.proxychains/proxychains.conf
# 注释：#quiet_mode

# 使用 strace 跟踪系统调用
strace -e trace=network proxychains4 curl https://github.com

# 查看环境变量
env | grep -i proxy
```

### 日志分析

```bash
# proxychains 输出到文件
proxychains4 curl https://github.com 2>&1 | tee proxychains.log

# 分析连接过程
cat proxychains.log | grep -E 'chain|connect|timeout'
```

### 网络连通性测试

```bash
# 测试本地连接
ping 127.0.0.1
telnet 127.0.0.1 9910

# 测试外部连接（不通过代理）
curl https://ipinfo.io/json

# 测试外部连接（通过代理）
proxychains4 curl https://ipinfo.io/json

# 比较 IP 地址
# 不通过代理的 IP 应该是本机 IP
# 通过代理的 IP 应该是代理服务器 IP
```

### 配置验证

```bash
# 验证配置文件语法
proxychains4 -f ~/.proxychains/proxychains.conf true

# 测试不同的代理类型
# HTTP
proxychains4 -f - curl https://github.com << 'EOF'
strict_chain
[ProxyList]
http 127.0.0.1 9910
EOF

# SOCKS5
proxychains4 -f - curl https://github.com << 'EOF'
strict_chain
[ProxyList]
socks5 127.0.0.1 1080
EOF
```

---

## 性能问题

### 连接缓慢

**症状：** 命令执行很慢

**解决方案：**

```bash
# 1. 减少超时时间
nano ~/.proxychains/proxychains.conf
tcp_connect_time_out 5000
tcp_read_time_out 10000

# 2. 启用 quiet_mode 减少输出
quiet_mode

# 3. 使用更快的代理服务器

# 4. 测试代理延迟
time proxychains4 curl -I https://github.com

# 5. 使用 dynamic_chain 跳过慢速代理
dynamic_chain
```

### 频繁断开

**症状：** 连接经常中断

**解决方案：**

```bash
# 1. 增加超时时间
tcp_read_time_out 30000

# 2. 检查代理服务器稳定性
# 持续 ping 测试
ping -c 100 127.0.0.1

# 3. 更换代理服务器

# 4. 检查网络稳定性
mtr 8.8.8.8
```

---

## 检查清单

使用此清单快速诊断问题：

```bash
# ✅ 检查 1: proxychains 已安装
which proxychains4

# ✅ 检查 2: 配置文件存在
ls -la ~/.proxychains/proxychains.conf

# ✅ 检查 3: 配置文件格式正确
cat ~/.proxychains/proxychains.conf

# ✅ 检查 4: 代理服务运行中
netstat -tunlp | grep 9910

# ✅ 检查 5: 代理可直接访问
curl -x http://127.0.0.1:9910 https://www.google.com

# ✅ 检查 6: DNS 解析正常
proxychains4 nslookup github.com

# ✅ 检查 7: proxychains 连接正常
proxychains4 curl https://ipinfo.io/json

# ✅ 检查 8: IP 地址已变更
# 对比直接访问和代理访问的 IP 应该不同
curl https://ipinfo.io/json
proxychains4 curl https://ipinfo.io/json
```

---

## 获取帮助

如果以上方法都无法解决问题：

```bash
# 查看帮助文档
man proxychains4
proxychains4 --help

# 查看系统日志
sudo journalctl -xe | grep proxy
dmesg | grep -i proxy

# 检查 proxychains 版本
proxychains4 --version

# GitHub Issues
# https://github.com/haad/proxychains/issues
```

---

**提示：** 大多数问题都是由于代理服务未运行或端口配置错误造成的。首先确保代理服务正常运行。
