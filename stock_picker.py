import csv
import os
import statistics
from datetime import datetime
# "%d-%b-%Y"

class StockPicker:
    def __init__(self, *args, **kwargs):
        self.filename = args[0]

    def binarySearchDate(self,query,dateArray):
        last = len(dateArray)-1
        first = 0
        mid = first + int((last - first)/2)
        while(last>first):
            mid = first + int((last - first)/2)
            if(datetime.strptime(query, "%d-%b-%Y") == datetime.strptime(dateArray[mid], "%d-%b-%Y")):
                return mid
            elif(datetime.strptime(query, "%d-%b-%Y") <= datetime.strptime(dateArray[first], "%d-%b-%Y")):
                return first
            elif(datetime.strptime(query, "%d-%b-%Y") >= datetime.strptime(dateArray[last], "%d-%b-%Y")):
                return last
            elif(datetime.strptime(query, "%d-%b-%Y") < datetime.strptime(dateArray[mid], "%d-%b-%Y")):
                last = mid - 1
            else:
                first = mid + 1
        return mid

    def inRangeDateArray(self,start,end,dateArray):
        # print(dateArray)
        start_index = self.binarySearchDate(start,dateArray)
        end_index = self.binarySearchDate(end,dateArray)
        # print(start_index,end_index)
        return dateArray[start_index:end_index+1]

    def get_mean(self,date_array,date_price_dict):
        sum_price = 0
        for date in date_array:
            # print(date_price_dict[date])
            sum_price += float(date_price_dict[date])
        return sum_price/len(date_array)

    def get_standard_deviation(self,date_array,date_price_dict):
        values = []
        for date in date_price_dict:
            values.append(float(date_price_dict[date]))
        return statistics.stdev(values)
        
    def get_profit_details(self,date_array,date_price_dict,mean_value):
        min_value = mean_value
        min_value_date = ''
        max_value = mean_value
        max_value_date = ''
        for date in date_array:
            if float(date_price_dict[date])<min_value:
                min_value_date = date
                min_value = float(date_price_dict[date])
            if float(date_price_dict[date])>max_value:
                max_value_date = date
                max_value = float(date_price_dict[date])
        return {"min_value_date":min_value_date,"max_value_date":max_value_date,"profit":max_value-min_value}

    def run(self):
        input_stock_name = input("Welcome Agent! Which stock you need to process?:-")
        proper_value_acquired = False
        while(not proper_value_acquired):
            with open(self.filename,"r") as f:
                data = csv.reader(f)
                similar_stock_names = []
                matching_date_price_dict = {}
                dates = []
                for row in data:
                    if(row[0]==input_stock_name):
                        dates.append(row[1])
                        matching_date_price_dict[row[1]] = row[2]
                    elif(input_stock_name in row[0] ):
                        similar_stock_names.append(row[0])
                f.close()
                if len(matching_date_price_dict) == 0:
                    if len(similar_stock_names)==0:
                        print("Not able to find the emtioned stock")
                    else:
                        confirm =input("Did you mean " + similar_stock_names[0]+"(y/n)")
                        if confirm.lower()=='y':
                            input_stock_name = similar_stock_names[0]
                            proper_value_acquired = True
                        else:
                            input_stock_name = input("Which stock you need to process?:-")
        dates.sort(key = lambda date: datetime.strptime(date, "%d-%b-%Y")) 
        is_date_proper = False
        while(not is_date_proper):
            start_date = input("From which date you want to start:- ")
            end_date = input("Till which date you want to analyze:- ")
            try:
                datetime.strptime(start_date,"%d-%b-%Y")
                datetime.strptime(end_date,"%d-%b-%Y")
                is_date_proper =True
            except ValueError as v:
                print("date is not of proper format. The format should be of %d-%b-%Y Ex: 22-Jan-2019")
        # TODO: date check
        inclusiveDates = self.inRangeDateArray(start_date,end_date,dates)
        # print(inclusiveDates)
        mean_value = self.get_mean(inclusiveDates,matching_date_price_dict)
        standard_deviation = self.get_standard_deviation(inclusiveDates,matching_date_price_dict)
        profit_details = self.get_profit_details(inclusiveDates,matching_date_price_dict,mean_value)
        # print(matching_date_price_dict)
        # print(mean_value,standard_deviation,profit_details)

        