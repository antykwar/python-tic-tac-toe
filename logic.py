class BasicGameLogic:
    @staticmethod
    def get_winner_combination(snapshot):
        result = {'winner': None, 'winner_combination': None}
        winner_combinations = BasicGameLogic._winner_combinations()

        for combination in winner_combinations:
            combination_result = set()

            for index in combination:
                combination_result.add(snapshot[index])

            if len(combination_result) == 1:
                marker = combination_result.pop()
                if marker == '-':
                    continue
                result['winner'] = marker
                result['winner_combination'] = combination
                return result

        return result

    @staticmethod
    def _winner_combinations():
        winner_combinations = (
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 4, 8), (2, 4, 6)
        )
        return winner_combinations


class PvpGameLogic(BasicGameLogic):
    def __init__(self):
        super(PvpGameLogic, self).__init__()

    def get_movement_result(self, snapshot):
        return self.get_winner_combination(snapshot)
