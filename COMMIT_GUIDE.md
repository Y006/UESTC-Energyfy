# 📤 提交到 GitHub 指南

本文档将指导你如何将改造后的项目提交到 GitHub。

---

## 🎯 提交前检查清单

在提交之前，请确认以下文件已正确创建：

### ✅ 核心文件

- [x] `.github/workflows/energy-monitor.yml` - GitHub Actions 工作流
- [x] `scripts/generate_config.py` - 配置生成脚本  
- [x] `scripts/test_config.py` - 配置验证工具
- [x] `requirements.txt` - Python 依赖列表
- [x] `config.example.json` - 配置示例

### ✅ 文档文件

- [x] `QUICKSTART.md` - 快速开始指南
- [x] `DEPLOYMENT.md` - 完整部署指南
- [x] `CLOUDSERVER.md` - 云服务器部署指南
- [x] `SUMMARY.md` - 项目分析总结
- [x] `README_NEW.md` - 新版 README
- [x] `README_ORIGINAL.md` - 原始 README 备份
- [x] `COMMIT_GUIDE.md` - 本文件

### ✅ 配置文件

- [x] `.gitignore` - Git 忽略规则（已更新）

---

## 🚀 方式 1：创建新仓库（推荐）

### 步骤 1：创建 GitHub 仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `UESTC-Energyfy-Auto` (或其他名称)
   - **Description**: `电子科大宿舍电费自动监控 - 支持 GitHub Actions`
   - **Visibility**: 选择 **Private**（推荐）或 Public
   - ⚠️ **不要** 勾选 "Initialize this repository with a README"
3. 点击 **Create repository**

### 步骤 2：准备本地仓库

```bash
# 进入项目目录
cd /Users/qiujinyu/Documents/UESTC-Energyfy

# 初始化 Git 仓库（如果还没有）
git init

# 添加所有文件
git add .

# 查看将要提交的文件
git status

# 提交到本地
git commit -m "feat: 添加 GitHub Actions 自动化部署支持

- 新增 GitHub Actions 工作流
- 新增配置生成和验证脚本
- 新增完整的部署文档
- 支持云服务器部署
- 优化 .gitignore 规则
"
```

### 步骤 3：推送到 GitHub

```bash
# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/YOUR_USERNAME/UESTC-Energyfy-Auto.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

---

## 🔄 方式 2：更新现有 Fork

如果你已经 Fork 了原仓库，可以在此基础上提交：

```bash
cd /Users/qiujinyu/Documents/UESTC-Energyfy

# 查看当前远程仓库
git remote -v

# 添加所有新文件
git add .

# 提交
git commit -m "feat: 添加 GitHub Actions 自动化部署支持"

# 推送到你的 Fork
git push origin master
# 或
git push origin main
```

---

## 📝 提交后配置

### 1. 替换 README（可选）

如果你想使用新版 README：

```bash
cd /Users/qiujinyu/Documents/UESTC-Energyfy

# 备份当前 README
mv README.md README_ORIGINAL.md

# 使用新版 README
mv README_NEW.md README.md

# 提交更改
git add README.md README_ORIGINAL.md README_NEW.md
git commit -m "docs: 更新 README 为新版文档"
git push
```

### 2. 配置 GitHub Secrets

在 GitHub 仓库页面：

1. 点击 **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**
3. 按照 [QUICKSTART.md](QUICKSTART.md) 添加必需的 Secrets

### 3. 启用 GitHub Actions

1. 点击 **Actions** 标签
2. 如果提示需要启用，点击 **I understand my workflows, go ahead and enable them**
3. 选择 **UESTC Energy Monitor** workflow
4. 点击 **Enable workflow**

### 4. 测试运行

1. 在 Actions 页面，点击 **UESTC Energy Monitor**
2. 点击 **Run workflow**
3. 选择分支（通常是 main 或 master）
4. 点击绿色的 **Run workflow** 按钮
5. 等待 1-2 分钟，查看运行结果

---

## 🔍 验证提交

### 检查文件结构

访问你的 GitHub 仓库，确认以下结构：

```
your-repo/
├── .github/
│   └── workflows/
│       └── energy-monitor.yml          ✅
├── scripts/
│   ├── generate_config.py              ✅
│   └── test_config.py                  ✅
├── utils/                               ✅
├── Energyfy.py                         ✅
├── requirements.txt                    ✅
├── schema.json                         ✅
├── config.example.json                 ✅
├── QUICKSTART.md                       ✅
├── DEPLOYMENT.md                       ✅
├── CLOUDSERVER.md                      ✅
├── SUMMARY.md                          ✅
├── README.md                           ✅
└── .gitignore                          ✅
```

### 检查 Actions

1. 进入 **Actions** 页面
2. 确认能看到 **UESTC Energy Monitor** workflow
3. 尝试手动触发一次
4. 查看运行日志，确保没有错误

---

## 📊 提交信息规范（参考）

使用规范的提交信息，便于后续维护：

```bash
# 新功能
git commit -m "feat: 添加 GitHub Actions 支持"

# 文档更新
git commit -m "docs: 更新部署文档"

# Bug 修复
git commit -m "fix: 修复配置验证错误"

# 性能优化
git commit -m "perf: 优化通知发送速度"

# 代码重构
git commit -m "refactor: 重构配置读取逻辑"
```

---

## 🛡️ 安全建议

### ⚠️ 不要提交敏感信息

确保以下文件已被 `.gitignore` 忽略：

- ❌ `config.json` - 包含真实的账号密码
- ❌ `*.log` - 日志文件可能包含敏感信息
- ❌ `active` - 激活配置的符号链接
- ❌ `private-folder-alias.json` - 私有配置

### ✅ 检查提交内容

提交前务必检查：

```bash
# 查看将要提交的文件
git status

# 查看文件内容
git diff

# 查看已暂存的更改
git diff --cached
```

如果发现敏感信息：

```bash
# 从暂存区移除
git reset HEAD <file>

# 或者修改文件后重新添加
git add <file>
```

---

## 🎉 完成！

恭喜！你已经成功提交了改造后的项目。

### 下一步

1. ✅ 配置 GitHub Secrets
2. ✅ 启用 Actions
3. ✅ 测试运行
4. ✅ 开始使用自动化监控

### 分享你的项目

如果你想分享：

1. 确保仓库是 **Public**
2. 在 README 中添加你的自定义说明
3. 添加 GitHub Actions 徽章：

```markdown
![Energy Monitor](https://github.com/YOUR_USERNAME/UESTC-Energyfy-Auto/workflows/UESTC%20Energy%20Monitor/badge.svg)
```

---

## 📞 需要帮助？

- 📖 查看 [QUICKSTART.md](QUICKSTART.md)
- 📖 查看 [DEPLOYMENT.md](DEPLOYMENT.md)
- 🐛 提交 Issue

---

**祝你使用愉快！** 🎉
