"""One Line, One Laugh — make.fun entry.

Writes a single original funny line to entry.txt and prints it to
stdout with no trailing newline. Stdlib only, deterministic.
"""

import os
import sys

LINE = "My dog learned to fetch my slippers, my newspaper, and my will to live. He only brings back two of them."

# The gate requires 1 to 140 characters; enforce it before writing.
assert 1 <= len(LINE) <= 140, "line must be 1-140 characters"


def output_dirs():
    """Candidate output directories, in preference order."""
    dirs = ["/output"]
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        dirs.append(env_dir)
    dirs.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output"))
    return dirs


def main():
    data = LINE.encode("utf-8")
    last_error = None
    for out_dir in output_dirs():
        path = os.path.join(out_dir, "entry.txt")
        try:
            os.makedirs(out_dir, exist_ok=True)
            with open(path, "wb") as f:
                f.write(data)
            with open(path, "rb") as f:
                written = f.read()
        except OSError as exc:
            last_error = exc
            continue
        if written != data:
            sys.stderr.write("entry.txt read-back mismatch\n")
            return 1
        sys.stdout.buffer.write(data)
        sys.stdout.buffer.flush()
        return 0
    sys.stderr.write("could not write entry.txt: %s\n" % last_error)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
