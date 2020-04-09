import lex
import yacc
import re

# TODO: Add documentation explaining specific rules and convention for token_rules

# TODO: Remove all SOURCE from final commit

class TokenRules:
    def __init__(self):
        self.lexer = None

        self.reserved_commands = {}
        self.populate_reserved_commands()

        self.tokens = list(self.reserved_commands.values()) + [
            'FLAG',
            'VERBOSE_FLAG',
            'NUMBER',
        ]

    def populate_reserved_commands(self):
        pattern = re.compile('[\W]+')
        with open("token_list") as file:
            data = file.read()
        command_list = data.split("\n")
        for command in command_list:
            # Token name should have only alphanumeric and "_" characters only
            # reserved_commands contain command(key): token_name(value)

            # FIXME: Suppose we have a command "a+" and another command "a-" then both will
            # have value/token as "a_ ". To prevent this either maintain inverted dictionary
            # where "a_" will point to "a+" and "a_1" will point to "a*" or convert all
            # non alphanumeric to corresponding ascii value to have unique value/token

            # replace every non alphanumeric with "_"
            command_value = pattern.sub("_", command)
            if (command_value != "_"):
                self.reserved_commands[command] = "t_" + str(command_value)

    # Rule for commands
    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved_commands.get(t.value, 'ID')
        return t

    # Rule for verbose flags
    def t_VERBOSE_FLAG(self, t):
        r'--[a-zA-Z]*'
        return t

    # Rule for flags
    def t_FLAG(self, t):
        r'-[a-zA-Z]*'
        return t

    # Rule for Numbers
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    # Rule for tracking line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Rule for whitespaces
    def t_whitespace(self, t):
        r'\s'

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def feed_to_parser(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)
