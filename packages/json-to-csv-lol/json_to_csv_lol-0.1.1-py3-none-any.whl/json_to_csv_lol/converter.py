import polars as pl
from pathlib import Path


def convert(input_path: Path, output_path: Path):
    df = pl.read_json(input_path)
    df.write_csv(output_path)
