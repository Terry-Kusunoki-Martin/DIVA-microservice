"""
Used to download resources from the Valley Forge Nexus repository.
"""

import argparse
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import urllib3


def download_artifact(url: str, user: str, password: str, artifact: str, target_dir: Path):
    target_dir.mkdir(parents=True, exist_ok=True)

    http = urllib3.PoolManager()
    headers = urllib3.make_headers(basic_auth=user + ":" + password)
    artifact_url = "/".join([url, artifact])

    print(f"Getting artifact at url: {artifact_url}")
    response = http.request("GET", artifact_url, headers=headers)

    if response.status == 200:
        if artifact.endswith(".zip"):
            zipfile = ZipFile(BytesIO(response.data))
            zipfile.extractall(path=target_dir)
        else:
            artifact_name = artifact.split("/")[-1]
            dest = Path(target_dir, artifact_name)
            dest.write_bytes(response.data)
    else:
        print(f"Failed to download the file. HTTP status code: {response.status}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL to Nexus repository.")
    parser.add_argument("user", help="Nexus username.")
    parser.add_argument("password", help="Nexus password.")
    parser.add_argument(
        "artifacts",
        nargs="+",
        help="Nexus artifact paths (e.g., speechview/language-modeling/translation/nllb-200-distilled-500M.zip)",
    )
    parser.add_argument(
        "--dest", type=Path, help="The directory to put the resources.", default="resources"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    for artifact in args.artifacts:
        download_artifact(args.url, args.user, args.password, artifact, args.dest)


if __name__ == "__main__":
    main()
