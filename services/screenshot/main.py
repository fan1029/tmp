import json
import asyncio

import nb_log
from playwright.async_api import async_playwright
from services.screenshot.lifeCycleFuntion_manager import LifeCycle
from services.screenshot.plugin_service import PlguinService
import multiprocessing
import base64

pluginConfig = {
    'pluginName': 'screenshot',
    'author': 'maple',
    'maxThread': 2,
    'pluginType': 2
}

service = PlguinService(pluginConfig)


async def screenshot(context, url):
    page = await context.new_page()
    try:
        # await asyncio.sleep(random.uniform(0, 10))
        await page.goto(url, timeout=100000)
    except Exception as e:
        nb_log.error(e)
        service.setResult(url, e)
        await page.close()
        return True
    res = await page.screenshot()
    service.setResult(url, base64.b64encode(res).decode('utf-8'))
    await page.close()


async def main(msgId, urls2):
    urls = [_.strip() for _ in urls2]
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--use-gl=egl'])
        context = await browser.new_context(
            extra_http_headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
        await asyncio.gather(*(screenshot(context, url) for url in urls))
        await browser.close()
    nb_log.debug('exit-ack')
    service.ackMsg(msgId)


def runTool(msgId, url: str):
    print('start')
    asyncio.run(main(msgId, url))


@LifeCycle.toolInit
def toolInit():
    print('init')
    pass


@LifeCycle.toolRunning
def toolRun(msgId: str, msg: dict):
    urls = msg.get('url')
    if type(urls) == str:
        urls = json.loads(urls)
    p1 = multiprocessing.Process(target=runTool, args=(msgId, urls,))
    p1.start()
    p1.join()

def reg():
    service.regPluginCenter()


def runFromPythonImport():

    service.runService()


if __name__ == '__main__':
    service.runService()
