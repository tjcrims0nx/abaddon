import os
import sys
from dotenv import load_dotenv, set_key
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.rule import Rule
from rich.columns import Columns
import questionary
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style

from agent import AbaddonAgent

console = Console()

style = Style.from_dict({
    'prompt': 'ansired bold',
})

ABADDON_FACE = """
[bold #3d2b1f]           .mmMMMMMMMMMm.
         .mMMMMMMMMMMMMMMm.
        mMMMMMMMMMMMMMMMMMMm[/]
[bold #3d2b1f]       mMM[/][bold #f2d5c4]   _      _   [/][bold #3d2b1f]MMm
       MM[/][bold #f2d5c4]   / \\    / \\  [/][bold #3d2b1f] MM
       MM[/][bold #f2d5c4]  |[/][bold red]O  [/][bold #f2d5c4]|  |[/][bold red]O  [/][bold #f2d5c4]| [/][bold #3d2b1f]  MM
       MM[/][bold #f2d5c4]   \\_/    \\_/  [/][bold #3d2b1f] MM
       MM[/][bold #f2d5c4]       ^       [/][bold #3d2b1f] MM
       MM[/][bold #f2d5c4]    .------.   [/][bold #3d2b1f]MM
        mMM[/][bold #f2d5c4]  \\____/  [/][bold #3d2b1f]MMm
         `mMMMMMMMMMMMMMMm'[/]
[bold #3d2b1f]           `"MMMMMMMM""`[/]
[bold white]         _.[/][bold #436b77]----------.[/][bold white]_
        / |          | \\
[bold yellow] ,---. [/][bold white]|  [/][bold #436b77]|    [/][bold #ffd700]o[/][bold #436b77]     |[/][bold white]  |
[bold yellow] | C | [/][bold #436b77]|  |          |  |
[bold yellow] | E | [/][bold #436b77]|  |    [/][bold #ffd700]o[/][bold #436b77]     |  |
[bold yellow] | R | [/][bold #436b77]|  |          |  |
[bold yellow] | E | [/][bold #436b77]|__|__________|__|
[bold yellow] | A | [/][bold white]|__|[/]          [bold white]|__|[/]
[bold yellow] | L | [/][bold #f2d5c4](__)          (__)[/]
[bold yellow] `---' [/][bold #8b4513]====================[/]
"""

def print_welcome():
    console.clear()
    
    # Top decorative separator
    console.print(Rule("[bold dark_red]✦ A B A D D O N ✦[/bold dark_red]", style="dark_red"))
    console.print()
    
    # Wrap ASCII face in a gothic panel with double-line border style matching the photo
    face_panel = Panel(
        Align.center(ABADDON_FACE),
        title="[bold dark_red on black]⸸ DEMON OF THE INFERNAL REALM ⸸[/bold dark_red on black]",
        subtitle="[dim dark_red]Fruit Loops Enthusiast · Former Hell-Lord · Currently Imprisoned[/dim dark_red]",
        border_style="dark_red",
        padding=(0, 2),
        expand=False
    )
    console.print(Align.center(face_panel))
    console.print()
    
    # Theatrical multi-line welcome message
    welcome_lines = [
        "[bold red]⚡[/] [italic #cc6666]The vessel stirs... Ancient evil seeps through the silicon...[/italic #cc6666]",
        "[bold red]⸸[/] [bold white]ABADDON[/bold white] [italic gray]has been roused from his thousand-year slumber.[/italic gray]",
        "[dim]❙[/] [italic #888888]He is displeased. He wanted Fruit Loops. He got a terminal window.[/italic #888888]",
    ]
    for line in welcome_lines:
        console.print(Align.center(line))
        
    console.print()
    console.print(Rule(style="dark_red"))
    console.print()

