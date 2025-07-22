# Mac PDF Compression

A command-line tool for compressing PDF files on macOS using the **Reduce File Size** Quartz filter. It prevents corruption with atomic file operations and supports both individual files and batch processing of directories.

## Prerequisites

- macOS (required for Quartz filter support)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager

## Installation

Install all dependencies using uv:

```bash
uv sync --compile-bytecode
```

## Usage

### Basic Syntax

```bash
uv run main.py <file_or_directory>
```

The tool accepts either a single PDF file or a directory path. When given a directory, it recursively processes all PDF files found within.

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

### Batch Directory Processing

Process all PDFs in a directory (including subdirectories):

```bash
uv run main.py documents/
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