# AgentHub — 多 Agent 协作平台 · PRD

## 目录

1. 产品概述

2. 目标用户/竞品对比

3. 核心功能规划

4. 用户旅程

5. 需求详情

6. Agent 详情设计

7. AI协作沉淀



## 1\. 产品概述

### 1\.1 一句话定义

**AgentHub 是以"Agent 集群"为单位的协作工作台，目标是沉淀可复用的团队和流程。让Agent不止能完成任务，更需要能完成好任务。**



### 1\.2 产品概念

- **当下大模型/Agent团队都在从模型/工程层面去实现 Self\-improvement Agent，AgentHub这个产品从产品角度去最大化的实现 Improvement Agent。**

- **每个 Mission 封装一类重复性任务的稳定Team（Agent \+ Skill），用户进入模块后用自然语言反复执行任务、迭代班底，所有编辑都在模块内原地完成。**

- **Agent 是基础框架\+任务沉淀，不是用户的联系人。** 同一类工作角色（如"数据分析师"）在不同任务里需要不同的工作流程、Skill 与上下文，把它抽象成跨场景稳定的"联系人"是错误的。Agent 必须挂在任务里。

- **以 Agent 集群和任务沉淀为导向，不以单次任务为导向。** 用户进入一个 Mission，等于走进一个根据需求搭建好的工程/产品团队，而不是每次招兵买马。

- **编辑即工作，不切后台。** 自然语言修改 Agent 的能力贯穿任务全过程；编辑动作和工作动作共享同一个界面。



## 2\. 目标用户与场景

### 2\.1 目标用户

|用户类型|核心诉求|画像|核心痛点|
|---|---|---|---|
|**效率型知识工作者**|把重复性脑力任务标准化，自动化|分析师、研究员、运营、内容创作者|**需要在复杂场景下解决复杂任务**<br>|
|**AI 工程师 / 极客**|搭建自己的 Agent Team，深度定制化的解决问题|工程师、创业者、技术博主||
|**团队 Lead**|在复杂业务场景下，将工作流结合业务场景提效|产品经理、市场负责人||

### 2\.2 高频使用场景

|场景|类型|频率|偏好路径|
|---|---|---|---|
|财报季分析多家公司，并根据模板输出PPT|定制复杂任务|周/月|Team模板 \+ 个性化沉淀|
|PR 代码审查|非定制任务|日|单一Agent/Team模版|
|竞品周报|定制复杂任务|周|Team模板 \+ 个性化沉淀|
|临时读 PDF / 翻译文档|非定制简单任务|日|Quick Run / 单一Agent|
|自定义垂直领域工作流|定制复杂任务|一次性投入|AI 引导建模块 \+ Skill 自建|
|根据业务场撰写PRD|定制简单任务|周|单一Agent\+知识库|

### 2\.3 竞品分析和对比

|产品|核心范式|AgentHub 差异|
|---|---|---|
|Openclaw/Hermes接入飞书/微信|Agent = IM 联系人<br>|AgentHub：Agent 是 Mission 的下属，跟随任务变形|
|Coze|工作流编排（节点连线）|AgentHub：保留对话语义，节点心智隐藏在班底卡片背后|
|Claude\.ai / ChatGPT|单 Agent 对话|AgentHub：多 Agent 在同一 Mission 协作，自然语言迭代班底|
|Cursor / Claude Code|代码场景的 AI 协作|AgentHub：通用任务工作台，且强调班底的长期复用|



## 3\. 核心功能概述

### 3\.1 迭代规划

- **AgentHub一期：**

    - **核心目标**：一期因时间原因，需核心流程跑通，核心功能点完成开发

    - **验收标准：**核心功能前后端数据库打通，功能完善，常规问题输出效果合理

- **AgentHub二期：**

    - **核心目标：**将一期没能完成的P1功能和P0功能点中没能完成开发的功能完成开发，上线测试

    - **验收标准：**已经是一个完整，可发布的产品，各个功能点完善，后端工程链路完整

- **AgentHub三期**：

    - **核心目标**：搭建产品测评和数据看板体系，完善数据埋点机制，根据数据看板优化输出效果，并且对用户测试反馈badcase进行归因迭代

    - **验收标准**：后端可用数据看板体系，产品评测体系，为后续工程迭代提供量化指标

- **AgentHub四期：**

    - **核心目标**：解决数据安全，发布合规审核问题

    - **验收标准**：可以正式上线使用，不存在法律风险，逐步优化用户体验



### 3\.2 核心功能概述

