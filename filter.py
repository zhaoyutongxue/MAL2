import numpy as np
from datetime import datetime, timedelta

def output_list_file(path, data_list):
    with open(path, "w") as outfile:
        outfile.write("date\ttime\tvalue\n")
        outfile.write("\n".join(("%s\t%s\t%s" % (date, time, val) for (date, time, val) in data_list)))
        
def print_result(result, record_number):
    record_len = len(result)
    print("successfuly write %s records in 'output.txt' file, deleted %s number of records" % (record_len, record_number - record_len))

def main():
    #
    # load data
    #
    with open('2020 MAL3.txt', "r", encoding='UTF-8') as f:    
        s = f.read()

    s = s.split() 
    del s[0:16] 

    # make the record data: 3 col * n row

    record_number = 7000
    records = s[0: 3*record_number]

    # enable this you will run all records
    # record_number = len(s)/3
    # records = s

    # datatime list, a list of dict
    table_list = list()

    # get data and covert to  a list of tuple
    for i in range(0,len(records)): 
        if i%3==0:
            date = records[i]
        elif i%3==1:
            time = records[i]
        else:
            data_time = datetime.strptime(date + ' ' + time,'%d/%m/%Y %H:%M:%S')
            table_list.append((data_time, float(records[i])))


    #
    # set up the threshold and get the range list
    #

    # get the range
    low = 375
    high = 391

    interval_minutes = 30

    datetime_range_list = list()

    for row in table_list:
        (data_time, val) = row

        # check if number is in range.
        if low <= val <= high:
            start = data_time - timedelta(minutes=interval_minutes)
            end = data_time + timedelta(minutes=interval_minutes)

            if len(datetime_range_list) > 0:
                # if range list is not empty, make the current start is greater than last end
                (_, last_end) = datetime_range_list[-1]
                if start > last_end:
                    datetime_range_list.append((start,end))
            else:
                datetime_range_list.append((start,end))


    if len(datetime_range_list) == 0:
        print("the value from %s to %s is not found over %s records" % (low, high, record_number))

    print("find %s range records in time range (%s, %s) from %s records" % (len(datetime_range_list), low, high, record_number))

    #
    # check if is in range
    #

    i = 0
    result = list()

    for row in table_list:
        (data_time, val) = row

        # if the index is out of the range. just leve because all range has been scan
        if(i > len(datetime_range_list) - 1):
            print_result(result, record_number)
            return output_list_file("output.txt", result)

        (start, end) = datetime_range_list[i]

        # if the record is not in the range, add to result.
        if not start <= data_time <= end:
            result.append((data_time.date().strftime("%m/%d/%Y"), data_time.time().strftime("%H:%M:%S"), val))

        # if the record is out of current end. go to next range
        if data_time > end:
            i = i + 1

  
    output_list_file("output.txt", result)

if __name__ == "__main__":
    main()
