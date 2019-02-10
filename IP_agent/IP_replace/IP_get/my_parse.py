from lxml import etree


class Parse(object):
    def xpath_parse(self, text, rule):
        page = etree.HTML(text)
        ip_list = page.xpath(rule['ip'])
        port_list = page.xpath(rule['port'])
        proxy_list = []
        for ip, port in zip(ip_list, port_list):
            proxy = {
                'proxy' : ip + ':'+ port
            }
            proxy_list.append(proxy)

        return proxy_list