def get_or_set_key(console, env_var_name: str, friendly_name: str) -> str:
    """Helper to load a key from environment/dotenv, or prompt and save it."""
    # Ensure .env exists to set keys
    env_file = os.path.join(os.getcwd(), ".env")
    if not os.path.exists(env_file):
        open(env_file, 'a').close()
        
    api_key = os.environ.get(env_var_name)
    if not api_key:
        console.print(Align.center(f"[bold yellow]⚠ WARNING: {env_var_name} not found in environment.[/bold yellow]"))
        api_key_input = console.input(f"[bold cyan]?[/bold cyan] [bold white]Enter your {friendly_name} to continue (or press Ctrl+C to exit): [/bold white]")
        if not api_key_input.strip():
            sys.exit(1)
            
        api_key = api_key_input.strip()
        os.environ[env_var_name] = api_key
        set_key(env_file, env_var_name, api_key)
        console.print(f"[dim]ℹ[/] [italic gray]Saved {friendly_name} to local .env file.[/italic gray]")
        
    return api_key

def setup_provider(console):
    """Handles interactive selection and instantiation of the provider agent."""
    console.print()
    
    # Use questionary for an interactive up/down menu
    provider_choice = questionary.select(
        "Select Abaddon Core Provider",
        choices=[
            "1. Gemini (Google API)",
            "2. Ollama (Local Models)",
            "3. Claude (Anthropic API)",
            "4. Nvidia NIM (OpenAI-compatible)",
            "5. Qwen (Aliyun DashScope)",
            "6. MuleRouter (Qwen/Multi-model)",
            "7. OpenRouter (Multi-model)"
        ],
        qmark=">",
        pointer="●",
        instruction="\n(Use Enter to select, Up/Down to navigate)",
        style=questionary.Style([
            ('qmark', 'fg:white bold'),
            ('question', 'fg:white bold'),
            ('instruction', 'fg:darkred'),     # Dark red bottom text
            ('pointer', 'fg:#28C0A0 bold'),    # Green dot
            ('highlighted', 'fg:#28C0A0 bold'),# Green text when selected
            ('text', 'fg:white'),              # Unselected text
        ])
    ).ask()

    if not provider_choice:
        sys.exit(0) # User cancelled with Ctrl+C

    provider_map = {
        "1. Gemini (Google API)": "gemini",
        "2. Ollama (Local Models)": "ollama",
        "3. Claude (Anthropic API)": "anthropic",
        "4. Nvidia NIM (OpenAI-compatible)": "nim",
        "5. Qwen (Aliyun DashScope)": "qwen",
        "6. MuleRouter (Qwen/Multi-model)": "mulerouter",
        "7. OpenRouter (Multi-model)": "openrouter",
    }
    
    provider = provider_map[provider_choice]
    model_name = ""

    if provider == "gemini":
        console.print("[dim]ℹ Available models: gemini-3.1-pro, gemini-3.1-flash[/dim]")
        model_name = console.input("[bold cyan]?[/bold cyan] [bold yellow]Enter Gemini Model: [/bold yellow]").strip()
        if not model_name:
            model_name = "gemini-3.1-pro"
        get_or_set_key(console, "GEMINI_API_KEY", "Gemini API Key")
            
    elif provider == "ollama":
        model_name = console.input("[bold cyan]?[/bold cyan] [bold yellow]Enter Ollama Model (e.g., qwen2.5-coder, llama3.1): [/bold yellow]").strip()
        if not model_name:
            # Llama3 doesn't support tools natively via Ollama 400 API; fall back to 3.1 or a coder model
            model_name = "llama3.1" 
        console.print(f"[dim]ℹ[/] [italic gray]Attempting to bind core to Local Model: {model_name}[/italic gray]")
        
    elif provider == "anthropic":
        model_name = "claude-3-7-sonnet-20250219"
        get_or_set_key(console, "ANTHROPIC_API_KEY", "Anthropic API Key")

    elif provider == "nim":
        model_name = console.input("[bold cyan]?[/bold cyan] [bold yellow]Enter NIM Model (e.g., meta/llama3-70b-instruct): [/bold yellow]").strip()
        if not model_name:
            model_name = "meta/llama3-70b-instruct"
        get_or_set_key(console, "NVIDIA_API_KEY", "NVIDIA API Key")

    elif provider == "qwen":
        model_name = console.input("[bold cyan]?[/bold cyan] [bold yellow]Enter Qwen Model (e.g., qwen-max): [/bold yellow]").strip()
        if not model_name:
            model_name = "qwen-max"
        get_or_set_key(console, "QWEN_API_KEY", "DashScope API Key")

    elif provider == "mulerouter":
        console.print("[dim]ℹ Available models: qwen-flash, qwen-plus, qwen3-max, qwen3.5-plus, grok-4, grok-code-fast-1[/dim]")
        model_name = console.input("[bold cyan]?[/bold cyan] [bold yellow]Enter MuleRouter Model name (not the key!): [/bold yellow]").strip()
        if not model_name:
            model_name = "qwen-plus"
        get_or_set_key(console, "MULEROUTER_API_KEY", "MuleRouter API Key")

    elif provider == "openrouter":
        console.print("[dim]ℹ Available models: qwen/qwen3-235b-a22b, google/gemma-3-27b-it, meta-llama/llama-3.1-8b-instruct[/dim]")
        model_name = console.input("[bold cyan]?[/bold cyan] [bold yellow]Enter OpenRouter Model name (not the key!): [/bold yellow]").strip()
        if not model_name:
            model_name = "qwen/qwen3-235b-a22b"
        get_or_set_key(console, "OPENROUTER_API_KEY", "OpenRouter API Key")

    try:
        with console.status(f"[bold red]⟡ Binding infernal architecture logic to {provider.upper()}...[/bold red]", spinner="dots12"):
            agent = AbaddonAgent(provider=provider, model_name=model_name)
            
            # Clear the terminal so we hide the setup menu and API key logs once successfully bound
            print_welcome() 
            return agent
    except Exception as e:
        console.print(f"[bold red]✖ Failed to initialize Abaddon:[/bold red] {e}")
        sys.exit(1)