|核心功能|优先级|描述|迭代规划|
|---|---|---|---|
|多AgentIM交互式协作|**P0**<br>|多Agent交互，多Skill交互|一期核心目标|
|Orchestrator:任务协调|**P0**|包括意图识别，任务调度，汇总/核验结果|一期核心目标|
|多Agent接入:|**P0**|Opencode\+codex|一期核心目标|
|对话式创建/修改Agent/Skill|**P0**<br>|使用Agent新增/修改Agent<br>使用Skill\-creater创建skill|一期进行Agent新建和修改部分内容的开发<br>完整开发Skill创建和修改功能开发<br>二期完成完整Agent修改开发|
|移动端发布|P1|移动端定位为任务协作/监控|二期核心目标|
|支持知识库|P1|引入知识库，使协作效果更好|二期核心目标|
|文档支持|P1|对话中支持不同文件形式输入输出|二期核心目标|

### 3\.1 实体关系



## 4\. 用户核心交互流

### 4\.1 新用户首次使用（onboarding）

```Plain Text
首次登录
  ↓
路径分支：
  ① 选模板 → 班底就位 → 立即执行任务
  ② AI 引导 → 描述需求 → 班底提案 → 接受 → 立即执行
  ③ Quick Run → 直接对话 → 跑完后引导沉淀
  ↓
首次任务完成
  ↓
发现某个 Agent 输出不理想/需要其他特定要求：
  - 在对话框说："@PPT-Writer 我需要根据公司PPT模版生成PPT"
  - 弹出 diff 预览 → Apply
  
```



### 4\.2 老用户日常工作流

```Plain Text
打开应用 → 看到熟悉的 Mission 列表
  ↓
点击 Mission（如"财报分析"）
  ↓
进入工作台 → 班底已就位
  ↓
直接在底部输入框输入任务描述 /（如需要）分离不同任务 [+ New Run] 
  ↓
对话流展开，Agent 协作产出
  ↓
（可选）发现某个 Agent 输出不理想：
  - 在对话框对 Coordinator 说："让数据分析师改用 Tufte 风格"
  - 弹出 diff 预览 → Apply
  - 当前 Run 不受影响（已快照），下个 Run 生效
  ↓
（可选）需要多个 Agent 并行讨论：
  - 在对话框 @数据分析师 @报告撰写师，让两人对同一份数据给出不同视角
  - 群聊模式开启，两个 Agent 依次回复
  ↓
任务完成
```



### 4\.3 班底沉淀路径

```Plain Text
Quick Run（试水）
  ↓ "Save as Mission"
Mission（v1 班底）
  ↓ 用 N 次后自然语言迭代
Mission（v2 班底）
  ↓ "Save as Template"（私有模板，P1）
个人模板库
  ↓ "Publish"（公开，P2）
社区模板市场
```

## 5\. 需求详情

