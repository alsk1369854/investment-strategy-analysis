# InvestmentStrategyAnalysis

投資策略回測指標計算工具，載入 .excel 文件須包含 "日期" 與 “資本” 數據

- 日期：時間序列
- 資本：對應時間點所擁有的資產總額

回測指標：

- 年化收益
- 夏普比
- 收益波動
- 最大回撤

## DEMO

<p align="center">
    <img height="400px" src="https://raw.githubusercontent.com/alsk1369854/investment-strategy-analysis/master/docs/demo.gif"/>
</p>

## DEV

### MacOS / Linux

```bash
conda create -n isaenv python=3.12
conda activate isaenv
pip install -r requirements.txt
```

### Run

```bash
python main.py
```

### Build

```bash
pyinstaller --name isa_app --windowed main.py
# pyinstaller --name isa_app --onefile --windowed main.py
```
