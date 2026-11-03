# V0.1 引擎选型技术基准（2026-11-03）

## 本轮实际执行环境
- Python 3.13.5；可用 pandas 2.2.3、pytest 9.0.2。
- 当前运行容器 DNS 无法解析 github.com 和 pypi.org。
- 当前容器未安装 AKShare、Backtrader、RQAlpha，无法进行真实行情或框架的本地动态验证。

## 已执行的离线测试
测试文件：`poc/engine/test_reference_ledger.py`。
实际命令：`python -m pytest -q`（在该目录运行）。
结果：**8 passed in 0.06s**，同时 Python 编译检查通过。

| 场景 | 结果 |
|---|---|
| 信号日不能当日成交 | PASS |
| 次日开盘买卖与现金、权益核对 | PASS |
| T+1 当日卖出被拒且账簿不变 | PASS |
| 100 份整手、资金不足、坏价格 | PASS |
| 不可交易时拒单 | PASS |
| 多笔买入后按可卖持仓扣减 | PASS |
| 佣金费率高于最低费时按费率计算 | PASS |
| 相同输入/参数结果一致 | PASS |

假数据校验：D2 开盘价 2.00 元买 100 份，D3 开盘价 2.20 元全部卖出，假设双边滑点 0.1%、单边最低佣金 5 元，最终现金为 **10,009.58 元**。仅用于会计对账，不是历史收益、收益率预测或实盘推荐。

## 框架验证状态
| 验证 | Backtrader | RQAlpha |
|---|---|---|
| 文档与接口确认 | 已参考公开文档 | 已参考公开文档 |
| 动态安装/导入 | 当前环境未验证 | 当前环境未验证 |
| 相同合成账本对照 | 已提交基本次日成交测试，CI 结果待核实 | 待编写 |
| ETF T+1、整手、分红、最低佣金 | 未完成 | 未完成 |
| 真实历史 ETF 数据回测 | 未完成 | 未完成 |
| 确定正式框架 | **否** | **否** |

GitHub Actions 配置 `.github/workflows/poc-validation.yml` 包含离线测试与 Backtrader 时间顺序冒烟测试；是否运行通过以远端检查结果为准，本记录不提前宣布成功。

## 许可风险
RQAlpha 项目根目录 LICENSE 对商业用途有限制，即使 PyPI 元数据写有 Apache-2.0，也不能忽略项目当前实际许可证。后续若要发布可商用代码，必须单独核查许可；优先避免复制框架内部源码。

## 下一步决策门槛
1. 有网络环境下验证 AKShare 两个 ETF 日线源，尤其成交量单位、复权、分红和丢失日期。
2. 取得可使用的冻结 ETF 数据快照。
3. 两个框架对照同一快照，同一仓位/费用/时间因果规则，检查每一笔买卖、持仓、成本及权益。
4. 逐项解决分红和交易限制；之后才将 ADR-002 标为 Accepted。

## 资料
- Backtrader broker：https://www.backtrader.com/docu/broker/
- RQAlpha 安装/数据：https://rqalpha.readthedocs.io/zh-cn/latest/intro/install.html
- RQAlpha 授权：https://github.com/ricequant/rqalpha/blob/master/LICENSE
- AKShare ETF 文档：https://akshare.akfamily.xyz/data/fund/fund_public.html
