"""This file handles passing the CLI arguments into the processor"""

import sys
from pathlib import Path
import argparse
import pefile
import debloat.processor

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("executable", \
                        help="Path to the executable to be debloated",\
                        type=Path)
    parser.add_argument("--output", \
                        help="Output location", type=Path,\
                        required=False)
    args = parser.parse_args()

    file_path = args.executable
    out_path = args.output

    if not out_path:
        out_path = file_path.parent \
            / f"{file_path.stem}_patched{file_path.suffix}"

    try:
        pe = pefile.PE(file_path)
    except Exception:
        print("Provided file is not an executable! \
              Please try again with an executable. \
              Maybe it needs unzipped?")
        return 1

    debloat.processor.process_pe(pe, \
                                 out_path=str(out_path), \
                                 log_message=print)
    return 0

if __name__ == "__main__":
    sys.exit(main())
