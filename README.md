# A-Share AI Quant Lab

中国 A 股（首期为境内股票型 ETF）AI 量化研究实验室。

> 项目处于规划阶段。当前不提供投资建议、收益承诺或真实交易能力。

## 目标

构建可复现的研究链路：**行情采集 → 数据校验与快照 → 策略信号 → 事件驱动回测 → 风险/交易成本模拟 → 样本外验证 → 绩效与实验报告**。

- 初始模拟本金：人民币 10,000 元；不使用杠杆。
- **V0.1**：ETF 日频数据、买入持有基准与趋势基线、可信回测、实验记录和报告；**没有实盘下单**。
- **V0.2**：Codex / 可选模型 API 通过受控研究工具提出假设；Python 引擎执行可复现验证。
- **V0.3**：真实交易日行情下运行的模拟账户、定时任务、审计与异常告警。
- **V1.0（有条件）**：经过长期模拟和合规核查后，才评估小额实盘；不默认启用。

## 文档入口

- [项目概览](doc/00-project-overview.md)
- [需求与范围](doc/01-requirements.md)
- [系统架构](doc/02-architecture.md)
- [数据设计](doc/03-data-design.md)
- [策略设计](doc/04-strategy-design.md)
- [回测设计](doc/05-backtest-design.md)
- [风险管理](doc/06-risk-management.md)
- [AI 集成](doc/07-ai-integration.md)
- [开发路线图](doc/08-development-roadmap.md)
- [验收标准](doc/09-acceptance-criteria.md)
- [开源项目调研](doc/research/open-source-landscape.md)
- [V0.1 技术预研与测试记录](doc/research/poc-2026-11-03.md)
- [引擎基准与测试结果](doc/research/engine-benchmark.md)
- [数据接口探针运行说明](poc/README.md)
- [架构决策记录](doc/adr/README.md)

## 工程原则

1. 数据源不可用时明确报错，禁止杜撰价格、成交量和回测成绩。
2. 交易信号、订单、成交分别记录；策略不得使用未来信息。
3. 研究数据、策略参数、代码版本、费用模型与实验结果可追溯。
4. AI 仅提出研究方案和调用受控工具；交易与风控由确定性程序执行。
5. 实盘交易默认不存在；任何实盘能力需要独立设计、权限与合规评审。
6. 交易规则、数据服务可用性、第三方代码许可，均须在实现前重新核实。

## 状态

- 当前：文档骨架 + ETF 数据源只读探针；离线测试已通过 5 项；真实行情接口与回测框架尚未在线验证，未实现量化引擎。
- V0.1 的回测引擎（Backtrader / RQAlpha）和 ETF 行情供应商尚未选型完成。
- 默认采用 Python；初期 SQLite + Parquet；.NET/Vue3 仅为后期扩展。

## 开源许可

暂未选定 LICENSE。引用第三方项目实现时，应先检查各自许可和数据使用条款；不能直接复制受限制源码。
