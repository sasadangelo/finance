# Quick Start Guide

Get started with ETF Finance in 3 simple steps:

## 1. Install UV

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 2. Setup Project

```bash
cd finance
uv sync
```

## 3. Test Setup

```bash
uv run python test_setup.py
```

## Ready to Use!

```bash
# Download ETF data
uv run python download.py -t VUSA.MI

# Update all quotes (using shell script)
./update_quotes.sh

# View chart
uv run python graph.py VUSA.MI

# Analyze performance
uv run python perf.py VUSA.MI IWRD.MI

# Monitor portfolios (using shell script)
./monitor.sh
```

For detailed documentation, see [README-UV.md](README-UV.md)