class Token():
    def __init__(self, token_type: str, value: str, line_num: int):
        self.token_type = token_type
        self.value = value
        self.line = line_num

    def to_string(self) -> str:
        return "(" + self.token_type + ",\"" + self.value + "\"," + str(self.line) + ")"
    

if __name__ == "__main__":
    token: Token = Token("COLON_DASH", ":-", 1)
    print(token.to_string())