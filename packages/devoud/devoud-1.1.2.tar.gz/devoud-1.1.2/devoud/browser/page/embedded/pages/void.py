from devoud.browser.page.embedded.view import EmbeddedView


class VoidPage(EmbeddedView):
    def __init__(self, abstract_page, url=None, *args):
        super().__init__(abstract_page, url, *args)
        self.title = 'Vasily ate cheese'  # Спасибо Егору
        self.url = 'devoud://void.py'
