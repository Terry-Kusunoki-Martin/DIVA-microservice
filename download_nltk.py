"""
Used to download resources from NLTK through the Noblis proxy.
"""

import argparse
import ssl
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("resources", nargs="+", help="Names of resources to download (e.g., punkt)")
    parser.add_argument(
        "--dest", type=Path, help="The directory to put the resources.", default="resources"
    )
    return parser.parse_args()


def download_nltk_from_web(resources: list[str], dest: Path):
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    import nltk

    dler = nltk.downloader.Downloader(download_dir=dest)
    print("Downloading NLTK data.")
    for resource in resources:
        print(f"Downloading: '{resource}'")
        dler.download(resource)
    print("Downloaded NLTK data.")


if __name__ == "__main__":
    args = parse_args()
    download_nltk_from_web(**vars(args))
