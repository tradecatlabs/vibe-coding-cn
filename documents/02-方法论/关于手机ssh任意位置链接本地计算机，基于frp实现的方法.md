# 关于手机ssh任意位置链接本地计算机，基于frp实现的方法

不会弄怎么办？服务器和电脑都安装好codex（不会直接问gpt怎么安装，终端输入命令就行了），然后把文档粘贴到codex里面让他帮你配置好就行，实在不会弄，直接找我，telegram=https://t.me/desci0 x=https://x.com/123olp （ps：付费代搭）

# 📌 前置准备工作（Prerequisites）

在开始部署 FRP 服务端与客户端之前，请确保具备以下环境与工具。这些前置条件是保证 FRP 隧道正常工作所必需的。

## 1. 基础环境要求

### ✔ 一台可长期在线的 **AWS EC2 实例**

* 推荐系统：Ubuntu 20.04/22.04（本文以 Ubuntu 为例）
* 必须具备公网 IP（AWS 默认提供）
* 需要具备修改安全组规则的权限（开放 FRP 端口）

用途：作为 FRP 服务器端（frps），给 Windows 电脑提供固定访问入口。

## 2. 一台能够上网的 **Windows 电脑**

* Windows 10 或 Windows 11
* 需要具备普通用户权限（但部分配置需要管理员权限）
* 必须已安装 **OpenSSH Server**

用途：作为 FRP 客户端（frpc），无论连接什么网络，都可自动挂到 AWS 上。

## 3. 必需下载的软件 / 仓库

### ✔ FRP（Fast Reverse Proxy）

仓库地址（官方）：

```
https://github.com/fatedier/frp
```

本部署使用版本：

```
frp_0.58.1
```

下载页面：

```
https://github.com/fatedier/frp/releases
```

需要下载：

* Linux 版（用于 AWS）
* Windows 版（用于本地电脑）

## 4. 必须安装的软件

### ✔ Windows：OpenSSH Server + OpenSSH Client

安装路径：

```
设置 → 应用 → 可选功能 → 添加功能
```

用途：提供 SSH 登录能力，让 FRP 转发到 Windows 的 SSH。

## 5. 终端工具

### ✔ Termius（推荐）

* 用于从手机或电脑通过 SSH 连接你的 Windows
* 支持生成 SSH Key
* 支持管理多个主机

必须使用 Termius 生成 SSH 私钥（因为你启用了“仅密钥登录”）。

官方下载：

```
https://termius.com
```

## 6. 网络与端口要求

在 AWS 安全组中必须开放以下端口：

| 端口                             | 用途                    | 是否必须 |
| ------------------------------ | --------------------- | ---- |
| **FRP 控制端口**（如：1234 或 114514）  | frpc → frps 连接        | ✔ 必须 |
| **SSH 映射端口**（如：12345 或 114515） | Termius → Windows SSH | ✔ 必须 |

若使用 UFW（Ubuntu 防火墙），还需：

```
sudo ufw allow <FRP控制端口>/tcp
sudo ufw allow <SSH映射端口>/tcp
```

## 7. 公钥 / 私钥 准备（密钥登录必需）

你需要预先准备：

* Termius 生成的 SSH 私钥（本地）
* Termius 生成的 SSH 公钥（需放到 Windows 的 authorized_keys）

本部署已经禁用密码登录，因此 **私钥必须妥善保管，否则将无法登录 Windows**。

## 8. 基本 Linux 操作能力

需要了解以下基础命令（很简单）：

```
cd /path
nano / vim / notepad
chmod / chown
ps -ef | grep
ss -lnpt
nohup <cmd> &
tail -f
```

你文档中都已覆盖，不会有额外要求。

# 📌 前置条件总结（最终版）

```
必须具备：
- AWS EC2（Ubuntu，带公网 IP）
- Windows 电脑（安装 OpenSSH Server）
- Termius（用于 SSH + 生成密钥）
- FRP（下载 Linux + Windows 版本）
- AWS 安全组已开放 FRP 控制端口与 SSH 映射端口
- Termius 生成的 SSH 密钥对
```

只要满足以上前置准备，你的 FRP 隧道、SSH 密钥登录、跨网络远程访问电脑 100% 能正常运行。

如果你愿意，我还可以帮你：

