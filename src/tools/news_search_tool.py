from langchain.tools import tool, ToolRuntime
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context

@tool
def search_ai_news(query: str = "AI人工智能 最新动态", sites: str = "", runtime: ToolRuntime = None) -> str:
    """
    搜索AI相关的热点新闻
    
    Args:
        query: 搜索关键词，默认为"AI人工智能 最新动态"
        sites: 指定搜索的网站（可选），多个网站用逗号分隔，例如 "xinhuanet.com,qq.com,163.com"
    
    Returns:
        搜索到的新闻列表，包含标题、来源、链接、摘要等信息
    """
    try:
        # 获取或创建context
        ctx = runtime.context if runtime else new_context(method="search_ai_news")
        
        # 初始化搜索客户端
        client = SearchClient(ctx=ctx)
        
        # 准备搜索参数
        search_params = {
            "query": query,
            "search_type": "web",
            "count": 20,  # 获取20条新闻供筛选
            "need_summary": True,  # 获取AI生成的摘要
            "time_range": "1d"  # 搜索最近1天的新闻
        }
        
        # 如果指定了网站，添加sites参数
        if sites and sites.strip():
            search_params["sites"] = sites.strip()
            print(f"🔍 在指定网站搜索: {sites.strip()}")
        
        # 执行搜索
        response = client.search(**search_params)
        
        if not response.web_items or len(response.web_items) == 0:
            return "未找到相关新闻，请尝试更换关键词或稍后再试。"
        
        # 格式化搜索结果
        news_list = []
        for idx, item in enumerate(response.web_items, 1):
            news_info = {
                "序号": idx,
                "标题": item.title,
                "来源": item.site_name,
                "发布时间": item.publish_time or "未知",
                "链接": item.url,
                "摘要": item.summary or item.snippet
            }
            news_list.append(news_info)
        
        # 返回格式化的新闻列表
        result_text = f"搜索到 {len(news_list)} 条AI相关新闻"
        if sites and sites.strip():
            result_text += f"（来源网站: {sites.strip()}）"
        result_text += ":\n\n"
        
        for news in news_list:
            result_text += f"{news['序号']}. {news['标题']}\n"
            result_text += f"   来源: {news['来源']}\n"
            result_text += f"   时间: {news['发布时间']}\n"
            result_text += f"   摘要: {news['摘要'][:200]}...\n"
            result_text += f"   链接: {news['链接']}\n\n"
        
        return result_text
        
    except Exception as e:
        return f"搜索新闻时发生错误: {str(e)}"
