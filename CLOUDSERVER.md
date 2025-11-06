# ☁️ 云服务器部署指南

如果你有云服务器（阿里云、腾讯云、AWS等），可以使用本指南进行部署。

---

## 📋 环境要求

- **操作系统**：Linux (推荐 Ubuntu 20.04+, CentOS 7+)
- **Python**：3.8+
- **内存**：512MB 以上
- **磁盘**：1GB 以上
- **网络**：需要能访问 UESTC 官网

---

## 🚀 快速部署（一键脚本）

### 1. 创建部署脚本

```bash
# 连接到服务器
ssh user@your-server-ip

# 创建安装脚本
cat > install_energyfy.sh << 'EOF'
#!/bin/bash

set -e

echo "🚀 开始安装 UESTC-Energyfy..."

# 检查 Python 版本
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，正在安装..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip
fi

# 检查 git
if ! command -v git &> /dev/null; then
    echo "📦 安装 git..."
    sudo apt-get install -y git
fi

# 克隆仓库
echo "📥 克隆仓库..."
cd ~
if [ -d "UESTC-Energyfy" ]; then
    echo "⚠️  目录已存在，正在更新..."
    cd UESTC-Energyfy
    git pull
else
    git clone https://github.com/YOUR_USERNAME/UESTC-Energyfy.git
    cd UESTC-Energyfy
fi

# 安装依赖
echo "📦 安装 Python 依赖..."
pip3 install --user -r requirements.txt

# 安装 Node.js (用于 execjs)
if ! command -v node &> /dev/null; then
    echo "📦 安装 Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

echo "✅ 安装完成！"
echo ""
echo "📝 接下来的步骤："
echo "1. 编辑配置文件: nano ~/UESTC-Energyfy/config.json"
echo "2. 启动服务: cd ~/UESTC-Energyfy && ./start_service.sh"
EOF

chmod +x install_energyfy.sh
./install_energyfy.sh
```

### 2. 创建配置文件

```bash
cd ~/UESTC-Energyfy

# 复制模板
cat > config.json << 'EOF'
{
  "username": "YOUR_STUDENT_ID",
  "password": "YOUR_PASSWORD",
  "check_interval": 1800,
  "alert_balance": 10,
  "smtp": {
    "server": "smtp.qq.com",
    "port": 465,
    "username": "your@email.com",
    "password": "your_auth_code",
    "security": "ssl"
  },
  "queries": [
    {
      "room_name": "114514",
      "recipients": [
        "recipient@email.com"
      ],
      "server_chan": {
        "enabled": false,
        "recipients": []
      }
    }
  ]
}
EOF

# 编辑配置
nano config.json
```

---

## 🔧 服务管理

### 方案1: systemd 服务（推荐）

创建系统服务，开机自启、自动重启：

```bash
# 创建服务文件
sudo cat > /etc/systemd/system/energyfy.service << EOF
[Unit]
Description=UESTC Energy Monitor Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/UESTC-Energyfy
ExecStart=/usr/bin/python3 $HOME/UESTC-Energyfy/Energyfy.py -c $HOME/UESTC-Energyfy/config.json
Restart=always
RestartSec=30
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# 重载服务配置
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start energyfy

# 设置开机自启
sudo systemctl enable energyfy

# 查看状态
sudo systemctl status energyfy

# 查看日志
sudo journalctl -u energyfy -f
```

**常用命令：**
```bash
# 启动服务
sudo systemctl start energyfy

# 停止服务
sudo systemctl stop energyfy

# 重启服务
sudo systemctl restart energyfy

# 查看状态
sudo systemctl status energyfy

# 查看实时日志
sudo journalctl -u energyfy -f

# 查看最近100行日志
sudo journalctl -u energyfy -n 100
```

### 方案2: screen 后台运行

适合临时运行或调试：

```bash
# 安装 screen
sudo apt-get install screen

# 创建新会话并运行
screen -S energyfy
cd ~/UESTC-Energyfy
python3 Energyfy.py -c config.json

# 按 Ctrl+A 然后按 D 退出会话（程序继续运行）

# 恢复会话
screen -r energyfy

# 查看所有会话
screen -ls

# 结束会话
screen -X -S energyfy quit
```

### 方案3: nohup 后台运行

最简单的后台运行方式：

```bash
cd ~/UESTC-Energyfy

# 后台运行
nohup python3 Energyfy.py -c config.json > output.log 2>&1 &

# 查看进程
ps aux | grep Energyfy

# 查看日志
tail -f output.log

# 停止服务
pkill -f Energyfy.py
```

---

## 📊 监控和维护