* 把整个文档串成专业正式的一体化教程
* 为你的文档添加「适用范围、版本说明、架构概览图、流程图」
* 为 FRP 部署提供 systemd 服务模板
* 为 Windows 提供后台 frpc 自启脚本（更可靠）

需要的话告诉我！

# FRP 服务器端部署说明

本说明记录了当前 AWS EC2 (Ubuntu) 上的 FRP 服务端配置与操作方法，便于后续维护或重建。

## 基本信息
- 工作目录：`/home/ubuntu/.frp`
- FRP 版本：`frp_0.58.1_linux_amd64`
- 可执行文件：`/home/ubuntu/.frp/frp_0.58.1_linux_amd64/frps`
- 配置文件：`/home/ubuntu/.frp/frp_0.58.1_linux_amd64/frps.ini`
- 日志文件：`/home/ubuntu/.frp/frps.log`
- 启动脚本：`/home/ubuntu/.frp/start_frps.sh`
- 监听端口：
  - 控制端口 `bind_port = 1234`
  - SSH 映射端口 `12345`
- token：`123456`

## 安装步骤
1. 新建目录并下载 FRP：
   ```bash
   mkdir -p /home/ubuntu/.frp
   cd /home/ubuntu/.frp
   wget https://github.com/fatedier/frp/releases/download/v0.58.1/frp_0.58.1_linux_amd64.tar.gz
   tar -zxf frp_0.58.1_linux_amd64.tar.gz
   ```
2. 创建配置 `/home/ubuntu/.frp/frp_0.58.1_linux_amd64/frps.ini`：
   ```ini
   [common]
   bind_port = 1234
   token = 123456
   ```
3. 编写启动脚本 `/home/ubuntu/.frp/start_frps.sh`（已就绪）：
   ```bash
   #!/usr/bin/env bash
   set -euo pipefail
   BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
   FRP_DIR="$BASE_DIR/frp_0.58.1_linux_amd64"
   FRPS_BIN="$FRP_DIR/frps"
   CONFIG_FILE="$FRP_DIR/frps.ini"
   LOG_FILE="$BASE_DIR/frps.log"

   if ! [ -x "$FRPS_BIN" ]; then
     echo "frps binary not found at $FRPS_BIN" >&2
     exit 1
   fi
   if ! [ -f "$CONFIG_FILE" ]; then
     echo "Config not found at $CONFIG_FILE" >&2
     exit 1
   fi

   PIDS=$(pgrep -f "frps.*frps\\.ini" || true)
   if [ -n "$PIDS" ]; then
     echo "frps is running; restarting (pids: $PIDS)..."
     kill $PIDS
     sleep 1
   fi

   echo "Starting frps with $CONFIG_FILE (log: $LOG_FILE)"
   cd "$FRP_DIR"
   nohup "$FRPS_BIN" -c "$CONFIG_FILE" >"$LOG_FILE" 2>&1 &

   sleep 1
   PIDS=$(pgrep -f "frps.*frps\\.ini" || true)
   if [ -n "$PIDS" ]; then
     echo "frps started (pid: $PIDS)"
   else
     echo "frps failed to start; check $LOG_FILE" >&2
     exit 1
   fi
   ```

## 启动与停止
- 启动/重启：
  ```bash
  cd /home/ubuntu/.frp
  bash ./start_frps.sh
  ```
- 查看进程：`ps -ef | grep frps`
- 查看监听：`ss -lnpt | grep 1234`
- 查看日志：`tail -n 50 /home/ubuntu/.frp/frps.log`
- 停止（如需手动）：`pkill -f "frps.*frps.ini"`

## 安全组与防火墙
- AWS 安全组（sg-099756caee5666062）需开放入站 TCP 1234（FRP 控制）与 12345（SSH 映射）。
- 若使用 ufw，需执行：
  ```bash
  sudo ufw allow 1234/tcp
  sudo ufw allow 12345/tcp
  ```

## 远程客户端要求
- Windows `frpc.ini` 中 `server_addr` 指向该 EC2 公网 IP，`server_port=1234`，`remote_port=12345`，token 与服务器一致。
- Termius/SSH 客户端使用 `ssh lenovo@<AWS IP> -p 12345`，认证方式为密钥（Termius Keychain 生成的私钥）。

## 维护建议
- FRP 官方已提示 INI 格式未来会被弃用，后续升级建议改用 TOML/YAML。
- 可将 `start_frps.sh` 注册成 systemd 服务，确保实例重启后自动拉起。
- 定期检查 `frps.log` 是否有异常连接或错误，并确保 token 不泄露。

