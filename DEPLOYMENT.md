# 🚀 GitHub Actions 一键部署指南

本文档将指导你如何将 UESTC-Energyfy 部署到 GitHub Actions，实现自动化监控。

---

## 📋 前置准备

### 1. Fork 或上传本仓库到你的 GitHub

```bash
# 方式1: Fork 原仓库
# 在 GitHub 页面点击 Fork 按钮

# 方式2: 上传到新仓库
cd /path/to/UESTC-Energyfy
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/UESTC-Energyfy.git
git push -u origin master
```

### 2. 准备配置信息

你需要准备以下信息：

#### 必需配置：
- **UESTC_USERNAME**: 你的学号
- **UESTC_PASSWORD**: 统一认证平台密码
- **ROOM_NAME**: 宿舍号（多个用逗号分隔，如 `114514,214514`）
- **SMTP_SERVER**: SMTP服务器地址（如 `smtp.qq.com`）
- **SMTP_USERNAME**: SMTP用户名（通常是邮箱）
- **SMTP_PASSWORD**: SMTP密码或授权码
- **EMAIL_RECIPIENTS**: 收件人邮箱（多个用逗号分隔）

#### 可选配置：
- **ALERT_BALANCE**: 告警阈值（默认 `10` 元）
- **CHECK_INTERVAL**: 检查间隔（默认 `0`，单次模式）
- **SMTP_PORT**: SMTP端口（默认 `465`）
- **SMTP_SECURITY**: 加密方式（`ssl`/`tls`/`none`，默认 `ssl`）
- **SERVER_CHAN_ENABLED**: 是否启用Server酱（`true`/`false`）
- **SERVER_CHAN_UID**: Server酱用户UID
- **SERVER_CHAN_SENDKEY**: Server酱发送密钥

---

## ⚙️ 配置 GitHub Secrets

### 步骤 1：进入仓库设置

1. 打开你的 GitHub 仓库
2. 点击 **Settings** (设置)
3. 在左侧菜单找到 **Secrets and variables** → **Actions**
4. 点击 **New repository secret**

### 步骤 2：添加 Secrets

依次添加以下 secrets（**Name** 必须完全匹配）：

| Name | Value | 示例 |
|------|-------|------|
| `UESTC_USERNAME` | 你的学号 | `2021010101` |
| `UESTC_PASSWORD` | 统一认证密码 | `yourPassword123` |
| `ROOM_NAME` | 宿舍号 | `114514` 或 `114514,214514` |
| `ALERT_BALANCE` | 告警阈值 | `10` |
| `SMTP_SERVER` | SMTP服务器 | `smtp.qq.com` |
| `SMTP_PORT` | SMTP端口 | `465` |
| `SMTP_USERNAME` | SMTP用户名 | `your@email.com` |
| `SMTP_PASSWORD` | SMTP密码 | `授权码` |
| `SMTP_SECURITY` | 加密方式 | `ssl` |
| `EMAIL_RECIPIENTS` | 收件人邮箱 | `user1@qq.com,user2@163.com` |
| `SERVER_CHAN_ENABLED` | 启用Server酱 | `false` 或 `true` |
| `SERVER_CHAN_UID` | Server酱UID | `your-uid` |
| `SERVER_CHAN_SENDKEY` | Server酱密钥 | `your-sendkey` |

### 步骤 3：保存配置

每个 secret 添加后点击 **Add secret** 保存。

---

## 🎯 启用 GitHub Actions

### 自动启用

1. 进入仓库的 **Actions** 标签页
2. 如果看到提示，点击 **I understand my workflows, go ahead and enable them**
3. 在左侧找到 **UESTC Energy Monitor** workflow
4. 点击 **Enable workflow**

### 手动触发测试

1. 在 **Actions** 页面选择 **UESTC Energy Monitor**
2. 点击右侧的 **Run workflow** 下拉菜单
3. 点击绿色的 **Run workflow** 按钮
4. 等待执行完成，查看日志

---

## ⏰ 定时任务配置

默认配置为**每30分钟执行一次**。如需修改：

编辑 `.github/workflows/energy-monitor.yml` 文件：

```yaml
schedule:
  - cron: '*/30 * * * *'  # 每30分钟
  # - cron: '0 */1 * * *'   # 每1小时
  # - cron: '0 */2 * * *'   # 每2小时
  # - cron: '0 8,20 * * *'  # 每天8点和20点
```

⚠️ **注意**：GitHub Actions cron 最短间隔建议不低于 5 分钟。

---

## 🔍 监控运行状态

### 查看执行日志

1. 进入 **Actions** 页面
2. 点击任意一次运行记录
3. 展开 **🔍 执行监控检查** 步骤查看详细日志

### 常见日志输出

```
✅ 正常运行：
配置文件验证通过
开始查询1个房间的余额信息
房间 114514 当前余额: 25.50元

⚠️ 低余额告警：
房间 114514 当前余额: 8.50元, 低于阈值 (8.50 < 10)
1个房间需要通知
已向Server酱用户 xxx 发送通知
已向房间 114514 发送邮件通知

❌ 错误情况：
登录失败，状态码401  # 检查账号密码
配置文件验证失败    # 检查 Secrets 配置
```

