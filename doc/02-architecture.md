# 02 系统架构

## V0.1 部署形态
一个 Python 进程中的模块化单体：CLI → Research Application → Data / Strategy / Backtest / Evaluation → Storage。
SQLite 存储元数据、运行与实验索引；Parquet 保存标准化历史快照（具体分工可在 PoC 后调整）。

## 逻辑模块
1. **Provider Adapter**：访问第三方数据源、重试、标识源与抓取时间。
2. **Data Validation / Snapshot**：规范化、完整性检查、冻结回测输入。
3. **Strategy**：根据某时点可见数据产生目标仓位或买卖信号。
4. **Portfolio / Risk**：校验现金、交易单位、仓位和退出条件。
5. **Backtest Engine Adapter**：把信号转为订单、撮合及交易流水。
6. **Evaluator**：比较基准、成本、回撤和样本外表现。
7. **Experiment Registry / Reporter**：记录版本、参数、指标和报告路径。

## 核心数据流
Provider → Validated Snapshot → Strategy → Order Intent → Risk Check → Simulated Fill → Ledger → Metrics → Report。

## 设计边界
- 策略不访问网络，不自行完成订单成交。
- 数据层不生成交易建议；报告层不“推算”不存在的交易。
- AI 后续只能调用带 schema 的研究工具；核心模块不依赖特定模型。
- 实盘交易模块不属于当前架构，后期需单独安全审计与授权。

## 未来扩展
V0.2 增加 Research Tools/ModelProvider；V0.3 模拟运行调度；按确实存在的多用户需要再引入 FastAPI/.NET/Vue3。先不要把模块拆成微服务。
