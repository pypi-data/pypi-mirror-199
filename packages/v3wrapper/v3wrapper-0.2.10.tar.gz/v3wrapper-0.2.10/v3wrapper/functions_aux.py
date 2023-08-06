#required imports
import requests
import re
import pandas as pd

def __build_dictionary(parent_href, category_name, user, pwd, separator="'"):
    response = requests.get(parent_href, auth=(user, pwd))
    r = response.json()
    dictionary = dict()
    for item in r['items']:
        item_href = item['href']
        for metadata in item['item-metadata']:
            if metadata['rel'] == 'urn:X-hypercat:rels:hasDescription:en':
                s = metadata['val']
                des = re.findall(category_name + separator + r"(.*)", s)
                if des != []:
                    if separator == "":
                        item_name = des[0]
                    else:
                        item_name = ""
                        for subname in re.findall(separator + r"([^" + separator + r"]*)" + separator,
                                                  separator + des[0]):
                            item_name = item_name + "~" + subname
                        item_name = item_name[1:]
                    if item_name in dictionary:
                        dictionary[item_name] = dictionary[item_name] + [item_href]
                    else:
                        dictionary[item_name] = [item_href]

    return dictionary


def __fill_dataframe_gaps(df, from_time='2022-01-01T00:00:00', to_time='2022-01-21T23:59:00', interval="min",
                          interval_freq="",na_fill="ffill"):
    '''
    :param df:
    :param from_time:
    :param to_time:
    :param interval:
    :param interval_freq:
    :param method: "ffill", None, or the value we want to add
    :return:
    '''
    if na_fill==None:
        return df
    else:
        # Create full time series
        new_df = pd.DataFrame(index=pd.date_range(from_time, to_time, freq=interval_freq + interval))
        # Concatenate items
        new_df = pd.concat([new_df, df], axis=1)
        # fill blanks
        if na_fill=="ffill":
            new_df = new_df.fillna(method='ffill')
        else:
            new_df = new_df.fillna(na_fill)
        # initial blanks dropped
        new_df = new_df.dropna()
        # return value
        return new_df

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def list_results(result,tab="___"):
    if not (isinstance(result,list) or isinstance(result,dict) or isinstance(result,tuple)):
        print(tab,result)
        return
    if isinstance(result,list) or isinstance(result,tuple):
        for listElement in result:
            list_results(listElement)
        return
    for key in result:
        value = result[key]
        if isinstance(value,dict):
            print(tab, key)
            newtab=tab+"___"
            list_results(value,newtab)
        elif isinstance(value,list):
            print(tab, key)
            newtab = tab + "___"
            for listElement in value:
                list_results(listElement,newtab)
        else:
            print(tab,key,":",result[key])
