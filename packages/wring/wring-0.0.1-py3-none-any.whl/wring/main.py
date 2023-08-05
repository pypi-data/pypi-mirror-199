import os

import click
import pyarrow.csv as pc
import pyarrow.parquet as pq


@click.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--compression", default="zstd", help="compression algorithm")
@click.option("--compression-level", default=9, help="compression algorithm")
def wring(directory, compression, compression_level):
    """Crawl a directory and compress csv files into parquet."""
    click.echo(f"wringing {directory} [{compression=}, {compression_level=}]")
    click.echo(f"[{compression=}, {compression_level=}]")
    for dirpath, _dirnames, filenames in os.walk(directory):
        for f in filenames:
            source = os.path.join(dirpath, f)
            target = None
            if source.endswith(".csv"):
                target = source[:-4] + ".parquet"
            elif source.endswith(".csv.gz"):
                target = source[:-7] + ".parquet"
            if target is not None:
                if not os.path.exists(target):
                    click.echo(click.style("converting ", fg="green") + source)
                    try:
                        t = pc.read_csv(source)
                        pq.write_table(
                            t,
                            target,
                            compression=compression,
                            compression_level=compression_level,
                        )
                    except Exception as err:
                        click.echo(click.style(str(err), fg="red", bold=True))
                else:
                    click.echo(
                        click.style("not converting ", fg="red")
                        + source
                        + click.style(" (parquet already exists)", fg="red")
                    )


if __name__ == "__main__":
    wring()
