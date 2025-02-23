import os
import platform
import subprocess


def validate_command(command: str) -> bool:
    """Basic safety validation of the generated command."""
    dangerous_commands = ['rm -rf', 'mkfs', ':(){:|:&};:', '> /dev/sda',
                        'dd if=/dev/zero', 'chmod -R 777', '$(', '`',
                        'eval', 'exec', 'del /f', 'deltree']
    
    return not any(dangerous in command.lower() for dangerous in dangerous_commands)

def detect_shell() -> str:
    """Detect which shell is being used."""
    if platform.system().lower() == "windows":
        # Check if PowerShell is being used
        try:
            result = subprocess.run(
                ['echo', '$PSVersionTable'],
                shell=True,
                text=True,
                capture_output=True
            )
            if result.returncode == 0 and 'PSVersion' in result.stdout:
                return "powershell"
            return "cmd"
        except:
            return "cmd"
    else:
        # Check for bash/other shells on Unix
        shell = os.environ.get('SHELL', '')
        if 'bash' in shell.lower():
            return "bash"
        elif 'zsh' in shell.lower():
            return "zsh"
        return "sh"  # default to sh


# def split_commands(command_string: str) -> List[str]:
#     """Split compound commands into individual commands."""
#     # Split on && while preserving quoted strings
#     commands = []
#     current_command = ""
#     in_quotes = False
#     quote_char = None
    
#     for char in command_string:
#         if char in ['"', "'"]:
#             if not in_quotes:
#                 in_quotes = True
#                 quote_char = char
#             elif quote_char == char:
#                 in_quotes = False
#                 quote_char = None
        
#         if char == '&' and not in_quotes:
#             if current_command.endswith('&'):
#                 commands.append(current_command[:-1].strip())
#                 current_command = ""
#             else:
#                 current_command += char
#         else:
#             current_command += char
    
#     if current_command:
#         commands.append(current_command.strip())
    
#     return commands
