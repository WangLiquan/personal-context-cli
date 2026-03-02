# Personal Context CLI（中文）

本项目是本地优先（local-first）的命令行工具，用于加密保存个人/家庭上下文，并基于上下文进行问答。

[English](README.md) | 简体中文

## 安装（测试者路径）

### 1) 安装 CLI（一次）

```bash
pipx install --force "git+https://github.com/WangLiquan/personal-context-cli.git@main"
```

安装后可直接使用 `personal-context` 命令。

如果你希望固定到一个 beta 版本：

```bash
pipx install --force "git+https://github.com/WangLiquan/personal-context-cli.git@v0.1.3-beta"
```

### 2) 安装 skills（一次，无需 wrapper 脚本）

```bash
npx skills add WangLiquan/personal-context-cli -g --all -y
```

在 OpenX / Claude Code 中可直接调用以下 skill：
- `personal-context-cli-workflow`
- `personal-context-init-profile`
- `personal-context-ask-flow`
- `personal-context-reinit`

## 密码配置（推荐）

```bash
# 首次写入 macOS Keychain
security add-generic-password -a "$USER" -s personal-context-cli -w "your-strong-password" -U

# 在当前 shell 会话中加载
export PCTX_PASSWORD="$(security find-generic-password -a "$USER" -s personal-context-cli -w 2>/dev/null)"
```

可选：把这一行加入 `~/.zshrc`，新终端自动加载。

```bash
export PCTX_PASSWORD="$(security find-generic-password -a "$USER" -s personal-context-cli -w 2>/dev/null)"
```

之后的大部分命令都可以省略 `--password`。

## 核心命令

```bash
# 初始化加密存储
personal-context init \
  --data-file ./profile.enc

# 设置与读取 profile
personal-context profile set \
  --data-file ./profile.enc \
  --age 32 --industry internet --income-range 50-100w

personal-context profile get \
  --data-file ./profile.enc

# 预览上下文
personal-context context preview \
  "Should I increase my emergency fund?" \
  --data-file ./profile.enc

# 发问（通过宿主登录态 relay，不需要项目 API key）
personal-context ask \
  "Should I increase my emergency fund?" \
  --provider auto \
  --relay-timeout-seconds 45 \
  --relay-retries 1 \
  --data-file ./profile.enc
```

当上下文不足时，`ask` 会先追问补充信息，并将补充内容加密写回本地，再生成最终回答。

## Provider 模式

- `auto`（默认）：使用已登录的 `codex` / `claude` relay
- `codex`：强制走 `codex exec`
- `claude`：强制走 `claude -p`

## 安全模型

- 数据落盘前会先加密。
- 真实数据文件（`*.enc`）与 `.env` 已被 git 忽略。
- 密码可通过 `--password` 或环境变量 `PCTX_PASSWORD` 提供。
- 仓库应只保存代码与模板，不保存真实隐私数据。

## 开发

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
pip install pytest
PYTHONPATH=src .venv/bin/pytest -v
```
