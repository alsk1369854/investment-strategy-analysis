## InvestmentStrategyAnalysis

### venv

#### create

```bash
python3 -m venv .venv
```

#### start

```bash
# windows
.venv\Scripts\activate.bat

# linux
source .venv/bin/activate
```

#### close

```bash
deactivate
```

### install dependence libs

```bash
pip install -r requirements.txt
```



### Nasdaq_history_data.xlsx

#### columns description

- Price: 收盤價

- Change: 每日漲跌幅

- QLD: 追蹤每日漲跌幅兩倍

- 季線下彎AND收盤在季線下1倍其餘3倍: 投資策略



#### 需求

- 收益波動率

- 夏普比率

- 年化報酬率

- 最大回測
