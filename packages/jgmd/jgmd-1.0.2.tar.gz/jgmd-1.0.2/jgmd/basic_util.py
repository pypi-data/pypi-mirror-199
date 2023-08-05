from datetime import datetime,timedelta,timezone
from tabulate import tabulate
from traceback import print_exc
from distutils.util import strtobool
from functools import wraps
import traceback

TYPES = {cls.__name__: cls for cls in [str, int, float, bool, dict]}
TYPES['bool']=strtobool #allows us to convert the string input to a bool in a more intuitive way

def exception_to_str(e):
    formatted_lines = traceback.format_exc().splitlines()
    return '\n'.join(formatted_lines)

def add_to_dte(dte,days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
    return dte + timedelta(days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)

def dte_to_str(dte):
    if dte is None:
        return None
    return dte.strftime("%Y-%m-%d")

def now():
    rslt = datetime.utcnow().replace(tzinfo=timezone.utc)
    return rslt

def seconds_between(dte1 : datetime,dte2 : datetime):
    if dte1 is None or dte2 is None:
        return None
    time_diff = dte2-dte1
    return time_diff.total_seconds()

def first(lst,matching_fxn):
    try:
        return next(item for item in lst if matching_fxn(item))
    except StopIteration as e:
        return None

# A decorator that catches exceptions and logs them.
# Requires that the function be an instance method and the instance has a self.logger.error() function
def catches_exceptions(fxn):
    def wrapper(self,*args,**kwargs):
        try:
            fxn(self,*args,**kwargs)
        except Exception as e:
            self.logger.error(f'Exception occurred during {fxn.__qualname__}: {str(e)}')
            print_exc()
    return wrapper

def print_table(rows,col_headers):
    # rows = [col_headers, *rows]
    # print(tabulate(rows, headers='firstrow', tablefmt='fancy_grid'))
    print(get_table(rows,col_headers))

def get_table(rows,col_headers,num_indents=0,title=None):
    rows = [col_headers, *rows]
    table = tabulate(rows, headers='firstrow', tablefmt='fancy_grid')
    if title is not None:
        table = f'{title}\n{table}'
    indents=''
    if num_indents>0:
        indents = '\t'*num_indents
        table = table.replace('\n',f'\n{indents}')
    return indents+table

def get_mapped_val(map,key):
    if key not in map:
        raise ValueError(f'unrecognized key: {key}')
    return map[key]

def params_to_str(*args,**kwargs):
    params = [f'{key} = {val}' for key,val in kwargs.items()]
    return ', '.join([ str(x) for x in [*args,*params]])

def get_log_fxn_from_obj_safe(obj, optional_lambda = None):
    if hasattr(obj,'logger'):
        if optional_lambda is not None:
            return optional_lambda(obj.logger)
        return obj.logger.log
    return print

def logged_method(fxn):
    @wraps(fxn)
    def wrapper(self,*args,**kwargs):
        params_str = params_to_str(*args,**kwargs)
        log_fxn = get_log_fxn_from_obj_safe(self)
        log_fxn(f'{fxn.__qualname__} called with params ({params_str})')
        return fxn(self,*args,**kwargs)
    return wrapper

def checks_test_mode(fxn):
    @wraps(fxn)
    def wrapper(self,*args,**kwargs):
        is_test_mode = getattr(self,'is_test_mode',None)
        if is_test_mode:
            params_str = params_to_str(*args,**kwargs)
            log_fxn = get_log_fxn_from_obj_safe(self, lambda x : x.warning)
            log_fxn(f'{fxn.__qualname__} not executing bc test_mode is enabled. Params were ({params_str})')
            return
        return fxn(self,*args,**kwargs)
    return wrapper

def logged_and_checks_test_mode(fxn):
    @wraps(fxn)
    def wrapper(self,*args,**kwargs):
        params_str = params_to_str(*args,**kwargs)
        is_test_mode = getattr(self,'is_test_mode',None)
        if is_test_mode:
            log_fxn = get_log_fxn_from_obj_safe(self, lambda x : x.warning)
            log_fxn(f'{fxn.__qualname__} not executing bc test_mode is enabled. Params were ({params_str})')
            return
        log_fxn = get_log_fxn_from_obj_safe(self)
        log_fxn(f'{fxn.__qualname__} called with params ({params_str})')
        return fxn(self,*args,**kwargs)
    return wrapper

