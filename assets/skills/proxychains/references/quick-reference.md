# Proxychains 快速参考

## 基本语法

```bash
proxychains4 [command] [arguments]
```

## 常用命令模式

### Git 操作

```bash
# 克隆仓库
proxychains4 git clone https://github.com/user/repo.git

# 拉取更新
proxychains4 git pull

# 推送代码
proxychains4 git push origin main

# 添加子模块
proxychains4 git submodule update --init --recursive
```

### Python/pip

```bash
# 安装包
proxychains4 pip install requests
proxychains4 pip install -r requirements.txt

# 升级包
proxychains4 pip install --upgrade package-name

# 搜索包
proxychains4 pip search package-name

# 使用国内镜像 + 代理（双保险）
proxychains4 pip install -i https://pypi.tuna.tsinghua.edu.cn/simple package-name
```

### Node.js/npm/yarn

```bash
# npm 安装
proxychains4 npm install package-name
proxychains4 npm install -g package-name
proxychains4 npm install

# yarn 安装
proxychains4 yarn add package-name
proxychains4 yarn install

# 清理缓存后安装
proxychains4 npm cache clean --force
proxychains4 npm install
```

### curl/wget

```bash
# curl 下载
proxychains4 curl -O https://example.com/file.tar.gz
proxychains4 curl -L https://example.com/redirect

# wget 下载
proxychains4 wget https://example.com/file.tar.gz
proxychains4 wget -c https://example.com/large-file.iso

# API 请求
proxychains4 curl -X POST https://api.example.com/endpoint
```

### Docker

```bash
# 拉取镜像
proxychains4 docker pull ubuntu:latest
proxychains4 docker pull nginx:alpine

# 构建镜像（如果需要下载基础镜像）
proxychains4 docker build -t myapp:latest .

# 推送镜像
proxychains4 docker push myregistry.com/myapp:latest
```

### SSH/SCP

```bash
# SSH 连接
proxychains4 ssh user@remote-host

# SCP 文件传输
proxychains4 scp file.txt user@remote-host:/path/
proxychains4 scp -r folder/ user@remote-host:/path/

# rsync 同步
proxychains4 rsync -avz folder/ user@remote-host:/path/
```

### 其他工具

```bash
# telnet
proxychains4 telnet example.com 80

# nc (netcat)
proxychains4 nc example.com 80

# ftp
proxychains4 ftp ftp.example.com

# svn
proxychains4 svn checkout https://example.com/svn/repo

# mercurial (hg)
proxychains4 hg clone https://example.com/hg/repo
```

## 配置文件选项

### 指定配置文件

```bash
# 使用自定义配置文件
proxychains4 -f /path/to/proxychains.conf curl https://example.com

# 使用当前目录配置
proxychains4 -f ./proxychains.conf command
```

### 环境变量方式

```bash
# 设置代理主机和端口（SOCKS5）
export PROXYCHAINS_SOCKS5_HOST=127.0.0.1
export PROXYCHAINS_SOCKS5_PORT=9910
proxychains4 curl https://example.com

# 指定配置文件路径
export PROXYCHAINS_CONF_FILE=~/.proxychains/custom.conf
proxychains4 command

# 自定义 DNS 服务器
export PROXY_DNS_SERVER=8.8.8.8
proxychains4 curl https://example.com
```

### 启动代理会话

```bash
# 在代理环境中启动 shell
proxychains4 bash
# 或
proxychains4 zsh

# 然后所有命令都会通过代理
git clone https://github.com/user/repo.git
pip install requests
npm install package-name

# 退出代理会话
exit
```

## 诊断和测试

### 测试代理连接

```bash
# 测试 HTTP 代理
proxychains4 curl https://ipinfo.io/json
proxychains4 curl https://ifconfig.me

# 测试特定网站
proxychains4 curl -I https://github.com
proxychains4 curl -I https://google.com

# 详细输出（调试）
proxychains4 -q curl -v https://example.com
```

### 检查代理服务

