def format_cookies(cookie: str) -> dict:
    def splitattr(attr):
        attr, delimiter, value = attr.partition('=')
        return attr.strip(), (value if delimiter else '').strip()

    def filter_useless(s: str):
        """Remove the incomplete key-value"""
        return not any([s.endswith('='), s.startswith('='), not s.strip()])

    return dict(map(splitattr, filter(filter_useless, cookie.split(';'))))


if __name__ == '__main__':
    cookies = 'aliyungf_tc=AQAAAOgxCHX0LwkAkKfqerDgQpnJBr44; csrfToken=LrCpyhAqhvA9d-R2PKLn84TG; TYCID=4cd09160f18d11e8a1892fe837dc6c02; undefined=4cd09160f18d11e8a1892fe837dc6c02; ssuid=5330500629; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1543244986; _ga=GA1.2.968284323.1543244986; _gid=GA1.2.776213082.1543244986; RTYCID=3c5092102d4e47a6b1a2f95707e04abe; CT_TYCID=6f025cdb9bda4dd1abdb084954de4dbb; cloud_token=4070ccf2f7a346a48449e30b4c70d594; bannerFlag=true; token=60fe72bcd2d74322b519e1312e9c0ef9; _utm=0a0c35e772124891ac75efe84d4d2331; tyc-user-info=%257B%2522myQuestionCount%2522%253A%25220%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODgxNzg0MzQwNSIsImlhdCI6MTU0MzI0NjQ1MSwiZXhwIjoxNTU4Nzk4NDUxfQ.-W29_30t3hlMWgt54KDmEI16qR0EgphL0JGwWLxvgxW0jq1Azjn7BiyWYO7RZ9fZJFNPCRA_HqxiGwkvbkILlA%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522mobile%2522%253A%252218817843405%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODgxNzg0MzQwNSIsImlhdCI6MTU0MzI0NjQ1MSwiZXhwIjoxNTU4Nzk4NDUxfQ.-W29_30t3hlMWgt54KDmEI16qR0EgphL0JGwWLxvgxW0jq1Azjn7BiyWYO7RZ9fZJFNPCRA_HqxiGwkvbkILlA; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1543246590'
    print(format_cookies(cookies))
