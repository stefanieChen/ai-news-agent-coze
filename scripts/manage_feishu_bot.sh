#!/bin/bash
# 飞书Bot服务管理脚本

SERVICE_NAME="feishu_bot"
SCRIPT_PATH="/workspace/projects/scripts/feishu_bot_ws.py"
PID_FILE="/tmp/feishu_bot.pid"
LOG_FILE="/app/work/logs/bypass/feishu_bot.log"

# 颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 启动服务
start() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo -e "${YELLOW}飞书Bot服务已经在运行中 (PID: $PID)${NC}"
            return 1
        else
            rm -f "$PID_FILE"
        fi
    fi

    echo -e "${GREEN}启动飞书Bot服务...${NC}"
    nohup python "$SCRIPT_PATH" >> "$LOG_FILE" 2>&1 &
    PID=$!
    echo $PID > "$PID_FILE"

    sleep 2

    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ 飞书Bot服务启动成功 (PID: $PID)${NC}"
        echo -e "${GREEN}📝 日志文件: $LOG_FILE${NC}"
        return 0
    else
        echo -e "${RED}❌ 飞书Bot服务启动失败${NC}"
        tail -20 "$LOG_FILE"
        return 1
    fi
}

# 停止服务
stop() {
    if [ ! -f "$PID_FILE" ]; then
        echo -e "${YELLOW}飞书Bot服务未运行${NC}"
        return 1
    fi

    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${YELLOW}停止飞书Bot服务 (PID: $PID)...${NC}"
        kill $PID
        sleep 2

        if ps -p "$PID" > /dev/null 2>&1; then
            echo -e "${YELLOW}强制停止...${NC}"
            kill -9 $PID
        fi

        rm -f "$PID_FILE"
        echo -e "${GREEN}✅ 飞书Bot服务已停止${NC}"
        return 0
    else
        echo -e "${YELLOW}飞书Bot服务进程不存在${NC}"
        rm -f "$PID_FILE"
        return 1
    fi
}

# 重启服务
restart() {
    stop
    sleep 1
    start
}

# 查看状态
status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo -e "${GREEN}✅ 飞书Bot服务正在运行 (PID: $PID)${NC}"

            # 显示连接状态
            if grep -q "connected to" "$LOG_FILE" 2>/dev/null; then
                LAST_CONNECTION=$(tail -5 "$LOG_FILE" | grep "connected to" | tail -1)
                echo -e "${GREEN}🔌 已连接: $LAST_CONNECTION${NC}"
            fi
            return 0
        else
            echo -e "${RED}❌ 飞书Bot服务未运行 (PID文件存在但进程不存在)${NC}"
            return 1
        fi
    else
        echo -e "${YELLOW}飞书Bot服务未运行${NC}"
        return 1
    fi
}

# 查看日志
logs() {
    if [ -f "$LOG_FILE" ]; then
        tail -f "$LOG_FILE"
    else
        echo -e "${RED}日志文件不存在: $LOG_FILE${NC}"
        return 1
    fi
}

# 查看最近日志
show_logs() {
    if [ -f "$LOG_FILE" ]; then
        tail -30 "$LOG_FILE"
    else
        echo -e "${RED}日志文件不存在: $LOG_FILE${NC}"
        return 1
    fi
}

# 主程序
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    logs)
        logs
        ;;
    show)
        show_logs
        ;;
    *)
        echo "飞书Bot服务管理脚本"
        echo ""
        echo "用法: $0 {start|stop|restart|status|logs|show}"
        echo ""
        echo "命令说明:"
        echo "  start   - 启动服务"
        echo "  stop    - 停止服务"
        echo "  restart - 重启服务"
        echo "  status  - 查看服务状态"
        echo "  logs    - 实时查看日志 (Ctrl+C 退出)"
        echo "  show    - 查看最近30行日志"
        echo ""
        exit 1
        ;;
esac

exit $?
