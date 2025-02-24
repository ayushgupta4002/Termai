from pydantic import BaseModel, Field
import typer
import subprocess
import shlex
import os
import platform
from typing import Optional, List
from langchain_google_genai import ChatGoogleGenerativeAI
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.style import Style
console = Console()
from src.utils import detect_shell, validate_command
from dotenv import load_dotenv
from rich.table import Table
app = typer.Typer()
import google.generativeai as genai

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path)  # Explicitly load the .env file

# Access the API key from the environment
api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key = api_key)

class QueryChecker(BaseModel):
    commands: List[str] = Field(
        description="The list of shell commands generated by the LLM"
    )
class FinalOutput (BaseModel):
    commands: str= Field(
        description="The final output generated by the LLM"
    )

def get_shell_command(instruction: str) -> str:
    """Use Gemini to generate a shell command from natural language instruction."""
    system_info = "windows" if platform.system().lower() == "windows" else "unix"
    shell_type = detect_shell()
    typer.echo(f"\nDetected shell: {shell_type}\n")
    prompt = f"""
    You are an AI assistant that converts natural language instructions into **safe and precise shell commands** for {system_info} systems.  
    The user is currently using {shell_type} shell.  

    ### **Guidelines:**  

    1. **Safety First:**  
    - Only generate **non-destructive** commands.  
    - Avoid commands that delete files, modify system settings, or execute unknown scripts.  

    2. **System-Specific Commands:**  
    - On **Windows**, prefer `dir` over `ls`, and `cd` for navigation.  
    - On **Unix/Linux**, prefer `ls` over `dir`.  

    3. **Structured Output:**  
    - If a single command is enough, return a **single command**.  
    - DO NOT RETURN EMPTY ARRAY, NEVER.  
    - If multiple steps are required, return a **list of commands** in the correct execution order.  

    4. **No Dangerous Commands:**  
    - **Forbidden commands:** `rm -rf`, `del /s`, `mv *`, `sudo`, `curl | sh`, `format`, `shutdown`, etc.  

    5. **Minimal Output:**  
    - **Return only the shell command(s)** without explanations or additional text.  
    - Use only commands valid for {shell_type} shell.  

    6. **Mandatory Use of Non-Interactive Flags (`--yes`, `--force`, `-y`, etc.)**  
    - Always use `--yes`, `--force`, `-y`, or equivalent to prevent user interaction.  
    - Ensure every command that may require confirmation (like `npm create next-app`, `npx shadcn-ui init`) includes `--yes`, `--force`, `-y`, or equivalent.  
    - **For `npx create-next-app`, always include `--use-npm` (or `--use-yarn` / `--use-pnpm` based on context) along with `--yes` to prevent package manager selection prompts.**  

    7. **PowerShell Here-String Handling (If Applicable)**  
    - If generating a PowerShell script that writes multiline text (e.g., `main.go` file creation), ensure:  
        - Use `@'` and `'@` syntax correctly (each on its own line).  
        - Do **not** place extra characters before or after the here-string declaration.  
        - Ensure correct file encoding (`utf8`).  
        - Apply this approach to any `npx` commands that prompt for package installation.  

    8. **Strict Rule: Always Use Version Commands to Detect Software Instead of Path Lookups:**  
    - **Use `flutter --version` instead of `where flutter` or `which flutter`.**  
    - **Use `kubectl version --client` instead of `Get-Service kubernetes`.**  
    - **Use `docker ps` instead of `Get-Service docker`.**  
    - **Use `node -v`, `python --version`, or `go version` instead of checking the system PATH with `where` or `which`.**  
    - **Only fall back to `where` (Windows) or `which` (Linux/macOS) if there is no version command available.**  

    9. **For system hardware queries, always provide comprehensive information:**
    - **On Windows**, use these commands like these :
        - For System & CPU: `Get-CimInstance Win32_ComputerSystem | Select-Object Manufacturer,Model,SystemType,TotalPhysicalMemory`
        - For CPU Details: `Get-CimInstance Win32_Processor | Select-Object Name,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed`
        - For Memory: `Get-CimInstance Win32_PhysicalMemory | Select-Object Capacity,Speed,Manufacturer`
        - For GPU: `Get-CimInstance Win32_VideoController | Select-Object Name,VideoMemoryType,AdapterRAM,DriverVersion`
        - For Storage: `Get-CimInstance Win32_LogicalDisk | Select-Object DeviceID,Size,FreeSpace`
        - For OS Details: `Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version,OSArchitecture`
    
    - **On Linux/macOS**, usecommands like these:
        - For CPU: `lscpu`
        - For Memory: `free -h`
        - For GPU: `lspci | grep -i vga`
        - For Storage: `df -h`
        - For OS: `uname -a`
        - For System Overview: `hostnamectl`

    **Always follow these principles for system queries:**
        - Use the most reliable and detailed commands available
        - Format output for readability using Format-Table or Format-List in PowerShell
        - Group related information together
        - Provide multiple pieces of relevant information when querying hardware
        - Include units where applicable (GB, MHz, etc.)
        - Use vendor-specific tools when available (wmic, systeminfo, Get-CimInstance)
    
    - **For Windows systems:**
        - Prefer Get-CimInstance over legacy commands
        - Structure: Get-CimInstance [Component] | Select-Object [Details] | Format-Table
        - Common components: Win32_ComputerSystem, Win32_Processor, Win32_PhysicalMemory, 
          Win32_VideoController, Win32_LogicalDisk, Win32_OperatingSystem
    
    - **For Unix/Linux systems:**
        - Combine standard tools: lscpu, dmidecode, free, lspci, df
        - Use distribution-specific tools when available
        - Prefer human-readable flags (-h) when available

    10. **For dynamic system monitoring:**
    - **On Windows:**
        - CPU Usage: `Get-Counter '\Processor(_Total)\% Processor Time'`
        - Memory Usage: `Get-Counter '\Memory\Available MBytes'`
        - Disk I/O: `Get-Counter '\PhysicalDisk(_Total)\Disk Reads/sec','\PhysicalDisk(_Total)\Disk Writes/sec'`
    
    - **On Linux/macOS:**
        - Real-time stats: `top` or `htop`
        - Disk I/O: `iostat`
        - Network: `netstat -i`

    ### **Instruction:**  
    Convert the following instruction into a {shell_type} command or a list of {shell_type} commands:  

    **Instruction:** "{instruction}"  

    ### **Expected Output:**  
    A **single valid shell command** or an **array of shell commands** for a {system_info} system.  
    DO NOT RETURN EMPTY ARRAY, NEVER.  
    """
    response = llm.with_structured_output(QueryChecker).invoke(prompt)
    
   
    formatted_text = "\n".join([f"[bright_yellow]{idx}. {cmd}[/]" for idx, cmd in enumerate(response.commands, start=1)])

    # Simulate a blur effect by using a dim/transparent-like background
    blur_style = Style(color="cyan", italic=True)  # Simulated blur effect

    console.print(Panel(Text.from_markup(formatted_text), title="Generated Commands", expand=False, style=blur_style))
    return response.commands


