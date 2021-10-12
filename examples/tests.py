import unittest

from scrapy.spiders import Spider
from scrapy.utils.url import (
    add_http_if_no_scheme,
    guess_scheme,
    _is_filesystem_path,
    strip_url,
    url_is_from_any_domain,
    url_is_from_spider,
)


__doctests__ = ['scrapy.utils.url']


class UrlUtilsTest(unittest.TestCase):

    def test_url_is_from_any_domain(self):
        url = 'http://www.wheele-bin-art.co.uk/get/product/123'
        self.assertTrue(url_is_from_any_domain(url, ['wheele-bin-art.co.uk']))
        self.assertFalse(url_is_from_any_domain(url, ['art.co.uk']))

        url = 'http://wheele-bin-art.co.uk/get/product/123'
        self.assertTrue(url_is_from_any_domain(url, ['wheele-bin-art.co.uk']))
        self.assertFalse(url_is_from_any_domain(url, ['art.co.uk']))

        url = 'http://www.Wheele-Bin-Art.co.uk/get/product/123'
        self.assertTrue(url_is_from_any_domain(url, ['wheele-bin-art.CO.UK']))
        self.assertTrue(url_is_from_any_domain(url, ['WHEELE-BIN-ART.CO.UK']))

        url = 'http://192.169.0.15:8080/mypage.html'
        self.assertTrue(url_is_from_any_domain(url, ['192.169.0.15:8080']))
        self.assertFalse(url_is_from_any_domain(url, ['192.169.0.15']))

        url = (
            'javascript:%20document.orderform_2581_1190810811.mode.value=%27add%27;%20'
            'javascript:%20document.orderform_2581_1190810811.submit%28%29'
        )
        self.assertFalse(url_is_from_any_domain(url, ['testdomain.com']))
        self.assertFalse(url_is_from_any_domain(url + '.testdomain.com', ['testdomain.com']))