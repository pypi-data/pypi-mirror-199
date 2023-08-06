from TopicFactory import TopicFactory

class stress(TopicFactory):
    def __init__(self):
        self.input_dict = {
            "F": ["", 3, "length", "", ""],
            "A": ["", 4, "length", "", ""],
            "stress": ["", "", "length", "", ""],
                      }

        self.info = {
             "input": self.input_dict,
             "formula": "stress == F/A",
             "Note": "This is a stress calculator",
             "solve_method": "",
             "plot_method": False,
             "Bonus": self.Bonus
             }

    def giveInfo(self):
        return self.info
