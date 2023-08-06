from .constants import parameter_to_return_value
def out_of_bands(raw_df,
                 optimal_bands={"AREA_COUNT": [0, 0]},
                 telemetries=["AREA_COUNT"],
                 add_sensors_average=False,
                 ):
    '''
    :param raw_df: a df of the allSensors type where the index is a datetime and sensor columns have _telemetry in their name
    :param optimal_bands: dictionary of telemetry in caps and inclusive range outside of which the sensor is considered out of bands
    :param telemetries: telemetries in caps
    :param add_sensors_average: if True, it calculates the average of out of bands for sensors with a given telemetry and adds it to the computation
    :return df, df_grouped, df_grouped_averages: where
            df will be of the form [datetime index, various sensorX_telemetryY, avg_telemetryY]
            and df_grouped will be the same but grouped by month-day-hour
            and df_grouped_averages will be the same as df_grouped but only taking the avg_telemetryY bits
    '''

    # calculate the average % time that each sensor has been out of bands for each metric
    df = raw_df.copy()
    nameList = df.columns
    cols = []
    avg_cols = []
    for telemetry in telemetries:
        for sensor in nameList:
            metric = parameter_to_return_value[telemetry]
            if metric in sensor and "avg_sensor_" not in sensor:
                optimal_min = optimal_bands[telemetry][0]
                optimal_max = optimal_bands[telemetry][1]
                # determine for each point in time, sensor and metric whether it was out of bands or not
                df[sensor] = df[sensor].apply(lambda x: 1 if ((x > optimal_max) or (x < optimal_min)) else 0)
                cols += [sensor]
        if add_sensors_average:
            df["avg_sensor_" + metric] = df[[col for col in df.columns if metric in col]].mean(axis=1)
            cols += ["avg_sensor_" + metric]
            avg_cols += ["avg_sensor_" + metric]

    # limit response to those sensors with selected telemetries
    df = df[cols]

    #return values
    return df

def mean_by(df,by="year_month_day_hour_minute",resample_rule="15Min",convention="start",operation="mean",interval_operation="mean"):
    '''
    :param df: df with a datetime index and sensor readings
    :param by: any subsegment of "year_month_day_hour_minute"
    :param resample_rule: see https://stackoverflow.com/questions/17001389/pandas-resample-documentation
    :param operation: EG ACROSS ALL 15MIN INTERVALS STARTING AT 8AM: "mean" (default), "median", "sum", "max", "min", "first", "last", or "quantileXX" where XX is between 00 and 99
    :param interval_operation: EG WITHIN EACH 15 MINS BLOCK: "mean" (default), "median", "sum", "max", "min", "first", "last", or "quantileXX" where XX is between 00 and 99
    :return:
    '''
    #resample and apply operation
    if resample_rule!="":
        if interval_operation == "mean":
            df_grouped = df.resample(rule=resample_rule,convention=convention).mean().copy()
        elif interval_operation == "sum":
            df_grouped = df.resample(rule=resample_rule,convention=convention).sum().copy()
        elif interval_operation == "min":
            df_grouped = df.resample(rule=resample_rule,convention=convention).min().copy()
        elif interval_operation == "max":
            df_grouped = df.resample(rule=resample_rule,convention=convention).max().copy()
        elif interval_operation == "first":
            df_grouped = df.resample(rule=resample_rule,convention=convention).first().copy()
        elif interval_operation == "last":
            df_grouped = df.resample(rule=resample_rule,convention=convention).last().copy()
        elif interval_operation == "median":
            df_grouped = df.resample(rule=resample_rule,convention=convention).median().copy()
        elif interval_operation[0:8] == "quantile":
            df_grouped = df.resample(rule=resample_rule,convention=convention).quantile(int(interval_operation[8:])/100).copy()
        else:
            df_grouped = df.resample(rule=resample_rule, convention=convention).mean().copy()

    else:
        df_grouped = df.copy()

    #what is it that we want to show?
    by_split = by.split(sep="_")
    df_grouped['iso_idx'] = df_grouped.index
    df_grouped['iso_idx'] = df_grouped['iso_idx'].apply(lambda x: x.isoformat())
    df_grouped['grouping']=""
    if "year" in by_split:
        df_grouped['grouping'] = df_grouped['grouping'] + df_grouped['iso_idx'].apply(lambda x: x[2:4])
    if "month" in by_split:
        df_grouped['grouping'] = df_grouped['grouping'] + df_grouped['iso_idx'].apply(lambda x: x[5:7])
    if "day" in by_split:
        df_grouped['grouping'] = df_grouped['grouping'] + df_grouped['iso_idx'].apply(lambda x: "-" + x[8:10])
    if "hour" in by_split:
        df_grouped['grouping'] = df_grouped['grouping'] + df_grouped['iso_idx'].apply(lambda x: " " + x[11:13])
    if "minute" in by_split:
        df_grouped['grouping'] = df_grouped['grouping'] + df_grouped['iso_idx'].apply(lambda x: ":" + x[14:16])
    if by=="month_day":
        df_grouped['grouping'] = "_" + df_grouped['grouping']

    #delete temp field
    df_grouped = df_grouped.drop(columns=["iso_idx"])

    #group
    if operation=="mean":
        df_grouped = df_grouped.groupby("grouping").mean().dropna(how="all") #when we resample we create NAs for the out of office hours
    elif operation=="sum":
        df_grouped = df_grouped.groupby("grouping").sum().dropna(how="all")  # when we resample we create NAs for the out of office hours
    elif operation=="min":
        df_grouped = df_grouped.groupby("grouping").min().dropna(how="all")  # when we resample we create NAs for the out of office hours
    elif operation=="max":
        df_grouped = df_grouped.groupby("grouping").max().dropna(how="all")  # when we resample we create NAs for the out of office hours
    elif operation=="first":
        df_grouped = df_grouped.groupby("grouping").first().dropna(how="all")  # when we resample we create NAs for the out of office hours
    elif operation=="last":
        df_grouped = df_grouped.groupby("grouping").last().dropna(how="all")  # when we resample we create NAs for the out of office hours
    elif operation=="median":
        df_grouped = df_grouped.groupby("grouping").median().dropna(how="all")  # when we resample we create NAs for the out of office hours
    elif operation[0:8] == "quantile":
        df_grouped = df_grouped.groupby("grouping").quantile(int(operation[8:]) / 100).dropna(how="all")  # when we resample we create NAs for the out of office hours
    else:
        df_grouped = df_grouped.groupby("grouping").mean().dropna(how="all")  # when we resample we create NAs for the out of office hours

    return df_grouped


