"""

L'bojet qui est renvoyé à l'ia


"""



class action_feedback():

    """ init """
    def __init__(self, x_bar, x_bal, reward, partie_en_cours):
        self.x_bar = x_bar
        self.x_bal = x_bal
        self.x_reward = reward
        self.partie_en_cours = partie_en_cours



