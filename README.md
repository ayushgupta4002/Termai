# Termai - AI-Powered Command Line Assistant

## Overview
Termai is a command-line tool specially designed for beginners,it translates natural language instructions into shell commands and executes them. It streamlines terminal interactions by automating command generation, reducing the need to memorize complex syntax.

## Features
- **Natural Language to Shell Command Conversion** – Converts plain English instructions into executable shell commands using the Gemini language model.
- **Command Review** – Allows users to review generated commands before execution to ensure accuracy.
- **Command Execution** – Runs commands directly and presents output in a user-friendly format.
- **Shell Detection** – Identifies the active shell environment (bash, zsh, PowerShell, etc.) for compatibility.
- **Command Validation** – Implements security measures to prevent execution of potentially harmful commands.

## Installation

### Using pip (Recommended)
```sh
pip install termai-cli
```

### From Source
```sh
git clone https://github.com/ayushgupta4002/Termai
cd termai
pip install .
```

## Usage

### Basic Usage
```sh
termai "Your instruction here" -e
```

### Example Commands
#### Create a Next.js project and spin up a PostgreSQL container in Docker:
```sh
termai "Make a Next.js project and spin up a PostgreSQL image in Docker" -e
```

![image](https://github.com/user-attachments/assets/84428b25-4cee-4542-b547-75504907dae2)

#### List all running Docker containers:
```sh
termai "Show all running Docker containers" -e
```
![image](https://github.com/user-attachments/assets/cde6badf-d2ad-4353-9639-fa6849841e02)

#### Find and delete all `.log` files in the current directory:
```sh
termai "Find and delete all .log files in this folder" -e
```

## Architecture
Termai's core logic is in `cli.py`, which:
1. Receives a natural language instruction.
2. Uses `get_shell_command` (via `langchain_google_genai`) to generate shell commands.
3. Validates commands using `validate_command` in `utils.py`.
4. Executes commands securely and displays results.

## Project Structure
```
termai/
├── src/
│   ├── cli.py       # Command-line interface logic
│   ├── utils.py     # Utility functions (validation, shell detection)
│   └── __init__.py
├── setup.py       # Build script for packaging
└── README.md
```

## Dependencies
- **Python** – Primary language
- **Typer** – CLI framework
- **Pydantic** – Data validation
- **Rich** – Enhanced terminal output
- **google-generativeai & langchain-google-genai** – AI model integration
- **python-dotenv** – Environment variable management
- **setuptools** – Packaging and distribution
- **subprocess** – Command execution

## Configuration
Before using Termai, set up your Gemini API key:
```sh
echo "GOOGLE_API_KEY=your_api_key" > .env
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue.

## Support
For any issues or feature requests, please open an issue on GitHub.
