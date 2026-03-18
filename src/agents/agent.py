import os
import json
from typing import Annotated
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from coze_coding_utils.runtime_ctx.context import default_headers

# 导入工具
from tools.news_search_tool import search_ai_news
from tools.email_tool import send_news_email

# 导入记忆存储
from storage.memory.memory_saver import get_memory_saver

LLM_CONFIG = "config/agent_llm_config.json"

# 默认保留最近 20 轮对话 (40 条消息)
MAX_MESSAGES = 40

def _windowed_messages(old, new):
    """滑动窗口: 只保留最近 MAX_MESSAGES 条消息"""
    return add_messages(old, new)[-MAX_MESSAGES:]  # type: ignore

class AgentState(MessagesState):
    messages: Annotated[list[AnyMessage], _windowed_messages]

def build_agent(ctx=None):
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    config_path = os.path.join(workspace_path, LLM_CONFIG)

    # 读取配置文件
    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")

    # 获取激活的模型（优先使用环境变量，否则使用配置文件中的active_model）
    active_model_key = os.getenv("COZE_ACTIVE_MODEL", cfg.get("active_model", "balanced"))

    # 从models对象中获取对应的模型配置
    models = cfg.get("models", {})
    if active_model_key not in models:
        print(f"警告: 未找到模型 '{active_model_key}'，使用默认模型 'balanced'")
        active_model_key = "balanced"

    model_config = models[active_model_key]

    # 合并全局配置和模型特定配置
    global_config = cfg.get("config", {})
    final_config = {
        "model": model_config.get("id"),
        "temperature": model_config.get("temperature", global_config.get("temperature", 0.7)),
        "top_p": model_config.get("top_p", global_config.get("top_p", 0.9)),
        "max_completion_tokens": model_config.get("max_completion_tokens", global_config.get("max_completion_tokens", 10000)),
        "timeout": global_config.get("timeout", 600),
        "thinking": model_config.get("thinking", global_config.get("thinking", "disabled"))
    }

    print(f"使用模型: {model_config.get('name')} ({model_config.get('id')})")

    # 初始化LLM
    llm = ChatOpenAI(
        model=final_config["model"],
        api_key=api_key,
        base_url=base_url,
        temperature=final_config["temperature"],
        streaming=True,
        timeout=final_config["timeout"],
        extra_body={
            "thinking": {
                "type": final_config["thinking"]
            }
        },
        default_headers=default_headers(ctx) if ctx else {}
    )

    # 创建Agent，包含新闻搜索和邮件发送工具
    return create_agent(
        model=llm,
        system_prompt=cfg.get("sp"),
        tools=[search_ai_news, send_news_email],
        checkpointer=get_memory_saver(),
        state_schema=AgentState,
    )
