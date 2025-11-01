# unicode-inspect

Inspect Unicode characters and display tables with code points, names (character concepts), glyphs, and encodings (UTF‑8/16/32) in hexadecimal and bits.

# Pip installation

```bash
pip install unicode-inspect
```


## Local installation

```bash
pip install -e .
```

Requirements: Python >= 3.8

## CLI usage

```bash
unicode-inspect "A€😀"
```

Example output (default table format):

```
╒══════════════╤═══════════════════════════════════════════╤════════════════════════╤═══════════╤══════════════╤════════════════════════════════════════════════════╕
│ Code point   │ Character concept (Unicode name)          │ Visual representation (glyph) │ Decimal  │ UTF-8 (hex)  │ UTF-8 (bit)                                     │
├──────────────┼───────────────────────────────────────────┼────────────────────────┼───────────┼──────────────┼────────────────────────────────────────────────────┤
│ U+0041       │ LATIN CAPITAL LETTER A                    │ A                      │ 65        │ 41           │ 01000001                                           │
│ U+20AC       │ EURO SIGN                                 │ €                      │ 8364      │ E2 82 AC     │ 11100010 10000010 10101100                         │
│ U+1F600      │ GRINNING FACE                             │ 😀                     │ 128512    │ F0 9F 98 80  │ 11110000 10011111 10011000 10000000                │
╘══════════════╧═══════════════════════════════════════════╧════════════════════════╧═══════════╧══════════════╧════════════════════════════════════════════════════╛
```

### Change format

```bash
unicode-inspect "€" --format markdown
unicode-inspect "€" --format csv
unicode-inspect "€" --format json
```

### Add an additional encoding (besides UTF-8)

```bash
unicode-inspect "€" --encoding utf-16-le
```

### Notes
- Control, surrogate, or unassigned characters are shown with a placeholder `␣` in the *glyph* column.
- UTF-8 is always displayed; the `--encoding` option adds columns for a second encoding.
- Use `--no-header` for compact script-friendly tables.

## License
MIT