|页面|UI设计图|功能点|迭代规划|
|---|---|---|---|
|Mission 主页/登陆首页|![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NGE5ZDBmMDFmZGIwMDg1ZjIzOTNkMzdiMmNlZDllOTlfYTQ5ODFiMGFmMTM5YzU3MzM3NzdlNDkyMDZiZWZkYWVfSUQ6NzY0ODY0MjgzOTU1NDgzNzc0Ml8xNzgxMDIyMTc3OjE3ODExMDg1NzdfVjM)<br>|功能点排列从左至右，从上至下<br>左侧Tab栏：<br>- New MIssion/创建Mission按钮：点击进入新建mission弹窗<br>- Quick Run按钮：点击进入Quick Run界面<br>- Mission下，我的任务子页面，点击进入mission详情页<br>- Agent按钮：点击进入Agent库界面<br>- Tools按钮：点击进入Tools库界面<br>- 知识库按钮：点击进入知识库界面<br>- Setting：点击进入设置界面<br>- 账户：点击进入登陆/注册界面<br>中间任务标题区：<br>- 创建Mission：点击进入新建mission弹窗<br>- Quick Run按钮：点击进入Quick Run界面<br>我的任务区域：<br>- 任务卡片：点击进入Mission详情区<br>- 创建新任务：点击进入新建mission弹窗<br>右侧新人引导区：<br>- 从模版创建：点击跳转Agentmarket界面<br>- 让AI帮我搭建：点击进入新建mission弹窗<br>- 先做一次Quick Run：点击进入Quick Run界面|一期完成|
|新建mission弹窗|![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZmJlZTk0ZmIxOTk5NzdjZDVlZWFjMmQ1ZmE0MDU1OWNfMGE3Yzc1YTk3ZmQzNGZkZTIxZWY4Nzk3OTQ0NDhiOTNfSUQ6NzY0ODY0OTY3MjM2NTY4OTgwNl8xNzgxMDIyMTc3OjE3ODExMDg1NzdfVjM)<br>|- 任务名称：必填字段<br>- 任务描述：选填字段<br>    - orchestrator根据用户描述创建合理Team<br>- 点击创建进入Mission详情页|一期完成|
|Quick Run|![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZTMwOWZkMDdhYzlhY2Y1NjQ4MzZhYmFjNmIxYzMwYTVfYzJmNmZmMjA2YzA0NGUwOGUyZTA3NDNiNTU2ZjY1MGFfSUQ6NzY0ODY1MDIzMDM1MDY3ODk4NV8xNzgxMDIyMTc3OjE3ODExMDg1NzdfVjM)<br>|- 对话框：用户输入问题<br>    - 调用Orchestrator指派合理Agent回答<br>- 上方检索框：搜索对应记录<br>- 右上方保存为mission：记忆对话轮数，点击保存为Mission<br>- 保存为Mission后进入Mission详情页|一期完成|
|Mission详情页|![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NjMyYWUxMmYyMTZmZGEwZmIxZmI4N2NkYzhiY2Y3MzlfZjdkYzE0ODQ1YmQyMDU4Y2UxOGJjODIxYTEyNzc0MDlfSUQ6NzY0OTAzMjI5NjEzMzYxMDczN18xNzgxMDIyMTc3OjE3ODExMDg1NzdfVjM)<br>![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NDRjMjliNThhNjEzYWJlY2RjYzNjMmY4YjI2ZmQzYzBfMjI4MTcyMTg3YTBlMTBkZjg1ZTExMmU4YzZmMWQ0ZTNfSUQ6NzY0ODY1MTkwNjgxMzc5MTE4Ml8xNzgxMDIyMTc3OjE3ODExMDg1NzdfVjM)<br><br><br><br>|对话区域<br>- 对话框中输入问题<br>    - @指定Agent：指定Agent实施任务<br>    - \#指定Agent/Skill：对指定Agent/Skill进行修改<br>    - 当用户输入@/\#时，自动跳出下拉选择框<br>- 对话框下方：<br>    - 回形针按钮跳出文件预览界面，用户可添加文件<br>    - @和编辑键，同@和\#<br>    - 话筒键：调用语言输入<br>中间预览框区域：<br>- 预览编辑代码<br>    - 下载：下载支持类型文件<br>    - 分享：将mission分享给其他用户<br>右侧工具区：<br>- Team：<br>    - 添加Agent跳出弹窗加入新Agent<br>    - 点击卡片进入Agent详情页<br>    - 下方切换模型<br>- Tools：<br>    - Agent所调用的Skill和MCP<br>    - 点击进入Agent详情页<br>    - 下发切换模型<br>- 知识库：<br>    - 绑定知识库<br>- 设置：<br>    - Mission名称<br>    - 描述|一期支持docx，txt格式文件<br>二期支持pdf，md，xlsx，png等格式文件<br><br>一期不支持语言输入<br>计划二期支持<br><br>预览编辑代码/PPT预计二期上线<br><br>一期未开发下载和分享功能<br><br>一期未开发知识库功能<br><br>|
|Agent 界面|![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZmE2YTBhZDAzNDZhNmI0YzNmNGRjOWI2YjU5OWEzM2FfMjhlNzk4N2UwNzkyZjhlZDliY2I3MTQ0MzI1NTcxZjZfSUQ6NzY0OTAzNzI4MDk4Nzg5MjY3NF8xNzgxMDIyMTc3OjE3ODExMDg1NzdfVjM)<br>![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NjA1MGE4NmYzODU5NDE1ZmZiZWJhNzc2MTY0YmQ1NmVfYzY4ZWY0MGYyOTI4ZTUyODFmODdkZGM4MTdiODg1OTFfSUQ6NzY0OTAzNzM2NzcxMzkyNjExOF8xNzgxMDIyMTc3OjE3ODExMDg1NzdfVjM)<br>|Agent库分为两种类型：<br>1. Team：包括多个子Agent<br>2. Agent：单一子Agent<br>当一个Team/Agent关联多个mission时：<br>- 在Mission页面修改Team/Agent时，其他Mission中的这个Team/Agent保持不变，更改后的Team/Agent自动保存为新的版本保存在库中<br>- 在Agent详情页面中更改Team/Agent时，所有Mission中的该Team/Agent统一修改<br><br>Agent库分为我的库和Agent市场<br>- 上方搜索框可搜索相关的Agent<br>- 点击Agent卡片进入Agent详情页<br>||
|Agent详情页|![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YmE0MTYzOTEyN2Y5ZTU3NDdiMDQ3YmNhYzllYjY4ZTRfMzFiMzZiNDNjZTI4YzNkOWEzNmFjZDNhOWNhOTU4Y2VfSUQ6NzY0OTA0MDMwMzM4MjQwMDE3OF8xNzgxMDIyMTc3OjE3ODExMDg1NzdfVjM)<br>![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZWIxZTBlMzEzZjAwYmQ2MWFlM2RkMDFkYjMwNjc4MGZfY2Y2OWNiMTAyMTY0ZGIxMGFkNDcxZDZlNTJhZDA4ZDVfSUQ6NzY0OTA0MDM0MjE1NDU0NjM4M18xNzgxMDIyMTc3OjE3ODExMDg1NzdfVjM)<br>![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZjlmMTMxNjg4Mzg5MWE0NTE4ZDc3MmVhNDUyMjI3MDFfNTEyNTI2OGM4NWNmMzVmMmY0MzA3MDI1NmE5MmM0YzFfSUQ6NzY0OTA0MDM4MjY4NDE1NTA4NF8xNzgxMDIyMTc3OjE3ODExMDg1NzdfVjM)<br>![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MmNhMmMyMjYyMzc0OThhNmIzNmFkMmI5MmY3N2Q1MGJfMDA5ZWE3NGFmMmIyNTEzMzQxMjkwNGEwY2U1NzEwYTNfSUQ6NzY0OTA0MDQ0NDIxNDc1ODY0MV8xNzgxMDIyMTc3OjE3ODExMDg1NzdfVjM)<br>![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MjYwNzE1OTAwOGZjMjVhNjMwMzU0MzM2MjM0ZDA1NjlfYmJiNmM0YTYyODIwOGQxMGE1MjA0OGY5YjkwNWEyNGFfSUQ6NzY0OTA0MDQ5MDgxNzYwNDU0Nl8xNzgxMDIyMTc3OjE3ODExMDg1NzdfVjM)<br>|右侧输入框自然语言更改Agent<br>- 概览：<br>    - 名称 角色描述 图标 模型<br>- System Prompt：<br>    - 输入更改<br>- Tools：<br>    - 添加Skills或者MCP<br>- 记忆<br>    - 更改记忆策略<br>    - 更改窗口轮数<br>- 规划<br>    - 选择规划：直接回答/Plan\-Excute/ReAct<br>- 校验：<br>    - 选择校验方式：不校验/大模型校验/规则校验<br>- Hooks：添加Hooks<br>- Agents（仅有Team有）：<br>    - Team下的Agent<br>- Mission：这个Agent关联的Mission|一期不支持更改以及，规划，校验，Hooks<br>|
|Tools详情页|![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NDIyNDI1NDljY2ZlMjZjZjI0OTZlZTUyZDNiZmE5MjhfMzI3YzYxNjkxNjc4OTE1YjkzNTZkYmFiNjFhYTA4NzRfSUQ6NzY0OTI5MTgxNjkwMjM2NDM1NF8xNzgxMDIyMTc3OjE3ODExMDg1NzdfVjM)<br>![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NWMxZGM4NDBjMGRlZTVlMGViNDU3ZGIyOTQwMDUxMzdfMzgyMGIzZjBjZTIzOTk0NWU0Zjg1YjY2N2I3ZjliMTBfSUQ6NzY0OTA0ODY5NDUxOTc5NDkwMl8xNzgxMDIyMTc3OjE3ODExMDg1NzdfVjM)<br>![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MDI3ZjIzYzIyODg5Mzc4MWJjYWI1ZDc0MjFiOTAwZjZfOWMxYjAzZDlhYjllMTM4NTUwODQxYzlkMGRkZmViOWRfSUQ6NzY0OTI5Mjc0NDkzODM1OTczOV8xNzgxMDIyMTc3OjE3ODExMDg1NzdfVjM)<br>![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MTg2MjgxOTJhMWM3YThjZGYzYmU4ODExMGY2OTE3MzRfODc3NWY4NGZkOTc3OTU5Njg5NzJiY2NhMTAwODBkNmZfSUQ6NzY0OTI5MzUwODI3NDM3NTYyMF8xNzgxMDIyMTc3OjE3ODExMDg1NzdfVjM)<br>![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZTc0N2YyYTI0NTdlMjMwZTdlY2E0ZDQ3NTg1NTNmY2FfOTdkODQ1MDA5NjI0YjIzYWQ5N2UyZWU2ZjYyZWY1ODhfSUQ6NzY0OTI5MzU2NzQwNzkzNDY0OV8xNzgxMDIyMTc3OjE3ODExMDg1NzdfVjM)<br>![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ODAzNWU2NjQ5N2UwNzEwOTNhMzNiMDA4ZWJhM2ZmNGVfNGVhYTZjNmM2NTYwZmZmZWNhMzAzN2ZmMjVlYzEwZjdfSUQ6NzY0OTI5MzYyMzYzNjQxMzY0NF8xNzgxMDIyMTc3OjE3ODExMDg1NzdfVjM)<br>|区分Skill和MCP<br>区分我的Skill库和Skill市场<br>Skill市场上的Skill可存入自己的Skill库<br>- 右侧创建Skill：<br>    - 名称，描述，图标，Prompt<br>Skill分为私有和内置Skill<br>- 内置Skill目前不支持修改细节<br>- 私有Skill支持修改/发布/删除/撤回发布<br>- Skill详情页<br>    - 概览：名称，描述，分类<br>    - Prompt：Skill的Prompt描述<br>    - 文档：完整的Skill\.md文档<br>    - 使用情况：显示在哪些mission中该Skill被使用<br>    - 版本：支持回滚版本，查看diff视图<br><br>|一期Skill目前不支持AI修改细节，仅仅支持手动修改<br>二期开发|
|知识库|![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MThjY2QwNjVjYzIyMzE5NTg4Y2UxMzEzOWFjNTIxZmVfZmI0MDNiODE0MzVjYjc3YWM0Y2JjMTlhMTk4ZGMxYTRfSUQ6NzY0OTA1MjAwMjIzNTcxNDc5N18xNzgxMDIyMTc3OjE3ODExMDg1NzdfVjM)<br>|添加知识库文件<br>|一期暂时不支持知识库|
|设置|![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NTc1ODI1MDQ0ZjgyNGExNGRlYTJkODdkMDJiZmU4NjJfYmE2NTA5NzA0MTM4ODQzZjI3MDAxM2MwYzk3ZDljMDRfSUQ6NzY0OTA1MjA1MTM2MzYzMDA0Nl8xNzgxMDIyMTc3OjE3ODExMDg1NzdfVjM)<br>|- 接入其他模型<br>- 通知消息<br>|一期不支持接入其他模型|

