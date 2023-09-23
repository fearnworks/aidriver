"""
This script downloads a model from Hugging Face and saves it to a specified output folder. It uses the Hugging Face API to get the download links for the model files and downloads them using multiple threads. The progress of the download is displayed using a progress bar.

The script takes in a list of models to download, the branch to download from, the number of threads to use for downloading, the output base folder, and the number of retries to attempt if the download fails.

The script defines the following functions:
- get_filename_from_url(url: str) -> str: Returns the filename from a given URL.
- get_output_path(output_folder: str, filename: str) -> str: Returns the output path for a given output folder and filename.
- get_http_response(url: str, headers: dict = {}, timeout: int = 10) -> requests.Response: Sends an HTTP GET request to the given URL with the specified headers and timeout and returns the response.
- write_content_to_file(output_path: str, data: bytes, mode: str = "ab") -> None: Writes the given data to a file at the specified output path with the specified mode.
- download_file(url: str, output_folder: str, progress_bar: Optional[Callable[[float, str], None]] = None) -> None: Downloads a file from a given URL and saves it to the specified output folder. If a progress bar function is provided, it will be called with the download progress and message.
- get_download_links(session: requests.Session, model: str, branch: str) -> List[str]: Gets the download links for the model files from the Hugging Face API for the given model and branch using the provided requests session.

The script can be run as a standalone script or imported as a module.
"""
from typing import Dict, Optional, Callable, Any, List
import base64
import json
import os
from pathlib import Path
from loguru import logger
import requests
import tqdm
from requests.adapters import HTTPAdapter
from tqdm.contrib.concurrent import thread_map
from requests import Session
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def get_filename_from_url(url: str) -> str:
    """
    Extracts the filename from a given URL.

    Args:
        url (str): The URL to extract the filename from.

    Returns:
        str: The filename.
    """
    return os.path.basename(url)


def get_output_path(folder: str, filename: str) -> str:
    """
    Constructs the full output path for a file.

    Args:
        folder (str): The output folder to save the file in.
        filename (str): The name of the file.

    Returns:
        str: The full output path.
    """
    return os.path.join(folder, filename)


def get_http_response(
    url: str, headers: Dict[str, str] = None, timeout: int = 10
) -> requests.Response:
    """
    Makes an HTTP GET request to a URL and returns the response.

    Args:
        url (str): The URL to make the request to.
        headers (Dict[str, str], optional): The headers to include in the request. Defaults to {}.
        timeout (int, optional): The timeout for the request in seconds. Defaults to 10.

    Returns:
        requests.Response: The HTTP response.
    """
    if headers is None:
        headers = {}
    return requests.get(url, stream=True, headers=headers, timeout=timeout)


def write_content_to_file(output_path: str, data: bytes, mode: str = "ab") -> None:
    """
    Writes data to a file.

    Args:
        output_path (str): The path to the file to write to.
        data (bytes): The data to write.
        mode (str, optional): The mode to open the file in. Defaults to "ab".
    """
    with open(output_path, mode) as f:
        f.write(data)


def download_file(
    url: str, folder: str, progress_bar: Optional[Callable[..., Any]] = None
) -> None:
    """
    Downloads a file from a URL and saves it to an output folder, optionally updating a progress bar.

    Args:
        url (str): The URL of the file to download.
        output_folder (str): The folder to save the downloaded file in.
        progress_bar (Callable[..., Any], optional): A function to call to update a progress bar. Defaults to None.

    Raises:
        Exception: If there is an error downloading the file.
    """
    filename = get_filename_from_url(url)
    output_path = get_output_path(folder, filename)
    headers = {}
    block_size = 1024 * 1024  # 1MB
    logger.info(url)
    try:
        response = get_http_response(url, headers=headers)
        response.raise_for_status()
        logger.info(response)
        total_size = int(response.headers.get("content-length", 0))
        with tqdm.tqdm(
            total=total_size,
            unit="iB",
            unit_scale=True,
            bar_format="{l_bar}{bar}| {n_fmt:6}/{total_fmt:6} {rate_fmt:6}",
        ) as t:
            count = 0
            for data in response.iter_content(block_size):
                t.update(len(data))
                write_content_to_file(output_path, data)
                if total_size != 0 and progress_bar is not None:
                    count += len(data)
                    progress_bar(
                        float(count) / float(total_size),
                        f"Downloading {filename}",
                    )
    except Exception as err:
        logger.error(f"Error downloading file: {err}")
        raise


####


def construct_url(base: str, page: str, cursor: Optional[bytes] = None) -> str:
    """
    Constructs a URL given the base, page, and an optional cursor.

    Args:
        base (str): The base of the URL.
        page (str): The specific page after the base.
        cursor (Optional[bytes], optional): Optional cursor for pagination. Defaults to None.

    Returns:
        str: The full URL.
    """
    return f"{base}{page}" + (f"?cursor={cursor.decode()}" if cursor else "")


