# zhu-dong Skill

个人 Claude Code 技能集合，覆盖开发工作流、可视化图表、数据分析与机器学习全流程。

## 安装

```bash
git clone https://github.com/zhud2000/zhudong-skill.git ~/.claude/skills/
```

## 技能清单

### 开发工作流

| 技能 | 说明 |
|------|------|
| `task-orchestrator` | 复杂任务编排，防偷懒、防跳步、防粗心。5+步骤或 15 轮以上自动触发 |
| `engineering-disciplines` | 多文件改动时强制工程规范，适用范围评估与风险识别 |
| `prompt-data-flow-guard` | 数据格式/API/提示词变更时追踪下游影响面 |

### 可视化

| 技能 | 说明 |
|------|------|
| `excalidraw-diagram` | 生成 Excalidraw 手绘风格图表，支持架构图、流程图、概念图 |

### 数据分析

| 技能 | 说明 |
|------|------|
| `exploratory-data-analysis` | 数据探索与画像，分布分析、相关性、目标泄漏检查 |
| `pandas-patterns` | pandas 惯用写法，向量化优化、内存效率、防 SettingWithCopyWarning |
| `data-cleaning` | 数据清洗，缺失值、重复值、异常值、类型一致性处理 |

### 机器学习

| 技能 | 说明 |
|------|------|
| `feature-engineering` | 特征工程，编码、缩放、聚合、目标编码防泄漏 |
| `sklearn-pipelines` | scikit-learn Pipeline/ColumnTransformer，预处理与交叉验证防泄漏 |
| `model-evaluation` | 模型评估，指标选择、交叉验证策略、校准分析 |
| `model-serving` | 模型部署，FastAPI 推理服务、ONNX 加速、健康检查 |
| `ml-debugging` | 模型调试，loss NaN/不收敛/过拟合系统排查 |
| `reproducible-ml` | 可复现实验，种子固定、环境锁定、数据版本化 |
| `experiment-tracking` | 实验追踪，MLflow/W&B 日志、运行组织、模型注册 |
| `hyperparameter-tuning` | 超参调优，随机搜索/Bayesian/Optuna，搜索空间设计 |
| `imbalanced-data` | 不平衡数据处理，SMOTE/欠采样/类别权重/阈值调整 |

### 深度学习 & LLM

| 技能 | 说明 |
|------|------|
| `pytorch-training-loop` | PyTorch 训练循环，混合精度、checkpoint、可复现性 |
| `rag-pipeline` | RAG 检索增强生成，分块策略、向量库、混合检索 |
| `llm-finetuning` | 大模型微调，LoRA/QLoRA、PEFT/TRL、评估与防过拟合 |

## 使用方式

在 Claude Code 会话中，技能会根据上下文自动触发。也可手动调用：

```
/excalidraw-diagram 画一个系统架构图
```

## 维护

```bash
# 添加新技能
cp -r new-skill ~/.claude/skills/
git add . && git commit -m "添加 new-skill" && git push

# 更新技能
cd ~/.claude/skills && git pull
```