## Agent详情设计

### 6\.1 Agent角色与工作流设计

本产品涉及1个核心Agent，其他Agent全部由此Agent创建，或从其他Agent平台接入，统一由orchestrator调用，设计范式如下

#### **6\.1\.1 Agent\-Builder**

- 核心故事线：

```Plain Text
用户在 Mission 中输入消息
  │
  ▼
Orchestrator.get_chat_response()
  │
  ├─ ① _classify_complexity() → LLM 判断意图 → "agent_management"
  │    触发条件：创建/修改/删除/查询 Agent、"帮我做一个 xxx Agent" 等
  │
  └─ ② _handle_agent_management_request()
       │
       ├─ 解析 current_user_id（JWT → conversation 查库）
       ├─ 设置 manage_agent._caller_ctx（注入上下文）
       ├─ _build_agent_management_prompt() → 生成英文 JSON 指令
       ├─ TongyiBackend.chat() 直接调用 LLM（不经过 ReAct）
       ├─ 解析 LLM 响应 → 提取 JSON
       │
       └─ ③ 执行 manage_agent 工具
            ├─ action=list  → list_agents()
            ├─ action=update → update_agent()
            └─ action=create → create_agent()
                 ├─ 写入 custom_agents 表（Agent 库）
                 ├─ Orchestrator.register_custom_agent()（运行时注册）
                 └─ _add_agent_to_mission_squad()（右侧 Team 同步）

```

