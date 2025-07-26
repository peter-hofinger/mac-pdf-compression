# Mac PDF Compression

A command-line tool for compressing PDF files on macOS using the **Reduce File Size** Quartz filter. It prevents corruption with atomic file operations and keeps metadata.

## Prerequisites

- [macOS](https://www.apple.com/macos)
- [git](https://git-scm.com/downloads/mac)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Installation

Clone the repository with git and install all dependencies using uv:

```bash
git clone https://github.com/peter-hofinger/mac-pdf-compression.git
cd mac-pdf-compression
uv sync
```

## Usage

### Basic Syntax

```bash
uv run main.py /pattern/with/wildcards.pdf
```

The tool accepts any path and supports [wildcards](https://docs.python.org/3/library/pathlib.html#pathlib-pattern-language). If the given pattern resolves to existing PDF files, it processes all of them Largest files are processed first, so the estimated time remaining will be overestimated.

### Single File Compression

Compress an individual PDF document:

```bash
uv run main.py document.pdf
```

**Example output:**
```
Found 1 PDF with 5.844 MiB
Compressed 1 PDF by 55.56% to 2.597 MiB
```

### Batch Processing

Process all PDFs in a directory, including subdirectories:

```bash
uv run main.py ~/Downloads/**/*.pdf
```

**Example output:**
```
Found 7 PDFs totalling 161.4 MiB
100%|█████████████████████████| 7/7 [00:07<00:00,  1.01s/it]
Compressed 7 PDFs by 45.96% to 87.21 MiB
```

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.