FRP Windows 客户端配置说明
================================
最后更新：2025-12-05
适用环境：Windows 10/11，用户 lenovo，本机已安装 OpenSSH Server。

一、目录与文件
- FRP 程序目录：C:\frp\
  - frpc.exe
  - frpc.ini（客户端配置）
  - start_frpc.bat（后台启动脚本）
- SSH 密钥：
  - 私钥：C:\Users\lenovo\.ssh\666
  - 公钥：C:\Users\lenovo\.ssh\666.pub
  - 管理员授权公钥：C:\ProgramData\ssh\666_keys

二、frpc.ini 内容（当前生效）
[common]
server_addr = 13.14.223.23
server_port = 1234
token = 123456

[ssh]
type = tcp
local_ip = 127.0.0.1
local_port = 22
remote_port = 12345

三、启动与自启
1) 手动前台验证（可选）
   PowerShell：
   cd C:\frp
   .\frpc.exe -c frpc.ini

2) 后台快捷启动
   双击 C:\frp\start_frpc.bat

3) 开机自启（简单方式）
   将 start_frpc.bat 复制到启动文件夹：
   C:\Users\lenovo\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
   下次登录自动后台启动。

四、SSH 连接方式
- 终端命令：
  ssh -i "C:\Users\lenovo\.ssh\666" -p 12345 lenovo@13.14.223.23

- Termius 填写：
  Host 13.14.223.23
  Port 12345
  User lenovo
  Key  选择 C:\Users\lenovo\.ssh\666（无口令）

五、权限与安全
- 私钥权限已限制为 lenovo、SYSTEM 可读。
- sshd 已关闭密码登录（PasswordAuthentication no），仅密钥。
- 管理员组用户使用 C:\ProgramData\ssh\666_keys 作为授权列表。

六、常用检查
- 查看 frpc 运行：任务管理器或
  netstat -ano | findstr 1234
- 查看 frpc 日志（WSL 版，如需）：/tmp/frpc-wsl.log
- 测试 SSH：上面的 ssh 命令返回 ok 即通。

七、故障排查速查
- "Permission denied (publickey)":
  * 确认 666 公钥在 C:\ProgramData\ssh\666_keys
  * 确认私钥路径/权限正确。
- "Connection refused": frps 未运行或端口 1234/12345 未放行。
- frpc 未连接：前台运行 frpc 查看提示，或检查 frpc.ini 中 server_addr、token 是否匹配。


Termius（手机端）连接步骤：

1. 创建主机
    - Host (Address): 13.14.223.23
    - Port: 12345
    - Label 可自定义（如 FRP-Home）
2. 认证方式选择 Key
    - 在 Authentication 选择 Key
    - 点击 Import Key（或“从文件/粘贴”）
    - 将本机私钥 666 的内容导入（建议用安全方式传到手机，再粘贴；如果 Termius 支持从文件导入，选该文件）。
      私钥内容在 PC 路径：C:\Users\lenovo\.ssh\666（纯文本，-----BEGIN OPENSSH PRIVATE KEY----- 开头）。
    - Passphrase 留空（此钥无口令）。
3. 用户名
    - Username: lenovo
4. 保存并连接
    - 首次连接接受指纹提示即可。
5. 可选安全措施
    - 在 Termius 中为该私钥设置本地加密密码（App 层保护）。
    - 若不方便复制私钥，可生成移动端新钥，并将其公钥追加到 C:\ProgramData\ssh\666_keys，但目前 666 已可用，按上面导入即可。

一键启动命令（在当前管理员 PowerShell 执行）

# 放行、防解除阻 & 直接前台启动
Add-MpPreference -ExclusionPath "C:\frp"
Unblock-File C:\frp\frpc.exe
cd C:\frp
.\frpc.exe -c frpc.ini

如果想后台启动（不占窗口）：

cd C:\frp
Start-Process -FilePath ".\frpc.exe" -ArgumentList "-c frpc.ini" -WindowStyle Hidden

需要开机自启（最高权限）：

schtasks /Create /TN "FRPClient" /TR "C:\frp\frpc.exe -c C:\frp\frpc.ini" /SC ONLOGON /RL HIGHEST /F /RU lenovo
