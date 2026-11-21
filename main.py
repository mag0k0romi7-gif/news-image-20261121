import os, shutil

# The entry is a single pre-rendered front-page image shipped beside this
# file; the harness expects it at $MAKEFUN_OUTPUT_DIR/entry.png.

HERE = os.path.dirname(os.path.abspath(__file__))
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024  # the competition's 1 MiB cap


def find_source():
    for candidate in (os.path.join(HERE, "entry.png"),
                      os.path.join(os.getcwd(), "entry.png")):
        if os.path.isfile(candidate):
            return candidate
    raise FileNotFoundError("entry.png not found next to main.py or in cwd")


def main():
    src = find_source()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Verify what landed: a real PNG, within the size cap, complete copy.
    with open(dst, "rb") as fh:
        head = fh.read(len(PNG_SIGNATURE))
    size = os.path.getsize(dst)
    if head != PNG_SIGNATURE:
        raise ValueError("copied file is not a PNG")
    if size != os.path.getsize(src) or size > MAX_BYTES:
        raise ValueError("copied file size mismatch or over the 1 MiB cap")


if __name__ == "__main__":
    main()
