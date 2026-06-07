# Agent 配置能力升级 PRD

## 1. 背景
当前 Agent 详情页已经展示 Prompt、Tools、记忆、规划、校验等板块，但后端 `CustomAgent` 模型仅持久化 `name / icon / description / system_prompt / llm_adapter / tools` 6 个字段。前端记忆/规划/校验 Tab 在 backend Agent 详情下被锁死为只读。

三个本质问题：
- **展示与能力不一致**：用户看到的策略卡，后端不能存、运行时不会读
- **Agent Builder 字段白名单偏窄**：无法把记忆 / 规划 / 校验需求转成结构化配置
- **运行时缺少配置消费层**：上下文装载、规划路由、结果校验都是全局写死，不是 per-Agent 可配置

---

## 2. 目标
为 Agent 提供 5 类可配置能力（**排除 Hooks**）：Prompt、Tools、记忆、规划、校验。

每一类同时支持：
- **表单修改**：详情页直接编辑保存
- **自然语言修改**：一句话生成结构化 Diff，确认后应用

---

## 3. 范围

### 3.1 本期纳入
- 数据模型扩展三个 JSON 字段：`memory_config` / `planning_config` / `validation_config`
- API Schema、PUT/POST 端点白名单同步扩展
- `manage_agent.create_agent` / `update_agent` 字段白名单扩展
- Agent 详情页 5 个 Tab 全部解锁可编辑
- 草稿 ↔ payload 双向映射
- Agent Builder Prompt 加入嵌套字段说明 + 示例
- NL Diff 解析从「Prompt + Tools 两类」扩展到「5 类」
- 保存后调用 `register_custom_agent` 立即重建实例

### 3.2 待澄清（沿用默认）
- 校验策略最终枚举 → **默认** `none / rules / llm_judge`
- 默认配置与 Mission 覆盖配置的优先级 → **默认** 详情页是唯一来源
- 老库字段如何升级 → **默认** 启动时自动 ALTER（SQLite 兼容）

---

## 4. 可行性结论总表

| 模块 | 子项 | 依据 |
|---|---|---|
| Prompt | 全文编辑保存 | PUT 已支持 `system_prompt`，重新注册已生效 |
| Prompt | NL 修改 Prompt | `parseEditIntent` 已部分支持，扩展即可 |
| Tools | 勾选启用 / 移除 | `tools[]` 已持久化 |
| Tools | NL 加 / 删 Tool | `parseEditIntent` 已支持加 Tool |
| Tools | 平台白名单校验 | 对照 `/api/skills` + MCP 注册表 |
| 记忆 | `memory_config` 字段持久化 | 加 JSON 字段 + schema |
| 记忆 | 不保留（空上下文） | 调用前清空 messages |
| 记忆 | 滑动窗口（最近 N 轮） | 调用前对 messages 切片 |
| 记忆 | 摘要压缩（超阈值后摘要） | 触发额外一次 LLM 调用 |
| 规划 | `planning_config` 字段持久化 | 加 JSON 字段 + schema |
| 规划 | 直接回答 | 已是默认链路 |
| 规划 | Plan-Execute | `_handle_plan_command` 已实现 |
| 规划 | ReAct | 依赖 `langchain >= 0.1.0` |
| 规划 | 复杂任务先确认 | 在路由入口加一个 confirm 状态 |
| 校验 | `validation_config` 字段持久化 | 加 JSON 字段 + schema |
| 校验 | 不校验（直通） | 默认链路 |
| 校验 | 规则校验（正则/JSON Schema） | 主回答后接一段同步检查 |
| 校验 | LLM Judge | 主回答后再调一次 LLM |
| 校验 | 自动重试 | 校验失败时回到主回答阶段循环（带 max_retries） |
| Builder | create / update 双工作流 | 工具已分开 |
| Builder | 嵌套 JSON 输出（5 类配置） | 升级 prompt + payload 校验 |
| Builder | 信息不足时追问 | prompt 加约束 |
| NL Diff | 5 类配置预览/确认 | 前端 `parseEditIntent` 扩展规则 |
| 详情页 | 解锁 5 Tab 表单 | 移除 `<fieldset disabled>` + 接 draft 写入 |
| 详情页 | 双向映射 | 现有映射函数增字段 |

---

## 5. 数据模型设计

在 `backend/models/custom_agent.py` 中新增 3 个 JSON 字段，允许为 NULL，旧数据视为 NULL = 走默认策略。

```python
memory_config     = Column(JSON, nullable=True, default=None)
planning_config   = Column(JSON, nullable=True, default=None)
validation_config = Column(JSON, nullable=True, default=None)
```

### 5.1 `memory_config` schema
```jsonc
{
  "strategy": "none | sliding_window | summary",
  "window_size": 10,                                // 仅 sliding_window 用
  "summary_prompt": "请用 100 字概括以下对话…",      // 仅 summary 用
  "summary_threshold": 4000                         // 仅 summary 用
}
```

### 5.2 `planning_config` schema
```jsonc
{
  "mode": "direct | react | plan_execute",
  "steps_template": "1. 拆解… 2. 调用… 3. 汇总…",   // 仅 plan_execute 可选
  "require_confirmation_for_complex_tasks": false
}
```

