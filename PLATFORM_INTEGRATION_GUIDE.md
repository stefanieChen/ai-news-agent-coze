# 平台集成指南

## 📊 当前状态

您的AI新闻助手是一个**独立的API服务**，可以通过集成到各种平台使用。

---

## ✅ 支持的平台

### 1. 飞书群机器人 ✅

#### 功能
- 发送文本、富文本消息
- 发送交互式卡片
- 支持按钮交互

#### 集成步骤

**步骤1：创建飞书机器人**
1. 在飞书群中添加机器人
2. 自定义机器人名称
3. 复制Webhook地址

**步骤2：配置环境变量**
在Coze平台配置飞书机器人集成：
```
integration-feishu-message
```
填入Webhook地址

**步骤3：添加工具到Agent**
修改 `src/agents/agent.py`：
```python
from tools.feishu_tool import send_feishu_message

# 在create_agent中添加工具
tools=[search_ai_news, send_news_email, send_feishu_message]
```

**步骤4：使用示例**
```
用户：搜索AI新闻并发送到飞书群
Agent：正在搜索并推送到飞书...
```

---

### 2. 豆包 ⚠️

**说明**：豆包是一个**LLM模型**，不是平台

#### 使用方式

**方式1：选择豆包模型**
在配置文件中选择豆包模型：
```json
{
    "active_model": "balanced",  // 豆包2.0 Lite
    // 或者
    "active_model": "pro",  // 豆包2.0 Pro
    // 或者
    "active_model": "current",  // 豆包1.6
}
```

**方式2：环境变量**
```bash
export COZE_ACTIVE_MODEL=balanced
```

#### 说明
- ✅ 豆包是Agent使用的LLM模型
- ❌ 豆包不是消息平台
- ✅ 可以选择不同版本的豆包模型

---

## 🎯 推荐方案

### 方案1：多平台集成（推荐）

同时支持邮件和飞书：

```python
# src/agents/agent.py
from tools.news_search_tool import search_ai_news
from tools.email_tool import send_news_email
from tools.feishu_tool import send_feishu_message

create_agent(
    ...
    tools=[
        search_ai_news,
        send_news_email,
        send_feishu_message
    ]
)
```

**使用示例**：
```
用户：搜索AI新闻并发送到飞书
Agent：正在搜索并推送到飞书群...
```

---

### 方案2：选择单一平台

根据您的需求选择一个主要平台：

| 平台 | 优势 | 适用场景 |
|------|------|----------|
| 邮件 | 正式、可存档 | 工作汇报、重要通知 |
| 飞书 | 功能丰富、卡片式 | 项目管理、信息展示 |

---

## 📝 快速集成示例

### 完整的Agent工具配置

```python
# src/agents/agent.py

from tools.news_search_tool import search_ai_news
from tools.email_tool import send_news_email
from tools.feishu_tool import send_feishu_message

def build_agent(ctx=None):
    ...
    return create_agent(
        model=llm,
        system_prompt=cfg.get("sp"),
        tools=[
            search_ai_news,        # 搜索新闻
            send_news_email,       # 发送邮件
            send_feishu_message    # 发送到飞书
        ],
        checkpointer=get_memory_saver(),
        state_schema=AgentState,
    )
```

### 更新系统提示词

在 `config/agent_llm_config.json` 中添加：

```
# 能力
1. 搜索AI热点新闻：使用search_ai_news工具搜索最新的AI相关新闻
2. 筛选和评估：根据新闻的实用价值、重要性、时效性等维度评估新闻
3. 总结内容：用简洁清晰的语言总结每条新闻的核心内容
4. 发送邮件：使用send_news_email工具将汇总的新闻发送到指定邮箱
5. 推送到飞书：使用send_feishu_message工具推送到飞书群

# 过程
...
5. **推送消息**：
   - 用户可以指定推送到邮箱或飞书
   - 可以同时推送到多个平台
   - 如果未指定，默认使用邮件发送
```

---

## 🔧 配置清单

### 必需配置

| 配置项 | 平台 | 状态 |
|--------|------|------|
| `integration-email-imap-smtp` | 邮件 | ✅ 已配置 |
| `integration-feishu-message` | 飞书 | ⚠️ 需配置 |

### 配置位置

在Coze平台 → 项目设置 → 集成配置 中添加

---

## 💡 使用示例

### 示例1：只发送邮件
```
搜索AI新闻并发送到 myemail@example.com
```

### 示例2：推送到飞书
```
搜索AI新闻并发送到飞书群
```

### 示例3：多平台推送
```
搜索AI新闻并发送到飞书和邮箱 myemail@example.com
```

---

## ⚠️ 注意事项

1. **飞书机器人**
   - 需要先在飞书群中创建机器人
   - Webhook地址需要保密

2. **邮件**
   - 需要配置SMTP服务器
   - 需要邮箱授权码（非登录密码）

3. **豆包模型**
   - 已集成，无需额外配置
   - 可以选择不同版本

---

## 🎉 总结

| 平台 | 支持状态 | 配置难度 | 推荐指数 |
|------|----------|----------|----------|
| 邮件 | ✅ 已支持 | ⭐ 简单 | ⭐⭐⭐⭐⭐ |
| 飞书 | ✅ 可集成 | ⭐⭐ 中等 | ⭐⭐⭐⭐ |
| 豆包 | ✅ 已支持 | ⭐ 简单 | N/A（是模型） |

**建议**：根据您的实际使用场景选择1-2个主要平台集成即可。
