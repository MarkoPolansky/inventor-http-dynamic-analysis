


## adblock_cache/

Persistent cache for using the adblocker. Avoids re-running the `adblock.mjs` script on already seen resources across runs and across notebooks.


> **Note:** Both files are pre-populated with data from the current available dataset.


---

### adblock_cache/blocked_urls.txt

One entry per line. Each line is an **md5 hash** of a composite key built from:

```
md5(url + "\x00" + sourceUrl + "\x00" + type)
```

Example:
```
5d41402abc4b2a76b9719d911017c592
3f2a1b4c5d6e7f8a9b0c1d2e3f4a5b6c
```

The hash is computed in python notebook `analysis_etdl_plus_one_clustering.ipynb` using  (`hashlib.md5`).

---

### adblock_cache/processed_files.txt

One filename per line. Each line is the **basename** of a file from `data/raw/` that has already been fully processed by `adblock_check.mjs`. It means that all resources from data file were checked and any blocked ones were written to `blocked_urls.txt`.

Example:
```
webapp.http_dynamic.single_page.tranco.2026-02-24.json
webapp.http_dynamic.single_page.tranco.2026-02-25.json
```


On each run, the analysis notebook compares `selected_files` against this list. Files not present here are sent to `adblock_check.mjs`; files already listed are skipped entirely.

---

## adblocer_ghostery/adblock.mjs

Node.js script that checks resources against the Ghostery adblocker engine (EasyList + EasyPrivacy).
### Requirements

| Requirement | Minimum version |
|---|-----------------|
| Node.js | 18 LTS          | 
| npm | 9+              | 

### Installation

```bash
cd shared/adblocker_ghostery
npm install
```
### Input format

One composite key per line, fields separated by a null byte (`\x00`):

```
<url>\x00<sourceUrl>\x00<type>
```

| Field | Required | Description                                                        |
|---|---|--------------------------------------------------------------------|
| `url` | Yes | The URL to check. Must start with `http`                           |
| `sourceUrl` | No | Initiator of this resource                                         |
| `type` | No | Request type: `script`, `image`, `xhr`, `other` (default: `other`) |

### Output

Only **blocked** composite keys are written to stdout, one per line. Non-blocked URLs produce no output.


### How it works

1. On startup, downloads the current **EasyList** and **EasyPrivacy** filter lists from `easylist.to`
2. Builds a filter engine in memory using `@ghostery/adblocker`
3. Reads lines from stdin one by one (each line one composite key null byte delimiter) 
4. For each composite key, it checks it against the engine
5. Prints the same composite key to stdout only if it matches a filter rule (i.e. is blocked)


