from pathlib import Path
from jgmd.basic_util import get_table
class AnsiEscapes:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    PURPLE = '\033[1m\033[34m'
    PINK = '\033[35m'
    CYAN = '\033[1m\033[96m'
    WHITE = '\033[37m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

# class ColoredText:
#     def color_str(s,color):
#         return f"{color}{s}{AnsiEscapes.ENDC}"

class Logger:
    SECTION_DIVIDER_WIDTH=50

    def __init__(self,file_path=None,should_print_to_screen=False,log_in_color=False):
        self.file_paths=[]
        if file_path is not None:
            self.file_paths = [file_path]
            Path(file_path).parent.mkdir(parents=True, exist_ok=True) #ensure the directory exists

        self.log_in_color = log_in_color
        self.should_print_to_screen = should_print_to_screen

    def add_file_path(self,file_path):
        self.file_paths.append(file_path)
        Path(file_path).parent.mkdir(parents=True, exist_ok=True) #ensure the directory exists
        return self

    def spawn_sub_log(self,file_path): # the spawned sub_log is the "main" log. The spawning log is secondary
        return Logger(
            file_path=file_path,
            should_print_to_screen=False, # silent spawned sub_log that will not print to screen; just writes specific info to a specific file :)
            log_in_color=self.log_in_color
        ).add_file_path(self.file_paths[0])

    def empty_log(self):
        if self.file_paths[0] is None:
            return self
        with open(self.file_paths[0],'wt',encoding='utf-8') as f:
            f.write('')
        return self

    def log_colored(self,color,*strs):
        colored_strs=[]
        for s in strs:
            s = f"{color}{s}{AnsiEscapes.ENDC}"
            colored_strs.append(s)

        if self.should_print_to_screen:
            print(*colored_strs)

        for file_path in self.file_paths:
            if file_path is not None:
                with open(file_path,'at',encoding='utf-8') as f:
                    if self.log_in_color:
                        f.write(' '.join(colored_strs)+'\n')
                    else:
                        f.write(' '.join([str(s) for s in strs])+'\n')

    def success(self,*s):
        self.log_colored(AnsiEscapes.GREEN,*s)

    def error(self,*s):
        self.log_colored(AnsiEscapes.RED,*s)

    def warning(self,*s):
        self.log_colored(AnsiEscapes.YELLOW,*s)

    def info(self,*s):
        self.log_colored(AnsiEscapes.CYAN,*s)

    def primary(self,*s):
        self.log_colored(AnsiEscapes.PURPLE,*s)

    def secondary(self,*s):
        self.log_colored(AnsiEscapes.PINK,*s)

    def bold(self,*s):
        self.log_colored(AnsiEscapes.BOLD,*s)

    def underline(self,*s):
        self.log_colored(AnsiEscapes.UNDERLINE,*s)

    def log(self,*s):
        self.log_colored(AnsiEscapes.WHITE,*s)

    def section_header(self,title,text_color : AnsiEscapes = AnsiEscapes.WHITE, divider_color : AnsiEscapes = AnsiEscapes.WHITE):
        divider = ''.join(['*' for _ in range(0,Logger.SECTION_DIVIDER_WIDTH)])
        double_divider = divider+'\n'+divider
        self.log_colored(divider_color,'\n'+double_divider)
        self.log_colored(text_color,title)
        self.log_colored(divider_color,double_divider)

    def subsection_header(self,title,text_color : AnsiEscapes = AnsiEscapes.WHITE, divider_color : AnsiEscapes = AnsiEscapes.WHITE):
        divider = ''.join(['-' for _ in range(0,Logger.SECTION_DIVIDER_WIDTH)])
        self.log_colored(divider_color,'\n'+divider)
        self.log_colored(text_color,title)
        self.log_colored(divider_color,divider)

    def log_as_table(self,rows,col_headers,num_indents=0,title=None,color : AnsiEscapes =AnsiEscapes.WHITE):
        table_str = get_table(rows,col_headers,num_indents=num_indents,title=title)
        self.log_colored(color, table_str)