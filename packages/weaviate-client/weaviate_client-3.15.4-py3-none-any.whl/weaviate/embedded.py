import hashlib
import os
import platform
import signal
import socket
import stat
import subprocess
import tarfile
import time
import urllib.request
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

from weaviate.exceptions import WeaviateStartUpError

DEFAULT_BINARY_PATH = str((Path.home() / ".cache/weaviate-embedded/"))
DEFAULT_PERSISTENCE_DATA_PATH = str((Path.home() / ".local/share/weaviate"))
GITHUB_RELEASE_DOWNLOAD_URL = "https://github.com/weaviate/weaviate/releases/download/"


@dataclass
class EmbeddedOptions:
    persistence_data_path: str = os.environ.get("XDG_DATA_HOME", DEFAULT_PERSISTENCE_DATA_PATH)
    binary_path: str = os.environ.get("XDG_CACHE_HOME", DEFAULT_BINARY_PATH)
    version: str = "https://github.com/weaviate/weaviate/releases/download/v1.18.1/weaviate-v1.18.1-linux-amd64.tar.gz"
    port: int = 6666
    hostname: str = "127.0.0.1"
    cluster_hostname: str = "embedded"
    additional_env_vars: Optional[Dict[str, str]] = None


def get_random_port() -> int:
    sock = socket.socket()
    sock.bind(("", 0))
    port_num = int(sock.getsockname()[1])
    sock.close()
    return port_num


class EmbeddedDB:
    def __init__(self, options: EmbeddedOptions):
        self.data_bind_port = get_random_port()
        self.options = options
        self.pid = 0
        self.ensure_paths_exist()
        self.check_supported_platform()
        self._parsed_weaviate_version = ""
        if self.options.version.startswith(GITHUB_RELEASE_DOWNLOAD_URL):
            # replace with str.removeprefix() after 3.8 has been deprecated
            self._parsed_weaviate_version = self.options.version[
                len(GITHUB_RELEASE_DOWNLOAD_URL) :
            ].split("/")[0]

    def __del__(self):
        self.stop()

    def ensure_paths_exist(self):
        Path(self.options.binary_path).mkdir(parents=True, exist_ok=True)
        Path(self.options.persistence_data_path).mkdir(parents=True, exist_ok=True)

    def ensure_weaviate_binary_exists(self):
        self._weaviate_binary_path = Path(
            self.options.binary_path,
            "weaviate-"
            + self._parsed_weaviate_version
            + "-"
            + str(hashlib.sha256(self.options.version.encode("utf-8")).hexdigest()),
        )
        if not self._weaviate_binary_path.exists():
            print(
                f"Binary {self.options.binary_path} did not exist. Downloading binary from {self.options.version}"
            )
            tar_filename = Path(self.options.binary_path, "tmp_weaviate.tgz")
            urllib.request.urlretrieve(self.options.version, tar_filename)
            binary_tar = tarfile.open(tar_filename)
            binary_tar.extract("weaviate", path=Path(self.options.binary_path))
            (Path(self.options.binary_path) / "weaviate").rename(self._weaviate_binary_path)
            tar_filename.unlink()

            # Ensuring weaviate binary is executable
            self._weaviate_binary_path.chmod(
                self._weaviate_binary_path.stat().st_mode | stat.S_IEXEC
            )

    def is_listening(self) -> bool:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.options.hostname, self.options.port))
            s.close()
            return True
        except (socket.error, ConnectionRefusedError):
            s.close()
            return False

    def wait_till_listening(self):
        seconds = 30
        sleep_interval = 0.1
        retries = int(seconds / sleep_interval)
        while self.is_listening() is False and retries > 0:
            time.sleep(sleep_interval)
            retries -= 1
        if retries == 0:
            raise WeaviateStartUpError(
                f"Embedded DB did not start listening on port {self.options.port} within {seconds} seconds"
            )

    @staticmethod
    def check_supported_platform():
        if platform.system() in ["Darwin", "Windows"]:
            raise WeaviateStartUpError(
                f"{platform.system()} is not supported with EmbeddedDB. Please upvote the feature request if "
                f"you want this: https://github.com/weaviate/weaviate-python-client/issues/239"
            )

    def start(self):
        if self.is_listening():
            print(f"embedded weaviate is already listing on port {self.options.port}")
            return

        self.ensure_weaviate_binary_exists()
        my_env = os.environ.copy()

        my_env.setdefault("AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED", "true")
        my_env.setdefault("QUERY_DEFAULTS_LIMIT", "20")
        my_env.setdefault("PERSISTENCE_DATA_PATH", self.options.persistence_data_path)
        my_env.setdefault("CLUSTER_HOSTNAME", self.options.cluster_hostname)
        # Bug with weaviate requires setting gossip and data bind port
        my_env.setdefault("CLUSTER_GOSSIP_BIND_PORT", str(get_random_port()))
        my_env.setdefault(
            "ENABLE_MODULES",
            "text2vec-openai,text2vec-cohere,text2vec-huggingface,ref2vec-centroid,generative-openai,qna-openai",
        )

        if self.options.additional_env_vars is not None:
            my_env.update(self.options.additional_env_vars)

        # filter warning about running processes.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            process = subprocess.Popen(
                [
                    f"{self._weaviate_binary_path}",
                    "--host",
                    self.options.hostname,
                    "--port",
                    str(self.options.port),
                    "--scheme",
                    "http",
                ],
                env=my_env,
            )
            self.pid = process.pid
        print(f"Started {self.options.binary_path}: process ID {self.pid}")
        self.wait_till_listening()

    def stop(self):
        if self.pid > 0:
            try:
                os.kill(self.pid, signal.SIGTERM)
            except ProcessLookupError:
                print(
                    f"Tried to stop embedded weaviate process {self.pid}. Process {self.pid} "
                    f"was not found. So not doing anything"
                )

    def ensure_running(self):
        if not self.is_listening():
            print(
                f"Embedded weaviate wasn't listening on port {self.options.port}, so starting embedded weaviate again"
            )
            self.start()