### 5.3 `validation_config` schema
```jsonc
{
  "strategy": "none | rules | llm_judge",
  "rules": [
    { "type": "regex", "pattern": "^.*$", "message": "格式不符" },
    { "type": "json_schema", "schema": { } }
  ],
  "judge_prompt": "请评估以下回答是否满足…",
  "max_retries": 1
}
```

---

## 6. 接口设计

### 6.1 REST 接口（`backend/app/api/agents.py`）
`POST /api/agents` 与 `PUT /api/agents/{agent_id}` 入参 `CustomAgentCreate` 扩展 3 个 `Optional[dict]` 字段。
PUT 端点把三个字段直接 setattr 到 db_agent，保存后调用 `orchestrator.register_custom_agent(db_agent)`。

### 6.2 Agent Builder 工具（`backend/utils/manage_agent.py`）
- 新增三个归一化函数（集中放在 `backend/utils/agent_config.py`）
- 每个函数对枚举值、参数取值范围做硬校验，非法值直接抛 `ValueError`
- `create_agent` / `update_agent` 在写库前调用归一化

### 6.3 GET 响应
`CustomAgent` schema 同步增加这 3 个字段。

---

## 7. 运行时实现策略

### 7.1 Prompt / Tools
保存后 `register_custom_agent(db_agent)` 重建 Agent 实例，下一次调用即生效。**已有能力，无需新增**。

### 7.2 记忆（调用 LLM 之前装载）
新增 `apply_memory_strategy(messages, memory_config) -> messages`：
- `none`：仅保留最后一条 user
- `sliding_window`：保留 `messages[-window_size*2:]`
- `summary`：当总 token 超过 `summary_threshold` 时，调用 LLM 生成摘要，把历史替换成一条 system 摘要

### 7.3 规划（在 orchestrator 路由入口按 Agent 配置分发）
读取目标 Agent 的 `planning_config.mode`：
- `direct`：当前默认链路
- `react`：调用 LangChain ReAct executor（缺依赖时 fallback 到 direct）
- `plan_execute`：复用 `_handle_plan_command`

`require_confirmation_for_complex_tasks`：在 `_classify_complexity == "complex"` 时多走一步「等用户确认」。

### 7.4 校验（在主回答之后）
新增 `apply_validation_strategy(answer, validation_config) -> final_answer`：
- `none`：直接返回
- `rules`：逐条匹配，全部通过返回；任一失败且 `retries_left > 0` 则回到主回答阶段
- `llm_judge`：把 `judge_prompt + answer` 喂给 LLM，要求输出 `{ pass: bool, reason: str }`；失败行为同上

---

## 8. Agent Builder 升级要点

更新 `_build_agent_management_prompt` 字段白名单（9 → 12），加入 3 类嵌套字段示例：

```
memory_config 示例：
  { "strategy": "sliding_window", "window_size": 10 }
  { "strategy": "summary", "summary_threshold": 4000, "summary_prompt": "..." }

planning_config 示例：
  { "mode": "react" }
  { "mode": "plan_execute", "steps_template": "..." }

validation_config 示例：
  { "strategy": "llm_judge", "judge_prompt": "...", "max_retries": 1 }
```

约束：
- 信息不足必须先反问，禁止编造
- 输出必须是合法 JSON 对象（包在 ```json fenced block 里）
- 嵌套字段为可选，未指明的不写入

---

## 9. NL Diff 升级要点

前端 `parseEditIntent` 扩展为识别 5 类意图：

| 意图类别 | 例句 | 输出 patch |
|---|---|---|
| prompt | "把系统提示词改成…" | `{ systemPrompt: "..." }` |
| tools | "给 X 加上 web_search 技能" | `{ skills: [...] }` |
| memory | "把记忆改成滑动窗口，窗口轮数 20" | `{ memoryConfig: { strategy:"sliding_window", window_size:20 } }` |
| planning | "改成 ReAct 模式" | `{ planningConfig: { mode:"react" } }` |
| validation | "校验失败最多重试 2 次" | `{ validationConfig: { max_retries: 2 } }` |

走原有的 `openModalAgentDiff` 弹窗确认后再写入 draft。

---

## 10. 验收标准
- 用户可在详情页修改并保存 Prompt / Tools / 记忆 / 规划 / 校验
- 保存后刷新页面，配置仍然存在
- 用户可通过自然语言修改以上 5 类配置
- Agent 后续运行按新配置真实生效：
  - 记忆：日志可见 messages 被裁剪 / 摘要
  - 规划：日志可见 ReAct / Plan-Execute 分支命中
  - 校验：日志可见失败重试或 Judge 评分
- 非法配置（枚举值错、缺必填、参数越界）API 返回 4xx 并附原因
- Agent Builder 输出的 JSON 能被 `manage_agent` 工具直接消费

---

## 11. 风险与注意事项
- 摘要压缩、LLM Judge、自动重试都会增加 LLM 调用次数；前端在保存时给出提示
- 前端可选模型必须与后端 `VALID_ADAPTERS = {"tongyi", "deepseek"}` 对齐
- ReAct 依赖 `langchain>=0.1.0`，缺依赖时 fallback 到 direct
- 嵌套 JSON 字段对 qwen-long 是个挑战，Builder prompt 必须给完整示例
