class SQLTablename(str):
    @property
    def parent_tablename(self) -> str:
        result = self
        if "." in result:
            result = result[result.rindex(".") + 1 :]
        return result[
            : next(
                (i for (i, letter) in enumerate(result[1:]) if letter.isupper()),
                len(result) - 1,
            )
            + 1
        ].lower()

    @property
    def camel_cased(self) -> str:
        return "".join(w.capitalize() for w in self.split("_"))

    @property
    def snake_cased(self) -> str:
        words = []
        start = 0
        for i in (i for i in range(1, len(self)) if self[i].isupper()):
            words.append(self[start:i].lower())
            start = i
        words.append(self[start:].lower())
        return "_".join(words)