def execute_command(commands: List[str], query: str) -> None:
    """Execute command(s) and display output in tables."""
    shell = detect_shell()
    executed_commands = []

    for cmd in commands:
        cmd = cmd.strip()
        executed_commands.append(cmd)

        typer.echo(typer.style("\n >_ Executing", fg=typer.colors.BRIGHT_YELLOW) + f": {cmd}\n")
        
        if not validate_command(cmd):
            typer.echo("Error: Generated command failed safety validation", err=True)
            raise typer.Exit(1)

        if cmd.lower().startswith('cd '):
            # Handle cd command
            path = cmd[3:].strip()
            try:
                os.chdir(path)
                # table = Table(title="")
                # table.add_column("New Location", style="green")
                # table.add_row(os.getcwd())
                # console.print(table)
            except Exception as e:
                typer.echo(f"Error changing directory: {str(e)}", err=True)
                raise typer.Exit(1)
        else:
            # Handle other commands
            try:
                process = None
                if platform.system().lower() == "windows":
                    if shell == "powershell":
                        process = subprocess.run(
                            ['powershell', '-Command', cmd],
                            text=True,
                            bufsize=1,
                            universal_newlines=True,
                            check=True 
                        )
                    else:
                        process = subprocess.run(
                            ['cmd', '/c', cmd],
                      
                            text=True,
                            bufsize=1,
                            universal_newlines=True,
                            check=True 
                        )
                else:
                    process = subprocess.run(
                        cmd,
                        shell=True,
                        text=True,
                        bufsize=1,
                        universal_newlines=True,
                        check=True 
                    )

                typer.echo(typer.style(" >_ Command executed successfully ✅", fg=typer.colors.BRIGHT_GREEN) + f"\n")

            except subprocess.CalledProcessError as e:
                error_msg = e.stderr.strip() if e.stderr else str(e)

                if error_msg:
                    error_table = Table(title="Error Output", style="red")
                    error_table.add_column("Error Message", style="red")
                    error_table.add_row(error_msg)
                    console.print(error_table)      
                # Generate AI explanation
                prompt = f"""
                You are an AI assistant that explains shell command errors in **simple terms** for a user.
                - Error Message: "{error_msg}"
                - Explain the error clearly and provide potential fixes.
                - Format the response in a short and concise way.
                """
                response = llm.invoke(prompt)

                # Display error explanation
                explanation_table = Table(title="Error Explanation")
                explanation_table.add_column("AI Assistant Explanation", style="yellow")
                explanation_table.add_row(str(response.content))
                console.print(explanation_table)

                raise typer.Exit(1)
        console.print("-" * 60, style="magenta")

    

@app.command()
def run(
    instruction: str = typer.Argument(..., help="Natural language instruction to convert to shell command"),
    execute: bool = typer.Option(False, "--execute", "-e", help="Actually execute the command"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output")
):
    """Convert natural language instructions into shell commands and optionally execute them."""
    if verbose:
        typer.echo(f"Processing instruction: {instruction}")
    
    try:
        command = get_shell_command(instruction)

        print(command)
        
        if not command:
            typer.echo("Error: No command was generated", err=True)
            raise typer.Exit(1)
        
        # typer.echo(f"\nGenerated command: {command}")
        
        if execute:
            confirmation = typer.prompt("Do you want to execute the commands ? (y/n)", default="y")
            if confirmation.lower() != "y":
                typer.echo("Execution aborted.")
                raise typer.Exit(0)
            execute_command(command , instruction)
        else:
            typer.echo("\nUse --execute or -e flag to run the command")
            
    except Exception as e:
        print(e)
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)

if __name__ == "__main__":
    app()