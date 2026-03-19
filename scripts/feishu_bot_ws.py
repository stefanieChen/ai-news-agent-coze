#!/usr/bin/env python3
"""
飞书对话机器人服务（WebSocket长连接模式）
使用飞书官方SDK的WebSocket客户端
"""

import sys
import os
import json
import logging
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# 飞书SDK
import lark_oapi as lark
from lark_oapi.ws.client import Client as WSClient
from lark_oapi.api.im.v1 import CreateMessageRequest, CreateMessageRequestBody
from lark_oapi.event.dispatcher_handler import EventDispatcherHandler

# 导入Agent
from agents.agent import build_agent
from coze_coding_utils.runtime_ctx.context import new_context

# 配置
FEISHU_APP_ID = "cli_a930e5b631795cef"
FEISHU_APP_SECRET = "cMDvA5Nprt8DAUwXUh5UNb0ukoTiWoQk"

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/work/logs/bypass/feishu_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 全局变量
_agent_instance = None
_agent_ctx = None
_http_client = None

def get_agent():
    """获取Agent实例（单例）"""
    global _agent_instance, _agent_ctx
    if _agent_instance is None:
        _agent_ctx = new_context(method="feishu_chat")
        # 飞书Bot在非异步环境中运行，使用同步的 MemorySaver
        _agent_instance = build_agent(_agent_ctx, force_sync_checkpointer=True)
        logger.info("Agent实例已初始化")
    return _agent_instance

def get_http_client():
    """获取HTTP客户端（用于发送消息）"""
    global _http_client
    if _http_client is None:
        _http_client = lark.Client.builder() \
            .app_id(FEISHU_APP_ID) \
            .app_secret(FEISHU_APP_SECRET) \
            .log_level(lark.LogLevel.INFO) \
            .build()
    return _http_client

def send_message(open_id, text):
    """发送飞书消息"""
    try:
        from lark_oapi.api.im.v1.model import CreateMessageRequestBody

        client = get_http_client()

        # 构建消息内容
        content = {
            "text": text
        }

        # 构建请求体
        body = CreateMessageRequestBody.builder() \
            .receive_id(open_id) \
            .msg_type("text") \
            .content(json.dumps(content)) \
            .build()

        # 构建请求
        req = CreateMessageRequest.builder() \
            .receive_id_type("open_id") \
            .request_body(body) \
            .build()

        # 发送消息
        response = client.im.v1.message.create(req)

        if response.code != 0:
            logger.error(f"发送消息失败: {response.code}, {response.msg}")
            return False

        logger.info(f"消息已发送到 {open_id}")
        return True

    except Exception as e:
        logger.error(f"发送消息异常: {e}")
        import traceback
        traceback.print_exc()
        return False

def on_message(event):
    """处理接收到的飞书消息事件（接受 CustomizedEvent 对象）"""
    try:
        # CustomizedEvent 对象结构
        logger.info(f"收到事件: {event}")

        # 获取事件数据
        event_data = event.event if hasattr(event, 'event') else {}
        sender = event_data.get("sender", {})
        message = event_data.get("message", {})

        # 获取消息内容
        content_str = message.get("content", "{}")
        content = json.loads(content_str) if isinstance(content_str, str) else content_str
        user_message = content.get("text", "").strip()

        if not user_message:
            logger.warning("消息内容为空，跳过")
            return

        # 获取发送者ID
        sender_info = sender.get("sender_id", {})
        sender_open_id = sender_info.get("open_id", "")
        chat_id = message.get("chat_id", "")

        logger.info(f"收到消息: {user_message} from {sender_open_id} (chat: {chat_id})")

        # 调用Agent处理
        agent = get_agent()

        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        }

        config = {"configurable": {"thread_id": chat_id}}

        # 在新线程中调用Agent（避免异步事件循环冲突）
        import threading

        result = None
        error = None

        logger.info("开始在线程中调用Agent...")

        def sync_invoke():
            nonlocal result, error
            try:
                logger.info("Agent.invoke() 被调用")
                result = agent.invoke(payload, config=config, context=_agent_ctx)
                logger.info("Agent.invoke() 完成")
            except Exception as e:
                error = e
                logger.error(f"Agent调用异常: {e}")
                import traceback
                traceback.print_exc()

        thread = threading.Thread(target=sync_invoke)
        logger.info("启动Agent线程")
        thread.start()
        logger.info("等待Agent线程完成...")
        thread.join(timeout=120)  # 最多等待120秒

        logger.info(f"线程状态: is_alive={thread.is_alive()}, error={error}, result={result}")

        if thread.is_alive():
            logger.error("Agent调用超时（超过120秒）")
            reply = "抱歉，处理超时，请稍后重试。"
        elif error:
            logger.error(f"Agent调用异常: {error}")
            import traceback
            traceback.print_exc()
            reply = "抱歉，处理您的请求时出现错误。"
        else:
            # 提取回复
            logger.info("提取Agent回复...")
            if result and "messages" in result:
                last_message = result["messages"][-1]
                reply = last_message.content if hasattr(last_message, 'content') else str(last_message)
            else:
                reply = "抱歉，我暂时无法处理您的请求。"

        logger.info(f"Agent回复: {reply}")

        # 发送回复
        send_message(sender_open_id, reply)

    except Exception as e:
        logger.error(f"处理事件异常: {e}")
        import traceback
        traceback.print_exc()

def main():
    """启动WebSocket长连接机器人"""
    logger.info("=" * 60)
    logger.info("飞书对话机器人服务（WebSocket长连接模式）")
    logger.info("=" * 60)

    logger.info(f"App ID: {FEISHU_APP_ID}")
    logger.info("使用WebSocket长连接模式，无需公网IP")
    logger.info("使用简单事件处理器（不加密）")
    logger.info("\n✅ 服务启动中...")
    logger.info("   按 Ctrl+C 停止服务\n")

    try:
        # 创建事件处理器（不加密模式）
        # 注意：飞书SDK的WebSocket长连接模式仍然需要 EventDispatcherHandler
        # 但如果不配置加密，encrypt_key 和 verification_token 传空字符串
        handler_builder = EventDispatcherHandler.builder("", "")

        # 注册消息接收事件处理器（v1和v2都需要注册）
        handler_builder.register_p1_customized_event("im.message.receive_v1", on_message)
        handler_builder.register_p2_customized_event("im.message.receive_v1", on_message)

        event_handler = handler_builder.build()

        # 创建WebSocket客户端
        ws_client = WSClient(
            app_id=FEISHU_APP_ID,
            app_secret=FEISHU_APP_SECRET,
            log_level=lark.LogLevel.INFO,
            event_handler=event_handler
        )

        logger.info("✅ WebSocket客户端已创建")
        logger.info("✅ 事件处理器已注册（不加密模式）")
        logger.info("🔌 正在连接飞书服务器...\n")

        # 启动长连接（阻塞）
        ws_client.start()

    except KeyboardInterrupt:
        logger.info("\n\n⏹️  服务已停止")
    except Exception as e:
        logger.error(f"服务异常: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
