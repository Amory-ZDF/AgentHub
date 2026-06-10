<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688?logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-WAL-003B57?logo=sqlite)
![Status](https://img.shields.io/badge/Status-WIP-orange)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

# AgentHub

**以「Agent 集群」为单位的协作工作台**

每个 Mission 封装一类重复性任务的稳定班底（Agent + Skill），用户进入模块后用自然语言反复执行任务、迭代班底，所有编辑都在模块内原地完成。

</div>

---

## 产品理念

**Agent 是任务的下属，不是用户的联系人。** 同一类角色（如「数据分析师」）在不同任务里需要不同的工作流和 Skill。Agent 挂在 Mission 里，跟随任务变形。

**以 Agent 集群和任务沉淀为导向。** 用户进入一个 Mission，等于走进一个已搭建好的工程团队，而不是每次招兵买马。

**编辑即工作，不切后台。** 用自然语言修改 Agent 配置贯穿任务全过程，对话和配置共享同一个界面。

---

## 核心功能

### Mission 工作台

- 每个 Mission 包含一组 **Agent Team** + **Skill 工具集** + **知识库**
- 支持 `@Agent` 指定调度、多 Agent 群聊协作
- 自然语言迭代班底：对话中即可修改 Agent 配置
- 多 Run 并行：同一 Mission 可开启多个独立运行，互不干扰

### 可配置的大模型

- 支持接入**通义千问 / DeepSeek / OpenCode** 等兼容 OpenAI 协议的模型
- 用户可为每个 Agent 独立选择后端模型
- 启动时自动健康检查，不可用后端自动停用
- 通过 `.env` 配置 API Key，支持扩展更多模型

### 可配置的 Skill 工具集

- 内置技能：`web_search` / `rag_retrieval` / `scan_vulnerabilities` / `file_converter`
- 支持用户自建 Skill：编写 Markdown 描述即可注册为可调用技能
- Skill 市场：Fork / 发布 / 安装 / 版本回滚
- 创建 Agent 时可自由组合分配 Skill

### Agent Builder — 对话式创建 Agent

- 在对话中用自然语言创建/修改 Agent：「帮我创建一个财报分析专家」
- 创建后自动同步到 **Agent 库** 和 **Mission 右侧 Team 面板**
- 智能去重：同名 Agent 会提示用户使用已有还是创建新的
- 新建 Agent 可指定后端模型和工具集

### Orchestrator 智能调度

- **7 级优先级路由**：@mention → Agent 管理 → 工作流匹配 → 复杂度路由 → Skill 调用 → 系统查询 → 默认对话
- LLM 自动识别意图：简单聊天 / 复杂规划 / Agent 管理
- 复杂任务自动拆解为子任务，Planner Agent 并行调度执行

### 知识库（基础支持）

- 客户端解析 PDF / DOCX / XLSX（pdf.js + mammoth + SheetJS）
- RAG 检索注入对话上下文

---

## 迭代计划

### 一期（已完成 ✅）

- Mission 工作台：创建 Mission、多 Agent Team、对话交互
- 7 级 Orchestrator 智能路由
- Agent Builder：对话式创建/修改 Agent
- Skill 市场：内置 Skill + 用户自建
- 多模型接入：Tongyi / DeepSeek / OpenCode
- JWT 注册登录
- 快速开始部署（单一 FastAPI 进程）

### 二期（规划中 🚧）

- Agent 详情页完整编辑（记忆策略、规划模式、校验方式）
- Skill 的 AI 创建与修改
- 对话中文件输入输出增强（PDF / XLSX / 图片）
- 移动端适配
- 知识库完整功能（上传、管理、绑定 Mission）

### 三期（计划中 📋）

- Agent 市场 / 模板市场
- 第三方 Agent 平台接入
- 产品测评与数据看板
- 任务执行 Trace / Log / Cost 可观测性

---

## 快速开始

```bash
# 1. 配置 API Key
cp .env.example .env   # 填入 DASHSCOPE_API_KEY / DEEPSEEK_API_KEY 等

# 2. 安装依赖
pip install fastapi uvicorn sqlalchemy python-dotenv dashscope httpx \
    langchain langchain-core langgraph langchain-chroma langchain-text-splitters \
    passlib python-jose bcrypt python-multipart loguru pyyaml

# 3. 启动
cd AgentHub-1
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

打开 `http://localhost:8000`

---

## 环境变量

| 变量 | 说明 |
|------|------|
| `DASHSCOPE_API_KEY` | 通义千问 API Key（必填） |
| `DEEPSEEK_API_KEY` | DeepSeek API Key（必填） |
| `OPENCODE_API_KEY` | OpenCode Zen API Key（可选） |
| `JWT_SECRET` | JWT 签名密钥 |
| `WEBSEARCH_API_KEY` | 网络搜索 API Key（可选） |

---

## 目录结构

```
AgentHub/
├── backend/
│   ├── app/api/              # auth / chat / agents / missions / skills / knowledge
│   ├── core/
│   │   └── orchestrator.py   # 核心调度器（7 级路由 + 动态规划）
│   ├── agents/               # Agent 实现
│   ├── utils/
│   │   └── manage_agent.py   # Agent 创建/修改/查询工具
│   ├── models/               # 数据模型
│   ├── llm/backends/         # LLM 后端适配
│   └── config/prompts/       # YAML 提示词
├── AgentHub-my flicker/
│   └── index.html            # 单页前端
├── custom_agents.yaml        # 内置 Agent 定义
└── .env                      # API Key（不入库）
```

---

## License

MIT © 2025 [@zhangdifei03](https://github.com/zhangdifei03)
