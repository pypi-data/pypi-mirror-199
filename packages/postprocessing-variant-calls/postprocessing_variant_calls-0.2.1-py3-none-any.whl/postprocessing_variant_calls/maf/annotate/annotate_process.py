#!/usr/bin/env python
# imports 
from __future__ import division
import os
import sys
import vcf
import time
import logging
from pathlib import Path
from typing import List, Optional
import typer
from vcf.parser import _Info as VcfInfo, _Format as VcfFormat, _vcf_metadata_parser as VcfMetadataParser
from .annotate_helpers import read_bed, read_maf
from utils.pybed_intersect import annotater
import pandas as pd


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.DEBUG,
)

logger = logging.getLogger("annotate")

app = typer.Typer(help="post-processing command annotating maf file by bed a bed file.")
# app.add_typer(app, name="annotate", help="annotate maf files based on a given input. Currently supports bed and maf files as references.")

@app.command("mafbybed")
def maf_bed(
    maf: Path = typer.Option(
        ...,
        "--maf",
        "-m",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
        help="input maf file",
    ),
    bed: Path = typer.Option(
        ...,
        "--bed",
        "-b",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
        help="bed file to annotate maf",
    ),
    outputFile: str = typer.Option(
        'output',
        '--output',
        "-o",
        help="output maf file",
    ),
    cname: str = typer.Option(
        'annotation',
        '--cname',
        "-c",
        help="name for annotation column",
    )
):
    logger.info("starting annotation")
    typer.secho(f"annotating {maf} with {bed}".format(maf=maf, bed=bed), fg=typer.colors.GREEN)
    # read bed 
    bed_df = read_bed(bed)
    # read maf
    maf_df = read_maf(maf)
    # annotate maf with processed bed file
    annotated_maf = annotater(maf_df,bed_df,cname)
    # write to csv
    typer.secho(f"Writing out maf file to the following location: {outputFile}.maf".format(outputFile=outputFile), fg=typer.colors.GREEN)
    annotated_maf.to_csv(f"{outputFile}.maf".format(outputFile=outputFile), index=False,sep="\t")
    return 1

if __name__ == "__main__":
    app()
