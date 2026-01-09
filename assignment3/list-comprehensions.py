#Task 3
import csv
import traceback

try:
    with open("../csv/employees.csv", "r") as f:
        reader = csv.reader(f)
        data = list(reader)

    names = [row[1] + " " + row[2] for row in data[1:]]
    print(names)

    names_contain_e = [name for name in names if "e" in name.lower()]
    print("\n")
    print(names_contain_e)
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