# 开箱即用（Standalone）版本使用说明

## 概述

本项目提供 Windows 可执行文件版本，无需安装 Python 或任何依赖，直接运行即可使用。

---

## 系统要求

- **操作系统**：Windows 10 或更高版本
- **内存**：建议至少 2GB 可用内存
- **网络**：需要能连接到校园网网关

---

## 快速开始

### 1. 下载并解压

1. 下载 `campus-portal-autologin.zip`
2. 解压到任意目录（建议：`C:\CampusPortalAutologin`）

### 2. 配置

1. 找到 `config.json.template` 文件
2. 复制并重命名为 `config.json`
3. 使用文本编辑器（记事本或 VS Code）编辑

```json
{
  "username": "你的学号",
  "password": "你的密码",
  "isp": "telecom",
  "gateway_url": "http://你的网关IP地址",
  "retry_times": 3,
  "retry_interval": 5
}
```

**参数说明**：

| 参数 | 说明 | 示例 |
|:-----|:-----|:------|
| `username` | 学号或宽带账号（不需要加后缀） | `"123456789"` |
| `password` | 校园网登录密码 | `"MyPassword"` |
| `isp` | 运营商 | `free`（免费）、`telecom`（电信）、`mobile`（移动）、`unicom`（联通） |
| `gateway_url` | 校园网登录页面地址 | `"http://172.16.1.11"` |
| `retry_times` | 登录失败重试次数 | `3` |
| `retry_interval` | 每次重试间隔（秒） | `5` |

### 3. 运行

**方式一：手动运行测试**

```bash
# 进入解压目录
cd CampsPortalAutologin

# 运行可执行文件
CampusPortalAutologin.exe
```

**方式二：设置开机自启（推荐）**

确认手动运行成功后，设置开机自动连接：

1. 在目录中找到 `install_task.py`
2. 右键 → "使用管理员 PowerShell 运行"
3. 按照屏幕提示操作即可

脚本会自动：
- 请求管理员权限
- 生成静默启动脚本
- 注册 Windows 任务计划（开机登录后 30 秒触发）
- 完成后无需手动干预

### 4. 取消开机自启

如需卸载：

1. 在目录中找到 `remove_task_scheduler.bat`
2. 右键 → "以管理员身份运行"
3. 确认卸载

---

## 文件说明

解压后的目录结构：

```
CampusPortalAutologin/
├── CampusPortalAutologin.exe          # 主程序（内置 Python 和 Playwright）
├── config.json.template              # 配置文件模板
├── config.json                     # 用户配置文件（需手动创建）
├── install_task.py                 # 一键安装开机自启脚本
├── remove_task_scheduler.bat          # 一键卸载开机自启
└── README_STANDALONE.md            # 本说明文档
```

---

## 常见问题

### Q1：运行提示缺少 DLL 文件？

**原因**：某些 Windows 版本缺少系统运行库

**解决**：
- 安装 [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64)
- 重新运行可执行文件

### Q2：浏览器无法启动？

**原因**：Playwright 浏览器组件问题

**解决**：
- 确保 Windows 系统已更新到最新版本
- 禁用杀毒软件临时测试（可能误报）

### Q3：如何查看运行日志？

日志文件位置：`campus_connect.log`（程序运行目录）

```bash
# 查看日志
type campus_connect.log  # Windows CMD
Get-Content campus_connect.log  # PowerShell

# 或用文本编辑器打开
```

### Q4：提示配置文件不存在？

**解决**：
1. 检查是否存在 `config.json`
2. 如果不存在，从 `config.json.template` 复制并重命名
3. 填写正确的配置信息

### Q5：可以修改延迟启动时间吗？

可以！编辑生成的 `run_hidden.vbs` 文件，修改以下行：

```vbscript
WScript.Sleep 30000  ' 30000 = 30秒，可按需调整
```

---

## 安全说明

### 密码保护

- `config.json` 包含明文存储的密码
- 建议将程序安装在用户目录，不要共享
- 定期更换校园网密码

### 权限管理

程序需要以下权限：
- 网络访问（连接校园网）
- 文件读写（日志和配置）
- 任务计划注册（开机自启）

### 杀毒软件

首次运行时，某些杀毒软件可能误报为病毒。这是因为：
- PyInstaller 生成的可执行文件有时会被误报
- 建议添加到杀毒软件白名单

---

## 性能说明

- **首次启动时间**：5-10 秒（解压资源）
- **后续启动时间**：2-3 秒
- **内存占用**：150-300MB（包含浏览器）
- **磁盘占用**：约 300MB（解压后）

---

## 更新说明

如需更新到新版本：

1. 下载新版本的可执行文件
2. 备份当前的 `config.json`
3. 删除旧版本目录
4. 解压新版本
5. 恢复 `config.json`

---

## 技术支持

如遇到问题：

1. 查看日志文件 `campus_connect.log`
2. 检查配置文件是否正确
3. 确认网络连接正常
4. 联系开发者或在 GitHub 提交 Issue

---

## 开源项目

本项目基于 Python + Playwright 开发，源码地址：

https://github.com/wengao65-svg/campus-portal-autologin

如需自行编译或修改代码，请查看源码仓库的 README.md。

---

<div align="center">

**如果这个工具对你有帮助，请给它一个 ⭐ Star！**

Made with ❤️ by 广科学生

</div>
