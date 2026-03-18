# 配置默认收件人邮箱

## 📧 问题说明

在使用AI新闻助手时，每次发送邮件都需要指定收件人邮箱。如果您希望自动发送到固定邮箱，可以配置默认收件人。

---

## 🔧 配置方法

### 步骤1：编辑配置文件

打开 `config/agent_llm_config.json` 文件

### 步骤2：设置默认收件人

在文件开头找到 `default_recipient_email` 字段，填入您的邮箱：

```json
{
    "default_recipient_email": "your-email@example.com",
    "models": {
        ...
    }
}
```

### 步骤3：保存并重启服务

保存文件后，重启Agent服务即可生效。

---

## ✅ 配置后的效果

### 之前（每次需要输入）
```
用户：搜索AI新闻并发送
Agent：请问您的收件邮箱地址是什么？
用户：myemail@example.com
Agent：好的，正在发送...
```

### 配置后（自动使用默认邮箱）
```
用户：搜索AI新闻并发送
Agent：好的，正在搜索并自动发送到默认邮箱（myemail@example.com）...
```

---

## 🎯 优先级说明

邮件发送的收件人优先级：

1. **用户指定的邮箱**（最高优先级）
   - 例如："搜索AI新闻并发送到 test@example.com"
   - Agent会使用用户指定的邮箱

2. **配置文件中的默认邮箱**
   - 如果用户没有指定，使用配置文件中的 `default_recipient_email`

3. **询问用户**（最后兜底）
   - 如果用户未指定，且配置文件也没有默认邮箱，才会询问用户

---

## 📝 示例配置

```json
{
    "default_recipient_email": "zhangsan@company.com",
    "models": {
        "cost-effective": {
            "id": "doubao-seed-2-0-mini-260215",
            "name": "豆包 2.0 Mini",
            ...
        },
        "balanced": {
            "id": "doubao-seed-2-0-lite-260215",
            ...
        }
    },
    "active_model": "balanced",
    ...
}
```

---

## ⚠️ 注意事项

1. **邮箱格式验证**
   - 邮箱地址必须包含 `@` 符号
   - 例如：`user@example.com`

2. **留空表示不使用默认邮箱**
   ```json
   {
       "default_recipient_email": "",
       ...
   }
   ```
   如果留空，则每次都需要用户指定邮箱

3. **可以随时修改**
   - 修改配置文件后重启服务即可生效
   - 无需修改代码

---

## 🔍 验证配置

### 测试1：不指定邮箱
```
用户：搜索AI新闻并发送
```
如果配置了默认邮箱，Agent会自动发送到默认邮箱。

### 测试2：指定邮箱
```
用户：搜索AI新闻并发送到 other@example.com
```
即使配置了默认邮箱，也会使用用户指定的邮箱。

---

## 💡 常见问题

**Q: 配置后还能发送给其他人吗？**
A: 可以！在对话中指定邮箱即可，例如："发送到 other@example.com"

**Q: 如何查看当前配置的默认邮箱？**
A: 查看 `config/agent_llm_config.json` 文件中的 `default_recipient_email` 字段

**Q: 可以配置多个默认收件人吗？**
A: 当前版本不支持，但可以在对话中指定多个收件人（逗号分隔）

**Q: 配置文件修改后需要重启吗？**
A: 是的，需要重启Agent服务才能生效

---

## 🎉 完成！

配置默认收件人后，您可以更方便地使用AI新闻助手，无需每次都输入邮箱地址。
