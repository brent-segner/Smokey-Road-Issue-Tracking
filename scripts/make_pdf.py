"""Render the report to a dated PDF in reports/.

Usage (from the repo root):
    pip install playwright pyyaml && python -m playwright install chromium
    python scripts/make_pdf.py              # all items, grouped by area
    python scripts/make_pdf.py --party Troyer   # only the Troyer items

The PDF is what gets emailed each week, so the dated copy in reports/ is the
record of exactly what the builder was sent.
"""
import argparse, datetime, functools, http.server, pathlib, threading, urllib.parse

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--party", choices=["Schumacher", "Troyer"], help="limit to one responsible party")
    ap.add_argument("--chrome", help="path to a Chrome/Chromium executable (optional)")
    args = ap.parse_args()

    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    handler = functools.partial(Quiet, directory=str(ROOT))
    with http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler) as httpd:
        port = httpd.server_address[1]
        threading.Thread(target=httpd.serve_forever, daemon=True).start()

        frag = ""
        if args.party:
            value = "Schumacher" if args.party == "Schumacher" else "Troyer (homeowner contract)"
            frag = "#" + urllib.parse.urlencode({"c": value})

        today = datetime.date.today().isoformat()
        suffix = f"-{args.party.lower()}" if args.party else ""
        out = ROOT / "reports" / f"smokey-road-outstanding-items-{today}{suffix}.pdf"
        out.parent.mkdir(exist_ok=True)

        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=args.chrome) if args.chrome else p.chromium.launch()
            page = browser.new_page()
            page.goto(f"http://127.0.0.1:{port}/index.html{frag}")
            page.wait_for_selector("body[data-ready='1']")
            page.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
            # Load every lazy image before printing.
            page.evaluate("document.querySelectorAll('img[loading]').forEach(i => i.loading = 'eager')")
            page.wait_for_function("[...document.images].every(i => i.complete)", timeout=60000)
            page.emulate_media(media="print")
            page.pdf(path=str(out), format="Letter", print_background=True,
                     margin={"top": "0.55in", "bottom": "0.6in", "left": "0.5in", "right": "0.5in"},
                     display_header_footer=True,
                     header_template="<span></span>",
                     footer_template=f"<div style='font-size:8px;width:100%;padding:0 0.5in;color:#555;display:flex;justify-content:space-between'>"
                                     f"<span>Smokey Road outstanding items, printed {today}</span>"
                                     "<span>Page <span class='pageNumber'></span> of <span class='totalPages'></span></span></div>")
            browser.close()
        print(out)


if __name__ == "__main__":
    main()
