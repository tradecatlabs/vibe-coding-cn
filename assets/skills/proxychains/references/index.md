# Proxychains 参考文档索引

## 核心文档

- **proxychains.conf** - 完整配置文件示例（针对 127.0.0.1:9910 优化）
- **quick-reference.md** - 快速命令参考和常见场景
- **troubleshooting.md** - 故障排除指南
- **setup-guide.md** - 安装和初始配置指南

## 使用场景

本技能包专为以下场景设计：

1. **自动代理重试** - Claude 检测到网络错误时自动使用代理
2. **已知慢速源** - 访问 GitHub、PyPI、npm 等自动走代理
3. **一键配置** - 快速配置代理指向 127.0.0.1:9910

## 快速开始

### 1. 安装 proxychains4

```bash
# Ubuntu/Debian
sudo apt install proxychains4

# CentOS/RHEL
sudo yum install proxychains-ng

# macOS
brew install proxychains-ng
```

### 2. 配置代理（127.0.0.1:9910）

```bash
mkdir -p ~/.proxychains
cat > ~/.proxychains/proxychains.conf << 'EOF'
strict_chain
proxy_dns
remote_dns_subnet 224
tcp_read_time_out 15000
tcp_connect_time_out 8000

[ProxyList]
http 127.0.0.1 9910
EOF
```

### 3. 测试代理

```bash
# 测试配置
proxychains4 curl https://ipinfo.io/json

# 应该显示代理服务器的 IP 地址
```

## 核心概念

**Proxychains 工作原理：**
- 通过 LD_PRELOAD 拦截程序的 socket 调用
- 将所有 TCP 连接重定向到代理服务器
- 支持 HTTP、SOCKS4、SOCKS5 代理协议
- 透明代理，应用程序无需修改

**适用范围：**
- ✅ 动态链接的程序
- ✅ TCP 连接
- ✅ HTTP/HTTPS 请求
- ❌ 静态链接程序
- ❌ UDP 连接

## 参考文档说明

### proxychains.conf
完整的配置文件模板，已针对 127.0.0.1:9910 优化，包含：
- 超时时间设置
- DNS 代理配置
- 代理链模式选择

### quick-reference.md
快速命令参考，包含：
- 常用命令模式
- 不同工具的代理使用方法
- 环境变量配置

### troubleshooting.md
故障排除指南，包含：
- 常见错误和解决方案
- 代理服务检查方法
- 配置验证步骤

### setup-guide.md
详细的安装和配置指南，包含：
- 不同系统的安装方法
- 配置文件详解
- 高级配置选项

---

**使用提示：** Claude 会自动使用这些参考文档中的信息来帮助解决网络问题。
