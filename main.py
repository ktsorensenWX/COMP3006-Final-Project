import argparse, sys
import csv
from get_data import SeaTemps, StormData
from data_manipulation import *
from plot import *


def main():
    nh_sea_data = SeaTemps()
    storm_data = StormData()

    data_parser = argparse.ArgumentParser(description='Compiling Hurricane Initiation with Sea Temperatures')
    data_parser.add_argument('command', metavar='<command>',
                             choices=['print', 'by_decade', 'merge_storms', 'merge_majors'], type=str,
                             help='command to execute')
    data_parser.add_argument('-o', '--ofile', metavar='<outfile>', dest='ofile', action='store')
    data_parser.add_argument('-p', '--plot', action='store_true', dest='plot')
    data_parser.add_argument('-s', '--sort', metavar='<sort>', choices=['confidence', 'anomaly', 'merge', 'tropical'],
                             dest='sort')
    args = data_parser.parse_args()

    if args.command == 'print':

        head_row = [['Year', 'Annual Anomaly', 'Lower Confidence Interval', 'Upper Confidence Interval']]
        anomaly_row, confidence_row = [['Year', 'Annual Anomaly']], [['Year', 'Lower', 'Upper']]
        tropical_row = [['Year', 'Named Storms', 'Hurricanes', 'Major Hurricanes']]

        if args.sort is None:

            for x in nh_sea_data:
                row = [x.year, x.avg_anomaly, x.lower_confidence, x.upper_confidence]
                head_row.append(row)

        if args.sort == 'anomaly':

            for x in nh_sea_data:
                row2 = [x.year, x.avg_anomaly]
                anomaly_row.append(row2)

        if args.sort == 'confidence':

            for x in nh_sea_data:
                row3 = [x.year, x.lower_confidence, x.upper_confidence]
                confidence_row.append(row3)

        if args.sort == 'tropical':

            for x in storm_data:
                row4 = [x.year, x.storms, x.hurricanes, x.majors]
                tropical_row.append(row4)

        if args.ofile is None:

            if args.sort is None:
                to_stdout = csv.writer(sys.stdout)
                to_stdout.writerows(head_row)

            if args.sort == 'anomaly':
                to_stdout = csv.writer(sys.stdout)
                to_stdout.writerows(anomaly_row)

            if args.sort == 'confidence':
                to_stdout = csv.writer(sys.stdout)
                to_stdout.writerows(confidence_row)

            if args.sort == 'tropical':
                to_stdout = csv.writer(sys.stdout)
                to_stdout.writerows(tropical_row)

        else:
            with open(args.ofile, 'w', newline='') as optimised_sst:
                to_file = csv.writer(optimised_sst, quoting=csv.QUOTE_ALL)

                if args.sort is None:
                    to_file.writerows(head_row)

                if args.sort == 'anomaly':
                    to_file.writerows(anomaly_row)
                    if args.plot is not None:
                        plot_standard_anomalies(nh_sea_data.sea_values)

                if args.sort == 'confidence':
                    to_file.writerows(confidence_row)
                    if args.plot is not None:
                        plot_standard_confidence(nh_sea_data.sea_values)

                if args.sort == 'tropical':
                    to_file.writerows(tropical_row)
                    storm_data.stormCSV()
                    if args.plot is not None:
                        graphStorm(storm_data.hurricane_values)
                        graph_severe_hurricanes(storm_data.hurricane_values)

    if args.command == 'by_decade':

        if args.sort is None:

            if args.ofile is None:
                data = average_per_decade(nh_sea_data.sea_values)
                confidence = avg_lower_upper_decade(nh_sea_data.sea_values)
                data.to_csv(sys.stdout, header=False)
                confidence.to_csv(sys.stdout, header=False)
            else:
                with open(args.ofile, 'w', newline='') as decade_information:
                    data = average_per_decade(nh_sea_data.sea_values)
                    confidence = avg_lower_upper_decade(nh_sea_data.sea_values)
                    data.to_csv(decade_information, header=False)
                    confidence.to_csv(sys.stdout, header=False)

        # Sorts by anomaly from avg_per_decade
        elif args.sort == 'anomaly':

            if args.ofile is None:
                print('Decade', '|', 'Average Anomaly')
                data = average_per_decade(nh_sea_data.sea_values)
                data.to_csv(sys.stdout, header=False)
            else:
                with open(args.ofile, 'w', newline='') as decade_information:
                    data = average_per_decade(nh_sea_data.sea_values)
                    data.to_csv(decade_information, header=False)

            if args.plot is not None:
                data = average_per_decade(nh_sea_data.sea_values)
                plot_decade_anomalies(data)

        # Sorts by confidence intervals from avg_per_decade
        elif args.sort == 'confidence':

            if args.ofile is None:
                print('Decade', '|', 'Lower Conf.', '|', 'Upper Conf.')
                confidence = avg_lower_upper_decade(nh_sea_data.sea_values)
                confidence.to_csv(sys.stdout, header=False)
            else:
                with open(args.ofile, 'w', newline='') as confidence_information:
                    confidence = avg_lower_upper_decade(nh_sea_data.sea_values)
                    confidence.to_csv(confidence_information, header=False)

            if args.plot is not None:
                plot_decade_confidence(confidence)

        elif args.sort == 'merge':

            if args.plot is not None:
                merged = merge(nh_sea_data.sea_values)
                merge_decade(merged)

    if args.command == 'merge_storms':
        combine_anomaly_storms(StormData.hurricane_values, SeaTemps.sea_values)

    if args.command == 'merge_majors':
        combine_anomaly_majors(StormData.hurricane_values, SeaTemps.sea_values)


if '__main__' == __name__:
    main()
