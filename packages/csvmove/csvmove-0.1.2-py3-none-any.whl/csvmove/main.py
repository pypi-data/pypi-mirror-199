import typer
import pandas as pd
from pathlib import Path
from rich.progress import track

# Creating a typer app
app = typer.Typer()

# Defining a function to move files based on cluster column
def move_files(input_csv: Path, path_col: str, cluster_col: str, output_dir: Path):
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
        # Moving the file to the cluster subdirectory
        file_path.rename(cluster_dir / file_path.name)

# Defining a command for the app that takes the arguments from the user
@app.command()
def run(
    input_file: Path = typer.Argument(..., help="The input csv file"),
    path: str = typer.Option("path", help="The name of the path column"),
    cluster: str = typer.Option("cluster", help="The name of the cluster column"),
    output: Path = typer.Option('.', help="The output directory")
):
    # Calling the move_files function with the arguments
    move_files(input_file, path, cluster, output)