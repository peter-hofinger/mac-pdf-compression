import os
from functools import partial
from glob import glob
from os.path import expanduser
from pathlib import Path
from subprocess import run
from sys import argv, platform

from tqdm.contrib.concurrent import thread_map


def _sanity_check():
    if platform != "darwin":
        raise RuntimeError("This script only supports macOS.")

    if not Path("/System/Library/Filters/Reduce File Size.qfilter").exists():
        raise RuntimeError(
            "The Quartz filter is missing at '/System/Library/Filters/Reduce File Size.qfilter'."
        )

    if len(argv) != 2:
        msg = f"This script is only intended to be called from the CLI with a single argument. You passed {len(argv) - 1} arguments."
        raise RuntimeError(msg)


def _find_pdfs(path):
    pdfs = [Path(path) for path in glob(expanduser(path), recursive=True)]

    invalid_paths = [
        p for p in pdfs if not (p.exists() and p.is_file() and p.suffix == ".pdf")
    ]
    if invalid_paths:
        raise ValueError(f"Resolved following invalid paths: {invalid_paths}")

    if len(pdfs) == 0:
        f"No PDFs found for {path}"
        raise ValueError(f"No PDFs found in {path}")

    tuples = sorted(((pdf.stat().st_size, pdf) for pdf in pdfs), reverse=True)
    sizes, pdfs = zip(*tuples)

    return pdfs, sizes


def _human_readable(size, precision=4):
    for unit in ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB"]:
        if size < 1024:
            break

        size /= 1024

    return f"{size:.{max(precision - len(str(int(size))), 0)}f} {unit}"


def _compress(pdfs, sizes):
    n_pdfs = len(pdfs)
    total_size = sum(sizes)
    if n_pdfs == 1:
        print(f"Found 1 PDF with {_human_readable(total_size)}")

        with open(os.devnull, "w") as devnull:
            run(["python", "convert.py", str(pdfs[0].resolve())], stderr=devnull)
    else:
        print(f"Found {n_pdfs} PDFs totalling {_human_readable(total_size)}")

        commands = [["python", "convert.py", str(pdf.resolve())] for pdf in pdfs]
        with open(os.devnull, "w") as devnull:
            thread_map(partial(run, stderr=devnull), commands)

    new_total = sum(pdf.stat().st_size for pdf in pdfs)
    ratio = 1 - new_total / total_size
    if n_pdfs == 1:
        print(f"Compressed 1 PDF by {ratio * 100:.2f}% to {_human_readable(new_total)}")
    else:
        print(
            f"Compressed {n_pdfs} PDFs by {ratio * 100:.2f}% to {_human_readable(new_total)}"
        )


if __name__ == "__main__":
    _sanity_check()

    pdfs, sizes = _find_pdfs(argv[1])

    _compress(pdfs, sizes)
