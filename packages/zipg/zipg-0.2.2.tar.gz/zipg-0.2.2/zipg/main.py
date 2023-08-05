import os
import typer
import zipfile
from pathlib import Path
from rich.progress import track

app = typer.Typer()

class FileGroup:
    def __init__(self, name: str, files: list[Path]):
        self.name = name
        self.files = files

    def zip(self, output_dir: Path):
        os.makedirs(output_dir, exist_ok=True)
        with zipfile.ZipFile(output_dir / f"{self.name}.zip", "w") as zip_file:
            for file in self.files:
                zip_file.write(file, file.name)

class FileGrouper:
    def __init__(self, input_dir: Path, filters: list[str]):
        self.input_dir = input_dir
        self.filters = filters

    def group_files(self) -> list[FileGroup]:
        files = {}
        for filter in self.filters:
            if filter == "*":
                for file in self.input_dir.glob("*"):
                    if file.is_file():
                        key = file.stem
                        if key not in files:
                            files[key] = []
                        files[key].append(file)
            else:
                for file in self.input_dir.glob(f"*{filter}"):
                    key = file.stem
                    if key not in files:
                        files[key] = []
                    files[key].append(file)
        return [FileGroup(key, group) for key, group in files.items()]

class Zipper:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir

    def zip_groups(self, groups: list[FileGroup]):
        for group in track(groups, description="Zipping files..."):
            group.zip(self.output_dir)

aliases = {
    'shapefile': ['.shp', '.shx', '.dbf', '.prj', '.cpg'],
}

@app.command()
def run(
    input_dir: str = typer.Argument(".", help="Directory to look for files"),
    output_dir: str = typer.Argument(".", help="Path for the output archives"),
    filter: list[str] = typer.Option(["*"], "-f", "--filter", help="Filter file types. Should start with . (i.e.: .shp)"),
):
    """
    Zips groups of files inside a given directory, creating a different zip archive for every group.
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    filters = filter
    for i, f in enumerate(filters):
        if f[0] != '.' and f != '*':
            filters.pop(i)
            filters.extend(aliases[f])
    file_grouper = FileGrouper(input_dir, filters)
    groups = file_grouper.group_files()
    zipper = Zipper(output_dir)
    zipper.zip_groups(groups)
