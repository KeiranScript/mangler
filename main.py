from utils import COLORS
from pathlib import Path
import tempfile
import shutil
import typer
import time
import os

app = typer.Typer()

# Enable this if you're a developer who will need to clone this repo multiple times
# It's mainly just for me but you can use it if you want
DEV = True

CONFIG_DIR = f"/tmp/{time.time()}/" if DEV else os.path.expanduser("~/.config")
CONFIG_REPO = "git@github.com:KeiranScript/.config.git"


@app.command(name="config", help="Clone config files from git repository")
def config():

    with tempfile.TemporaryDirectory() as temp_dir:
        typer.echo(f"{COLORS.GREEN}Cloning config files from {COLORS.BOLD_CYAN}{
                   CONFIG_REPO} {COLORS.GREEN}to temporary directory{COLORS.RESET}")

        try:
            clone_result = os.system(
                f"git clone --depth 1 --quiet {CONFIG_REPO} {temp_dir}")
            if clone_result != 0:
                raise Exception("Failed to clone repository")

            typer.echo(f"{COLORS.BOLD_GREEN}Clone successful!{COLORS.RESET}")

            config_home = Path(os.path.expanduser("~/.config"))
            temp_path = Path(temp_dir)

            source_path = temp_path / \
                '.config' if (temp_path / '.config').exists() else temp_path

            config_home.mkdir(parents=True, exist_ok=True)

            for item in source_path.iterdir():
                if item.name.startswith('.git'):
                    continue

                target_path = config_home / item.name

                if target_path.exists():
                    typer.echo(f"\n{COLORS.YELLOW}Conflict detected: {
                               COLORS.BOLD_CYAN}{item.name}{COLORS.RESET}")
                    choice = typer.prompt(
                        f"What would you like to do?\n"
                        f"[s]kip, [o]verwrite, [b]ackup existing",
                        type=str,
                        default="s"
                    ).lower()

                    if choice == 's':
                        typer.echo(f"{COLORS.BLUE}Skipping {
                                   item.name}{COLORS.RESET}")
                        continue
                    elif choice == 'b':
                        backup_path = str(target_path) + '.bak'
                        shutil.move(str(target_path), backup_path)
                        typer.echo(f"{COLORS.GREEN}Created backup at: {
                                   COLORS.BOLD_CYAN}{backup_path}{COLORS.RESET}")

                if item.is_dir():
                    shutil.copytree(str(item), str(
                        target_path), dirs_exist_ok=True)
                else:
                    shutil.copy2(str(item), str(target_path))

                typer.echo(f"{COLORS.GREEN}Copied: {COLORS.BOLD_CYAN}{
                           item.name}{COLORS.RESET}")

            typer.echo(f"\n{COLORS.BOLD_GREEN}Configuration files installed successfully!{
                       COLORS.RESET}")

        except Exception as e:
            typer.echo(f"{COLORS.BOLD_RED}Error occurred:\n{
                       COLORS.UNDERLINE_YELLOW}{str(e)}{COLORS.RESET}")
            return


@app.command(name="i", help="Install packages")
def install():
    typer.echo(f"{COLORS.GREEN}Installing packages...")
    try:
        os.system("paru -V")
    except Exception:
        os.system("sudo pacman -S --noconfirm paru")
    try:
        os.system("paru -Syyu --noconfirm")
        os.system("paru -S --needed - < ~/.config/keiran/pkglist.txt")
        typer.echo(f"{COLORS.BOLD_GREEN}Done! :D{COLORS.RESET}")
    except Exception as e:
        typer.echo(f"{COLORS.BOLD_RED}Oh, no!\n {
                   COLORS.UNDERLINE_YELLOW}{e}{COLORS.RESET}")
        return


@app.command(name="up", help="Update packages")
def update():
    typer.echo(f"{COLORS.GREEN}Updating packages...")
    try:
        os.system("paru -V")
    except Exception:
        os.system("sudo pacman -S --noconfirm paru")
    try:
        os.system("paru -Syyu --noconfirm")
        typer.echo(f"{COLORS.BOLD_GREEN}Done! :D{COLORS.RESET}")
    except Exception as e:
        typer.echo(f"{COLORS.BOLD_RED}Oh, no!\n {
                   COLORS.UNDERLINE_YELLOW}{e}{COLORS.RESET}")
        return


def main() -> None:
    app()


if __name__ == "__main__":
    main()
