# 平台集成方案详解

## 📊 真实支持情况

### ❌ 不支持的平台

#### 1. 豆包app
- **状态**：不支持
- **原因**：豆包app是字节跳动的消费级应用，不开放API接口
- **无法实现**：不能在豆包app中集成您的Agent

#### 2. 个人微信
- **状态**：不支持
- **原因**：微信官方不开放个人微信机器人接口
- **无法实现**：不能在个人微信中接收消息并回复

---

### ⚠️ 支持但需要开发

#### 1. 微信公众号
- **支持功能**：接收用户消息、自动回复
- **开发难度**：⭐⭐⭐ 中等
- **需要**：
  1. 注册微信公众号（服务号或订阅号）
  2. 配置服务器URL
  3. 处理消息接收和回复
  4. 处理微信签名验证

#### 2. 企业微信应用
- **支持功能**：接收消息、自动回复、定时推送
- **开发难度**：⭐⭐ 中等
- **需要**：
  1. 创建企业微信应用
  2. 配置回调URL
  3. 处理消息接收和回复

#### 3. 飞书机器人
- **支持功能**：接收消息、自动回复、定时推送
- **开发难度**：⭐⭐ 中等
- **需要**：
  1. 创建飞书应用
  2. 配置事件订阅
  3. 处理消息回调

---

### ✅ 完全支持

#### 定时推送（推荐方案）⭐⭐⭐⭐⭐
- **支持功能**：每天固定时间自动推送AI资讯
- **开发难度**：⭐ 简单
- **支持平台**：
  - ✅ 邮件
  - ✅ 飞书群（通过机器人Webhook）

---

## 🚀 推荐方案：定时推送

### 方案说明

创建定时任务，每天自动：
1. 搜索最新的AI新闻
2. 筛选出10条最有价值的新闻
3. 推送到您指定的平台

### 实现步骤

#### 第1步：配置推送平台

编辑 `config/schedule_config.json`：

```json
{
    "schedule": {
        "time": "09:00",
        "timezone": "Asia/Shanghai"
    },
    "platforms": {
        "email": {
            "enabled": true,
            "recipient": "your-email@example.com"
        },
        "feishu": {
            "enabled": true,
            "webhook_url": "your-webhook-url"
        }
    }
}
```

#### 第2步：配置飞书群机器人（可选）

1. 在飞书群中添加机器人
2. 复制Webhook地址
3. 将Webhook地址配置到Coze平台

#### 第3步：设置定时任务

**方式1：使用cron（Linux/Mac）**

```bash
# 编辑crontab
crontab -e

# 添加定时任务（每天早上9点执行）
0 9 * * * cd /workspace/projects && python scripts/scheduled_news_push.py >> /app/work/logs/bypass/scheduled.log 2>&1
```

**方式2：使用APScheduler（Python）**

创建 `scripts/scheduler.py`：

```python
from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess

scheduler = BlockingScheduler()

@scheduler.scheduled_job('cron', hour=9, minute=0)
def push_news():
    subprocess.run(['python', 'scripts/scheduled_news_push.py'])

scheduler.start()
```

运行：
```bash
python scripts/scheduler.py
```

**方式3：使用系统服务（systemd）**

创建 `/etc/systemd/system/ai-news-push.service`：

```ini
[Unit]
Description=AI News Push Service
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/bin/python /workspace/projects/scripts/scheduled_news_push.py
WorkingDirectory=/workspace/projects

[Install]
WantedBy=multi-user.target
```

创建定时器 `/etc/systemd/system/ai-news-push.timer`：

```ini
[Unit]
Description=AI News Push Timer

[Timer]
OnCalendar=*-*-* 09:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

启用：
```bash
systemctl enable ai-news-push.timer
systemctl start ai-news-push.timer
```

---

## 🎯 最佳实践建议

### 场景1：每天接收AI资讯推送
- **推荐方案**：定时推送
- **推送平台**：邮件 + 飞书群
- **实现难度**：⭐ 简单
- **时间投入**：30分钟

### 场景2：在飞书中与Agent对话
- **推荐方案**：飞书机器人
- **开发难度**：⭐⭐ 中等
- **时间投入**：1天

---

## 📝 快速开始

### 最简单的方案：定时推送到邮件

#### 第1步：配置收件人邮箱
```bash
vi config/schedule_config.json
```

修改：
```json
{
    "platforms": {
        "email": {
            "enabled": true,
            "recipient": "your-email@example.com"
        }
    }
}
```

#### 第2步：手动测试
```bash
python scripts/scheduled_news_push.py
```

#### 第3步：设置定时任务
```bash
# 添加到crontab
crontab -e

# 每天早上9点执行
0 9 * * * cd /workspace/projects && python scripts/scheduled_news_push.py
```

---

## ⚠️ 重要说明

### 关于豆包app
- ❌ **无法在豆包app中集成您的Agent**
- ✅ **豆包是LLM模型，您的Agent已经在使用豆包模型**
- ✅ **如果您想在豆包的对话界面使用，需要在Coze平台上操作**

### 关于飞书
- ✅ **飞书群机器人支持单向推送**
- ✅ **飞书应用支持双向对话（需要开发）**

---

## 🎉 总结

| 需求 | 推荐方案 | 实现难度 | 时间投入 |
|------|----------|----------|----------|
| 每天接收AI资讯 | 定时推送 | ⭐ 简单 | 30分钟 |
| 飞书对话 | 飞书机器人 | ⭐⭐ 中等 | 1天 |
| 豆包app对话 | 不支持 | - | - |

**建议**：先实现定时推送（最实用、最简单），后续有需要再开发双向对话功能。
