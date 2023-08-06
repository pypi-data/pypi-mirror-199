from src.TopicFactory import TopicFactory


class Velocity_in_y(TopicFactory):
    def __init__(self):

        g = 9.81

        self.input_dict = {
            "vy": ["", 3, "velocity", "", ""],
            "vyi": ["", 4, "velocity", "", ""],
            "time": ["", 5, "time", "", ""],
                      }

        self.info = {
             "input": self.input_dict,
             "formula": f"vy == vyi - {g} * time",
             "Note": "This is the velocity of the projectile at any time",
             "solve_method": "",
             "plot_method": False,
             "Bonus": self.Bonus
             }

    def giveInfo(self):
        return self.info