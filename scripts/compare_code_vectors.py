from pathlib import Path
import argparse
import sys


def read_normalized(path: Path) -> str:
    """
    Read a code-vector file and normalize it for comparison.

    This ignores:
    - comment lines
    - blank lines
    - whitespace differences at line edges
    """
    lines = []

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        lines.append(line)

    return "\n".join(lines)


def first_difference(a: str, b: str) -> int | None:
    """
    Return first differing character index, or None if equal.
    """
    n = min(len(a), len(b))

    for i in range(n):
        if a[i] != b[i]:
            return i

    if len(a) != len(b):
        return n

    return None


def compare_files(reference: Path, candidate: Path) -> tuple[bool, int | None]:
    """
    Compare two normalized code-vector files.

    Returns:
        (exact_match, first_difference_index)
    """
    ref_text = read_normalized(reference)
    cand_text = read_normalized(candidate)

    if ref_text == cand_text:
        return True, None

    return False, first_difference(ref_text, cand_text)


def compare_dirs(reference_dir: Path, candidate_dir: Path) -> int:
    """
    Compare generated code vector files between two directories.

    Returns:
        number of mismatched or missing files
    """
    reference_files = sorted(reference_dir.glob("codes_prn*.hex"))

    if not reference_files:
        raise RuntimeError(f"No codes_prn*.hex files found in {reference_dir}")

    compared = 0
    exact = 0
    missing = 0
    different = 0

    print("LSIS-AFS Code Vector Comparison")
    print("===============================")
    print(f"Reference : {reference_dir}")
    print(f"Candidate : {candidate_dir}")
    print()

    for ref_file in reference_files:
        cand_file = candidate_dir / ref_file.name

        if not cand_file.exists():
            print(f"MISSING: {ref_file.name}")
            missing += 1
            continue

        matched, first = compare_files(ref_file, cand_file)
        compared += 1

        if matched:
            exact += 1
            # print(f"OK      : {ref_file.name}")
        else:
            different += 1
            print(
                f"DIFF    : {ref_file.name} | "
                f"first_normalized_char={first}"
            )

    print()
    print("Summary")
    print("-------")
    print(f"Compared : {compared}")
    print(f"Exact    : {exact}")
    print(f"Missing  : {missing}")
    print(f"Different: {different}")

    if compared == exact and missing == 0:
        print()
        print("OK — bit-exact normalized match.")

    return missing + different


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare LSIS-AFS generated code vector directories."
    )

    parser.add_argument(
        "reference_dir",
        type=Path,
        help="Directory containing reference codes_prn*.hex files.",
    )

    parser.add_argument(
        "candidate_dir",
        type=Path,
        help="Directory containing candidate codes_prn*.hex files.",
    )

    args = parser.parse_args()

    return compare_dirs(args.reference_dir, args.candidate_dir)


if __name__ == "__main__":
    sys.exit(main())

