# 定时推送设置指南

## 📧 快速配置（3步完成）

### 第1步：配置收件邮箱

编辑 `scripts/schedule_config.json` 文件：

```json
{
    "platforms": {
        "email": {
            "enabled": true,
            "recipient": "your-real-email@example.com"  // ← 修改为您的真实邮箱
        }
    }
}
```

**或者使用环境变量**（推荐）：

```bash
export DEFAULT_RECIPIENT_EMAIL="your-real-email@example.com"
```

---

### 第2步：验证配置

运行测试脚本，确保邮件发送正常：

```bash
cd /workspace/projects
python scripts/scheduled_news_push.py
```

如果成功，您会收到一封测试邮件。

---

### 第3步：启动定时服务

#### 方式一：使用Python调度器（推荐，最简单）

```bash
cd /workspace/projects
python scripts/start_scheduler.py
```

**特点**：
- ✅ 开箱即用，无需额外配置
- ✅ 自动按配置的时间推送
- ⚠️ 需要保持进程运行

**后台运行**（推荐使用 nohup）：

```bash
nohup python scripts/start_scheduler.py > /app/work/logs/bypass/scheduler.log 2>&1 &
```

**查看日志**：

```bash
tail -f /app/work/logs/bypass/scheduler.log
```

**停止服务**：

```bash
# 查找进程
ps aux | grep start_scheduler.py

# 终止进程
kill <PID>
```

---

#### 方式二：使用cron（Linux/Mac）

**1. 编辑crontab**：

```bash
crontab -e
```

**2. 添加定时任务**：

```bash
# 每天16:00推送AI新闻
0 16 * * * cd /workspace/projects && python scripts/scheduled_news_push.py >> /app/work/logs/bypass/scheduled.log 2>&1
```

**3. 保存并退出**

- Vim: 按 `Esc` 然后输入 `:wq` 回车
- Nano: 按 `Ctrl+O` 保存，`Ctrl+X` 退出

**查看已设置的定时任务**：

```bash
crontab -l
```

**查看日志**：

```bash
tail -f /app/work/logs/bypass/scheduled.log
```

---

#### 方式三：使用systemd（Linux，适合生产环境）

**1. 创建服务文件**：

```bash
sudo vim /etc/systemd/system/ai-news-push.service
```

**内容**：

```ini
[Unit]
Description=AI News Push Service
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /workspace/projects/scripts/scheduled_news_push.py
WorkingDirectory=/workspace/projects
User=root
Environment="DEFAULT_RECIPIENT_EMAIL=your-email@example.com"

[Install]
WantedBy=multi-user.target
```

**2. 创建定时器**：

```bash
sudo vim /etc/systemd/system/ai-news-push.timer
```

**内容**：

```ini
[Unit]
Description=AI News Push Timer

[Timer]
OnCalendar=*-*-* 16:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

**3. 启用并启动**：

```bash
# 重载systemd配置
sudo systemctl daemon-reload

# 启用定时器
sudo systemctl enable ai-news-push.timer

# 启动定时器
sudo systemctl start ai-news-push.timer
```

**查看状态**：

```bash
# 查看定时器状态
sudo systemctl status ai-news-push.timer

# 查看下次运行时间
sudo systemctl list-timers ai-news-push.timer
```

---

## 🕐 修改推送时间

编辑 `scripts/schedule_config.json`：

```json
{
    "schedule": {
        "time": "16:00",      // ← 修改为您需要的时间
        "timezone": "Asia/Shanghai"
    }
}
```

**常用时区**：
- `Asia/Shanghai` - 中国标准时间
- `Asia/Tokyo` - 日本时间
- `America/New_York` - 美国东部时间
- `Europe/London` - 英国时间

---

## 📊 当前配置

```json
{
    "schedule": {
        "time": "16:00",
        "timezone": "Asia/Shanghai"
    },
    "platforms": {
        "email": {
            "enabled": true,
            "recipient": "your-email@example.com"  // ← 需要修改
        }
    }
}
```

---

## ✅ 验证清单

- [ ] 修改了收件邮箱地址
- [ ] 运行测试脚本验证邮件发送
- [ ] 选择并配置了定时任务方式
- [ ] 检查日志确认定时任务正常运行

---

## 🐛 常见问题

### Q1: 邮件发送失败？

**检查项**：
1. 确认邮箱地址正确
2. 检查邮件集成配置（`integration-email-imap-smtp`）
3. 查看日志 `/app/work/logs/bypass/app.log`

### Q2: 定时任务没有执行？

**检查项**：
1. 确认服务正在运行（Python调度器）
2. 检查cron任务列表（cron方式）
3. 查看systemd定时器状态（systemd方式）
4. 检查日志文件

### Q3: 如何立即测试推送？

```bash
python scripts/scheduled_news_push.py
```

### Q4: 如何查看推送历史？

查看日志文件：

```bash
# Python调度器日志
tail -f /app/work/logs/bypass/scheduler.log

# cron日志
tail -f /app/work/logs/bypass/scheduled.log

# 应用日志
tail -f /app/work/logs/bypass/app.log
```

---

## 🎯 推荐配置

**开发/测试环境**：使用方式一（Python调度器）
- 简单快速，方便调试
- 可以随时Ctrl+C停止

**生产环境**：使用方式三（systemd）
- 稳定可靠，自动重启
- 适合长期运行

**服务器无权限**：使用方式二（cron）
- 用户级别配置，无需root权限
- 灵活简单

---

## 📞 需要帮助？

如果遇到问题，请：
1. 检查日志文件
2. 确认配置正确
3. 运行测试脚本验证
