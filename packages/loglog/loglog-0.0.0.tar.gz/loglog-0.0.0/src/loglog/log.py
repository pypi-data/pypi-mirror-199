from colored import fg
from colors import *

from datetime import datetime
import re

from loglog.loglog_error import LogLogError

class logger():
    def __init__(self, path : str | None = None):
        self.debug_color = BLUE_COLOR
        self.info_color = AQUAMARINE_COLOR
        self.warn_color = YELLOW_COLOR
        self.error_color = RED_COLOR
        self.fatal_color = PURPLE_COLOR
        self.text_color = WHITE_COLOR
        self.hide_color = GREY_COLOR
        pass

    def __get_time(self):
        return datetime.now().strftime("%H:%M:%S")

    def __is_color_hex_code(self, color_code : str):
        match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color_code)
        return match

    def set_debug_color(self, color_code : str):
        if not self.__is_color_hex_code(color_code): raise LogLogError("`color_code` should be a valid color hexcode e.g `#121212`")
        else: self.debug_color = color_code
    
    def set_info_color(self, color_code : str):
        if not self.__is_color_hex_code(color_code): raise LogLogError("`color_code` should be a valid color hexcode e.g `#121212`")
        else: self.info_color = color_code
    
    def set_warn_color(self, color_code : str):
        if not self.__is_color_hex_code(color_code): raise LogLogError("`color_code` should be a valid color hexcode e.g `#121212`")
        else: self.warn_color = color_code
    
    def set_error_color(self, color_code : str):
        if not self.__is_color_hex_code(color_code): raise LogLogError("`color_code` should be a valid color hexcode e.g `#121212`")
        else: self.error_color = color_code
    
    def set_fatal_color(self, color_code : str):
        if not self.__is_color_hex_code(color_code): raise LogLogError("`color_code` should be a valid color hexcode e.g `#121212`")
        else: self.fatal_color = color_code
    
    def set_hide_color(self, color_code : str):
        if not self.__is_color_hex_code(color_code): raise LogLogError("`color_code` should be a valid color hexcode e.g `#121212`")
        else: self.hide_color = color_code

    def log(self, level, text):
        print(text)

    def log_text(self, title : str, text : str, title_color : str, level : str, key, value):
        key_val_text = f"{str(key)}={str(value)}"
        if str(key) == "" or str(value) == "": key_val_text = ""
        self.log(title, f"{self.__get_time()} {fg(title_color)}{title}{fg(self.text_color)} {str(text)} {fg(self.hide_color)}{key_val_text}{RESET}")

    def debug(self, text : any, key : any = "", value : any = ""):
        self.log_text("DEBUG", text, self.debug_color, "debug", key, value)

    def info(self, text : any, key : any = "", value : any = ""):
        self.log_text("INFO ", text, self.info_color, "info", key, value)

    def warn(self, text : any, key : any = "", value : any = ""):
        self.log_text("WARN ", text, self.warn_color, "warn", key, value)

    def error(self, text : any, key : any = "", value : any = ""):
        self.log_text("ERROR", text, self.error_color, "error", key, value)

    def fatal(self, text : any, key : any = "", value : any = ""):
        self.log_text("FATAL", text, self.fatal_color, "fatal", key, value)