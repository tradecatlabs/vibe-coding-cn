#!/bin/bash
# Proxychains 快速配置脚本
# 自动配置代理指向 127.0.0.1:9910

set -e

echo "=========================================="
echo "Proxychains 快速配置脚本"
echo "=========================================="
echo

# 检查 proxychains4 是否安装
if ! command -v proxychains4 &> /dev/null; then
    echo "❌ proxychains4 未安装"
    echo
    echo "请先安装 proxychains4："
    echo
    echo "  Ubuntu/Debian:"
    echo "    sudo apt install proxychains4"
    echo
    echo "  CentOS/RHEL:"
    echo "    sudo yum install epel-release"
    echo "    sudo yum install proxychains-ng"
    echo
    echo "  macOS:"
    echo "    brew install proxychains-ng"
    echo
    exit 1
fi

echo "✅ proxychains4 已安装"
echo

# 创建配置目录
echo "📁 创建配置目录..."
mkdir -p ~/.proxychains

# 创建配置文件
echo "📝 创建配置文件..."
cat > ~/.proxychains/proxychains.conf << 'EOF'
# Proxychains 配置文件
# 代理地址：127.0.0.1:9910

# 代理链模式（严格按顺序使用所有代理）
strict_chain

# 代理 DNS 请求（避免 DNS 泄漏）
proxy_dns

# DNS 设置
remote_dns_subnet 224

# 超时设置（毫秒）
tcp_read_time_out 15000
tcp_connect_time_out 8000

# 代理列表
[ProxyList]
# HTTP 代理：127.0.0.1:9910
http 127.0.0.1 9910

# 备用代理（取消注释以启用）
#http 127.0.0.1 8080
#socks5 127.0.0.1 1080
EOF

# 设置权限
chmod 644 ~/.proxychains/proxychains.conf

echo "✅ 配置文件已创建: ~/.proxychains/proxychains.conf"
echo

# 测试代理服务
echo "🔍 检查代理服务..."
if curl -s -x http://127.0.0.1:9910 --connect-timeout 3 https://www.google.com > /dev/null 2>&1; then
    echo "✅ 代理服务 127.0.0.1:9910 可用"
    echo

    # 测试 proxychains
    echo "🧪 测试 proxychains..."
    if proxychains4 curl -s --connect-timeout 5 https://ipinfo.io/json > /dev/null 2>&1; then
        echo "✅ Proxychains 配置成功！"
        echo
        echo "🎉 配置完成！可以开始使用了。"
    else
        echo "⚠️  Proxychains 测试失败"
        echo "   但配置文件已创建，请检查代理服务是否正常"
    fi
else
    echo "⚠️  代理服务 127.0.0.1:9910 无法连接"
    echo
    echo "请检查："
    echo "  1. 代理服务是否运行"
    echo "  2. 代理端口是否正确（127.0.0.1:9910）"
    echo "  3. 防火墙设置"
    echo
    echo "检查代理端口："
    echo "  netstat -tunlp | grep 9910"
    echo "  ss -tunlp | grep 9910"
    echo
    echo "配置文件已创建，代理服务就绪后即可使用。"
fi

echo
echo "=========================================="
echo "使用方法："
echo "=========================================="
echo
echo "  proxychains4 curl https://github.com"
echo "  proxychains4 git clone https://github.com/user/repo.git"
echo "  proxychains4 pip install package-name"
echo "  proxychains4 npm install package-name"
echo
echo "配置文件位置："
echo "  ~/.proxychains/proxychains.conf"
echo
echo "查看配置："
echo "  cat ~/.proxychains/proxychains.conf"
echo
echo "修改代理地址："
echo "  nano ~/.proxychains/proxychains.conf"
echo "=========================================="
