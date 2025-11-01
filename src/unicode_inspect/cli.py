from __future__ import annotations
import argparse
import json
import sys
from tabulate import tabulate
from .core import describe_text, Encoding


COLUMNS_BASE = [
    ("codepoint", "Code point"),
    ("char_concept", "Character concept (Unicode name)"),
    ("glyph", "Visual representation (glyph)"),
    ("decimal", "Decimal"),
    ("utf8_hex", "UTF-8 (hex)"),
    ("utf8_bits", "UTF-8 (bit)"),
]


def make_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="unicode-inspect",
        description="Display tables with Unicode information (code points, names, glyphs, UTF‑8/16/32 encodings in hex and bits)",
    )
    p.add_argument("text", nargs="+", help="Text to inspect (you can pass multiple arguments which will be joined with spaces)")
    p.add_argument("--encoding", default="utf-8", choices=["utf-8","utf-16-le","utf-16-be","utf-32-le","utf-32-be"], help="Additional encoding to display besides UTF-8")
    p.add_argument("--format", dest="fmt", default="table", choices=["table","markdown","csv","json"], help="Output format")
    p.add_argument("--no-header", action="store_true", help="Do not print table/csv headers")
    return p


def main(argv: list[str] | None = None) -> int:
    args = make_parser().parse_args(argv)
    text = " ".join(args.text)

    rows = describe_text(text, encoding=args.encoding)

    extra_cols = []
    if args.encoding != "utf-8":
        extra_cols = [
            (f"{args.encoding}_hex", f"{args.encoding.upper()} (hex)"),
            (f"{args.encoding}_bits", f"{args.encoding.upper()} (bit)"),
        ]

    cols = COLUMNS_BASE + extra_cols

    if args.fmt == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0

    if args.fmt == "csv":
        import csv
        writer = csv.writer(sys.stdout)
        headers = [label for _, label in cols]
        if not args.no_header:
            writer.writerow(headers)
        for r in rows:
            writer.writerow([r.get(key, "") for key, _ in cols])
        return 0

    headers = None if args.no_header else [label for _, label in cols]
    table = [[r.get(key, "") for key, _ in cols] for r in rows]

    tablefmt = "fancy_grid" if args.fmt == "table" else "github"
    print(tabulate(table, headers=headers, tablefmt=tablefmt))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())