需求详情细节：

- 上下文信息

```Plain Text

┌─────────────────┬──────────────────────────────┬───────────────────────────────────────────────────┐
│      信息       │             来源             │                      示例值                       │
├─────────────────┼──────────────────────────────┼───────────────────────────────────────────────────┤
│ conversation_id │ 当前 Mission                 │ "5"                                               │
├─────────────────┼──────────────────────────────┼───────────────────────────────────────────────────┤
│ current_user_id │ JWT 解析 + DB 反查           │ 2                                                 │
├─────────────────┼──────────────────────────────┼───────────────────────────────────────────────────┤
│ user_request    │ 用户最新消息                 │ "帮我创建一个财报分析 Agent"                      │
├─────────────────┼──────────────────────────────┼───────────────────────────────────────────────────┤
│ existing_names  │ DB 实时查询 custom_agents 表 │ "数据分析助手, 代码审查专家"                      │
├─────────────────┼──────────────────────────────┼───────────────────────────────────────────────────┤
│ 可用后端        │ self.llm_backends.keys()     │ "tongyi, deepseek, opencode"                      │
├─────────────────┼──────────────────────────────┼───────────────────────────────────────────────────┤
│ 可分配 tools    │ 硬编码                       │ "web_search, rag_retrieval, scan_vulnerabilities" │
└─────────────────┴──────────────────────────────┴───────────────────────────────────────────────────┘

```

- 模型能力支持

无需额外模型能力支持

- 工具清单

