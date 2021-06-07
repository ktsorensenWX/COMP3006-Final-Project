# This class is here to only change the types of the desired variables and give them a format for printing

class DisplaySeaTemps:
    # Applies specific types to object for SST
    def __init__(self, year, avg_anomaly, lower_confidence, upper_confidence):
        self.year = int(year)
        self.avg_anomaly = float(avg_anomaly)
        self.lower_confidence = float(lower_confidence)
        self.upper_confidence = float(upper_confidence)

    def __repr__(self):
        return f'{self.year}, {self.avg_anomaly}, {self.lower_confidence}, {self.upper_confidence}'

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash((self.year, self.avg_anomaly, self.lower_confidence, self.upper_confidence))


class Storm:
    # Applies specific types to object for Hurricane data
    def __init__(self, year, storms, hurricanes, majors):
        self.year = int(year)
        self.storms = int(storms)
        self.hurricanes = int(hurricanes)
        self.majors = int(majors)

    def __repr__(self):
        return f"{self.year} {self.storms} {self.hurricanes} {self.majors}"

    def __str__(self):
        return str(self.__repr__())
