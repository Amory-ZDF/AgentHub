<div align="center">

<img src="https://img.shields.io/badge/Python-3.11+-blue?logo=python" alt="Python">
<img src="https://img.shields.io/badge/FastAPI-0.136-009688?logo=fastapi" alt="FastAPI">
<img src="https://img.shields.io/badge/SQLite-WAL-003B57?logo=sqlite" alt="SQLite">
<img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">

# AgentHub

**以「Agent 集群」为单位的协作工作台**

每个 Mission 封装一类重复性任务的稳定班底（Agent + Skill），用户进入模块后用自然语言反复执行任务、迭代班底，所有编辑都在模块内原地完成。

</div>

---

## 产品理念

**Agent 是任务的下属，不是用户的联系人。**

同一类角色（如「数据分析师」）在不同任务里需要不同的工作流和 Skill，把它抽象成跨场景稳定的「联系人」是错的。Agent 挂在 Mission 里，跟随任务变形。

**以 Agent 集群和任务沉淀为导向。** 用户进入一个 Mission，等于走进一个已搭建好的工程团队，而不是每次招兵买马。

**编辑即工作，不切后台。** 用自然语言修改 Agent 配置贯穿任务全过程，对话和配置共享同一个界面。

---

## 核心功能

### Mission 工作台
- 每个 Mission 包含一组 **Agent Team** + **Skill 工具集** + **知识库**
- 支持 `@Agent` 指定调度、多 Agent 群聊协作
- 自然语言迭代班底：对话中即可修改 Agent 配置
- 多 Run 并行：同一 Mission 可开启多个独立运行，互不干扰

### Agent Builder — 对话式创建 Agent
- 在对话中用自然语言创建/修改 Agent：「帮我创建一个财报分析专家」
- 创建后自动同步到 **Agent 库** 和 **Mission 右侧 Team 面板**
- 智能去重：同名 Agent 会提示用户使用已有还是创建新的
- 支持为新建 Agent 指定 LLM 后端和工具集

### Orchestrator 智能调度
- 7 级优先级路由：@mention → Agent 管理 → 工作流匹配 → 复杂度路由 → Skill 调用 → 系统查询 → 默认对话
- LLM 自动识别意图：简单聊天 / 复杂规划 / Agent 管理
- 复杂任务自动拆解为子任务，Planner Agent 并行调度执行

### Skill 市场
- 内置技能：`web_search` / `rag_retrieval` / `scan_vulnerabilities` / `file_converter`
- 支持 Fork / 发布 / 安装 / 版本回滚

### 多 LLM 后端
- **通义千问** (qwen-plus) — 默认后端
- **DeepSeek** (deepseek-chat) — 代码审查
- **OpenCode Zen** (deepseek-v4-flash-free) — 免费档
- 启动时自动健康检查，不可用后端自动停用

### 知识库
- 客户端解析 PDF / DOCX / XLSX（pdf.js + mammoth + SheetJS）
- RAG 检索注入对话上下文

---

## 内置 Agent 团队

| Agent | 角色 | 后端 |
|-------|------|------|
| `agent_builder` | 用自然语言创建/修改 Agent | tongyi |
| `planner` | 任务规划与拆解 | tongyi |
| `summarizer` | 对话总结与记忆压缩 | tongyi |
| `code_reviewer` | 代码审查与漏洞扫描 | deepseek |
| `product_manager` | 需求分析与 PRD 撰写 | tongyi |
| `opencode_coder` | 免费代码助手 | opencode |
| `opencode_bigpickle` | 实验性通用 Agent | opencode |

---

## 目标用户

| 用户 | 场景 |
|------|------|
| **效率型知识工作者** | 财报分析、竞品周报、文档翻译 — 把重复性脑力任务标准化 |
| **AI 工程师 / 极客** | 搭建自定义 Agent Team，深度定制工作流 |
| **团队 Lead** | 将工作流结合业务场景提效、沉淀团队知识 |

---

## 快速开始

```bash
# 1. 配置 API Key
cp .env.example .env   # 填入 DASHSCOPE_API_KEY / DEEPSEEK_API_KEY 等

# 2. 安装依赖
pip install fastapi uvicorn sqlalchemy python-dotenv dashscope httpx \
    langchain langchain-core langgraph langchain-chroma langchain-text-splitters \
    passlib python-jose bcrypt python-multipart loguru pyyaml

# 3. 启动（单一进程托管前后端）
cd AgentHub-1
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

打开 `http://localhost:8000`，注册账号后即可使用。

---

## 环境变量

| 变量 | 说明 |
|------|------|
| `DASHSCOPE_API_KEY` | 通义千问 API Key（必填） |
| `DEEPSEEK_API_KEY` | DeepSeek API Key（必填） |
| `OPENCODE_API_KEY` | OpenCode Zen API Key（可选，免费档） |
| `JWT_SECRET` | JWT 签名密钥 |
| `WEBSEARCH_API_KEY` | 网络搜索 API Key（可选） |

---

## 目录结构

```
AgentHub/
├── backend/
│   ├── app/api/              # auth / chat / agents / missions / skills / knowledge
│   ├── core/
│   │   └── orchestrator.py   # 核心调度器（2439 行，7 级路由 + 动态规划）
│   ├── agents/               # Agent 实现（planner / summarizer / custom_agent）
│   ├── utils/
│   │   └── manage_agent.py   # Agent 创建/修改/查询工具
│   ├── models/               # SQLAlchemy 数据模型
│   ├── llm/backends/         # tongyi / deepseek / opencode 后端
│   └── config/prompts/       # YAML 提示词配置
├── AgentHub-my flicker/
│   └── index.html            # 单页前端（8000+ 行）
├── custom_agents.yaml        # 内置 Agent 定义
└── .env                      # API Key 配置（不入库）
```

---

## License

MIT © 2025 [@zhangdifei03](https://github.com/zhangdifei03)