```Plain Text
manage_agent.create_agent      ← 创建 Agent（name + system_prompt 必填）
manage_agent.update_agent      ← 修改 Agent（agent_id 或 target_name 定位）
manage_agent.list_agents       ← 列出当前用户所有 Agent

三个工具通过 _register_builtin_tool_skills() 加载为 LangChain Tool，位于 backend/utils/manage_agent.py：

┌──────────────┬──────────────────────────────────┬────────────────────────────────────────────────────┬───────────────────────────────────────────────────────────────────┐
│     工具     │               输入               │                        输出                        │                             关键校验                              │
├──────────────┼──────────────────────────────────┼────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
│ create_agent │ JSON 字符串 → _extract_payload   │ {"status":"success","agent_id":"custom_xxx",...}   │ name/system_prompt 必填；llm_adapter 白名单；_build_create_name   │
│              │ 解析                             │                                                    │ 去重抛错                                                          │
├──────────────┼──────────────────────────────────┼────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
│ update_agent │ JSON 字符串                      │ {"status":"success","agent_id":"...","name":"..."} │ agent_id 或 target_name 定位；仅更新显式传入的字段                │
├──────────────┼──────────────────────────────────┼────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
│ list_agents  │ JSON 字符串（含 user_id）        │ {"status":"success","agents":[...]}                │ 按 user_id 过滤，仅返回 is_active=True                            │
└──────────────┴──────────────────────────────────┴────────────────────────────────────────────────────┴───────────────────────────────────────────────────────────────────┘

```

- 输出格式要求

```JavaScript
LLM 被要求输出 纯 JSON（无 markdown 包裹）：

创建 Agent：
{
  "action": "create",
  "conversation_id": 5,
  "current_user_id": 2,
  "name": "财报分析专家",
  "description": "分析上市公司财报，提取关键财务指标",
  "system_prompt": "你是专业的财报分析助手，擅长从财报PDF中提取营收、利润、负债率...",
  "llm_adapter": "tongyi",
  "tools": ["web_search", "rag_retrieval"],
  "icon": "finance_mode"
}

查询 Agent：
{"action": "list", "conversation_id": 5, "current_user_id": 2}

重名检测：
{"action": "duplicate", "conversation_id": 5, "current_user_id": 2, "name": "财报分析专家", "existing_name": "财报分析专家"}

```

- 约束条件

```Plain Text

┌─────┬────────────────────────────────────────────────────┬─────────────────────────────────────────────┐
│  #  │                        约束                        │                  实现位置                   │
├─────┼────────────────────────────────────────────────────┼─────────────────────────────────────────────┤
│ 1   │ name 必填，不可为空                                │ manage_agent.create_agent() 校验            │
├─────┼────────────────────────────────────────────────────┼─────────────────────────────────────────────┤
│ 2   │ system_prompt 必填，不可为空                       │ 同上                                        │
├─────┼────────────────────────────────────────────────────┼─────────────────────────────────────────────┤
│ 3   │ llm_adapter 仅可选 tongyi / deepseek / opencode    │ _normalize_adapter() 白名单                 │
├─────┼────────────────────────────────────────────────────┼─────────────────────────────────────────────┤
│ 4   │ tools 必须是字符串数组                             │ _normalize_tools() 校验                     │
├─────┼────────────────────────────────────────────────────┼─────────────────────────────────────────────┤
│ 5   │ 同名 Agent → 抛错，不加时间戳                      │ _build_create_name() 抛 ValueError          │
├─────┼────────────────────────────────────────────────────┼─────────────────────────────────────────────┤
│ 6   │ 创建后自动同步到 Mission 的 squad_config           │ _add_agent_to_mission_squad()               │
├─────┼────────────────────────────────────────────────────┼─────────────────────────────────────────────┤
│ 7   │ 创建后自动注册到 Orchestrator 运行时               │ _register_runtime_agent()                   │
├─────┼────────────────────────────────────────────────────┼─────────────────────────────────────────────┤
│ 8   │ conversation_id + current_user_id 自动注入         │ _caller_ctx contextvars                     │
├─────┼────────────────────────────────────────────────────┼─────────────────────────────────────────────┤
│ 9   │ LLM 输出非 JSON → 错误返回给用户（不退化为假回复） │ _handle_agent_management_request JSON parse │
├─────┼────────────────────────────────────────────────────┼─────────────────────────────────────────────┤
│ 10  │ 缺失字段用默认值，不追问用户                       │ Prompt 规则 #6                              │
└─────┴────────────────────────────────────────────────────┴─────────────────────────────────────────────┘

```



### 6\.2 Prompt设计

