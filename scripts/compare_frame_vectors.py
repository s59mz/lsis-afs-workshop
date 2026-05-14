import argparse
from pathlib import Path


def compare_files(reference: Path, candidate: Path) -> tuple[int, int | None]:
    """
    Compare two binary files byte-by-byte.

    Returns:
        (mismatch_count, first_mismatch_index)
    """
    ref = reference.read_bytes()
    cand = candidate.read_bytes()

    if len(ref) != len(cand):
        raise ValueError(
            f"Length mismatch: {reference.name}: "
            f"{len(ref)} vs {len(cand)}"
        )

    mismatches = 0
    first = None

    for i, (a, b) in enumerate(zip(ref, cand)):
        if a != b:
            mismatches += 1

            if first is None:
                first = i

    return mismatches, first


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare LSIS-AFS frame vectors."
    )

    parser.add_argument(
        "reference_dir",
        type=Path,
        help="Reference frame directory.",
    )

    parser.add_argument(
        "candidate_dir",
        type=Path,
        help="Candidate frame directory.",
    )

    args = parser.parse_args()

    reference_dir = args.reference_dir
    candidate_dir = args.candidate_dir

    candidate_files = sorted(candidate_dir.glob("*.bin"))

    if not candidate_files:
        raise SystemExit(
            f"No .bin files found in {candidate_dir}"
        )

    compared = 0
    exact = 0
    missing = 0

    print("LSIS-AFS Frame Vector Comparison")
    print("================================")
    print(f"Reference : {reference_dir}")
    print(f"Candidate : {candidate_dir}")
    print()

    for candidate in candidate_files:
        reference = reference_dir / candidate.name

        if not reference.exists():
            print(f"MISSING: {candidate.name}")
            missing += 1
            continue

        mismatches, first = compare_files(reference, candidate)

        compared += 1

        if mismatches == 0:
            exact += 1
            print(f"OK      : {candidate.name}")
        else:
            print(
                f"DIFF    : {candidate.name} | "
                f"mismatches={mismatches} | "
                f"first={first}"
            )

    print()
    print("Summary")
    print("-------")
    print(f"Compared : {compared}")
    print(f"Exact    : {exact}")
    print(f"Missing  : {missing}")
    print(f"Different: {compared - exact}")

    if compared == exact and missing == 0:
        print()
        print("OK — bit-exact match.")


if __name__ == "__main__":
    main()
