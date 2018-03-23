class PointsAccumulator:
    """Accumulates points and player ids, then produces a summary (max, min, avg, count) for each player."""

    def __init__(self):
        self._scores = {}

    def add(self, player_id, score):
        """Adds a score to the data set."""
        player_scores = self._scores.setdefault(player_id, [])
        player_scores.append(score)

    def summarize(self):
        """Summarizes the accumulated data.

        :return: a dictionary keyed on player id, containing tuple of max, min, avg, count for each player
        """
        out = {}
        for key, value in self._scores.iteritems():
            out[key] = summarize(value)
        return out


def summarize(numbers):
    """Produces a very simple summary of a list of numbers.

    :param numbers: a list of numbers
    :return: max, min, avg, count for the given list
    """
    tot = 0
    min_val = max_val = numbers[0]
    for n in numbers:
        tot += n
        if n < min_val:
            min_val = n
        elif n > max_val:
            max_val = n
    count = len(numbers)
    average = float(tot) / count
    return min_val, max_val, average, count
