import asyncio
import nb_log
from playwright.async_api import async_playwright
from pluginService.lifeCycleFuntion_manager import LifeCycle
from pluginService.plugin_service import PlguinService
import random
import base64


pluginConfig = {
    'pluginName': 'plugin_screenshot',
    'author': 'maple',
    'maxThread': 2,
    'pluginType': 2,
    'semaphore': 10
}

service = PlguinService(pluginConfig)
sem = asyncio.Semaphore(pluginConfig.get('semaphore'))


async def screenshot(context, url):
    async with sem:
        page = await context.new_page()
        try:
            await asyncio.sleep(random.uniform(0.1, 0.8))
            await page.goto(url, timeout=100000)
        except Exception as e:
            nb_log.error(e)
            service.reportError('截图出错', [url])
            await page.close()
            return True
        res = await page.screenshot()
        service.setResult(url, "data:image/png;base64,"+base64.b64encode(res).decode('utf-8'),finish=True)
        await page.close()


async def main(targets):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--use-gl=egl'])
        context = await browser.new_context(
            extra_http_headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},ignore_https_errors=True)
        await asyncio.gather(*(screenshot(context, url) for url in targets))
        await browser.close()
    nb_log.debug('exit-ack')
    return True


def runTool(targets):
    print('start')
    asyncio.run(main(targets, ))


@LifeCycle.toolInit
def toolInit():
    print('init')
    pass


@LifeCycle.toolRunning
def toolRun(targets: list, config: dict):
    asyncio.run(main(targets, ))
    print('finish')


def reg():
    service.regPluginCenter()


def runFromPythonImport():
    service.runService()


if __name__ == '__main__':
    service.runService()
