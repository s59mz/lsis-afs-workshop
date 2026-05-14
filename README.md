# LSIS-AFS Workshop Artifacts
This package contains LSIS-AFS interoperability artifacts prepared for
workshop exchange and black-box protocol testing.
Directory structure:

```text
lsis-afs-workshop/
├── code_vectors/
├── frame_vectors/
├── reports/
└── scripts/
```
⸻

## Contents

`code_vectors/`

Generated spreading code test vectors.

Includes:

* Gold codes
* Weil primary codes
* Weil tertiary codes
* Secondary codes

Format:

`codes_prnXXX.hex`

Used for Gateway-1 interoperability verification.

⸻

`frame_vectors/`

Generated LSIS-AFS navigation frame vectors.

Includes:

* message_1 : all zeros
* message_2 : all ones
* message_3 : alternating bits
* message_4 : bytewise marker
* message_5 : xorshift32 PRNG
* boundary frames

Used for Gateway-2 and Gateway-3 interoperability verification.

⸻

`reports/`

Validation and interoperability reports.

Includes:

* Gateway-1 code validation
* Gateway-2 FEC validation
* Gateway-3 frame validation

⸻

`scripts/`

Standalone comparison utilities.

These scripts intentionally avoid dependencies on the main LSIS-AFS source tree.

`compare_code_vectors.py`

Compare generated code vectors against a reference implementation.

Usage:

```
python3 compare_code_vectors.py \
    reference_code_vectors \
    candidate_code_vectors
```

Example:

```
python3 scripts/compare_code_vectors.py ../lsis-afs/artifacts/code_vectors ./code_vectors
```

⸻

`compare_frame_vectors.py`

Compare generated frame vectors against a reference implementation.

Usage:

```
python3 compare_frame_vectors.py \
    reference_frame_vectors \
    candidate_frame_vectors
```

Example:

```
python3 scripts/compare_frame_vectors.py ../lsis-afs/artifacts/frame_vectors ./frame_vectors
```

⸻

Notes

* Frame vectors are compared byte-for-byte.
* Code vectors are normalized before comparison:
  * comments ignored
  * blank lines ignored
  * whitespace normalized
* Binary frame headers use little-endian encoding.
* All symbols represented as uint8 {0,1}.
* Bit ordering is MSB-first.