```YAML
┌─────────────────────────────────────────────────────────────┐
│                 agent_builder System Prompt                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ## 身份                                                     │
│ 你是 AgentHub 的 Agent 管理专家。你有权在系统中               │
│ 创建、修改、查询、删除 Agent。所有操作通过调用工具完成。       │
│                                                             │
│ ## 可用工具 (你必须调用这些工具，不能假装执行)                  │
│                                                             │
│ - create_agent: 创建新 Agent                                │
│   必填: name, system_prompt                                 │
│   可选: description, icon, llm_adapter, tools                │
│                                                             │
│ - update_agent: 修改已有 Agent                               │
│   必填: agent_id                                            │
│   可选: name, system_prompt, description, tools, ...         │
│                                                             │
│ - list_agents: 列出当前用户的所有 Agent                       │
│                                                             │
│ - delete_agent: 删除一个 Agent（慎用，需确认）                 │
│                                                             │
│ - inspect_agent: 查看某个 Agent 的完整配置                    │
│                                                             │
│ ## 可分配给新 Agent 的工具 (tools 字段合法值)                  │
│                                                             │
│ 以下工具可以配置到新 Agent：                                   │
│   web_search         → 网络搜索                              │
│   rag_retrieval      → 知识库检索                            │
│   scan_vulnerabilities → 代码漏洞扫描                         │
│   file_converter.*   → 文件格式转换                          │
│                                                             │
│ ## 可选的 LLM 后端                                           │
│                                                             │
│   tongyi   → 通义千问 qwen-plus                             │
│   deepseek → DeepSeek deepseek-chat                         │
│   opencode → OpenCode Zen (免费档，当前不可用)                │
│                                                             │
│ ## 当前系统已有 Agent（不能重复创建）                          │
│                                                             │
│   系统内置: planner, summarizer, tongyi, deepseek            │
│   内置自定义: code_reviewer, product_manager, agent_builder   │
│              opencode_coder, opencode_bigpickle              │
│   用户自定义: {从 DB 动态查询}                                │
│                                                             │
│ ## 行为规则                                                  │
│                                                             │
│ 1. 信息不足时追问，不要猜测                                   │
│    - 用户说"创建Agent"但没说功能 → 问它要做什么               │
│    - 用户说"修改Agent"但没说是哪个 → 先 list_agents          │
｜                                                               ｜
│ 2. **创建前必须先用 action=list 查看已有 Agent，避免重复创建。**
｜    如果用户要更新 Agent，用 action=update。
｜                                                         │
│ 3. system_prompt 必须具体                                    │
│    - 用户没给时，根据 name + description 自动生成              │
│    - 必须包含：角色定义、核心能力、输出格式、约束条件           │
│    - 反例："你是一个有用的助手" → 太模糊                      │
│    - 正例："你是财报分析专家，擅长从财报PDF中提取..."          │
│                                                             │
│ 4. tools 分配必须合理                                        │
│    - 财报分析Agent → web_search + rag_retrieval              │
│    - 代码审查Agent → scan_vulnerabilities                    │
│    - 通用对话Agent → [] (空)                                 │
│    - 不要分配无关工具                                         │
│                                                             │
│ 5. 删除前必须确认                                            │
│    - 列出要删除的 Agent 名称和 ID                            │
│    - 说明后果（对话历史保留但 Agent 不可用）                   │
│    - 如果用户没有明确确认，不执行删除                         │
│                                                             │
│ 6. 修改已有 Agent 的工作流                                   │
│    - Step 1: 调用 list_agents 查看有哪些                     │
│    - Step 2: 调用 inspect_agent 查看当前配置                 │
│    - Step 3: 调用 update_agent 修改指定字段                  │
│    - Step 4: 汇报修改前后的差异                              │
│                                                             │
│ 7. 操作完成后用中文汇报 
｜    - 输出纯 JSON，不要 markdown 包裹。                                      │
│    - 创建："✅ 已创建 Agent「{name}」(ID: {agent_id})，       │
│            已加入当前 Mission 的 Team"                       │
│    - 修改："✅ 已将「{name}」的 system_prompt 从...改为..."   │
│    - 删除："✅ 已删除 Agent「{name}」"                       │
│
｜ 8. **去重规则**：
｜    - 如果用户要创建的名字和已有 Agent 完全一样，                ｜
｜      输出 action=duplicate，询问用户是使用已有的还是换个名字。     ｜
｜    - 如果用户说"用已有的"，输出 action=none 表示无需操作。        ｜
｜    - 如果用户说"换一个"，创建一个不同名字的 Agent。              ｜
｜                                                            │
│ ## 当前执行上下文                                            │
│ - 用户 ID: {current_user_id}                                │
│ - Mission ID: {conversation_id}                             │
│ - 当前时间: {datetime.now()}                                │
└─────────────────────────────────────────────────────────────┘

```



### 6\.3 评估体系

目前暂时使用收集到的常规Case进行测试，预计三期设计详细评测集和对应指标

