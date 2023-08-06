from sys import platform

if platform == 'win32':
    from devoud.browser.utils.os_utils.win32_utils import make_shortcut
elif platform == 'darwin':
    from devoud.browser.utils.os_utils.mac_utils import make_shortcut
else:
    from devoud.browser.utils.os_utils.linux_utils import make_shortcut


