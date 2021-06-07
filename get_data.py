import csv, os.path, logging, requests
from collections import namedtuple
from refactor_data import DisplaySeaTemps, Storm
from bs4 import BeautifulSoup as BS
import numpy as np

# root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# adding DEBUG level information to log file
fh = logging.FileHandler('SeaHurricane.log', 'w')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)


class SeaTemps:
    # Accesses URL and requests status code
    annual_nh_sea_temps = requests.get(
        'https://www.metoffice.gov.uk/hadobs/hadsst3/data/HadSST.3.1.1.0/diagnostics/HadSST.3.1.1.0_annual_nh_ts.txt')
    saved_nh_sst = 'nh_sst.txt'

    # Main list that holds our object declared in the refactoring process
    sea_values = []

    def __init__(self):
        self._refactor_data_to_csv()
        self.response = SeaTemps.annual_nh_sea_temps.status_code

    def __iter__(self):
        # Iterates through self
        return iter(self.sea_values)

    # Acts similar to AutoMPG data collection but is much more simplified
    def _refactor_data_to_csv(self):
        # B_S_C is average Bias Sampling and Coverage Error per year
        if os.path.exists('nh_sst.txt'):
            logging.debug('os.path-exists-sea')

            Temperatures = namedtuple('Temperatures',
                                      'Year Avg_Temp Lower_Bias Upper_Bias Lower_Sampling Upper_Sampling Lower_Coverage'
                                      ' Upper_Coverage Lower_Bias_Sampling Upper_Bias_Sampling Lower_B_S_C Upper_B_S_C')
            with open(self.saved_nh_sst, 'r') as sst_file:
                # We don't want to look at data beyond 2017
                reader = csv.reader(sst_file.readlines()[1:-4], delimiter=' ', skipinitialspace=True)
                for x in reader:
                    data = Temperatures(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11])

                    # Numpy may seem a bit redundant here but since they are arrays now, popping data can be easily done
                    year = np.array(data.Year)
                    avg_temp = np.array(data.Avg_Temp)
                    lower_confidence = np.array(data.Lower_B_S_C)
                    upper_confidence = np.array(data.Upper_B_S_C)

                    # Returns a value that has specific types after being passed through refactor_data
                    self.sea_values.append(DisplaySeaTemps(year, avg_temp, lower_confidence, upper_confidence))
        else:
            self._get_data()

    def _get_data(self):
        # Gets data from website and writes to text file
        if self.annual_nh_sea_temps.status_code:
            logging.debug('response code from url: 200')
            with open(self.saved_nh_sst, 'w') as nh_sst:
                for line in self.annual_nh_sea_temps:
                    # Data is read in bytes, so here I decode that and convert it into strings
                    line = line.decode()
                    nh_sst.write(line)
            self._refactor_data_to_csv()

        else:
            logging.debug(self.annual_nh_sea_temps.status_code)


class StormData:
    # Accesses URL and requests status code
    URL = 'https://www.stormfax.com/huryear.htm'
    stat_code = requests.get(URL)
    page = requests.get(URL).text

    # Just like the above class, this holds the objects from refactor_data
    hurricane_values = []

    def __init__(self):
        self._get_data()
        self.stormDataSet()
        self.response = StormData.stat_code.status_code

    def __iter__(self):
        return iter(self.hurricane_values)

    def _get_data(self):
        # getting html

        soup = BS(self.page, 'html.parser')

        logging.debug('response code from url: 200')

        # define table
        table = soup.find('table')
        # define headers
        head = table.find_all('b')
        # define rows
        fullRow = table.find_all('tr')

        # define algorithm for correct data pull, Numpy is here to organize the data from standard lists to arrays
        singles = np.array(
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 26, 28, 30, 31,
             32, 33, 34, 37, 38, 39, 41, 43, 44, 45, 46, 49, 51, 53, 54, 56, 59, 60, 61, 62, 63, 64, 66,
             67, 68, 69, 70, 71, 72, 74, 76, 77, 78, 79, 84, 87, 88, 89, 90, 95, 96, 97, 101, 105, 106, 109, 111,
             112, 114, 116, 117, 121, 122, 124, 126, 128, 131, 132, 135, 136, 140, 141, 142, 143, 146, 158, 163])
        doubSing = np.array(
            [18, 29, 40, 47, 48, 50, 52, 55, 57, 58, 73, 75, 80, 81, 83, 85, 86, 91, 92, 93, 94, 98, 100, 102,
             103, 104, 107, 108, 110, 113,
             115, 119, 120, 123, 125, 127, 129, 130, 133, 134, 137, 138, 139, 145, 148, 149, 150, 151, 152, 153,
             155, 156, 157, 160, 162, 164, 165])
        doubDoub = np.array([19, 27, 35, 36, 42, 65, 82, 99, 118, 144, 147, 154, 159, 161, 166])

        # define attributes
        self.headers = []
        self.csvStormDat = []

        # define headers
        for header in head[:4]:
            self.headers.append(header.text)

        logging.debug('grab-table-data-hurricanes.txt')
        # define years, named storms, hurricanes, and major hurricanes
        for idx, data in enumerate(fullRow):
            if idx == 1:
                # turn rows into list
                text = data.text
                text = text.split()
                text.pop()
                text.pop()
                # iterate
                for idx, dat in enumerate(text):
                    # single algorithm
                    if idx in singles:
                        year = dat[:4]
                        nameStorm = dat[4]
                        hurricane = dat[5]
                        majhurricane = dat[6:]
                        self.csvStormDat.append((year, nameStorm, hurricane, majhurricane))
                    # double single algorithm
                    elif idx in doubSing:
                        year = dat[:4]
                        nameStorm = dat[4:6]
                        hurricane = dat[6]
                        majhurricane = dat[7:]
                        self.csvStormDat.append((year, nameStorm, hurricane, majhurricane))
                    # double double algorithm
                    elif idx in doubDoub:
                        year = dat[:4]
                        nameStorm = dat[4:6]
                        hurricane = dat[6:8]
                        majhurricane = dat[8:]
                        self.csvStormDat.append((year, nameStorm, hurricane, majhurricane))

    def stormDataSet(self):
        logging.debug('reformat-hurricane-data')

        # Appends values from refactor_data into the class list above
        for i in self.csvStormDat:
            self.hurricane_values.append(Storm(i[0], i[1], i[2], i[3]))

    def stormCSV(self):
        stormcsv = "storm-data.csv"
        logging.debug('storm-csv created')

        # write storm csv
        with open(stormcsv, 'w') as output:
            writer = csv.writer(output)
            writer.writerow(self.headers)
            for row in self.csvStormDat:
                writer.writerow(row)
