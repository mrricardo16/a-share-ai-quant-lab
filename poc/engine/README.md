# 独立参考账本与框架对照

## 为什么有 reference_ledger
这不是另造完整回测引擎。它只用 Python 标准库和 Decimal，表达可手工核对的**合成 ETF 订单场景**，为 Backtrader / RQAlpha 适配层提供“预期行为基准”。

可检查：
- 收盘信号不能在同一交易日立即按已知收盘价成交。
- 买入以 100 份为整数单位，资金不足拒单。
- T+1 的当日买入份额不可当日卖出。
- 成交滑点、最低佣金、现金和持仓余额一致。
- 不可交易日不虚构成交，同样输入产生一致结果。

暂未覆盖：分红与除息、真实交易所行情、撮合深度、涨跌限制、部分成交、交易日历、ETF 不同类别规则。**因此不能将它作为生产回测引擎**。

## 本地运行
```powershell
python -m pip install "pytest>=8,<10"
python -m pytest poc/engine/test_reference_ledger.py -q
```

在真实安装 Backtrader 之后：
```powershell
python -m pip install backtrader pandas
python -m pytest poc/engine/test_backtrader_smoke.py -q
```
Backtrader 合成测试单独校验默认次日开盘成交，不等于完整交易规则通过。

GitHub Actions 已定义：推送 PoC 相关文件会触发离线校验和 Backtrader 合成时间测试；公开行情接口的请求需要在 Actions 中显式选择 `workflow_dispatch` 的 `live_data=true`，避免无意对上游数据服务产生流量。

实际在线验证结果需要以 GitHub Actions 日志/产物为准，不能仅因为存在 workflow 文件就声称通过。
