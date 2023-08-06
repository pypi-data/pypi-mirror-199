from usu_apex.TopicFactory import TopicFactory


class Law_of_Cosines(TopicFactory):
    def __init__(self):
        self.input_dict = {
            "a": ["", 14.62, "length", "", ""],
            "b": ["", 9, "length", "", ""],
            "c": ["", 12, "length", "", ""],
            "A": ["", "", "angle", "", ""]
        }

        self.info = {
             "input": self.input_dict,
             "formula": "a**2 == b**2 + c**2 - 2 * b * c * cos(A)",
             "Note": "This is the law of cosines",
             "solve_method": "",
             "plot_method": False,
             "Bonus": self.Bonus
             }

    def giveInfo(self):
        return self.info
