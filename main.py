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

    _qstyle = questionary.Style([
        ('qmark', 'fg:red bold'),
        ('question', 'fg:yellow bold'),
        ('answer', 'fg:cyan bold'),
        ('pointer', 'fg:red bold'),
        ('highlighted', 'fg:white bold bg:darkred'),
        ('selected', 'fg:cyan'),
    ])

    if provider == "gemini":
        model_name = questionary.select(
            "Select Gemini Model:",
            choices=["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash", "gemini-1.5-pro"],
            style=_qstyle
        ).ask() or "gemini-2.5-flash"
        get_or_set_key(console, "GEMINI_API_KEY", "Gemini API Key")
            
    elif provider == "ollama":
        # Dynamically detect installed Ollama models
        import subprocess as _sp
        _detected_models = []
        try:
            _result = _sp.run("ollama list", shell=True, capture_output=True, text=True, timeout=5)
            for _line in _result.stdout.splitlines()[1:]:  # skip header row
                _parts = _line.split()
                if _parts:
                    _detected_models.append(_parts[0])  # e.g. "qwen3.5:latest"
        except Exception:
            pass

        if _detected_models:
            _ollama_choices = _detected_models + ["Other (type below)"]
            console.print(f"[dim]ℹ[/] [italic gray]Detected {len(_detected_models)} installed Ollama model(s).[/italic gray]")
        else:
            _ollama_choices = ["llama3.1", "qwen2.5-coder", "mistral", "deepseek-r1", "Other (type below)"]
            console.print("[dim]ℹ[/] [italic gray]Could not reach Ollama — showing default models.[/italic gray]")

        model_name = questionary.select(
            "Select Ollama Model:",
            choices=_ollama_choices,
            style=_qstyle
        ).ask() or _ollama_choices[0]
        if model_name == "Other (type below)":
            model_name = console.input("[bold cyan]?[/bold cyan] [bold yellow]Enter Ollama Model name: [/bold yellow]").strip() or "llama3.1"
        console.print(f"[dim]ℹ[/] [italic gray]Attempting to bind core to Local Model: {model_name}[/italic gray]")
        
    elif provider == "anthropic":
        model_name = questionary.select(
            "Select Claude Model:",
            choices=["claude-3-7-sonnet-20250219", "claude-3-5-sonnet-20241022", "claude-3-haiku-20240307"],
            style=_qstyle
        ).ask() or "claude-3-7-sonnet-20250219"
        get_or_set_key(console, "ANTHROPIC_API_KEY", "Anthropic API Key")

    elif provider == "nim":
        model_name = questionary.select(
            "Select NIM Model:",
            choices=["meta/llama3-70b-instruct", "meta/llama3-8b-instruct", "mistralai/mistral-7b-instruct-v0.3", "Other (type below)"],
            style=_qstyle
        ).ask() or "meta/llama3-70b-instruct"
        if model_name == "Other (type below)":
            model_name = console.input("[bold cyan]?[/bold cyan] [bold yellow]Enter NIM Model name: [/bold yellow]").strip() or "meta/llama3-70b-instruct"
        get_or_set_key(console, "NVIDIA_API_KEY", "NVIDIA API Key")

    elif provider == "qwen":
        model_name = questionary.select(
            "Select Qwen Model:",
            choices=["qwen-max", "qwen-plus", "qwen-turbo", "qwen-long"],
            style=_qstyle
        ).ask() or "qwen-max"
        get_or_set_key(console, "QWEN_API_KEY", "DashScope API Key")

    elif provider == "mulerouter":
        model_name = questionary.select(
            "Select MuleRouter Model:",
            choices=["qwen-plus", "qwen-flash", "qwen3-max", "qwen3.5-plus", "grok-4", "grok-code-fast-1"],
            style=_qstyle
        ).ask() or "qwen-plus"
        get_or_set_key(console, "MULEROUTER_API_KEY", "MuleRouter API Key")

    elif provider == "openrouter":
        model_name = questionary.select(
            "Select OpenRouter Model:",
            choices=["qwen/qwen3-235b-a22b", "google/gemma-3-27b-it", "meta-llama/llama-3.1-8b-instruct", "Other (type below)"],
            style=_qstyle
        ).ask() or "qwen/qwen3-235b-a22b"
        if model_name == "Other (type below)":
            model_name = console.input("[bold cyan]?[/bold cyan] [bold yellow]Enter OpenRouter Model name: [/bold yellow]").strip() or "qwen/qwen3-235b-a22b"
        get_or_set_key(console, "OPENROUTER_API_KEY", "OpenRouter API Key")

    try:
        with console.status(f"[bold red]⟡ Binding infernal architecture logic to {provider.upper()}...[/bold red]", spinner="dots12"):
            agent = AbaddonAgent(provider=provider, model_name=model_name)
            
            # Clear the terminal so we hide the setup menu and API key logs once successfully bound
            print_welcome() 
            return agent, provider, model_name
    except Exception as e:
        console.print(f"[bold red]✖ Failed to initialize Abaddon:[/bold red] {e}")
        sys.exit(1)

