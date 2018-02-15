from containers import ManyItems.manyTimes

@manyTimes
def fetch(data, toExtract):
    if 'datapath' in data.info:
        data.info['datapath'] = data.info.['datapath'] + '['+toExtract+']'
    else:
        data.info['datapath'] = '['+ toExtract +']'
    return data[toExtract]
