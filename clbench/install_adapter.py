"""
install_adapter.py — Install the SFP bridge system into a CL-Bench checkout.

CL-Bench (https://github.com/pgasawa/continual-learning-bench) discovers systems
by scanning ``src/systems/<name>/__init__.py``. This script copies (or symlinks)
the bundled ``sfp_system`` package into ``<clbench>/src/systems/sfp`` so that
``clbench run --system sfp`` can find it.

Usage:
    # copy the adapter in (default)
    python clbench/install_adapter.py --clbench /path/to/continual-learning-bench

    # or symlink it, so edits here are reflected live
    python clbench/install_adapter.py --clbench /path/to/clbench --symlink

After installing, from the CL-Bench repo:
    uv run clbench list           # 'sfp' should appear under systems
    clbench run exploitable_poker --system sfp --schedule quick_test \\
        --system.model Qwen/Qwen2.5-1.5B-Instruct
"""

from __future__ import annotations

import argparse
import os
import shutil


def install(clbench_root: str, *, symlink: bool = False, force: bool = False) -> str:
    """Place the ``sfp_system`` package at ``<clbench>/src/systems/sfp``.

    Args:
        clbench_root: Path to a CL-Bench checkout (the repo root).
        symlink: Symlink instead of copying (live edits during development).
        force: Overwrite an existing ``sfp`` system directory.

    Returns:
        The destination path that was created.
    """
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sfp_system")
    systems_dir = os.path.join(clbench_root, "src", "systems")
    if not os.path.isdir(systems_dir):
        raise FileNotFoundError(
            f"Not a CL-Bench checkout (missing src/systems): {clbench_root}"
        )

    dest = os.path.join(systems_dir, "sfp")
    if os.path.exists(dest) or os.path.islink(dest):
        if not force:
            raise FileExistsError(
                f"{dest} already exists. Re-run with --force to overwrite."
            )
        if os.path.islink(dest) or os.path.isfile(dest):
            os.unlink(dest)
        else:
            shutil.rmtree(dest)

    if symlink:
        os.symlink(src, dest)
        print(f"Symlinked {src} -> {dest}")
    else:
        shutil.copytree(src, dest)
        print(f"Copied {src} -> {dest}")

    print("\nNext steps (from the CL-Bench repo):")
    print("  uv sync --all-extras")
    print("  uv pip install torch transformers peft accelerate  # local-model deps")
    print("  uv run clbench list   # 'sfp' should be listed under systems")
    return dest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--clbench",
        required=True,
        help="Path to a continual-learning-bench checkout (repo root).",
    )
    parser.add_argument(
        "--symlink",
        action="store_true",
        help="Symlink instead of copying (reflects edits live).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing sfp system directory.",
    )
    args = parser.parse_args()
    install(args.clbench, symlink=args.symlink, force=args.force)


if __name__ == "__main__":
    main()
