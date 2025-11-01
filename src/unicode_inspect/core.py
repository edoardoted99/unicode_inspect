from __future__ import annotations
import unicodedata
from typing import Dict, List, Literal, Tuple

PrintableCategories = {"Ll","Lu","Lt","Lo","Lm","Nd","Nl","No","Pc","Pd","Ps","Pe","Pi","Pf","Po","Sm","Sc","Sk","So","Zs"}

Encoding = Literal["utf-8","utf-16-le","utf-16-be","utf-32-le","utf-32-be"]


def _is_surrogate(cp: int) -> bool:
    return 0xD800 <= cp <= 0xDFFF


def _is_control_or_nonprintable(cp: int) -> bool:
    cat = unicodedata.category(chr(cp)) if not _is_surrogate(cp) else "Cs"
    return cat.startswith("C") and cat not in {"Zs"}


def _safe_glyph(c: str) -> str:
    cp = ord(c)
    if _is_surrogate(cp) or _is_control_or_nonprintable(cp):
        return "␣"  # placeholder for non-printable characters
    return c


def _bytes_hex_and_bits(b: bytes) -> Tuple[str, str]:
    if not b:
        return "", ""
    hx = b.hex(" ").upper()
    bits = " ".join(format(x, "08b") for x in b)
    return hx, bits


def describe_char(c: str, encoding: Encoding = "utf-8") -> Dict[str, str]:
    """Return a dictionary with all table columns for a single character."""
    if not c or len(c) != 1:
        raise ValueError("describe_char requires a single character")

    cp = ord(c)
    cp_hex = f"U+{cp:04X}"
    name = unicodedata.name(c, "<UNASSIGNED>")
    glyph = _safe_glyph(c)

    rows = {
        "codepoint": cp_hex,
        "char_concept": name,
        "glyph": glyph,
        "decimal": str(cp),
    }

    try:
        b_utf8 = c.encode("utf-8")
        hx8, bits8 = _bytes_hex_and_bits(b_utf8)
        rows["utf8_hex"] = hx8
        rows["utf8_bits"] = bits8
    except UnicodeEncodeError:
        rows["utf8_hex"] = "<NA>"
        rows["utf8_bits"] = "<NA>"

    if encoding != "utf-8":
        try:
            b_other = c.encode(encoding)
            hx, bits = _bytes_hex_and_bits(b_other)
        except UnicodeEncodeError:
            hx, bits = "<NA>", "<NA>"
        rows[f"{encoding}_hex"] = hx
        rows[f"{encoding}_bits"] = bits

    return rows


def describe_text(text: str, encoding: Encoding = "utf-8") -> List[Dict[str, str]]:
    """Describe each character in the string."""
    if text is None:
        raise ValueError("text cannot be None")
    return [describe_char(ch, encoding=encoding) for ch in text]