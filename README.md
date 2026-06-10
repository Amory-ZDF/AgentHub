<div align="center">

# AgentHub

**多 Agent 协作工作台 — 用自然语言管理 Agent 团队，完成复杂任务**

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![SQLite](https://img.shields.io/badge/SQLite-WAL-003B57?logo=sqlite)](https://www.sqlite.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

</div>

---

## 简介

AgentHub 是一个面向重复性任务自动化的多 Agent 协作平台。将 **Agent + Skill + 知识库** 封装为 Mission 模块，用户用自然语言即可触发任务、管理 Agent 团队。

## 核心特性

- **Mission 班底**：每个 Mission 包含一组 Agent Team，支持自然语言调度和配置
- **Agent Builder**：用自然语言创建/修改 Agent，自动同步到 Team 和 Agent 库
- **Skill 市场**：内置 web_search、rag_retrieval、file_converter 等工具技能
- **多 LLM 后端**：通义千问 / DeepSeek / OpenCode Zen — 自动健康检查
- **知识库**：支持 PDF/DOCX/XLSX 客户端解析（pdf.js + mammoth + SheetJS）
- **JWT 鉴权**：邮箱注册登录，bcrypt 哈希
- **零依赖部署**：SQLite + 单一 FastAPI 进程托管前后端

## 技术栈

| 层 | 技术 |
|---|------|
| 后端框架 | FastAPI + Uvicorn |
| 数据库 | SQLite (better-sqlite3 / SQLAlchemy) |
| LLM 调度 | LangGraph + 自研 Orchestrator |
| 前端 | 原生 HTML/JS + Tailwind CSS CDN |
| 文档解析 | pdf.js / mammoth.js / SheetJS |

## 内置 Agent

| Agent | 职责 | 后端 |
|-------|------|------|
| `planner` | 任务规划与拆解 | tongyi |
| `summarizer` | 对话总结与压缩 | tongyi |
| `code_reviewer` | 代码审查与漏洞扫描 | deepseek |
| `product_manager` | 需求分析与 PRD 撰写 | tongyi |
| `agent_builder` | 用自然语言创建/修改 Agent | tongyi |
| `opencode_coder` | 免费代码助手 | opencode |
| `opencode_bigpickle` | 实验性通用 Agent | opencode |

## 快速开始

### 环境要求
- Python ≥ 3.11

### 安装与启动

```bash
# 1. 配置 API Key
cp .env.example .env
# 编辑 .env，填入 DASHSCOPE_API_KEY / DEEPSEEK_API_KEY

# 2. 安装依赖
pip install fastapi uvicorn sqlalchemy python-dotenv dashscope httpx \
    langchain langchain-core langgraph langchain-chroma langchain-text-splitters \
    passlib python-jose bcrypt python-multipart loguru pyyaml

# 3. 启动
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

打开 `http://localhost:8000`

> 首次启动自动建表，写入种子技能。前端由 FastAPI 直接托管。

## 目录结构

```
AgentHub/
├── backend/
│   ├── app/api/           # auth / chat / agents / conversations / skills / knowledge
│   ├── core/
│   │   └── orchestrator.py   # 核心调度器：路由 → Agent → 工具
│   ├── agents/            # Agent 实现（planner / summarizer / custom_agent）
│   ├── utils/             # manage_agent / web_search / file_converter
│   ├── models/            # SQLAlchemy 模型
│   ├── llm/               # tongyi / deepseek / opencode 后端
│   └── config/prompts/    # YAML 提示词配置
├── AgentHub-my flicker/
│   └── index.html         # 单页前端
├── custom_agents.yaml     # 内置 Agent 定义
└── .env                   # API Key 配置
```

## 配置说明

| 环境变量 | 说明 |
|----------|------|
| `DASHSCOPE_API_KEY` | 通义千问 API Key |
| `DEEPSEEK_API_KEY` | DeepSeek API Key |
| `OPENCODE_API_KEY` | OpenCode Zen API Key（可选） |
| `JWT_SECRET` | JWT 签名密钥 |
| `WEBSEARCH_API_KEY` | 网络搜索 API Key |

## License

MIT © 2025 [@zhangdifei03](https://github.com/zhangdifei03)
