from utils import COLORS

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
    typer.echo(f"{COLORS.GREEN}Cloning config files from {COLORS.BOLD_CYAN}{
               CONFIG_REPO} {COLORS.GREEN}to {COLORS.BOLD_CYAN}{CONFIG_DIR}{COLORS.RESET}")
    try:
        os.system(
            f"git clone --depth 1 --quiet {CONFIG_REPO} {CONFIG_DIR}"
        )
        typer.echo(f"{COLORS.BOLD_GREEN}Done! :D{COLORS.RESET}")
    except Exception as e:
        typer.echo(f"{COLORS.BOLD_RED}Oh, no!\n {
                   COLORS.UNDERLINE_YELLOW}{e}{COLORS.RESET}")
        return
    typer.echo(f"{COLORS.GREEN}Copying files to {
               COLORS.BOLD_CYAN}~/{COLORS.RESET}")
    try:
        typer.prompt("Press Enter to continue...")
    except KeyboardInterrupt:
        typer.echo(f"{COLORS.BOLD_RED}Aborted!{COLORS.RESET}")
        return

    try:
        os.system(f"cp -r {CONFIG_DIR}.* ~/")
        typer.echo(f"{COLORS.BOLD_GREEN}Done! :D{COLORS.RESET}")
    except Exception as e:
        typer.echo(f"{COLORS.BOLD_RED}Oh, no!\n {
                   COLORS.UNDERLINE_YELLOW}{e}{COLORS.RESET}")
        return


@app.command(name="install", help="Install packages")
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


def main() -> None:
    app()


if __name__ == "__main__":
    main()
