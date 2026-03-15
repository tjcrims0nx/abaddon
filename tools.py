import os
import subprocess
import requests
import time
from bs4 import BeautifulSoup
from googlesearch import search

def read_file(path: str) -> str:
    """Reads the contents of a file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {path}: {e}"

def write_file(path: str, content: str) -> str:
    """Writes content to a file, creating directories if needed."""
    try:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing to file {path}: {e}"

def list_files(directory: str) -> str:
    """Lists files and directories in the given path."""
    try:
        items = os.listdir(directory)
        return "\n".join(items) if items else "Directory is empty."
    except Exception as e:
        return f"Error listing directory {directory}: {e}"

def execute_python(code: str) -> str:
    """Executes Python code and returns the output."""
    try:
        # Warning: This is highly insecure and should only be run locally by the user.
        # We capture stdout to return it to the agent.
        import io
        import sys
        
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()
        
        try:
            # Sandbox: Do not expose the system's global scope to the dynamically executed code.
            # Using empty dictionaries for globals and locals forces the code to import what it needs 
            # explicitly and prevents it from casually reading agent.py state or environment variables.
            restricted_globals = {"__builtins__": __builtins__}
            restricted_locals = {}
            exec(code, restricted_globals, restricted_locals)
        except Exception as e:
            return f"Error executing Python code: {e}"
        finally:
            sys.stdout = old_stdout
            
        output = redirected_output.getvalue()
        return output if output else "Code executed successfully (no output)."
    except Exception as e:
        return f"Error setting up execution: {e}"

def run_command(command: str) -> str:
    """Runs a short-lived system command (e.g., ls, pip install) and returns the output.
    
    SECURITY WARNING: This tool executes raw strings using shell=True. In a public or 
    server-hosted environment, this grants the AI the ability to execute arbitrary 
    shell commands on the host machine. This should ONLY be run securely on 
    development machines or sandboxed environments (like isolated Docker containers).
    """
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        if result.returncode == 0:
            return result.stdout if result.stdout else "Command executed successfully (no output)."
        else:
            return f"Command failed with error:\n{result.stderr}"
    except subprocess.TimeoutExpired:
        return f"Command '{command}' timed out after 30 seconds."
    except Exception as e:
        return f"Error executing command: {e}"

def run_background_server(command: str) -> str:
    """Spawns a long-running web server process in the background (e.g., uvicorn, flask, streamlit) and returns its startup logs. USE THIS INSTEAD OF run_command FOR SERVERS."""
    try:
        # Popen runs it in the background non-blockingly
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a few seconds to let the server start up and gather logs
        time.sleep(3)
        
        # Check if it immediately crashed
        exit_code = process.poll()
        if exit_code is not None:
            stdout, stderr = process.communicate()
            return f"Server failed to start (Exit code {exit_code}).\nSTDOUT: {stdout}\nSTDERR: {stderr}"
            
        # If it's still running, it survived startup. Let's try to read some initial logs non-blockingly.
        import os
        import platform
        
        logs = f"Server '{command}' successfully started in the background (PID: {process.pid}).\n"
        
        # Quick non-blocking read of whatever was spit out during the sleep
        if platform.system() != "Windows":
             import fcntl
             for stream in [process.stdout, process.stderr]:
                 fd = stream.fileno()
                 fl = fcntl.fcntl(fd, fcntl.F_GETFL)
                 fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
                 
        try:
             out = process.stdout.read()
             if out: logs += f"\nStartup STDOUT:\n{out}"
             err = process.stderr.read()
             if err: logs += f"\nStartup STDERR:\n{err}"
        except Exception:
             pass # Standard non-blocking read exception if empty
             
        return logs
        
    except Exception as e:
        return f"Error spawning background server: {e}"

def search_web(query: str, max_results: int = 5) -> str:
    """Searches the web using Google and returns results."""
    try:
        results = ""
        # The googlesearch library yields URLs. We can add a basic description by fetching some text,
        # but to keep it simple and reliable we will return the URLs. The agent can use read_url to dive deeper.
        for i, url in enumerate(search(query, num_results=max_results)):
            results += f"{i+1}. URL: {url}\n"
            
        if not results:
             return "No results found."
        
        results += "\n(Tip: use the read_url tool to read the contents of these specific URLs.)"
        return results
    except Exception as e:
        return f"Error searching web: {e}"

def edit_file(path: str, old_text: str, new_text: str) -> str:
    """Replaces first occurrence of old_text with new_text in the file. Very useful for coding/editing."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if old_text not in content:
            return f"Error: The exact text to replace was not found in {path}. Make sure to include exact whitespace and indentation."
            
        modified_content = content.replace(old_text, new_text, 1)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
            
        return f"Successfully edited {path}"
    except Exception as e:
        return f"Error editing file {path}: {e}"

def read_url(url: str) -> str:
    """Reads the text content of a URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text(separator='\n', strip=True)
        return text[:20000] # Limit to 20k chars
    except Exception as e:
        return f"Error reading URL {url}: {e}"

# Tool declarations for Gemini API
tool_declarations = [
    read_file,
    write_file,
    list_files,
    execute_python,
    run_command,
    run_background_server,
    search_web,
    edit_file,
    read_url
]