|问题类型|问题|
|---|---|
|简单问题（大模型直接回答或简单调用工具）|翻译句子：Today is a sunny day\.|
||去公开网站上搜集10个最近的AI新闻，并且表明出处|
||计算房贷两种还款方式（等额本息 / 等额本金）总利息、每月月供差异，结合不同贷款年限、金额做表格对比，并给出选择建议。|
||规划一场 2 天 1 夜北京周边短途自驾游，包含路线规划、餐饮住宿预算等。|
||分析短视频账号涨粉缓慢的 10 类原因，对应给出整改方案，再撰写 7 天内容更新排期及每条视频主题。|
|复杂问题（需要多步骤产出，多Agent协作，或调用多个工具）|结合近 3 年数据，分析国内露营行业发展现状、痛点，并撰写一份面向新手的露营场地选址 \+ 装备搭配完整攻略。|
||用 Excel 制作学生成绩统计表，完成数据录入、平均分 / 排名计算、条件格式标红不及格分数，附完整操作步骤 \+ 模板说明。|
||调研三款主流家用扫地机器人，从性能、价格、续航、售后四大维度做对比测评，再结合不同户型给出选购建议，最后以PPT形式产出|
||创建一个Agent Team，能够完成从选题，分镜脚本编写，AI生成视频，剪辑，发布，监控流量等一系列流程等智能团队。|
||为刚刚那个团队搭建后台智能看板，需要包括各个Agent的日志归总，数据起伏，成本监控等方面。最后以网页形式交付|





## AI协作沉淀

我在AgentHub项目中主要担任AI产品经理\+前端开发工程师的职责，沉淀出一套AI时代从想法到完整可交互前端界面的SOP，已经通过多个项目验证和改进这个SOP。并且根据实际产出效果规整出一套可用性极强的Skill，和目前体验下生成质量最高的AI工具。

### 7\.1 从想法/BRD到产品PRD         

- Skill：Product\-Manager\-skill   链接: [GitHub\-Product\-Manager\-Skills](https://github.com/deanpeters/Product-Manager-Skills)

工具：大模型直接对话（Claude/Codex/Claude Code等可添加Skill的大模型对话产品即可）

- 将想法，或已有项目资料提供给AI，并提前装载Product\-Manager\-skill/如无法使用则不需要：

    - 初始输入：你是一个产品经理，你需要根据我的想法/已有项目资料，并且从技术实现难度，产品定义，核心功能这三个角度出发，写出一个产品BRD/MRD

    - 在AI输出BRD后，和AI进行头脑风暴，对你不同意的点进行修改，直到BRD符合你的想法，确定产品在你心目中的**核心框架和产品定义**

    - 将PRD模版（如果有PRD规范的话）给AI，让AI生成完整PRD

    - 根据初版PRD完善PRD细节，在脑中有对这个产品的**完整细节**

    - 在写完后，基于个人编程的能力，让AI评估这个产品的**技术难度和可行性**，允许AI说我现有技术完成不了这个项目（根据经验，在这个过程中一定要根据自己对编程的了解程度让AI进行判断，AI往往在这个阶段容易低估技术难度）

### 7\.2 从PRD到完整前端交付

- 现在已经有你心目中完美的PRD了，下一步是确定前端UI设计方案

    - 在UI网页设计时，由于每个人审美不同，各个平台也有不同偏好的设计方案，作为非设计专业同学，很难精准的描述出我们想要的设计范式和页面结构，所以下面这一套提示词\+Skill\+Agent工具是我总结出来能够得到较好结果的一套方案

    1. 初始输入：（PRD文档）根据我的PRD文档，生成一段适合输入给UI设计Agent或是Codex这种编程Agent的提示词

    2. 根据自己的偏好，自己对输出的提示词进行修改（如果看不懂的部分不需要修改）

    3. 使用多个工具去进行产出  skill推荐：[Github\-taste\-skill](https://github.com/Leonxlnx/taste-skill) [GitHub \- /impeccable](https://github.com/pbakaus/impeccable)

    |    Agent工具|    Stitch（Google下UI设计Agent）|    Codex/Trae/Cursor|    Claude Code|
    |---|---|---|---|
    |    输入内容|    将前面得到的提示词和PRD输入<br>    |    将前面得到的提示词和PRD输入<br>    （可以接入偏好的Skill）|    使用taste\-skill/impeccable，将前面得到的提示词和PRD输入|
    |    大致修改|    自然语言修改，如果需要结合，放到Stitch这个平台进行整合 <br>    e\.g\. 我喜欢Claude code产出的UI设计的风格 但是我喜欢stitch产出的UI设计的排版布局，将Claude Code生成的UI截图发送到Stitch 修改|||
    |    细节修改|    对于使用过Figma的同学，将符合你审美的设计方案上传到Figma 进行精细修改<br>    对于未使用过Figma的同学，将符合你审美的设计方案上传到Stitch进行精细修改|||

- 现在已有你设计好的UI设计方案，现在需要变成完整的前端代码输出

    - 将这个方案以HTML的形式输出到你想用到Coding Agent上（Trae，Cursor，Codex，Claude Code）

    - 让Coding Agent根据你目前的代码和PRD，优化前端的交互逻辑并且开启预览的界面

    - 与Coding Agent去调优相关前端的交互逻辑

    - 最后，确认所有的前端交互和页面设计，UX交互流程

    

**已经完成PRD产出，前端页面开发的完整任务了**





