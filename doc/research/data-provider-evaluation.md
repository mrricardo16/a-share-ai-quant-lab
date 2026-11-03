# ETF 数据供应商验证计划

## 候选
AKShare 提供的新浪/东方财富 ETF 历史行情入口，以及其他明确许可的来源。

## 验证项目
- 能否获得指定基金的 5 年或可用历史区间日线。
- 是否含 OHLCV、成交额、日历、分红/复权事件。
- 重复调用结果一致性、异常码、限流和网络超时。
- 对照公开价格与基金公司公告，抽样核对公司行为。
- 数据源变化时，是否能冻结快照、发出故障并保留旧研究结果。
- 使用条款是否允许本地研究、缓存与公开展示。

## 评估记录格式
provider / api / test_time / symbols / date_range / success_rate / missing_days / corporate_actions / license_notes / decision。

## 当前结论
**尚未完成实际联通测试**；无生产可用的数据源结论。
