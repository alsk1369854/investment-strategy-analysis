## InvestmentStrategyAnalysis

### environment

```bash
python version : 3.11.4
```

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

### build

```bash
pyinstaller --name investment_strategy_analysis_app --onefile
pyinstaller --name myapp --onefile --windowed --icon=icon.ico main.py
```
