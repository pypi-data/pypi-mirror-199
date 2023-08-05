import typer

from typing import List, Optional

from src.utils.watcher import watch_files
from src.utils.configure import app as configure, Config

app = typer.Typer(rich_markup_mode="rich", add_completion=False)
app.add_typer(configure, name="configure", help="Configure Pytest-File-Watcher")


def version_callback(value: bool):
    if value:
        typer.echo(f"Pytest-File-Watcher Version: {typer.style('0.2.1', fg='blue')}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show current version",
    ),
):
    """
    Pytest-File-Watcher is a CLI tool that watches for changes in your code and runs pytest on the changed files.

    \b
    [underline magenta]Recommended:[/underline magenta] Use the configure command to create a config file that will be used for testing.
    [underline magenta]Note:[/underline magenta] If you use the configure command, you can use the -c flag to use the config file for testing.
    """  # noqa: E501
    return


@app.command()
def test(
    path: str = typer.Argument(..., help="Path to a test folder"),
    verbose: Optional[bool] = typer.Option(
        None, "-v", "--verbose", help="Show verbose output."
    ),
    autoClear: Optional[bool] = typer.Option(
        None, "-a", "--auto-clear", help="Clear the console after each test."
    ),
    config: Optional[str] = typer.Option(
        None, "-c", "--config", help="Path to a config file."
    ),
    ignore: Optional[List[str]] = typer.Option(
        None, "-i", "--ignore", help="Paths to ignore when watching for changes."
    ),
    extensions: Optional[List[str]] = typer.Option(
        None, "-e", "--ext", help="Extra file extensions to watch."
    ),
    passthrough: Optional[List[str]] = typer.Option(
        None, "-p", "--pass", help="Passes arguments to pytest."
    ),
    onPass: Optional[str] = typer.Option(
        None, "--on-pass", help="Shell command to run on passed tests."
    ),
    onFail: Optional[str] = typer.Option(
        None, "--on-fail", help="Shell command to run on failed tests."
    ),
):
    """
    Run pytest on a given path.

    [blue]
    Example:
        Pytest-File-Watcher test tests/
    [/blue]

    To pass a list of arguments to Pytest-File-Watcher you must use the flag for each argument you want to pass.
    [blue]
    Example:
        Pytest-File-Watcher test tests/ -p "-k test_something" -p "-m slow"
    [/blue]
    [blue]
    Example:
        Pytest-File-Watcher test tests/ -p "-k test_something" -p "-m slow" -i "tests/test_something.py" -i "tests/test_something_else.py"
    [/blue]
    """  # noqa: E501
    config = Config(
        path=path,
        ignore=ignore,
        onPass=onPass,
        onFail=onFail,
        config=config,
        verbose=verbose,
        autoClear=autoClear,
        extensions=extensions,
        passthrough=passthrough,
    )

    watch_files(config)


def cli():
    app()


if __name__ == "__main__":
    cli()
