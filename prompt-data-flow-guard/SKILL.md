---
name: prompt-data-flow-guard
description: Use when modifying AI prompt templates, data schemas, JSON key names, function signatures, or any data format that has downstream consumers. Triggers on: changing prompt output format, renaming dict keys, adding new input fields, modifying API contracts, or any change where upstream data flows to multiple downstream readers.
---

# 数据流完整性守卫

## 概述

修改任何数据格式时，必须追踪全链路：谁生产这个数据 → 谁消费这个数据 → 是否每个消费者都同步更新了。

**核心原则：改一处，查全家。**

## 规则 1：改键名 → 查全链路

修改 Prompt 输出 JSON 的键名（如 `basic_info` → `基本信息`）时，立即检查并更新：

```
Prompt 输出键名变更
  ├── doc_assembler.py     ← 读取 JSON 拼装 Word 文档
  ├── _extract_*() 函数    ← 读取 JSON 做数据提取
  ├── 下游 Prompt          ← 用此 JSON 作为输入的后续 Prompt
  ├── API 返回给前端的字段  ← 前端展示用的字段映射
  └── 数据库 JSONB 列      ← 存储原始 JSON 的地方
```

**检查方法**：grep 搜索旧键名，确认为什么每个引用不需要改？如果应该改，立即改。

## 规则 2：加新输入 → 追踪到最终输出

添加任何新输入字段（前端表单、API 参数、Prompt 变量）时：

```
前端表单字段 → API 接收参数 → Celery 任务参数 → Prompt {变量} → AI 输出 → doc_assembler 展示
```

如果中间任何一环断开（变量传了但 Prompt 没用，Prompt 用了但没传给模板），要么接上，要么删掉字段。

**真实案例**：今天加了 `birthplace`（籍贯）字段，前端 → API → 任务都传了，但 Prompt 没明确要求 AI 使用 → 用户填了却没输出。

## 规则 3：改代码 → 先搜索所有引用

修改 `.py` 文件中任何函数签名、字典键名、Prompt 变量名时：

1. `grep` 搜索该项目中所有引用该名称的地方
2. 列出每个引用
3. 确认每个引用是否需要同步修改
4. 改完后再搜一次，确认没有遗漏

**真实案例**：今天改 Prompt 键名从英文到中文，改了 Prompt 模板和 doc_assembler，但漏了 `_extract_summary()` 函数 → 摘要为空 → 策略 Prompt 没有上下文。

## 规则 4：改代码 → 加注释标注

**每次修改任何代码文件时，在改动处加注释**，格式：

```python
# [2026-06-09] 修改原因：xxxx。关联影响：需同步改 X、Y、Z
```

**注释包含**：
- 修改日期
- 为什么改（不是"改了什么"，而是"为什么这样改"）
- 关联影响（改这个会影响哪些其他地方）

**为什么必要**：项目文件多、逻辑链长。今天的你能记住为什么这样写，三个月后的你（或接手的人）只能靠注释。

## 规则 5：Docker 重建 → 确认缓存已清除

```
前端 rebuild 后：ls -l frontend/dist/assets/ 检查时间戳
后端 rebuild 后：检查容器内文件 mtime 是否更新
数据库变更后：确认 Alembic/自动建表已生效
```

**真实案例**：今天 `company_id=""` 改 `nullable=True`，`--build` 用了缓存 → 旧镜像仍然有外键约束 → 连报三次同样的错。

## 检查清单

每次改 Prompt 或数据格式后，逐项打勾：

- [ ] Prompt 输出键名改了 → doc_assembler 同步了
- [ ] Prompt 输出键名改了 → _extract 函数同步了
- [ ] Prompt 输出键名改了 → 下游 Prompt 的 {变量} 同步了
- [ ] 加了新变量 → 调用处的 .format() 传了值
- [ ] 加了新变量 → Prompt 模板里确实用了 {变量}
- [ ] 改了函数签名 → grep 搜过所有调用方
- [ ] 每条改动都有注释标注日期和原因
- [ ] Docker 重建用了 `--no-cache` 或确认缓存没挡路

## 常见错误模式

| 症状 | 根因 | 违反的规则 |
|------|------|-----------|
| 方案某章节空白 | 改了 JSON 键名，doc_assembler 还在读旧键名 | 规则 1 |
| 填了信息但方案没体现 | 输入传到了 API，但 Prompt 没要求 AI 使用 | 规则 2 |
| 摘要/提取函数返回空 | 键名改了，提取函数还在用旧键名 | 规则 3 |
| 改了代码重建不生效 | Docker 缓存了旧镜像 | 规则 5 |
