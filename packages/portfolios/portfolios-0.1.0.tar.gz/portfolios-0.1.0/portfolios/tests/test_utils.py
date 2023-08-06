import rich
import typer

from ..utils import flatten, toMatrix

app = typer.Typer(
    name="test",
    help="A CLI for portfolio optimization experiments.",
    no_args_is_help=True,
)


test_case = {
    "a": 1,
    "b": 2,
    "c": {
        "d": 3,
        "da": 1,
        "db": 2,
        "dc": {
            "dcd": 3,
            "dce": 4,
            "dcf": {
                "dcfg": 5,
                "dcfh": 6,
            },
        },
    }
}

@app.command("example")
def example():
    rich.print(test_case)


@app.command("flatten")
def test_flatten():
    rich.print(flatten(test_case))
    
@app.command("tomatrix")
def test_toMatrix():
    rich.print(toMatrix(test_case))
    
@app.command("test")
def test():
    rich.print(test_case)
    rich.print(flatten(test_case))
    rich.print(toMatrix(test_case))
    rich.print(toMatrix(flatten(test_case)))