
# PDF Downloader

  

This Python program reads URLs from an Excel file, downloads the associated PDF files, and logs the results in an Excel file.

  

## Prerequisites

  

Before running the program, ensure you have the following installed:

- Python 3.x

- Required Python packages (install via pip):

```bash
pip install -r /path/to/requirements.txt
```

  
  

## Directory Setup


**Output Directories:**

- Create a directory named `out` in the project folder. 

- Inside `out`, create a folder named `files` where the downloaded PDFs will be stored.

- The program will also save a log file, `downloaded_files.xlsx`, in the `out` folder.

**Excel File:** Place `GRI_2017_2020.xlsx` in the `out` directory.

## Usage

1. Open a terminal and navigate to the project directory.

2. Run the program with the following command:

	```bash
	python Main.py
	```
Make sure `Main.py` and all necessary files are in the same directory as the terminal.

## Configuration

You can adjust the following variables in the code:

  

- `WORKERS`: Set the number of threads (for concurrent downloads).

- `FILES`: Set the maximum number of files to download.

Currently, these values are set as follows:  

- `WORKERS = 10`

- `FILES = 100`

## Files Generated

- **Downloaded PDFs**: Stored in the `out/files` folder.

- **Log File**: An Excel file, `downloaded_files.xlsx`, is generated in the `out` folder, listing download statuses for each file.

## Code Structure

- **Controller**: Initializes the program and manages the file handler.

- **Downloader**: Handles individual PDF downloads.

- **FileHandler**: Reads URLs from the Excel file, manages the download process, and writes the log of downloaded files.

## Notes

- The program relies heavily on `GRI_2017_2020.xlsx`. Ensure this file is correctly formatted and includes the columns `Pdf_URL`, `ReportHtmlAddress`, and `BRnum`.

- The download process will stop after reaching the `FILES` limit.

## Error Handling

If any download fails, the log file will record the status as `'Ikke downloadet'`, indicating the file was not downloaded.

  

## Example

1. Prepare `GRI_2017_2020.xlsx` in the `out` folder.

2. Run:

	```bash
	python Main.py
	```

3. Check the downloaded PDFs in `out/files` and the log in `out/downloaded_files.xlsx`.

## Author 
Created by [Mike Kragelund](https://github.com/MikeKragelundSpecialisterne)

Enjoy using the PDF Downloader!