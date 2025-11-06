# 🚀 快速开始：一键配置 GitHub Actions

本文档提供最简化的步骤，帮你在 **5分钟内** 完成 GitHub Actions 部署。

---

## 📋 准备清单

在开始之前，请准备以下信息：

- [ ] 电子科大学号
- [ ] 统一认证平台密码  
- [ ] 宿舍号（如：`114514`）
- [ ] 邮箱账号（QQ邮箱或163邮箱）
- [ ] 邮箱授权码（**不是密码！**）

> 💡 **如何获取邮箱授权码？**
> - **QQ邮箱**：设置 → 账户 → POP3/IMAP/SMTP → 生成授权码
> - **163邮箱**：设置 → POP3/SMTP/IMAP → 开启服务 → 设置授权密码

---

## 🎯 三步完成部署

### 第一步：Fork 本仓库

1. 点击本仓库右上角的 **Fork** 按钮
2. 等待 Fork 完成（约5秒）

### 第二步：配置 Secrets

1. 在你 Fork 的仓库中，点击 **Settings** (设置)
2. 左侧菜单选择 **Secrets and variables** → **Actions**  
3. 点击 **New repository secret**，依次添加以下配置：

#### 必需配置（共8个）

| Name（必须完全一致） | Value（填你的信息） | 示例 |
|---------------------|-------------------|------|
| `UESTC_USERNAME` | 你的学号 | `2021010101` |
| `UESTC_PASSWORD` | 统一认证密码 | `MyPassword123` |
| `ROOM_NAME` | 宿舍号 | `114514` |
| `ALERT_BALANCE` | 余额告警阈值（元） | `10` |
| `SMTP_SERVER` | 邮箱SMTP服务器 | `smtp.qq.com` |
| `SMTP_PORT` | SMTP端口 | `465` |
| `SMTP_USERNAME` | 你的邮箱 | `your@qq.com` |
| `SMTP_PASSWORD` | **邮箱授权码** | `abcdefghijklmnop` |

#### 可选配置（不用也行）

| Name | Value | 默认值 |
|------|-------|--------|
| `SMTP_SECURITY` | 加密方式 | `ssl` |
| `EMAIL_RECIPIENTS` | 收件人邮箱 | 同发件人 |
| `SERVER_CHAN_ENABLED` | 是否启用Server酱 | `false` |

> ⚠️ **重要提示**：
> - `SMTP_PASSWORD` 必须填写**授权码**，不是邮箱登录密码！
> - QQ邮箱 `SMTP_SERVER` 填 `smtp.qq.com`
> - 163邮箱 `SMTP_SERVER` 填 `smtp.163.com`

### 第三步：启用 Actions

1. 点击仓库顶部的 **Actions** 标签页
2. 如果看到提示，点击 **I understand my workflows, go ahead and enable them**
3. 在左侧找到 **UESTC Energy Monitor**
4. 点击 **Enable workflow**
5. 点击右侧 **Run workflow** → 绿色按钮 **Run workflow** 进行首次测试

---

## ✅ 验证部署

### 1. 查看执行结果

- 等待约 1-2 分钟
- 在 **Actions** 页面查看运行状态
- 绿色 ✅ = 成功，红色 ❌ = 失败

### 2. 查看日志

点击运行记录 → 展开 **🔍 执行监控检查** 步骤：

**成功示例：**
```
✅ 配置文件已生成：config.json
📊 监控房间数：1
配置文件验证通过
房间 114514 当前余额: 25.50元
```

**告警示例：**
```
房间 114514 当前余额: 8.50元, 低于阈值 (8.50 < 10)
已向房间 114514 发送邮件通知
```

### 3. 检查邮箱

如果余额低于阈值，你会收到邮件通知。

---

## 🎉 完成！

恭喜！你已经成功部署了自动监控服务：

- ⏰ **每30分钟自动检查一次**
- 📧 **余额不足自动发送邮件**
- 🔄 **完全自动化，无需人工干预**

---

## 📝 进阶配置

### 监控多个宿舍

在 `ROOM_NAME` 中用逗号分隔：
```
ROOM_NAME: 114514,214514,314514
```

### 添加多个收件人

添加 Secret：
```
EMAIL_RECIPIENTS: user1@qq.com,user2@163.com,user3@gmail.com
```

### 调整检查频率

编辑 `.github/workflows/energy-monitor.yml` 文件中的 cron 表达式：

```yaml
schedule:
  - cron: '*/30 * * * *'  # 每30分钟（默认）
  # - cron: '0 * * * *'     # 每小时
  # - cron: '0 8,20 * * *'  # 每天8点和20点
```

### 启用 Server酱推送

1. 访问 [Server酱官网](https://sc3.ft07.com/) 注册
2. 获取 UID 和 SendKey
3. 添加 Secrets：
   - `SERVER_CHAN_ENABLED`: `true`
   - `SERVER_CHAN_UID`: 你的UID
   - `SERVER_CHAN_SENDKEY`: 你的SendKey
4. 在手机上安装 **Server酱** APP

---

## ❓ 常见问题

### Q: 报错 "登录失败，状态码401"

**A:** 检查 `UESTC_USERNAME` 和 `UESTC_PASSWORD` 是否正确，尝试到官网手动登录一次。

### Q: 邮件发送失败

**A:** 
1. 确认使用的是**授权码**不是密码
2. 确认 SMTP 服务已在邮箱设置中开启
3. 检查 `SMTP_SERVER` 和 `SMTP_PORT` 是否正确

### Q: Actions 没有自动执行

**A:** 
1. 确认已启用 Actions
2. 首次可能需要手动触发一次
3. 等待下一个30分钟周期

### Q: 如何停止监控？

**A:** Actions → UESTC Energy Monitor → 右上角 **...** → Disable workflow

### Q: GitHub Actions 免费吗？

**A:** 
- **公开仓库**：完全免费，无限制
- **私有仓库**：每月 2000 分钟免费额度
- 本项目每次约 1-2 分钟，足够使用

---

## 📖 详细文档

- **完整部署指南**：[DEPLOYMENT.md](DEPLOYMENT.md)
- **云服务器部署**：[CLOUDSERVER.md](CLOUDSERVER.md)
- **原始 README**：[README.md](README.md)

---

## 🔐 安全提示

1. ✅ 建议将仓库设为**私有**（Private）
2. ✅ 不要泄露你的 Secrets
3. ✅ 定期更换密码和授权码
4. ✅ 不要在公开位置分享你的配置

---

## 💡 提示

- 第一次部署建议手动触发测试
- 确保邮箱 SMTP 服务已开启
- 授权码和密码是两个东西！
- 遇到问题查看 Actions 日志

---

**祝你使用愉快！** 🎉

有问题？查看 [完整文档](DEPLOYMENT.md) 或在原仓库提 Issue。
