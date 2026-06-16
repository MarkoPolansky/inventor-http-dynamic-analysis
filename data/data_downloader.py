# Generated using Claude Sonnet 4.6
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET
from urllib.parse import urljoin
from pathlib import Path
import concurrent.futures
import threading
import tempfile
import zipfile
import io


BASE_URL = "https://nextcloud.fit.vutbr.cz/public.php/dav/files/8siMfiKcp4Y7oAq/"

ROOT = Path(__file__).resolve().parent.parent
DATA_RAW_DIR = ROOT / "data" / "raw"

print_lock = threading.Lock()

CHUNK = 1024 * 1024  # 1 MB per chunk for streaming downloads


def _fmt_size(bytes_: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if bytes_ < 1024:
            return f"{bytes_:.1f} {unit}"
        bytes_ /= 1024
    return f"{bytes_:.1f} TB"


def list_files() -> list[tuple[str, int]]:
    req = Request(BASE_URL, method="PROPFIND")
    req.add_header("Depth", "1")

    with urlopen(req) as resp:
        xml_data = resp.read()

    root = ET.fromstring(xml_data)
    ns = {"d": "DAV:"}

    files = []
    for response in root.findall("d:response", ns):
        href = response.find("d:href", ns).text
        size_node = response.find(".//d:getcontentlength", ns)
        size = int(size_node.text) if size_node is not None else 0
        if href.endswith(".json"):
            files.append((href, size))

    return files


def download_file(url: str, name: str) -> None:
    try:
        with urlopen(urljoin(BASE_URL, url), timeout=30) as r:
            with open(DATA_RAW_DIR / name, "wb") as f:
                while True:
                    chunk = r.read(CHUNK)
                    if not chunk:
                        break
                    f.write(chunk)

        with print_lock:
            print(f"downloaded: {name}")

    except Exception as e:
        with print_lock:
            print(f"failed {name}: {e}")


def download_selected(files: list[tuple[str, int]], indexes: list[int], max_workers: int = 5) -> None:
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    print("Downloading...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        tasks = [
            executor.submit(download_file, files[i][0], files[i][0].split("/")[-1])
            for i in indexes
        ]
        for t in concurrent.futures.as_completed(tasks):
            try:
                t.result()
            except Exception as e:
                with print_lock:
                    print(f"error: {e}")


def download_and_extract_zip(url: str) -> None:
    """Stream a ZIP from url to a temp file on disk, then extract only .json entries.

    Streaming in chunks avoids loading hundreds of MB into RAM at once,
    which would block the process and look like a hang.
    """

    print("Downloading ZIP...")

    tmp_path = Path(tempfile.mktemp(suffix=".zip"))

    try:
        with urlopen(url, timeout=120) as resp:
            content_length = resp.headers.get("Content-Length")
            if content_length:
                print(f"Total size: {_fmt_size(int(content_length))}")

            downloaded = 0
            with open(tmp_path, "wb") as tmp:
                while True:
                    chunk = resp.read(CHUNK)
                    if not chunk:
                        break
                    tmp.write(chunk)
                    downloaded += len(chunk)
                    print(f"\r  {_fmt_size(downloaded)} downloaded...", end="", flush=True)

        print(f"\r  {_fmt_size(downloaded)} downloaded.   ")

    except Exception as e:
        print(f"\nDownload failed: {e}")
        tmp_path.unlink(missing_ok=True)
        return

    try:
        zf = zipfile.ZipFile(tmp_path)
    except zipfile.BadZipFile:
        print("Not a valid ZIP archive.")
        tmp_path.unlink(missing_ok=True)
        return

    json_entries = [e for e in zf.infolist() if e.filename.endswith(".json")]

    if not json_entries:
        print("No .json files found in archive.")
        zf.close()
        tmp_path.unlink(missing_ok=True)
        return

    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)

    for entry in json_entries:
        # Flatten path: write every file directly into DATA_RAW_DIR.
        name = Path(entry.filename).name
        (DATA_RAW_DIR / name).write_bytes(zf.read(entry.filename))
        print(f"extracted: {name}")

    zf.close()
    tmp_path.unlink(missing_ok=True)
    print(f"Done. Files written to: {DATA_RAW_DIR}")


def main() -> None:
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    files: list[tuple[str, int]] = []

    ZIP_ALL_FILES_URL = "https://nextcloud.fit.vutbr.cz/public.php/dav/files/8siMfiKcp4Y7oAq/?accept=zip"

    while True:
        print("\n=== Nextcloud CLI ===")
        print("1) List files")
        print("2) Download selected files (parallel)")
        print("3) Download ZIP containing all files and unzip")
        print("4) Exit")

        choice = input("> ").strip()

        if choice == "1":
            files = list_files()
            for i, (f, size) in enumerate(files, 1):
                print(f"[{i}] {f.split('/')[-1]}  ({_fmt_size(size)})")

        elif choice == "2":
            if not files:
                files = list_files()

            selected = input("Enter indexes (e.g. 1-5 or 1 3 7): ").strip()
            if not selected:
                continue

            parts = selected.split()
            if len(parts) == 1 and "-" in parts[0]:
                lo, hi = parts[0].split("-", 1)
                indexes = list(range(int(lo) - 1, int(hi)))
            else:
                indexes = [int(p) - 1 for p in parts]

            download_selected(files, indexes)

        elif choice == "3":
            download_and_extract_zip(ZIP_ALL_FILES_URL)

        elif choice == "4":
            break

        else:
            print("Invalid choice.")


main()