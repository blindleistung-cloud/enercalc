"""Exercise the self-contained report through localhost, then with browser offline.

The managed system browser blocks file:// by policy. This test does not change
that policy and does not claim direct file:// validation.
Requires Playwright and a system Chromium.
"""
import functools
import http.server
import json
import pathlib
import threading

from playwright.sync_api import sync_playwright, expect

ROOT = pathlib.Path(__file__).resolve().parents[1]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def run():
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
            context = browser.new_context(viewport={'width':1440,'height':1080}, accept_downloads=True)
            page = context.new_page()
            exceptions, requests = [], []
            page.on('pageerror', lambda error: exceptions.append(str(error)))
            page.on('request', lambda request: requests.append(request.url))
            page.goto(f'http://127.0.0.1:{server.server_port}/index.html')
            page.wait_for_selector('.hero')
            assert page.evaluate('ENER_AUDIT.workbook.totalCells') == 179048
            page.screenshot(path='/tmp/enercalc-overview.png', full_page=True)
            context.set_offline(True)

            page.locator('nav a[data-view=workbook]').click()
            page.wait_for_selector('#cell-search')
            page.locator('#scope').select_option('all')
            page.locator('#kind').select_option('error')
            page.locator('#cell-search').fill('#VALUE!')
            assert '128 Treffer' in page.locator('.pagination').inner_text()
            page.locator('[data-page=next]').click()
            assert '81–128' in page.locator('.pagination').inner_text()
            page.locator('#cell-search').fill('<img src=x onerror=alert(1)>')
            assert 'Keine passenden Zellen' in page.locator('#cell-results').inner_text()
            assert page.locator('#cell-results img').count() == 0

            page.locator('button[data-tab=names]').click()
            page.locator('#data-search').fill('G_EBF')
            assert page.locator('#data-table tbody tr').count() >= 1
            page.locator('#data-table button[data-source=Eingabe][data-address=D85]').click()
            assert '821' in page.locator('#cell-detail').inner_text()
            assert 'SUMIF' in page.locator('#cell-detail pre').inner_text()
            page.screenshot(path='/tmp/enercalc-workbook.png', full_page=True)

            page.locator('button[data-tab=climate]').click()
            assert page.locator('#data-table tbody tr').count() == 18
            page.locator('button[data-tab=profiles]').click()
            assert page.locator('#data-table tbody tr').count() == 44
            page.locator('#data-search').fill('Parkhaus')
            assert '34' in page.locator('#data-table').inner_text()
            page.locator('button[data-tab=factors]').click()
            assert page.locator('#data-table tbody tr').count() == 6

            page.locator('nav a[data-view=logic]').click()
            expect(page.locator('.formula-card')).to_have_count(6)
            page.locator('button[data-source=Eingabe][data-address=E58]').click()
            assert '1,3' in page.locator('#cell-detail').inner_text()

            page.locator('nav a[data-view=vba]').click()
            page.locator('#vba-search').fill('PROJEKT_LADEN')
            assert 'Z_Data_Projektverwaltung.bas' in page.locator('#module-detail').inner_text()
            assert 'Line Input #1' in page.locator('#vba-code').inner_text()
            page.locator('#vba-search').fill('Onlinecheck')
            assert 'InternetExplorer.Application' in page.locator('#vba-code').inner_text()
            page.screenshot(path='/tmp/enercalc-vba.png', full_page=True)

            page.locator('nav a[data-view=migration]').click()
            expect(page.locator('.phase')).to_have_count(5)
            assert 'file://' in page.locator('#content').inner_text()
            with page.expect_download() as event:
                page.locator('#export').click()
            download = event.value
            data = json.loads(pathlib.Path(download.path()).read_text())
            assert data['namedRangeCount'] == 1671
            assert data['formulaCount'] == 141897

            page.set_viewport_size({'width':390,'height':844})
            page.locator('nav a[data-view=overview]').click()
            page.screenshot(path='/tmp/enercalc-mobile.png', full_page=True)
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            page.locator('nav a[data-view=workbook]').click()
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            page.locator('button[data-tab=names]').click()
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            assert not exceptions, exceptions
            assert all(url.startswith(f'http://127.0.0.1:{server.server_port}/') for url in requests), requests
            assert len(requests) == 1, requests
            print('PASS: desktop/mobile navigation, 179048 embedded cells, filtered search and pagination,')
            print('source links, 18 climates, 44 profiles, VBA source, JSON export, five migration phases.')
            print('PASS: all interactions after initial document load with browser offline; no external requests or JS exceptions.')
            print('LIMIT: direct file:// test blocked by managed Chromium policy; localhost transport used.')
            browser.close()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    run()
