# %%
import csv
import traceback
import os
import custom_module
from datetime import datetime

#%%
#Task 2
def read_employees():
    data_dict = {}
    rows = []
    
    try:
        with open("../csv/employees.csv", "r") as f:
            reader = csv.reader(f)
            
            for i, row in enumerate(reader):
                if i == 0:
                    data_dict["fields"] = row
                else:
                    rows.append(row)
                    
            data_dict["rows"] = rows
        
            return data_dict
    except Exception as e:
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
        print(f"Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")
        
employees = read_employees()
print(employees)

#%%
#Task 3
def column_index(feild):
    return employees["fields"].index(feild)

employee_id_column = column_index("employee_id")

#%%
#Task 4
def first_name(row_number):
    index = column_index("first_name")
    employee = employees["rows"][row_number]
    
    return employee[index]

#%%
#Task 5
def employee_find(employee_id):
    def employee_match(row):
        return int(row[employee_id_column]) == employee_id
    
    return list(filter(employee_match, employees["rows"]))

#%%
#Task 6
def employee_find_2(employee_id):
   matches = list(filter(lambda row : int(row[employee_id_column]) == employee_id , employees["rows"]))
   return matches   

#%%
#Task 7
def  sort_by_last_name():
    employees["rows"].sort(key=lambda row: row[column_index("last_name")])
    return employees["rows"]

#%%
#Task 8
def employee_dict(row):
    dict_keys = employees["fields"][:]
    dict_keys.remove("employee_id")
    row.pop(employee_id_column)
    
    return dict(zip(dict_keys, row))

#%%
#Task 9
def all_employees_dict():
    employees_dict = {}
    
    for employee in employees["rows"]:
       employees_dict[employee[employee_id_column]] = employee_dict(employee[:])
    
    return employees_dict
# %%
#Task 10
def get_this_value():
    return os.getenv("THISVALUE")
# %%
#Task 11
def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)

# %%
#Task 12
def minutes_to_dict(file):
    data_dict = {}
    rows = []
    
    try:
        with open(file, "r") as f:
            reader = csv.reader(f)
            
            for i, row in enumerate(reader):
                if i == 0:
                    data_dict["fields"] = row
                else:
                    rows.append(tuple(row))
                    
            data_dict["rows"] = rows
        
            return data_dict
    except Exception as e:
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
        print(f"Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")

def read_minutes():
    minutes1 = minutes_to_dict("../csv/minutes1.csv")
    minutes2 = minutes_to_dict("../csv/minutes2.csv")

    return minutes1, minutes2

minutes1, minutes2 = read_minutes()
# %%
#Task 13
def create_minutes_set():
    set1 = set(minutes1["rows"])
    set2 = set(minutes2["rows"])
    
    return set1.union(set2)
    
minutes_set = create_minutes_set()

# %%
#Task 14
def create_minutes_list():
    min_list = list(minutes_set)
    return list(map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), min_list ))
     
minutes_list = create_minutes_list()

# %%
#Task 14
def write_sorted_list():
    minutes_list.sort(key=lambda element: element[1])
    new_minutes_list = list(map(lambda x: (x[0], datetime.strftime(x[1], "%B %d, %Y")), minutes_list ))
    
    try:
        with open("./minutes.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(minutes1["fields"])
            writer.writerows(minutes_list)
    except Exception as e:
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
        print(f"Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")
    finally:
        return new_minutes_list
# %%
