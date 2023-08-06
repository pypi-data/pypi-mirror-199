import typer
import shutil
import pandas as pd
from pathlib import Path
from rich.progress import track

# Creating a typer app
app = typer.Typer()

# Defining a function to move files based on cluster column
def move_files(input_csv: Path, path_col: str, cluster_col: str, copy: bool, output_dir: Path):
    # Reading the csv file using pandas
    df = pd.read_csv(input_csv)
    # Looping over the rows of the dataframe
    for row in track(df.itertuples(), description="Moving files..."):
        # Getting the file path and cluster from the row
        file_path = Path(getattr(row, path_col))
        cluster = getattr(row, cluster_col)
        # Creating a subdirectory for the cluster if it does not exist
        cluster_dir = output_dir / cluster
        cluster_dir.mkdir(exist_ok=True)
        if copy:
            # Copying the file to the cluster subdirectory
            shutil.copy(file_path, (cluster_dir / file_path.name))
        else:
            # Moving the file to the cluster subdirectory
            file_path.rename(cluster_dir / file_path.name)

# Defining a command for the app that takes the arguments from the user
@app.command()
def run(
    input_file: Path = typer.Argument(..., help="The input csv file"),
    path: str = typer.Option("path", help="The name of the path column"),
    cluster: str = typer.Option("cluster", help="The name of the cluster column"),
    copy: bool = typer.Option(False, help="Whether or not to copy instead of move"),
    output: Path = typer.Option('.', help="The output directory")
):
    # Calling the move_files function with the arguments
    move_files(input_file, path, cluster, copy, output)