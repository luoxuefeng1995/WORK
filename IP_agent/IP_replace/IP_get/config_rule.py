parse_rule = [
    {
        'name' : 'xici',
        'url' : ['https://www.xicidaili.com/nn/{}'.format(i) for i in range(1, 4)],
        'parse_rule' : 'xpath',
        'ip' : '//*[@id="ip_list"]/tr/td[2]/text()',
        'port' : '//*[@id="ip_list"]/tr/td[3]/text()'

    }
]

# print(parse_rule)