def weekday_comparison(df,split_by_sensor=False,by="hour_minute",resample_rule="15Min",convention="start",time_operation="mean",weekday_operation="mean"):
    '''
    :param df: allSensors type of df
    :param split_by_sensor: if True - it will generate a  period x weekday pivot table for each sensor and return all of them. If False - it will average all sensors readings first.
    :param by: any subsegment of "month_day_hour_minute"
    :param resample_rule: see https://stackoverflow.com/questions/17001389/pandas-resample-documentation
    :param convention: "start" or "end" - normally we'll use "start" to note that hour = 09 includes from 09:00 to 09:59
    :param time_operation: "mean", "min","max", "first","last" etc. Applies to each time interval, i.e. how time intervals are built ("take the peak value within the bracket 8:00-8:15")
    :param weekday_operation: "mean", "min","max", "first","last" etc. Applies to each day of the week. E.g. calculate the mean value for each 8:00-8:15 interval that fell on a Monday.
    :return: either a single df (if we dont split by sensor) or a list of dfs, all of them of the type period x weekday
    '''
    weekdays = ["1_Mon", "2_Tue", "3_Wed", "4_Thu", "5_Fri", "6_Sat", "7_Sun"]
    global _df_grouped
    _df_grouped = df.copy()

    #if we're not splitting by sensor, we need to calculate an average
    if split_by_sensor==False:
        _df_grouped["average"] = _df_grouped.mean(axis=1)
        _df_grouped = _df_grouped[["average"]]
    #calculate day of the week
    _df_grouped["weekday"] = _df_grouped.index.weekday
    _df_grouped["weekday"] = _df_grouped["weekday"].apply(lambda x: weekdays[x])

    list_dfs = []
    #loop for each sensor
    for sensor in _df_grouped.columns[:-1]:
        #first, resample data set based on time_operation:
        exec ("_df_grouped = _df_grouped.resample(rule=resample_rule)."+time_operation+"()")
        #then, resample data set based on how we want to aggregate data within the same weekday
        df_weekday = _df_grouped.pivot(columns="weekday", values=sensor)
        df_weekday = mean_by(df=df_weekday, by=by, resample_rule=resample_rule, convention=convention,operation=weekday_operation)
        list_dfs+=[df_weekday]

    #return single df (if only on sensor or if choosing average) or the list of them
    if len(list_dfs)==1:
        return list_dfs[0]
    else:
        return list_dfs

