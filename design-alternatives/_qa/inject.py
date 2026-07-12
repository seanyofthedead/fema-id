"""Inject the shared data payload into a concept template.

Usage: python inject.py <template.html> <output_index.html>

The template must contain exactly one occurrence of the token:
    /*__FEMA_DATA__*/null
(typically as:  window.FEMA_DATA = /*__FEMA_DATA__*/null;)
It is replaced with the full JSON payload, producing a self-contained file.
"""
import sys, pathlib

HERE = pathlib.Path(__file__).parent
TOKEN = "/*__FEMA_DATA__*/null"

src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
count = src.count(TOKEN)
assert count == 1, f"template must contain the data token exactly once (found {count})"
blob = (HERE / "fema_data.json").read_text(encoding="utf-8")
out = pathlib.Path(sys.argv[2])
out.write_text(src.replace(TOKEN, blob), encoding="utf-8")
print(f"wrote {out} ({out.stat().st_size:,} bytes)")
