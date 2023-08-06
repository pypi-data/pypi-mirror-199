import pathlib

import typer

import utils
import carbon

app = typer.Typer()


def wrap_carbonier(file, exclude, output_folder, rgba, font):
    carbonizer = carbon.Carbonizer(input_file=file,
                                   output_filename=output_folder / ("carbonized_" + file.stem + ".png"),
                                   exclude=exclude,
                                   background=rgba,
                                   font=font)
    carbonizer()


@app.command()
def carbonize(
        walk: str = typer.Option("", "--walk", "-w"),
        file: str =typer.Option("", "--file"),
        output_folder: str = typer.Option(".", "--output-folder", "-t"),
        exclude: str = typer.Option("__pychache__*", "--exclude", "--filter", "-e")
):
    if walk:
        path = pathlib.Path(walk)
        files = path.rglob("*")
    elif file:
        files = [pathlib.Path(file)]
    else:
        raise ValueError("Neither File nor Folder are given")

    output_folder = pathlib.Path(output_folder)
    output_folder.mkdir(exist_ok=True)
    file: pathlib.PosixPath
    for file in files:
        wrap_carbonier(file,
                       output_folder / ("carbonized_" + file.stem + ".png"),
                       exclude,
                       utils.RGBA(0, 0, 0,0),
                       "night owl")


if __name__ == "__main__":
    typer.run(carbonize)
