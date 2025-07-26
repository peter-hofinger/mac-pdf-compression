import tempfile
from pathlib import Path
from shutil import copymode, copystat
from sys import argv

from Foundation import NSURL
from osxmetadata import ALL_ATTRIBUTES, OSXMetaData
from Quartz import PDFDocument, QuartzFilter


def _get_metadata(filepath):
    metadata = OSXMetaData(filepath)
    result = {}
    for attr in ALL_ATTRIBUTES:
        value = metadata.get(attr)
        if value is not None:
            result[attr] = value

    return result


def _set_metadata(filepath, metadata):
    dest_md = OSXMetaData(filepath)
    for attr, value in metadata.items():
        dest_md.set(attr, value)


def _compress_pdf(filepath):
    pdf_url = NSURL.fileURLWithPath_(filepath.as_posix())
    pdf = PDFDocument.alloc().initWithURL_(pdf_url)

    filter_path = "/System/Library/Filters/Reduce File Size.qfilter"
    filter_url = NSURL.fileURLWithPath_(filter_path)
    filter = QuartzFilter.quartzFilterWithURL_(filter_url)

    return bytes(pdf.dataRepresentationWithOptions_({"QuartzFilter": filter}))


def _atomic_modify(filepath, new_content):
    if filepath.stat().st_size <= len(new_content):
        return  # Quartz filter did not decrease file size

    metadata = _get_metadata(filepath)
    with tempfile.NamedTemporaryFile(
        prefix=filepath.name + ".", dir=filepath.parent
    ) as tmp:
        tmp_path = Path(tmp.name)

        tmp_path.write_bytes(new_content)
        copymode(filepath, tmp_path)
        copystat(filepath, tmp_path)
        _set_metadata(tmp_path, metadata)
        tmp_path = tmp_path.replace(filepath)  # Atomic rename

        Path(tmp.name).touch()  # Context manager expects a file


if __name__ == "__main__":
    if len(argv) != 2:
        msg = f"You passed {len(argv) - 1} arguments although 1 was expected."
        raise RuntimeError(msg)

    filepath = Path(argv[1]).resolve()
    if not filepath.exists():
        msg = f"File {filepath} does not exist."
        raise ValueError(msg)

    compressed_bytes = _compress_pdf(filepath)
    _atomic_modify(filepath, compressed_bytes)
