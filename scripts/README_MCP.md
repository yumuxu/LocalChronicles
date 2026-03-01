# LocalChronicles OCR MCP Server

This directory contains an MCP (Model Context Protocol) server that exposes the project's PDF processing and OCR capabilities.

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements_mcp.txt
   ```

## Usage

Run the MCP server:

```bash
python mcp_server.py
```

The server uses `stdio` transport by default, which is compatible with most MCP clients (like Claude Desktop, Trae, etc.).

## Available Tools

### `pdf_to_images`
Converts a PDF file to a series of images.
- **Inputs**: `pdf_path` (string), `output_folder` (optional string), `dpi` (optional int, default 300)
- **Returns**: Success message.

### `run_ocr_on_folder`
Runs PaddleOCR on all images in a specified folder.
- **Inputs**: `image_folder` (string)
- **Behavior**: Processes images sequentially (sorted by page number), skips already processed ones, and saves results to `folder_name_ocr_result.txt`.
- **Note**: This is a blocking operation and may take a long time for large folders.

### `ocr_single_image`
Runs OCR on a single image and returns the text.
- **Inputs**: `image_path` (string)
- **Returns**: The recognized text content.
