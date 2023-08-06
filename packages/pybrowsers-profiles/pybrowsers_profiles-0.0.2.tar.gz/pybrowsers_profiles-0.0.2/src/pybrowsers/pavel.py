from . import helpers
from .browser import BrowsersFound
from .browser import Browser

name = "firefox"
helpers.logging_debug(True)
config = helpers.get_browser_config(name)
browser = Browser(settings=config, rofi=True)

browser.load_profiles()
browser.add_profile("Incognito")
browser.select_profile()
