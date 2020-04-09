from token_rules import TokenRules

class Parser():
    def __init__(self):
        self._tr = TokenRules()

    def build(self, **kwargs):
        self._tr.build()

    def test(self, data):
        self._tr.feed_to_parser(data)

parser_obj = Parser()
parser_obj.build()
parser_obj.test("ls -a --recursive")