def make_request(session: Session, url: str) -> Dict:
    """
    Makes a GET request to a given URL and returns the JSON content.

    Args:
        session (Session): A requests Session object to make the request.
        url (str): The URL to make the request to.

    Returns:
        Dict: The JSON content of the response.
    """
    logger.info(f"Making request to: {url}")
    r = session.get(url, timeout=10)
    r.raise_for_status()
    return json.loads(r.content)


def filter_quants(fname: str, quant_filter: Dict[str, bool]) -> bool:
    """
    Filters filenames based on a quantization filter.

    Args:
        fname (str): The filename.
        quant_filter (Dict[str, bool]): A dictionary with key-value pairs to filter filenames.

    Returns:
        bool: True if the filename contains a key from the quant_filter where the corresponding value is True,
        and does not contain a key where the corresponding value is False, else False.
    """
    if not fname.endswith(".bin"):
        return False
    for key, value in quant_filter.items():
        if key in fname:
            if value:
                continue
            else:
                return True
    return False


def extract_links(
    data_list: List[Dict], model: str, branch: str, quant_filter: Dict[str, bool]
) -> List[str]:
    """
    Extracts download links from a list of file data.

    Args:
        data_list (List[Dict]): A list of dictionaries containing file data.
        model (str): The model name.
        branch (str): The branch name.
        quant_filter (Dict[str, bool]): A dictionary with key-value pairs to filter filenames.

    Returns:
        List[str]: A list of download links.
    """
    links = []
    for file in data_list:
        fname = file["path"]
        if filter_quants(fname, quant_filter):
            logger.info(f"Filter for quantized : {fname}")
            continue
        if fname in ["1_Pooling", "2_Dense"]:
            logger.info(f"Subdir for sentence embed : {fname}")
            links.append(
                f"https://huggingface.co/{model}/resolve/{branch}/{fname}/config.json"
            )
            links.append(
                f"https://huggingface.co/{model}/resolve/{branch}/{fname}/pytorch_model.bin"
            )
            continue
        link = f"https://huggingface.co/{model}/resolve/{branch}/{fname}"
        logger.info(link)
        links.append(link)
    return links


def update_cursor(data_list: List[Dict]) -> bytes:
    """
    Updates the cursor for pagination.

    Args:
        data_list (List[Dict]): A list of dictionaries containing file data.

    Returns:
        bytes: The updated cursor.
    """
    cursor = (
        base64.b64encode(f'{{"file_name":"{data_list[-1]["path"]}"}}'.encode()) + b":50"
    )
    cursor = base64.b64encode(cursor)
    return cursor.replace(b"=", b"%3D")


def get_download_links(session: Session, model: str, branch: str) -> List[str]:
    """
    Gets download links for a given model and branch.

    Args:
        session (Session): A requests Session object to make the request.
        model (str): The model name.
        branch (str): The branch name.

    Returns:
        List[str]: A list of download links.
    """
    base = "https://huggingface.co"
    page = f"/api/models/{model}/tree/{branch}"
    cursor = b""
    links = []

    quant_filter = {
        "q2_K": False,
        "q3_K_L": False,
        "q3_K_M": False,
        "q3_K_S": False,
        "q4_0": False,
        "q4_1": False,
        "q4_K_M": False,
        "q4_K_S": False,
        "q5_0": True,
        "q5_1": False,
        "q5_K_M": False,
        "q5_K_S": False,
        "q6_K": False,
        "q8_0": False,
    }

    while True:
        url = construct_url(base, page, cursor)
        data_list = make_request(session, url)
        if len(data_list) == 0:
            break
        links.extend(extract_links(data_list, model, branch, quant_filter=quant_filter))
        cursor = update_cursor(data_list)

    return links


if __name__ == "__main__":
    models = ["TheBloke/Llama-2-7B-Chat-GGML"]
    # sentence_models = ["sentence-transformers/all-MiniLM-L6-v2", "hkunlp/instructor-xl"]
    # test_model = ["google/flan-t5-base"]

    branch = "main"
    threads = 6
    output_base = "artifacts"
    retries = 5

    for model in models:
        session = requests.Session()

        session.mount(
            "https://cdn-lfs.huggingface.co", HTTPAdapter(max_retries=retries)
        )
        session.mount("https://huggingface.co", HTTPAdapter(max_retries=retries))
        session.headers = {
            "authorization": f'Bearer {os.getenv("HUGGINGFACE_API_TOKEN")}'
        }

        output_folder = f"{'_'.join(model.split('/')[-2:])}"
        output_folder = Path(output_base) / output_folder

        links = get_download_links(session, model, branch)
        output_folder.mkdir(parents=True, exist_ok=True)
        logger.info(f"Downloading from url: https://huggingface.co/{model}")

        # Downloading the files
        print(f"Downloading the model to {output_folder}")
        thread_map(
            lambda url: download_file(url, output_folder),
            links,
            max_workers=threads,
            disable=True,
        )

        # with ThreadPoolExecutor(max_workers=threads) as executor:
        #     futures = []
        #     for url in links:
        #         futures.append(executor.submit(download_file, url, output_folder))
        #     for future in tqdm.tqdm(futures, desc="Downloading files", unit="file"):
        #         future.result()
