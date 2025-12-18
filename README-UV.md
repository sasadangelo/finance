# ETF Finance - UV Setup Guide

This guide will help you set up and use the ETF Finance project with **uv**, the modern Python package manager written in Rust.

## 📋 Prerequisites

- Python 3.13 or higher
- Operating System: macOS, Linux, or Windows (WSL)
- UV package manager

## 🏗️ Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/sasadangelo/finance
cd finance
```

### 2. Sync Dependencies

```bash
# Create virtual environment and install all dependencies
uv sync
```

This command will:
- Automatically create a `.venv` virtual environment
- Install Python 3.13 if needed
- Install all dependencies from `pyproject.toml`
- Create a lock file for reproducibility

### 3. Verify Installation

```bash
# Activate virtual environment (optional, uv run does this automatically)
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# Check installed dependencies
uv pip list
```

## 📊 Using the Scripts

### Running Scripts with UV

Use `uv run` to execute any Python script:

```bash
# Download quotes for a specific ETF
uv run python download.py -t VUSA.MI

# Update all quotes
uv run python update_quotes.py

# Import data into database
uv run python import.py

# Display ETF chart
uv run python graph.py VUSA.MI
uv run python graph.py -p 1Y -m 50 VUSA.MI

# Analyze performance
uv run python perf.py VUSA.MI IWRD.MI
uv run python perf.py -s 2020-01-01 -e 2023-12-31 VUSA.MI

# Portfolio performance
uv run python perf_pfolio.py 60-40-a
uv run python perf_pfolio_yearly.py 60-40-a

# Yearly performance
uv run python perf_yearly.py VUSA.MI IWRD.MI
```

### Running the Flask Application

```bash
# Start the web server
cd flask
uv run python app.py

# Or with Flask CLI
uv run flask --app app run --debug
```

Open your browser at: http://localhost:5000

## 🔄 Managing Dependencies

### Adding a New Dependency

```bash
# Add a dependency
uv add package-name

# Add a development dependency
uv add --dev package-name
```

### Updating All Dependencies

```bash
# Update all dependencies to latest compatible versions
uv sync --upgrade
```

### Removing a Dependency

```bash
uv remove package-name
```

## 🛠️ Useful Commands

### Environment Management

```bash
# Create/update virtual environment
uv sync

# Clean and recreate environment
rm -rf .venv uv.lock
uv sync

# Show environment information
uv pip list
uv pip show package-name
```

### Running Scripts

```bash
# Run a Python script
uv run python script.py

# Run a command in the virtual environment
uv run command

# Run interactive Python
uv run python
```

### Development

```bash
# Install development dependencies
uv sync --all-extras

# Run tests (when available)
uv run pytest

# Format code with black
uv run black .

# Lint with ruff
uv run ruff check .
```

## 📁 Project Structure

```
finance/
├── pyproject.toml          # Project configuration and dependencies
├── .python-version         # Python version (3.13)
├── uv.lock                 # Dependencies lock file (auto-generated)
├── .venv/                  # Virtual environment (auto-generated)
├── database/               # SQLite database and CSV files
│   ├── etfs.db            # Main database
│   ├── ETF.csv            # ETF list
│   ├── quotes/            # Historical quotes
│   └── dividends/         # Dividend data
├── flask/                  # Web application
│   ├── app.py             # Flask entry point
│   ├── etfs.py            # Database models
│   └── templates/         # HTML templates
├── pfolio/                 # Sample portfolios
└── *.py                    # Main Python scripts
```

## ⚠️ Important Notes

### Legacy Code Note

The project contains some older code that may need updates:
- The `download.py` file uses deprecated patterns with `fix_yahoo_finance`
- Modern approach: use `yfinance` directly without `pdr_override()`
- All necessary dependencies are already installed

**If you encounter issues with download.py**, consider updating it to use modern yfinance syntax.

### Python Compatibility

The project requires Python 3.13+. If you have issues:

1. Check your Python version:
   ```bash
   python --version
   ```

2. UV will automatically install Python 3.13 if needed:
   ```bash
   uv python install 3.13
   ```

3. If you prefer a different version, modify `.python-version`

## 🐛 Troubleshooting

### Issue: "uv: command not found"

**Solution:** Restart your terminal after installation or add uv to PATH:

```bash
# macOS/Linux
export PATH="$HOME/.cargo/bin:$PATH"

# Add to your .bashrc or .zshrc to make it permanent
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
```

### Issue: Dependency errors

**Solution:** Clean and recreate the environment:

```bash
rm -rf .venv uv.lock
uv sync
```

### Issue: Python 3.13 not available

**Solution:** Install Python 3.13 with uv:

```bash
uv python install 3.13
```

Or use a previous version by modifying `.python-version`:

```bash
echo "3.12" > .python-version
uv sync
```

### Issue: Errors with fix_yahoo_finance

**Solution:** This is normal, the library is deprecated. Scripts should still work, but consider migrating to pure yfinance.

## 📚 Additional Resources

- [UV Documentation](https://docs.astral.sh/uv/)
- [UV Repository](https://github.com/astral-sh/uv)
- [PEP 621 - Metadata](https://peps.python.org/pep-0621/)
- [yfinance Documentation](https://github.com/ranaroussi/yfinance)

## 🔄 Migration from pip

If you were using pip, here's the command mapping:

| pip                               | uv                        |
| --------------------------------- | ------------------------- |
| `pip install -r requirements.txt` | `uv sync`                 |
| `pip install package`             | `uv add package`          |
| `pip uninstall package`           | `uv remove package`       |
| `pip list`                        | `uv pip list`             |
| `pip freeze`                      | `uv pip freeze`           |
| `python script.py`                | `uv run python script.py` |

## 🎯 Next Steps

1. ✅ Complete setup with `uv sync`
2. 📊 Explore available scripts
3. 🔄 Consider migrating from `fix_yahoo_finance` to `yfinance`
4. 🧪 Add tests with pytest
5. 📝 Improve documentation
6. 🚀 Develop new features

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check UV documentation
- Review error logs with `uv run python script.py -v`

---

**Happy trading! 📈**