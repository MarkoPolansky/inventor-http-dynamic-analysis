# Data

The raw dataset files are hosted externally on the VUT FIT Nextcloud instance because they are too large for GitHub. Single JSON file is around 200 MB.

All files must be placed in `data/raw/` directory before running any analysis.

---

## Option A — Download script 

**Requirements**
- Python 3.12+


**Usage**

```bash
python data_downloader.py
```

The interactive menu offers:

1. **List files** — shows all available files with their sizes
2. **Download selected files** — parallel download of one or more files by index; accepts a range (`1-5`) or individual indexes (`1 3 7`)
3. **Download ZIP containing all files** — downloads and extracts the full dataset in one step
4. **Exit**

Downloaded files are written to `data/raw/`.


> Downloading all files may take up multiple minutes (6.7 GB total size of dataset)
---

## Option B — Manual download

If you prefer not to run the script, files can be downloaded directly from the public link below:

**https://nextcloud.fit.vutbr.cz/s/8siMfiKcp4Y7oAq**

Save each file to `data/raw/` e.g.:

```
data/
└── raw/
    ├── webapp.http_dynamic.single_page.tranco.2026-03-01.json
    ├── webapp.http_dynamic.single_page.tranco.2026-03-02.json
    └── ...
```

---

## File Format

Each raw dataset is a **newline-delimited JSON** file (one JSON object per line) named:

```
webapp.http_dynamic.single_page.tranco.YYYY-MM-DD.json
```

Each line has the following structure:

```json
{
  "Meta": {
    "Timestamp": "2026-02-24T00:45:50",
    "TestId": "webapp.http.dynamic.64",
    "Config": {
      "target_host": "https://github.io",
      "screenshot_timing_type": "networkidle0",
      "timeout": 25000
    }
  },
  "Result": {
    "status": "completed",
    "visited_pages": [
      {
        "current_url": "https://docs.github.com/en/pages"
        "status": "completed",
        "load_time": 393,
        "dom_content_loaded_time": 389.30000000447035,
        "total_data_size": 3182833,
        "waterfall_analysis": [
          {
            "url": "https://pages.github.com/",
            "type": "document",
            "method": "GET",
            "status_code": 200,
            "size": 4239,
            "start_time": 50602.85876,
            "time": "69.7570",
            "sourceUrl": "https://pages.github.com/"
          },...
        ]
      }
    ]
  }
}
```

---

## Monitoring Configuration

### `test_id_to_target_host_mapper.json`

A helper mapping file that maps **TestId** to corresponding **target host URL** form yaml configuration file. Used to resolve which host a given test ID refers to when working with the raw dataset.


### `webapp.http.dynamic.yaml`

The monitoring configuration file that was used during data collection. Targets that produced output too large for processing or could not yield correct results were commented out before running data collection.