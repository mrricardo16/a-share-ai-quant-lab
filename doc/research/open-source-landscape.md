# 开源项目调研（初步清单）

> 本文件记录待复核的参考项目，不代表已运行、审计或核实收益。复用具体代码前需要检查源码许可与版本。

| 项目 | 地址 | 学习重点 | 拟用阶段 |
|---|---|---|---|
| AKShare | https://github.com/akfamily/akshare | ETF 数据源、字段对齐 | V0.1 |
| Backtrader | https://github.com/mementum/backtrader | 事件驱动订单、回测 | V0.1 PoC |
| RQAlpha | https://github.com/ricequant/rqalpha | 国内交易规则、账户/撮合 | V0.1 PoC |
| QuantStats | https://github.com/ranaroussi/quantstats | 绩效与回撤报告 | V0.1 |
| a-share-quant-sim | https://github.com/fkchaos/a-share-quant-sim | 回测和模拟复用、失败策略 | V0.1+ |
| etf-rotation-strategy | https://github.com/zhangsensen/etf-rotation-strategy | ETF 轮动、滚动验证 | V0.2 |
| daily_stock_analysis | https://github.com/ZhuLinsen/daily_stock_analysis | 多数据源、多模型、日报 | V0.2–0.3 |
| TradingAgents-CN | https://github.com/hsliuping/TradingAgents-CN | Agent 分工、工具、研究流程 | V0.2 |
| Microsoft Qlib | https://github.com/microsoft/qlib | 因子、模型与研究工作流 | 后续 |
| Microsoft RD-Agent | https://github.com/microsoft/RD-Agent | 自主研究和实验迭代 | 后续 |

## 评估步骤
1. 核对最后提交、issue 活跃度、安装文档和 Python 版本支持。
2. 阅读许可及第三方数据的使用限制。
3. 单独运行最小样例并保存环境/错误日志。
4. 仅摘录设计理念；不复制未经核实许可的实现。
5. 对“策略盈利”“稳定运行”等声明要求可复现实验而非引用 README。
