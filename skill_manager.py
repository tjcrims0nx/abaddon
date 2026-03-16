import os
import subprocess
from rich.console import Console

console = Console()

SKILL_LIST_FILE = "skill_list.md"
SKILLS_DIR = "skills"

TEMPLATE_CONTENT = """# Abaddon Skill List
Add ClawHub skills below as a markdown list. Abaddon will automatically install missing skills when it starts up.

# Example:
# - some-skill-slug
"""

def sync_skills():
    """
    Ensures skill_list.md exists, parses it for skills, and installs any missing ones via clawhub.
    """
    if not os.path.exists(SKILL_LIST_FILE):
        with open(SKILL_LIST_FILE, 'w', encoding='utf-8') as f:
            f.write(TEMPLATE_CONTENT)
        console.print(f"[dim]ℹ[/] [italic gray]Created {SKILL_LIST_FILE} template.[/italic gray]")
        
    os.makedirs(SKILLS_DIR, exist_ok=True)
    
    skills_to_install = []
    
    with open(SKILL_LIST_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith("- "):
                slug = line[2:].strip()
                if slug:
                    skills_to_install.append(slug)
                    
    for slug in skills_to_install:
        skill_name = slug.split('/')[-1] if '/' in slug else slug
        
        # Check if the skill directory already exists (heuristic)
        skill_path = os.path.join(SKILLS_DIR, skill_name)
        if not os.path.exists(skill_path):
            console.print(f"[bold yellow]⟡ Installing missing skill:[/bold yellow] {slug}")
            try:
                # Run clawhub install
                result = subprocess.run(
                    f'clawhub install "{slug}"',
                    capture_output=True,
                    text=True,
                    check=False,
                    shell=True
                )
                if result.returncode == 0:
                    console.print(f"[bold green]✔ Successfully installed {slug}[/bold green]")
                else:
                    console.print(f"[bold red]✖ Failed to install {slug}:[/bold red]\n{result.stderr}")
            except Exception as e:
                console.print(f"[bold red]✖ Error executing clawhub command:[/bold red] {e}")

if __name__ == "__main__":
    sync_skills()