def main():
    # Load completely persistent variables
    load_dotenv(override=True)
    
    print_welcome()

    # --- First-run: check system access permission ---
    _env_file = os.path.join(os.getcwd(), ".env")
    if os.environ.get("ABADDON_SYSTEM_ACCESS") is None:
        console.print()
        console.print("[bold dark_red]✶ FIRST RUN: SYSTEM ACCESS PERMISSION ✶[/bold dark_red]")
        console.print("[dark_red]" + "─" * 50 + "[/dark_red]")
        console.print("[white]Granting system access allows Abaddon to:[/white]")
        console.print("  [dim]• Read/write/delete files anywhere on the filesystem[/dim]")
        console.print("  [dim]• Execute system commands without asking[/dim]")
        console.print("  [dim]• Install packages and spawn processes[/dim]")
        console.print("[yellow]You can change this later with [bold]/settings[/bold][/yellow]")
        console.print("[dark_red]" + "─" * 50 + "[/dark_red]")
        _grant = questionary.select(
            "Grant Abaddon full system access?",
            choices=[
                questionary.Choice("Yes — Full autonomy (recommended for power users)", value="true"),
                questionary.Choice("No — Restricted mode (safer, may ask before acting)", value="false"),
            ],
            style=questionary.Style([('qmark', 'fg:red bold'), ('question', 'fg:yellow bold'), ('pointer', 'fg:#28C0A0 bold'), ('highlighted', 'fg:#28C0A0 bold')])
        ).ask() or "false"
        set_key(_env_file, "ABADDON_SYSTEM_ACCESS", _grant)
        os.environ["ABADDON_SYSTEM_ACCESS"] = _grant
        load_dotenv(override=True)
        console.print(f"[bold green]✔ System access set to: {'GRANTED' if _grant == 'true' else 'RESTRICTED'}[/bold green]")
        console.print()

    agent, current_provider, current_model = setup_provider(console)


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
                agent, current_provider, current_model = setup_provider(console)
                continue

            if user_input.lower() in ['/help', '/h', '/?']:
                console.print()
                console.print("[bold dark_red]✶ ABADDON COMMAND LIST ✶[/bold dark_red]")
                console.print("[dark_red]" + "─" * 50 + "[/dark_red]")
                commands = [
                    ("/help",         "Show this command list"),
                    ("/provider",     "Switch AI provider / model"),
                    ("/settings",     "Toggle permissions (system access, etc.)"),
                    ("/api-key",      "Update an API key"),
                    ("/skills",       "Search & install skills from ClawHub"),
                    ("/run-skill",    "Run an installed OpenClaw skill directly"),
                    ("/sync-skills",  "Sync skill_list.md and install missing skills"),
                    ("/clear-keys",   "Wipe all stored API keys from .env"),
                    ("clear / cls",   "Clear the terminal"),
                    ("exit / quit",   "Exit Abaddon"),
                ]
                for cmd, desc in commands:
                    console.print(f"  [bold red]{cmd:<18}[/bold red] [white]{desc}[/white]")
                console.print("[dark_red]" + "─" * 50 + "[/dark_red]")
                console.print()
                continue

            if user_input.lower() in ['/sync-skills', '/sync']:
                from skill_manager import sync_skills
                with console.status("[bold red]⟡ Syncing Infernal Skills...[/bold red]", spinner="bouncingBar"):
                    sync_skills()
                console.print("[bold green]✔ Skills synced![/bold green] [dim]Type /provider to reload the agent with any new skills.[/dim]")
                continue

            if user_input.lower() in ['/settings', '/setting']:
                _env_file = os.path.join(os.getcwd(), ".env")
                _current_access = os.environ.get("ABADDON_SYSTEM_ACCESS", "false") == "true"
                console.print()
                console.print("[bold dark_red]✶ ABADDON SETTINGS ✶[/bold dark_red]")
                console.print("[dark_red]" + "─" * 50 + "[/dark_red]")
                console.print(f"  System Access: [bold {'green' if _current_access else 'red'}]{'GRANTED' if _current_access else 'RESTRICTED'}[/bold {'green' if _current_access else 'red'}]")
                console.print("[dark_red]" + "─" * 50 + "[/dark_red]")
                _setting_choice = questionary.select(
                    "What would you like to change?",
                    choices=[
                        questionary.Choice(
                            f"{'Revoke' if _current_access else 'Grant'} system access",
                            value="toggle_access"
                        ),
                        questionary.Choice("Cancel", value=None),
                    ],
                    style=questionary.Style([('qmark', 'fg:red bold'), ('question', 'fg:yellow bold'), ('pointer', 'fg:#28C0A0 bold'), ('highlighted', 'fg:#28C0A0 bold')])
                ).ask()

                if _setting_choice == "toggle_access":
                    _new_val = "false" if _current_access else "true"
                    set_key(_env_file, "ABADDON_SYSTEM_ACCESS", _new_val)
                    os.environ["ABADDON_SYSTEM_ACCESS"] = _new_val
                    load_dotenv(override=True)
                    _label = "GRANTED — Full autonomy enabled" if _new_val == "true" else "RESTRICTED — Safer mode"
                    console.print(f"[bold green]✔ System access: {_label}[/bold green]")
                    console.print("[dim]ℹ[/] [italic gray]Reloading Abaddon with updated permissions...[/italic gray]")
                    try:
                        with console.status(f"[bold red]⟡ Rebinding to {current_provider.upper()}...[/bold red]", spinner="dots12"):
                            agent = AbaddonAgent(provider=current_provider, model_name=current_model)
                        console.print("[bold green]✔ Abaddon reloaded.[/bold green]")
                    except Exception as _e:
                        console.print(f"[bold red]✖ Reload failed:[/bold red] {_e}")
                continue

            if user_input.lower() in ['/run-skill', '/run']:
                import subprocess, os as _os
                # Find installed skills in the skills/ directory
                skills_dir = _os.path.join(_os.getcwd(), "skills")
                _skill_dirs = []
                if _os.path.isdir(skills_dir):
                    for _d in _os.listdir(skills_dir):
                        _skill_path = _os.path.join(skills_dir, _d)
                        if _os.path.isdir(_skill_path):
                            _skill_dirs.append(_d)

                if not _skill_dirs:
                    console.print("[italic gray]No installed OpenClaw skills found. Use /skills to install some.[/italic gray]")
                    continue

                _skill_choices = [questionary.Choice(title=s, value=s) for s in sorted(_skill_dirs)]
                _skill_choices.append(questionary.Choice(title="↩  Cancel", value=None))

                chosen_skill = questionary.select(
                    "Select a skill to run:",
                    choices=_skill_choices,
                    style=questionary.Style([
                        ('qmark',       'fg:red bold'),
                        ('question',    'fg:yellow bold'),
                        ('pointer',     'fg:#28C0A0 bold'),
                        ('highlighted', 'fg:#28C0A0 bold'),
                    ])
                ).ask()

                if chosen_skill:
                    _skill_path = _os.path.join(skills_dir, chosen_skill)
                    # Check for a run.sh / run.py / scripts/run entry
                    _entry = None
                    for _candidate in ["run.py", "run.sh", "scripts/run.py", "scripts/run.sh"]:
                        _fp = _os.path.join(_skill_path, _candidate)
                        if _os.path.isfile(_fp):
                            _entry = _fp
                            break

                    if _entry:
                        console.print(f"[bold red]⟡ Running skill: {chosen_skill}...[/bold red]")
                        subprocess.run(["python", _entry] if _entry.endswith(".py") else ["bash", _entry])
                    else:
                        # Fall back to reading SKILL.md and asking Abaddon to act on it
                        _skill_md = _os.path.join(_skill_path, "SKILL.md")
                        if _os.path.isfile(_skill_md):
                            with open(_skill_md, "r", encoding="utf-8") as _f:
                                _md = _f.read()
                            console.print(f"\n[bold dark_red]✶ Skill:[/bold dark_red] [white]{chosen_skill}[/white]")
                            _task_input = console.input("[bold cyan]?[/bold cyan] [bold white]What do you want Abaddon to do with this skill? [/bold white]").strip()
                            if not _task_input:
                                console.print("[italic gray]Cancelled.[/italic gray]")
                            else:
                                prompt = f"[System: You are activating the '{chosen_skill}' OpenClaw skill. Use its instructions below to complete the user's task.]\n\nSkill Instructions:\n{_md}\n\nUser Task:\n{_task_input}"
                                with console.status("[bold red]⟡ Abaddon is executing the skill...[/bold red]", spinner="bouncingBar"):
                                    response = agent.send_message(prompt)
                                console.print(f"\n[bold dark_red]Abaddon[/bold dark_red]\n{response}")
                        else:
                            console.print(f"[italic gray]No entry point or SKILL.md found in '{chosen_skill}'.[/italic gray]")
                continue

            if user_input.lower() in ['/skills', '/skill']:
                import subprocess
                query = console.input("[bold cyan]?[/bold cyan] [bold white]Search ClawHub for skills (or press Enter to browse): [/bold white]").strip()
                
                with console.status("[bold red]⟡ Consulting the Infernal Skill Registry...[/bold red]", spinner="bouncingBar"):
                    try:
                        if query:
                            result = subprocess.run(f'clawhub search "{query}"', shell=True, capture_output=True, text=True)
                        else:
                            result = subprocess.run("clawhub list", shell=True, capture_output=True, text=True)
                    except Exception as e:
                        console.print(f"[bold red]✖ Failed to query ClawHub: {e}[/bold red]")
                        continue
                        
                output = result.stdout.strip() if result.returncode == 0 else result.stderr.strip()
                
                if not output:
                    console.print("[italic gray]No skills found.[/italic gray]")
                    continue

                # Parse lines: "slug  Name  (score)"
                skill_choices = []
                for line in output.splitlines():
                    parts = line.split()
                    if parts:
                        slug = parts[0]
                        name = " ".join(p for p in parts[1:] if not p.startswith("("))
                        label = f"{slug:<30} {name}" if name else slug
                        skill_choices.append(questionary.Choice(title=label, value=slug))

                if not skill_choices:
                    console.print("[italic gray]Could not parse any skills from results.[/italic gray]")
                    console.print(f"[dim]{output}[/dim]")
                    continue

                skill_choices.append(questionary.Choice(title="↩  Cancel", value=None))

                chosen_slug = questionary.select(
                    "Select a skill to install:",
                    choices=skill_choices,
                    style=questionary.Style([
                        ('qmark',       'fg:red bold'),
                        ('question',    'fg:yellow bold'),
                        ('pointer',     'fg:#28C0A0 bold'),
                        ('highlighted', 'fg:#28C0A0 bold'),
                        ('text',        'fg:white'),
                    ])
                ).ask()

                if chosen_slug:
                    with console.status(f"[bold red]⟡ Installing {chosen_slug}...[/bold red]", spinner="bouncingBar"):
                        install_result = subprocess.run(f'clawhub install "{chosen_slug}"', shell=True, capture_output=True, text=True)
                    
                    if install_result.returncode == 0:
                        console.print(f"[bold green]✔ Installed '{chosen_slug}' successfully![/bold green]")
                        # Append to skill_list.md
                        skill_list_path = os.path.join(os.getcwd(), "skill_list.md")
                        try:
                            with open(skill_list_path, "r", encoding="utf-8") as f:
                                existing = f.read()
                            if chosen_slug not in existing:
                                with open(skill_list_path, "a", encoding="utf-8") as f:
                                    f.write(f"\n- {chosen_slug}")
                                console.print(f"[dim]ℹ[/] [italic gray]Added '{chosen_slug}' to skill_list.md for future sessions.[/italic gray]")
                        except Exception:
                            pass
                        console.print("[dim]ℹ[/] [italic gray]Reloading Abaddon with new skill...[/italic gray]")
                        try:
                            with console.status(f"[bold red]⟡ Rebinding to {current_provider.upper()}...[/bold red]", spinner="dots12"):
                                agent = AbaddonAgent(provider=current_provider, model_name=current_model)
                            console.print("[bold green]✔ Abaddon reloaded with new skill![/bold green]")
                        except Exception as _e:
                            console.print(f"[bold red]✖ Reload failed:[/bold red] {_e}")
                    else:
                        console.print(f"[bold red]✖ Failed to install:[/bold red] {install_result.stderr.strip()}")
                continue

                
            if user_input.lower() in ['/api-key', '/apikey', '/token']:
                env_file = os.path.join(os.getcwd(), ".env")
                key_choice = questionary.select(
                    "Which API Key do you wish to update?",
                    choices=[
                        "GEMINI_API_KEY",
                        "ANTHROPIC_API_KEY",
                        "NVIDIA_API_KEY",
                        "QWEN_API_KEY",
                        "MULEROUTER_API_KEY",
                        "OPENROUTER_API_KEY"
                    ],
                    style=questionary.Style([('qmark', 'fg:red bold'), ('question', 'fg:yellow bold')])
                ).ask()
                
                if key_choice:
                    new_key = console.input(f"[bold cyan]?[/bold cyan] [bold white]Enter new {key_choice}: [/bold white]").strip()
                    if new_key:
                        os.environ[key_choice] = new_key
                        set_key(env_file, key_choice, new_key)
                        console.print(f"[dim]ℹ[/] [italic gray]Updated {key_choice} successfully.[/italic gray]")
                        console.print("[dim]ℹ[/] [italic gray]You may need to run /provider to bind the core with the new key.[/italic gray]")
                continue
                
            if user_input.lower() == '/clear-keys':
                env_file = os.path.join(os.getcwd(), ".env")
                key_names = ["GEMINI_API_KEY", "ANTHROPIC_API_KEY", "NVIDIA_API_KEY", "QWEN_API_KEY", "MULEROUTER_API_KEY", "OPENROUTER_API_KEY"]
                if os.path.exists(env_file):
                    for key in key_names:
                        set_key(env_file, key, "")
                        os.environ.pop(key, None)
                console.print("[bold yellow]⚡ All stored API keys purged from .env. Your secrets have been cast into the void.[/bold yellow]")
                console.print("[dim]ℹ[/] [italic gray]Type /provider to re-bind a new provider.[/italic gray]")
                continue
                
            if not user_input.strip():
                continue

            # Run agent in a background thread so Ctrl+C can cancel mid-call
            import threading
            _result = [None]
            _error = [None]
            def _call_agent():
                try:
                    _result[0] = agent.send_message(user_input)
                except Exception as e:
                    _error[0] = e

            _thread = threading.Thread(target=_call_agent, daemon=True)
            _thread.start()
            try:
                with console.status("[bold red on black] ⟡ ABADDON PONDERS... (Ctrl+C to cancel) [/]", spinner="bouncingBar"):
                    while _thread.is_alive():
                        _thread.join(timeout=0.1)
            except KeyboardInterrupt:
                console.print("\n[bold yellow]⚡ Abaddon's thought interrupted. The demon is displeased.[/bold yellow]")
                continue

            if _error[0]:
                console.print(f"[bold red]⚠ Error:[/bold red] {_error[0]}")
                continue

            response = _result[0]
            # Print the response using Rich Markdown inside a panel
            if response:
                console.print(Panel(Markdown(response), border_style="red", title="[bold red]Abaddon >[/bold red]", title_align="left"))
            else:
                console.print("[italic gray](No textual response provided)[/italic gray]")
                
        except KeyboardInterrupt:
            # Ctrl+C at the prompt = exit
            console.print("\n[bold red]✖ Abaddon core shutting down... Goodbye.[/bold red]")
            break
        except EOFError:
            # Handle Ctrl+D
            console.print("\\n[bold red]✖ Connection terminated. Goodbye.[/bold red]")
            break
        except Exception as e:
            console.print(f"[bold red]⚠ An unexpected error occurred:[/bold red] {e}")

if __name__ == "__main__":
    main()
