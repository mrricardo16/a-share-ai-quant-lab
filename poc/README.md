# V0.1 技术预研（PoC）

本目录只包含**只读行情探针**和离线验证，不含回测策略、真实交易或券商接入。

## 1. 环境准备

建议 Python 3.11、独立虚拟环境：

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r poc/requirements-data.txt
```

## 2. 离线字段/异常测试

```powershell
python -m pytest poc/data/test_etf_source_probe.py -q
```

## 3. 真实行情接口测试（需可联网）

```powershell
python poc/data/etf_source_probe.py --symbol 510050 --source sina --output reports/probe-sina-510050.json
python poc/data/etf_source_probe.py --symbol 510050 --source em --start 20240101 --end 20261030 --output reports/probe-em-510050.json
```

可选证券代码：510050、510300、510500。逐个测试并记录延迟、成功次数、不同日重复调用结果和上游错误。避免高频请求。

**重要限制：** 本探针只验证日线数据的基本结构与 OHLCV 完整性；不等于完成交易日历、成交量单位、分红/复权、授权或真实回测校验。Sina 接口文档没有成交额字段，无法直接补造。

## 4. PoC 分阶段标准

- **P0-Data**：实际联网调用两家源，记录接口可达、时间范围、字段质量及错误。
- **P0-Corporate actions**：分红/复权和成交量单位核实（阻塞正式长期回测）。
- **P0-Engine**：在同一份数据快照上比较 Backtrader 与 RQAlpha，验证次日成交、T+1、100 份、费用、现金和分红。
- **ADR**：实测后更新 doc/adr/ADR-002-backtest-engine.md 并选择引擎。

当前执行环境无法访问公网安装依赖，实际联网和框架运行测试均标记为**待验证**；参见 doc/research/poc-2026-11-03.md。