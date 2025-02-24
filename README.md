# Project Overview

## Project Purpose

Termai is a command-line tool that translates natural language instructions into shell commands using the power of AI. It aims to make interacting with your terminal more intuitive and efficient by automating command generation and reducing the need to memorize complex syntax. Think of it as having an AI assistant that helps you navigate the command line.

## Key Features

*   **Natural Language to Shell Command Conversion:** Translates your plain English instructions into executable shell commands using the Gemini language model.
*   **Command Review:** Allows you to review the generated command(s) before execution, ensuring accuracy and preventing unintended actions.
*   **Command Execution:** Executes the generated commands directly from the tool, capturing and displaying the output in a user-friendly format.
*   **Shell Detection:** Automatically detects your shell environment (bash, zsh, powershell, etc.) to ensure compatibility.
*   **Command Validation:** Implements basic security measures by validating commands against a list of potentially dangerous patterns.

## Architecture

Termai's core functionality revolves around the `cli.py` script, which acts as the command-line interface. When you provide an instruction, `cli.py` uses the `get_shell_command` function to leverage the Gemini model (via `langchain_google_genai`) to generate the corresponding shell command(s). Before execution, the generated command is validated using the `validate_command` function from `utils.py` to prevent potentially harmful commands from running. Finally, the `execute_command` function executes the command(s), captures the output, and displays it to you. The `setup.py` file manages the project's dependencies and packaging.

## Technical Stack

*   **Python:** The primary programming language.
*   **Typer:** Used for building the command-line interface.
*   **Pydantic:** Used for data validation and settings management.
*   **Rich:** Used for creating visually appealing output in the terminal.
*   **google-generativeai & langchain-google-genai:** Used to interact with the Gemini language model.
*   **python-dotenv:** Used for managing environment variables.
*   **setuptools:** Used for packaging and distributing the project.
*   **subprocess:** Used for executing shell commands.
*   **Design Patterns:** Pydantic models are used for data validation.

## Getting Started

1.  **Clone the repository:** `git clone <repository_url>`
2.  **Navigate to the project directory:** `cd termai`
3.  **Install the dependencies:** `pip install .` (This uses `setup.py` to install the necessary packages)
4.  **Configure your Gemini API key:** Set the `GOOGLE_API_KEY` environment variable. You can do this by creating a `.env` file in the project root and adding `GOOGLE_API_KEY=YOUR_API_KEY`.
5.  **Run the tool:** `termai "Your instruction here" -e`

## Project Structure

```
termai/
├── src/
│   ├── cli.py       # Command-line interface logic
│   ├── utils.py     # Utility functions (command validation, shell detection)
│   └── __init__.py
├── try.py         # Script for creating a new Next.js application (example)
├── setup.py       # Build script for packaging and distribution
└── README.md
```
