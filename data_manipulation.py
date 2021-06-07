import pandas as pd


# Averaging temp anomalies and intervals per decade
def average_per_decade(args):
    years, temp_flux = [], []
    for x in args:
        years.append(x.year)
        temp_flux.append(x.avg_anomaly)

    # Pandas dataframe to create two columns of upper/lower averages and decades as indices
    df = pd.DataFrame({'Anomaly Avg (F)': temp_flux}, index=years)

    # We get the decade conversion by floor dividing the index (years) and re-multiplying by 10
    decade = df.groupby((df.index // 10) * 10)
    avg_decade_anomaly = round((decade.mean()), 4)

    # Returns the values averaged per decade
    return avg_decade_anomaly


# Averages both the lower and upper confidence values by decade
def avg_lower_upper_decade(args):
    years, lower, upper = [], [], []
    for x in args:
        years.append(x.year)
        lower.append(x.lower_confidence)
        upper.append(x.upper_confidence)
    df = pd.DataFrame({'Lower Conf.': lower, 'Upper Conf.': upper}, index=years)
    decade = df.groupby((df.index // 10) * 10)
    avg_decade_confidence = round((decade.mean()), 4)

    # Returns the confidences averaged per decade
    return avg_decade_confidence


# This merges the values from both functions above together
def merge(args):
    years, lower, upper, temp_flux = [], [], [], []
    for x in args:
        years.append(x.year)
        lower.append(x.lower_confidence)
        upper.append(x.upper_confidence)
        temp_flux.append(x.avg_anomaly)
    df = pd.DataFrame({'Lower Conf.': lower, 'Upper Conf.': upper, 'Anomaly Avg.': temp_flux}, index=years)
    decade = df.groupby((df.index // 10) * 10)
    merge_values = round((decade.mean()), 4)

    # Returns the merged values averaged per decade
    return merge_values
