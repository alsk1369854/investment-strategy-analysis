# InvestmentStrategyAnalysis

## DEMO

<video src="https://raw.githubusercontent.com/alsk1369854/investment-strategy-analysis/master/docs/demo.mp4" width="400" autoplay loop muted></video>

<p align="center">
    <img height="400px" src="https://raw.githubusercontent.com/alsk1369854/investment-strategy-analysis/master/docs/demo.gif"/>
</p>

## DEV

- python version: 3.11.4

## MacOS / Linux

```bash
conda create -n isaenv python=3.12
conda activate isaenv
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

### Build

```bash
pyinstaller --name app --onefile --windowed main.py
```
