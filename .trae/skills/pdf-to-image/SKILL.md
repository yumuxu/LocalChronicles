---
name: "pdf-to-image"
description: "Convert PDF to images. Invoke when user wants to convert PDFs or extract text from them."
---

# PDF to Image Skill

This skill converts PDF files into high-quality images.

## Prerequisites

1.  **Python Environment**: Ensure Python is installed.
2.  **Dependencies**:
    -   Basic: `pip install pdf2image`
3.  **System Dependency (Poppler)**:
    -   **Windows**: Download/install poppler and add `bin/` to PATH.
    -   **macOS**: `brew install poppler`
    -   **Linux**: `sudo apt-get install poppler-utils`

## Usage

### Conversion Script (`convert_pdf_to_images.py`)

A script named `convert_pdf_to_images.py` is available at `scripts/convert_pdf_to_images.py`.

```python
import os
import sys
from pathlib import Path
# ... (imports and checks) ...

def convert_pdf(pdf_path, output_folder=None, dpi=300, fmt='png'):
    # ... conversion loop ...
    pass

if __name__ == "__main__":
    # ... argument parsing ...
    pass
```

### Running the Conversion

To convert a PDF:

```bash
python scripts/convert_pdf_to_images.py "path/to/doc.pdf" [output_folder] [dpi]
```

**Arguments:**
- `pdf_path`: Path to PDF file.
- `output_folder` (Optional): Destination folder.
- `dpi` (Optional): Image quality (default 300).

**Examples:**

1.  **Convert only**:
    ```bash
    python scripts/convert_pdf_to_images.py "docs/report.pdf"
    ```