### 查看运行状态

```bash
# systemd 服务状态
sudo systemctl status energyfy

# 实时日志
sudo journalctl -u energyfy -f

# 查看特定时间的日志
sudo journalctl -u energyfy --since "2024-01-01" --until "2024-01-02"

# 查看错误日志
sudo journalctl -u energyfy -p err
```

### 更新代码

```bash
cd ~/UESTC-Energyfy
git pull
sudo systemctl restart energyfy
```

### 修改配置

```bash
nano ~/UESTC-Energyfy/config.json
sudo systemctl restart energyfy
```

### 定期清理日志

```bash
# 限制 journal 日志大小
sudo journalctl --vacuum-size=100M

# 清理应用日志
cd ~/UESTC-Energyfy
rm -rf logs/*.log.backup*
```

---

## 🔐 安全加固

### 1. 文件权限

```bash
# 设置配置文件权限（防止他人读取密码）
chmod 600 ~/UESTC-Energyfy/config.json

# 确保只有所有者可以访问
ls -l ~/UESTC-Energyfy/config.json
# 应该显示: -rw------- 1 user user ...
```

### 2. 防火墙设置

```bash
# 如果使用 ufw
sudo ufw enable
sudo ufw allow 22/tcp  # SSH
sudo ufw status

# 如果使用 firewalld
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload
```

### 3. 定期更新系统

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get upgrade

# CentOS
sudo yum update
```

---

## 📈 性能优化

### 调整检查间隔

根据实际需求调整 `check_interval`：

- **高频监控**：600秒（10分钟）
- **常规监控**：1800秒（30分钟）
- **低频监控**：3600秒（1小时）

```json
{
  "check_interval": 1800
}
```

### 资源使用

本程序资源占用极小：
- **内存**：约 30-50MB
- **CPU**：查询时瞬间峰值 < 10%
- **磁盘**：日志文件，建议定期清理
- **网络**：每次查询约 100KB

---

## 🐳 Docker 部署（高级）

### 1. 创建 Dockerfile

```bash
cd ~/UESTC-Energyfy

cat > Dockerfile << 'EOF'
FROM python:3.11-slim

# 安装依赖
RUN apt-get update && \
    apt-get install -y nodejs npm && \
    rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 创建日志目录
RUN mkdir -p logs

# 运行程序
CMD ["python", "Energyfy.py", "-c", "config.json"]
EOF
```

### 2. 构建并运行

```bash
# 构建镜像
docker build -t energyfy:latest .

# 运行容器
docker run -d \
  --name energyfy \
  --restart unless-stopped \
  -v $(pwd)/config.json:/app/config.json:ro \
  -v $(pwd)/logs:/app/logs \
  energyfy:latest

# 查看日志
docker logs -f energyfy

# 停止容器
docker stop energyfy

# 重启容器
docker restart energyfy
```

### 3. Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  energyfy:
    build: .
    container_name: energyfy
    restart: unless-stopped
    volumes:
      - ./config.json:/app/config.json:ro
      - ./logs:/app/logs
    environment:
      - TZ=Asia/Shanghai
```

运行：
```bash
docker-compose up -d
docker-compose logs -f
```

---

## ❓ 故障排除

### 问题1: ImportError: No module named 'xxx'

**解决方案：**
```bash
pip3 install --user -r requirements.txt
# 或
sudo pip3 install -r requirements.txt
```

### 问题2: execjs 错误

**解决方案：**
```bash
# 安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# 验证安装
node --version
```

### 问题3: 登录失败 401

**解决方案：**
1. 检查账号密码
2. 到官网手动登录一次
3. 等待几分钟后重试

### 问题4: 邮件发送失败

**解决方案：**
1. 检查 SMTP 配置
2. 确认使用授权码
3. 检查服务器网络是否能访问邮箱服务器

### 问题5: 服务自动停止

**解决方案：**
```bash
# 使用 systemd 自动重启
sudo systemctl enable energyfy
sudo systemctl restart energyfy
```

---

## 📞 技术支持

遇到问题？

1. 查看日志：`sudo journalctl -u energyfy -f`
2. 检查配置：`cat ~/UESTC-Energyfy/config.json`
3. 查看进程：`ps aux | grep Energyfy`
4. 在原仓库提交 Issue

---

## 🎉 完成

恭喜！你已经成功在云服务器上部署了 UESTC-Energyfy。

**建议：**
- 定期检查服务状态
- 设置告警通知
- 定期更新代码和依赖
- 备份配置文件

**下一步：**
- 添加监控多个宿舍
- 配置 Server酱推送
- 调整检查频率
