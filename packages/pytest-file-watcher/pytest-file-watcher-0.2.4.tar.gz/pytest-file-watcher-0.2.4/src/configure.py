import yaml
import typer

from rich import print
from rich.table import Table
from rich.console import Console
from dataclasses import dataclass, fields, field, MISSING

app = typer.Typer()
console = Console()


@dataclass
class Config:
    path: str
    onPass: str = field(default="")
    onFail: str = field(default="")
    verbose: bool = field(default=False)
    autoClear: bool = field(default=False)
    config: bool = field(default=None)
    ignore: list[str] = field(default_factory=list)
    extensions: list[str] = field(default_factory=list)
    passthrough: list[str] = field(default_factory=list)

    def __post_init__(self):
        if self.config:
            loaded_config = load_config(self.config)
            self.verbose = self.verbose or loaded_config["verbose"]
            self.autoClear = self.autoClear or loaded_config["autoClear"]
            self.passthrough = self.passthrough or loaded_config["passthrough"]
            self.ignore = self.ignore or loaded_config["ignore"]
            self.extensions = self.extensions or loaded_config["extensions"]
            self.onPass = loaded_config["onPass"] or ""
            self.onFail = loaded_config["onFail"] or ""


def display_table(data: dict):
    table = Table()
    table.add_column("Key")
    table.add_column("Value")
    for key, value in data.items():
        table.add_row(key, str(value))
    console.print(table)


def load_config(path: str = "config.yaml"):
    try:
        with open(path, "r") as f:
            config = yaml.safe_load(f)
            return config
    except FileNotFoundError:
        print("Config file not found")
        raise typer.Exit()


def get_optional_fields(instance: Config):
    data = {}
    for instance_field in fields(instance):
        if (
            instance_field.default is not MISSING and instance_field.default is not None
        ) or instance_field.default_factory is not MISSING:
            if instance_field.default_factory is not MISSING:
                if instance_field.default_factory == list:
                    data[instance_field.name] = []
                else:
                    data[instance_field.name] = instance_field.default_factory
            else:
                data[instance_field.name] = instance_field.default
    return data


@app.command()
def create(
    path: str = typer.Option(
        "config.yaml",
        "-c",
        "--config",
        help="Path to a config file.",
    ),
):
    """
    Create a config file for Pytest-File-Watcher.

    \b
    Use the [cyan]create[/cyan] command to create a config file that will be used for testing.

    [underline magenta]Note:[/underline magenta] This command will overwrite any existing config file. Unless a different path is specified.
    [underline magenta]Note:[/underline magenta] If you use the configure command, you can use the -c flag when testing to include that config file for testing.
    [underline magenta]Note:[/underline magenta] If you are passing a list of values, enclose them in quotes and separate them with spaces. Example: [cyan]passthrough: "param1" "param2" "param3"[/cyan]
    """  # noqa: E501
    print("Enter values for the config. Leave blank to ignore.")

    config = {}
    optional_fields = get_optional_fields(Config)
    for k, v in optional_fields.items():
        if isinstance(v, list):
            config[k] = typer.prompt(
                f"{k} (separate with spaces and enclose in quotes)",
                default="",
                type=str,
            )
            config[k] = config[k].split(" ")
            config[k] = [x.strip('"') for x in config[k] if x]
        else:
            config[k] = typer.prompt(
                k,
                default=v,
                type=type(v),
            )

    show_and_save(config, path)


@app.command()
def edit(
    path: str = typer.Option(
        "config.yaml",
        "-c",
        "--config",
        help="Path to the config file",
    )
):
    """
    Edit the config file for Pytest-File-Watcher.

    \b
    Use the [cyan]edit[/cyan] command to edit an existing config file that will be used for testing.

    [underline magenta]Note:[/underline magenta] This command will overwrite any existing config file.
    [underline magenta]Note:[/underline magenta] If you use the configure command, you can use the -c flag when testing to include that config file for testing.
    [underline magenta]Note:[/underline magenta] If you are passing a list of values, enclose them in quotes and separate them with spaces. Example: [cyan]passthrough: "param1" "param2" "param3"[/cyan]
    """  # noqa: E501
    config = load_config(path)

    print("Enter new values for the config. Leave blank to keep the current value.")
    optional_fields = get_optional_fields(Config)
    for k, v in optional_fields.items():
        if isinstance(v, list):
            config[k] = typer.prompt(
                f"{k} (separate with spaces and enclose in quotes)",
                default=" ".join(config.get(k, v)),
                type=str,
            )
            config[k] = config[k].split(" ")
            config[k] = [x.strip('"') for x in config[k] if x]
        else:
            config[k] = typer.prompt(
                k,
                default=config.get(k, v),
                type=type(v),
            )

    show_and_save(config, path)


def show_and_save(config, path):
    display_table(config)
    confirmation = typer.confirm("Are all the values correct?", abort=True)

    if confirmation:
        with open(path, "w") as f:
            yaml.dump(config, f)

        print("Config edited successfully")
    else:
        print("Config edit aborted")


@app.command()
def show(
    path: str = typer.Option(
        "config.yaml",
        "-c",
        "--config",
        help="Path to the config file",
    )
):
    """
    Show the config file for Pytest-File-Watcher.

    \b
    Use the [cyan]show[/cyan] command to show the current config file that will be used for testing.
    """
    config = load_config(path)
    display_table(config)
