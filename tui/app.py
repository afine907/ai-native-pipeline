"""
AI Native Pipeline TUI - Main Application
基于 Textual 的交互式终端 UI
"""
import os
import asyncio

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Button, Input, Log
from textual.binding import Binding
from textual import work


# Agent 列表 (从 skills 目录动态加载)
AGENTS = [
    ("impact-analyzer", "📊 影响分析"),
    ("prd-agent", "📝 需求分析"),
    ("spec-agent", "⚙️ 技术规格"),
    ("coding-agent", "💻 代码生成"),
    ("verification-agent", "✅ 验收验证"),
]

# Skills 列表
SKILLS = [
    ("pipeline", "🔄 完整流水线"),
    ("task-breakdown", "📋 任务拆解"),
    ("code-review", "🔍 代码审查"),
    ("test-generator", "🧪 测试生成"),
]

# 所有可用命令
COMMANDS = [
    "/pipeline - 完整流水线",
    "/impact - 影响分析",
    "/prd - 需求分析",
    "/spec - 技术规格",
    "/coding - 代码生成",
    "/verify - 验收验证",
    "/breakdown - 任务拆解",
    "/review - 代码审查",
    "/test - 测试生成",
    "/skills - 列出所有 skills",
    "/clear - 清除屏幕",
    "/help - 帮助信息",
]


class AgentStatus(Static):
    """Agent 状态面板"""
    
    def __init__(self, agent_id: str, label: str):
        super().__init__(label)
        self.agent_id = agent_id
        self.status = "waiting"  # waiting, running, done, error
    
    def set_status(self, status: str):
        """设置状态"""
        self.status = status
        self.update(self.label.replace("⏳", "🔄").replace("✅", "❌").replace("❌", "✅") if status == "done" else self.label)
        # TODO: 更新样式


class CommandInput(Input):
    """命令输入框，支持补全"""
    
    COMMANDS = [
        "/pipeline - 完整流水线",
        "/impact - 影响分析",
        "/prd - 需求分析",
        "/spec - 技术规格",
        "/coding - 代码生成",
        "/verify - 验收验证",
        "/breakdown - 任务拆解",
        "/review - 代码审查",
        "/test - 测试生成",
        "/clear - 清除屏幕",
        "/help - 帮助信息",
    ]
    
    def __init__(self):
        super().__init__(placeholder="输入命令 (Tab 补全)...")
        self.history = []
        self.history_index = -1
    
    def key_down(self, event) -> None:
        """处理下方向键 - 历史记录"""
        if event.key == "up":
            if self.history and self.history_index < len(self.history) - 1:
                self.history_index += 1
                self.value = self.history[-(self.history_index + 1)]
        elif event.key == "down":
            if self.history_index > 0:
                self.history_index -= 1
                self.value = self.history[-(self.history_index + 1)]
            elif self.history_index == 0:
                self.history_index = -1
                self.value = ""
        else:
            super().key_down(event)


class AgentPanel(Vertical):
    """左侧 Agent + Skills 面板"""
    
    def compose(self) -> ComposeResult:
        yield Static("🤖 Agents", classes="panel-title")
        for agent_id, label in AGENTS:
            yield Static(f"⏳ {label}", id=f"agent-{agent_id}")
        
        yield Static("", classes="divider")
        yield Static("🔧 Skills", classes="panel-title")
        for skill_id, label in SKILLS:
            yield Static(f"⏳ {label}", id=f"skill-{skill_id}")


class MainPanel(Vertical):
    """主面板 - 输出区域"""
    
    def compose(self) -> ComposeResult:
        yield Static("📋 对话记录", classes="panel-title")
        yield Log(id="output-log", auto_scroll=True)


class StatusBar(Static):
    """底部状态栏"""
    
    def __init__(self):
        super().__init__("就绪 | 按 / 或输入命令 | Ctrl+C 取消")
    
    def update_status(self, text: str):
        self.update(text)