```bash
# 检查端口是否监听
netstat -tunlp | grep 9910
ss -tunlp | grep 9910
lsof -i :9910

# 测试代理直接连接（不用 proxychains）
curl -x http://127.0.0.1:9910 https://www.google.com
curl -x socks5://127.0.0.1:1080 https://www.google.com

# 测试代理认证
curl -x http://username:password@127.0.0.1:9910 https://www.google.com
```

### DNS 解析测试

```bash
# 通过代理解析 DNS
proxychains4 nslookup google.com
proxychains4 dig google.com

# 使用 proxyresolv 工具（proxychains 自带）
proxyresolv google.com
proxyresolv github.com
```

## 快速配置生成

### 单行命令创建配置

```bash
# 创建用户级配置（HTTP 代理 127.0.0.1:9910）
mkdir -p ~/.proxychains && cat > ~/.proxychains/proxychains.conf << 'EOF'
strict_chain
proxy_dns
remote_dns_subnet 224
tcp_read_time_out 15000
tcp_connect_time_out 8000
[ProxyList]
http 127.0.0.1 9910
EOF

# 创建 SOCKS5 配置
mkdir -p ~/.proxychains && cat > ~/.proxychains/proxychains.conf << 'EOF'
strict_chain
proxy_dns
[ProxyList]
socks5 127.0.0.1 1080
EOF
```

### 临时配置（当前目录）

```bash
# 在当前目录创建临时配置
cat > proxychains.conf << 'EOF'
strict_chain
proxy_dns
[ProxyList]
http 127.0.0.1 9910
EOF

# 使用临时配置
proxychains4 -f ./proxychains.conf curl https://github.com
```

## 性能优化

### 减少延迟

```bash
# 配置文件中调整超时
tcp_connect_time_out 5000  # 5秒
tcp_read_time_out 10000    # 10秒

# 使用 quiet_mode 减少输出
quiet_mode
```

### 并行下载

```bash
# aria2 多线程下载
proxychains4 aria2c -x 16 https://example.com/large-file.iso

# wget 多连接下载
proxychains4 wget --limit-rate=10m https://example.com/file.tar.gz
```

## 常见组合场景

### 场景 1: Python 项目依赖安装

```bash
# 克隆项目
proxychains4 git clone https://github.com/user/project.git
cd project

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
proxychains4 pip install -r requirements.txt
```

### 场景 2: Node.js 项目初始化

```bash
# 克隆项目
proxychains4 git clone https://github.com/user/project.git
cd project

# 安装依赖
proxychains4 npm install
# 或
proxychains4 yarn install

# 运行项目（如果需要下载额外资源）
proxychains4 npm start
```

### 场景 3: Docker 镜像构建

```bash
# 拉取基础镜像
proxychains4 docker pull node:18-alpine

# 构建镜像（Dockerfile 中有 FROM 远程镜像）
proxychains4 docker build -t myapp:latest .

# 推送到仓库
proxychains4 docker push myregistry.com/myapp:latest
```

### 场景 4: 系统软件更新

```bash
# Ubuntu/Debian
proxychains4 sudo apt update
proxychains4 sudo apt upgrade

# CentOS/RHEL
proxychains4 sudo yum update

# Arch Linux
proxychains4 sudo pacman -Syu
```

## 别名设置（可选）

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
alias pc='proxychains4'
alias pcgit='proxychains4 git'
alias pcpip='proxychains4 pip'
alias pcnpm='proxychains4 npm'
alias pccurl='proxychains4 curl'
alias pcwget='proxychains4 wget'

# 使用别名
pc curl https://github.com
pcgit clone https://github.com/user/repo.git
pcpip install requests
```

## 故障排除快速检查清单

```bash
# 1. 检查 proxychains 是否安装
which proxychains4

# 2. 检查配置文件是否存在
ls -la ~/.proxychains/proxychains.conf
cat ~/.proxychains/proxychains.conf

# 3. 检查代理服务是否运行
netstat -tunlp | grep 9910

# 4. 测试代理直接连接
curl -x http://127.0.0.1:9910 https://www.google.com

# 5. 测试 proxychains 连接
proxychains4 curl https://ipinfo.io/json

# 6. 查看详细错误信息
proxychains4 curl -v https://example.com
```

---

**提示：** 将常用命令保存为 shell 脚本或别名，可以提高效率。
