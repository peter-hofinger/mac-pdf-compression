import os
import tempfile
from pathlib import Path
from sys import argv

from Foundation import NSURL
from Quartz import PDFDocument, QuartzFilter


def _compress_pdf(filepath):
    pdf_url = NSURL.fileURLWithPath_(filepath.as_posix())
    pdf = PDFDocument.alloc().initWithURL_(pdf_url)

    filter_path = "/System/Library/Filters/Reduce File Size.qfilter"
    filter_url = NSURL.fileURLWithPath_(filter_path)
    filter = QuartzFilter.quartzFilterWithURL_(filter_url)

    return bytes(pdf.dataRepresentationWithOptions_({"QuartzFilter": filter}))


def _atomic_modify(filepath, new_content):
    stat = filepath.stat()
    if stat.st_size <= len(new_content):
        return

    with tempfile.NamedTemporaryFile(
        prefix=filepath.name + ".", dir=filepath.resolve().parent
    ) as tmp:
        tmp_path = Path(tmp.name)

        tmp_path.write_bytes(new_content)
        tmp_path = tmp_path.replace(filepath)  # atomic rename

        Path(tmp.name).touch()  # Context manager expects a file

    tmp_path.chmod(stat.st_mode)
    os.chown(tmp_path, stat.st_uid, stat.st_gid)


if __name__ == "__main__":
    if len(argv) != 2:
        msg = f"You passed {len(argv) - 1} arguments although 1 was expected."
        raise RuntimeError(msg)

    filepath = Path(argv[1])
    if not filepath.exists():
        msg = f"File {filepath} does not exist."
        raise ValueError(msg)

    compressed_bytes = _compress_pdf(filepath)
    _atomic_modify(filepath, compressed_bytes)