class AIPipelineTUI(App):
    """AI Native Pipeline TUI 主应用"""
    
    CSS = """
    Screen {
        layout: vertical;
    }
    
    # header {
        background: $accent;
        color: white;
        height: 3;
        content-align: center middle;
    }
    
    # main {
        layout: horizontal;
        height: 100%;
    }
    
    # agent-panel {
        width: 25;
        background: $surface;
        border-right: solid $border;
        padding: 1;
    }
    
    # agent-panel .panel-title {
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }
    
    # agent-panel Static {
        margin: 1 0;
    }
    
    # main-panel {
        width: 75;
        background: $surface;
        padding: 1;
    }
    
    # main-panel .panel-title {
        text-style: bold;
        color: $accent;
    }
    
    # output-log {
        height: 100%;
        border: solid $border;
        margin-top: 1;
    }
    
    # status-bar {
        height: 3;
        background: $surface-darken-1;
        content-align: center middle;
    }
    
    # input-container {
        height: 3;
        padding: 1;
        background: $surface;
    }
    
    # command-input {
        width: 100%;
    }
    """
    
    BINDINGS = [
        Binding("ctrl+c", "cancel", "取消", show=False),
        Binding("ctrl+l", "clear", "清屏", show=False),
        Binding("ctrl+q", "quit", "退出", show=False),
        Binding("f1", "help", "帮助", show=False),
    ]
    
    def __init__(self):
        super().__init__()
        self.current_agent = None
        self._running_tasks: list[asyncio.Task] = []
    
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        with Horizontal(id="main"):
            with Vertical(id="agent-panel"):
                yield AgentPanel()
            
            with Vertical(id="main-panel"):
                yield MainPanel()
        
        yield StatusBar(id="status-bar")
        
        with Container(id="input-container"):
            yield Input(placeholder="输入命令 (Tab 补全, /help 查看帮助)", id="command-input")
    
    def on_mount(self) -> None:
        """应用启动"""
        self.title = "🤖 AI Native Pipeline"
        self.sub_title = "基于 Harness Engineering 的 AI 开发流水线"
        
        # 显示欢迎信息
        log = self.query_one("#output-log", Log)
        log.write_line("🎉 欢迎使用 AI Native Pipeline TUI!")
        log.write_line("")
        log.write_line("📋 可用命令:")
        log.write_line("  /pipeline  - 完整流水线")
        log.write_line("  /impact    - 影响分析")
        log.write_line("  /prd       - 需求分析")
        log.write_line("  /spec      - 技术规格")
        log.write_line("  /coding    - 代码生成")
        log.write_line("  /verify    - 验收验证")
        log.write_line("  /help      - 查看帮助")
        log.write_line("")
        log.write_line("💡 提示: 输入命令后按 Enter 执行")
        
        # 聚焦输入框
        self.query_one("#command-input", Input).focus()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """处理输入的命令"""
        command = event.value.strip()
        if not command:
            return
        
        # 添加到历史
        input_widget = self.query_one("#command-input", Input)
        if command not in input_widget.history:
            input_widget.history.append(command)
        
        # 清空输入
        event.input.value = ""
        
        # 处理命令
        self.execute_command(command)
    
    def execute_command(self, command: str):
        """执行命令"""
        log = self.query_one("#output-log", Log)
        status = self.query_one("#status-bar", StatusBar)
        
        # 解析命令
        if command.startswith("/"):
            parts = command.split(maxsplit=1)
            cmd = parts[0]
            arg = parts[1] if len(parts) > 1 else ""
        else:
            # 非命令前缀，当作需求处理
            cmd = "/pipeline"
            arg = command
        
        log.write_line(f"\n➜ 执行: {command}")
        status.update_status(f"执行中: {cmd}...")
        
        # 根据命令执行
        if cmd == "/help":
            self.show_help(log)
        elif cmd == "/clear":
            log.clear()
        elif cmd == "/skills":
            self.show_skills(log, status)
        elif cmd == "/pipeline":
            self.run_pipeline(arg, log, status)
        elif cmd in ["/impact", "/prd", "/spec", "/coding", "/verify"]:
            self.run_agent(cmd[1:], arg, log, status)
        elif cmd == "/breakdown":
            self.run_skill("task-breakdown", arg, log, status)
        elif cmd == "/review":
            self.run_skill("code-review", arg, log, status)
        elif cmd == "/test":
            self.run_skill("test-generator", arg, log, status)
        else:
            log.write_line(f"❓ 未知命令: {cmd}")
            log.write_line("💡 输入 /help 查看可用命令")
            status.update_status("就绪")
    
    def show_help(self, log: Log):
        """显示帮助"""
        log.write_line("""
📖 AI Native Pipeline TUI 帮助

可用命令:
  /pipeline [需求]  - 运行完整流水线
  /impact [需求]    - 运行影响分析 Agent
  /prd [需求]       - 运行需求分析 Agent
  /spec             - 运行技术规格 Agent
  /coding           - 运行代码生成 Agent
  /verify           - 运行验收验证 Agent
  /breakdown        - 任务拆解
  /review           - 代码审查
  /test             - 测试生成
  /skills           - 列出所有 Skills
  /clear            - 清除屏幕
  /help             - 显示帮助

快捷键:
  Ctrl+C  - 取消当前任务
  Ctrl+L  - 清除屏幕
  Ctrl+Q  - 退出应用
  ↑/↓     - 命令历史
  Tab     - 命令补全
""")
        self.query_one("#status-bar", StatusBar).update_status("就绪")
    
    def show_skills(self, log: Log, status: StatusBar):
        """显示所有 Skills"""
        log.write_line("\n📦 AI Native Pipeline Skills:")
        log.write_line("")
        log.write_line("🤖 Agents (5):")
        for agent_id, label in AGENTS:
            log.write_line(f"  {label}")
        log.write_line("")
        log.write_line("🔧 Skills (4):")
        for skill_id, label in SKILLS:
            log.write_line(f"  {label}")
        log.write_line("")
        log.write_line("📁 Skills 位置: ./skills/")
        log.write_line("📁 Agents 位置: ./skills/ (已同步)")
        status.update_status("就绪")
    
    def run_skill(self, skill: str, arg: str, log: Log, status: StatusBar):
        """运行 Skill"""
        skill_display = {
            "task-breakdown": "📋 任务拆解",
            "code-review": "🔍 代码审查",
            "test-generator": "🧪 测试生成",
            "pipeline": "🔄 完整流水线",
        }
        
        log.write_line(f"\n🔧 运行 Skill: {skill_display.get(skill, skill)}...")
        
        # 检查 skill 文件是否存在
        skill_path = f"skills/{skill}/SKILL.md"
        if os.path.exists(skill_path):
            log.write_line(f"  ✅ Skill 文件: {skill_path}")
            # 使用 worker 装饰器执行异步任务
            self._run_skill_worker(skill, skill_display, log, status)
        else:
            log.write_line(f"  ❌ Skill 文件不存在: {skill_path}")
            status.update_status("就绪")
    
    @work(exclusive=True)
    async def _run_skill_worker(self, skill: str, skill_display: dict, log: Log, status: StatusBar):
        """Worker for skill execution"""
        await asyncio.sleep(0.5)
        log.write_line(f"  ✅ {skill_display.get(skill, skill)} 完成")
        status.update_status("就绪")
    
    def run_agent(self, agent: str, arg: str, log: Log, status: StatusBar):
        """运行单个 Agent"""
        agent_display = {
            "impact-analyzer": "📊 影响分析",
            "prd-agent": "📝 需求分析",
            "spec-agent": "⚙️ 技术规格",
            "coding-agent": "💻 代码生成",
            "verification-agent": "✅ 验收验证",
        }
        
        log.write_line(f"\n🔄 运行 {agent_display.get(agent, agent)}...")
        
        # 更新 Agent 状态
        agent_widget = self.query_one(f"#agent-{agent}", Static)
        agent_widget.update(f"🔄 {agent_display.get(agent, agent)}")
        
        # 使用 worker 装饰器执行异步任务
        self._run_agent_worker(agent, agent_display, agent_widget, log, status)
    
    @work(exclusive=True)
    async def _run_agent_worker(self, agent: str, agent_display: dict, agent_widget: Static, log: Log, status: StatusBar):
        """Worker for agent execution"""
        await asyncio.sleep(1)
        log.write_line(f"  ✓ {agent_display.get(agent, agent)} 完成")
        agent_widget.update(f"✅ {agent_display.get(agent, agent)}")
        status.update_status("就绪")
    
    def run_pipeline(self, requirement: str, log: Log, status: StatusBar):
        """运行完整流水线"""
        if not requirement:
            log.write_line("❌ 请输入需求描述")
            log.write_line("💡 用法: /pipeline [需求描述]")
            status.update_status("就绪")
            return
        
        log.write_line(f"\n🚀 启动完整流水线...")
        log.write_line(f"📝 需求: {requirement}")
        
        # 使用 worker 装饰器执行流水线
        self._run_pipeline_worker(requirement, log, status)
    
    @work(exclusive=True)
    async def _run_pipeline_worker(self, requirement: str, log: Log, status: StatusBar):
        """Worker for pipeline execution"""
        for agent_id, label in AGENTS:
            log.write_line(f"\n🔄 运行 {label}...")
            status.update_status(f"执行中: {label}")
            
            # 模拟执行
            await asyncio.sleep(0.8)
            log.write_line(f"  ✓ {label} 完成")
            
            await asyncio.sleep(0.3)
        
        log.write_line("\n🎉 流水线执行完成!")
        status.update_status("就绪")
    
    def action_cancel(self):
        """取消当前任务"""
        log = self.query_one("#output-log", Log)
        log.write_line("\n⚠️ 任务已取消")
        self.query_one("#status-bar", StatusBar).update_status("就绪")
    
    def action_clear(self):
        """清除屏幕"""
        self.query_one("#output-log", Log).clear()
    
    def action_help(self):
        """显示帮助"""
        log = self.query_one("#output-log", Log)
        self.show_help(log)
    
    def action_quit(self):
        """退出应用"""
        self.exit()


def main():
    """入口函数"""
    app = AIPipelineTUI()
    app.run()


if __name__ == "__main__":
    main()