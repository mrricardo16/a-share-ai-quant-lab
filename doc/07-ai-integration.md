# 07 AI 接入规划（V0.2 起）

## 双入口策略
- Codex：开发与交互式研究，可调用受控量化研究工具。
- Model API（例如 DeepSeek/OpenAI）：用于日后定时研究和独立部署；通过 Provider 抽象接入，非 V0.1 必需支出。
- 两者共享相同研究服务与实验记录，避免策略输出因入口不同而不可比较。

## 权限
AI 可：检索已校验数据摘要、提出假设、提交可验证的策略定义、运行限额回测、比较结果、撰写引用实验 ID 的报告。
AI 不可：直接交易、修改历史行情、篡改实验结果、绕过风控、无限调用付费模型、把测试集当训练数据。

## 未来工具候选
list_datasets, get_market_summary, create_strategy_candidate, run_backtest, get_experiment, compare_experiments, publish_report。

## API 工程要求
- API key 仅后端环境变量/安全凭据保存；不提交仓库或放在浏览器端。
- 请求预算、Token/费用日志、模型和 prompt 版本、时间范围、实验 ID 全量可追溯。
- 网络/API 失败不得影响确定性回测；配置允许停用模型调用。

## V0.1
只为研究核心保留边界，不实现 Provider 框架或正式 Agent runtime；Codex 可以作为外部开发工具。
