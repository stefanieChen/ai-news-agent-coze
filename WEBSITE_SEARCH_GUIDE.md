# 新闻搜索网站指定功能使用指南

## 📰 新闻搜索范围说明

### 默认搜索范围
当前Agent默认进行**全网搜索**，会从各大新闻网站获取AI相关新闻，包括但不限于：

#### 官方媒体
- 新华网 (xinhuanet.com)
- 中国新闻网 (chinanews.com)
- 人民网 (people.com.cn)
- 经济日报 (jjxww.cn)

#### 商业媒体
- 今日头条 (toutiao.com)
- 腾讯新闻 (qq.com)
- 新浪新闻 (sina.com.cn)
- 网易新闻 (163.com)
- 凤凰网 (ifeng.com)

#### 科技媒体
- 36氪 (36kr.com)
- 钛媒体 (tmtpost.com)
- 虎嗅网 (huxiu.com)
- InfoQ (infoq.cn)
- CSDN (csdn.net)
- 数智中国

---

## 🎯 网站指定功能

### 功能说明
现在支持指定搜索特定网站，可以：
- ✅ 只从指定网站搜索新闻
- ✅ 同时搜索多个网站
- ✅ 提高搜索结果的精准度
- ✅ 避免不相关网站的干扰

### 使用方法

#### 方法1: 对话中指定网站
直接告诉Agent要从哪些网站搜索：

```
请搜索今天的AI新闻，只从新华网和腾讯新闻搜索
```

```
从今日头条、36氪和钛媒体搜索最新的AI技术新闻
```

```
帮我从CSDN和InfoQ获取今天的技术动态
```

#### 方法2: Agent会自动识别
Agent会根据您的需求自动选择合适的网站：

```
搜索官方媒体报道的AI新闻
```
→ Agent会自动选择新华网、人民网等官方媒体

```
获取科技圈的最新动态
```
→ Agent会自动选择36氪、钛媒体、InfoQ等科技媒体

---

## 📝 支持的网站格式

网站可以使用以下格式：

| 格式 | 示例 | 说明 |
|------|------|------|
| 完整域名 | `xinhuanet.com` | 推荐使用 |
| 带协议 | `https://www.xinhuanet.com` | 也支持 |
| 多个网站 | `xinhuanet.com,qq.com,163.com` | 用逗号分隔 |

---

## 🔥 推荐网站组合

### 1. 官方媒体组合
```
xinhuanet.com,people.com.cn,chinanews.com
```
特点：权威、准确、官方发布

### 2. 科技媒体组合
```
36kr.com,tmtpost.com,huxiu.com,infoq.cn
```
特点：深度、专业、行业洞察

### 3. 商业媒体组合
```
toutiao.com,qq.com,163.com,sina.com.cn
```
特点：全面、及时、覆盖面广

### 4. 技术社区组合
```
csdn.cn,juejin.cn,infoq.cn,oschina.net
```
特点：技术细节、开发者视角

### 5. 全覆盖组合
```
xinhuanet.com,qq.com,163.com,36kr.com,tmtpost.com,csdn.net
```
特点：综合多个来源，信息最全面

---

## 💡 使用场景示例

### 场景1: 获取官方政策新闻
**用户需求**：
```
我想了解官方对AI的最新政策动向
```

**Agent行为**：
- 自动选择：新华网、人民网
- 搜索关键词：AI 政策 最新

### 场景2: 获取技术突破新闻
**用户需求**：
```
搜索AI技术突破的新闻，只看科技媒体的报道
```

**Agent行为**：
- 使用指定网站：36kr.com,tmtpost.com,infoq.cn
- 搜索关键词：AI 技术突破

### 场景3: 综合获取多角度信息
**用户需求**：
```
帮我从多个来源搜集今天的AI新闻
```

**Agent行为**：
- 使用默认全网搜索
- 整合官方媒体、商业媒体、科技媒体多个角度

---

## 🚨 注意事项

1. **网站域名要准确**
   - ❌ 错误：`xinhua`
   - ✅ 正确：`xinhuanet.com`

2. **多个网站用逗号分隔**
   - ❌ 错误：`xinhuanet.com qq.com`
   - ✅ 正确：`xinhuanet.com,qq.com`

3. **小写域名**
   - 推荐：使用小写域名
   - 大小写不敏感，但小写更规范

4. **不要加空格**
   - ❌ 错误：`xinhuanet. com`
   - ✅ 正确：`xinhuanet.com`

5. **英文逗号分隔**
   - ❌ 错误：`xinhuanet.com，qq.com`（中文逗号）
   - ✅ 正确：`xinhuanet.com,qq.com`（英文逗号）

---

## 🔧 技术实现细节

### 工具参数
`search_ai_news` 工具现在支持以下参数：

```python
@tool
def search_ai_news(
    query: str = "AI人工智能 最新动态",
    sites: str = "",  # 新增：指定网站
    runtime: ToolRuntime = None
) -> str:
```

### 搜索逻辑
```python
search_params = {
    "query": query,
    "search_type": "web",
    "count": 20,
    "need_summary": True,
    "time_range": "1d"
}

# 如果指定了网站
if sites and sites.strip():
    search_params["sites"] = sites.strip()
```

---

## 📞 常见问题

**Q: 搜索结果还是包含其他网站的新闻？**
A: 网站指定是"优先搜索"而非"强制限制"，可能会有少量其他网站的推荐结果。

**Q: 可以排除某些网站吗？**
A: 当前版本不支持排除功能，但可以指定您想要的网站，间接达到排除效果。

**Q: 搜索不到指定网站的新闻怎么办？**
A: 可能是网站名称不对或该网站暂无相关新闻，建议：
1. 检查网站域名是否正确
2. 尝试全网搜索
3. 更换搜索关键词

**Q: 可以搜索国外网站吗？**
A: 可以，只要是支持中文搜索的网站都可以尝试。

**Q: 如何知道当前搜索了哪些网站？**
A: 搜索结果会显示每条新闻的来源网站，您可以在结果中看到。

---

## 🎉 总结

现在您可以：
- ✅ 全网搜索（默认）
- ✅ 指定单个网站搜索
- ✅ 指定多个网站搜索
- ✅ Agent智能推荐网站

开始使用吧！如有任何问题，随时反馈。
