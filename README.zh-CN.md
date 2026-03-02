# Personal Context CLI（中文）

这是一个面向 Claude Code / OpenX 的插件优先项目。
底层是 CLI，但日常使用建议通过 skills 调用，完成个人上下文管理与问答。

[English](README.md) | 简体中文

## 项目定位

这个项目的主要用法不是手敲脚本，而是 skill 调用：

- 主要入口：在 Claude Code / OpenX 里直接调用 skills。
- CLI 是底层引擎，主要用于初始化和排错。
- 数据默认本地加密存储（`profile.enc`）。

## 这个库解决什么问题

- 跨会话时个人背景容易丢失，导致回答泛化、不贴合。
- 隐私信息很难做到“可复用”与“本地安全”兼顾。
- 对话历史越多越嘈杂，长期会拉低回答准确性。

这个库把上下文拆成三层并本地加密：
- `ask_history`：完整追溯
- `fact_memory`：长期有效关键事实
- 精简检索上下文：减少噪声，提高命中率

## 插件优先快速开始

### 1) 安装 CLI 运行时（一次）

```bash
pipx install --force "git+https://github.com/WangLiquan/personal-context-cli.git@main"
```

安装后可直接使用 `personal-context` 命令。

如果你希望固定到一个稳定版本：

```bash
pipx install --force "git+https://github.com/WangLiquan/personal-context-cli.git@v1.0.0"
```

### 2) 安装 skills（一次）

```bash
npx skills add WangLiquan/personal-context-cli -g --all -y
```

### 3) 在 Claude Code / OpenX 中直接调用

可直接使用以下 skill：
- `personal-context-cli-workflow`
- `personal-context-init-profile`
- `personal-context-ask-flow`
- `personal-context-reinit`

常见流程：
- 首次建档：`personal-context-init-profile`
- 日常提问：`personal-context-ask-flow`
- 清空重建：`personal-context-reinit`

## 密码输入方式

- 密码由 init 流程设置/确认。
- 不需要配置环境变量。
- 直接 CLI 调用时，通过 `--password` 显式传入。

## Ask 持久化策略

- 每次 `ask` 的提问都会写入加密的 `ask_history`。
- 会提炼长期有效信息写入 `owner_profile.fact_memory`（如房贷/收入/风险偏好）。
- 传给模型的是精简相关上下文（`fact_memory` + 最近笔记），避免历史噪声过多。
- 上下文不足时会追问，补充回答同样会持久化。

## Relay Provider

- `auto`（默认）：自动尝试已登录的 `codex` / `claude`
- `codex`：强制走 `codex exec`
- `claude`：强制走 `claude -p`

如果提示 relay 不可用，先确认至少一个 CLI 已安装并登录：
- `codex`
- `claude`

## 直接 CLI（高级/排障）

```bash
personal-context init --data-file ./profile.enc --password "<你的密码>"
personal-context profile set --data-file ./profile.enc --password "<你的密码>" --age 32 --industry internet --income-range 50-100w
personal-context context preview "Should I increase my emergency fund?" --data-file ./profile.enc --password "<你的密码>"
personal-context ask "Should I increase my emergency fund?" --provider auto --relay-timeout-seconds 45 --relay-retries 1 --data-file ./profile.enc --password "<你的密码>"
```

## 安全模型

- 数据落盘前会先加密。
- 真实数据文件（`*.enc`）与 `.env` 已被 git 忽略。
- 密码通过 `--password`（或交互输入）提供。
- 仓库应只保存代码与模板，不保存真实隐私数据。

## 开发

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
pip install pytest
PYTHONPATH=src .venv/bin/pytest -v
```
