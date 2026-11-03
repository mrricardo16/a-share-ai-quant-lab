# ADR-002：回测引擎选型

**状态：Proposed（待评估）**

## 决策候选
Backtrader 和 RQAlpha。

## 评估要求
用相同的股票型 ETF 数据、10,000 元起始现金及相同交易费用执行相同策略，对照手工参考账。重点检查 T+1、现金、ETF 买卖单位、费用、分红和下一交易日成交。

## 当前决定
暂不绑定任一实现。选型见 [评估计划](../research/framework-evaluation.md)，完成 PoC 后更新本 ADR。
