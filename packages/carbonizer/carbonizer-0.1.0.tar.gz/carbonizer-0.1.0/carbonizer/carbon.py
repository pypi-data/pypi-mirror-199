import dataclasses
import asyncio
import pathlib
import re
from urllib.parse import quote

from loguru import logger
from pyppeteer import launch

import utils


@dataclasses.dataclasses
class Carbonizer:
    input_file: str
    output_filename: str
    exclude: str
    background: utils.RGBA = utils.RGBA(0, 0, 0, 0)
    font: str

    def __call__(self):
        if not self.is_valid():
            return 0
        try:
            with open(self.input_file, "r") as f:
                code = f.read()
            self.carbonize_code(code)
        except Exception as e:
            logger.error(f"Failed to carbonize {self.input_file} - due to: {e}")

    def carbonize_code(self, code):
        loop = asyncio.get_event_loop()
        data = {"code": quote(code.encode("utf-8")),
                "backgroundColor": "rgba(0, 0, 0, 0)",
                "shadow": True
                }
        validated_body = utils.validate_body(data)
        carbon_url = utils.create_url(validated_body)
        loop.run_until_complete(self.get_response(carbon_url))

    async def get_response(self, url):
        browser, page = await open_carbonnowsh(url, "/tmp")  # FIXME - let python create a temporary path
        element = await page.querySelector("#export-container  .container-bg")
        await element.screenshot({'path': self.output_filename.absolute()})
        await browser.close()

    def is_valid(self) -> bool:
        res = False
        if self.input_file.is_file():
            res = True
        if re.search(self.exclude, self.input_file.absolute()):
            logger.debug(f"Skipping file - {self.input_file}")
            res = False
        return res


async def open_carbonnowsh(url, tmp_path):
    browser = await launch(
        defaultViewPort=None,
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False,
        headless=True,
        args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = await browser.newPage()
    await page._client.send('Page.setDownloadBehavior', {
        'behavior': 'allow',
        'downloadPath': tmp_path
    })
    await page.goto(url, timeout=100000)
    return browser, page




