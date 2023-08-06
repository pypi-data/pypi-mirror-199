import datetime

from typing import Optional

def datetime_string(datetime_obj = None) -> str:
    if datetime_obj:
        return datetime_obj.strftime("%m-%d-%y %H:%M:%S")
    else:
        return datetime.datetime.now().strftime("%m-%d-%y %H:%M:%S")


def datetime_object(datetime_string: Optional[str] = None) -> datetime.date:
    if datetime_string:
        return datetime.datetime.strptime(datetime_string, "%m-%d-%y %H:%M:%S")
    else:
        return datetime.datetime.now() 
        
def check_datetime_object(datetime_object: datetime.date) -> bool:
    return datetime.datetime == type(datetime_object)
    
# Returns true if still valid
def check_delta_timestamp(datetime_start: datetime.date, datetime_end: datetime.date) -> bool:
    return datetime_end > datetime_start
    
def add_time(datetime_start: datetime.date, add_secs: int) -> datetime.date:
    return datetime_start + datetime.delta(seconds=add_secs)


if __name__ == "__main__":
    string = datetime_string()
    print(type(string))

    print(datetime.datetime.now())
    print(string)

    print(datetime_object(string))
    print(type(datetime.datetime))
    print(type(datetime_object(string)))
    
    print(datetime.datetime ==  type(datetime_object(string)))
    
    print(datetime_object())