---

## 📧 邮箱配置指南

### QQ 邮箱

1. 登录 QQ 邮箱网页版
2. **设置** → **账户** → 找到 **POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务**
3. 开启 **IMAP/SMTP服务**
4. 生成**授权码**（不是QQ密码！）
5. 配置：
   - `SMTP_SERVER`: `smtp.qq.com`
   - `SMTP_PORT`: `465`
   - `SMTP_SECURITY`: `ssl`
   - `SMTP_PASSWORD`: 使用**授权码**

### 163 邮箱

1. 登录 163 邮箱网页版
2. **设置** → **POP3/SMTP/IMAP** → 开启 **IMAP/SMTP服务**
3. 设置**客户端授权密码**
4. 配置：
   - `SMTP_SERVER`: `smtp.163.com`
   - `SMTP_PORT`: `465`
   - `SMTP_SECURITY`: `ssl`
   - `SMTP_PASSWORD`: 使用**授权密码**

### Gmail

1. 开启 **两步验证**
2. 生成 **应用专用密码**
3. 配置：
   - `SMTP_SERVER`: `smtp.gmail.com`
   - `SMTP_PORT`: `587`
   - `SMTP_SECURITY`: `tls`
   - `SMTP_PASSWORD`: 使用**应用专用密码**

---

## 📱 Server酱³配置（可选）

Server酱³ 是一款手机推送服务，无需后台常驻即可接收消息。

### 注册步骤

1. 访问 [Server酱³官网](https://sc3.ft07.com/)
2. 注册账号并登录
3. 获取 **UID** 和 **SendKey**
4. 手机安装 **Server酱** APP
5. 在 APP 中登录同一账号

### 配置 Secrets

- `SERVER_CHAN_ENABLED`: `true`
- `SERVER_CHAN_UID`: 你的UID
- `SERVER_CHAN_SENDKEY`: 你的SendKey

---

## 🛠️ 高级配置

### 监控多个宿舍

在 `ROOM_NAME` 中用逗号分隔多个房间号：

```
ROOM_NAME: 114514,214514,314514
```

### 多个收件人

在 `EMAIL_RECIPIENTS` 中用逗号分隔多个邮箱：

```
EMAIL_RECIPIENTS: user1@qq.com,user2@163.com,user3@gmail.com
```

### 调整执行频率

编辑 `.github/workflows/energy-monitor.yml`：

```yaml
schedule:
  # 每小时执行
  - cron: '0 * * * *'
  
  # 每天早晚各执行一次
  - cron: '0 8,20 * * *'
  
  # 工作日每2小时执行
  - cron: '0 */2 * * 1-5'
```

---

## ❓ 常见问题

### Q1: Actions 没有自动执行？

**A:** 
1. 检查 Actions 是否已启用
2. 确认 workflow 文件路径正确：`.github/workflows/energy-monitor.yml`
3. 首次运行可能需要手动触发一次

### Q2: 提示 "登录失败，状态码401"？

**A:**
1. 检查 `UESTC_USERNAME` 和 `UESTC_PASSWORD` 是否正确
2. 尝试在官网手动登录，完成滑动验证
3. 等待几分钟后重试

### Q3: 邮件发送失败？

**A:**
1. 确认使用的是**授权码**而不是邮箱密码
2. 检查 SMTP 服务器地址和端口
3. 确认 SMTP 服务已在邮箱设置中开启
4. 查看 Actions 日志中的详细错误信息

### Q4: 如何停止监控？

**A:**
1. 进入 **Actions** 页面
2. 选择 **UESTC Energy Monitor** workflow
3. 点击右上角的 **...** (三个点)
4. 选择 **Disable workflow**

### Q5: GitHub Actions 有使用限制吗？

**A:**
- **公开仓库**：完全免费，无限制
- **私有仓库**：每月 2000 分钟免费额度
- 本项目每次执行约 1-2 分钟
- 每30分钟执行一次，每月约 1440 次，约 1440-2880 分钟

### Q6: 如何查看历史记录？

**A:**
- GitHub Actions 会保留最近的执行记录
- 可以在 **Actions** 页面查看所有历史运行
- 失败的运行会自动保存日志文件（保留7天）

---

## 🔐 安全建议

1. **使用私有仓库**：避免配置信息泄露
2. **定期更换密码**：建议定期更换 UESTC 密码和邮箱授权码
3. **最小权限原则**：仅添加必需的 Secrets
4. **不要共享 Secrets**：不要将 Secrets 分享给他人
5. **审查代码**：部署前检查代码，确保没有后门

---

## 📝 维护说明

### 更新依赖

编辑 `requirements.txt` 后，下次执行会自动安装新版本。

### 修改代码

1. 修改本地代码
2. 提交到 GitHub
3. Actions 会自动使用最新代码

### 备份配置

建议将你的 Secrets 配置保存到本地安全位置，以便迁移或重建。

---

## 📞 支持

遇到问题？

1. 查看本文档的**常见问题**部分
2. 查看 Actions 执行日志中的详细错误信息
3. 在原仓库提交 Issue

---

## 📄 许可证

本项目继承原仓库的许可证。

---

**祝你使用愉快！🎉**
