from .annotate import annotate_process
from .concat import concat_process
from .concat.concat_helpers import concat_mafs, check_maf, check_txt, process_paths, process_header
from .concat.resources import de_duplication_columns, minimal_maf_columns
import typer 
import logging
from pathlib import Path
from typing import List, Optional
import typer
import logging
import time
import os 
# dir path 
dir_path = os.path.dirname(os.path.realpath(__file__))

# setup logger
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.DEBUG,
)

logger = logging.getLogger("concat")

app = typer.Typer()


# Add Annote App 
app.add_typer(annotate_process.app, name="annotate", help="annotate maf files based on a given input.")

# Concat Features: This needs to be in main since we it doesn't have sub-commands
@app.command("concat", help="row-wise concatenation for maf files.")
def maf_maf(
    files: List[Path] = typer.Option(
        None, 
        "--files",
        "-f",
        help="MAF file to concatenate. Maf files are specified here, or using paths parameter.",
        callback = check_maf # call back allow us to check input parameters
    ),
    paths: Path = typer.Option(
        None,
        "--paths",
        "-p",
        help="A text file containing paths of maf files to concatenate. Maf files are specified here, or using files parameter.",
        callback = check_txt # call back allow us to check input parameters
    ),
    output_maf: Path = typer.Option(
        "output.maf",
        "--output",
        "-o",
        help="Maf output file name."
    ),
    header: Path = typer.Option(
        os.path.join(dir_path, "../../resources/maf_concat/default_header.txt"),
        "--header",
        "-h",
        help="a header file containing the headers for maf file",
        callback = check_txt
    ),
    deduplicate: bool = typer.Option(
        False,
        '--deduplicate',
        "-de",
        help="deduplicate outputted maf file.",
    )
):
    logger.info("started concat")
    # make sure files or paths was specified
    # as of < 0.7.0 does not support mutually exclusive arguments
    if not (files or paths): 
        typer.secho(
            f"Either paths, or files must be specified for concatenation to run.",
            fg=typer.colors.RED)
        raise typer.Abort()
    # process our paths txt file 
    if paths:
        files = process_paths(paths)
    # process our header file
    if header:
        header = process_header(header)
    # concat maf files 
    # paths vs files is taken care of at this point
    concat_df = concat_mafs(files, output_maf, header)
    # deduplicate 
    if deduplicate:
        concat_df = concat_df[de_duplication_columns].drop_duplicates()
    # write out paths
    concat_df.to_csv(f"{output_maf}.maf", index=False, sep="\t")
    return 0
    

if __name__ == "__main__":
    app()
