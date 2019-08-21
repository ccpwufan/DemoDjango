class MovieBase:
    def __init__(self, no=0, name='', actors='', time='', score=''):
        self.data = {'no': int(no), 'name': name, 'actors': actors, 'time': time, 'score': score}