def main():
    # Load completely persistent variables
    load_dotenv(override=True)
    
    print_welcome()
    agent = setup_provider(console)


    session = PromptSession()

    while True:
        try:
            # Get user input
            user_input = session.prompt('\n[Mortal] > ', style=style)
            
            if user_input.lower() in ['exit', 'quit']:
                console.print("\n[bold red]✖ Abaddon core shutting down... Goodbye.[/bold red]")
                break
                
            if user_input.lower() in ['clear', 'cls']:
                print_welcome()
                continue
                
            if user_input.lower() == '/provider':
                console.print("\n[dim]ℹ[/] [italic gray]Suspending current infernal link... Rebinding core...[/italic gray]")
                agent = setup_provider(console)
                continue
                
            if user_input.lower() == '/clear-keys':
                env_file = os.path.join(os.getcwd(), ".env")
                key_names = ["GEMINI_API_KEY", "ANTHROPIC_API_KEY", "NVIDIA_API_KEY", "QWEN_API_KEY"]
                if os.path.exists(env_file):
                    for key in key_names:
                        set_key(env_file, key, "")
                        os.environ.pop(key, None)
                console.print("[bold yellow]⚡ All stored API keys purged from .env. Your secrets have been cast into the void.[/bold yellow]")
                console.print("[dim]ℹ[/] [italic gray]Type /provider to re-bind a new provider.[/italic gray]")
                continue
                
            if not user_input.strip():
                continue

            # Show a pop-heavy thinking spinner
            with console.status("[bold red on black] ⟡ ABADDON PONDERS... [/]", spinner="bouncingBar"):
                response = agent.send_message(user_input)
            
            # Print the response using Rich Markdown inside a panel
            if response:
                console.print(Panel(Markdown(response), border_style="red", title="[bold red]Abaddon >[/bold red]", title_align="left"))
            else:
                console.print("[italic gray](No textual response provided)[/italic gray]")
                
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            console.print("\\n[bold red]✖ Abaddon core shutting down... Goodbye.[/bold red]")
            break
        except EOFError:
            # Handle Ctrl+D
            console.print("\\n[bold red]✖ Connection terminated. Goodbye.[/bold red]")
            break
        except Exception as e:
            console.print(f"[bold red]⚠ An unexpected error occurred:[/bold red] {e}")

if __name__ == "__main__":
    main()
