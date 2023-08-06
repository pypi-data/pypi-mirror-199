from platform import system

if system() == 'Windows':
    from devoud.browser.utils.os_utils.win32_utils import make_shortcut
elif system() == 'Darwin':
    from devoud.browser.utils.os_utils.mac_utils import make_shortcut
else:
    from devoud.browser.utils.os_utils.linux_utils import make_shortcut


