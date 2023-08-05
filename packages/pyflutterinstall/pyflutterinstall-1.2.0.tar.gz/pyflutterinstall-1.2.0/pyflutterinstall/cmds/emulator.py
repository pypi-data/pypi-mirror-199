"""
Command stub for sdkmanager
"""

import os
import sys

from pyflutterinstall.trampoline import trampoline
from pyflutterinstall.config import config_load

android_sdk = config_load().get("ANDROID_SDK", ".")

COMMAND = "emulator"
DEFAULT_PATH = os.path.join(android_sdk, "emulator")


def main(argv: list[str] | None = None) -> int:
    """Main"""
    return trampoline(COMMAND, args=argv, default_path=DEFAULT_PATH)


if __name__ == "__main__":
    sys.exit(main())
