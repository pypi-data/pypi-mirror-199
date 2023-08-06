from typing import List, Optional, Dict, Iterable
import aspose.pycore
import aspose.pydrawing
import aspose.cells
import aspose.cells.charts
import aspose.cells.digitalsignatures
import aspose.cells.drawing
import aspose.cells.drawing.activexcontrols
import aspose.cells.drawing.equations
import aspose.cells.drawing.texts
import aspose.cells.externalconnections
import aspose.cells.json
import aspose.cells.markup
import aspose.cells.metadata
import aspose.cells.numbers
import aspose.cells.ods
import aspose.cells.pivot
import aspose.cells.properties
import aspose.cells.querytables
import aspose.cells.rendering
import aspose.cells.rendering.pdfsecurity
import aspose.cells.revisions
import aspose.cells.saving
import aspose.cells.settings
import aspose.cells.slicers
import aspose.cells.tables
import aspose.cells.timelines
import aspose.cells.utility
import aspose.cells.vba
import aspose.cells.webextensions

class AboveAverage:
    '''Describe the AboveAverage conditional formatting rule.
    This conditional formatting rule highlights cells that
    are above or below the average for all values in the range.'''
    
    @property
    def is_above_average(self) -> bool:
        ...
    
    @is_above_average.setter
    def is_above_average(self, value : bool):
        ...
    
    @property
    def is_equal_average(self) -> bool:
        ...
    
    @is_equal_average.setter
    def is_equal_average(self, value : bool):
        ...
    
    @property
    def std_dev(self) -> int:
        ...
    
    @std_dev.setter
    def std_dev(self, value : int):
        ...
    
    ...

class AbstractCalculationEngine:
    '''Represents user's custom calculation engine to extend the default calculation engine of Aspose.Cells.'''
    
    def calculate(self, data : aspose.cells.CalculationData):
        '''Calculates one function with given data.
        
        :param data: the required data to calculate function such as function name, parameters, ...etc.'''
        ...
    
    @property
    def is_param_literal_required(self) -> bool:
        ...
    
    @property
    def process_built_in_functions(self) -> bool:
        ...
    
    ...

class AbstractCalculationMonitor:
    '''Monitor for user to track the progress of formula calculation.'''
    
    def before_calculate(self, sheet_index : int, row_index : int, col_index : int):
        '''Implement this method to do business before calculating one cell.
        
        :param sheet_index: Index of the sheet that the cell belongs to.
        :param row_index: Row index of the cell
        :param col_index: Column index of the cell'''
        ...
    
    def after_calculate(self, sheet_index : int, row_index : int, col_index : int):
        '''Implement this method to do business after one cell has been calculated.
        
        :param sheet_index: Index of the sheet that the cell belongs to.
        :param row_index: Row index of the cell
        :param col_index: Column index of the cell'''
        ...
    
    def on_circular(self, circular_cells_data : collections.abc.Iterator) -> bool:
        '''Implement this method to do business when calculating formulas with circular references.
        
        :param circular_cells_data: IEnumerator with CalculationCell items representing cells that
        depend on circular references.
        :returns: Whether the formula engine needs to calculate those cells in circular after this call.
        True to let the formula engine continue to do calculation for them.
        False to let the formula engine just mark those cells as Calculated.'''
        ...
    
    @property
    def original_value(self) -> any:
        ...
    
    @property
    def value_changed(self) -> bool:
        ...
    
    @property
    def calculated_value(self) -> any:
        ...
    
    ...

class AbstractGlobalizationSettings:
    '''Represents the globalization settings.'''
    
    def compare(self, v1 : str, v2 : str, ignore_case : bool) -> int:
        '''Compares two string values according to certain collation rules.
        
        :param v1: the first string
        :param v2: the second string
        :param ignore_case: whether ignore case when comparing values
        :returns: Integer that indicates the lexical relationship between the two comparands'''
        ...
    
    ...

class AbstractInterruptMonitor:
    '''Monitor for interruption requests in all time-consuming operations.'''
    
    @property
    def is_interruption_requested(self) -> bool:
        ...
    
    @property
    def terminate_without_exception(self) -> bool:
        ...
    
    ...

class AbstractTextLoadOptions(LoadOptions):
    '''Common options for loading text values'''
    
    def set_paper_size(self, type : aspose.cells.PaperSizeType):
        '''Sets the default print paper size from default printer's setting.
        
        :param type: The default paper size.'''
        ...
    
    @property
    def load_format(self) -> aspose.cells.LoadFormat:
        ...
    
    @property
    def password(self) -> str:
        '''Gets and set the password of the workbook.'''
        ...
    
    @password.setter
    def password(self, value : str):
        '''Gets and set the password of the workbook.'''
        ...
    
    @property
    def parsing_formula_on_open(self) -> bool:
        ...
    
    @parsing_formula_on_open.setter
    def parsing_formula_on_open(self, value : bool):
        ...
    
    @property
    def parsing_pivot_cached_records(self) -> bool:
        ...
    
    @parsing_pivot_cached_records.setter
    def parsing_pivot_cached_records(self, value : bool):
        ...
    
    @property
    def language_code(self) -> aspose.cells.CountryCode:
        ...
    
    @language_code.setter
    def language_code(self, value : aspose.cells.CountryCode):
        ...
    
    @property
    def region(self) -> aspose.cells.CountryCode:
        '''Gets the system regional settings based on CountryCode at the time the file was loaded.'''
        ...
    
    @region.setter
    def region(self, value : aspose.cells.CountryCode):
        '''Sets the system regional settings based on CountryCode at the time the file was loaded.'''
        ...
    
    @property
    def default_style_settings(self) -> aspose.cells.DefaultStyleSettings:
        ...
    
    @property
    def standard_font(self) -> str:
        ...
    
    @standard_font.setter
    def standard_font(self, value : str):
        ...
    
    @property
    def standard_font_size(self) -> float:
        ...
    
    @standard_font_size.setter
    def standard_font_size(self, value : float):
        ...
    
    @property
    def interrupt_monitor(self) -> aspose.cells.AbstractInterruptMonitor:
        ...
    
    @interrupt_monitor.setter
    def interrupt_monitor(self, value : aspose.cells.AbstractInterruptMonitor):
        ...
    
    @property
    def ignore_not_printed(self) -> bool:
        ...
    
    @ignore_not_printed.setter
    def ignore_not_printed(self, value : bool):
        ...
    
    @property
    def check_data_valid(self) -> bool:
        ...
    
    @check_data_valid.setter
    def check_data_valid(self, value : bool):
        ...
    
    @property
    def check_excel_restriction(self) -> bool:
        ...
    
    @check_excel_restriction.setter
    def check_excel_restriction(self, value : bool):
        ...
    
    @property
    def keep_unparsed_data(self) -> bool:
        ...
    
    @keep_unparsed_data.setter
    def keep_unparsed_data(self, value : bool):
        ...
    
    @property
    def load_filter(self) -> aspose.cells.LoadFilter:
        ...
    
    @load_filter.setter
    def load_filter(self, value : aspose.cells.LoadFilter):
        ...
    
    @property
    def light_cells_data_handler(self) -> aspose.cells.LightCellsDataHandler:
        ...
    
    @light_cells_data_handler.setter
    def light_cells_data_handler(self, value : aspose.cells.LightCellsDataHandler):
        ...
    
    @property
    def memory_setting(self) -> aspose.cells.MemorySetting:
        ...
    
    @memory_setting.setter
    def memory_setting(self, value : aspose.cells.MemorySetting):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def auto_fitter_options(self) -> aspose.cells.AutoFitterOptions:
        ...
    
    @auto_fitter_options.setter
    def auto_fitter_options(self, value : aspose.cells.AutoFitterOptions):
        ...
    
    @property
    def auto_filter(self) -> bool:
        ...
    
    @auto_filter.setter
    def auto_filter(self, value : bool):
        ...
    
    @property
    def font_configs(self) -> aspose.cells.IndividualFontConfigs:
        ...
    
    @font_configs.setter
    def font_configs(self, value : aspose.cells.IndividualFontConfigs):
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets and sets the default encoding. Only applies for csv file.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Gets and sets the default encoding. Only applies for csv file.'''
        ...
    
    @property
    def load_style_strategy(self) -> aspose.cells.TxtLoadStyleStrategy:
        ...
    
    @load_style_strategy.setter
    def load_style_strategy(self, value : aspose.cells.TxtLoadStyleStrategy):
        ...
    
    @property
    def convert_numeric_data(self) -> bool:
        ...
    
    @convert_numeric_data.setter
    def convert_numeric_data(self, value : bool):
        ...
    
    @property
    def convert_date_time_data(self) -> bool:
        ...
    
    @convert_date_time_data.setter
    def convert_date_time_data(self, value : bool):
        ...
    
    @property
    def keep_precision(self) -> bool:
        ...
    
    @keep_precision.setter
    def keep_precision(self, value : bool):
        ...
    
    ...

class AutoFilter:
    '''Represents autofiltering for the specified worksheet.'''
    
    @overload
    def remove_filter(self, field_index : int, criteria : str):
        '''Removes a filter for a filter column.
        
        :param field_index: The integer offset of the field on which you want to base the filter
        (from the left of the list; the leftmost field is field 0).
        :param criteria: The specified criteria (a string; for example, "101").
        It only can be null or be one of the cells' value in this column.'''
        ...
    
    @overload
    def remove_filter(self, field_index : int):
        '''Remove the specific filter.
        
        :param field_index: The specific filter index'''
        ...
    
    @overload
    def custom(self, field_index : int, operator_type1 : aspose.cells.FilterOperatorType, criteria1 : any):
        '''Filters a list with a custom criteria.
        
        :param field_index: The integer offset of the field on which you want to base the filter
        (from the left of the list; the leftmost field is field 0).
        :param operator_type1: The filter operator type
        :param criteria1: The custom criteria'''
        ...
    
    @overload
    def custom(self, field_index : int, operator_type1 : aspose.cells.FilterOperatorType, criteria1 : any, is_and : bool, operator_type2 : aspose.cells.FilterOperatorType, criteria2 : any):
        '''Filters a list with custom criteria.
        
        :param field_index: The integer offset of the field on which you want to base the filter
        (from the left of the list; the leftmost field is field 0).
        :param operator_type1: The filter operator type
        :param criteria1: The custom criteria
        :param operator_type2: The filter operator type
        :param criteria2: The custom criteria'''
        ...
    
    @overload
    def refresh(self) -> List[int]:
        '''Refresh auto filters to hide or unhide the rows.
        
        :returns: Returns all hidden rows' indexes.'''
        ...
    
    @overload
    def refresh(self, hide_rows : bool) -> List[int]:
        '''Gets all hidden rows' indexes.
        
        :param hide_rows: If true, hide the filtered rows.
        :returns: Returns all hidden rows indexes.'''
        ...
    
    def set_range(self, row : int, start_column : int, end_column : int):
        '''Sets the range to which the specified AutoFilter applies.
        
        :param row: Row index.
        :param start_column: Start column index.
        :param end_column: End column Index.'''
        ...
    
    def get_cell_area(self) -> aspose.cells.CellArea:
        '''Gets the :py:class:`aspose.cells.CellArea` where the specified AutoFilter applies to.'''
        ...
    
    def add_filter(self, field_index : int, criteria : str):
        '''Adds a filter for a filter column.
        
        :param field_index: The integer offset of the field on which you want to base the filter
        (from the left of the list; the leftmost field is field 0).
        :param criteria: The specified criteria (a string; for example, "101").
        It only can be null or be one of the cells' value in this column.'''
        ...
    
    def add_date_filter(self, field_index : int, date_time_grouping_type : aspose.cells.DateTimeGroupingType, year : int, month : int, day : int, hour : int, minute : int, second : int):
        '''Adds a date filter.
        
        :param field_index: The integer offset of the field on which you want to base the filter
        (from the left of the list; the leftmost field is field 0).
        :param date_time_grouping_type: :py:class:`aspose.cells.DateTimeGroupingType`
        :param year: The year.
        :param month: The month.
        :param day: The day.
        :param hour: The hour.
        :param minute: The minute.
        :param second: The second.'''
        ...
    
    def remove_date_filter(self, field_index : int, date_time_grouping_type : aspose.cells.DateTimeGroupingType, year : int, month : int, day : int, hour : int, minute : int, second : int):
        '''Removes a date filter.
        
        :param field_index: The integer offset of the field on which you want to base the filter
        (from the left of the list; the leftmost field is field 0).
        :param date_time_grouping_type: :py:class:`aspose.cells.DateTimeGroupingType`
        :param year: The year.
        :param month: The month.
        :param day: The day.
        :param hour: The hour.
        :param minute: The minute.
        :param second: The second.'''
        ...
    
    def filter(self, field_index : int, criteria : str):
        '''Filters a list with specified criteria.
        
        :param field_index: The integer offset of the field on which you want to base the filter
        (from the left of the list; the leftmost field is field 0).
        :param criteria: The specified criteria (a string; for example, "101").'''
        ...
    
    def filter_top10(self, field_index : int, is_top : bool, is_percent : bool, item_count : int):
        '''Filter the top 10 item in the list
        
        :param field_index: The integer offset of the field on which you want to base the filter
        (from the left of the list; the leftmost field is field 0).
        :param is_top: Indicates whether filter from top or bottom
        :param is_percent: Indicates whether the items is percent or count
        :param item_count: The item count'''
        ...
    
    def dynamic_filter(self, field_index : int, dynamic_filter_type : aspose.cells.DynamicFilterType):
        '''Adds a dynamic filter.
        
        :param field_index: The integer offset of the field on which you want to base the filter
        (from the left of the list; the leftmost field is field 0).
        :param dynamic_filter_type: Dynamic filter type.'''
        ...
    
    def add_font_color_filter(self, field_index : int, color : aspose.cells.CellsColor):
        '''Adds a font color filter.
        
        :param field_index: The integer offset of the field on which you want to base the filter
        (from the left of the list; the leftmost field is field 0).
        :param color: The :py:class:`aspose.cells.CellsColor` object.'''
        ...
    
    def add_fill_color_filter(self, field_index : int, pattern : aspose.cells.BackgroundType, foreground_color : aspose.cells.CellsColor, background_color : aspose.cells.CellsColor):
        '''Adds a fill color filter.
        
        :param field_index: The integer offset of the field on which you want to base the filter
        (from the left of the list; the leftmost field is field 0).
        :param pattern: The background pattern type.
        :param foreground_color: The foreground color.
        :param background_color: The background color.'''
        ...
    
    def add_icon_filter(self, field_index : int, icon_set_type : aspose.cells.IconSetType, icon_id : int):
        '''Adds an icon filter.
        
        :param field_index: The integer offset of the field on which you want to base the filter
        (from the left of the list; the leftmost field is field 0).
        :param icon_set_type: The icon set type.
        :param icon_id: The icon id.'''
        ...
    
    def match_blanks(self, field_index : int):
        '''Match all blank cell in the list.
        
        :param field_index: The integer offset of the field on which you want to base the filter
        (from the left of the list; the leftmost field is field 0).'''
        ...
    
    def match_non_blanks(self, field_index : int):
        '''Match all not blank cell in the list.
        
        :param field_index: The integer offset of the field on which you want to base the filter
        (from the left of the list; the leftmost field is field 0).'''
        ...
    
    def show_all(self):
        '''Unhide all rows.'''
        ...
    
    @property
    def sorter(self) -> aspose.cells.DataSorter:
        '''Gets the data sorter.'''
        ...
    
    @property
    def range(self) -> str:
        '''Represents the range to which the specified AutoFilter applies.'''
        ...
    
    @range.setter
    def range(self, value : str):
        '''Represents the range to which the specified AutoFilter applies.'''
        ...
    
    @property
    def show_filter_button(self) -> bool:
        ...
    
    @show_filter_button.setter
    def show_filter_button(self, value : bool):
        ...
    
    @property
    def filter_columns(self) -> aspose.cells.FilterColumnCollection:
        ...
    
    ...

class AutoFitterOptions:
    '''Represents all auto fitter options.'''
    
    @property
    def default_edit_language(self) -> aspose.cells.DefaultEditLanguage:
        ...
    
    @default_edit_language.setter
    def default_edit_language(self, value : aspose.cells.DefaultEditLanguage):
        ...
    
    @property
    def auto_fit_merged_cells(self) -> bool:
        ...
    
    @auto_fit_merged_cells.setter
    def auto_fit_merged_cells(self, value : bool):
        ...
    
    @property
    def auto_fit_merged_cells_type(self) -> aspose.cells.AutoFitMergedCellsType:
        ...
    
    @auto_fit_merged_cells_type.setter
    def auto_fit_merged_cells_type(self, value : aspose.cells.AutoFitMergedCellsType):
        ...
    
    @property
    def only_auto(self) -> bool:
        ...
    
    @only_auto.setter
    def only_auto(self, value : bool):
        ...
    
    @property
    def ignore_hidden(self) -> bool:
        ...
    
    @ignore_hidden.setter
    def ignore_hidden(self, value : bool):
        ...
    
    @property
    def max_row_height(self) -> float:
        ...
    
    @max_row_height.setter
    def max_row_height(self, value : float):
        ...
    
    @property
    def auto_fit_wrapped_text_type(self) -> aspose.cells.AutoFitWrappedTextType:
        ...
    
    @auto_fit_wrapped_text_type.setter
    def auto_fit_wrapped_text_type(self, value : aspose.cells.AutoFitWrappedTextType):
        ...
    
    @property
    def format_strategy(self) -> aspose.cells.CellValueFormatStrategy:
        ...
    
    @format_strategy.setter
    def format_strategy(self, value : aspose.cells.CellValueFormatStrategy):
        ...
    
    ...

class Border:
    '''Encapsulates the object that represents the cell border.'''
    
    @property
    def theme_color(self) -> aspose.cells.ThemeColor:
        ...
    
    @theme_color.setter
    def theme_color(self, value : aspose.cells.ThemeColor):
        ...
    
    @property
    def color(self) -> aspose.pydrawing.Color:
        '''Gets the :py:class:`aspose.pydrawing.Color` of the border.'''
        ...
    
    @color.setter
    def color(self, value : aspose.pydrawing.Color):
        '''Sets the :py:class:`aspose.pydrawing.Color` of the border.'''
        ...
    
    @property
    def argb_color(self) -> int:
        ...
    
    @argb_color.setter
    def argb_color(self, value : int):
        ...
    
    @property
    def line_style(self) -> aspose.cells.CellBorderType:
        ...
    
    @line_style.setter
    def line_style(self, value : aspose.cells.CellBorderType):
        ...
    
    ...

class BorderCollection:
    '''Encapsulates a collection of :py:class:`aspose.cells.Border` objects.'''
    
    def set_color(self, color : aspose.pydrawing.Color):
        '''Sets the :py:class:`aspose.pydrawing.Color` of all borders in the collection.
        
        :param color: Borders' :py:class:`aspose.pydrawing.Color`.'''
        ...
    
    def set_style(self, style : aspose.cells.CellBorderType):
        '''Sets the style of all borders of the collection.
        
        :param style: Borders' style'''
        ...
    
    @property
    def diagonal_color(self) -> aspose.pydrawing.Color:
        ...
    
    @diagonal_color.setter
    def diagonal_color(self, value : aspose.pydrawing.Color):
        ...
    
    @property
    def diagonal_style(self) -> aspose.cells.CellBorderType:
        ...
    
    @diagonal_style.setter
    def diagonal_style(self, value : aspose.cells.CellBorderType):
        ...
    
    ...

class CalculationCell:
    '''Represents the calculation relevant data about one cell which is being calculated.'''
    
    def set_calculated_value(self, v : any):
        '''Sets the calculated value for the cell.'''
        ...
    
    @property
    def workbook(self) -> aspose.cells.Workbook:
        '''Gets the Workbook object.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the Worksheet object where the cell is in.'''
        ...
    
    @property
    def cell_row(self) -> int:
        ...
    
    @property
    def cell_column(self) -> int:
        ...
    
    @property
    def cell(self) -> aspose.cells.Cell:
        '''Gets the Cell object which is being calculated.'''
        ...
    
    ...

class CalculationData:
    '''Represents the required data when calculating one function, such as function name, parameters, ...etc.'''
    
    def get_param_value(self, index : int) -> any:
        '''Gets the represented value object of the parameter at given index.
        
        :param index: index of the parameter(0 based)
        :returns: If the parameter is plain value, then returns the plain value.
        If the parameter is reference, then returns ReferredArea object.
        If the parameter references to multiple datasets, then returns array of objects.'''
        ...
    
    def get_param_text(self, index : int) -> str:
        '''Gets the literal text of the parameter at given index.
        
        :param index: index of the parameter(0 based)
        :returns: literal text of the parameter'''
        ...
    
    @property
    def calculated_value(self) -> any:
        ...
    
    @calculated_value.setter
    def calculated_value(self, value : any):
        ...
    
    @property
    def workbook(self) -> aspose.cells.Workbook:
        '''Gets the Workbook object where the function is in.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the Worksheet object where the function is in.'''
        ...
    
    @property
    def cell_row(self) -> int:
        ...
    
    @property
    def cell_column(self) -> int:
        ...
    
    @property
    def cell(self) -> aspose.cells.Cell:
        '''Gets the Cell object where the function is in.'''
        ...
    
    @property
    def function_name(self) -> str:
        ...
    
    @property
    def param_count(self) -> int:
        ...
    
    ...

class CalculationOptions:
    '''Represents options for calculation.'''
    
    @property
    def ignore_error(self) -> bool:
        ...
    
    @ignore_error.setter
    def ignore_error(self, value : bool):
        ...
    
    @property
    def recursive(self) -> bool:
        '''Indicates whether calculate the dependent cells recursively when calculating one cell and it depends on other cells.
        The default value if true.'''
        ...
    
    @recursive.setter
    def recursive(self, value : bool):
        '''Indicates whether calculate the dependent cells recursively when calculating one cell and it depends on other cells.
        The default value if true.'''
        ...
    
    @property
    def custom_function(self) -> aspose.cells.ICustomFunction:
        ...
    
    @custom_function.setter
    def custom_function(self, value : aspose.cells.ICustomFunction):
        ...
    
    @property
    def custom_engine(self) -> aspose.cells.AbstractCalculationEngine:
        ...
    
    @custom_engine.setter
    def custom_engine(self, value : aspose.cells.AbstractCalculationEngine):
        ...
    
    @property
    def calculation_monitor(self) -> aspose.cells.AbstractCalculationMonitor:
        ...
    
    @calculation_monitor.setter
    def calculation_monitor(self, value : aspose.cells.AbstractCalculationMonitor):
        ...
    
    @property
    def calc_stack_size(self) -> int:
        ...
    
    @calc_stack_size.setter
    def calc_stack_size(self, value : int):
        ...
    
    @property
    def precision_strategy(self) -> aspose.cells.CalculationPrecisionStrategy:
        ...
    
    @precision_strategy.setter
    def precision_strategy(self, value : aspose.cells.CalculationPrecisionStrategy):
        ...
    
    @property
    def linked_data_sources(self) -> List[aspose.cells.Workbook]:
        ...
    
    @linked_data_sources.setter
    def linked_data_sources(self, value : List[aspose.cells.Workbook]):
        ...
    
    ...

class Cell:
    '''Encapsulates the object that represents a single Workbook cell.'''
    
    @overload
    def calculate(self, options : aspose.cells.CalculationOptions):
        '''Calculates the formula of the cell.
        
        :param options: Options for calculation'''
        ...
    
    @overload
    def calculate(self, ignore_error : bool, custom_function : aspose.cells.ICustomFunction):
        '''Calculates the formula of the cell.
        
        :param ignore_error: Indicates if hide the error in calculating formulas.
        The error may be unsupported function, external links, etc.
        :param custom_function: The custom formula calculation functions to extend the calculation engine.'''
        ...
    
    @overload
    def put_value(self, bool_value : bool):
        '''Puts a boolean value into the cell.'''
        ...
    
    @overload
    def put_value(self, int_value : int):
        '''Puts an integer value into the cell.
        
        :param int_value: Input value'''
        ...
    
    @overload
    def put_value(self, double_value : float):
        '''Puts a double value into the cell.
        
        :param double_value: Input value'''
        ...
    
    @overload
    def put_value(self, string_value : str, is_converted : bool, set_style : bool):
        '''Puts a value into the cell, if appropriate the value will be converted to other data type and cell's number format will be reset.
        
        :param string_value: Input value
        :param is_converted: True: converted to other data type if appropriate.
        :param set_style: True: set the number format to cell's style when converting to other data type'''
        ...
    
    @overload
    def put_value(self, string_value : str, is_converted : bool):
        '''Puts a string value into the cell and converts the value to other data type if appropriate.
        
        :param string_value: Input value
        :param is_converted: True: converted to other data type if appropriate.'''
        ...
    
    @overload
    def put_value(self, string_value : str):
        '''Puts a string value into the cell.
        
        :param string_value: Input value'''
        ...
    
    @overload
    def put_value(self, date_time : DateTime):
        '''Puts a DateTime value into the cell.
        
        :param date_time: Input value'''
        ...
    
    @overload
    def put_value(self, object_value : any):
        '''Puts an object value into the cell.
        
        :param object_value: input value'''
        ...
    
    @overload
    def get_display_style(self) -> aspose.cells.Style:
        '''Gets the display style of the cell.
        If this cell is also affected by other settings such as conditional formatting, list objects, etc.,
        then the display style may be different from cell.GetStyle().'''
        ...
    
    @overload
    def get_display_style(self, include_merged_borders : bool) -> aspose.cells.Style:
        '''Gets the display style of the cell.
        If the cell is conditional formatted, the display style is not same as the cell.GetStyle().
        
        :param include_merged_borders: Indicates whether checking borders of the merged cells.'''
        ...
    
    @overload
    def get_style(self) -> aspose.cells.Style:
        '''Gets the cell style.
        
        :returns: Style object.'''
        ...
    
    @overload
    def get_style(self, check_borders : bool) -> aspose.cells.Style:
        '''If checkBorders is true, check whether other cells' borders will effect the style of this cell.
        
        :param check_borders: Check other cells' borders
        :returns: Style object.'''
        ...
    
    @overload
    def set_style(self, style : aspose.cells.Style):
        '''Sets the cell style.
        
        :param style: The cell style.'''
        ...
    
    @overload
    def set_style(self, style : aspose.cells.Style, explicit_flag : bool):
        '''Apply the cell style.
        
        :param style: The cell style.
        :param explicit_flag: True, only overwriting formatting which is explicitly set.'''
        ...
    
    @overload
    def set_style(self, style : aspose.cells.Style, flag : aspose.cells.StyleFlag):
        '''Apply the cell style.
        
        :param style: The cell style.
        :param flag: The style flag.'''
        ...
    
    @overload
    def set_formula(self, formula : str, value : any):
        '''Set the formula and the value of the formula.
        
        :param formula: The formula.
        :param value: The value of the formula.'''
        ...
    
    @overload
    def set_formula(self, formula : str, is_r1c1 : bool, is_local : bool, value : any):
        '''Set the formula and the value of the formula.
        
        :param formula: The formula.
        :param is_r1c1: Whether the formula is R1C1 formula.
        :param is_local: Whether the formula is locale formatted.
        :param value: The value of the formula.'''
        ...
    
    @overload
    def set_formula(self, formula : str, options : aspose.cells.FormulaParseOptions, value : any):
        '''Set the formula and the value of the formula.
        
        :param formula: The formula.
        :param options: Options for parsing the formula.
        :param value: The value of the formula.'''
        ...
    
    @overload
    def set_array_formula(self, array_formula : str, row_number : int, column_number : int, is_r1c1 : bool, is_local : bool):
        '''Sets an array formula to a range of cells.
        
        :param array_formula: Array formula.
        :param row_number: Number of rows to populate result of the array formula.
        :param column_number: Number of columns to populate result of the array formula.
        :param is_r1c1: whether the formula is R1C1 formula
        :param is_local: whether the formula is locale formatted'''
        ...
    
    @overload
    def set_array_formula(self, array_formula : str, row_number : int, column_number : int):
        '''Sets an array formula(legacy array formula entered via CTRL+SHIFT+ENTER in ms excel) to a range of cells.
        
        :param array_formula: Array formula.
        :param row_number: Number of rows to populate result of the array formula.
        :param column_number: Number of columns to populate result of the array formula.'''
        ...
    
    @overload
    def set_array_formula(self, array_formula : str, row_number : int, column_number : int, options : aspose.cells.FormulaParseOptions):
        '''Sets an array formula to a range of cells.
        
        :param array_formula: Array formula.
        :param row_number: Number of rows to populate result of the array formula.
        :param column_number: Number of columns to populate result of the array formula.
        :param options: Options for parsing the formula.'''
        ...
    
    @overload
    def set_array_formula(self, array_formula : str, row_number : int, column_number : int, options : aspose.cells.FormulaParseOptions, values : List[List[any]]):
        '''Sets an array formula to a range of cells.
        
        :param array_formula: Array formula.
        :param row_number: Number of rows to populate result of the array formula.
        :param column_number: Number of columns to populate result of the array formula.
        :param options: Options for parsing the formula.
        :param values: values for those cells with given array formula'''
        ...
    
    @overload
    def set_shared_formula(self, shared_formula : str, row_number : int, column_number : int, is_r1c1 : bool, is_local : bool):
        '''Sets a formula to a range of cells.
        
        :param shared_formula: Shared formula.
        :param row_number: Number of rows to populate the formula.
        :param column_number: Number of columns to populate the formula.
        :param is_r1c1: whether the formula is R1C1 formula
        :param is_local: whether the formula is locale formatted'''
        ...
    
    @overload
    def set_shared_formula(self, shared_formula : str, row_number : int, column_number : int):
        '''Sets shared formulas to a range of cells.
        
        :param shared_formula: Shared formula.
        :param row_number: Number of rows to populate the formula.
        :param column_number: Number of columns to populate the formula.'''
        ...
    
    @overload
    def set_shared_formula(self, shared_formula : str, row_number : int, column_number : int, options : aspose.cells.FormulaParseOptions):
        '''Sets shared formulas to a range of cells.
        
        :param shared_formula: Shared formula.
        :param row_number: Number of rows to populate the formula.
        :param column_number: Number of columns to populate the formula.
        :param options: Options for parsing the formula.'''
        ...
    
    @overload
    def set_shared_formula(self, shared_formula : str, row_number : int, column_number : int, options : aspose.cells.FormulaParseOptions, values : List[List[any]]):
        '''Sets shared formulas to a range of cells.
        
        :param shared_formula: Shared formula.
        :param row_number: Number of rows to populate the formula.
        :param column_number: Number of columns to populate the formula.
        :param options: Options for parsing the formula.
        :param values: values for those cells with given shared formula'''
        ...
    
    @overload
    def get_leafs(self) -> collections.abc.Iterator:
        '''Get all cells which reference to this cell directly and need to be updated when this cell is modified.
        
        :returns: Enumerator to enumerate all dependents(Cell)'''
        ...
    
    @overload
    def get_leafs(self, recursive : bool) -> collections.abc.Iterator:
        '''Get all cells which will be updated when this cell is modified.
        
        :param recursive: Whether returns those leafs that do not reference to this cell directly
        but reference to other leafs of this cell
        :returns: Enumerator to enumerate all dependents(Cell)'''
        ...
    
    @overload
    def set_dynamic_array_formula(self, array_formula : str, options : aspose.cells.FormulaParseOptions, calculate_value : bool) -> aspose.cells.CellArea:
        '''Sets dynamic array formula and make the formula spill into neighboring cells if possible.
        
        :param array_formula: the formula expression
        :param options: options to parse formula.
        "Parse" option will be ignored and the formula will always be parsed immediately
        :param calculate_value: whether calculate this dynamic array formula for those cells in the spilled range.
        :returns: the range that the formula should spill into.'''
        ...
    
    @overload
    def set_dynamic_array_formula(self, array_formula : str, options : aspose.cells.FormulaParseOptions, values : List[List[any]], calculate_range : bool, calculate_value : bool) -> aspose.cells.CellArea:
        '''Sets dynamic array formula and make the formula spill into neighboring cells if possible.
        
        :param array_formula: the formula expression
        :param options: options to parse formula.
        "Parse" option will be ignored and the formula will always be parsed immediately
        :param values: values for those cells with given dynamic array formula
        :param calculate_range: Whether calculate the spilled range for this dynamic array formula.
        If the "values" parameter is not null and this flag is false,
        then the spilled range's height will be values.Length and width will be values[0].Length.
        :param calculate_value: whether calculate this dynamic array formula for those cells in the spilled range when "values" is null
        or corresponding item in "values" for one cell is null.
        :returns: the range that the formula should spill into.'''
        ...
    
    @overload
    def set_dynamic_array_formula(self, array_formula : str, options : aspose.cells.FormulaParseOptions, values : List[List[any]], calculate_range : bool, calculate_value : bool, copts : aspose.cells.CalculationOptions) -> aspose.cells.CellArea:
        '''Sets dynamic array formula and make the formula spill into neighboring cells if possible.
        
        :param array_formula: the formula expression
        :param options: options to parse formula.
        "Parse" option will be ignored and the formula will always be parsed immediately
        :param values: values for those cells with given dynamic array formula
        :param calculate_range: Whether calculate the spilled range for this dynamic array formula.
        If the "values" parameter is not null and this flag is false,
        then the spilled range's height will be values.Length and width will be values[0].Length.
        :param calculate_value: whether calculate this dynamic array formula for those cells in the spilled range when "values" is null
        or corresponding item in "values" for one cell is null.
        :param copts: The options for calculating formula.
        Commonly, for performance consideration, the :py:attr:`aspose.cells.CalculationOptions.recursive` property should be false.
        :returns: the range that the formula should spill into.'''
        ...
    
    @overload
    def set_table_formula(self, row_number : int, column_number : int, row_input_cell : str, column_input_cell : str, values : List[List[any]]):
        '''Create two-variable data table for given range starting from this cell.
        
        :param row_number: Number of rows to populate the formula.
        :param column_number: Number of columns to populate the formula.
        :param row_input_cell: the row input cell
        :param column_input_cell: the column input cell
        :param values: values for cells in table formula range'''
        ...
    
    @overload
    def set_table_formula(self, row_number : int, column_number : int, input_cell : str, is_row_input : bool, values : List[List[any]]):
        '''Create one-variable data table for given range starting from this cell.
        
        :param row_number: Number of rows to populate the formula.
        :param column_number: Number of columns to populate the formula.
        :param input_cell: the input cell
        :param is_row_input: Indicates whether the input cell is a row input cell(true) or a column input cell(false).
        :param values: values for cells in table formula range'''
        ...
    
    @overload
    def set_table_formula(self, row_number : int, column_number : int, row_index_of_row_input_cell : int, column_index_of_row_input_cell : int, row_index_of_column_input_cell : int, column_index_of_column_input_cell : int, values : List[List[any]]):
        '''Create two-variable data table for given range starting from this cell.
        
        :param row_number: Number of rows to populate the formula.
        :param column_number: Number of columns to populate the formula.
        :param row_index_of_row_input_cell: row index of the row input cell
        :param column_index_of_row_input_cell: column index of the row input cell
        :param row_index_of_column_input_cell: row index of the column input cell
        :param column_index_of_column_input_cell: column index of the column input cell
        :param values: values for cells in table formula range'''
        ...
    
    @overload
    def set_table_formula(self, row_number : int, column_number : int, row_index_of_input_cell : int, column_index_of_input_cell : int, is_row_input : bool, values : List[List[any]]):
        '''Create one-variable data table for given range starting from this cell.
        
        :param row_number: Number of rows to populate the formula.
        :param column_number: Number of columns to populate the formula.
        :param row_index_of_input_cell: row index of the input cell
        :param column_index_of_input_cell: column index of the input cell
        :param is_row_input: Indicates whether the input cell is a row input cell(true) or a column input cell(false).
        :param values: values for cells in table formula range'''
        ...
    
    @overload
    def get_characters(self) -> List[aspose.cells.FontSetting]:
        '''Returns all Characters objects
        that represents a range of characters within the cell text.
        
        :returns: All Characters objects'''
        ...
    
    @overload
    def get_characters(self, flag : bool) -> List[aspose.cells.FontSetting]:
        '''Returns all Characters objects
        that represents a range of characters within the cell text.
        
        :param flag: Indicates whether applying table style to the cell if the cell is in the table.
        :returns: All Characters objects'''
        ...
    
    def get_string_value(self, format_strategy : aspose.cells.CellValueFormatStrategy) -> str:
        '''Gets the string value by specific formatted strategy.
        
        :param format_strategy: The formatted strategy.'''
        ...
    
    def get_width_of_value(self) -> int:
        '''Gets the width of the value in unit of pixels.'''
        ...
    
    def get_height_of_value(self) -> int:
        '''Gets the height of the value in unit of pixels.'''
        ...
    
    def get_format_conditions(self) -> List[aspose.cells.FormatConditionCollection]:
        '''Gets format conditions which applies to this cell.
        
        :returns: Returns :py:class:`aspose.cells.FormatConditionCollection` object'''
        ...
    
    def get_formula(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Get the formula of this cell.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: the formula of this cell.'''
        ...
    
    def get_precedents(self) -> aspose.cells.ReferredAreaCollection:
        '''Gets all references appearing in this cell's formula.
        
        :returns: Collection of all references appearing in this cell's formula.'''
        ...
    
    def get_dependents(self, is_all : bool) -> List[aspose.cells.Cell]:
        '''Get all cells whose formula references to this cell directly.
        
        :param is_all: Indicates whether check formulas in other worksheets'''
        ...
    
    def get_precedents_in_calculation(self) -> collections.abc.Iterator:
        '''Gets all precedents(reference to cells in current workbook) used by this cell's formula while calculating it.
        
        :returns: Enumerator to enumerate all references(ReferredArea)'''
        ...
    
    def get_dependents_in_calculation(self, recursive : bool) -> collections.abc.Iterator:
        '''Gets all cells whose calculated result depends on this cell.
        
        :param recursive: Whether returns those dependents which do not reference to this cell directly
        but reference to other leafs of this cell
        :returns: Enumerator to enumerate all dependents(Cell objects)'''
        ...
    
    def get_array_range(self) -> aspose.cells.CellArea:
        '''Gets the array range if the cell's formula is an array formula.
        
        :returns: The array range.'''
        ...
    
    def remove_array_formula(self, leave_normal_formula : bool):
        '''Remove array formula.
        
        :param leave_normal_formula: True represents converting the array formula to normal formula.'''
        ...
    
    def copy(self, cell : aspose.cells.Cell):
        '''Copies data from a source cell.
        
        :param cell: Source :py:class:`aspose.cells.Cell` object.'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the cell text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def is_rich_text(self) -> bool:
        '''Indicates whether the cell string value is a rich text.'''
        ...
    
    def set_characters(self, characters : List[aspose.cells.FontSetting]):
        '''Sets rich text format of the cell.
        
        :param characters: All Characters objects.'''
        ...
    
    def get_merged_range(self) -> aspose.cells.Range:
        '''Returns a :py:class:`aspose.cells.Range` object which represents a merged range.
        
        :returns: :py:class:`aspose.cells.Range` object. Null if this cell is not merged.'''
        ...
    
    def get_html_string(self, html5 : bool) -> str:
        '''Gets the html string which contains data and some formats in this cell.
        
        :param html5: Indicates whether the value is compatible for html5'''
        ...
    
    def to_json(self) -> str:
        '''Convert :py:class:`aspose.cells.Cell` to JSON struct data.'''
        ...
    
    def equals(self, cell : aspose.cells.Cell) -> bool:
        '''Checks whether this object refers to the same cell with another cell object.
        
        :param cell: another cell object
        :returns: true if two cell objects refers to the same cell.'''
        ...
    
    def get_conditional_formatting_result(self) -> aspose.cells.ConditionalFormattingResult:
        '''Get the result of the conditional formatting.'''
        ...
    
    def get_validation(self) -> aspose.cells.Validation:
        '''Gets the validation applied to this cell.'''
        ...
    
    def get_validation_value(self) -> bool:
        '''Gets the value of validation which applied to this cell.'''
        ...
    
    def get_table(self) -> aspose.cells.tables.ListObject:
        '''Gets the table which contains this cell.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the parent worksheet.'''
        ...
    
    @property
    def date_time_value(self) -> DateTime:
        ...
    
    @property
    def row(self) -> int:
        '''Gets row number (zero based) of the cell.'''
        ...
    
    @property
    def column(self) -> int:
        '''Gets column number (zero based) of the cell.'''
        ...
    
    @property
    def is_formula(self) -> bool:
        ...
    
    @property
    def type(self) -> aspose.cells.CellValueType:
        '''Represents cell value type.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name of the cell.'''
        ...
    
    @property
    def is_error_value(self) -> bool:
        ...
    
    @property
    def is_numeric_value(self) -> bool:
        ...
    
    @property
    def string_value(self) -> str:
        ...
    
    @property
    def string_value_without_format(self) -> str:
        ...
    
    @property
    def number_category_type(self) -> aspose.cells.NumberCategoryType:
        ...
    
    @property
    def display_string_value(self) -> str:
        ...
    
    @property
    def int_value(self) -> int:
        ...
    
    @property
    def double_value(self) -> float:
        ...
    
    @property
    def float_value(self) -> float:
        ...
    
    @property
    def bool_value(self) -> bool:
        ...
    
    @property
    def has_custom_style(self) -> bool:
        ...
    
    @property
    def shared_style_index(self) -> int:
        ...
    
    @property
    def formula(self) -> str:
        '''Gets a formula of the :py:class:`aspose.cells.Cell`.'''
        ...
    
    @formula.setter
    def formula(self, value : str):
        '''Sets a formula of the :py:class:`aspose.cells.Cell`.'''
        ...
    
    @property
    def formula_local(self) -> str:
        ...
    
    @formula_local.setter
    def formula_local(self, value : str):
        ...
    
    @property
    def r1c1_formula(self) -> str:
        ...
    
    @r1c1_formula.setter
    def r1c1_formula(self, value : str):
        ...
    
    @property
    def contains_external_link(self) -> bool:
        ...
    
    @property
    def is_array_header(self) -> bool:
        ...
    
    @property
    def is_dynamic_array_formula(self) -> bool:
        ...
    
    @property
    def is_array_formula(self) -> bool:
        ...
    
    @property
    def is_in_array(self) -> bool:
        ...
    
    @property
    def is_shared_formula(self) -> bool:
        ...
    
    @property
    def is_table_formula(self) -> bool:
        ...
    
    @property
    def is_in_table(self) -> bool:
        ...
    
    @property
    def value(self) -> any:
        '''Gets the value contained in this cell.'''
        ...
    
    @value.setter
    def value(self, value : any):
        '''Gets the value contained in this cell.'''
        ...
    
    @property
    def is_style_set(self) -> bool:
        ...
    
    @property
    def is_merged(self) -> bool:
        ...
    
    @property
    def comment(self) -> aspose.cells.Comment:
        '''Gets the comment of this cell.'''
        ...
    
    @property
    def html_string(self) -> str:
        ...
    
    @html_string.setter
    def html_string(self, value : str):
        ...
    
    ...

class CellArea:
    '''Represent an area of cells.'''
    
    @overload
    @staticmethod
    def create_cell_area(start_row : intstart_column : int, end_row : int, end_column : int) -> aspose.cells.CellArea:
        '''Creates a cell area.
        
        :param start_row: The start row.
        :param start_column: The start column.
        :param end_row: The end row.
        :param end_column: The end column.
        :returns: Return a :py:class:`aspose.cells.CellArea`.'''
        ...
    
    @overload
    @staticmethod
    def create_cell_area(start_cell_name : strend_cell_name : str) -> aspose.cells.CellArea:
        '''Creates a cell area.
        
        :param start_cell_name: The top-left cell of the range.
        :param end_cell_name: The bottom-right cell of the range.
        :returns: Return a :py:class:`aspose.cells.CellArea`.'''
        ...
    
    def compare_to(self, obj : any) -> int:
        '''Compare two CellArea objects according to their top-left corner.
        
        :returns: If two corners are in different rows, then compare their row index. Otherwise compare their column index.
        If two corners are same, then 0 will be returned.'''
        ...
    
    @property
    def start_row(self) -> int:
        ...
    
    @start_row.setter
    def start_row(self, value : int):
        ...
    
    @property
    def end_row(self) -> int:
        ...
    
    @end_row.setter
    def end_row(self, value : int):
        ...
    
    @property
    def start_column(self) -> int:
        ...
    
    @start_column.setter
    def start_column(self, value : int):
        ...
    
    @property
    def end_column(self) -> int:
        ...
    
    @end_column.setter
    def end_column(self, value : int):
        ...
    
    ...

class CellWatch:
    '''Represents Cell Watch Item in the 'watch window'.'''
    
    @property
    def row(self) -> int:
        '''Gets and sets the row of the cell.'''
        ...
    
    @row.setter
    def row(self, value : int):
        '''Gets and sets the row of the cell.'''
        ...
    
    @property
    def column(self) -> int:
        '''Gets and sets the column of the cell.'''
        ...
    
    @column.setter
    def column(self, value : int):
        '''Gets and sets the column of the cell.'''
        ...
    
    @property
    def cell_name(self) -> str:
        ...
    
    @cell_name.setter
    def cell_name(self, value : str):
        ...
    
    ...

class CellWatchCollection:
    '''Represents the collection of cells on this worksheet being watched in the 'watch window'.'''
    
    @overload
    def add(self, row : int, column : int) -> int:
        '''Adds :py:class:`aspose.cells.CellWatch` with row and column.
        
        :param row: The row index.
        :param column: The column index.
        :returns: Returns the position of this item in the collection.'''
        ...
    
    @overload
    def add(self, cell_name : str) -> int:
        '''Adds :py:class:`aspose.cells.CellWatch` with the name the of cell.
        
        :param cell_name: The name of the cell.'''
        ...
    
    @overload
    def copy_to(self, array : List[aspose.cells.CellWatch]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.CellWatch], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.CellWatch, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.CellWatch, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.CellWatch) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.CellWatch, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.CellWatch, index : int, count : int) -> int:
        ...
    
    def binary_search(self, item : aspose.cells.CellWatch) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class Cells:
    '''Encapsulates a collection of cell relevant objects, such as :py:class:`aspose.cells.Cell`, :py:class:`aspose.cells.Row`, ...etc.'''
    
    @overload
    def create_range(self, upper_left_cell : str, lower_right_cell : str) -> aspose.cells.Range:
        '''Creates a :py:class:`aspose.cells.Range` object from a range of cells.
        
        :param upper_left_cell: Upper left cell name.
        :param lower_right_cell: Lower right cell name.
        :returns: A :py:class:`aspose.cells.Range` object'''
        ...
    
    @overload
    def create_range(self, first_row : int, first_column : int, total_rows : int, total_columns : int) -> aspose.cells.Range:
        '''Creates a :py:class:`aspose.cells.Range` object from a range of cells.
        
        :param first_row: First row of this range
        :param first_column: First column of this range
        :param total_rows: Number of rows
        :param total_columns: Number of columns
        :returns: A :py:class:`aspose.cells.Range` object'''
        ...
    
    @overload
    def create_range(self, address : str) -> aspose.cells.Range:
        '''Creates a :py:class:`aspose.cells.Range` object from an address of the range.
        
        :param address: The address of the range.
        :returns: A :py:class:`aspose.cells.Range` object'''
        ...
    
    @overload
    def create_range(self, first_index : int, number : int, is_vertical : bool) -> aspose.cells.Range:
        '''Creates a :py:class:`aspose.cells.Range` object from rows of cells or columns of cells.
        
        :param first_index: First row index or first column index, zero based.
        :param number: Total number of rows or columns, one based.
        :param is_vertical: True - Range created from columns of cells. False - Range created from rows of cells.
        :returns: A :py:class:`aspose.cells.Range` object.'''
        ...
    
    @overload
    def get(self, row : int, column : int) -> aspose.cells.Cell:
        '''Add API for Python Via .Net.since this[int row, int column] is unsupported
        
        :param row: Row index.
        :param column: Column index.
        :returns: The :py:class:`aspose.cells.Cell` object.'''
        ...
    
    @overload
    def get(self, cell_name : str) -> aspose.cells.Cell:
        '''Add API for Python Via .Net.since this[string cellName] is unsupported
        
        :param cell_name: Cell name,including its column letter and row number, for example A5.
        :returns: A :py:class:`aspose.cells.Cell` object'''
        ...
    
    @overload
    def import_object_array(self, obj_array : List[any], first_row : int, first_column : int, is_vertical : bool):
        '''Imports an array of data into a worksheet.
        
        :param obj_array: Data array.
        :param first_row: The row number of the first cell to import in.
        :param first_column: The column number of the first cell to import in.
        :param is_vertical: Specifies to import data vertically or horizontally.'''
        ...
    
    @overload
    def import_object_array(self, obj_array : List[any], first_row : int, first_column : int, is_vertical : bool, skip : int):
        '''Imports an array of data into a worksheet.
        
        :param obj_array: Data array.
        :param first_row: The row number of the first cell to import in.
        :param first_column: The column number of the first cell to import in.
        :param is_vertical: Specifies to import data vertically or horizontally.
        :param skip: Skipped number of rows or columns.'''
        ...
    
    @overload
    def import_array(self, string_array : List[str], first_row : int, first_column : int, is_vertical : bool):
        '''Imports an array of string into a worksheet.
        
        :param string_array: String array.
        :param first_row: The row number of the first cell to import in.
        :param first_column: The column number of the first cell to import in.
        :param is_vertical: Specifies to import data vertically or horizontally.'''
        ...
    
    @overload
    def import_array(self, int_array : List[int], first_row : int, first_column : int, is_vertical : bool):
        '''Imports an array of integer into a worksheet.
        
        :param int_array: Integer array.
        :param first_row: The row number of the first cell to import in.
        :param first_column: The column number of the first cell to import in.
        :param is_vertical: Specifies to import data vertically or horizontally.'''
        ...
    
    @overload
    def import_array(self, double_array : List[float], first_row : int, first_column : int, is_vertical : bool):
        '''Imports an array of double into a worksheet.
        
        :param double_array: Double array.
        :param first_row: The row number of the first cell to import in.
        :param first_column: The column number of the first cell to import in.
        :param is_vertical: Specifies to import data vertically or horizontally.'''
        ...
    
    @overload
    def import_csv(self, file_name : str, splitter : str, convert_numeric_data : bool, first_row : int, first_column : int):
        '''Import a CSV file to the cells.
        
        :param file_name: The CSV file name.
        :param splitter: The splitter
        :param convert_numeric_data: Whether the string in text file is converted to numeric data.
        :param first_row: The row number of the first cell to import in.
        :param first_column: The column number of the first cell to import in.'''
        ...
    
    @overload
    def import_csv(self, stream : io.RawIOBase, splitter : str, convert_numeric_data : bool, first_row : int, first_column : int):
        '''Import a CSV file to the cells.
        
        :param stream: The CSV file stream.
        :param splitter: The splitter
        :param convert_numeric_data: Whether the string in text file is converted to numeric data.
        :param first_row: The row number of the first cell to import in.
        :param first_column: The column number of the first cell to import in.'''
        ...
    
    @overload
    def import_csv(self, file_name : str, options : aspose.cells.TxtLoadOptions, first_row : int, first_column : int):
        '''Import a CSV file to the cells.
        
        :param file_name: The CSV file name.
        :param options: The load options for reading text file
        :param first_row: The row number of the first cell to import in.
        :param first_column: The column number of the first cell to import in.'''
        ...
    
    @overload
    def import_csv(self, stream : io.RawIOBase, options : aspose.cells.TxtLoadOptions, first_row : int, first_column : int):
        '''Import a CSV file to the cells.
        
        :param stream: The CSV file stream.
        :param options: The load options for reading text file
        :param first_row: The row number of the first cell to import in.
        :param first_column: The column number of the first cell to import in.'''
        ...
    
    @overload
    def merge(self, first_row : int, first_column : int, total_rows : int, total_columns : int):
        '''Merges a specified range of cells into a single cell.
        
        :param first_row: First row of this range(zero based)
        :param first_column: First column of this range(zero based)
        :param total_rows: Number of rows(one based)
        :param total_columns: Number of columns(one based)'''
        ...
    
    @overload
    def merge(self, first_row : int, first_column : int, total_rows : int, total_columns : int, merge_conflict : bool):
        '''Merges a specified range of cells into a single cell.
        
        :param first_row: First row of this range(zero based)
        :param first_column: First column of this range(zero based)
        :param total_rows: Number of rows(one based)
        :param total_columns: Number of columns(one based)
        :param merge_conflict: Merge conflict merged ranges.'''
        ...
    
    @overload
    def merge(self, first_row : int, first_column : int, total_rows : int, total_columns : int, check_conflict : bool, merge_conflict : bool):
        '''Merges a specified range of cells into a single cell.
        
        :param first_row: First row of this range(zero based)
        :param first_column: First column of this range(zero based)
        :param total_rows: Number of rows(one based)
        :param total_columns: Number of columns(one based)
        :param check_conflict: Indicates whether check the merged cells intersects other merged cells
        :param merge_conflict: Merge conflict merged ranges.'''
        ...
    
    @overload
    def copy_columns(self, source_cells0 : aspose.cells.Cells, source_column_index : int, destination_column_index : int, column_number : int, paste_options : aspose.cells.PasteOptions):
        '''Copies data and formats of a whole column.
        
        :param source_cells0: Source Cells object contains data and formats to copy.
        :param source_column_index: Source column index.
        :param destination_column_index: Destination column index.
        :param column_number: The copied column number.
        :param paste_options: the options of pasting.'''
        ...
    
    @overload
    def copy_columns(self, source_cells0 : aspose.cells.Cells, source_column_index : int, destination_column_index : int, column_number : int):
        '''Copies data and formats of a whole column.
        
        :param source_cells0: Source Cells object contains data and formats to copy.
        :param source_column_index: Source column index.
        :param destination_column_index: Destination column index.
        :param column_number: The copied column number.'''
        ...
    
    @overload
    def copy_columns(self, source_cells : aspose.cells.Cells, source_column_index : int, source_total_columns : int, destination_column_index : int, destination_total_columns : int):
        '''Copies data and formats of the whole columns.
        
        :param source_cells: Source Cells object contains data and formats to copy.
        :param source_column_index: Source column index.
        :param source_total_columns: The number of the source columns.
        :param destination_column_index: Destination column index.
        :param destination_total_columns: The number of the destination columns.'''
        ...
    
    @overload
    def copy_rows(self, source_cells : aspose.cells.Cells, source_row_index : int, destination_row_index : int, row_number : int):
        '''Copies data and formats of some whole rows.
        
        :param source_cells: Source Cells object contains data and formats to copy.
        :param source_row_index: Source row index.
        :param destination_row_index: Destination row index.
        :param row_number: The copied row number.'''
        ...
    
    @overload
    def copy_rows(self, source_cells0 : aspose.cells.Cells, source_row_index : int, destination_row_index : int, row_number : int, copy_options : aspose.cells.CopyOptions):
        '''Copies data and formats of some whole rows.
        
        :param source_cells0: Source Cells object contains data and formats to copy.
        :param source_row_index: Source row index.
        :param destination_row_index: Destination row index.
        :param row_number: The copied row number.
        :param copy_options: The copy options.'''
        ...
    
    @overload
    def copy_rows(self, source_cells0 : aspose.cells.Cells, source_row_index : int, destination_row_index : int, row_number : int, copy_options : aspose.cells.CopyOptions, paste_options : aspose.cells.PasteOptions):
        '''Copies data and formats of some whole rows.
        
        :param source_cells0: Source Cells object contains data and formats to copy.
        :param source_row_index: Source row index.
        :param destination_row_index: Destination row index.
        :param row_number: The copied row number.
        :param copy_options: The copy options.
        :param paste_options: the options of pasting.'''
        ...
    
    @overload
    def group_columns(self, first_index : int, last_index : int):
        '''Groups columns.
        
        :param first_index: The first column index to be grouped.
        :param last_index: The last column index to be grouped.'''
        ...
    
    @overload
    def group_columns(self, first_index : int, last_index : int, is_hidden : bool):
        '''Groups columns.
        
        :param first_index: The first column index to be grouped.
        :param last_index: The last column index to be grouped.
        :param is_hidden: Specifies if the grouped columns are hidden.'''
        ...
    
    @overload
    def ungroup_rows(self, first_index : int, last_index : int, is_all : bool):
        '''Ungroups rows.
        
        :param first_index: The first row index to be ungrouped.
        :param last_index: The last row index to be ungrouped.
        :param is_all: True, removes all grouped info.Otherwise, remove the outer group info.'''
        ...
    
    @overload
    def ungroup_rows(self, first_index : int, last_index : int):
        '''Ungroups rows.
        
        :param first_index: The first row index to be ungrouped.
        :param last_index: The last row index to be ungrouped.'''
        ...
    
    @overload
    def group_rows(self, first_index : int, last_index : int, is_hidden : bool):
        '''Groups rows.
        
        :param first_index: The first row index to be grouped.
        :param last_index: The last row index to be grouped.
        :param is_hidden: Specifies if the grouped rows are hidden.'''
        ...
    
    @overload
    def group_rows(self, first_index : int, last_index : int):
        '''Groups rows.
        
        :param first_index: The first row index to be grouped.
        :param last_index: The last row index to be grouped.'''
        ...
    
    @overload
    def delete_column(self, column_index : int, update_reference : bool):
        '''Deletes a column.
        
        :param column_index: Column index.
        :param update_reference: Indicates if update references in other worksheets.'''
        ...
    
    @overload
    def delete_column(self, column_index : int):
        '''Deletes a column.
        
        :param column_index: Column index.'''
        ...
    
    @overload
    def delete_rows(self, row_index : int, total_rows : int) -> bool:
        '''Deletes several rows.
        
        :param row_index: The first row index to be deleted.
        :param total_rows: Number of rows to be deleted.'''
        ...
    
    @overload
    def delete_rows(self, row_index : int, total_rows : int, update_reference : bool) -> bool:
        '''Deletes multiple rows in the worksheet.
        
        :param row_index: Row index.
        :param total_rows: Number of rows to be deleted.
        :param update_reference: Indicates if update references in other worksheets.'''
        ...
    
    @overload
    def delete_blank_columns(self):
        '''Delete all blank columns which do not contain any data.'''
        ...
    
    @overload
    def delete_blank_columns(self, options : aspose.cells.DeleteOptions):
        '''Delete all blank columns which do not contain any data.
        
        :param options: The options of deleting range.'''
        ...
    
    @overload
    def delete_blank_rows(self):
        '''Delete all blank rows which do not contain any data.'''
        ...
    
    @overload
    def delete_blank_rows(self, options : aspose.cells.DeleteOptions):
        '''Delete all blank rows which do not contain any data.
        
        :param options: The options of deleting range.'''
        ...
    
    @overload
    def insert_columns(self, column_index : int, total_columns : int):
        '''Inserts some columns into the worksheet.
        
        :param column_index: Column index.
        :param total_columns: The number of columns.'''
        ...
    
    @overload
    def insert_columns(self, column_index : int, total_columns : int, update_reference : bool):
        '''Inserts some columns into the worksheet.
        
        :param column_index: Column index.
        :param total_columns: The number of columns.
        :param update_reference: Indicates if references in other worksheets will be updated.'''
        ...
    
    @overload
    def insert_column(self, column_index : int, update_reference : bool):
        '''Inserts a new column into the worksheet.
        
        :param column_index: Column index.
        :param update_reference: Indicates if references in other worksheets will be updated.'''
        ...
    
    @overload
    def insert_column(self, column_index : int):
        '''Inserts a new column into the worksheet.
        
        :param column_index: Column index.'''
        ...
    
    @overload
    def insert_rows(self, row_index : int, total_rows : int, update_reference : bool):
        '''Inserts multiple rows into the worksheet.
        
        :param row_index: Row index.
        :param total_rows: Number of rows to be inserted.
        :param update_reference: Indicates if references in other worksheets will be updated.'''
        ...
    
    @overload
    def insert_rows(self, row_index : int, total_rows : int, options : aspose.cells.InsertOptions):
        '''Inserts multiple rows into the worksheet.
        
        :param row_index: Row index.
        :param total_rows: Number of rows to be inserted.
        :param options: Indicates if references in other worksheets will be updated.'''
        ...
    
    @overload
    def insert_rows(self, row_index : int, total_rows : int):
        '''Inserts multiple rows into the worksheet.
        
        :param row_index: Row index.
        :param total_rows: Number of rows to be inserted.'''
        ...
    
    @overload
    def clear_range(self, range : aspose.cells.CellArea):
        '''Clears contents and formatting of a range.
        
        :param range: Range to be cleared.'''
        ...
    
    @overload
    def clear_range(self, start_row : int, start_column : int, end_row : int, end_column : int):
        '''Clears contents and formatting of a range.
        
        :param start_row: Start row index.
        :param start_column: Start column index.
        :param end_row: End row index.
        :param end_column: End column index.'''
        ...
    
    @overload
    def clear_contents(self, range : aspose.cells.CellArea):
        '''Clears contents of a range.
        
        :param range: Range to be cleared.'''
        ...
    
    @overload
    def clear_contents(self, start_row : int, start_column : int, end_row : int, end_column : int):
        '''Clears contents of a range.
        
        :param start_row: Start row index.
        :param start_column: Start column index.
        :param end_row: End row index.
        :param end_column: End column index.'''
        ...
    
    @overload
    def clear_formats(self, range : aspose.cells.CellArea):
        '''Clears formatting of a range.
        
        :param range: Range to be cleared.'''
        ...
    
    @overload
    def clear_formats(self, start_row : int, start_column : int, end_row : int, end_column : int):
        '''Clears formatting of a range.
        
        :param start_row: Start row index.
        :param start_column: Start column index.
        :param end_row: End row index.
        :param end_column: End column index.'''
        ...
    
    @overload
    def find(self, what : any, previous_cell : aspose.cells.Cell) -> aspose.cells.Cell:
        '''Finds the cell containing with the input object.
        
        :param what: The object to search for.
        The type should be int,double,DateTime,string,bool.
        :param previous_cell: Previous cell with the same object.
        This parameter can be set to null if searching from the start.
        :returns: Cell object.'''
        ...
    
    @overload
    def find(self, what : any, previous_cell : aspose.cells.Cell, find_options : aspose.cells.FindOptions) -> aspose.cells.Cell:
        '''Finds the cell containing with the input object.
        
        :param what: The object to search for.
        The type should be int,double,DateTime,string,bool.
        :param previous_cell: Previous cell with the same object.
        This parameter can be set to null if searching from the start.
        :param find_options: Find options
        :returns: Cell object.'''
        ...
    
    @overload
    def end_cell_in_row(self, row_index : int) -> aspose.cells.Cell:
        '''Gets the last cell in this row.
        
        :param row_index: Row index.
        :returns: Cell object.'''
        ...
    
    @overload
    def end_cell_in_row(self, start_row : int, end_row : int, start_column : int, end_column : int) -> aspose.cells.Cell:
        '''Gets the last cell with maximum row index in this range.
        
        :param start_row: Start row index.
        :param end_row: End row index.
        :param start_column: Start column index.
        :param end_column: End column index.
        :returns: Cell object.'''
        ...
    
    @overload
    def end_cell_in_column(self, column_index : int) -> aspose.cells.Cell:
        '''Gets the last cell in this column.
        
        :param column_index: Column index.
        :returns: Cell object.'''
        ...
    
    @overload
    def end_cell_in_column(self, start_row : int, end_row : int, start_column : int, end_column : int) -> aspose.cells.Cell:
        '''Gets the last cell with maximum column index in this range.
        
        :param start_row: Start row index.
        :param end_row: End row index.
        :param start_column: Start column index.
        :param end_column: End column index.
        :returns: Cell object.'''
        ...
    
    @overload
    def insert_range(self, area : aspose.cells.CellArea, shift_number : int, shift_type : aspose.cells.ShiftType, update_reference : bool):
        '''Inserts a range of cells and shift cells according to the shift option.
        
        :param area: Shift area.
        :param shift_number: Number of rows or columns to be inserted.
        :param shift_type: Shift cells option.
        :param update_reference: Indicates if update references in other worksheets.'''
        ...
    
    @overload
    def insert_range(self, area : aspose.cells.CellArea, shift_type : aspose.cells.ShiftType):
        '''Inserts a range of cells and shift cells according to the shift option.
        
        :param area: Shift area.
        :param shift_type: Shift cells option.'''
        ...
    
    @overload
    def insert_range(self, area : aspose.cells.CellArea, shift_number : int, shift_type : aspose.cells.ShiftType):
        '''Inserts a range of cells and shift cells according to the shift option.
        
        :param area: Shift area.
        :param shift_number: Number of rows or columns to be inserted.
        :param shift_type: Shift cells option.'''
        ...
    
    @overload
    def import_custom_objects(self, list : list, property_names : List[str], is_property_name_shown : bool, first_row : int, first_column : int, row_number : int, insert_rows : bool, date_format_string : str, convert_string_to_number : bool) -> int:
        '''Imports custom objects.
        
        :param list: The custom object
        :param property_names: The property names.If it is null,we will import all properties of the object.
        :param is_property_name_shown: Indicates whether the property name will be imported to the first row.
        :param first_row: The row number of the first cell to import in.
        :param first_column: The column number of the first cell to import in.
        :param row_number: Number of rows to be imported.
        :param insert_rows: Indicates whether extra rows are added to fit data.
        :param date_format_string: Date format string for cells.
        :param convert_string_to_number: Indicates if this method will try to convert string to number.
        :returns: Total number of rows imported.'''
        ...
    
    @overload
    def import_custom_objects(self, list : list, first_row : int, first_column : int, options : aspose.cells.ImportTableOptions) -> int:
        '''Imports custom objects.
        
        :param list: The custom object
        :param first_row: The row number of the first cell to import in.
        :param first_column: The column number of the first cell to import in.
        :param options: The import options.
        :returns: Total number of rows imported.'''
        ...
    
    @overload
    def subtotal(self, ca : aspose.cells.CellArea, group_by : int, function : aspose.cells.ConsolidationFunction, total_list : List[int]):
        '''Creates subtotals for the range.
        
        :param ca: The range
        :param group_by: The field to group by, as a zero-based integer offset
        :param function: The subtotal function.
        :param total_list: An array of zero-based field offsets, indicating the fields to which the subtotals are added.'''
        ...
    
    @overload
    def subtotal(self, ca : aspose.cells.CellArea, group_by : int, function : aspose.cells.ConsolidationFunction, total_list : List[int], replace : bool, page_breaks : bool, summary_below_data : bool):
        '''Creates subtotals for the range.
        
        :param ca: The range
        :param group_by: The field to group by, as a zero-based integer offset
        :param function: The subtotal function.
        :param total_list: An array of zero-based field offsets, indicating the fields to which the subtotals are added.
        :param replace: Indicates whether replace the current subtotals
        :param page_breaks: Indicates whether add page break between groups
        :param summary_below_data: Indicates whether add summary below data.'''
        ...
    
    @overload
    def remove_duplicates(self):
        '''Removes duplicate rows in the sheet.'''
        ...
    
    @overload
    def remove_duplicates(self, start_row : int, start_column : int, end_row : int, end_column : int):
        '''Removes duplicate values in the range.
        
        :param start_row: The start row.
        :param start_column: The start column
        :param end_row: The end row index.
        :param end_column: The end column index.'''
        ...
    
    @overload
    def remove_duplicates(self, start_row : int, start_column : int, end_row : int, end_column : int, has_headers : bool, column_offsets : List[int]):
        '''Removes duplicate data of the range.
        
        :param start_row: The start row.
        :param start_column: The start column
        :param end_row: The end row index.
        :param end_column: The end column index.
        :param has_headers: Indicates whether the range contains headers.
        :param column_offsets: The column offsets.'''
        ...
    
    def get_row_enumerator(self) -> collections.abc.Iterator:
        '''Gets the rows enumerator.
        
        :returns: The rows enumerator.'''
        ...
    
    def get_cell(self, row : int, column : int) -> aspose.cells.Cell:
        '''Gets the :py:class:`aspose.cells.Cell` element or null at the specified cell row index and column index.
        
        :param row: Row index
        :param column: Column index
        :returns: Return Cell object if a Cell object exists.
        Return null if the cell does not exist.'''
        ...
    
    def get_row(self, row : int) -> aspose.cells.Row:
        '''Gets the :py:class:`aspose.cells.Row` element at the specified cell row index.
        
        :param row: Row index
        :returns: If the row object does exist return Row object, otherwise return null.'''
        ...
    
    def check_cell(self, row : int, column : int) -> aspose.cells.Cell:
        '''Gets the :py:class:`aspose.cells.Cell` element or null at the specified cell row index and column index.
        
        :param row: Row index
        :param column: Column index
        :returns: Return Cell object if a Cell object exists.
        Return null if the cell does not exist.'''
        ...
    
    def check_row(self, row : int) -> aspose.cells.Row:
        '''Gets the :py:class:`aspose.cells.Row` element or at the specified cell row index.
        
        :param row: Row index
        :returns: If the row object does exist return Row object, otherwise return null.'''
        ...
    
    def check_column(self, column_index : int) -> aspose.cells.Column:
        '''Gets the :py:class:`aspose.cells.Column` element or null at the specified column index.
        
        :param column_index: The column index.
        :returns: The Column object.'''
        ...
    
    def is_row_hidden(self, row_index : int) -> bool:
        '''Checks whether a row at given index is hidden.
        
        :param row_index: row index
        :returns: true if the row is hidden'''
        ...
    
    def is_column_hidden(self, column_index : int) -> bool:
        '''Checks whether a column at given index is hidden.
        
        :param column_index: column index
        :returns: true if the column is hidden.'''
        ...
    
    def add_range(self, range_object : aspose.cells.Range):
        '''Adds a range object reference to cells
        
        :param range_object: The range object will be contained in the cells'''
        ...
    
    def clear(self):
        '''Clears all cell and row objects.'''
        ...
    
    def import_data(self, table : aspose.cells.ICellsDataTable, first_row : int, first_column : int, options : aspose.cells.ImportTableOptions) -> int:
        '''Import data from custom data table.
        
        :param table: The custom data table.
        :param first_row: First row index.
        :param first_column: First column index.
        :param options: The import options'''
        ...
    
    def import_array_list(self, array_list : list, first_row : int, first_column : int, is_vertical : bool):
        '''Imports an arraylist of data into a worksheet.
        
        :param array_list: Data arraylist.
        :param first_row: The row number of the first cell to import in.
        :param first_column: The column number of the first cell to import in.
        :param is_vertical: Specifies to import data vertically or horizontally.'''
        ...
    
    def import_formula_array(self, string_array : List[str], first_row : int, first_column : int, is_vertical : bool):
        '''Imports an array of formula into a worksheet.
        
        :param string_array: Formula array.
        :param first_row: The row number of the first cell to import in.
        :param first_column: The column number of the first cell to import in.
        :param is_vertical: Specifies to import data vertically or horizontally.'''
        ...
    
    def text_to_columns(self, row : int, column : int, total_rows : int, options : aspose.cells.TxtLoadOptions):
        '''Splits the text in the column to columns.
        
        :param row: The row index.
        :param column: The column index.
        :param total_rows: The number of rows.
        :param options: The split options.'''
        ...
    
    def un_merge(self, first_row : int, first_column : int, total_rows : int, total_columns : int):
        '''Unmerges a specified range of merged cells.
        
        :param first_row: First row of this range(zero based)
        :param first_column: First column of this range(zero based)
        :param total_rows: Number of rows(one based)
        :param total_columns: Number of columns(one based)'''
        ...
    
    def clear_merged_cells(self):
        '''Clears all merged ranges.'''
        ...
    
    def hide_row(self, row : int):
        '''Hides a row.
        
        :param row: Row index.'''
        ...
    
    def unhide_row(self, row : int, height : float):
        '''Unhides a row.
        
        :param row: Row index.
        :param height: Row height. The row's height will be changed only when the row is hidden and given height value is positive.'''
        ...
    
    def hide_rows(self, row : int, total_rows : int):
        '''Hides multiple rows.
        
        :param row: The row index.
        :param total_rows: The row number.'''
        ...
    
    def unhide_rows(self, row : int, total_rows : int, height : float):
        '''Unhides the hidden rows.
        
        :param row: The row index.
        :param total_rows: The row number.
        :param height: Row height. The row's height will be changed only when the row is hidden and given height value is positive.'''
        ...
    
    def set_row_height_pixel(self, row : int, pixels : int):
        '''Sets row height in unit of pixels.
        
        :param row: Row index.
        :param pixels: Number of pixels.'''
        ...
    
    def set_row_height_inch(self, row : int, inches : float):
        '''Sets row height in unit of inches.
        
        :param row: Row index.
        :param inches: Number of inches. It should be between 0 and 409.5/72.'''
        ...
    
    def set_row_height(self, row : int, height : float):
        '''Sets the height of the specified row.
        
        :param row: Row index.
        :param height: Height of row.In unit of point It should be between 0 and 409.5.'''
        ...
    
    def get_row_original_height_point(self, row : int) -> float:
        '''Gets original row's height in unit of point if the row is hidden
        
        :param row: The row index.'''
        ...
    
    def hide_column(self, column : int):
        '''Hides a column.
        
        :param column: Column index.'''
        ...
    
    def unhide_column(self, column : int, width : float):
        '''Unhides a column
        
        :param column: Column index.
        :param width: Column width.'''
        ...
    
    def hide_columns(self, column : int, total_columns : int):
        '''Hide multiple columns.
        
        :param column: Column index.
        :param total_columns: Column number.'''
        ...
    
    def unhide_columns(self, column : int, total_columns : int, width : float):
        '''Unhide multiple columns.
        
        :param column: Column index.
        :param total_columns: Column number
        :param width: Column width.'''
        ...
    
    def get_row_height(self, row : int) -> float:
        '''Gets the height of a specified row.
        
        :param row: Row index
        :returns: Height of row'''
        ...
    
    def get_view_row_height(self, row : int) -> float:
        '''Gets the height of a specified row.
        
        :param row: Row index
        :returns: Height of row'''
        ...
    
    def get_row_height_pixel(self, row : int) -> int:
        '''Gets the height of a specified row in unit of pixel.
        
        :param row: Row index
        :returns: Height of row'''
        ...
    
    def get_row_height_inch(self, row : int) -> float:
        '''Gets the height of a specified row in unit of inches.
        
        :param row: Row index
        :returns: Height of row'''
        ...
    
    def get_view_row_height_inch(self, row : int) -> float:
        '''Gets the height of a specified row in unit of inches.
        
        :param row: Row index
        :returns: Height of row'''
        ...
    
    def set_column_width_pixel(self, column : int, pixels : int):
        '''Sets column width in unit of pixels in normal view.
        
        :param column: Column index.
        :param pixels: Number of pixels.'''
        ...
    
    def set_column_width_inch(self, column : int, inches : float):
        '''Sets column width in unit of inches  in normal view.
        
        :param column: Column index.
        :param inches: Number of inches.'''
        ...
    
    def set_column_width(self, column : int, width : float):
        '''Sets the width of the specified column in normal view.
        
        :param column: Column index.
        :param width: Width of column.Column width must be between 0 and 255.'''
        ...
    
    def get_column_width_pixel(self, column : int) -> int:
        '''Gets the width of the specified column in normal view, in units of pixel.
        
        :param column: Column index
        :returns: Width of column in normal view.'''
        ...
    
    def get_column_width_inch(self, column : int) -> float:
        '''Gets the width of the specified column in normal view, in units of inches.
        
        :param column: Column index
        :returns: Width of column'''
        ...
    
    def get_column_width(self, column : int) -> float:
        '''Gets the width of the specified column in normal view
        
        :param column: Column index
        :returns: Width of column'''
        ...
    
    def get_view_column_width_pixel(self, column : int) -> int:
        '''Get the width in different view type.
        
        :param column: The column index.
        :returns: the column width in unit of pixels'''
        ...
    
    def set_view_column_width_pixel(self, column : int, pixels : int):
        '''Sets the width of the column in different view.
        
        :param column: The column index.
        :param pixels: The width in unit of pixels.'''
        ...
    
    def get_last_data_row(self, column : int) -> int:
        '''Gets the last row index of cell which contains data in the specified column.
        
        :param column: Column index.
        :returns: last row index.'''
        ...
    
    def apply_column_style(self, column : int, style : aspose.cells.Style, flag : aspose.cells.StyleFlag):
        '''Applies formats for a whole column.
        
        :param column: The column index.
        :param style: The style object which will be applied.
        :param flag: Flags which indicates applied formatting properties.'''
        ...
    
    def apply_row_style(self, row : int, style : aspose.cells.Style, flag : aspose.cells.StyleFlag):
        '''Applies formats for a whole row.
        
        :param row: The row index.
        :param style: The style object which will be applied.
        :param flag: Flags which indicates applied formatting properties.'''
        ...
    
    def apply_style(self, style : aspose.cells.Style, flag : aspose.cells.StyleFlag):
        '''Applies formats for a whole worksheet.
        
        :param style: The style object which will be applied.
        :param flag: Flags which indicates applied formatting properties.'''
        ...
    
    def copy_column(self, source_cells : aspose.cells.Cells, source_column_index : int, destination_column_index : int):
        '''Copies data and formats of a whole column.
        
        :param source_cells: Source Cells object contains data and formats to copy.
        :param source_column_index: Source column index.
        :param destination_column_index: Destination column index.'''
        ...
    
    def copy_row(self, source_cells : aspose.cells.Cells, source_row_index : int, destination_row_index : int):
        '''Copies data and formats of a whole row.
        
        :param source_cells: Source Cells object contains data and formats to copy.
        :param source_row_index: Source row index.
        :param destination_row_index: Destination row index.'''
        ...
    
    def get_grouped_row_outline_level(self, row_index : int) -> int:
        '''Gets the outline level (zero-based) of the row.
        
        :param row_index: The row index.
        :returns: The outline level (zero-based) of the row.'''
        ...
    
    def get_grouped_column_outline_level(self, column_index : int) -> int:
        '''Gets the outline level (zero-based) of the column.
        
        :param column_index: The column index
        :returns: The outline level of the column'''
        ...
    
    def get_max_grouped_column_outline_level(self) -> int:
        '''Gets the max grouped column outline level (zero-based).
        
        :returns: The max grouped column outline level (zero-based)'''
        ...
    
    def get_max_grouped_row_outline_level(self) -> int:
        '''Gets the max grouped row outline level (zero-based).
        
        :returns: The max grouped row outline level (zero-based)'''
        ...
    
    def show_group_detail(self, is_vertical : bool, index : int):
        '''Expands the grouped rows/columns.
        
        :param is_vertical: True, expands the grouped rows.
        :param index: The row/column index'''
        ...
    
    def hide_group_detail(self, is_vertical : bool, index : int):
        '''Collapses the grouped rows/columns.
        
        :param is_vertical: True, collapse the grouped rows.
        :param index: The row/column index'''
        ...
    
    def ungroup_columns(self, first_index : int, last_index : int):
        '''Ungroups columns.
        
        :param first_index: The first column index to be ungrouped.
        :param last_index: The last column index to be ungrouped.'''
        ...
    
    def delete_columns(self, column_index : int, total_columns : int, update_reference : bool):
        '''Deletes several columns.
        
        :param column_index: Column index.
        :param total_columns: Number of columns to be deleted.
        :param update_reference: Indicates if update references in other worksheets.'''
        ...
    
    def is_deleting_range_enabled(self, start_row : int, start_column : int, total_rows : int, total_columns : int) -> bool:
        '''Check whether the range could be deleted.
        
        :param start_row: The start row index of the range.
        :param start_column: The start column index of the range.
        :param total_rows: The number of the rows in the range.
        :param total_columns: The number of the columns in the range.'''
        ...
    
    def delete_row(self, row_index : int):
        '''Deletes a row.
        
        :param row_index: Row index.'''
        ...
    
    def is_blank_column(self, column_index : int) -> bool:
        '''Checks whether given column is blank(does not contain any data).
        
        :param column_index: the column index
        :returns: true if given column does not contain any data'''
        ...
    
    def insert_row(self, row_index : int):
        '''Inserts a new row into the worksheet.
        
        :param row_index: Row index.'''
        ...
    
    def link_to_xml_map(self, map_name : str, row : int, column : int, path : str):
        '''Link to a xml map.
        
        :param map_name: name of xml map
        :param row: row of the destination cell
        :param column: column of the destination cell
        :param path: path of xml element in xml map'''
        ...
    
    def find_formula(self, formula : str, previous_cell : aspose.cells.Cell) -> aspose.cells.Cell:
        '''Finds the cell with the input string.
        
        :param formula: The formula to search for.
        :param previous_cell: Previous cell with the same formula. This parameter can be set to null if searching from the start.
        :returns: Cell object.'''
        ...
    
    def find_formula_contains(self, formula : str, previous_cell : aspose.cells.Cell) -> aspose.cells.Cell:
        '''Finds the cell with formula which contains the input string.
        
        :param formula: The formula to search for.
        :param previous_cell: Previous cell with the same formula. This parameter can be set to null if searching from the start.
        :returns: Cell object.'''
        ...
    
    def move_range(self, source_area : aspose.cells.CellArea, dest_row : int, dest_column : int):
        '''Moves the range.
        
        :param source_area: The range which should be moved.
        :param dest_row: The dest row.
        :param dest_column: The dest column.'''
        ...
    
    def insert_cut_cells(self, cut_range : aspose.cells.Range, row : int, column : int, shift_type : aspose.cells.ShiftType):
        '''Insert cut range.
        
        :param cut_range: The cut range.
        :param row: The row.
        :param column: The column.
        :param shift_type: The shift type .'''
        ...
    
    def delete_range(self, start_row : int, start_column : int, end_row : int, end_column : int, shift_type : aspose.cells.ShiftType):
        '''Deletes a range of cells and shift cells according to the shift option.
        
        :param start_row: Start row index.
        :param start_column: Start column index.
        :param end_row: End row index.
        :param end_column: End column index.
        :param shift_type: Shift cells option.'''
        ...
    
    def retrieve_subtotal_setting(self, ca : aspose.cells.CellArea) -> aspose.cells.SubtotalSetting:
        '''Retrieves subtotals setting of the range.
        
        :param ca: The range'''
        ...
    
    def remove_formulas(self):
        '''Removes all formula and replaces with the value of the formula.'''
        ...
    
    def convert_string_to_numeric_value(self):
        '''Converts string data in cells to numeric value if possible.'''
        ...
    
    def get_dependents(self, is_all : bool, row : int, column : int) -> List[aspose.cells.Cell]:
        '''Get all cells which refer to the specific cell.
        
        :param is_all: Indicates whether check other worksheets
        :param row: The row index.
        :param column: The column index.'''
        ...
    
    def get_dependents_in_calculation(self, row : int, column : int, recursive : bool) -> collections.abc.Iterator:
        '''Gets all cells whose calculated result depends on specific cell.
        
        :param row: Row index of the specific cell
        :param column: Column index of the specific cell.
        :param recursive: Whether returns those dependents which do not reference to the specific cell directly
        but reference to other leafs of that cell.
        :returns: Enumerator to enumerate all dependents(Cell objects)'''
        ...
    
    def get_cell_style(self, row : int, column : int) -> aspose.cells.Style:
        '''Get the style of given cell.
        
        :param row: row index
        :param column: column
        :returns: the style of given cell.'''
        ...
    
    @property
    def ods_cell_fields(self) -> aspose.cells.ods.OdsCellFieldCollection:
        ...
    
    @property
    def count(self) -> int:
        '''Gets the total count of instantiated Cell objects.'''
        ...
    
    @property
    def count_large(self) -> int:
        ...
    
    @property
    def rows(self) -> aspose.cells.RowCollection:
        '''Gets the collection of :py:class:`aspose.cells.Row` objects that represents the individual rows in this worksheet.'''
        ...
    
    @property
    def merged_cells(self) -> list:
        ...
    
    @property
    def multi_thread_reading(self) -> bool:
        ...
    
    @multi_thread_reading.setter
    def multi_thread_reading(self, value : bool):
        ...
    
    @property
    def memory_setting(self) -> aspose.cells.MemorySetting:
        ...
    
    @memory_setting.setter
    def memory_setting(self, value : aspose.cells.MemorySetting):
        ...
    
    @property
    def style(self) -> aspose.cells.Style:
        '''Gets and sets the default style.'''
        ...
    
    @style.setter
    def style(self, value : aspose.cells.Style):
        '''Gets and sets the default style.'''
        ...
    
    @property
    def standard_width_inch(self) -> float:
        ...
    
    @standard_width_inch.setter
    def standard_width_inch(self, value : float):
        ...
    
    @property
    def standard_width_pixels(self) -> int:
        ...
    
    @standard_width_pixels.setter
    def standard_width_pixels(self, value : int):
        ...
    
    @property
    def standard_width(self) -> float:
        ...
    
    @standard_width.setter
    def standard_width(self, value : float):
        ...
    
    @property
    def standard_height(self) -> float:
        ...
    
    @standard_height.setter
    def standard_height(self, value : float):
        ...
    
    @property
    def standard_height_pixels(self) -> int:
        ...
    
    @standard_height_pixels.setter
    def standard_height_pixels(self, value : int):
        ...
    
    @property
    def standard_height_inch(self) -> float:
        ...
    
    @standard_height_inch.setter
    def standard_height_inch(self, value : float):
        ...
    
    @property
    def preserve_string(self) -> bool:
        ...
    
    @preserve_string.setter
    def preserve_string(self, value : bool):
        ...
    
    @property
    def min_row(self) -> int:
        ...
    
    @property
    def max_row(self) -> int:
        ...
    
    @property
    def min_column(self) -> int:
        ...
    
    @property
    def max_column(self) -> int:
        ...
    
    @property
    def min_data_row(self) -> int:
        ...
    
    @property
    def max_data_row(self) -> int:
        ...
    
    @property
    def min_data_column(self) -> int:
        ...
    
    @property
    def max_data_column(self) -> int:
        ...
    
    @property
    def is_default_row_height_matched(self) -> bool:
        ...
    
    @is_default_row_height_matched.setter
    def is_default_row_height_matched(self, value : bool):
        ...
    
    @property
    def is_default_row_hidden(self) -> bool:
        ...
    
    @is_default_row_hidden.setter
    def is_default_row_hidden(self, value : bool):
        ...
    
    @property
    def columns(self) -> aspose.cells.ColumnCollection:
        '''Gets the collection of :py:class:`aspose.cells.Column` objects that represents the individual columns in this worksheet.'''
        ...
    
    @property
    def ranges(self) -> aspose.cells.RangeCollection:
        '''Gets the collection of :py:class:`aspose.cells.Range` objects created at run time.'''
        ...
    
    @property
    def last_cell(self) -> aspose.cells.Cell:
        ...
    
    @property
    def max_display_range(self) -> aspose.cells.Range:
        ...
    
    @property
    def first_cell(self) -> aspose.cells.Cell:
        ...
    
    def __getitem__(self, key : int) -> aspose.cells.Cell:
        '''Gets :py:class:`aspose.cells.Cell` item within the worksheet'''
        ...
    
    ...

class CellsColor:
    '''Represents all types of color.'''
    
    def set_tint_of_shape_color(self, tint : float):
        '''Set the tint of the shape color'''
        ...
    
    @property
    def is_shape_color(self) -> bool:
        ...
    
    @is_shape_color.setter
    def is_shape_color(self, value : bool):
        ...
    
    @property
    def type(self) -> aspose.cells.ColorType:
        '''The color type.'''
        ...
    
    @property
    def theme_color(self) -> aspose.cells.ThemeColor:
        ...
    
    @theme_color.setter
    def theme_color(self, value : aspose.cells.ThemeColor):
        ...
    
    @property
    def color_index(self) -> int:
        ...
    
    @color_index.setter
    def color_index(self, value : int):
        ...
    
    @property
    def color(self) -> aspose.pydrawing.Color:
        '''Gets and sets the RGB color.'''
        ...
    
    @color.setter
    def color(self, value : aspose.pydrawing.Color):
        '''Gets and sets the RGB color.'''
        ...
    
    @property
    def argb(self) -> int:
        '''Gets and sets the color from a 32-bit ARGB value.'''
        ...
    
    @argb.setter
    def argb(self, value : int):
        '''Gets and sets the color from a 32-bit ARGB value.'''
        ...
    
    @property
    def transparency(self) -> float:
        '''Gets and sets transparency as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    @transparency.setter
    def transparency(self, value : float):
        '''Gets and sets transparency as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    ...

class CellsDataTableFactory:
    '''Utility to build ICellsDataTable from custom objects for user's convenience.'''
    
    @overload
    def get_instance(self, vals : List[int], column_names : List[str]) -> aspose.cells.ICellsDataTable:
        '''Creates ICellsDataTable from given sequence of int values.
        
        :param vals: int values to build table
        :param column_names: Column names of the table.
        Its length can only be either 1(build table by the int values vertically)
        or length of the int values(build table by the int values horizontally)
        :returns: Instance of ICellsDataTable'''
        ...
    
    @overload
    def get_instance(self, vals : List[int], vertial : bool) -> aspose.cells.ICellsDataTable:
        '''Creates ICellsDataTable from given sequence of int values.
        
        :param vals: int values to build table
        :param vertial: whether build table by the int values vertiacally(true) or horizontally(false)
        :returns: Instance of ICellsDataTable'''
        ...
    
    @overload
    def get_instance(self, vals : List[float], column_names : List[str]) -> aspose.cells.ICellsDataTable:
        '''Creates ICellsDataTable from given sequence of double values.
        
        :param vals: double values to build table
        :param column_names: Column names of the table.
        Its length can only be either 1(build table by the double values vertically)
        or length of the double values(build table by the double values horizontally)
        :returns: Instance of ICellsDataTable'''
        ...
    
    @overload
    def get_instance(self, vals : List[float], vertial : bool) -> aspose.cells.ICellsDataTable:
        '''Creates ICellsDataTable from given sequence of double values.
        
        :param vals: double values to build table
        :param vertial: whether build table by the double values vertiacally(true) or horizontally(false)
        :returns: Instance of ICellsDataTable'''
        ...
    
    @overload
    def get_instance(self, vals : List[any], column_names : List[str]) -> aspose.cells.ICellsDataTable:
        '''Creates ICellsDataTable from given sequence of objects.
        
        :param vals: objects to build table
        :param column_names: Column names of the table.
        Its length can only be either 1(build table by the objects vertically)
        or length of the objects(build table by the objects horizontally)
        :returns: Instance of ICellsDataTable'''
        ...
    
    @overload
    def get_instance(self, vals : List[any], vertial : bool) -> aspose.cells.ICellsDataTable:
        '''Creates ICellsDataTable from given sequence of objects.
        
        :param vals: objects to build table
        :param vertial: whether build table by the objects vertiacally(true) or horizontally(false)
        :returns: Instance of ICellsDataTable'''
        ...
    
    @overload
    def get_instance(self, collection : list) -> aspose.cells.ICellsDataTable:
        '''Creates ICellsDataTable from given collection.
        
        :param collection: the collection to build table
        :returns: Instance of ICellsDataTable'''
        ...
    
    ...

class CellsException:
    '''The exception that is thrown when Aspose.Cells specified error occurs.'''
    
    @property
    def code(self) -> aspose.cells.ExceptionType:
        '''Represents custom exception code.'''
        ...
    
    ...

class CellsFactory:
    '''Utility for instantiating classes of Cells model.'''
    
    def create_style(self) -> aspose.cells.Style:
        '''Creates a new style.
        
        :returns: Returns a style object.'''
        ...
    
    ...

class CellsHelper:
    '''Provides helper functions.'''
    
    @overload
    @staticmethod
    def create_safe_sheet_name(name_proposal : str) -> str:
        '''Checks given sheet name and create a valid one when needed.
        If given sheet name conforms to the rules of excel sheet name, then return it.
        Otherwise string will be truncated if length exceeds the limit
        and invalid characters will be replaced with ' ', then return the rebuilt string value.
        
        :param name_proposal: sheet name to be used'''
        ...
    
    @overload
    @staticmethod
    def create_safe_sheet_name(name_proposal : strreplace_char : char) -> str:
        '''Checks given sheet name and create a valid one when needed.
        If given sheet name conforms to the rules of excel sheet name, then return it.
        Otherwise string will be truncated if length exceeds the limit
        and invalid characters will be replaced with given character, then return the rebuilt string value.
        
        :param name_proposal: sheet name to be used
        :param replace_char: character which will be used to replace invalid characters in given sheet name'''
        ...
    
    @staticmethod
    def get_text_width(text : strfont : aspose.cells.Font, scaling : float) -> float:
        '''Get width of text in unit of points.
        
        :param text: The text.
        :param font: The font of the text.
        :param scaling: The scaling of text.'''
        ...
    
    @staticmethod
    def get_version() -> str:
        '''Get the release version.
        
        :returns: The release version.'''
        ...
    
    @staticmethod
    def cell_name_to_index(cell_name : strrow : Any, column : Any):
        '''Gets the cell row and column indexes according to its name.
        
        :param cell_name: Name of cell.
        :param row: Output row index
        :param column: Output column index'''
        ...
    
    @staticmethod
    def cell_index_to_name(row : intcolumn : int) -> str:
        '''Gets cell name according to its row and column indexes.
        
        :param row: Row index.
        :param column: Column index.
        :returns: Name of cell.'''
        ...
    
    @staticmethod
    def column_index_to_name(column : int) -> str:
        '''Gets column name according to column index.
        
        :param column: Column index.
        :returns: Name of column.'''
        ...
    
    @staticmethod
    def column_name_to_index(column_name : str) -> int:
        '''Gets column index according to column name.
        
        :param column_name: Column name.
        :returns: Column index.'''
        ...
    
    @staticmethod
    def row_index_to_name(row : int) -> str:
        '''Gets row name according to row index.
        
        :param row: Row index.
        :returns: Name of row.'''
        ...
    
    @staticmethod
    def row_name_to_index(row_name : str) -> int:
        '''Gets row index according to row name.
        
        :param row_name: Row name.
        :returns: Row index.'''
        ...
    
    @staticmethod
    def convert_r1c1_formula_to_a1(r_1c1_formula : strrow : int, column : int) -> str:
        '''Converts the r1c1 formula of the cell to A1 formula.
        
        :param r_1c1_formula: The r1c1 formula.
        :param row: The row index of the cell.
        :param column: The column index of the cell.
        :returns: The A1 formula.'''
        ...
    
    @staticmethod
    def convert_a1_formula_to_r1c1(formula : strrow : int, column : int) -> str:
        '''Converts A1 formula of the cell to the r1c1 formula.
        
        :param formula: The A1 formula.
        :param row: The row index of the cell.
        :param column: The column index of the cell.
        :returns: The R1C1 formula.'''
        ...
    
    @staticmethod
    def get_date_time_from_double(double_value : floatdate1904 : bool) -> DateTime:
        '''Convert the double value to the date time value.
        
        :param double_value: The double value.
        :param date1904: Date 1904 system.'''
        ...
    
    @staticmethod
    def get_double_from_date_time(date_time : DateTimedate1904 : bool) -> float:
        '''Convert the date time to double value.
        
        :param date_time: The date time.
        :param date1904: Date 1904 system.'''
        ...
    
    @staticmethod
    def get_used_colors(workbook : aspose.cells.Workbook) -> aspose.pydrawing.Color[]:
        '''Gets all used colors in the workbook.
        
        :param workbook: The workbook object.
        :returns: The used colors.'''
        ...
    
    @staticmethod
    def add_add_in_function(function : strmin_count_of_parameters : int, max_count_of_parameters : int, paramers_type : List[aspose.cells.ParameterType], function_value_type : aspose.cells.ParameterType):
        '''Add addin function.
        
        :param function: The function name.
        :param min_count_of_parameters: Minimum number of parameters this function requires
        :param max_count_of_parameters: Maximum number of parameters this function allows.
        :param paramers_type: The excepted parameters type of the function
        :param function_value_type: The function value type.'''
        ...
    
    @staticmethod
    def merge_files(files : List[str]cached_file : str, dest_file : str):
        '''Merges some large xls files to a xls file.
        
        :param files: The files.
        :param cached_file: The cached file.
        :param dest_file: The dest file.'''
        ...
    
    @staticmethod
    def init_for_dot_net_core():
        '''Do the initialization for .NetCore programme.
        We suggest you to call this method for all .NetCore initialization first.
        For example:
        CellsHelper.InitForDotNetCore();
        Workbook wb = new Workbook();'''
        ...
    
    @classmethod
    @property
    def significant_digits(cls) -> int:
        ...
    
    @classmethod
    @significant_digits.setter
    def significant_digits(cls, value : int):
        ...
    
    @classmethod
    @property
    def dpi(cls) -> float:
        '''Gets the DPI of the machine.'''
        ...
    
    @classmethod
    @dpi.setter
    def dpi(cls, value : float):
        '''Gets the DPI of the machine.'''
        ...
    
    @classmethod
    @property
    def startup_path(cls) -> str:
        ...
    
    @classmethod
    @startup_path.setter
    def startup_path(cls, value : str):
        ...
    
    @classmethod
    @property
    def alt_start_path(cls) -> str:
        ...
    
    @classmethod
    @alt_start_path.setter
    def alt_start_path(cls, value : str):
        ...
    
    @classmethod
    @property
    def library_path(cls) -> str:
        ...
    
    @classmethod
    @library_path.setter
    def library_path(cls, value : str):
        ...
    
    @classmethod
    @property
    def custom_implementation_factory(cls) -> aspose.cells.CustomImplementationFactory:
        ...
    
    @classmethod
    @custom_implementation_factory.setter
    def custom_implementation_factory(cls, value : aspose.cells.CustomImplementationFactory):
        ...
    
    @classmethod
    @property
    def is_cloud_platform(cls) -> bool:
        ...
    
    @classmethod
    @is_cloud_platform.setter
    def is_cloud_platform(cls, value : bool):
        ...
    
    ...

class ColorFilter:
    '''Represents the color filter.'''
    
    def get_color(self, sheets : aspose.cells.WorksheetCollection) -> aspose.pydrawing.Color:
        ''''''
        ...
    
    @property
    def filter_by_fill_color(self) -> bool:
        ...
    
    @filter_by_fill_color.setter
    def filter_by_fill_color(self, value : bool):
        ...
    
    ...

class ColorScale:
    '''Describe the ColorScale conditional formatting rule.
    This conditional formatting rule creates a gradated color scale on the cells.'''
    
    @property
    def is_3_color_scale(self) -> bool:
        ...
    
    @is_3_color_scale.setter
    def is_3_color_scale(self, value : bool):
        ...
    
    @property
    def min_cfvo(self) -> aspose.cells.ConditionalFormattingValue:
        ...
    
    @property
    def mid_cfvo(self) -> aspose.cells.ConditionalFormattingValue:
        ...
    
    @property
    def max_cfvo(self) -> aspose.cells.ConditionalFormattingValue:
        ...
    
    @property
    def min_color(self) -> aspose.pydrawing.Color:
        ...
    
    @min_color.setter
    def min_color(self, value : aspose.pydrawing.Color):
        ...
    
    @property
    def mid_color(self) -> aspose.pydrawing.Color:
        ...
    
    @mid_color.setter
    def mid_color(self, value : aspose.pydrawing.Color):
        ...
    
    @property
    def max_color(self) -> aspose.pydrawing.Color:
        ...
    
    @max_color.setter
    def max_color(self, value : aspose.pydrawing.Color):
        ...
    
    ...

class Column:
    '''Represents a single column in a worksheet.'''
    
    def apply_style(self, style : aspose.cells.Style, flag : aspose.cells.StyleFlag):
        '''Applies formats for a whole column.
        
        :param style: The style object which will be applied.
        :param flag: Flags which indicates applied formatting properties.'''
        ...
    
    def get_style(self) -> aspose.cells.Style:
        '''Gets the style of this column.'''
        ...
    
    def set_style(self, style : aspose.cells.Style):
        '''Sets the style of this column.
        
        :param style: the style to be used as the default style for cells in this column.'''
        ...
    
    @property
    def index(self) -> int:
        '''Gets the index of this column.'''
        ...
    
    @property
    def width(self) -> float:
        '''Gets and sets the column width in unit of characters.'''
        ...
    
    @width.setter
    def width(self, value : float):
        '''Gets and sets the column width in unit of characters.'''
        ...
    
    @property
    def group_level(self) -> byte:
        ...
    
    @group_level.setter
    def group_level(self, value : byte):
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def has_custom_style(self) -> bool:
        ...
    
    @property
    def style(self) -> aspose.cells.Style:
        '''Gets the style of this column.'''
        ...
    
    @property
    def is_collapsed(self) -> bool:
        ...
    
    @is_collapsed.setter
    def is_collapsed(self, value : bool):
        ...
    
    ...

class ColumnCollection:
    '''Collection of the :py:class:`aspose.cells.Column` objects that represent the individual column(setting)s in a worksheet.
    The Column object only represents the settings such as column width, styles, .etc. for the whole column,
    has nothing to do with the fact that there are non-empty cells(data) or not in corresponding column.
    And the "Count" of this collection only represents the count Column objects that have been instantiated in this collection,
    has nothing to do with the fact that there are non-empty cells(data) or not in the worksheet.'''
    
    @overload
    def copy_to(self, array : List[aspose.cells.Column]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.Column], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.Column, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.Column, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Column) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Column, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Column, index : int, count : int) -> int:
        ...
    
    def get_by_index(self, index : int) -> aspose.cells.Column:
        '''Gets the column object by the index.
        
        :returns: Returns the column object.'''
        ...
    
    def get_column_by_index(self, index : int) -> aspose.cells.Column:
        '''Gets the :py:class:`aspose.cells.Column` object by the position in the list.
        
        :param index: The position in the list.
        :returns: Returns the column object.'''
        ...
    
    def binary_search(self, item : aspose.cells.Column) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class Comment:
    '''Encapsulates the object that represents a cell comment.'''
    
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Format some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the comment text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the comment text.
        
        :returns: All Characters objects'''
        ...
    
    @property
    def author(self) -> str:
        '''Gets and sets Name of the original comment author'''
        ...
    
    @author.setter
    def author(self, value : str):
        '''Gets and sets Name of the original comment author'''
        ...
    
    @property
    def comment_shape(self) -> aspose.cells.drawing.CommentShape:
        ...
    
    @property
    def row(self) -> int:
        '''Gets the row index of the comment.'''
        ...
    
    @property
    def column(self) -> int:
        '''Gets the column index of the comment.'''
        ...
    
    @property
    def is_threaded_comment(self) -> bool:
        ...
    
    @property
    def threaded_comments(self) -> aspose.cells.ThreadedCommentCollection:
        ...
    
    @property
    def note(self) -> str:
        '''Represents the content of comment.'''
        ...
    
    @note.setter
    def note(self, value : str):
        '''Represents the content of comment.'''
        ...
    
    @property
    def html_note(self) -> str:
        ...
    
    @html_note.setter
    def html_note(self, value : str):
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Gets the font of comment.'''
        ...
    
    @property
    def is_visible(self) -> bool:
        ...
    
    @is_visible.setter
    def is_visible(self, value : bool):
        ...
    
    @property
    def text_orientation_type(self) -> aspose.cells.TextOrientationType:
        ...
    
    @text_orientation_type.setter
    def text_orientation_type(self, value : aspose.cells.TextOrientationType):
        ...
    
    @property
    def text_horizontal_alignment(self) -> aspose.cells.TextAlignmentType:
        ...
    
    @text_horizontal_alignment.setter
    def text_horizontal_alignment(self, value : aspose.cells.TextAlignmentType):
        ...
    
    @property
    def text_vertical_alignment(self) -> aspose.cells.TextAlignmentType:
        ...
    
    @text_vertical_alignment.setter
    def text_vertical_alignment(self, value : aspose.cells.TextAlignmentType):
        ...
    
    @property
    def auto_size(self) -> bool:
        ...
    
    @auto_size.setter
    def auto_size(self, value : bool):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of the comment, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of the comment, in unit of pixels.'''
        ...
    
    @property
    def height(self) -> int:
        '''Represents the Height of the comment, in unit of pixels.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the Height of the comment, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    ...

class CommentCollection:
    '''Encapsulates a collection of :py:class:`aspose.cells.Comment` objects.'''
    
    @overload
    def add_threaded_comment(self, row : int, column : int, text : str, author : aspose.cells.ThreadedCommentAuthor) -> int:
        '''Adds a threaded comment.
        
        :param row: Cell row index.
        :param column: Cell column index.
        :param text: The text of the comment
        :param author: The user of this threaded comment.
        :returns: :py:class:`aspose.cells.ThreadedComment` object index.'''
        ...
    
    @overload
    def add_threaded_comment(self, cell_name : str, text : str, author : aspose.cells.ThreadedCommentAuthor) -> int:
        '''Adds a threaded comment.
        
        :param cell_name: The name of the cell.
        :param text: The text of the comment
        :param author: The user of this threaded comment.
        :returns: :py:class:`aspose.cells.ThreadedComment` object index.'''
        ...
    
    @overload
    def get_threaded_comments(self, row : int, column : int) -> aspose.cells.ThreadedCommentCollection:
        '''Gets the threaded comments by row and column index.
        
        :param row: The row index.
        :param column: The column index.'''
        ...
    
    @overload
    def get_threaded_comments(self, cell_name : str) -> aspose.cells.ThreadedCommentCollection:
        '''Gets the threaded comments by cell name.
        
        :param cell_name: The name of the cell.'''
        ...
    
    @overload
    def add(self, row : int, column : int) -> int:
        '''Adds a comment to the collection.
        
        :param row: Cell row index.
        :param column: Cell column index.
        :returns: :py:class:`aspose.cells.Comment` object index.'''
        ...
    
    @overload
    def add(self, cell_name : str) -> int:
        '''Adds a comment to the collection.
        
        :param cell_name: Cell name.
        :returns: :py:class:`aspose.cells.Comment` object index.'''
        ...
    
    @overload
    def remove_at(self, cell_name : str):
        '''Removes the comment of the specific cell.
        
        :param cell_name: The name of cell which contains a comment.'''
        ...
    
    @overload
    def remove_at(self, row : int, column : int):
        '''Removes the comment of the specific cell.
        
        :param row: The row index.
        :param column: the column index.'''
        ...
    
    @overload
    def copy_to(self, array : List[aspose.cells.Comment]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.Comment], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.Comment, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.Comment, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Comment) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Comment, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Comment, index : int, count : int) -> int:
        ...
    
    def binary_search(self, item : aspose.cells.Comment) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class ConditionalFormattingCollection:
    '''Encapsulates a collection of :py:class:`aspose.cells.FormatCondition` objects.'''
    
    @overload
    def copy_to(self, array : List[aspose.cells.FormatConditionCollection]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.FormatConditionCollection], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.FormatConditionCollection, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.FormatConditionCollection, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.FormatConditionCollection) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.FormatConditionCollection, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.FormatConditionCollection, index : int, count : int) -> int:
        ...
    
    def remove_area(self, start_row : int, start_column : int, total_rows : int, total_columns : int):
        '''Remove all conditional formatting in the range.
        
        :param start_row: The start row of the range.
        :param start_column: The start column of the range.
        :param total_rows: The number of rows of the range.
        :param total_columns: The number of columns of the range.'''
        ...
    
    def add(self) -> int:
        '''Adds a FormatConditions to the collection.
        
        :returns: FormatConditions object index.'''
        ...
    
    def binary_search(self, item : aspose.cells.FormatConditionCollection) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class ConditionalFormattingIcon:
    '''Represents  the custom  icon of conditional formatting rule.'''
    
    @staticmethod
    def get_icon_image_data(type : aspose.cells.IconSetTypeindex : int) -> bytes:
        '''Get the icon set data
        
        :param type: icon's type
        :param index: icon's index'''
        ...
    
    def get_image_data(self, cell : aspose.cells.Cell) -> bytes:
        '''Gets the image data with the setting of cell.
        
        :param cell: The setting of cell.
        :returns: Returns the image data of icon.'''
        ...
    
    @property
    def image_data(self) -> bytes:
        ...
    
    @property
    def type(self) -> aspose.cells.IconSetType:
        '''Gets and sets the icon set type.'''
        ...
    
    @type.setter
    def type(self, value : aspose.cells.IconSetType):
        '''Gets and sets the icon set type.'''
        ...
    
    @property
    def index(self) -> int:
        '''Gets and sets the icon's index in the icon set.'''
        ...
    
    @index.setter
    def index(self, value : int):
        '''Gets and sets the icon's index in the icon set.'''
        ...
    
    ...

class ConditionalFormattingIconCollection:
    '''Represents  a collection of :py:class:`aspose.cells.ConditionalFormattingIcon` objects.'''
    
    @overload
    def add(self, type : aspose.cells.IconSetType, index : int) -> int:
        '''Adds :py:class:`aspose.cells.ConditionalFormattingIcon` object.
        
        :param type: The value type.
        :param index: The Index.
        :returns: Returns the index of new object in the list.'''
        ...
    
    @overload
    def add(self, cficon : aspose.cells.ConditionalFormattingIcon) -> int:
        '''Adds :py:class:`aspose.cells.ConditionalFormattingIcon` object.
        
        :param cficon: Returns the index of new object in the list.'''
        ...
    
    @overload
    def copy_to(self, array : List[aspose.cells.ConditionalFormattingIcon]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.ConditionalFormattingIcon], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.ConditionalFormattingIcon, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.ConditionalFormattingIcon, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.ConditionalFormattingIcon) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.ConditionalFormattingIcon, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.ConditionalFormattingIcon, index : int, count : int) -> int:
        ...
    
    def binary_search(self, item : aspose.cells.ConditionalFormattingIcon) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class ConditionalFormattingResult:
    '''Represents the result of conditional formatting which applies to a cell.'''
    
    @property
    def conditional_style(self) -> aspose.cells.Style:
        ...
    
    @property
    def conditional_formatting_icon(self) -> aspose.cells.ConditionalFormattingIcon:
        ...
    
    @property
    def conditional_formatting_data_bar(self) -> aspose.cells.DataBar:
        ...
    
    @property
    def conditional_formatting_color_scale(self) -> aspose.cells.ColorScale:
        ...
    
    @property
    def color_scale_result(self) -> aspose.pydrawing.Color:
        ...
    
    ...

class ConditionalFormattingValue:
    '''Describes the values of the interpolation points in a gradient scale, dataBar or iconSet.'''
    
    @property
    def value(self) -> any:
        '''Get or set the value of this conditional formatting value object.
        It should be used in conjunction with Type.'''
        ...
    
    @value.setter
    def value(self, value : any):
        '''Get or set the value of this conditional formatting value object.
        It should be used in conjunction with Type.'''
        ...
    
    @property
    def type(self) -> aspose.cells.FormatConditionValueType:
        '''Get or set the type of this conditional formatting value object.
        Setting the type to FormatConditionValueType.Min or FormatConditionValueType.Max
        will auto set "Value" to null.'''
        ...
    
    @type.setter
    def type(self, value : aspose.cells.FormatConditionValueType):
        '''Get or set the type of this conditional formatting value object.
        Setting the type to FormatConditionValueType.Min or FormatConditionValueType.Max
        will auto set "Value" to null.'''
        ...
    
    @property
    def is_gte(self) -> bool:
        ...
    
    @is_gte.setter
    def is_gte(self, value : bool):
        ...
    
    ...

class ConditionalFormattingValueCollection:
    '''Describes a collection of CFValueObject.
    Use only for icon sets.'''
    
    @overload
    def copy_to(self, array : List[aspose.cells.ConditionalFormattingValue]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.ConditionalFormattingValue], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.ConditionalFormattingValue, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.ConditionalFormattingValue, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.ConditionalFormattingValue) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.ConditionalFormattingValue, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.ConditionalFormattingValue, index : int, count : int) -> int:
        ...
    
    def add(self, type : aspose.cells.FormatConditionValueType, value : str) -> int:
        '''Adds :py:class:`aspose.cells.ConditionalFormattingValue` object.
        
        :param type: The value type.
        :param value: The value.
        :returns: Returns the index of new object in the list.'''
        ...
    
    def binary_search(self, item : aspose.cells.ConditionalFormattingValue) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class CopyOptions:
    '''Represents the copy options.'''
    
    @property
    def keep_macros(self) -> bool:
        ...
    
    @keep_macros.setter
    def keep_macros(self, value : bool):
        ...
    
    @property
    def extend_to_adjacent_range(self) -> bool:
        ...
    
    @extend_to_adjacent_range.setter
    def extend_to_adjacent_range(self, value : bool):
        ...
    
    @property
    def copy_names(self) -> bool:
        ...
    
    @copy_names.setter
    def copy_names(self, value : bool):
        ...
    
    @property
    def copy_invalid_formulas_as_values(self) -> bool:
        ...
    
    @copy_invalid_formulas_as_values.setter
    def copy_invalid_formulas_as_values(self, value : bool):
        ...
    
    @property
    def column_character_width(self) -> bool:
        ...
    
    @column_character_width.setter
    def column_character_width(self, value : bool):
        ...
    
    @property
    def refer_to_sheet_with_same_name(self) -> bool:
        ...
    
    @refer_to_sheet_with_same_name.setter
    def refer_to_sheet_with_same_name(self, value : bool):
        ...
    
    @property
    def refer_to_destination_sheet(self) -> bool:
        ...
    
    @refer_to_destination_sheet.setter
    def refer_to_destination_sheet(self, value : bool):
        ...
    
    ...

class CustomFilter:
    '''Represents the custom filter.'''
    
    def set_criteria(self, filter_operator : aspose.cells.FilterOperatorType, criteria : any):
        '''Sets the filter criteria.
        
        :param filter_operator: filter operator type
        :param criteria: filter criteria value'''
        ...
    
    @property
    def filter_operator_type(self) -> aspose.cells.FilterOperatorType:
        ...
    
    @filter_operator_type.setter
    def filter_operator_type(self, value : aspose.cells.FilterOperatorType):
        ...
    
    @property
    def criteria(self) -> any:
        '''Gets and sets the criteria.'''
        ...
    
    @criteria.setter
    def criteria(self, value : any):
        '''Gets and sets the criteria.'''
        ...
    
    ...

class CustomFilterCollection:
    '''Represents the custom filters.'''
    
    @overload
    def copy_to(self, array : List[aspose.cells.CustomFilter]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.CustomFilter], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.CustomFilter, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.CustomFilter, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.CustomFilter) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.CustomFilter, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.CustomFilter, index : int, count : int) -> int:
        ...
    
    def binary_search(self, item : aspose.cells.CustomFilter) -> int:
        ...
    
    @property
    def both(self) -> bool:
        ...
    
    @both.setter
    def both(self, value : bool):
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class CustomImplementationFactory:
    '''Factory to create some instances which may be re-implemented by user for special purpose.'''
    
    ...

class DataBar:
    '''Describe the DataBar conditional formatting rule.
    This conditional formatting rule displays a gradated
    data bar in the range of cells.'''
    
    def to_image(self, cell : aspose.cells.Cell, img_opts : aspose.cells.rendering.ImageOrPrintOptions) -> bytes:
        '''Render data bar in cell to image byte array.
        
        :param cell: Indicate the data bar in which cell to be rendered
        :param img_opts: ImageOrPrintOptions contains some property of output image'''
        ...
    
    @property
    def axis_color(self) -> aspose.pydrawing.Color:
        ...
    
    @axis_color.setter
    def axis_color(self, value : aspose.pydrawing.Color):
        ...
    
    @property
    def axis_position(self) -> aspose.cells.DataBarAxisPosition:
        ...
    
    @axis_position.setter
    def axis_position(self, value : aspose.cells.DataBarAxisPosition):
        ...
    
    @property
    def bar_fill_type(self) -> aspose.cells.DataBarFillType:
        ...
    
    @bar_fill_type.setter
    def bar_fill_type(self, value : aspose.cells.DataBarFillType):
        ...
    
    @property
    def direction(self) -> aspose.cells.TextDirectionType:
        '''Gets the direction the databar is displayed.'''
        ...
    
    @direction.setter
    def direction(self, value : aspose.cells.TextDirectionType):
        '''Sets the direction the databar is displayed.'''
        ...
    
    @property
    def bar_border(self) -> aspose.cells.DataBarBorder:
        ...
    
    @property
    def negative_bar_format(self) -> aspose.cells.NegativeBarFormat:
        ...
    
    @property
    def min_cfvo(self) -> aspose.cells.ConditionalFormattingValue:
        ...
    
    @property
    def max_cfvo(self) -> aspose.cells.ConditionalFormattingValue:
        ...
    
    @property
    def color(self) -> aspose.pydrawing.Color:
        '''Get or set this DataBar's Color.'''
        ...
    
    @color.setter
    def color(self, value : aspose.pydrawing.Color):
        '''Get or set this DataBar's Color.'''
        ...
    
    @property
    def min_length(self) -> int:
        ...
    
    @min_length.setter
    def min_length(self, value : int):
        ...
    
    @property
    def max_length(self) -> int:
        ...
    
    @max_length.setter
    def max_length(self, value : int):
        ...
    
    @property
    def show_value(self) -> bool:
        ...
    
    @show_value.setter
    def show_value(self, value : bool):
        ...
    
    ...

class DataBarBorder:
    '''Represents the border of the data bars specified by a conditional formatting rule.'''
    
    @property
    def color(self) -> aspose.pydrawing.Color:
        '''Gets the border's color of data bars specified by a conditional formatting rule.'''
        ...
    
    @color.setter
    def color(self, value : aspose.pydrawing.Color):
        '''Sets the border's color of data bars specified by a conditional formatting rule.'''
        ...
    
    @property
    def type(self) -> aspose.cells.DataBarBorderType:
        '''Gets the border's type of data bars specified by a conditional formatting rule.'''
        ...
    
    @type.setter
    def type(self, value : aspose.cells.DataBarBorderType):
        '''Sets the border's type of data bars specified by a conditional formatting rule.'''
        ...
    
    ...

class DataSorter:
    '''Summary description for DataSorter.'''
    
    @overload
    def add_key(self, key : int, order : aspose.cells.SortOrder):
        '''Adds sorted column index and sort order.
        
        :param key: The sorted column index(absolute position, column A is 0, B is 1, ...)
        :param order: The sort order'''
        ...
    
    @overload
    def add_key(self, key : int, order : aspose.cells.SortOrder, custom_list : str):
        '''Adds sorted column index and sort order with custom sort list.
        
        :param key: The sorted column index(absolute position, column A is 0, B is 1, ...)
        :param order: The sort order.
        :param custom_list: The custom sort list.'''
        ...
    
    @overload
    def add_key(self, key : int, type : aspose.cells.SortOnType, order : aspose.cells.SortOrder, custom_list : any):
        '''Adds sorted column index and sort order with custom sort list.
        
        :param key: The sorted column index(absolute position, column A is 0, B is 1, ...)
        :param type: The sorted value type.
        :param order: The sort order.
        :param custom_list: The custom sort list.'''
        ...
    
    @overload
    def add_key(self, key : int, order : aspose.cells.SortOrder, custom_list : List[str]):
        '''Adds sorted column index and sort order with custom sort list.
        
        :param key: The sorted column index(absolute position, column A is 0, B is 1, ...)
        :param order: The sort order.
        :param custom_list: The custom sort list.'''
        ...
    
    @overload
    def sort(self, cells : aspose.cells.Cells, start_row : int, start_column : int, end_row : int, end_column : int) -> List[int]:
        '''Sorts the data of the area.
        
        :param cells: The cells contains the data area.
        :param start_row: The start row of the area.
        :param start_column: The start column of the area.
        :param end_row: The end row of the area.
        :param end_column: The end column of the area.
        :returns: the original indices(absolute position, for example, column A is 0, B is 1, ...) of the sorted rows/columns.
        If no rows/columns needs to be moved by this sorting operation, null will be returned.'''
        ...
    
    @overload
    def sort(self, cells : aspose.cells.Cells, area : aspose.cells.CellArea) -> List[int]:
        '''Sort the data of the area.
        
        :param cells: The cells contains the data area.
        :param area: The area needed to sort
        :returns: the original indices(absolute position, for example, column A is 0, B is 1, ...) of the sorted rows/columns.
        If no rows/columns needs to be moved by this sorting operation, null will be returned.'''
        ...
    
    @overload
    def sort(self) -> List[int]:
        '''Sort the data in the range.
        
        :returns: the original indices(absolute position, for example, column A is 0, B is 1, ...) of the sorted rows/columns.
        If no rows/columns needs to be moved by this sorting operation, null will be returned.'''
        ...
    
    def clear(self):
        '''Clear all settings.'''
        ...
    
    @property
    def keys(self) -> aspose.cells.DataSorterKeyCollection:
        '''Gets the key list of data sorter.'''
        ...
    
    @property
    def has_headers(self) -> bool:
        ...
    
    @has_headers.setter
    def has_headers(self, value : bool):
        ...
    
    @property
    def key1(self) -> int:
        '''Represents first sorted column index(absolute position, column A is 0, B is 1, ...).'''
        ...
    
    @key1.setter
    def key1(self, value : int):
        '''Represents first sorted column index(absolute position, column A is 0, B is 1, ...).'''
        ...
    
    @property
    def order1(self) -> aspose.cells.SortOrder:
        '''Represents sort order of the first key.'''
        ...
    
    @order1.setter
    def order1(self, value : aspose.cells.SortOrder):
        '''Represents sort order of the first key.'''
        ...
    
    @property
    def key2(self) -> int:
        '''Represents second sorted column index(absolute position, column A is 0, B is 1, ...).'''
        ...
    
    @key2.setter
    def key2(self, value : int):
        '''Represents second sorted column index(absolute position, column A is 0, B is 1, ...).'''
        ...
    
    @property
    def order2(self) -> aspose.cells.SortOrder:
        '''Represents sort order of the second key.'''
        ...
    
    @order2.setter
    def order2(self, value : aspose.cells.SortOrder):
        '''Represents sort order of the second key.'''
        ...
    
    @property
    def key3(self) -> int:
        '''Represents third sorted column index(absolute position, column A is 0, B is 1, ...).'''
        ...
    
    @key3.setter
    def key3(self, value : int):
        '''Represents third sorted column index(absolute position, column A is 0, B is 1, ...).'''
        ...
    
    @property
    def order3(self) -> aspose.cells.SortOrder:
        '''Represents sort order of the third key.'''
        ...
    
    @order3.setter
    def order3(self, value : aspose.cells.SortOrder):
        '''Represents sort order of the third key.'''
        ...
    
    @property
    def sort_left_to_right(self) -> bool:
        ...
    
    @sort_left_to_right.setter
    def sort_left_to_right(self, value : bool):
        ...
    
    @property
    def case_sensitive(self) -> bool:
        ...
    
    @case_sensitive.setter
    def case_sensitive(self, value : bool):
        ...
    
    @property
    def sort_as_number(self) -> bool:
        ...
    
    @sort_as_number.setter
    def sort_as_number(self, value : bool):
        ...
    
    ...

class DataSorterKey:
    '''Represents the key of the data sorter.'''
    
    @property
    def order(self) -> aspose.cells.SortOrder:
        '''Indicates the order of sorting.'''
        ...
    
    @property
    def index(self) -> int:
        '''Gets the sorted column index(absolute position, column A is 0, B is 1, ...).'''
        ...
    
    @property
    def type(self) -> aspose.cells.SortOnType:
        '''Represents the type of sorting.'''
        ...
    
    @property
    def icon_set_type(self) -> aspose.cells.IconSetType:
        ...
    
    @property
    def icon_id(self) -> int:
        ...
    
    @property
    def color(self) -> aspose.pydrawing.Color:
        '''Gets the sorted color.'''
        ...
    
    ...

class DataSorterKeyCollection:
    '''Represents the key list of data sorter.'''
    
    @overload
    def copy_to(self, array : List[aspose.cells.DataSorterKey]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.DataSorterKey], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.DataSorterKey, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.DataSorterKey, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.DataSorterKey) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.DataSorterKey, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.DataSorterKey, index : int, count : int) -> int:
        ...
    
    def binary_search(self, item : aspose.cells.DataSorterKey) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class DateTimeGroupItem:
    '''Represents the datetime's group setting.'''
    
    @property
    def min_value(self) -> DateTime:
        ...
    
    @property
    def date_time_grouping_type(self) -> aspose.cells.DateTimeGroupingType:
        ...
    
    @date_time_grouping_type.setter
    def date_time_grouping_type(self, value : aspose.cells.DateTimeGroupingType):
        ...
    
    @property
    def year(self) -> int:
        '''Gets and sets the year of the grouped date time.'''
        ...
    
    @year.setter
    def year(self, value : int):
        '''Gets and sets the year of the grouped date time.'''
        ...
    
    @property
    def month(self) -> int:
        '''Gets and sets the month of the grouped date time.'''
        ...
    
    @month.setter
    def month(self, value : int):
        '''Gets and sets the month of the grouped date time.'''
        ...
    
    @property
    def day(self) -> int:
        '''Gets and sets the day of the grouped date time.'''
        ...
    
    @day.setter
    def day(self, value : int):
        '''Gets and sets the day of the grouped date time.'''
        ...
    
    @property
    def hour(self) -> int:
        '''Gets and sets the hour of the grouped date time.'''
        ...
    
    @hour.setter
    def hour(self, value : int):
        '''Gets and sets the hour of the grouped date time.'''
        ...
    
    @property
    def minute(self) -> int:
        '''Gets and sets the minute of the grouped date time.'''
        ...
    
    @minute.setter
    def minute(self, value : int):
        '''Gets and sets the minute of the grouped date time.'''
        ...
    
    @property
    def second(self) -> int:
        '''Gets and sets the second of the grouped date time.'''
        ...
    
    @second.setter
    def second(self, value : int):
        '''Gets and sets the second of the grouped date time.'''
        ...
    
    ...

class DefaultStyleSettings:
    '''Settings for the default values of workbook's style properties.'''
    
    @property
    def font_name(self) -> str:
        ...
    
    @font_name.setter
    def font_name(self, value : str):
        ...
    
    @property
    def font_size(self) -> float:
        ...
    
    @font_size.setter
    def font_size(self, value : float):
        ...
    
    @property
    def horizontal_alignment(self) -> aspose.cells.TextAlignmentType:
        ...
    
    @horizontal_alignment.setter
    def horizontal_alignment(self, value : aspose.cells.TextAlignmentType):
        ...
    
    @property
    def vertical_alignment(self) -> aspose.cells.TextAlignmentType:
        ...
    
    @vertical_alignment.setter
    def vertical_alignment(self, value : aspose.cells.TextAlignmentType):
        ...
    
    ...

class DeleteOptions:
    '''Represents the setting of deleting rows/columns.'''
    
    @property
    def update_reference(self) -> bool:
        ...
    
    @update_reference.setter
    def update_reference(self, value : bool):
        ...
    
    ...

class DifSaveOptions(SaveOptions):
    '''Represents the options of saving dif file.'''
    
    @property
    def save_format(self) -> aspose.cells.SaveFormat:
        ...
    
    @property
    def clear_data(self) -> bool:
        ...
    
    @clear_data.setter
    def clear_data(self, value : bool):
        ...
    
    @property
    def cached_file_folder(self) -> str:
        ...
    
    @cached_file_folder.setter
    def cached_file_folder(self, value : str):
        ...
    
    @property
    def validate_merged_areas(self) -> bool:
        ...
    
    @validate_merged_areas.setter
    def validate_merged_areas(self, value : bool):
        ...
    
    @property
    def merge_areas(self) -> bool:
        ...
    
    @merge_areas.setter
    def merge_areas(self, value : bool):
        ...
    
    @property
    def create_directory(self) -> bool:
        ...
    
    @create_directory.setter
    def create_directory(self, value : bool):
        ...
    
    @property
    def sort_names(self) -> bool:
        ...
    
    @sort_names.setter
    def sort_names(self, value : bool):
        ...
    
    @property
    def sort_external_names(self) -> bool:
        ...
    
    @sort_external_names.setter
    def sort_external_names(self, value : bool):
        ...
    
    @property
    def refresh_chart_cache(self) -> bool:
        ...
    
    @refresh_chart_cache.setter
    def refresh_chart_cache(self, value : bool):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def update_smart_art(self) -> bool:
        ...
    
    @update_smart_art.setter
    def update_smart_art(self, value : bool):
        ...
    
    ...

class DocxSaveOptions(PaginatedSaveOptions):
    '''Represents options of saving .docx file.'''
    
    @property
    def save_format(self) -> aspose.cells.SaveFormat:
        ...
    
    @property
    def clear_data(self) -> bool:
        ...
    
    @clear_data.setter
    def clear_data(self, value : bool):
        ...
    
    @property
    def cached_file_folder(self) -> str:
        ...
    
    @cached_file_folder.setter
    def cached_file_folder(self, value : str):
        ...
    
    @property
    def validate_merged_areas(self) -> bool:
        ...
    
    @validate_merged_areas.setter
    def validate_merged_areas(self, value : bool):
        ...
    
    @property
    def merge_areas(self) -> bool:
        ...
    
    @merge_areas.setter
    def merge_areas(self, value : bool):
        ...
    
    @property
    def create_directory(self) -> bool:
        ...
    
    @create_directory.setter
    def create_directory(self, value : bool):
        ...
    
    @property
    def sort_names(self) -> bool:
        ...
    
    @sort_names.setter
    def sort_names(self, value : bool):
        ...
    
    @property
    def sort_external_names(self) -> bool:
        ...
    
    @sort_external_names.setter
    def sort_external_names(self, value : bool):
        ...
    
    @property
    def refresh_chart_cache(self) -> bool:
        ...
    
    @refresh_chart_cache.setter
    def refresh_chart_cache(self, value : bool):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def update_smart_art(self) -> bool:
        ...
    
    @update_smart_art.setter
    def update_smart_art(self, value : bool):
        ...
    
    @property
    def default_font(self) -> str:
        ...
    
    @default_font.setter
    def default_font(self, value : str):
        ...
    
    @property
    def check_workbook_default_font(self) -> bool:
        ...
    
    @check_workbook_default_font.setter
    def check_workbook_default_font(self, value : bool):
        ...
    
    @property
    def check_font_compatibility(self) -> bool:
        ...
    
    @check_font_compatibility.setter
    def check_font_compatibility(self, value : bool):
        ...
    
    @property
    def is_font_substitution_char_granularity(self) -> bool:
        ...
    
    @is_font_substitution_char_granularity.setter
    def is_font_substitution_char_granularity(self, value : bool):
        ...
    
    @property
    def one_page_per_sheet(self) -> bool:
        ...
    
    @one_page_per_sheet.setter
    def one_page_per_sheet(self, value : bool):
        ...
    
    @property
    def all_columns_in_one_page_per_sheet(self) -> bool:
        ...
    
    @all_columns_in_one_page_per_sheet.setter
    def all_columns_in_one_page_per_sheet(self, value : bool):
        ...
    
    @property
    def ignore_error(self) -> bool:
        ...
    
    @ignore_error.setter
    def ignore_error(self, value : bool):
        ...
    
    @property
    def output_blank_page_when_nothing_to_print(self) -> bool:
        ...
    
    @output_blank_page_when_nothing_to_print.setter
    def output_blank_page_when_nothing_to_print(self, value : bool):
        ...
    
    @property
    def page_index(self) -> int:
        ...
    
    @page_index.setter
    def page_index(self, value : int):
        ...
    
    @property
    def page_count(self) -> int:
        ...
    
    @page_count.setter
    def page_count(self, value : int):
        ...
    
    @property
    def printing_page_type(self) -> aspose.cells.PrintingPageType:
        ...
    
    @printing_page_type.setter
    def printing_page_type(self, value : aspose.cells.PrintingPageType):
        ...
    
    @property
    def gridline_type(self) -> aspose.cells.GridlineType:
        ...
    
    @gridline_type.setter
    def gridline_type(self, value : aspose.cells.GridlineType):
        ...
    
    @property
    def text_cross_type(self) -> aspose.cells.TextCrossType:
        ...
    
    @text_cross_type.setter
    def text_cross_type(self, value : aspose.cells.TextCrossType):
        ...
    
    @property
    def default_edit_language(self) -> aspose.cells.DefaultEditLanguage:
        ...
    
    @default_edit_language.setter
    def default_edit_language(self, value : aspose.cells.DefaultEditLanguage):
        ...
    
    @property
    def sheet_set(self) -> aspose.cells.rendering.SheetSet:
        ...
    
    @sheet_set.setter
    def sheet_set(self, value : aspose.cells.rendering.SheetSet):
        ...
    
    @property
    def draw_object_event_handler(self) -> aspose.cells.rendering.DrawObjectEventHandler:
        ...
    
    @draw_object_event_handler.setter
    def draw_object_event_handler(self, value : aspose.cells.rendering.DrawObjectEventHandler):
        ...
    
    @property
    def page_saving_callback(self) -> aspose.cells.rendering.IPageSavingCallback:
        ...
    
    @page_saving_callback.setter
    def page_saving_callback(self, value : aspose.cells.rendering.IPageSavingCallback):
        ...
    
    ...

class DxfCollection:
    '''Represents the master differential formatting records.'''
    
    @overload
    def copy_to(self, array : List[aspose.cells.Style]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.Style], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.Style, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.Style, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Style) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Style, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Style, index : int, count : int) -> int:
        ...
    
    def binary_search(self, item : aspose.cells.Style) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class DynamicFilter:
    '''Represents the dynamic filter.'''
    
    @property
    def dynamic_filter_type(self) -> aspose.cells.DynamicFilterType:
        ...
    
    @dynamic_filter_type.setter
    def dynamic_filter_type(self, value : aspose.cells.DynamicFilterType):
        ...
    
    @property
    def value(self) -> any:
        '''Gets and sets the dynamic filter value.'''
        ...
    
    @value.setter
    def value(self, value : any):
        '''Gets and sets the dynamic filter value.'''
        ...
    
    @property
    def max_value(self) -> any:
        ...
    
    @max_value.setter
    def max_value(self, value : any):
        ...
    
    ...

class ErrorCheckOption:
    '''Error check setting applied on certain ranges.'''
    
    def is_error_check(self, error_check_type : aspose.cells.ErrorCheckType) -> bool:
        '''Checks whether given error type will be checked.
        
        :param error_check_type: error type can be checked
        :returns: return true if given error type will be checked(green triangle will be shown for cell if the check failed).'''
        ...
    
    def set_error_check(self, error_check_type : aspose.cells.ErrorCheckType, is_check : bool):
        '''Sets whether given error type will be checked.
        
        :param error_check_type: error type can be checked.
        :param is_check: true if given error type needs to be checked(green triangle will be shown for cell if the check failed).'''
        ...
    
    def get_count_of_range(self) -> int:
        '''Gets the count of ranges that influenced by this setting.
        
        :returns: the count of ranges that influenced by this setting.'''
        ...
    
    def add_range(self, ca : aspose.cells.CellArea) -> int:
        '''Adds one influenced range by this setting.
        
        :param ca: the range to be added.
        :returns: the index of the added range in the range list of this setting.'''
        ...
    
    def get_range(self, index : int) -> aspose.cells.CellArea:
        '''Gets the influenced range of this setting by given index.
        
        :param index: the index of range
        :returns: return influenced range at given index.'''
        ...
    
    def remove_range(self, index : int):
        '''Removes one range by given index.
        
        :param index: the index of the range to be removed.'''
        ...
    
    ...

class ErrorCheckOptionCollection:
    '''Represents all error check option.'''
    
    @overload
    def copy_to(self, array : List[aspose.cells.ErrorCheckOption]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.ErrorCheckOption], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.ErrorCheckOption, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.ErrorCheckOption, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.ErrorCheckOption) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.ErrorCheckOption, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.ErrorCheckOption, index : int, count : int) -> int:
        ...
    
    def add(self) -> int:
        '''Add an error check option.'''
        ...
    
    def binary_search(self, item : aspose.cells.ErrorCheckOption) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class ExportObjectEvent:
    '''The event triggered when exporting an object, such as Picture.'''
    
    def get_source(self) -> any:
        '''Gets the object to be exported.
        
        :returns: the object to be exported.'''
        ...
    
    ...

class ExportTableOptions:
    '''Represents all export table options.'''
    
    @property
    def export_column_name(self) -> bool:
        ...
    
    @export_column_name.setter
    def export_column_name(self, value : bool):
        ...
    
    @property
    def skip_error_value(self) -> bool:
        ...
    
    @skip_error_value.setter
    def skip_error_value(self, value : bool):
        ...
    
    @property
    def plot_visible_cells(self) -> bool:
        ...
    
    @plot_visible_cells.setter
    def plot_visible_cells(self, value : bool):
        ...
    
    @property
    def plot_visible_rows(self) -> bool:
        ...
    
    @plot_visible_rows.setter
    def plot_visible_rows(self, value : bool):
        ...
    
    @property
    def plot_visible_columns(self) -> bool:
        ...
    
    @plot_visible_columns.setter
    def plot_visible_columns(self, value : bool):
        ...
    
    @property
    def export_as_string(self) -> bool:
        ...
    
    @export_as_string.setter
    def export_as_string(self, value : bool):
        ...
    
    @property
    def export_as_html_string(self) -> bool:
        ...
    
    @export_as_html_string.setter
    def export_as_html_string(self, value : bool):
        ...
    
    @property
    def format_strategy(self) -> aspose.cells.CellValueFormatStrategy:
        ...
    
    @format_strategy.setter
    def format_strategy(self, value : aspose.cells.CellValueFormatStrategy):
        ...
    
    @property
    def check_mixed_value_type(self) -> bool:
        ...
    
    @check_mixed_value_type.setter
    def check_mixed_value_type(self, value : bool):
        ...
    
    @property
    def is_vertical(self) -> bool:
        ...
    
    @is_vertical.setter
    def is_vertical(self, value : bool):
        ...
    
    @property
    def indexes(self) -> List[int]:
        '''The indexes of columns/rows which should be exported out.'''
        ...
    
    @indexes.setter
    def indexes(self, value : List[int]):
        '''The indexes of columns/rows which should be exported out.'''
        ...
    
    @property
    def rename_strategy(self) -> aspose.cells.RenameStrategy:
        ...
    
    @rename_strategy.setter
    def rename_strategy(self, value : aspose.cells.RenameStrategy):
        ...
    
    ...

class ExternalLink:
    '''Represents an external link in a workbook.'''
    
    def add_external_name(self, text : str, refer_to : str):
        '''Adds an external name.
        
        :param text: The text of the external name.
        If the external name belongs to a worksheet, the text should be as Sheet1!Text.
        :param refer_to: The referTo of the external name. It must be a cell or the range.'''
        ...
    
    @property
    def type(self) -> aspose.cells.ExternalLinkType:
        '''Gets the type of external link.'''
        ...
    
    @property
    def original_data_source(self) -> str:
        ...
    
    @original_data_source.setter
    def original_data_source(self, value : str):
        ...
    
    @property
    def data_source(self) -> str:
        ...
    
    @data_source.setter
    def data_source(self, value : str):
        ...
    
    @property
    def is_referred(self) -> bool:
        ...
    
    @property
    def is_visible(self) -> bool:
        ...
    
    ...

class ExternalLinkCollection:
    '''Represents external links collection in a workbook.'''
    
    @overload
    def add(self, file_name : str, sheet_names : List[str]) -> int:
        '''Adds an external link.
        
        :param file_name: The external file name.
        :param sheet_names: All sheet names of the external file.
        :returns: The position of the external name in this list.'''
        ...
    
    @overload
    def add(self, directory_type : aspose.cells.DirectoryType, file_name : str, sheet_names : List[str]) -> int:
        '''Add an external link .
        
        :param directory_type: The directory type of the file name.
        :param file_name: the file name.
        :param sheet_names: All sheet names of the external file.
        :returns: The position of the external name in this list.'''
        ...
    
    @overload
    def clear(self):
        '''Removes all external links.'''
        ...
    
    @overload
    def clear(self, update_references_as_local : bool):
        '''Removes all external links.
        
        :param update_references_as_local: Whether update all references of external links as references of current workbook itself.'''
        ...
    
    @overload
    def remove_at(self, index : int):
        '''Removes the specified external link from the workbook.
        
        :param index: the index of the external link to be removed.'''
        ...
    
    @overload
    def remove_at(self, index : int, update_references_as_local : bool):
        '''Removes the specified external link from the workbook.
        
        :param index: the index of the external link to be removed.
        :param update_references_as_local: Whether update all references of given external link to reference of current workbook itself.'''
        ...
    
    @property
    def count(self) -> int:
        '''Gets the number of elements actually contained in the collection.'''
        ...
    
    def __getitem__(self, key : int) -> aspose.cells.ExternalLink:
        '''Gets the :py:class:`aspose.cells.ExternalLink` element at the specified index.'''
        ...
    
    ...

class FileFontSource(FontSourceBase):
    '''Represents the single TrueType font file stored in the file system.'''
    
    @property
    def type(self) -> aspose.cells.FontSourceType:
        '''Returns the type of the font source.'''
        ...
    
    @property
    def file_path(self) -> str:
        ...
    
    ...

class FileFormatInfo:
    '''Contains data returned by :py:class:`aspose.cells.FileFormatUtil` file format detection methods.'''
    
    @property
    def is_protected_by_rms(self) -> bool:
        ...
    
    @property
    def is_encrypted(self) -> bool:
        ...
    
    @property
    def file_format_type(self) -> aspose.cells.FileFormatType:
        ...
    
    @property
    def load_format(self) -> aspose.cells.LoadFormat:
        ...
    
    ...

class FileFormatUtil:
    '''Provides utility methods for converting file format enums to strings or file extensions and back.'''
    
    @overload
    @staticmethod
    def detect_file_format(stream : io.RawIOBase) -> aspose.cells.FileFormatInfo:
        '''Detects and returns the information about a format of an excel stored in a stream.
        
        :returns: A :py:class:`aspose.cells.FileFormatInfo` object that contains the detected information.'''
        ...
    
    @overload
    @staticmethod
    def detect_file_format(stream : io.RawIOBasepassword : str) -> aspose.cells.FileFormatInfo:
        '''Detects and returns the information about a format of an excel stored in a stream.
        
        :param password: The password for encrypted ooxml files.
        :returns: A :py:class:`aspose.cells.FileFormatInfo` object that contains the detected information.'''
        ...
    
    @overload
    @staticmethod
    def detect_file_format(file_path : str) -> aspose.cells.FileFormatInfo:
        '''Detects and returns the information about a format of an excel stored in a file.
        
        :param file_path: The file path.
        :returns: A :py:class:`aspose.cells.FileFormatInfo` object that contains the detected information.'''
        ...
    
    @overload
    @staticmethod
    def detect_file_format(file_path : strpassword : str) -> aspose.cells.FileFormatInfo:
        '''Detects and returns the information about a format of an excel stored in a file.
        
        :param file_path: The file path.
        :param password: The password for encrypted ooxml files.
        :returns: A :py:class:`aspose.cells.FileFormatInfo` object that contains the detected information.'''
        ...
    
    @staticmethod
    def verify_password(stream : io.RawIOBasepassword : str) -> bool:
        '''Detects and returns the information about a format of an excel stored in a stream.
        
        :param password: The password for encrypted ooxml files.
        :returns: Returns whether the password is corrected.'''
        ...
    
    @staticmethod
    def file_format_to_save_format(format : aspose.cells.FileFormatType) -> aspose.cells.SaveFormat:
        '''Converting file format to save format.
        
        :param format: The file format type.'''
        ...
    
    @staticmethod
    def extension_to_save_format(extension : str) -> aspose.cells.SaveFormat:
        '''Converts a file name extension into a SaveFormat value.
        
        :param extension: The file extension. Can be with or without a leading dot. Case-insensitive.'''
        ...
    
    @staticmethod
    def is_template_format(extension : str) -> bool:
        '''Returns true if the extension is .xlt, .xltX, .xltm,.ots.'''
        ...
    
    @staticmethod
    def load_format_to_extension(load_format : aspose.cells.LoadFormat) -> str:
        '''Converts a load format enumerated value into a file extension.
        
        :param load_format: The loaded file format.
        :returns: The returned extension is a lower-case string with a leading dot.'''
        ...
    
    @staticmethod
    def load_format_to_save_format(load_format : aspose.cells.LoadFormat) -> aspose.cells.SaveFormat:
        '''Converts a LoadFormat value to a SaveFormat value if possible.
        
        :param load_format: The load format.
        :returns: The save format.'''
        ...
    
    @staticmethod
    def save_format_to_extension(format : aspose.cells.SaveFormat) -> str:
        '''Converts a save format enumerated value into a file extension.
        
        :param format: The save format.
        :returns: The returned extension is a lower-case string with a leading dot.'''
        ...
    
    @staticmethod
    def save_format_to_load_format(save_format : aspose.cells.SaveFormat) -> aspose.cells.LoadFormat:
        '''Converts a SaveFormat value to a LoadFormat value if possible.
        
        :param save_format: The save format.
        :returns: The load format'''
        ...
    
    ...

class FilterColumn:
    '''Represents a filter for a single column. The Filter object is a member of the Filters collection'''
    
    @property
    def is_dropdown_visible(self) -> bool:
        ...
    
    @is_dropdown_visible.setter
    def is_dropdown_visible(self, value : bool):
        ...
    
    @property
    def visibledropdown(self) -> bool:
        '''Indicates whether the AutoFilter button for this column is visible.'''
        ...
    
    @visibledropdown.setter
    def visibledropdown(self, value : bool):
        '''Indicates whether the AutoFilter button for this column is visible.'''
        ...
    
    @property
    def filter(self) -> any:
        '''Gets and sets the condition of filtering data.'''
        ...
    
    @filter.setter
    def filter(self, value : any):
        '''Gets and sets the condition of filtering data.'''
        ...
    
    @property
    def filter_type(self) -> aspose.cells.FilterType:
        ...
    
    @filter_type.setter
    def filter_type(self, value : aspose.cells.FilterType):
        ...
    
    @property
    def field_index(self) -> int:
        ...
    
    @field_index.setter
    def field_index(self, value : int):
        ...
    
    ...

class FilterColumnCollection:
    '''A collection of Filter objects that represents all the filters in an autofiltered range.'''
    
    @overload
    def copy_to(self, array : List[aspose.cells.FilterColumn]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.FilterColumn], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.FilterColumn, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.FilterColumn, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.FilterColumn) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.FilterColumn, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.FilterColumn, index : int, count : int) -> int:
        ...
    
    def get_by_index(self, index : int) -> aspose.cells.FilterColumn:
        '''Returns a single Filter object from a collection.'''
        ...
    
    def binary_search(self, item : aspose.cells.FilterColumn) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class FindOptions:
    '''Represents find options.'''
    
    def get_range(self) -> aspose.cells.CellArea:
        '''Gets and sets the searched range.
        
        :returns: Returns the searched range.'''
        ...
    
    def set_range(self, ca : aspose.cells.CellArea):
        '''Sets the searched range.
        
        :param ca: the searched range.'''
        ...
    
    @property
    def is_case_sensitive(self) -> bool:
        ...
    
    @is_case_sensitive.setter
    def is_case_sensitive(self, value : bool):
        ...
    
    @property
    def case_sensitive(self) -> bool:
        ...
    
    @case_sensitive.setter
    def case_sensitive(self, value : bool):
        ...
    
    @property
    def look_at_type(self) -> aspose.cells.LookAtType:
        ...
    
    @look_at_type.setter
    def look_at_type(self, value : aspose.cells.LookAtType):
        ...
    
    @property
    def is_range_set(self) -> bool:
        ...
    
    @property
    def search_next(self) -> bool:
        ...
    
    @search_next.setter
    def search_next(self, value : bool):
        ...
    
    @property
    def search_backward(self) -> bool:
        ...
    
    @search_backward.setter
    def search_backward(self, value : bool):
        ...
    
    @property
    def seach_order_by_rows(self) -> bool:
        ...
    
    @seach_order_by_rows.setter
    def seach_order_by_rows(self, value : bool):
        ...
    
    @property
    def look_in_type(self) -> aspose.cells.LookInType:
        ...
    
    @look_in_type.setter
    def look_in_type(self, value : aspose.cells.LookInType):
        ...
    
    @property
    def regex_key(self) -> bool:
        ...
    
    @regex_key.setter
    def regex_key(self, value : bool):
        ...
    
    @property
    def value_type_sensitive(self) -> bool:
        ...
    
    @value_type_sensitive.setter
    def value_type_sensitive(self, value : bool):
        ...
    
    @property
    def style(self) -> aspose.cells.Style:
        '''The format to search for.'''
        ...
    
    @style.setter
    def style(self, value : aspose.cells.Style):
        '''The format to search for.'''
        ...
    
    @property
    def convert_numeric_data(self) -> bool:
        ...
    
    @convert_numeric_data.setter
    def convert_numeric_data(self, value : bool):
        ...
    
    ...

class FolderFontSource(FontSourceBase):
    '''Represents the folder that contains TrueType font files.'''
    
    @property
    def type(self) -> aspose.cells.FontSourceType:
        '''Returns the type of the font source.'''
        ...
    
    @property
    def folder_path(self) -> str:
        ...
    
    @property
    def scan_sub_folders(self) -> bool:
        ...
    
    ...

class Font:
    '''Encapsulates the font object used in a spreadsheet.'''
    
    def equals(self, font : aspose.cells.Font) -> bool:
        '''Checks if two fonts are equals.
        
        :param font: Compared font object.
        :returns: True if equal to the compared font object.'''
        ...
    
    @property
    def charset(self) -> int:
        '''Represent the character set.'''
        ...
    
    @charset.setter
    def charset(self, value : int):
        '''Represent the character set.'''
        ...
    
    @property
    def is_italic(self) -> bool:
        ...
    
    @is_italic.setter
    def is_italic(self, value : bool):
        ...
    
    @property
    def is_bold(self) -> bool:
        ...
    
    @is_bold.setter
    def is_bold(self, value : bool):
        ...
    
    @property
    def caps_type(self) -> aspose.cells.TextCapsType:
        ...
    
    @caps_type.setter
    def caps_type(self, value : aspose.cells.TextCapsType):
        ...
    
    @property
    def strike_type(self) -> aspose.cells.TextStrikeType:
        ...
    
    @strike_type.setter
    def strike_type(self, value : aspose.cells.TextStrikeType):
        ...
    
    @property
    def is_strikeout(self) -> bool:
        ...
    
    @is_strikeout.setter
    def is_strikeout(self, value : bool):
        ...
    
    @property
    def script_offset(self) -> float:
        ...
    
    @script_offset.setter
    def script_offset(self, value : float):
        ...
    
    @property
    def is_superscript(self) -> bool:
        ...
    
    @is_superscript.setter
    def is_superscript(self, value : bool):
        ...
    
    @property
    def is_subscript(self) -> bool:
        ...
    
    @is_subscript.setter
    def is_subscript(self, value : bool):
        ...
    
    @property
    def underline(self) -> aspose.cells.FontUnderlineType:
        '''Gets the font underline type.'''
        ...
    
    @underline.setter
    def underline(self, value : aspose.cells.FontUnderlineType):
        '''Sets the font underline type.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets  the name of the :py:class:`aspose.cells.Font`.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets  or sets the name of the :py:class:`aspose.cells.Font`.'''
        ...
    
    @property
    def double_size(self) -> float:
        ...
    
    @double_size.setter
    def double_size(self, value : float):
        ...
    
    @property
    def size(self) -> int:
        '''Gets the size of the font.'''
        ...
    
    @size.setter
    def size(self, value : int):
        '''Sets the size of the font.'''
        ...
    
    @property
    def theme_color(self) -> aspose.cells.ThemeColor:
        ...
    
    @theme_color.setter
    def theme_color(self, value : aspose.cells.ThemeColor):
        ...
    
    @property
    def color(self) -> aspose.pydrawing.Color:
        '''Gets the :py:class:`aspose.pydrawing.Color` of the font.'''
        ...
    
    @color.setter
    def color(self, value : aspose.pydrawing.Color):
        '''Sets the :py:class:`aspose.pydrawing.Color` of the font.'''
        ...
    
    @property
    def argb_color(self) -> int:
        ...
    
    @argb_color.setter
    def argb_color(self, value : int):
        ...
    
    @property
    def is_normalize_heights(self) -> bool:
        ...
    
    @is_normalize_heights.setter
    def is_normalize_heights(self, value : bool):
        ...
    
    @property
    def scheme_type(self) -> aspose.cells.FontSchemeType:
        ...
    
    @scheme_type.setter
    def scheme_type(self, value : aspose.cells.FontSchemeType):
        ...
    
    ...

class FontConfigs:
    '''Specifies font settings'''
    
    @staticmethod
    def is_font_available(font_name : str) -> bool:
        '''Indicate whether the font is available.
        
        :param font_name: font name
        :returns: true if font is available, otherwise false.'''
        ...
    
    @staticmethod
    def set_font_substitutes(original_font_name : strsubstitute_font_names : List[str]):
        '''Font substitute names for given original font name.
        
        :param original_font_name: Original font name.
        :param substitute_font_names: List of font substitute names to be used if original font is not presented.'''
        ...
    
    @staticmethod
    def get_font_substitutes(original_font_name : str) -> List[str]:
        '''Returns array containing font substitute names to be used if original font is not presented.
        
        :param original_font_name: originalFontName
        :returns: An array containing font substitute names to be used if original font is not presented.'''
        ...
    
    @staticmethod
    def set_font_folder(font_folder : strrecursive : bool):
        '''Sets the fonts folder
        
        :param font_folder: The folder that contains TrueType fonts.
        :param recursive: Determines whether or not to scan subfolders.'''
        ...
    
    @staticmethod
    def set_font_folders(font_folders : List[str]recursive : bool):
        '''Sets the fonts folders
        
        :param font_folders: The folders that contains TrueType fonts.
        :param recursive: Determines whether or not to scan subfolders.'''
        ...
    
    @staticmethod
    def set_font_sources(sources : List[aspose.cells.FontSourceBase]):
        '''Sets the fonts sources.
        
        :param sources: An array of sources that contain TrueType fonts.'''
        ...
    
    @staticmethod
    def get_font_sources() -> List[aspose.cells.FontSourceBase]:
        '''Gets a copy of the array that contains the list of sources'''
        ...
    
    @classmethod
    @property
    def default_font_name(cls) -> str:
        ...
    
    @classmethod
    @default_font_name.setter
    def default_font_name(cls, value : str):
        ...
    
    @classmethod
    @property
    def prefer_system_font_substitutes(cls) -> bool:
        ...
    
    @classmethod
    @prefer_system_font_substitutes.setter
    def prefer_system_font_substitutes(cls, value : bool):
        ...
    
    ...

class FontSetting:
    '''Represents a range of characters within the cell text.'''
    
    def set_word_art_style(self, style : aspose.cells.drawing.PresetWordArtStyle):
        '''Sets the preset WordArt style.
        
        :param style: The preset WordArt style.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.texts.TextNodeType:
        '''Gets the type of text node.'''
        ...
    
    @property
    def start_index(self) -> int:
        ...
    
    @property
    def length(self) -> int:
        '''Gets the length of the characters.'''
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Returns the font of this object.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    ...

class FontSourceBase:
    '''This is an abstract base class for the classes that allow the user to specify various font sources'''
    
    @property
    def type(self) -> aspose.cells.FontSourceType:
        '''Returns the type of the font source.'''
        ...
    
    ...

class FormatCondition:
    '''Represents conditional formatting condition.'''
    
    @overload
    def get_formula1(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the value or expression associated with this format condition.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The value or expression associated with this format condition.'''
        ...
    
    @overload
    def get_formula1(self, is_r1c1 : bool, is_local : bool, row : int, column : int) -> str:
        '''Gets the value or expression of the conditional formatting of the cell.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :param row: The row index.
        :param column: The column index.
        :returns: The value or expression associated with the conditional formatting of the cell.'''
        ...
    
    @overload
    def get_formula1(self, row : int, column : int) -> str:
        '''Gets the formula of the conditional formatting of the cell.
        
        :param row: The row index.
        :param column: The column index.
        :returns: The formula.'''
        ...
    
    @overload
    def get_formula2(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the value or expression associated with this format condition.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The value or expression associated with this format condition.'''
        ...
    
    @overload
    def get_formula2(self, is_r1c1 : bool, is_local : bool, row : int, column : int) -> str:
        '''Gets the value or expression of the conditional formatting of the cell.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :param row: The row index.
        :param column: The column index.
        :returns: The value or expression associated with the conditional formatting of the cell.'''
        ...
    
    @overload
    def get_formula2(self, row : int, column : int) -> str:
        '''Gets the formula of the conditional formatting of the cell.
        
        :param row: The row index.
        :param column: The column index.
        :returns: The formula.'''
        ...
    
    def set_formulas(self, formula1 : str, formula2 : str, is_r1c1 : bool, is_local : bool):
        '''Sets the value or expression associated with this format condition.
        
        :param formula1: The value or expression associated with this format condition.
        If the input value starts with '=', then it will be taken as formula. Otherwise it will be taken as plain value(text, number, bool).
        For text value that starts with '=', user may input it as formula in format: "=\"=...\"".
        :param formula2: The value or expression associated with this format condition. The input format is same with formula1
        :param is_r1c1: Whether the formula is R1C1 formula.
        :param is_local: Whether the formula is locale formatted.'''
        ...
    
    def set_formula1(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the value or expression associated with this format condition.
        
        :param formula: The value or expression associated with this format condition.
        If the input value starts with '=', then it will be taken as formula. Otherwise it will be taken as plain value(text, number, bool).
        For text value that starts with '=', user may input it as formula in format: "=\"=...\"".
        :param is_r1c1: Whether the formula is R1C1 formula.
        :param is_local: Whether the formula is locale formatted.'''
        ...
    
    def set_formula2(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the value or expression associated with this format condition.
        
        :param formula: The value or expression associated with this format condition.
        If the input value starts with '=', then it will be taken as formula. Otherwise it will be taken as plain value(text, number, bool).
        For text value that starts with '=', user may input it as formula in format: "=\"=...\"".
        :param is_r1c1: Whether the formula is R1C1 formula.
        :param is_local: Whether the formula is locale formatted.'''
        ...
    
    @property
    def formula1(self) -> str:
        '''Gets and sets the value or expression associated with conditional formatting.'''
        ...
    
    @formula1.setter
    def formula1(self, value : str):
        '''Gets and sets the value or expression associated with conditional formatting.'''
        ...
    
    @property
    def formula2(self) -> str:
        '''Gets and sets the value or expression associated with conditional formatting.'''
        ...
    
    @formula2.setter
    def formula2(self, value : str):
        '''Gets and sets the value or expression associated with conditional formatting.'''
        ...
    
    @property
    def operator(self) -> aspose.cells.OperatorType:
        '''Gets and sets the conditional format operator type.'''
        ...
    
    @operator.setter
    def operator(self, value : aspose.cells.OperatorType):
        '''Gets and sets the conditional format operator type.'''
        ...
    
    @property
    def stop_if_true(self) -> bool:
        ...
    
    @stop_if_true.setter
    def stop_if_true(self, value : bool):
        ...
    
    @property
    def priority(self) -> int:
        '''The priority of this conditional formatting rule. This value is used to determine which
        format should be evaluated and rendered. Lower numeric values are higher priority than
        higher numeric values, where '1' is the highest priority.'''
        ...
    
    @priority.setter
    def priority(self, value : int):
        '''The priority of this conditional formatting rule. This value is used to determine which
        format should be evaluated and rendered. Lower numeric values are higher priority than
        higher numeric values, where '1' is the highest priority.'''
        ...
    
    @property
    def style(self) -> aspose.cells.Style:
        '''Gets or setts style of conditional formatted cell ranges.'''
        ...
    
    @style.setter
    def style(self, value : aspose.cells.Style):
        '''Setts style of conditional formatted cell ranges.'''
        ...
    
    @property
    def type(self) -> aspose.cells.FormatConditionType:
        '''Gets and sets whether the conditional format Type.'''
        ...
    
    @type.setter
    def type(self, value : aspose.cells.FormatConditionType):
        '''Gets and sets whether the conditional format Type.'''
        ...
    
    @property
    def icon_set(self) -> aspose.cells.IconSet:
        ...
    
    @property
    def data_bar(self) -> aspose.cells.DataBar:
        ...
    
    @property
    def color_scale(self) -> aspose.cells.ColorScale:
        ...
    
    @property
    def top10(self) -> aspose.cells.Top10:
        '''Get the conditional formatting's "Top10" instance.
        The default instance's rule highlights cells whose
        values fall in the top 10 bracket.
        Valid only for type is Top10.'''
        ...
    
    @property
    def above_average(self) -> aspose.cells.AboveAverage:
        ...
    
    @property
    def text(self) -> str:
        '''The text value in a "text contains" conditional formatting rule.
        Valid only for type = containsText, notContainsText, beginsWith and endsWith.
        The default value is null.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''The text value in a "text contains" conditional formatting rule.
        Valid only for type = containsText, notContainsText, beginsWith and endsWith.
        The default value is null.'''
        ...
    
    @property
    def time_period(self) -> aspose.cells.TimePeriodType:
        ...
    
    @time_period.setter
    def time_period(self, value : aspose.cells.TimePeriodType):
        ...
    
    ...

class FormatConditionCollection:
    '''Represents conditional formatting.
    The FormatConditions can contain up to three conditional formats.'''
    
    @overload
    def add_condition(self, type : aspose.cells.FormatConditionType, operator_type : aspose.cells.OperatorType, formula1 : str, formula2 : str) -> int:
        '''Adds a formatting condition.
        
        :param type: :py:class:`aspose.cells.FormatConditionType` of conditional formatting.
        It could be one of the members of FormatConditionType.
        :param operator_type: The comparison :py:class:`aspose.cells.OperatorType`.
        It could be one of the members of OperatorType.
        :param formula1: The value or expression associated with conditional formatting.
        If the input value starts with '=', then it will be taken as formula.
        Otherwise it will be taken as plain value(text, number, bool).
        For text value that starts with '=', user may input it as formula in format: "=\"=...\"".
        :param formula2: The value or expression associated with conditional formatting.
        The input format is same with formula1
        :returns: Formatting condition object index;'''
        ...
    
    @overload
    def add_condition(self, type : aspose.cells.FormatConditionType) -> int:
        '''Add a format condition.
        
        :param type: Format condition type.
        :returns: Formatting condition object index;'''
        ...
    
    @overload
    def remove_area(self, index : int):
        '''Removes conditional formatted cell range by index.
        
        :param index: The index of the conditional formatted cell range to be removed.'''
        ...
    
    @overload
    def remove_area(self, start_row : int, start_column : int, total_rows : int, total_columns : int) -> bool:
        '''Remove conditional formatting int the range.
        
        :param start_row: The startRow of the range.
        :param start_column: The startColumn of the range.
        :param total_rows: The number of rows of the range.
        :param total_columns: The number of columns of the range.
        :returns: Returns TRUE, this FormatCondtionCollection should be removed.'''
        ...
    
    def add(self, cell_area : aspose.cells.CellArea, type : aspose.cells.FormatConditionType, operator_type : aspose.cells.OperatorType, formula1 : str, formula2 : str) -> List[int]:
        '''Adds a formatting condition and effected cell rang to the FormatConditions
        The FormatConditions can contain up to three conditional formats.
        References to the other sheets are not allowed in the formulas of conditional formatting.
        
        :param cell_area: Conditional formatted cell range.
        :param type: Type of conditional formatting.It could be one of the members of FormatConditionType.
        :param operator_type: Comparison operator.It could be one of the members of OperatorType.
        :param formula1: The value or expression associated with conditional formatting.
        :param formula2: The value or expression associated with conditional formatting
        :returns: [0]:Formatting condition object index;[1] Effected cell rang index.'''
        ...
    
    def add_area(self, cell_area : aspose.cells.CellArea) -> int:
        '''Adds a conditional formatted cell range.
        
        :param cell_area: Conditional formatted cell range.
        :returns: Conditional formatted cell rang index.'''
        ...
    
    def get_cell_area(self, index : int) -> aspose.cells.CellArea:
        '''Gets the conditional formatted cell range by index.
        
        :param index: the index of the conditional formatted cell range.
        :returns: the conditional formatted cell range'''
        ...
    
    def remove_condition(self, index : int):
        '''Removes the formatting condition by index.
        
        :param index: The index of the formatting condition to be removed.'''
        ...
    
    @property
    def count(self) -> int:
        '''Gets the count of the conditions.'''
        ...
    
    @property
    def range_count(self) -> int:
        ...
    
    def __getitem__(self, key : int) -> aspose.cells.FormatCondition:
        '''Gets the formatting condition by index.'''
        ...
    
    ...

class FormulaParseOptions:
    '''Represents options when parsing formula.'''
    
    @property
    def locale_dependent(self) -> bool:
        ...
    
    @locale_dependent.setter
    def locale_dependent(self, value : bool):
        ...
    
    @property
    def r1c1_style(self) -> bool:
        ...
    
    @r1c1_style.setter
    def r1c1_style(self, value : bool):
        ...
    
    @property
    def check_add_in(self) -> bool:
        ...
    
    @check_add_in.setter
    def check_add_in(self, value : bool):
        ...
    
    @property
    def parse(self) -> bool:
        '''Whether parse given formula. Default is true.
        If it is false, then given formula string will be kept as it is for the cell until user call other methods to parse them
        or parsed formula data is required by other operations such as calculating formulas.'''
        ...
    
    @parse.setter
    def parse(self, value : bool):
        '''Whether parse given formula. Default is true.
        If it is false, then given formula string will be kept as it is for the cell until user call other methods to parse them
        or parsed formula data is required by other operations such as calculating formulas.'''
        ...
    
    ...

class FormulaSettings:
    '''Settings of formulas and calculation.'''
    
    @property
    def calculate_on_open(self) -> bool:
        ...
    
    @calculate_on_open.setter
    def calculate_on_open(self, value : bool):
        ...
    
    @property
    def calculate_on_save(self) -> bool:
        ...
    
    @calculate_on_save.setter
    def calculate_on_save(self, value : bool):
        ...
    
    @property
    def force_full_calculation(self) -> bool:
        ...
    
    @force_full_calculation.setter
    def force_full_calculation(self, value : bool):
        ...
    
    @property
    def calculation_mode(self) -> aspose.cells.CalcModeType:
        ...
    
    @calculation_mode.setter
    def calculation_mode(self, value : aspose.cells.CalcModeType):
        ...
    
    @property
    def calculation_id(self) -> str:
        ...
    
    @calculation_id.setter
    def calculation_id(self, value : str):
        ...
    
    @property
    def enable_iterative_calculation(self) -> bool:
        ...
    
    @enable_iterative_calculation.setter
    def enable_iterative_calculation(self, value : bool):
        ...
    
    @property
    def max_iteration(self) -> int:
        ...
    
    @max_iteration.setter
    def max_iteration(self, value : int):
        ...
    
    @property
    def max_change(self) -> float:
        ...
    
    @max_change.setter
    def max_change(self, value : float):
        ...
    
    @property
    def precision_as_displayed(self) -> bool:
        ...
    
    @precision_as_displayed.setter
    def precision_as_displayed(self, value : bool):
        ...
    
    @property
    def enable_calculation_chain(self) -> bool:
        ...
    
    @enable_calculation_chain.setter
    def enable_calculation_chain(self, value : bool):
        ...
    
    ...

class GlobalizationSettings:
    '''Represents the globalization settings.'''
    
    def get_pivot_total_name(self) -> str:
        '''Gets the name of "Total" label in the PivotTable.
        You need to override this method when the PivotTable contains two or more PivotFields in the data area.
        
        :returns: The name of "Total" label'''
        ...
    
    def get_pivot_grand_total_name(self) -> str:
        '''Gets the name of "Grand Total" label in the PivotTable.
        
        :returns: The name of "Grand Total" label'''
        ...
    
    def get_multiple_items_name(self) -> str:
        '''Gets the name of "(Multiple Items)" label in the PivotTable.
        
        :returns: The name of "(Multiple Items)" label'''
        ...
    
    def get_all_name(self) -> str:
        '''Gets the name of "(All)" label in the PivotTable.
        
        :returns: The name of "(All)" label'''
        ...
    
    def get_protection_name_of_pivot_table(self) -> str:
        '''Gets the protection name in the PivotTable.
        
        :returns: The protection name of PivotTable'''
        ...
    
    def get_column_labels_of_pivot_table(self) -> str:
        '''Gets the name of "Column Labels" label in the PivotTable.
        
        :returns: The name of column labels'''
        ...
    
    def get_row_labels_name_of_pivot_table(self) -> str:
        '''Gets the name of "Row Labels" label in the PivotTable.
        
        :returns: The name of row labels'''
        ...
    
    def get_empty_data_name(self) -> str:
        '''Gets the name of "(blank)" label in the PivotTable.
        
        :returns: The name of empty data'''
        ...
    
    def get_data_field_header_name_of_pivot_table(self) -> str:
        '''Gets the the name of the value area field header in the PivotTable.
        
        :returns: The name of data field header name'''
        ...
    
    def get_sub_total_name(self, sub_total_type : aspose.cells.pivot.PivotFieldSubtotalType) -> str:
        '''Gets the name of :py:class:`aspose.cells.pivot.PivotFieldSubtotalType` type in the PivotTable.
        
        :param sub_total_type: The :py:class:`aspose.cells.pivot.PivotFieldSubtotalType` type
        :returns: The name of :py:class:`aspose.cells.pivot.PivotFieldSubtotalType` type'''
        ...
    
    def get_total_name(self, function_type : aspose.cells.ConsolidationFunction) -> str:
        '''Gets the total name of the function.
        
        :param function_type: The function type.
        :returns: The total name of the function.'''
        ...
    
    def get_grand_total_name(self, function_type : aspose.cells.ConsolidationFunction) -> str:
        '''Gets the grand total name of the function.
        
        :param function_type: The function type.
        :returns: The grand total name of the function.'''
        ...
    
    def get_table_row_type_of_headers(self) -> str:
        '''Gets the type name of table rows that consists of the table header.
        Default is "Headers", so in formula "#Headers" represents the table header.
        
        :returns: the type name of table rows'''
        ...
    
    def get_table_row_type_of_data(self) -> str:
        '''Gets the type name of table rows that consists of data region of referenced table.
        Default is "Data", so in formula "#Data" represents the data region of the table.
        
        :returns: the type name of table rows'''
        ...
    
    def get_table_row_type_of_all(self) -> str:
        '''Gets the type name of table rows that consists of all rows in referenced table.
        Default is "All", so in formula "#All" represents all rows in referenced table.
        
        :returns: the type name of table rows'''
        ...
    
    def get_table_row_type_of_totals(self) -> str:
        '''Gets the type name of table rows that consists of the total row of referenced table.
        Default is "Totals", so in formula "#Totals" represents the total row of referenced table.
        
        :returns: the type name of table rows'''
        ...
    
    def get_table_row_type_of_current(self) -> str:
        '''Gets the type name of table rows that consists of the current row in referenced table.
        Default is "This Row", so in formula "#This Row" represents the current row in referenced table.
        
        :returns: the type name of table rows'''
        ...
    
    def get_error_value_string(self, err : str) -> str:
        '''Gets the display string value for cell's error value
        
        :param err: error values such as #VALUE!,#NAME?
        :returns: Default returns the error value itself'''
        ...
    
    def get_boolean_value_string(self, bv : bool) -> str:
        '''Gets the display string value for cell's boolean value
        
        :param bv: boolean value
        :returns: Default returns "TRUE" for true value and "FALSE" for false value.'''
        ...
    
    def get_local_function_name(self, standard_name : str) -> str:
        '''Gets the locale dependent function name according to given standard function name.
        
        :param standard_name: Standard(en-US locale) function name.
        :returns: Locale dependent function name. The locale was specified by the Workbook for which this settings is used.'''
        ...
    
    def get_standard_function_name(self, local_name : str) -> str:
        '''Gets the standard function name according to given locale dependent function name.
        
        :param local_name: Locale dependent function name. The locale was specified by the Workbook for which this settings is used.
        :returns: Standard(en-US locale) function name.'''
        ...
    
    def get_local_built_in_name(self, standard_name : str) -> str:
        '''Gets the locale dependent text for built-in Name according to given standard text.
        
        :param standard_name: Standard(en-US locale) text of built-in Name.
        :returns: Locale dependent text. The locale was specified by the Workbook for which this settings is used.'''
        ...
    
    def get_standard_built_in_name(self, local_name : str) -> str:
        '''Gets the standard text of built-in Name according to given locale dependent text.
        
        :param local_name: Locale dependent text of built-in Name. The locale was specified by the Workbook for which this settings is used.
        :returns: Standard(en-US locale) text.'''
        ...
    
    def get_standard_header_footer_font_style_name(self, localfont_style_name : str) -> str:
        '''Gets standard English font style name(Regular, Bold, Italic) for Header/Footer according to given locale font style name.
        
        :param localfont_style_name: Locale font style name for Header/Footer.
        :returns: Standard English font style name(Regular, Bold, Italic)'''
        ...
    
    def get_comment_title_name(self, type : aspose.cells.rendering.CommentTitleType) -> str:
        '''Gets the locale dependent comment title name according to comment title type.'''
        ...
    
    def compare(self, v1 : str, v2 : str, ignore_case : bool) -> int:
        '''Compares two string values according to certain collation rules.
        
        :param v1: the first string
        :param v2: the second string
        :param ignore_case: whether ignore case when comparing values
        :returns: Integer that indicates the lexical relationship between the two comparands'''
        ...
    
    @property
    def chart_settings(self) -> aspose.cells.charts.ChartGlobalizationSettings:
        ...
    
    @chart_settings.setter
    def chart_settings(self, value : aspose.cells.charts.ChartGlobalizationSettings):
        ...
    
    @property
    def pivot_settings(self) -> aspose.cells.settings.PivotGlobalizationSettings:
        ...
    
    @pivot_settings.setter
    def pivot_settings(self, value : aspose.cells.settings.PivotGlobalizationSettings):
        ...
    
    @property
    def list_separator(self) -> char:
        ...
    
    @property
    def row_separator_of_formula_array(self) -> char:
        ...
    
    @property
    def column_separator_of_formula_array(self) -> char:
        ...
    
    ...

class HeaderFooterCommand:
    '''Represents the command of header/footer'''
    
    @property
    def type(self) -> aspose.cells.HeaderFooterCommandType:
        '''Gets the header/footer' command type .'''
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Gets the font of the command's value.'''
        ...
    
    @property
    def text(self) -> str:
        '''Gets the text of the command.'''
        ...
    
    ...

class HorizontalPageBreak:
    '''Encapsulates the object that represents a horizontal page break.'''
    
    @property
    def start_column(self) -> int:
        ...
    
    @property
    def end_column(self) -> int:
        ...
    
    @property
    def row(self) -> int:
        '''Gets the zero based row index.'''
        ...
    
    ...

class HorizontalPageBreakCollection:
    '''Encapsulates a collection of :py:class:`aspose.cells.HorizontalPageBreak` objects.'''
    
    @overload
    def add(self, row : int, start_column : int, end_column : int) -> int:
        '''Adds a horizontal page break to the collection.
        
        :param row: Row index, zero based.
        :param start_column: Start column index, zero based.
        :param end_column: End column index, zero based.
        :returns: :py:class:`aspose.cells.HorizontalPageBreak` object index.'''
        ...
    
    @overload
    def add(self, row : int) -> int:
        '''Adds a horizontal page break to the collection.
        
        :param row: Cell row index, zero based.
        :returns: :py:class:`aspose.cells.HorizontalPageBreak` object index.'''
        ...
    
    @overload
    def add(self, row : int, column : int) -> int:
        '''Adds a horizontal page break to the collection.
        
        :param row: Cell row index, zero based.
        :param column: Cell column index, zero based.
        :returns: :py:class:`aspose.cells.HorizontalPageBreak` object index.'''
        ...
    
    @overload
    def add(self, cell_name : str) -> int:
        '''Adds a horizontal page break to the collection.
        
        :param cell_name: Cell name.
        :returns: :py:class:`aspose.cells.HorizontalPageBreak` object index.'''
        ...
    
    @overload
    def copy_to(self, array : List[aspose.cells.HorizontalPageBreak]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.HorizontalPageBreak], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.HorizontalPageBreak, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.HorizontalPageBreak, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.HorizontalPageBreak) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.HorizontalPageBreak, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.HorizontalPageBreak, index : int, count : int) -> int:
        ...
    
    def binary_search(self, item : aspose.cells.HorizontalPageBreak) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class HtmlLoadOptions(AbstractTextLoadOptions):
    '''Represents options when importing a html file.'''
    
    def set_paper_size(self, type : aspose.cells.PaperSizeType):
        '''Sets the default print paper size from default printer's setting.
        
        :param type: The default paper size.'''
        ...
    
    @property
    def load_format(self) -> aspose.cells.LoadFormat:
        ...
    
    @property
    def password(self) -> str:
        '''Gets and set the password of the workbook.'''
        ...
    
    @password.setter
    def password(self, value : str):
        '''Gets and set the password of the workbook.'''
        ...
    
    @property
    def parsing_formula_on_open(self) -> bool:
        ...
    
    @parsing_formula_on_open.setter
    def parsing_formula_on_open(self, value : bool):
        ...
    
    @property
    def parsing_pivot_cached_records(self) -> bool:
        ...
    
    @parsing_pivot_cached_records.setter
    def parsing_pivot_cached_records(self, value : bool):
        ...
    
    @property
    def language_code(self) -> aspose.cells.CountryCode:
        ...
    
    @language_code.setter
    def language_code(self, value : aspose.cells.CountryCode):
        ...
    
    @property
    def region(self) -> aspose.cells.CountryCode:
        '''Gets the system regional settings based on CountryCode at the time the file was loaded.'''
        ...
    
    @region.setter
    def region(self, value : aspose.cells.CountryCode):
        '''Sets the system regional settings based on CountryCode at the time the file was loaded.'''
        ...
    
    @property
    def default_style_settings(self) -> aspose.cells.DefaultStyleSettings:
        ...
    
    @property
    def standard_font(self) -> str:
        ...
    
    @standard_font.setter
    def standard_font(self, value : str):
        ...
    
    @property
    def standard_font_size(self) -> float:
        ...
    
    @standard_font_size.setter
    def standard_font_size(self, value : float):
        ...
    
    @property
    def interrupt_monitor(self) -> aspose.cells.AbstractInterruptMonitor:
        ...
    
    @interrupt_monitor.setter
    def interrupt_monitor(self, value : aspose.cells.AbstractInterruptMonitor):
        ...
    
    @property
    def ignore_not_printed(self) -> bool:
        ...
    
    @ignore_not_printed.setter
    def ignore_not_printed(self, value : bool):
        ...
    
    @property
    def check_data_valid(self) -> bool:
        ...
    
    @check_data_valid.setter
    def check_data_valid(self, value : bool):
        ...
    
    @property
    def check_excel_restriction(self) -> bool:
        ...
    
    @check_excel_restriction.setter
    def check_excel_restriction(self, value : bool):
        ...
    
    @property
    def keep_unparsed_data(self) -> bool:
        ...
    
    @keep_unparsed_data.setter
    def keep_unparsed_data(self, value : bool):
        ...
    
    @property
    def load_filter(self) -> aspose.cells.LoadFilter:
        ...
    
    @load_filter.setter
    def load_filter(self, value : aspose.cells.LoadFilter):
        ...
    
    @property
    def light_cells_data_handler(self) -> aspose.cells.LightCellsDataHandler:
        ...
    
    @light_cells_data_handler.setter
    def light_cells_data_handler(self, value : aspose.cells.LightCellsDataHandler):
        ...
    
    @property
    def memory_setting(self) -> aspose.cells.MemorySetting:
        ...
    
    @memory_setting.setter
    def memory_setting(self, value : aspose.cells.MemorySetting):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def auto_fitter_options(self) -> aspose.cells.AutoFitterOptions:
        ...
    
    @auto_fitter_options.setter
    def auto_fitter_options(self, value : aspose.cells.AutoFitterOptions):
        ...
    
    @property
    def auto_filter(self) -> bool:
        ...
    
    @auto_filter.setter
    def auto_filter(self, value : bool):
        ...
    
    @property
    def font_configs(self) -> aspose.cells.IndividualFontConfigs:
        ...
    
    @font_configs.setter
    def font_configs(self, value : aspose.cells.IndividualFontConfigs):
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets and sets the default encoding. Only applies for csv file.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Gets and sets the default encoding. Only applies for csv file.'''
        ...
    
    @property
    def load_style_strategy(self) -> aspose.cells.TxtLoadStyleStrategy:
        ...
    
    @load_style_strategy.setter
    def load_style_strategy(self, value : aspose.cells.TxtLoadStyleStrategy):
        ...
    
    @property
    def convert_numeric_data(self) -> bool:
        ...
    
    @convert_numeric_data.setter
    def convert_numeric_data(self, value : bool):
        ...
    
    @property
    def convert_date_time_data(self) -> bool:
        ...
    
    @convert_date_time_data.setter
    def convert_date_time_data(self, value : bool):
        ...
    
    @property
    def keep_precision(self) -> bool:
        ...
    
    @keep_precision.setter
    def keep_precision(self, value : bool):
        ...
    
    @property
    def attached_files_directory(self) -> str:
        ...
    
    @attached_files_directory.setter
    def attached_files_directory(self, value : str):
        ...
    
    @property
    def load_formulas(self) -> bool:
        ...
    
    @load_formulas.setter
    def load_formulas(self, value : bool):
        ...
    
    @property
    def support_div_tag(self) -> bool:
        ...
    
    @support_div_tag.setter
    def support_div_tag(self, value : bool):
        ...
    
    @property
    def delete_redundant_spaces(self) -> bool:
        ...
    
    @delete_redundant_spaces.setter
    def delete_redundant_spaces(self, value : bool):
        ...
    
    @property
    def auto_fit_cols_and_rows(self) -> bool:
        ...
    
    @auto_fit_cols_and_rows.setter
    def auto_fit_cols_and_rows(self, value : bool):
        ...
    
    @property
    def convert_formulas_data(self) -> bool:
        ...
    
    @convert_formulas_data.setter
    def convert_formulas_data(self, value : bool):
        ...
    
    @property
    def has_formula(self) -> bool:
        ...
    
    @has_formula.setter
    def has_formula(self, value : bool):
        ...
    
    @property
    def stream_provider(self) -> aspose.cells.IStreamProvider:
        ...
    
    @stream_provider.setter
    def stream_provider(self, value : aspose.cells.IStreamProvider):
        ...
    
    @property
    def prog_id(self) -> str:
        ...
    
    ...

class HtmlSaveOptions(SaveOptions):
    '''Represents the options for saving html file.'''
    
    @property
    def save_format(self) -> aspose.cells.SaveFormat:
        ...
    
    @property
    def clear_data(self) -> bool:
        ...
    
    @clear_data.setter
    def clear_data(self, value : bool):
        ...
    
    @property
    def cached_file_folder(self) -> str:
        ...
    
    @cached_file_folder.setter
    def cached_file_folder(self, value : str):
        ...
    
    @property
    def validate_merged_areas(self) -> bool:
        ...
    
    @validate_merged_areas.setter
    def validate_merged_areas(self, value : bool):
        ...
    
    @property
    def merge_areas(self) -> bool:
        ...
    
    @merge_areas.setter
    def merge_areas(self, value : bool):
        ...
    
    @property
    def create_directory(self) -> bool:
        ...
    
    @create_directory.setter
    def create_directory(self, value : bool):
        ...
    
    @property
    def sort_names(self) -> bool:
        ...
    
    @sort_names.setter
    def sort_names(self, value : bool):
        ...
    
    @property
    def sort_external_names(self) -> bool:
        ...
    
    @sort_external_names.setter
    def sort_external_names(self, value : bool):
        ...
    
    @property
    def refresh_chart_cache(self) -> bool:
        ...
    
    @refresh_chart_cache.setter
    def refresh_chart_cache(self, value : bool):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def update_smart_art(self) -> bool:
        ...
    
    @update_smart_art.setter
    def update_smart_art(self, value : bool):
        ...
    
    @property
    def ignore_invisible_shapes(self) -> bool:
        ...
    
    @ignore_invisible_shapes.setter
    def ignore_invisible_shapes(self, value : bool):
        ...
    
    @property
    def page_title(self) -> str:
        ...
    
    @page_title.setter
    def page_title(self, value : str):
        ...
    
    @property
    def attached_files_directory(self) -> str:
        ...
    
    @attached_files_directory.setter
    def attached_files_directory(self, value : str):
        ...
    
    @property
    def attached_files_url_prefix(self) -> str:
        ...
    
    @attached_files_url_prefix.setter
    def attached_files_url_prefix(self, value : str):
        ...
    
    @property
    def default_font_name(self) -> str:
        ...
    
    @default_font_name.setter
    def default_font_name(self, value : str):
        ...
    
    @property
    def worksheet_scalable(self) -> bool:
        ...
    
    @worksheet_scalable.setter
    def worksheet_scalable(self, value : bool):
        ...
    
    @property
    def is_export_comments(self) -> bool:
        ...
    
    @is_export_comments.setter
    def is_export_comments(self, value : bool):
        ...
    
    @property
    def export_comments_type(self) -> aspose.cells.PrintCommentsType:
        ...
    
    @export_comments_type.setter
    def export_comments_type(self, value : aspose.cells.PrintCommentsType):
        ...
    
    @property
    def disable_downlevel_revealed_comments(self) -> bool:
        ...
    
    @disable_downlevel_revealed_comments.setter
    def disable_downlevel_revealed_comments(self, value : bool):
        ...
    
    @property
    def is_exp_image_to_temp_dir(self) -> bool:
        ...
    
    @is_exp_image_to_temp_dir.setter
    def is_exp_image_to_temp_dir(self, value : bool):
        ...
    
    @property
    def image_scalable(self) -> bool:
        ...
    
    @image_scalable.setter
    def image_scalable(self, value : bool):
        ...
    
    @property
    def width_scalable(self) -> bool:
        ...
    
    @width_scalable.setter
    def width_scalable(self, value : bool):
        ...
    
    @property
    def export_single_tab(self) -> bool:
        ...
    
    @export_single_tab.setter
    def export_single_tab(self, value : bool):
        ...
    
    @property
    def export_images_as_base64(self) -> bool:
        ...
    
    @export_images_as_base64.setter
    def export_images_as_base64(self, value : bool):
        ...
    
    @property
    def export_active_worksheet_only(self) -> bool:
        ...
    
    @export_active_worksheet_only.setter
    def export_active_worksheet_only(self, value : bool):
        ...
    
    @property
    def export_print_area_only(self) -> bool:
        ...
    
    @export_print_area_only.setter
    def export_print_area_only(self, value : bool):
        ...
    
    @property
    def export_area(self) -> aspose.cells.CellArea:
        ...
    
    @export_area.setter
    def export_area(self, value : aspose.cells.CellArea):
        ...
    
    @property
    def parse_html_tag_in_cell(self) -> bool:
        ...
    
    @parse_html_tag_in_cell.setter
    def parse_html_tag_in_cell(self, value : bool):
        ...
    
    @property
    def html_cross_string_type(self) -> aspose.cells.HtmlCrossType:
        ...
    
    @html_cross_string_type.setter
    def html_cross_string_type(self, value : aspose.cells.HtmlCrossType):
        ...
    
    @property
    def hidden_col_display_type(self) -> aspose.cells.HtmlHiddenColDisplayType:
        ...
    
    @hidden_col_display_type.setter
    def hidden_col_display_type(self, value : aspose.cells.HtmlHiddenColDisplayType):
        ...
    
    @property
    def hidden_row_display_type(self) -> aspose.cells.HtmlHiddenRowDisplayType:
        ...
    
    @hidden_row_display_type.setter
    def hidden_row_display_type(self, value : aspose.cells.HtmlHiddenRowDisplayType):
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''If not set,use Encoding.UTF8 as default enconding type.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''If not set,use Encoding.UTF8 as default enconding type.'''
        ...
    
    @property
    def export_object_listener(self) -> aspose.cells.IExportObjectListener:
        ...
    
    @export_object_listener.setter
    def export_object_listener(self, value : aspose.cells.IExportObjectListener):
        ...
    
    @property
    def file_path_provider(self) -> aspose.cells.IFilePathProvider:
        ...
    
    @file_path_provider.setter
    def file_path_provider(self, value : aspose.cells.IFilePathProvider):
        ...
    
    @property
    def stream_provider(self) -> aspose.cells.IStreamProvider:
        ...
    
    @stream_provider.setter
    def stream_provider(self, value : aspose.cells.IStreamProvider):
        ...
    
    @property
    def image_options(self) -> aspose.cells.rendering.ImageOrPrintOptions:
        ...
    
    @property
    def save_as_single_file(self) -> bool:
        ...
    
    @save_as_single_file.setter
    def save_as_single_file(self, value : bool):
        ...
    
    @property
    def show_all_sheets(self) -> bool:
        ...
    
    @show_all_sheets.setter
    def show_all_sheets(self, value : bool):
        ...
    
    @property
    def export_page_headers(self) -> bool:
        ...
    
    @export_page_headers.setter
    def export_page_headers(self, value : bool):
        ...
    
    @property
    def export_page_footers(self) -> bool:
        ...
    
    @export_page_footers.setter
    def export_page_footers(self, value : bool):
        ...
    
    @property
    def export_hidden_worksheet(self) -> bool:
        ...
    
    @export_hidden_worksheet.setter
    def export_hidden_worksheet(self, value : bool):
        ...
    
    @property
    def presentation_preference(self) -> bool:
        ...
    
    @presentation_preference.setter
    def presentation_preference(self, value : bool):
        ...
    
    @property
    def cell_css_prefix(self) -> str:
        ...
    
    @cell_css_prefix.setter
    def cell_css_prefix(self, value : str):
        ...
    
    @property
    def table_css_id(self) -> str:
        ...
    
    @table_css_id.setter
    def table_css_id(self, value : str):
        ...
    
    @property
    def is_full_path_link(self) -> bool:
        ...
    
    @is_full_path_link.setter
    def is_full_path_link(self, value : bool):
        ...
    
    @property
    def export_worksheet_css_separately(self) -> bool:
        ...
    
    @export_worksheet_css_separately.setter
    def export_worksheet_css_separately(self, value : bool):
        ...
    
    @property
    def export_similar_border_style(self) -> bool:
        ...
    
    @export_similar_border_style.setter
    def export_similar_border_style(self, value : bool):
        ...
    
    @property
    def merge_empty_td_forcely(self) -> bool:
        ...
    
    @merge_empty_td_forcely.setter
    def merge_empty_td_forcely(self, value : bool):
        ...
    
    @property
    def export_cell_coordinate(self) -> bool:
        ...
    
    @export_cell_coordinate.setter
    def export_cell_coordinate(self, value : bool):
        ...
    
    @property
    def export_extra_headings(self) -> bool:
        ...
    
    @export_extra_headings.setter
    def export_extra_headings(self, value : bool):
        ...
    
    @property
    def export_headings(self) -> bool:
        ...
    
    @export_headings.setter
    def export_headings(self, value : bool):
        ...
    
    @property
    def export_row_column_headings(self) -> bool:
        ...
    
    @export_row_column_headings.setter
    def export_row_column_headings(self, value : bool):
        ...
    
    @property
    def export_formula(self) -> bool:
        ...
    
    @export_formula.setter
    def export_formula(self, value : bool):
        ...
    
    @property
    def add_tooltip_text(self) -> bool:
        ...
    
    @add_tooltip_text.setter
    def add_tooltip_text(self, value : bool):
        ...
    
    @property
    def export_grid_lines(self) -> bool:
        ...
    
    @export_grid_lines.setter
    def export_grid_lines(self, value : bool):
        ...
    
    @property
    def export_bogus_row_data(self) -> bool:
        ...
    
    @export_bogus_row_data.setter
    def export_bogus_row_data(self, value : bool):
        ...
    
    @property
    def exclude_unused_styles(self) -> bool:
        ...
    
    @exclude_unused_styles.setter
    def exclude_unused_styles(self, value : bool):
        ...
    
    @property
    def export_document_properties(self) -> bool:
        ...
    
    @export_document_properties.setter
    def export_document_properties(self, value : bool):
        ...
    
    @property
    def export_worksheet_properties(self) -> bool:
        ...
    
    @export_worksheet_properties.setter
    def export_worksheet_properties(self, value : bool):
        ...
    
    @property
    def export_workbook_properties(self) -> bool:
        ...
    
    @export_workbook_properties.setter
    def export_workbook_properties(self, value : bool):
        ...
    
    @property
    def export_frame_scripts_and_properties(self) -> bool:
        ...
    
    @export_frame_scripts_and_properties.setter
    def export_frame_scripts_and_properties(self, value : bool):
        ...
    
    @property
    def export_data_options(self) -> aspose.cells.HtmlExportDataOptions:
        ...
    
    @export_data_options.setter
    def export_data_options(self, value : aspose.cells.HtmlExportDataOptions):
        ...
    
    @property
    def link_target_type(self) -> aspose.cells.HtmlLinkTargetType:
        ...
    
    @link_target_type.setter
    def link_target_type(self, value : aspose.cells.HtmlLinkTargetType):
        ...
    
    ...

class Hyperlink:
    '''Encapsulates the object that represents a hyperlink.'''
    
    def delete(self):
        '''Deletes this hyperlink'''
        ...
    
    @property
    def address(self) -> str:
        '''Represents the address of a hyperlink.'''
        ...
    
    @address.setter
    def address(self, value : str):
        '''Represents the address of a hyperlink.'''
        ...
    
    @property
    def text_to_display(self) -> str:
        ...
    
    @text_to_display.setter
    def text_to_display(self, value : str):
        ...
    
    @property
    def area(self) -> aspose.cells.CellArea:
        '''Gets the range of hyperlink.'''
        ...
    
    @property
    def screen_tip(self) -> str:
        ...
    
    @screen_tip.setter
    def screen_tip(self, value : str):
        ...
    
    @property
    def link_type(self) -> aspose.cells.TargetModeType:
        ...
    
    ...

class HyperlinkCollection:
    '''Encapsulates a collection of :py:class:`aspose.cells.Hyperlink` objects.'''
    
    @overload
    def add(self, first_row : int, first_column : int, total_rows : int, total_columns : int, address : str) -> int:
        '''Adds a hyperlink to a specified cell or a range of cells.
        
        :param first_row: First row of the hyperlink range.
        :param first_column: First column of the hyperlink range.
        :param total_rows: Number of rows in this hyperlink range.
        :param total_columns: Number of columns of this hyperlink range.
        :param address: Address of the hyperlink.
        :returns: :py:class:`aspose.cells.Hyperlink` object index.'''
        ...
    
    @overload
    def add(self, cell_name : str, total_rows : int, total_columns : int, address : str) -> int:
        '''Adds a hyperlink to a specified cell or a range of cells.
        
        :param cell_name: Cell name.
        :param total_rows: Number of rows in this hyperlink range.
        :param total_columns: Number of columns of this hyperlink range.
        :param address: Address of the hyperlink.
        :returns: :py:class:`aspose.cells.Hyperlink` object index.'''
        ...
    
    @overload
    def add(self, start_cell_name : str, end_cell_name : str, address : str, text_to_display : str, screen_tip : str) -> int:
        '''Adds a hyperlink to a specified cell or a range of cells.
        
        :param start_cell_name: The top-left cell of the range.
        :param end_cell_name: The bottom-right cell of the range.
        :param address: Address of the hyperlink.
        :param text_to_display: The text to be displayed for the specified hyperlink.
        :param screen_tip: The screenTip text for the specified hyperlink.
        :returns: :py:class:`aspose.cells.Hyperlink` object index.'''
        ...
    
    @overload
    def copy_to(self, array : List[aspose.cells.Hyperlink]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.Hyperlink], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.Hyperlink, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.Hyperlink, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Hyperlink) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Hyperlink, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Hyperlink, index : int, count : int) -> int:
        ...
    
    def binary_search(self, item : aspose.cells.Hyperlink) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class ICellsDataTable:
    '''Represents data table.'''
    
    def before_first(self):
        '''Move the cursor to the front of this object, just before the first row.'''
        ...
    
    def next(self) -> bool:
        '''Moves the cursor down one row from its current position.
        
        :returns: if the new current row is valid; false if there are no more rows'''
        ...
    
    @property
    def columns(self) -> List[str]:
        '''Gets the columns' name.'''
        ...
    
    @property
    def count(self) -> int:
        '''Gets the count of the records. -1 for unknown records count.'''
        ...
    
    def __getitem__(self, key : int) -> any:
        '''Gets the data stored in the column specified by index.'''
        ...
    
    ...

class ICustomFunction:
    
    def calculate_custom_function(self, function_name : str, params_list : list, context_objects : list) -> any:
        ...
    
    ...

class ICustomParser:
    '''Allows users to add their custom value parser for parsing string values to other proper cell value object.'''
    
    def parse_object(self, value : str) -> any:
        '''Parses given string to proper value object.
        
        :param value: The string value to be parsed
        :returns: Parsed value object from given string. If given string cannot be parsed to proper value object, returns null.'''
        ...
    
    def get_format(self) -> str:
        '''Gets the formatting pattern corresponding to the parsed value by last invocation of :py:func:`aspose.cells.ICustomParser.parse_object`.'''
        ...
    
    ...

class IExportObjectListener:
    '''Allows users to manipulate objects while exporting.'''
    
    def export_object(self, e : aspose.cells.ExportObjectEvent) -> any:
        '''Export one object.
        
        :param e: The event triggered when one object needs to be exported.
        :returns: The information about the result of exporting object.
        
        *'''
        ...
    
    ...

class IFilePathProvider:
    '''Represents the exported file path provider.'''
    
    def get_full_name(self, sheet_name : str) -> str:
        '''Gets the full path of the file by Worksheet name when exporting Worksheet to html separately.
        So the references among the Worksheets can be exported correctly.
        
        :param sheet_name: Worksheet name
        :returns: the full path of the file'''
        ...
    
    ...

class ISmartMarkerCallBack:
    '''Represents callback interface of processing smartmarker.'''
    
    def process(self, sheet_index : int, row_index : int, col_index : int, table_name : str, column_name : str):
        '''Callback for processing a smart marker.
        
        :param sheet_index: The sheet index.
        :param row_index: The row index.
        :param col_index: The column index.
        :param table_name: The table name of smartmarker.
        :param column_name: The table name of smartmarker.'''
        ...
    
    ...

class IStreamProvider:
    '''Represents the exported stream provider.'''
    
    def init_stream(self, options : aspose.cells.StreamProviderOptions):
        '''Gets the stream.'''
        ...
    
    def close_stream(self, options : aspose.cells.StreamProviderOptions):
        '''Closes the stream.'''
        ...
    
    ...

class IWarningCallback:
    '''Callback interface of warning.'''
    
    def warning(self, warning_info : aspose.cells.WarningInfo):
        '''Our callback only needs to implement the "Warning" method.
        
        :param warning_info: warning info'''
        ...
    
    ...

class IconFilter:
    '''Represents icon filter.'''
    
    @property
    def icon_set_type(self) -> aspose.cells.IconSetType:
        ...
    
    @icon_set_type.setter
    def icon_set_type(self, value : aspose.cells.IconSetType):
        ...
    
    @property
    def icon_id(self) -> int:
        ...
    
    @icon_id.setter
    def icon_id(self, value : int):
        ...
    
    ...

class IconSet:
    '''Describe the IconSet conditional formatting rule.
    This conditional formatting rule applies icons to cells
    according to their values.'''
    
    @property
    def cf_icons(self) -> aspose.cells.ConditionalFormattingIconCollection:
        ...
    
    @property
    def cfvos(self) -> aspose.cells.ConditionalFormattingValueCollection:
        '''Get the CFValueObjects instance.'''
        ...
    
    @property
    def type(self) -> aspose.cells.IconSetType:
        '''Get or Set the icon set type to display.
        Setting the type will auto check if the current Cfvos's count is
        accord with the new type. If not accord, old Cfvos will be cleaned and
        default Cfvos will be added.'''
        ...
    
    @type.setter
    def type(self, value : aspose.cells.IconSetType):
        '''Get or Set the icon set type to display.
        Setting the type will auto check if the current Cfvos's count is
        accord with the new type. If not accord, old Cfvos will be cleaned and
        default Cfvos will be added.'''
        ...
    
    @property
    def is_custom(self) -> bool:
        ...
    
    @property
    def show_value(self) -> bool:
        ...
    
    @show_value.setter
    def show_value(self, value : bool):
        ...
    
    @property
    def reverse(self) -> bool:
        '''Get or set the flag indicating whether to reverses the default order of the icons in this icon set.
        Default value is false.'''
        ...
    
    @reverse.setter
    def reverse(self, value : bool):
        '''Get or set the flag indicating whether to reverses the default order of the icons in this icon set.
        Default value is false.'''
        ...
    
    ...

class ImageSaveOptions(SaveOptions):
    '''Represents image save options.
    For advanced usage, please use :py:class:`aspose.cells.rendering.WorkbookRender` or :py:class:`aspose.cells.rendering.SheetRender`.'''
    
    @property
    def save_format(self) -> aspose.cells.SaveFormat:
        ...
    
    @property
    def clear_data(self) -> bool:
        ...
    
    @clear_data.setter
    def clear_data(self, value : bool):
        ...
    
    @property
    def cached_file_folder(self) -> str:
        ...
    
    @cached_file_folder.setter
    def cached_file_folder(self, value : str):
        ...
    
    @property
    def validate_merged_areas(self) -> bool:
        ...
    
    @validate_merged_areas.setter
    def validate_merged_areas(self, value : bool):
        ...
    
    @property
    def merge_areas(self) -> bool:
        ...
    
    @merge_areas.setter
    def merge_areas(self, value : bool):
        ...
    
    @property
    def create_directory(self) -> bool:
        ...
    
    @create_directory.setter
    def create_directory(self, value : bool):
        ...
    
    @property
    def sort_names(self) -> bool:
        ...
    
    @sort_names.setter
    def sort_names(self, value : bool):
        ...
    
    @property
    def sort_external_names(self) -> bool:
        ...
    
    @sort_external_names.setter
    def sort_external_names(self, value : bool):
        ...
    
    @property
    def refresh_chart_cache(self) -> bool:
        ...
    
    @refresh_chart_cache.setter
    def refresh_chart_cache(self, value : bool):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def update_smart_art(self) -> bool:
        ...
    
    @update_smart_art.setter
    def update_smart_art(self, value : bool):
        ...
    
    @property
    def image_or_print_options(self) -> aspose.cells.rendering.ImageOrPrintOptions:
        ...
    
    @property
    def stream_provider(self) -> aspose.cells.IStreamProvider:
        ...
    
    @stream_provider.setter
    def stream_provider(self, value : aspose.cells.IStreamProvider):
        ...
    
    ...

class ImportTableOptions:
    '''Represents the options of importing data into cells.'''
    
    @property
    def convert_grid_style(self) -> bool:
        ...
    
    @convert_grid_style.setter
    def convert_grid_style(self, value : bool):
        ...
    
    @property
    def convert_numeric_data(self) -> bool:
        ...
    
    @convert_numeric_data.setter
    def convert_numeric_data(self, value : bool):
        ...
    
    @property
    def insert_rows(self) -> bool:
        ...
    
    @insert_rows.setter
    def insert_rows(self, value : bool):
        ...
    
    @property
    def shift_first_row_down(self) -> bool:
        ...
    
    @shift_first_row_down.setter
    def shift_first_row_down(self, value : bool):
        ...
    
    @property
    def is_field_name_shown(self) -> bool:
        ...
    
    @is_field_name_shown.setter
    def is_field_name_shown(self, value : bool):
        ...
    
    @property
    def export_caption_as_field_name(self) -> bool:
        ...
    
    @export_caption_as_field_name.setter
    def export_caption_as_field_name(self, value : bool):
        ...
    
    @property
    def date_format(self) -> str:
        ...
    
    @date_format.setter
    def date_format(self, value : str):
        ...
    
    @property
    def number_formats(self) -> List[str]:
        ...
    
    @number_formats.setter
    def number_formats(self, value : List[str]):
        ...
    
    @property
    def is_formulas(self) -> List[bool]:
        ...
    
    @is_formulas.setter
    def is_formulas(self, value : List[bool]):
        ...
    
    @property
    def total_rows(self) -> int:
        ...
    
    @total_rows.setter
    def total_rows(self, value : int):
        ...
    
    @property
    def total_columns(self) -> int:
        ...
    
    @total_columns.setter
    def total_columns(self, value : int):
        ...
    
    @property
    def column_indexes(self) -> List[int]:
        ...
    
    @column_indexes.setter
    def column_indexes(self, value : List[int]):
        ...
    
    @property
    def default_values(self) -> List[any]:
        ...
    
    @default_values.setter
    def default_values(self, value : List[any]):
        ...
    
    @property
    def is_html_string(self) -> bool:
        ...
    
    @is_html_string.setter
    def is_html_string(self, value : bool):
        ...
    
    @property
    def check_merged_cells(self) -> bool:
        ...
    
    @check_merged_cells.setter
    def check_merged_cells(self, value : bool):
        ...
    
    ...

class IndividualFontConfigs:
    '''Font configs for each :py:class:`aspose.cells.Workbook` object.'''
    
    def set_font_substitutes(self, original_font_name : str, substitute_font_names : List[str]):
        '''Font substitute names for given original font name.
        
        :param original_font_name: Original font name.
        :param substitute_font_names: List of font substitute names to be used if original font is not presented.'''
        ...
    
    def get_font_substitutes(self, original_font_name : str) -> List[str]:
        '''Returns array containing font substitute names to be used if original font is not presented.
        
        :param original_font_name: originalFontName
        :returns: An array containing font substitute names to be used if original font is not presented.'''
        ...
    
    def set_font_folder(self, font_folder : str, recursive : bool):
        '''Sets the fonts folder
        
        :param font_folder: The folder that contains TrueType fonts.
        :param recursive: Determines whether or not to scan subfolders.'''
        ...
    
    def set_font_folders(self, font_folders : List[str], recursive : bool):
        '''Sets the fonts folders
        
        :param font_folders: The folders that contains TrueType fonts.
        :param recursive: Determines whether or not to scan subfolders.'''
        ...
    
    def set_font_sources(self, sources : List[aspose.cells.FontSourceBase]):
        '''Sets the fonts sources.
        
        :param sources: An array of sources that contain TrueType fonts.'''
        ...
    
    def get_font_sources(self) -> List[aspose.cells.FontSourceBase]:
        '''Gets a copy of the array that contains the list of sources'''
        ...
    
    ...

class InsertOptions:
    '''Represents the options of inserting.'''
    
    @property
    def copy_format_type(self) -> aspose.cells.CopyFormatType:
        ...
    
    @copy_format_type.setter
    def copy_format_type(self, value : aspose.cells.CopyFormatType):
        ...
    
    @property
    def update_reference(self) -> bool:
        ...
    
    @update_reference.setter
    def update_reference(self, value : bool):
        ...
    
    ...

class InterruptMonitor(AbstractInterruptMonitor):
    '''Represents all operator about the interrupt.'''
    
    def interrupt(self):
        '''Interrupt the current operator.'''
        ...
    
    @property
    def is_interruption_requested(self) -> bool:
        ...
    
    @property
    def terminate_without_exception(self) -> bool:
        ...
    
    ...

class JsonLoadOptions(LoadOptions):
    '''Represents the options of loading json files'''
    
    def set_paper_size(self, type : aspose.cells.PaperSizeType):
        '''Sets the default print paper size from default printer's setting.
        
        :param type: The default paper size.'''
        ...
    
    @property
    def load_format(self) -> aspose.cells.LoadFormat:
        ...
    
    @property
    def password(self) -> str:
        '''Gets and set the password of the workbook.'''
        ...
    
    @password.setter
    def password(self, value : str):
        '''Gets and set the password of the workbook.'''
        ...
    
    @property
    def parsing_formula_on_open(self) -> bool:
        ...
    
    @parsing_formula_on_open.setter
    def parsing_formula_on_open(self, value : bool):
        ...
    
    @property
    def parsing_pivot_cached_records(self) -> bool:
        ...
    
    @parsing_pivot_cached_records.setter
    def parsing_pivot_cached_records(self, value : bool):
        ...
    
    @property
    def language_code(self) -> aspose.cells.CountryCode:
        ...
    
    @language_code.setter
    def language_code(self, value : aspose.cells.CountryCode):
        ...
    
    @property
    def region(self) -> aspose.cells.CountryCode:
        '''Gets the system regional settings based on CountryCode at the time the file was loaded.'''
        ...
    
    @region.setter
    def region(self, value : aspose.cells.CountryCode):
        '''Sets the system regional settings based on CountryCode at the time the file was loaded.'''
        ...
    
    @property
    def default_style_settings(self) -> aspose.cells.DefaultStyleSettings:
        ...
    
    @property
    def standard_font(self) -> str:
        ...
    
    @standard_font.setter
    def standard_font(self, value : str):
        ...
    
    @property
    def standard_font_size(self) -> float:
        ...
    
    @standard_font_size.setter
    def standard_font_size(self, value : float):
        ...
    
    @property
    def interrupt_monitor(self) -> aspose.cells.AbstractInterruptMonitor:
        ...
    
    @interrupt_monitor.setter
    def interrupt_monitor(self, value : aspose.cells.AbstractInterruptMonitor):
        ...
    
    @property
    def ignore_not_printed(self) -> bool:
        ...
    
    @ignore_not_printed.setter
    def ignore_not_printed(self, value : bool):
        ...
    
    @property
    def check_data_valid(self) -> bool:
        ...
    
    @check_data_valid.setter
    def check_data_valid(self, value : bool):
        ...
    
    @property
    def check_excel_restriction(self) -> bool:
        ...
    
    @check_excel_restriction.setter
    def check_excel_restriction(self, value : bool):
        ...
    
    @property
    def keep_unparsed_data(self) -> bool:
        ...
    
    @keep_unparsed_data.setter
    def keep_unparsed_data(self, value : bool):
        ...
    
    @property
    def load_filter(self) -> aspose.cells.LoadFilter:
        ...
    
    @load_filter.setter
    def load_filter(self, value : aspose.cells.LoadFilter):
        ...
    
    @property
    def light_cells_data_handler(self) -> aspose.cells.LightCellsDataHandler:
        ...
    
    @light_cells_data_handler.setter
    def light_cells_data_handler(self, value : aspose.cells.LightCellsDataHandler):
        ...
    
    @property
    def memory_setting(self) -> aspose.cells.MemorySetting:
        ...
    
    @memory_setting.setter
    def memory_setting(self, value : aspose.cells.MemorySetting):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def auto_fitter_options(self) -> aspose.cells.AutoFitterOptions:
        ...
    
    @auto_fitter_options.setter
    def auto_fitter_options(self, value : aspose.cells.AutoFitterOptions):
        ...
    
    @property
    def auto_filter(self) -> bool:
        ...
    
    @auto_filter.setter
    def auto_filter(self, value : bool):
        ...
    
    @property
    def font_configs(self) -> aspose.cells.IndividualFontConfigs:
        ...
    
    @font_configs.setter
    def font_configs(self, value : aspose.cells.IndividualFontConfigs):
        ...
    
    @property
    def start_cell(self) -> str:
        ...
    
    @start_cell.setter
    def start_cell(self, value : str):
        ...
    
    @property
    def layout_options(self) -> aspose.cells.utility.JsonLayoutOptions:
        ...
    
    @layout_options.setter
    def layout_options(self, value : aspose.cells.utility.JsonLayoutOptions):
        ...
    
    @property
    def multiple_worksheets(self) -> bool:
        ...
    
    @multiple_worksheets.setter
    def multiple_worksheets(self, value : bool):
        ...
    
    ...

class JsonSaveOptions(SaveOptions):
    '''Represents the options of saving the workbook as a json file.'''
    
    @property
    def save_format(self) -> aspose.cells.SaveFormat:
        ...
    
    @property
    def clear_data(self) -> bool:
        ...
    
    @clear_data.setter
    def clear_data(self, value : bool):
        ...
    
    @property
    def cached_file_folder(self) -> str:
        ...
    
    @cached_file_folder.setter
    def cached_file_folder(self, value : str):
        ...
    
    @property
    def validate_merged_areas(self) -> bool:
        ...
    
    @validate_merged_areas.setter
    def validate_merged_areas(self, value : bool):
        ...
    
    @property
    def merge_areas(self) -> bool:
        ...
    
    @merge_areas.setter
    def merge_areas(self, value : bool):
        ...
    
    @property
    def create_directory(self) -> bool:
        ...
    
    @create_directory.setter
    def create_directory(self, value : bool):
        ...
    
    @property
    def sort_names(self) -> bool:
        ...
    
    @sort_names.setter
    def sort_names(self, value : bool):
        ...
    
    @property
    def sort_external_names(self) -> bool:
        ...
    
    @sort_external_names.setter
    def sort_external_names(self, value : bool):
        ...
    
    @property
    def refresh_chart_cache(self) -> bool:
        ...
    
    @refresh_chart_cache.setter
    def refresh_chart_cache(self, value : bool):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def update_smart_art(self) -> bool:
        ...
    
    @update_smart_art.setter
    def update_smart_art(self, value : bool):
        ...
    
    @property
    def export_hyperlink_type(self) -> aspose.cells.json.JsonExportHyperlinkType:
        ...
    
    @export_hyperlink_type.setter
    def export_hyperlink_type(self, value : aspose.cells.json.JsonExportHyperlinkType):
        ...
    
    @property
    def skip_empty_rows(self) -> bool:
        ...
    
    @skip_empty_rows.setter
    def skip_empty_rows(self, value : bool):
        ...
    
    @property
    def sheet_indexes(self) -> List[int]:
        ...
    
    @sheet_indexes.setter
    def sheet_indexes(self, value : List[int]):
        ...
    
    @property
    def export_area(self) -> aspose.cells.CellArea:
        ...
    
    @export_area.setter
    def export_area(self, value : aspose.cells.CellArea):
        ...
    
    @property
    def has_header_row(self) -> bool:
        ...
    
    @has_header_row.setter
    def has_header_row(self, value : bool):
        ...
    
    @property
    def export_as_string(self) -> bool:
        ...
    
    @export_as_string.setter
    def export_as_string(self, value : bool):
        ...
    
    @property
    def indent(self) -> str:
        '''Indicates the indent.'''
        ...
    
    @indent.setter
    def indent(self, value : str):
        '''Indicates the indent.'''
        ...
    
    @property
    def export_nested_structure(self) -> bool:
        ...
    
    @export_nested_structure.setter
    def export_nested_structure(self, value : bool):
        ...
    
    @property
    def export_empty_cells(self) -> bool:
        ...
    
    @export_empty_cells.setter
    def export_empty_cells(self, value : bool):
        ...
    
    @property
    def always_export_as_json_object(self) -> bool:
        ...
    
    @always_export_as_json_object.setter
    def always_export_as_json_object(self, value : bool):
        ...
    
    ...

class License:
    '''Provides methods to license the component.'''
    
    @overload
    def set_license(self, license_name : str):
        '''Licenses the component.'''
        ...
    
    @overload
    def set_license(self, stream : io.RawIOBase):
        '''Licenses the component.
        
        :param stream: A stream that contains the license.'''
        ...
    
    ...

class LightCellsDataHandler:
    '''Represents cells data handler for reading large spreadsheet files in light weight mode.'''
    
    def start_sheet(self, sheet : aspose.cells.Worksheet) -> bool:
        '''Starts to process a worksheet.
        
        :param sheet: the worksheet to read cells data.
        :returns: whether this sheet's cells data needs to be processed. false to ignore this sheet.'''
        ...
    
    def start_row(self, row_index : int) -> bool:
        '''Prepares to process a row.
        
        :param row_index: the index of next row to be processed
        :returns: whether this row(properties or cells data) needs to be processed. false to ignore this row and its cells and check the next row.'''
        ...
    
    def process_row(self, row : aspose.cells.Row) -> bool:
        '''Starts to process one row.
        
        :param row: Row object which is being processed currently.
        :returns: whether this row's cells need to be processed. false to ignore all cells in this row.'''
        ...
    
    def start_cell(self, column_index : int) -> bool:
        '''Prepares to process a cell.
        
        :param column_index: column index of the cell to be processed
        :returns: whether this cell needs to be processed. false to ignore the cell and check the next one until reach the end of cells data of current row'''
        ...
    
    def process_cell(self, cell : aspose.cells.Cell) -> bool:
        '''Starts to process one cell.
        
        :param cell: Cell object which is being processed currently
        :returns: whether this cell needs to be kept in cells model of current sheet.
        Commonly it should be false so that all cells will not be kept in memory after being processed and then memory be saved.
        For some special purpose such as user needs to access some cells later after the whole workbook having been processed,
        user can make this method return true to keep those special cells in Cells model and access them later by APIs such as Cells[row, column].
        However, keeping cells data in Cells model will requires more memory and if all cells are kept then reading template file
        in LightCells mode will become same with reading it in normal way.'''
        ...
    
    ...

class LightCellsDataProvider:
    '''Represents Data provider for saving large spreadsheet files in light weight mode.'''
    
    def start_sheet(self, sheet_index : int) -> bool:
        '''Starts to save a worksheet.
        
        :param sheet_index: index of current sheet to be saved.
        :returns: true if this provider will provide data for the given sheet; false if given sheet should use its normal data model(Cells).'''
        ...
    
    def next_row(self) -> int:
        '''Gets the next row to be saved.
        
        :returns: the next row index to be saved. -1 means the end of current sheet data has been reached and no further row of current sheet to be saved.'''
        ...
    
    def start_row(self, row : aspose.cells.Row):
        '''Starts to save data of one row.
        
        :param row: Row object for implementation to fill data. Its row index is the returned value of latest call of :py:func:`aspose.cells.LightCellsDataProvider.next_row`.
        If the row has been initialized in the inner cells model, the existing row object will be used.
        Otherwise a temporary Row object will be used for implementation to fill data.'''
        ...
    
    def next_cell(self) -> int:
        '''Gets next cell to be saved.
        
        :returns: column index of the next cell to be saved. -1 means the end of current row data has been reached and no further cell of current row to be saved.'''
        ...
    
    def start_cell(self, cell : aspose.cells.Cell):
        '''Starts to save data of one cell.
        
        :param cell: Cell object for implementation to fill data. Its column index is the returned value of latest call of :py:func:`aspose.cells.LightCellsDataProvider.next_cell`.
        If the cell has been initialized in the inner cells model, the existed cell object will be used.
        Otherwise a temporary Cell object will be used for implementation to fill data.'''
        ...
    
    def is_gather_string(self) -> bool:
        '''Checks whether the current string value of cell needs to be gathered into a global pool.
        
        :returns: true if string value need to be gathered into a global pool for the resultant file.'''
        ...
    
    ...

class LoadFilter:
    '''Represents the filter that provides options for loading data when loading workbook from template.'''
    
    def start_sheet(self, sheet : aspose.cells.Worksheet):
        '''Prepares filter options before loading given worksheet.
        User's implementation of LoadFilter can change the LoadDataFilterOptions here
        to denote how to load data for this worksheet.
        
        :param sheet: The worksheet to be loaded.
        There are only few properties can be used for the given worksheet object here
        because most data and properties have not been loaded. The available properties are:
        Name, Index, VisibilityType'''
        ...
    
    @property
    def load_data_filter_options(self) -> aspose.cells.LoadDataFilterOptions:
        ...
    
    @load_data_filter_options.setter
    def load_data_filter_options(self, value : aspose.cells.LoadDataFilterOptions):
        ...
    
    @property
    def sheets_in_loading_order(self) -> List[int]:
        ...
    
    ...

class LoadOptions:
    '''Represents the options of loading the file.'''
    
    def set_paper_size(self, type : aspose.cells.PaperSizeType):
        '''Sets the default print paper size from default printer's setting.
        
        :param type: The default paper size.'''
        ...
    
    @property
    def load_format(self) -> aspose.cells.LoadFormat:
        ...
    
    @property
    def password(self) -> str:
        '''Gets and set the password of the workbook.'''
        ...
    
    @password.setter
    def password(self, value : str):
        '''Gets and set the password of the workbook.'''
        ...
    
    @property
    def parsing_formula_on_open(self) -> bool:
        ...
    
    @parsing_formula_on_open.setter
    def parsing_formula_on_open(self, value : bool):
        ...
    
    @property
    def parsing_pivot_cached_records(self) -> bool:
        ...
    
    @parsing_pivot_cached_records.setter
    def parsing_pivot_cached_records(self, value : bool):
        ...
    
    @property
    def language_code(self) -> aspose.cells.CountryCode:
        ...
    
    @language_code.setter
    def language_code(self, value : aspose.cells.CountryCode):
        ...
    
    @property
    def region(self) -> aspose.cells.CountryCode:
        '''Gets the system regional settings based on CountryCode at the time the file was loaded.'''
        ...
    
    @region.setter
    def region(self, value : aspose.cells.CountryCode):
        '''Sets the system regional settings based on CountryCode at the time the file was loaded.'''
        ...
    
    @property
    def default_style_settings(self) -> aspose.cells.DefaultStyleSettings:
        ...
    
    @property
    def standard_font(self) -> str:
        ...
    
    @standard_font.setter
    def standard_font(self, value : str):
        ...
    
    @property
    def standard_font_size(self) -> float:
        ...
    
    @standard_font_size.setter
    def standard_font_size(self, value : float):
        ...
    
    @property
    def interrupt_monitor(self) -> aspose.cells.AbstractInterruptMonitor:
        ...
    
    @interrupt_monitor.setter
    def interrupt_monitor(self, value : aspose.cells.AbstractInterruptMonitor):
        ...
    
    @property
    def ignore_not_printed(self) -> bool:
        ...
    
    @ignore_not_printed.setter
    def ignore_not_printed(self, value : bool):
        ...
    
    @property
    def check_data_valid(self) -> bool:
        ...
    
    @check_data_valid.setter
    def check_data_valid(self, value : bool):
        ...
    
    @property
    def check_excel_restriction(self) -> bool:
        ...
    
    @check_excel_restriction.setter
    def check_excel_restriction(self, value : bool):
        ...
    
    @property
    def keep_unparsed_data(self) -> bool:
        ...
    
    @keep_unparsed_data.setter
    def keep_unparsed_data(self, value : bool):
        ...
    
    @property
    def load_filter(self) -> aspose.cells.LoadFilter:
        ...
    
    @load_filter.setter
    def load_filter(self, value : aspose.cells.LoadFilter):
        ...
    
    @property
    def light_cells_data_handler(self) -> aspose.cells.LightCellsDataHandler:
        ...
    
    @light_cells_data_handler.setter
    def light_cells_data_handler(self, value : aspose.cells.LightCellsDataHandler):
        ...
    
    @property
    def memory_setting(self) -> aspose.cells.MemorySetting:
        ...
    
    @memory_setting.setter
    def memory_setting(self, value : aspose.cells.MemorySetting):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def auto_fitter_options(self) -> aspose.cells.AutoFitterOptions:
        ...
    
    @auto_fitter_options.setter
    def auto_fitter_options(self, value : aspose.cells.AutoFitterOptions):
        ...
    
    @property
    def auto_filter(self) -> bool:
        ...
    
    @auto_filter.setter
    def auto_filter(self, value : bool):
        ...
    
    @property
    def font_configs(self) -> aspose.cells.IndividualFontConfigs:
        ...
    
    @font_configs.setter
    def font_configs(self, value : aspose.cells.IndividualFontConfigs):
        ...
    
    ...

class MarkdownSaveOptions(SaveOptions):
    '''Represents the save options for markdown.'''
    
    @property
    def save_format(self) -> aspose.cells.SaveFormat:
        ...
    
    @property
    def clear_data(self) -> bool:
        ...
    
    @clear_data.setter
    def clear_data(self, value : bool):
        ...
    
    @property
    def cached_file_folder(self) -> str:
        ...
    
    @cached_file_folder.setter
    def cached_file_folder(self, value : str):
        ...
    
    @property
    def validate_merged_areas(self) -> bool:
        ...
    
    @validate_merged_areas.setter
    def validate_merged_areas(self, value : bool):
        ...
    
    @property
    def merge_areas(self) -> bool:
        ...
    
    @merge_areas.setter
    def merge_areas(self, value : bool):
        ...
    
    @property
    def create_directory(self) -> bool:
        ...
    
    @create_directory.setter
    def create_directory(self, value : bool):
        ...
    
    @property
    def sort_names(self) -> bool:
        ...
    
    @sort_names.setter
    def sort_names(self, value : bool):
        ...
    
    @property
    def sort_external_names(self) -> bool:
        ...
    
    @sort_external_names.setter
    def sort_external_names(self, value : bool):
        ...
    
    @property
    def refresh_chart_cache(self) -> bool:
        ...
    
    @refresh_chart_cache.setter
    def refresh_chart_cache(self, value : bool):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def update_smart_art(self) -> bool:
        ...
    
    @update_smart_art.setter
    def update_smart_art(self, value : bool):
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets and sets the default encoding.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Gets and sets the default encoding.'''
        ...
    
    @property
    def format_strategy(self) -> aspose.cells.CellValueFormatStrategy:
        ...
    
    @format_strategy.setter
    def format_strategy(self, value : aspose.cells.CellValueFormatStrategy):
        ...
    
    @property
    def light_cells_data_provider(self) -> aspose.cells.LightCellsDataProvider:
        ...
    
    @light_cells_data_provider.setter
    def light_cells_data_provider(self, value : aspose.cells.LightCellsDataProvider):
        ...
    
    @property
    def line_separator(self) -> str:
        ...
    
    @line_separator.setter
    def line_separator(self, value : str):
        ...
    
    ...

class MemoryFontSource(FontSourceBase):
    '''Represents the single TrueType font file stored in memory.'''
    
    @property
    def type(self) -> aspose.cells.FontSourceType:
        '''Returns the type of the font source.'''
        ...
    
    @property
    def font_data(self) -> bytes:
        ...
    
    ...

class Metered:
    '''Provides methods to set metered key.'''
    
    def set_metered_key(self, public_key : str, private_key : str):
        '''Sets metered public and private key.
        If you purchase metered license, when start application, this API should be called, normally, this is enough. However, if always fail to upload consumption data and exceed 24 hours, the license will be set to evaluation status, to avoid such case, you should regularly check the license status, if it is evaluation status, call this API again.
        
        :param public_key: public key
        :param private_key: private key'''
        ...
    
    @staticmethod
    def get_consumption_quantity() -> float:
        '''Gets consumption file size
        
        :returns: consumption quantity'''
        ...
    
    @staticmethod
    def get_consumption_credit() -> float:
        '''Gets consumption credit
        
        :returns: consumption quantity'''
        ...
    
    ...

class MultipleFilterCollection:
    '''Represents the multiple filter collection.'''
    
    def add(self, filter : str):
        '''Adds string filter.
        
        :param filter: The filter data.'''
        ...
    
    @property
    def match_blank(self) -> bool:
        ...
    
    @match_blank.setter
    def match_blank(self, value : bool):
        ...
    
    ...

class Name:
    '''Represents a defined name for a range of cells.'''
    
    @overload
    def get_refers_to(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Get the reference of this Name.
        
        :param is_r1c1: Whether the reference needs to be formatted as R1C1.
        :param is_local: Whether the reference needs to be formatted by locale.'''
        ...
    
    @overload
    def get_refers_to(self, is_r1c1 : bool, is_local : bool, row : int, column : int) -> str:
        '''Get the reference of this Name based on specified cell.
        
        :param is_r1c1: Whether the reference needs to be formatted as R1C1.
        :param is_local: Whether the reference needs to be formatted by locale.
        :param row: The row index of the cell.
        :param column: The column index of the cell.'''
        ...
    
    @overload
    def get_ranges(self) -> List[aspose.cells.Range]:
        '''Gets all ranges referred by this name.
        
        :returns: All ranges.'''
        ...
    
    @overload
    def get_ranges(self, recalculate : bool) -> List[aspose.cells.Range]:
        '''Gets all ranges referred by this name.
        
        :param recalculate: whether recalculate it if this name has been calculated before this invocation.
        :returns: All ranges.'''
        ...
    
    @overload
    def get_range(self) -> aspose.cells.Range:
        '''Gets the range if this name refers to a range.
        
        :returns: The range.'''
        ...
    
    @overload
    def get_range(self, recalculate : bool) -> aspose.cells.Range:
        '''Gets the range if this name refers to a range
        
        :param recalculate: whether recalculate it if this name has been calculated before this invocation.
        :returns: The range.'''
        ...
    
    @overload
    def get_range(self, sheet_index : int, row : int, column : int) -> aspose.cells.Range:
        '''Gets the range if this name refers to a range.
        If the reference of this name is not absolute, the range may be different for different cell.
        
        :param sheet_index: The according sheet index.
        :param row: The according row index.
        :param column: The according column index
        :returns: The range.'''
        ...
    
    def set_refers_to(self, refers_to : str, is_r1c1 : bool, is_local : bool):
        '''Set the reference of this Name.
        
        :param refers_to: The reference.
        :param is_r1c1: Whether the reference is R1C1 format.
        :param is_local: Whether the reference is locale formatted.'''
        ...
    
    def get_referred_areas(self, recalculate : bool) -> List[aspose.cells.ReferredArea]:
        '''Gets all references referred by this name.
        
        :param recalculate: whether recalculate it if this name has been calculated before this invocation.
        :returns: All ranges.'''
        ...
    
    @property
    def comment(self) -> str:
        '''Gets and sets the comment of the name.
        Only applies for Excel 2007.'''
        ...
    
    @comment.setter
    def comment(self, value : str):
        '''Gets and sets the comment of the name.
        Only applies for Excel 2007.'''
        ...
    
    @property
    def text(self) -> str:
        '''Gets the name text of the object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Gets the name text of the object.'''
        ...
    
    @property
    def full_text(self) -> str:
        ...
    
    @property
    def refers_to(self) -> str:
        ...
    
    @refers_to.setter
    def refers_to(self, value : str):
        ...
    
    @property
    def r1c1_refers_to(self) -> str:
        ...
    
    @r1c1_refers_to.setter
    def r1c1_refers_to(self, value : str):
        ...
    
    @property
    def is_referred(self) -> bool:
        ...
    
    @property
    def is_visible(self) -> bool:
        ...
    
    @is_visible.setter
    def is_visible(self, value : bool):
        ...
    
    @property
    def sheet_index(self) -> int:
        ...
    
    @sheet_index.setter
    def sheet_index(self, value : int):
        ...
    
    ...

class NameCollection:
    '''Represents a collection of all the :py:class:`aspose.cells.Name` objects in the spreadsheet.'''
    
    @overload
    def get(self, index : int) -> aspose.cells.Name:
        '''Add API for Python Via .Net.since this[int index] is unsupported
        
        :param index: The zero based index of the element.'''
        ...
    
    @overload
    def get(self, text : str) -> aspose.cells.Name:
        '''Add API for Python Via .Net.since this[string text] is unsupported
        
        :param text: Name text.'''
        ...
    
    @overload
    def copy_to(self, array : List[aspose.cells.Name]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.Name], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.Name, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.Name, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Name) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Name, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Name, index : int, count : int) -> int:
        ...
    
    def add(self, text : str) -> int:
        '''Defines a new name.
        
        :param text: The text to use as the name.
        :returns: :py:class:`aspose.cells.Name` object index.'''
        ...
    
    def filter(self, type : aspose.cells.NameScopeType, sheet_index : int) -> List[aspose.cells.Name]:
        '''Gets all defined name by scope.
        
        :param type: The scope type.
        :param sheet_index: The sheet index.
        Only effects when scope type is :py:attr:`aspose.cells.NameScopeType.WORKSHEET`'''
        ...
    
    def remove_duplicate_names(self):
        '''Remove the duplicate defined names'''
        ...
    
    def binary_search(self, item : aspose.cells.Name) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class NegativeBarFormat:
    '''Represents the color settings of the data bars for negative values that are defined by a data bar conditional formatting rule.'''
    
    @property
    def border_color(self) -> aspose.pydrawing.Color:
        ...
    
    @border_color.setter
    def border_color(self, value : aspose.pydrawing.Color):
        ...
    
    @property
    def border_color_type(self) -> aspose.cells.DataBarNegativeColorType:
        ...
    
    @border_color_type.setter
    def border_color_type(self, value : aspose.cells.DataBarNegativeColorType):
        ...
    
    @property
    def color(self) -> aspose.pydrawing.Color:
        '''Gets a FormatColor object that you can use to specify the fill color for negative data bars.'''
        ...
    
    @color.setter
    def color(self, value : aspose.pydrawing.Color):
        '''Sets a FormatColor object that you can use to specify the fill color for negative data bars.'''
        ...
    
    @property
    def color_type(self) -> aspose.cells.DataBarNegativeColorType:
        ...
    
    @color_type.setter
    def color_type(self, value : aspose.cells.DataBarNegativeColorType):
        ...
    
    ...

class OdsLoadOptions(LoadOptions):
    '''Represents the options of loading ods file.'''
    
    def set_paper_size(self, type : aspose.cells.PaperSizeType):
        '''Sets the default print paper size from default printer's setting.
        
        :param type: The default paper size.'''
        ...
    
    @property
    def load_format(self) -> aspose.cells.LoadFormat:
        ...
    
    @property
    def password(self) -> str:
        '''Gets and set the password of the workbook.'''
        ...
    
    @password.setter
    def password(self, value : str):
        '''Gets and set the password of the workbook.'''
        ...
    
    @property
    def parsing_formula_on_open(self) -> bool:
        ...
    
    @parsing_formula_on_open.setter
    def parsing_formula_on_open(self, value : bool):
        ...
    
    @property
    def parsing_pivot_cached_records(self) -> bool:
        ...
    
    @parsing_pivot_cached_records.setter
    def parsing_pivot_cached_records(self, value : bool):
        ...
    
    @property
    def language_code(self) -> aspose.cells.CountryCode:
        ...
    
    @language_code.setter
    def language_code(self, value : aspose.cells.CountryCode):
        ...
    
    @property
    def region(self) -> aspose.cells.CountryCode:
        '''Gets the system regional settings based on CountryCode at the time the file was loaded.'''
        ...
    
    @region.setter
    def region(self, value : aspose.cells.CountryCode):
        '''Sets the system regional settings based on CountryCode at the time the file was loaded.'''
        ...
    
    @property
    def default_style_settings(self) -> aspose.cells.DefaultStyleSettings:
        ...
    
    @property
    def standard_font(self) -> str:
        ...
    
    @standard_font.setter
    def standard_font(self, value : str):
        ...
    
    @property
    def standard_font_size(self) -> float:
        ...
    
    @standard_font_size.setter
    def standard_font_size(self, value : float):
        ...
    
    @property
    def interrupt_monitor(self) -> aspose.cells.AbstractInterruptMonitor:
        ...
    
    @interrupt_monitor.setter
    def interrupt_monitor(self, value : aspose.cells.AbstractInterruptMonitor):
        ...
    
    @property
    def ignore_not_printed(self) -> bool:
        ...
    
    @ignore_not_printed.setter
    def ignore_not_printed(self, value : bool):
        ...
    
    @property
    def check_data_valid(self) -> bool:
        ...
    
    @check_data_valid.setter
    def check_data_valid(self, value : bool):
        ...
    
    @property
    def check_excel_restriction(self) -> bool:
        ...
    
    @check_excel_restriction.setter
    def check_excel_restriction(self, value : bool):
        ...
    
    @property
    def keep_unparsed_data(self) -> bool:
        ...
    
    @keep_unparsed_data.setter
    def keep_unparsed_data(self, value : bool):
        ...
    
    @property
    def load_filter(self) -> aspose.cells.LoadFilter:
        ...
    
    @load_filter.setter
    def load_filter(self, value : aspose.cells.LoadFilter):
        ...
    
    @property
    def light_cells_data_handler(self) -> aspose.cells.LightCellsDataHandler:
        ...
    
    @light_cells_data_handler.setter
    def light_cells_data_handler(self, value : aspose.cells.LightCellsDataHandler):
        ...
    
    @property
    def memory_setting(self) -> aspose.cells.MemorySetting:
        ...
    
    @memory_setting.setter
    def memory_setting(self, value : aspose.cells.MemorySetting):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def auto_fitter_options(self) -> aspose.cells.AutoFitterOptions:
        ...
    
    @auto_fitter_options.setter
    def auto_fitter_options(self, value : aspose.cells.AutoFitterOptions):
        ...
    
    @property
    def auto_filter(self) -> bool:
        ...
    
    @auto_filter.setter
    def auto_filter(self, value : bool):
        ...
    
    @property
    def font_configs(self) -> aspose.cells.IndividualFontConfigs:
        ...
    
    @font_configs.setter
    def font_configs(self, value : aspose.cells.IndividualFontConfigs):
        ...
    
    @property
    def apply_excel_default_style_to_hyperlink(self) -> bool:
        ...
    
    @apply_excel_default_style_to_hyperlink.setter
    def apply_excel_default_style_to_hyperlink(self, value : bool):
        ...
    
    @property
    def refresh_pivot_tables(self) -> bool:
        ...
    
    @refresh_pivot_tables.setter
    def refresh_pivot_tables(self, value : bool):
        ...
    
    ...

class OdsSaveOptions(SaveOptions):
    '''Represents the options of saving ods file.'''
    
    @property
    def save_format(self) -> aspose.cells.SaveFormat:
        ...
    
    @property
    def clear_data(self) -> bool:
        ...
    
    @clear_data.setter
    def clear_data(self, value : bool):
        ...
    
    @property
    def cached_file_folder(self) -> str:
        ...
    
    @cached_file_folder.setter
    def cached_file_folder(self, value : str):
        ...
    
    @property
    def validate_merged_areas(self) -> bool:
        ...
    
    @validate_merged_areas.setter
    def validate_merged_areas(self, value : bool):
        ...
    
    @property
    def merge_areas(self) -> bool:
        ...
    
    @merge_areas.setter
    def merge_areas(self, value : bool):
        ...
    
    @property
    def create_directory(self) -> bool:
        ...
    
    @create_directory.setter
    def create_directory(self, value : bool):
        ...
    
    @property
    def sort_names(self) -> bool:
        ...
    
    @sort_names.setter
    def sort_names(self, value : bool):
        ...
    
    @property
    def sort_external_names(self) -> bool:
        ...
    
    @sort_external_names.setter
    def sort_external_names(self, value : bool):
        ...
    
    @property
    def refresh_chart_cache(self) -> bool:
        ...
    
    @refresh_chart_cache.setter
    def refresh_chart_cache(self, value : bool):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def update_smart_art(self) -> bool:
        ...
    
    @update_smart_art.setter
    def update_smart_art(self, value : bool):
        ...
    
    @property
    def generator_type(self) -> aspose.cells.ods.OdsGeneratorType:
        ...
    
    @generator_type.setter
    def generator_type(self, value : aspose.cells.ods.OdsGeneratorType):
        ...
    
    @property
    def is_strict_schema11(self) -> bool:
        ...
    
    @is_strict_schema11.setter
    def is_strict_schema11(self, value : bool):
        ...
    
    ...

class OoxmlSaveOptions(SaveOptions):
    '''Represents the options of saving office open xml file.'''
    
    @property
    def save_format(self) -> aspose.cells.SaveFormat:
        ...
    
    @property
    def clear_data(self) -> bool:
        ...
    
    @clear_data.setter
    def clear_data(self, value : bool):
        ...
    
    @property
    def cached_file_folder(self) -> str:
        ...
    
    @cached_file_folder.setter
    def cached_file_folder(self, value : str):
        ...
    
    @property
    def validate_merged_areas(self) -> bool:
        ...
    
    @validate_merged_areas.setter
    def validate_merged_areas(self, value : bool):
        ...
    
    @property
    def merge_areas(self) -> bool:
        ...
    
    @merge_areas.setter
    def merge_areas(self, value : bool):
        ...
    
    @property
    def create_directory(self) -> bool:
        ...
    
    @create_directory.setter
    def create_directory(self, value : bool):
        ...
    
    @property
    def sort_names(self) -> bool:
        ...
    
    @sort_names.setter
    def sort_names(self, value : bool):
        ...
    
    @property
    def sort_external_names(self) -> bool:
        ...
    
    @sort_external_names.setter
    def sort_external_names(self, value : bool):
        ...
    
    @property
    def refresh_chart_cache(self) -> bool:
        ...
    
    @refresh_chart_cache.setter
    def refresh_chart_cache(self, value : bool):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def update_smart_art(self) -> bool:
        ...
    
    @update_smart_art.setter
    def update_smart_art(self, value : bool):
        ...
    
    @property
    def export_cell_name(self) -> bool:
        ...
    
    @export_cell_name.setter
    def export_cell_name(self, value : bool):
        ...
    
    @property
    def light_cells_data_provider(self) -> aspose.cells.LightCellsDataProvider:
        ...
    
    @light_cells_data_provider.setter
    def light_cells_data_provider(self, value : aspose.cells.LightCellsDataProvider):
        ...
    
    @property
    def update_zoom(self) -> bool:
        ...
    
    @update_zoom.setter
    def update_zoom(self, value : bool):
        ...
    
    @property
    def enable_zip64(self) -> bool:
        ...
    
    @enable_zip64.setter
    def enable_zip64(self, value : bool):
        ...
    
    @property
    def embed_ooxml_as_ole_object(self) -> bool:
        ...
    
    @embed_ooxml_as_ole_object.setter
    def embed_ooxml_as_ole_object(self, value : bool):
        ...
    
    @property
    def compression_type(self) -> aspose.cells.OoxmlCompressionType:
        ...
    
    @compression_type.setter
    def compression_type(self, value : aspose.cells.OoxmlCompressionType):
        ...
    
    ...

class Outline:
    '''Represents an outline on a worksheet.'''
    
    @property
    def summary_row_below(self) -> bool:
        ...
    
    @summary_row_below.setter
    def summary_row_below(self, value : bool):
        ...
    
    @property
    def summary_column_right(self) -> bool:
        ...
    
    @summary_column_right.setter
    def summary_column_right(self, value : bool):
        ...
    
    ...

class PageSetup:
    '''Encapsulates the object that represents the page setup description.
    The PageSetup object contains all page setup options.'''
    
    @overload
    def get_picture(self, is_header : bool, section : int) -> aspose.cells.drawing.Picture:
        '''Gets the :py:class:`aspose.cells.drawing.Picture` object of the header / footer.
        
        :param is_header: Indicates whether it is in the header or footer.
        :param section: 0: Left Section, 1: Center Section, 2: Right Section.
        :returns: Returns :py:class:`aspose.cells.drawing.Picture` object.
        Returns null if there is no picture.'''
        ...
    
    @overload
    def get_picture(self, is_first : bool, is_even : bool, is_header : bool, section : int) -> aspose.cells.drawing.Picture:
        '''Gets the :py:class:`aspose.cells.drawing.Picture` object of the header / footer.
        
        :param is_first: Indicates whether getting the picture of first page header/footer.
        :param is_even: Indicates whether getting the picture of even page header/footer.
        :param is_header: Indicates whether getting the picture of header/footer.
        :param section: 0: Left Section, 1: Center Section, 2: Right Section.
        :returns: Returns :py:class:`aspose.cells.drawing.Picture` object.'''
        ...
    
    def copy(self, source : aspose.cells.PageSetup, copy_options : aspose.cells.CopyOptions):
        '''Copies the setting of the page setup.
        
        :param source: The source.
        :param copy_options: The copy options.'''
        ...
    
    def set_fit_to_pages(self, wide : int, tall : int):
        '''Sets the number of pages the worksheet will be scaled to when it's printed.
        
        :param wide: Pages wide.
        :param tall: Pages tall.'''
        ...
    
    def custom_paper_size(self, width : float, height : float):
        '''Sets the custom paper size, in unit of inches.
        
        :param width: The width of the paper.
        :param height: The height of the paper.'''
        ...
    
    def clear_header_footer(self):
        '''Clears header and footer setting.'''
        ...
    
    def get_header(self, section : int) -> str:
        '''Gets a script formatting the header of an Excel file.
        
        :param section: 0: Left Section, 1: Center Section, 2: Right Section.'''
        ...
    
    def get_commands(self, header_footer_script : str) -> List[aspose.cells.HeaderFooterCommand]:
        '''Gets all commands of header or footer.
        
        :param header_footer_script: The header/footer script
        :returns: Returns all commands of header or footer.'''
        ...
    
    def get_footer(self, section : int) -> str:
        '''Gets a script formatting the footer of an Excel file.
        
        :param section: 0: Left Section, 1: Center Section, 2: Right Section.'''
        ...
    
    def set_header(self, section : int, header_script : str):
        '''Sets a script formatting the header of an Excel file.
        
        :param section: 0: Left Section, 1: Center Section, 2: Right Section.
        :param header_script: Header format script.'''
        ...
    
    def set_footer(self, section : int, footer_script : str):
        '''Sets a script formatting the footer of an Excel file.
        
        :param section: 0: Left Section, 1: Center Section, 2: Right Section.
        :param footer_script: Footer format script.'''
        ...
    
    def set_even_header(self, section : int, header_script : str):
        '''Sets a script formatting the even page header of an Excel file.
        Only effect in Excel 2007 when IsHFDiffOddEven is true.
        
        :param section: 0: Left Section, 1: Center Section, 2: Right Section.
        :param header_script: Header format script.'''
        ...
    
    def get_even_header(self, section : int) -> str:
        '''Gets a script formatting the even header of an Excel file.
        
        :param section: 0: Left Section, 1: Center Section, 2: Right Section.'''
        ...
    
    def set_even_footer(self, section : int, footer_script : str):
        '''Sets a script formatting the even page footer of an Excel file.
        Only effect in Excel 2007 when IsHFDiffOddEven is true.
        
        :param section: 0: Left Section, 1: Center Section, 2: Right Section.
        :param footer_script: Footer format script.'''
        ...
    
    def get_even_footer(self, section : int) -> str:
        '''Gets a script formatting the even footer of an Excel file.
        
        :param section: 0: Left Section, 1: Center Section, 2: Right Section.'''
        ...
    
    def set_first_page_header(self, section : int, header_script : str):
        '''Sets a script formatting the first page header of an Excel file.
        Only effect in Excel 2007 when IsHFDiffFirst is true.
        
        :param section: 0: Left Section, 1: Center Section, 2: Right Section.
        :param header_script: Header format script.'''
        ...
    
    def get_first_page_header(self, section : int) -> str:
        '''Gets a script formatting the first page header of an Excel file.
        
        :param section: 0: Left Section, 1: Center Section, 2: Right Section.'''
        ...
    
    def set_first_page_footer(self, section : int, footer_script : str):
        '''Sets a script formatting the first page footer of an Excel file.
        
        :param section: 0: Left Section, 1: Center Section, 2: Right Section.
        :param footer_script: Footer format script.'''
        ...
    
    def get_first_page_footer(self, section : int) -> str:
        '''Gets a script formatting the first page footer of an Excel file.
        
        :param section: 0: Left Section, 1: Center Section, 2: Right Section.'''
        ...
    
    def set_header_picture(self, section : int, header_picture : bytes) -> aspose.cells.drawing.Picture:
        '''Sets an image in the header of a worksheet.
        
        :param section: 0: Left Section, 1: Center Section, 2: Right Section.
        :param header_picture: Image data.
        :returns: Returns :py:class:`aspose.cells.drawing.Picture` object.'''
        ...
    
    def set_footer_picture(self, section : int, footer_picture : bytes) -> aspose.cells.drawing.Picture:
        '''Sets an image in the footer of a worksheet.
        
        :param section: 0: Left Section, 1: Center Section, 2: Right Section.
        :param footer_picture: Image data.
        :returns: Returns :py:class:`aspose.cells.drawing.Picture` object.'''
        ...
    
    def set_picture(self, is_first : bool, is_even : bool, is_header : bool, section : int, image_data : bytes) -> aspose.cells.drawing.Picture:
        '''Sets an image in the header/footer of a worksheet.
        
        :param is_first: Indicates whether setting the picture of first page header/footer.
        :param is_even: Indicates whether setting the picture of even page header/footer.
        :param is_header: Indicates whether setting the picture of header/footer.
        :param section: 0: Left Section, 1: Center Section, 2: Right Section.
        :param image_data: Image data.
        :returns: Returns :py:class:`aspose.cells.drawing.Picture` object.'''
        ...
    
    @property
    def ods_page_background(self) -> aspose.cells.ods.OdsPageBackground:
        ...
    
    @property
    def print_area(self) -> str:
        ...
    
    @print_area.setter
    def print_area(self, value : str):
        ...
    
    @property
    def print_title_columns(self) -> str:
        ...
    
    @print_title_columns.setter
    def print_title_columns(self, value : str):
        ...
    
    @property
    def print_title_rows(self) -> str:
        ...
    
    @print_title_rows.setter
    def print_title_rows(self, value : str):
        ...
    
    @property
    def black_and_white(self) -> bool:
        ...
    
    @black_and_white.setter
    def black_and_white(self, value : bool):
        ...
    
    @property
    def center_horizontally(self) -> bool:
        ...
    
    @center_horizontally.setter
    def center_horizontally(self, value : bool):
        ...
    
    @property
    def center_vertically(self) -> bool:
        ...
    
    @center_vertically.setter
    def center_vertically(self, value : bool):
        ...
    
    @property
    def print_draft(self) -> bool:
        ...
    
    @print_draft.setter
    def print_draft(self, value : bool):
        ...
    
    @property
    def footer_margin(self) -> float:
        ...
    
    @footer_margin.setter
    def footer_margin(self, value : float):
        ...
    
    @property
    def footer_margin_inch(self) -> float:
        ...
    
    @footer_margin_inch.setter
    def footer_margin_inch(self, value : float):
        ...
    
    @property
    def header_margin(self) -> float:
        ...
    
    @header_margin.setter
    def header_margin(self, value : float):
        ...
    
    @property
    def header_margin_inch(self) -> float:
        ...
    
    @header_margin_inch.setter
    def header_margin_inch(self, value : float):
        ...
    
    @property
    def printer_settings(self) -> bytes:
        ...
    
    @printer_settings.setter
    def printer_settings(self, value : bytes):
        ...
    
    @property
    def left_margin(self) -> float:
        ...
    
    @left_margin.setter
    def left_margin(self, value : float):
        ...
    
    @property
    def left_margin_inch(self) -> float:
        ...
    
    @left_margin_inch.setter
    def left_margin_inch(self, value : float):
        ...
    
    @property
    def right_margin(self) -> float:
        ...
    
    @right_margin.setter
    def right_margin(self, value : float):
        ...
    
    @property
    def right_margin_inch(self) -> float:
        ...
    
    @right_margin_inch.setter
    def right_margin_inch(self, value : float):
        ...
    
    @property
    def top_margin(self) -> float:
        ...
    
    @top_margin.setter
    def top_margin(self, value : float):
        ...
    
    @property
    def top_margin_inch(self) -> float:
        ...
    
    @top_margin_inch.setter
    def top_margin_inch(self, value : float):
        ...
    
    @property
    def bottom_margin(self) -> float:
        ...
    
    @bottom_margin.setter
    def bottom_margin(self, value : float):
        ...
    
    @property
    def bottom_margin_inch(self) -> float:
        ...
    
    @bottom_margin_inch.setter
    def bottom_margin_inch(self, value : float):
        ...
    
    @property
    def first_page_number(self) -> int:
        ...
    
    @first_page_number.setter
    def first_page_number(self, value : int):
        ...
    
    @property
    def fit_to_pages_tall(self) -> int:
        ...
    
    @fit_to_pages_tall.setter
    def fit_to_pages_tall(self, value : int):
        ...
    
    @property
    def fit_to_pages_wide(self) -> int:
        ...
    
    @fit_to_pages_wide.setter
    def fit_to_pages_wide(self, value : int):
        ...
    
    @property
    def is_percent_scale(self) -> bool:
        ...
    
    @is_percent_scale.setter
    def is_percent_scale(self, value : bool):
        ...
    
    @property
    def order(self) -> aspose.cells.PrintOrderType:
        '''Represents the order that Microsoft Excel uses to number pages when printing a large worksheet.'''
        ...
    
    @order.setter
    def order(self, value : aspose.cells.PrintOrderType):
        '''Represents the order that Microsoft Excel uses to number pages when printing a large worksheet.'''
        ...
    
    @property
    def is_automatic_paper_size(self) -> bool:
        ...
    
    @property
    def paper_size(self) -> aspose.cells.PaperSizeType:
        ...
    
    @paper_size.setter
    def paper_size(self, value : aspose.cells.PaperSizeType):
        ...
    
    @property
    def paper_width(self) -> float:
        ...
    
    @property
    def paper_height(self) -> float:
        ...
    
    @property
    def orientation(self) -> aspose.cells.PageOrientationType:
        '''Represents page print orientation.'''
        ...
    
    @orientation.setter
    def orientation(self, value : aspose.cells.PageOrientationType):
        '''Represents page print orientation.'''
        ...
    
    @property
    def print_comments(self) -> aspose.cells.PrintCommentsType:
        ...
    
    @print_comments.setter
    def print_comments(self, value : aspose.cells.PrintCommentsType):
        ...
    
    @property
    def print_errors(self) -> aspose.cells.PrintErrorsType:
        ...
    
    @print_errors.setter
    def print_errors(self, value : aspose.cells.PrintErrorsType):
        ...
    
    @property
    def print_headings(self) -> bool:
        ...
    
    @print_headings.setter
    def print_headings(self, value : bool):
        ...
    
    @property
    def print_gridlines(self) -> bool:
        ...
    
    @print_gridlines.setter
    def print_gridlines(self, value : bool):
        ...
    
    @property
    def zoom(self) -> int:
        '''Represents the scaling factor in percent. It should be between 10 and 400.'''
        ...
    
    @zoom.setter
    def zoom(self, value : int):
        '''Represents the scaling factor in percent. It should be between 10 and 400.'''
        ...
    
    @property
    def is_auto_first_page_number(self) -> bool:
        ...
    
    @is_auto_first_page_number.setter
    def is_auto_first_page_number(self, value : bool):
        ...
    
    @property
    def print_quality(self) -> int:
        ...
    
    @print_quality.setter
    def print_quality(self, value : int):
        ...
    
    @property
    def print_copies(self) -> int:
        ...
    
    @print_copies.setter
    def print_copies(self, value : int):
        ...
    
    @property
    def is_hf_diff_odd_even(self) -> bool:
        ...
    
    @is_hf_diff_odd_even.setter
    def is_hf_diff_odd_even(self, value : bool):
        ...
    
    @property
    def is_hf_diff_first(self) -> bool:
        ...
    
    @is_hf_diff_first.setter
    def is_hf_diff_first(self, value : bool):
        ...
    
    @property
    def is_hf_scale_with_doc(self) -> bool:
        ...
    
    @is_hf_scale_with_doc.setter
    def is_hf_scale_with_doc(self, value : bool):
        ...
    
    @property
    def is_hf_align_margins(self) -> bool:
        ...
    
    @is_hf_align_margins.setter
    def is_hf_align_margins(self, value : bool):
        ...
    
    ...

class PaginatedSaveOptions(SaveOptions):
    '''Represents the options for pagination.'''
    
    @property
    def save_format(self) -> aspose.cells.SaveFormat:
        ...
    
    @property
    def clear_data(self) -> bool:
        ...
    
    @clear_data.setter
    def clear_data(self, value : bool):
        ...
    
    @property
    def cached_file_folder(self) -> str:
        ...
    
    @cached_file_folder.setter
    def cached_file_folder(self, value : str):
        ...
    
    @property
    def validate_merged_areas(self) -> bool:
        ...
    
    @validate_merged_areas.setter
    def validate_merged_areas(self, value : bool):
        ...
    
    @property
    def merge_areas(self) -> bool:
        ...
    
    @merge_areas.setter
    def merge_areas(self, value : bool):
        ...
    
    @property
    def create_directory(self) -> bool:
        ...
    
    @create_directory.setter
    def create_directory(self, value : bool):
        ...
    
    @property
    def sort_names(self) -> bool:
        ...
    
    @sort_names.setter
    def sort_names(self, value : bool):
        ...
    
    @property
    def sort_external_names(self) -> bool:
        ...
    
    @sort_external_names.setter
    def sort_external_names(self, value : bool):
        ...
    
    @property
    def refresh_chart_cache(self) -> bool:
        ...
    
    @refresh_chart_cache.setter
    def refresh_chart_cache(self, value : bool):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def update_smart_art(self) -> bool:
        ...
    
    @update_smart_art.setter
    def update_smart_art(self, value : bool):
        ...
    
    @property
    def default_font(self) -> str:
        ...
    
    @default_font.setter
    def default_font(self, value : str):
        ...
    
    @property
    def check_workbook_default_font(self) -> bool:
        ...
    
    @check_workbook_default_font.setter
    def check_workbook_default_font(self, value : bool):
        ...
    
    @property
    def check_font_compatibility(self) -> bool:
        ...
    
    @check_font_compatibility.setter
    def check_font_compatibility(self, value : bool):
        ...
    
    @property
    def is_font_substitution_char_granularity(self) -> bool:
        ...
    
    @is_font_substitution_char_granularity.setter
    def is_font_substitution_char_granularity(self, value : bool):
        ...
    
    @property
    def one_page_per_sheet(self) -> bool:
        ...
    
    @one_page_per_sheet.setter
    def one_page_per_sheet(self, value : bool):
        ...
    
    @property
    def all_columns_in_one_page_per_sheet(self) -> bool:
        ...
    
    @all_columns_in_one_page_per_sheet.setter
    def all_columns_in_one_page_per_sheet(self, value : bool):
        ...
    
    @property
    def ignore_error(self) -> bool:
        ...
    
    @ignore_error.setter
    def ignore_error(self, value : bool):
        ...
    
    @property
    def output_blank_page_when_nothing_to_print(self) -> bool:
        ...
    
    @output_blank_page_when_nothing_to_print.setter
    def output_blank_page_when_nothing_to_print(self, value : bool):
        ...
    
    @property
    def page_index(self) -> int:
        ...
    
    @page_index.setter
    def page_index(self, value : int):
        ...
    
    @property
    def page_count(self) -> int:
        ...
    
    @page_count.setter
    def page_count(self, value : int):
        ...
    
    @property
    def printing_page_type(self) -> aspose.cells.PrintingPageType:
        ...
    
    @printing_page_type.setter
    def printing_page_type(self, value : aspose.cells.PrintingPageType):
        ...
    
    @property
    def gridline_type(self) -> aspose.cells.GridlineType:
        ...
    
    @gridline_type.setter
    def gridline_type(self, value : aspose.cells.GridlineType):
        ...
    
    @property
    def text_cross_type(self) -> aspose.cells.TextCrossType:
        ...
    
    @text_cross_type.setter
    def text_cross_type(self, value : aspose.cells.TextCrossType):
        ...
    
    @property
    def default_edit_language(self) -> aspose.cells.DefaultEditLanguage:
        ...
    
    @default_edit_language.setter
    def default_edit_language(self, value : aspose.cells.DefaultEditLanguage):
        ...
    
    @property
    def sheet_set(self) -> aspose.cells.rendering.SheetSet:
        ...
    
    @sheet_set.setter
    def sheet_set(self, value : aspose.cells.rendering.SheetSet):
        ...
    
    @property
    def draw_object_event_handler(self) -> aspose.cells.rendering.DrawObjectEventHandler:
        ...
    
    @draw_object_event_handler.setter
    def draw_object_event_handler(self, value : aspose.cells.rendering.DrawObjectEventHandler):
        ...
    
    @property
    def page_saving_callback(self) -> aspose.cells.rendering.IPageSavingCallback:
        ...
    
    @page_saving_callback.setter
    def page_saving_callback(self, value : aspose.cells.rendering.IPageSavingCallback):
        ...
    
    ...

class PaneCollection:
    '''Represents all Pane objects shown in the specified window.'''
    
    @property
    def first_visible_row_of_bottom_pane(self) -> int:
        ...
    
    @first_visible_row_of_bottom_pane.setter
    def first_visible_row_of_bottom_pane(self, value : int):
        ...
    
    @property
    def first_visible_column_of_right_pane(self) -> int:
        ...
    
    @first_visible_column_of_right_pane.setter
    def first_visible_column_of_right_pane(self, value : int):
        ...
    
    @property
    def acitve_pane_type(self) -> aspose.cells.drawing.RectangleAlignmentType:
        ...
    
    @acitve_pane_type.setter
    def acitve_pane_type(self, value : aspose.cells.drawing.RectangleAlignmentType):
        ...
    
    ...

class PasteOptions:
    '''Represents the paste special options.'''
    
    @property
    def paste_type(self) -> aspose.cells.PasteType:
        ...
    
    @paste_type.setter
    def paste_type(self, value : aspose.cells.PasteType):
        ...
    
    @property
    def skip_blanks(self) -> bool:
        ...
    
    @skip_blanks.setter
    def skip_blanks(self, value : bool):
        ...
    
    @property
    def only_visible_cells(self) -> bool:
        ...
    
    @only_visible_cells.setter
    def only_visible_cells(self, value : bool):
        ...
    
    @property
    def transpose(self) -> bool:
        '''True to transpose rows and columns when the range is pasted. The default value is False.'''
        ...
    
    @transpose.setter
    def transpose(self, value : bool):
        '''True to transpose rows and columns when the range is pasted. The default value is False.'''
        ...
    
    @property
    def operation_type(self) -> aspose.cells.PasteOperationType:
        ...
    
    @operation_type.setter
    def operation_type(self, value : aspose.cells.PasteOperationType):
        ...
    
    @property
    def ignore_links_to_original_file(self) -> bool:
        ...
    
    @ignore_links_to_original_file.setter
    def ignore_links_to_original_file(self, value : bool):
        ...
    
    ...

class PdfSaveOptions(PaginatedSaveOptions):
    '''Represents the options for saving pdf file.'''
    
    def set_image_resample(self, desired_ppi : int, jpeg_quality : int):
        '''Sets desired PPI(pixels per inch) of resample images and jpeg quality.
        All images will be converted to JPEG with the specified quality setting,
        and images that are greater than the specified PPI (pixels per inch) will be resampled.
        
        :param desired_ppi: Desired pixels per inch. 220 high quality. 150 screen quality. 96 email quality.
        :param jpeg_quality: 0 - 100% JPEG quality.'''
        ...
    
    @property
    def save_format(self) -> aspose.cells.SaveFormat:
        ...
    
    @property
    def clear_data(self) -> bool:
        ...
    
    @clear_data.setter
    def clear_data(self, value : bool):
        ...
    
    @property
    def cached_file_folder(self) -> str:
        ...
    
    @cached_file_folder.setter
    def cached_file_folder(self, value : str):
        ...
    
    @property
    def validate_merged_areas(self) -> bool:
        ...
    
    @validate_merged_areas.setter
    def validate_merged_areas(self, value : bool):
        ...
    
    @property
    def merge_areas(self) -> bool:
        ...
    
    @merge_areas.setter
    def merge_areas(self, value : bool):
        ...
    
    @property
    def create_directory(self) -> bool:
        ...
    
    @create_directory.setter
    def create_directory(self, value : bool):
        ...
    
    @property
    def sort_names(self) -> bool:
        ...
    
    @sort_names.setter
    def sort_names(self, value : bool):
        ...
    
    @property
    def sort_external_names(self) -> bool:
        ...
    
    @sort_external_names.setter
    def sort_external_names(self, value : bool):
        ...
    
    @property
    def refresh_chart_cache(self) -> bool:
        ...
    
    @refresh_chart_cache.setter
    def refresh_chart_cache(self, value : bool):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def update_smart_art(self) -> bool:
        ...
    
    @update_smart_art.setter
    def update_smart_art(self, value : bool):
        ...
    
    @property
    def default_font(self) -> str:
        ...
    
    @default_font.setter
    def default_font(self, value : str):
        ...
    
    @property
    def check_workbook_default_font(self) -> bool:
        ...
    
    @check_workbook_default_font.setter
    def check_workbook_default_font(self, value : bool):
        ...
    
    @property
    def check_font_compatibility(self) -> bool:
        ...
    
    @check_font_compatibility.setter
    def check_font_compatibility(self, value : bool):
        ...
    
    @property
    def is_font_substitution_char_granularity(self) -> bool:
        ...
    
    @is_font_substitution_char_granularity.setter
    def is_font_substitution_char_granularity(self, value : bool):
        ...
    
    @property
    def one_page_per_sheet(self) -> bool:
        ...
    
    @one_page_per_sheet.setter
    def one_page_per_sheet(self, value : bool):
        ...
    
    @property
    def all_columns_in_one_page_per_sheet(self) -> bool:
        ...
    
    @all_columns_in_one_page_per_sheet.setter
    def all_columns_in_one_page_per_sheet(self, value : bool):
        ...
    
    @property
    def ignore_error(self) -> bool:
        ...
    
    @ignore_error.setter
    def ignore_error(self, value : bool):
        ...
    
    @property
    def output_blank_page_when_nothing_to_print(self) -> bool:
        ...
    
    @output_blank_page_when_nothing_to_print.setter
    def output_blank_page_when_nothing_to_print(self, value : bool):
        ...
    
    @property
    def page_index(self) -> int:
        ...
    
    @page_index.setter
    def page_index(self, value : int):
        ...
    
    @property
    def page_count(self) -> int:
        ...
    
    @page_count.setter
    def page_count(self, value : int):
        ...
    
    @property
    def printing_page_type(self) -> aspose.cells.PrintingPageType:
        ...
    
    @printing_page_type.setter
    def printing_page_type(self, value : aspose.cells.PrintingPageType):
        ...
    
    @property
    def gridline_type(self) -> aspose.cells.GridlineType:
        ...
    
    @gridline_type.setter
    def gridline_type(self, value : aspose.cells.GridlineType):
        ...
    
    @property
    def text_cross_type(self) -> aspose.cells.TextCrossType:
        ...
    
    @text_cross_type.setter
    def text_cross_type(self, value : aspose.cells.TextCrossType):
        ...
    
    @property
    def default_edit_language(self) -> aspose.cells.DefaultEditLanguage:
        ...
    
    @default_edit_language.setter
    def default_edit_language(self, value : aspose.cells.DefaultEditLanguage):
        ...
    
    @property
    def sheet_set(self) -> aspose.cells.rendering.SheetSet:
        ...
    
    @sheet_set.setter
    def sheet_set(self, value : aspose.cells.rendering.SheetSet):
        ...
    
    @property
    def draw_object_event_handler(self) -> aspose.cells.rendering.DrawObjectEventHandler:
        ...
    
    @draw_object_event_handler.setter
    def draw_object_event_handler(self, value : aspose.cells.rendering.DrawObjectEventHandler):
        ...
    
    @property
    def page_saving_callback(self) -> aspose.cells.rendering.IPageSavingCallback:
        ...
    
    @page_saving_callback.setter
    def page_saving_callback(self, value : aspose.cells.rendering.IPageSavingCallback):
        ...
    
    @property
    def embed_standard_windows_fonts(self) -> bool:
        ...
    
    @embed_standard_windows_fonts.setter
    def embed_standard_windows_fonts(self, value : bool):
        ...
    
    @property
    def bookmark(self) -> aspose.cells.rendering.PdfBookmarkEntry:
        '''Gets and sets the :py:class:`aspose.cells.rendering.PdfBookmarkEntry` object.'''
        ...
    
    @bookmark.setter
    def bookmark(self, value : aspose.cells.rendering.PdfBookmarkEntry):
        '''Gets and sets the :py:class:`aspose.cells.rendering.PdfBookmarkEntry` object.'''
        ...
    
    @property
    def compliance(self) -> aspose.cells.rendering.PdfCompliance:
        '''Workbook converts to pdf will according to PdfCompliance in this property.'''
        ...
    
    @compliance.setter
    def compliance(self, value : aspose.cells.rendering.PdfCompliance):
        '''Workbook converts to pdf will according to PdfCompliance in this property.'''
        ...
    
    @property
    def security_options(self) -> aspose.cells.rendering.pdfsecurity.PdfSecurityOptions:
        ...
    
    @security_options.setter
    def security_options(self, value : aspose.cells.rendering.pdfsecurity.PdfSecurityOptions):
        ...
    
    @property
    def image_type(self) -> aspose.cells.drawing.ImageType:
        ...
    
    @image_type.setter
    def image_type(self, value : aspose.cells.drawing.ImageType):
        ...
    
    @property
    def calculate_formula(self) -> bool:
        ...
    
    @calculate_formula.setter
    def calculate_formula(self, value : bool):
        ...
    
    @property
    def pdf_compression(self) -> aspose.cells.rendering.PdfCompressionCore:
        ...
    
    @pdf_compression.setter
    def pdf_compression(self, value : aspose.cells.rendering.PdfCompressionCore):
        ...
    
    @property
    def created_time(self) -> DateTime:
        ...
    
    @created_time.setter
    def created_time(self, value : DateTime):
        ...
    
    @property
    def producer(self) -> str:
        '''Gets and sets producer of generated pdf document.'''
        ...
    
    @producer.setter
    def producer(self, value : str):
        '''Gets and sets producer of generated pdf document.'''
        ...
    
    @property
    def optimization_type(self) -> aspose.cells.rendering.PdfOptimizationType:
        ...
    
    @optimization_type.setter
    def optimization_type(self, value : aspose.cells.rendering.PdfOptimizationType):
        ...
    
    @property
    def custom_properties_export(self) -> aspose.cells.rendering.PdfCustomPropertiesExport:
        ...
    
    @custom_properties_export.setter
    def custom_properties_export(self, value : aspose.cells.rendering.PdfCustomPropertiesExport):
        ...
    
    @property
    def export_document_structure(self) -> bool:
        ...
    
    @export_document_structure.setter
    def export_document_structure(self, value : bool):
        ...
    
    @property
    def emf_render_setting(self) -> aspose.cells.EmfRenderSetting:
        ...
    
    @emf_render_setting.setter
    def emf_render_setting(self, value : aspose.cells.EmfRenderSetting):
        ...
    
    @property
    def display_doc_title(self) -> bool:
        ...
    
    @display_doc_title.setter
    def display_doc_title(self, value : bool):
        ...
    
    @property
    def font_encoding(self) -> aspose.cells.rendering.PdfFontEncoding:
        ...
    
    @font_encoding.setter
    def font_encoding(self, value : aspose.cells.rendering.PdfFontEncoding):
        ...
    
    ...

class PptxSaveOptions(PaginatedSaveOptions):
    '''Represents the pptx save options.'''
    
    @property
    def save_format(self) -> aspose.cells.SaveFormat:
        ...
    
    @property
    def clear_data(self) -> bool:
        ...
    
    @clear_data.setter
    def clear_data(self, value : bool):
        ...
    
    @property
    def cached_file_folder(self) -> str:
        ...
    
    @cached_file_folder.setter
    def cached_file_folder(self, value : str):
        ...
    
    @property
    def validate_merged_areas(self) -> bool:
        ...
    
    @validate_merged_areas.setter
    def validate_merged_areas(self, value : bool):
        ...
    
    @property
    def merge_areas(self) -> bool:
        ...
    
    @merge_areas.setter
    def merge_areas(self, value : bool):
        ...
    
    @property
    def create_directory(self) -> bool:
        ...
    
    @create_directory.setter
    def create_directory(self, value : bool):
        ...
    
    @property
    def sort_names(self) -> bool:
        ...
    
    @sort_names.setter
    def sort_names(self, value : bool):
        ...
    
    @property
    def sort_external_names(self) -> bool:
        ...
    
    @sort_external_names.setter
    def sort_external_names(self, value : bool):
        ...
    
    @property
    def refresh_chart_cache(self) -> bool:
        ...
    
    @refresh_chart_cache.setter
    def refresh_chart_cache(self, value : bool):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def update_smart_art(self) -> bool:
        ...
    
    @update_smart_art.setter
    def update_smart_art(self, value : bool):
        ...
    
    @property
    def default_font(self) -> str:
        ...
    
    @default_font.setter
    def default_font(self, value : str):
        ...
    
    @property
    def check_workbook_default_font(self) -> bool:
        ...
    
    @check_workbook_default_font.setter
    def check_workbook_default_font(self, value : bool):
        ...
    
    @property
    def check_font_compatibility(self) -> bool:
        ...
    
    @check_font_compatibility.setter
    def check_font_compatibility(self, value : bool):
        ...
    
    @property
    def is_font_substitution_char_granularity(self) -> bool:
        ...
    
    @is_font_substitution_char_granularity.setter
    def is_font_substitution_char_granularity(self, value : bool):
        ...
    
    @property
    def one_page_per_sheet(self) -> bool:
        ...
    
    @one_page_per_sheet.setter
    def one_page_per_sheet(self, value : bool):
        ...
    
    @property
    def all_columns_in_one_page_per_sheet(self) -> bool:
        ...
    
    @all_columns_in_one_page_per_sheet.setter
    def all_columns_in_one_page_per_sheet(self, value : bool):
        ...
    
    @property
    def ignore_error(self) -> bool:
        ...
    
    @ignore_error.setter
    def ignore_error(self, value : bool):
        ...
    
    @property
    def output_blank_page_when_nothing_to_print(self) -> bool:
        ...
    
    @output_blank_page_when_nothing_to_print.setter
    def output_blank_page_when_nothing_to_print(self, value : bool):
        ...
    
    @property
    def page_index(self) -> int:
        ...
    
    @page_index.setter
    def page_index(self, value : int):
        ...
    
    @property
    def page_count(self) -> int:
        ...
    
    @page_count.setter
    def page_count(self, value : int):
        ...
    
    @property
    def printing_page_type(self) -> aspose.cells.PrintingPageType:
        ...
    
    @printing_page_type.setter
    def printing_page_type(self, value : aspose.cells.PrintingPageType):
        ...
    
    @property
    def gridline_type(self) -> aspose.cells.GridlineType:
        ...
    
    @gridline_type.setter
    def gridline_type(self, value : aspose.cells.GridlineType):
        ...
    
    @property
    def text_cross_type(self) -> aspose.cells.TextCrossType:
        ...
    
    @text_cross_type.setter
    def text_cross_type(self, value : aspose.cells.TextCrossType):
        ...
    
    @property
    def default_edit_language(self) -> aspose.cells.DefaultEditLanguage:
        ...
    
    @default_edit_language.setter
    def default_edit_language(self, value : aspose.cells.DefaultEditLanguage):
        ...
    
    @property
    def sheet_set(self) -> aspose.cells.rendering.SheetSet:
        ...
    
    @sheet_set.setter
    def sheet_set(self, value : aspose.cells.rendering.SheetSet):
        ...
    
    @property
    def draw_object_event_handler(self) -> aspose.cells.rendering.DrawObjectEventHandler:
        ...
    
    @draw_object_event_handler.setter
    def draw_object_event_handler(self, value : aspose.cells.rendering.DrawObjectEventHandler):
        ...
    
    @property
    def page_saving_callback(self) -> aspose.cells.rendering.IPageSavingCallback:
        ...
    
    @page_saving_callback.setter
    def page_saving_callback(self, value : aspose.cells.rendering.IPageSavingCallback):
        ...
    
    ...

class ProtectedRange:
    '''A specified range to be allowed to edit when the sheet protection is ON.'''
    
    def get_areas(self) -> List[aspose.cells.CellArea]:
        '''Gets all referred areas.
        
        :returns: Returns all referred areas.'''
        ...
    
    def add_area(self, start_row : int, start_column : int, end_row : int, end_column : int):
        '''Adds a referred area to this
        
        :param start_row: The start row.
        :param start_column: The start column.
        :param end_row: The end row.
        :param end_column: The end column.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the Range title. This is used as a descriptor, not as a named range definition.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets the Range title. This is used as a descriptor, not as a named range definition.'''
        ...
    
    @property
    def cell_area(self) -> aspose.cells.CellArea:
        ...
    
    @property
    def is_protected_with_password(self) -> bool:
        ...
    
    @property
    def password(self) -> str:
        '''Represents the password to protect the range.'''
        ...
    
    @password.setter
    def password(self, value : str):
        '''Represents the password to protect the range.'''
        ...
    
    @property
    def security_descriptor(self) -> str:
        ...
    
    @security_descriptor.setter
    def security_descriptor(self, value : str):
        ...
    
    ...

class ProtectedRangeCollection:
    '''Encapsulates a collection of :py:class:`aspose.cells.ProtectedRange` objects.'''
    
    @overload
    def copy_to(self, array : List[aspose.cells.ProtectedRange]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.ProtectedRange], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.ProtectedRange, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.ProtectedRange, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.ProtectedRange) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.ProtectedRange, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.ProtectedRange, index : int, count : int) -> int:
        ...
    
    def add(self, name : str, start_row : int, start_column : int, end_row : int, end_column : int) -> int:
        '''Adds a :py:class:`aspose.cells.ProtectedRange` item to the collection.
        
        :param name: Range title. This is used as a descriptor, not as a named range definition.
        :param start_row: Start row index of the range.
        :param start_column: Start column index of the range.
        :param end_row: End row index of the range.
        :param end_column: End column index of the range.
        :returns: object index.'''
        ...
    
    def binary_search(self, item : aspose.cells.ProtectedRange) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class Protection:
    '''Represents the various types of protection options available for a worksheet.'''
    
    def copy(self, source : aspose.cells.Protection):
        '''Copy protection info.'''
        ...
    
    def get_password_hash(self) -> int:
        '''Gets the hash of current password.'''
        ...
    
    def verify_password(self, password : str) -> bool:
        '''Verifies password.
        
        :param password: The password.'''
        ...
    
    @property
    def allow_deleting_column(self) -> bool:
        ...
    
    @allow_deleting_column.setter
    def allow_deleting_column(self, value : bool):
        ...
    
    @property
    def is_deleting_columns_allowed(self) -> bool:
        ...
    
    @is_deleting_columns_allowed.setter
    def is_deleting_columns_allowed(self, value : bool):
        ...
    
    @property
    def allow_deleting_row(self) -> bool:
        ...
    
    @allow_deleting_row.setter
    def allow_deleting_row(self, value : bool):
        ...
    
    @property
    def is_deleting_rows_allowed(self) -> bool:
        ...
    
    @is_deleting_rows_allowed.setter
    def is_deleting_rows_allowed(self, value : bool):
        ...
    
    @property
    def allow_filtering(self) -> bool:
        ...
    
    @allow_filtering.setter
    def allow_filtering(self, value : bool):
        ...
    
    @property
    def is_filtering_allowed(self) -> bool:
        ...
    
    @is_filtering_allowed.setter
    def is_filtering_allowed(self, value : bool):
        ...
    
    @property
    def allow_formatting_cell(self) -> bool:
        ...
    
    @allow_formatting_cell.setter
    def allow_formatting_cell(self, value : bool):
        ...
    
    @property
    def is_formatting_cells_allowed(self) -> bool:
        ...
    
    @is_formatting_cells_allowed.setter
    def is_formatting_cells_allowed(self, value : bool):
        ...
    
    @property
    def allow_formatting_column(self) -> bool:
        ...
    
    @allow_formatting_column.setter
    def allow_formatting_column(self, value : bool):
        ...
    
    @property
    def is_formatting_columns_allowed(self) -> bool:
        ...
    
    @is_formatting_columns_allowed.setter
    def is_formatting_columns_allowed(self, value : bool):
        ...
    
    @property
    def allow_formatting_row(self) -> bool:
        ...
    
    @allow_formatting_row.setter
    def allow_formatting_row(self, value : bool):
        ...
    
    @property
    def is_formatting_rows_allowed(self) -> bool:
        ...
    
    @is_formatting_rows_allowed.setter
    def is_formatting_rows_allowed(self, value : bool):
        ...
    
    @property
    def allow_inserting_column(self) -> bool:
        ...
    
    @allow_inserting_column.setter
    def allow_inserting_column(self, value : bool):
        ...
    
    @property
    def is_inserting_columns_allowed(self) -> bool:
        ...
    
    @is_inserting_columns_allowed.setter
    def is_inserting_columns_allowed(self, value : bool):
        ...
    
    @property
    def allow_inserting_hyperlink(self) -> bool:
        ...
    
    @allow_inserting_hyperlink.setter
    def allow_inserting_hyperlink(self, value : bool):
        ...
    
    @property
    def is_inserting_hyperlinks_allowed(self) -> bool:
        ...
    
    @is_inserting_hyperlinks_allowed.setter
    def is_inserting_hyperlinks_allowed(self, value : bool):
        ...
    
    @property
    def allow_inserting_row(self) -> bool:
        ...
    
    @allow_inserting_row.setter
    def allow_inserting_row(self, value : bool):
        ...
    
    @property
    def is_inserting_rows_allowed(self) -> bool:
        ...
    
    @is_inserting_rows_allowed.setter
    def is_inserting_rows_allowed(self, value : bool):
        ...
    
    @property
    def allow_sorting(self) -> bool:
        ...
    
    @allow_sorting.setter
    def allow_sorting(self, value : bool):
        ...
    
    @property
    def is_sorting_allowed(self) -> bool:
        ...
    
    @is_sorting_allowed.setter
    def is_sorting_allowed(self, value : bool):
        ...
    
    @property
    def allow_using_pivot_table(self) -> bool:
        ...
    
    @allow_using_pivot_table.setter
    def allow_using_pivot_table(self, value : bool):
        ...
    
    @property
    def is_using_pivot_tables_allowed(self) -> bool:
        ...
    
    @is_using_pivot_tables_allowed.setter
    def is_using_pivot_tables_allowed(self, value : bool):
        ...
    
    @property
    def allow_editing_content(self) -> bool:
        ...
    
    @allow_editing_content.setter
    def allow_editing_content(self, value : bool):
        ...
    
    @property
    def is_editing_contents_allowed(self) -> bool:
        ...
    
    @is_editing_contents_allowed.setter
    def is_editing_contents_allowed(self, value : bool):
        ...
    
    @property
    def allow_editing_object(self) -> bool:
        ...
    
    @allow_editing_object.setter
    def allow_editing_object(self, value : bool):
        ...
    
    @property
    def is_editing_objects_allowed(self) -> bool:
        ...
    
    @is_editing_objects_allowed.setter
    def is_editing_objects_allowed(self, value : bool):
        ...
    
    @property
    def allow_editing_scenario(self) -> bool:
        ...
    
    @allow_editing_scenario.setter
    def allow_editing_scenario(self, value : bool):
        ...
    
    @property
    def is_editing_scenarios_allowed(self) -> bool:
        ...
    
    @is_editing_scenarios_allowed.setter
    def is_editing_scenarios_allowed(self, value : bool):
        ...
    
    @property
    def password(self) -> str:
        '''Represents the password to protect the worksheet.'''
        ...
    
    @password.setter
    def password(self, value : str):
        '''Represents the password to protect the worksheet.'''
        ...
    
    @property
    def is_protected_with_password(self) -> bool:
        ...
    
    @property
    def allow_selecting_locked_cell(self) -> bool:
        ...
    
    @allow_selecting_locked_cell.setter
    def allow_selecting_locked_cell(self, value : bool):
        ...
    
    @property
    def is_selecting_locked_cells_allowed(self) -> bool:
        ...
    
    @is_selecting_locked_cells_allowed.setter
    def is_selecting_locked_cells_allowed(self, value : bool):
        ...
    
    @property
    def allow_selecting_unlocked_cell(self) -> bool:
        ...
    
    @allow_selecting_unlocked_cell.setter
    def allow_selecting_unlocked_cell(self, value : bool):
        ...
    
    @property
    def is_selecting_unlocked_cells_allowed(self) -> bool:
        ...
    
    @is_selecting_unlocked_cells_allowed.setter
    def is_selecting_unlocked_cells_allowed(self, value : bool):
        ...
    
    ...

class QueryTable:
    '''Represents QueryTable information.'''
    
    @property
    def connection_id(self) -> int:
        ...
    
    @property
    def external_connection(self) -> aspose.cells.externalconnections.ExternalConnection:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name of querytable.'''
        ...
    
    @property
    def result_range(self) -> aspose.cells.Range:
        ...
    
    @property
    def preserve_formatting(self) -> bool:
        ...
    
    @preserve_formatting.setter
    def preserve_formatting(self, value : bool):
        ...
    
    @property
    def adjust_column_width(self) -> bool:
        ...
    
    @adjust_column_width.setter
    def adjust_column_width(self, value : bool):
        ...
    
    ...

class QueryTableCollection:
    '''A collection of :py:class:`aspose.cells.QueryTableCollection` objects that represent QueryTable collection information.'''
    
    @overload
    def copy_to(self, array : List[aspose.cells.QueryTable]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.QueryTable], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.QueryTable, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.QueryTable, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.QueryTable) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.QueryTable, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.QueryTable, index : int, count : int) -> int:
        ...
    
    def binary_search(self, item : aspose.cells.QueryTable) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class Range:
    '''Encapsulates the object that represents a range of cells within a spreadsheet.'''
    
    @overload
    def auto_fill(self, target : aspose.cells.Range):
        '''Automaticall fill the target range.
        
        :param target: the target range.'''
        ...
    
    @overload
    def auto_fill(self, target : aspose.cells.Range, auto_fill_type : aspose.cells.AutoFillType):
        '''Automaticall fill the target range.
        
        :param target: The targed range.
        :param auto_fill_type: The auto fill type.'''
        ...
    
    @overload
    def set_style(self, style : aspose.cells.Style, explicit_flag : bool):
        '''Apply the cell style.
        
        :param style: The cell style.
        :param explicit_flag: True, only overwriting formatting which is explicitly set.'''
        ...
    
    @overload
    def set_style(self, style : aspose.cells.Style):
        '''Sets the style of the range.
        
        :param style: The Style object.'''
        ...
    
    @overload
    def set_outline_borders(self, border_style : aspose.cells.CellBorderType, border_color : aspose.cells.CellsColor):
        '''Sets the outline borders around a range of cells with same border style and color.
        
        :param border_style: Border style.
        :param border_color: Border color.'''
        ...
    
    @overload
    def set_outline_borders(self, border_style : aspose.cells.CellBorderType, border_color : aspose.pydrawing.Color):
        '''Sets the outline borders around a range of cells with same border style and color.
        
        :param border_style: Border style.
        :param border_color: Border color.'''
        ...
    
    @overload
    def set_outline_borders(self, border_styles : List[aspose.cells.CellBorderType], border_colors : aspose.pydrawing.Color[]):
        '''Sets out line borders around a range of cells.
        
        :param border_styles: Border styles.
        :param border_colors: Border colors.'''
        ...
    
    @overload
    def set_outline_border(self, border_edge : aspose.cells.BorderType, border_style : aspose.cells.CellBorderType, border_color : aspose.cells.CellsColor):
        '''Sets outline border around a range of cells.
        
        :param border_edge: Border edge.
        :param border_style: Border style.
        :param border_color: Border color.'''
        ...
    
    @overload
    def set_outline_border(self, border_edge : aspose.cells.BorderType, border_style : aspose.cells.CellBorderType, border_color : aspose.pydrawing.Color):
        '''Sets outline border around a range of cells.
        
        :param border_edge: Border edge.
        :param border_style: Border style.
        :param border_color: Border color.'''
        ...
    
    @overload
    def copy(self, range : aspose.cells.Range, options : aspose.cells.PasteOptions):
        '''Copying the range with paste special options.
        
        :param range: The source range.
        :param options: The paste special options.'''
        ...
    
    @overload
    def copy(self, range : aspose.cells.Range):
        '''Copies data (including formulas), formatting, drawing objects etc. from a source range.
        
        :param range: Source :py:class:`aspose.cells.Range` object.'''
        ...
    
    def get_enumerator(self) -> collections.abc.Iterator:
        '''Gets the enumerator for cells in this Range.
        
        :returns: The cells enumerator'''
        ...
    
    def is_intersect(self, range : aspose.cells.Range) -> bool:
        '''Indicates whether the range is intersect.
        
        :param range: The range.
        :returns: Whether the range is intersect.'''
        ...
    
    def intersect(self, range : aspose.cells.Range) -> aspose.cells.Range:
        '''Returns a :py:class:`aspose.cells.Range` object that represents the rectangular intersection of two ranges.
        
        :param range: The intersecting range.
        :returns: Returns a :py:class:`aspose.cells.Range` object'''
        ...
    
    def union(self, range : aspose.cells.Range) -> list:
        '''Returns the union of two ranges.
        
        :param range: The range
        :returns: The union of two ranges.'''
        ...
    
    def merge(self):
        '''Combines a range of cells into a single cell.'''
        ...
    
    def un_merge(self):
        '''Unmerges merged cells of this range.'''
        ...
    
    def put_value(self, string_value : str, is_converted : bool, set_style : bool):
        '''Puts a value into the range, if appropriate the value will be converted to other data type and cell's number format will be reset.
        
        :param string_value: Input value
        :param is_converted: True: converted to other data type if appropriate.
        :param set_style: True: set the number format to cell's style when converting to other data type'''
        ...
    
    def apply_style(self, style : aspose.cells.Style, flag : aspose.cells.StyleFlag):
        '''Applies formats for a whole range.
        
        :param style: The style object which will be applied.
        :param flag: Flags which indicates applied formatting properties.'''
        ...
    
    def set_inside_borders(self, border_edge : aspose.cells.BorderType, line_style : aspose.cells.CellBorderType, border_color : aspose.cells.CellsColor):
        '''Set inside borders of the range.
        
        :param border_edge: Inside borde type, only can be :py:attr:`aspose.cells.BorderType.VERTICAL` and :py:attr:`aspose.cells.BorderType.HORIZONTAL`.
        :param line_style: The border style.
        :param border_color: The color of the border.'''
        ...
    
    def move_to(self, dest_row : int, dest_column : int):
        '''Move the current range to the dest range.
        
        :param dest_row: The start row of the dest range.
        :param dest_column: The start column of the dest range.'''
        ...
    
    def copy_data(self, range : aspose.cells.Range):
        '''Copies cell data (including formulas) from a source range.
        
        :param range: Source :py:class:`aspose.cells.Range` object.'''
        ...
    
    def copy_value(self, range : aspose.cells.Range):
        '''Copies cell value from a source range.
        
        :param range: Source :py:class:`aspose.cells.Range` object.'''
        ...
    
    def copy_style(self, range : aspose.cells.Range):
        '''Copies style settings from a source range.
        
        :param range: Source :py:class:`aspose.cells.Range` object.'''
        ...
    
    def get_cell_or_null(self, row_offset : int, column_offset : int) -> aspose.cells.Cell:
        '''Gets :py:class:`aspose.cells.Cell` object or null in this range.
        
        :param row_offset: Row offset in this range, zero based.
        :param column_offset: Column offset in this range, zero based.
        :returns: :py:class:`aspose.cells.Cell` object.'''
        ...
    
    def get_offset(self, row_offset : int, column_offset : int) -> aspose.cells.Range:
        '''Gets :py:class:`aspose.cells.Range` range by offset.
        
        :param row_offset: Row offset in this range, zero based.
        :param column_offset: Column offset in this range, zero based.'''
        ...
    
    @property
    def current_region(self) -> aspose.cells.Range:
        ...
    
    @property
    def hyperlinks(self) -> List[aspose.cells.Hyperlink]:
        '''Gets all hyperlink in the range.'''
        ...
    
    @property
    def row_count(self) -> int:
        ...
    
    @property
    def column_count(self) -> int:
        ...
    
    @property
    def cell_count(self) -> int:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name of the range.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name of the range.'''
        ...
    
    @property
    def refers_to(self) -> str:
        ...
    
    @property
    def address(self) -> str:
        '''Gets address of the range.'''
        ...
    
    @property
    def left(self) -> float:
        '''Gets the distance, in points, from the left edge of column A to the left edge of the range.'''
        ...
    
    @property
    def top(self) -> float:
        '''Gets the distance, in points, from the top edge of row 1 to the top edge of the range.'''
        ...
    
    @property
    def width(self) -> float:
        '''Gets the width of a range in points.'''
        ...
    
    @property
    def height(self) -> float:
        '''Gets the width of a range in points.'''
        ...
    
    @property
    def first_row(self) -> int:
        ...
    
    @property
    def first_column(self) -> int:
        ...
    
    @property
    def value(self) -> any:
        '''Gets and sets the value of the range.'''
        ...
    
    @value.setter
    def value(self, value : any):
        '''Gets and sets the value of the range.'''
        ...
    
    @property
    def column_width(self) -> float:
        ...
    
    @column_width.setter
    def column_width(self, value : float):
        ...
    
    @property
    def row_height(self) -> float:
        ...
    
    @row_height.setter
    def row_height(self, value : float):
        ...
    
    @property
    def entire_column(self) -> aspose.cells.Range:
        ...
    
    @property
    def entire_row(self) -> aspose.cells.Range:
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.Range.worksheet`object which contains this range.'''
        ...
    
    ...

class RangeCollection:
    '''Encapsulates a collection of :py:class:`aspose.cells.Range` objects.'''
    
    @overload
    def copy_to(self, array : List[aspose.cells.Range]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.Range], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.Range, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.Range, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Range) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Range, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Range, index : int, count : int) -> int:
        ...
    
    def add(self, range : aspose.cells.Range) -> int:
        '''Adds a :py:class:`aspose.cells.Range` item to the collection.
        
        :param range: Range object'''
        ...
    
    def binary_search(self, item : aspose.cells.Range) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class ReferredArea:
    '''Represents a referred area by the formula.'''
    
    @overload
    def get_values(self) -> any:
        '''Gets cell values in this area.
        
        :returns: If this area is invalid, "#REF!" will be returned;
        If this area is one single cell, then return the cell value object;
        Otherwise return one 2D array for all values in this area.'''
        ...
    
    @overload
    def get_values(self, calculate_formulas : bool) -> any:
        '''Gets cell values in this area.
        
        :param calculate_formulas: In this range, if there are some formulas that have not been calculated,
        this flag denotes whether those formulas should be calculated recursively
        :returns: If this area is invalid, "#REF!" will be returned;
        If this area is one single cell, then return the cell value object;
        Otherwise return one 2D array for all values in this area.'''
        ...
    
    @overload
    def get_value(self, row_offset : int, col_offset : int) -> any:
        '''Gets cell value with given offset from the top-left of this area.
        
        :param row_offset: row offset from the start row of this area
        :param col_offset: column offset from the start row of this area
        :returns: "#REF!" if this area is invalid;
        "#N/A" if given offset out of this area;
        Otherwise return the cell value at given position.'''
        ...
    
    @overload
    def get_value(self, row_offset : int, col_offset : int, calculate_formulas : bool) -> any:
        '''Gets cell value with given offset from the top-left of this area.
        
        :param row_offset: row offset from the start row of this area
        :param col_offset: column offset from the start row of this area
        :param calculate_formulas: Whether calculate it recursively if the specified reference is formula
        :returns: "#REF!" if this area is invalid;
        "#N/A" if given offset out of this area;
        Otherwise return the cell value at given position.'''
        ...
    
    @property
    def is_external_link(self) -> bool:
        ...
    
    @property
    def external_file_name(self) -> str:
        ...
    
    @property
    def sheet_name(self) -> str:
        ...
    
    @property
    def is_area(self) -> bool:
        ...
    
    @property
    def end_column(self) -> int:
        ...
    
    @property
    def start_column(self) -> int:
        ...
    
    @property
    def end_row(self) -> int:
        ...
    
    @property
    def start_row(self) -> int:
        ...
    
    ...

class ReferredAreaCollection:
    '''Represents all referred cells and areas.'''
    
    @overload
    def copy_to(self, array : List[aspose.cells.ReferredArea]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.ReferredArea], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.ReferredArea, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.ReferredArea, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.ReferredArea) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.ReferredArea, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.ReferredArea, index : int, count : int) -> int:
        ...
    
    def binary_search(self, item : aspose.cells.ReferredArea) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class ReplaceOptions:
    '''Represent the replace options.'''
    
    @property
    def case_sensitive(self) -> bool:
        ...
    
    @case_sensitive.setter
    def case_sensitive(self, value : bool):
        ...
    
    @property
    def match_entire_cell_contents(self) -> bool:
        ...
    
    @match_entire_cell_contents.setter
    def match_entire_cell_contents(self, value : bool):
        ...
    
    @property
    def regex_key(self) -> bool:
        ...
    
    @regex_key.setter
    def regex_key(self, value : bool):
        ...
    
    ...

class Row:
    '''Represents a single row in a worksheet.'''
    
    def get_cell_by_index(self, index : int) -> aspose.cells.Cell:
        '''Get the cell by specific index in the list.
        
        :param index: The position.
        :returns: The Cell object.'''
        ...
    
    def get_cell_or_null(self, column : int) -> aspose.cells.Cell:
        '''Gets the cell or null in the specific index.
        
        :param column: The column index
        :returns: Returns the cell object if the cell exists.
        Or returns null if the cell object does not exist.'''
        ...
    
    def get_style(self) -> aspose.cells.Style:
        '''Gets the style of this row.'''
        ...
    
    def set_style(self, style : aspose.cells.Style):
        '''Sets the style of this row.
        
        :param style: the style to be used as the default style for cells in this row.'''
        ...
    
    def copy_settings(self, source : aspose.cells.Row, check_style : bool):
        '''Copy settings of row, such as style, height, visibility, ...etc.
        
        :param source: the source row whose settings will be copied to this one
        :param check_style: whether check and gather style.
        Only takes effect and be needed when two row objects belong to different workbook and the styles of two workbooks are different.'''
        ...
    
    def apply_style(self, style : aspose.cells.Style, flag : aspose.cells.StyleFlag):
        '''Applies formats for a whole row.
        
        :param style: The style object which will be applied.
        :param flag: Flags which indicates applied formatting properties.'''
        ...
    
    def equals(self, row : aspose.cells.Row) -> bool:
        '''Checks whether this object refers to the same row with another row object.
        
        :param row: another row object
        :returns: true if two row objects refers to the same row.'''
        ...
    
    @property
    def is_blank(self) -> bool:
        ...
    
    @property
    def is_collapsed(self) -> bool:
        ...
    
    @is_collapsed.setter
    def is_collapsed(self, value : bool):
        ...
    
    @property
    def height(self) -> float:
        '''Gets and sets the row height in unit of Points.'''
        ...
    
    @height.setter
    def height(self, value : float):
        '''Gets and sets the row height in unit of Points.'''
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def index(self) -> int:
        '''Gets the index of this row.'''
        ...
    
    @property
    def group_level(self) -> byte:
        ...
    
    @group_level.setter
    def group_level(self, value : byte):
        ...
    
    @property
    def is_height_matched(self) -> bool:
        ...
    
    @is_height_matched.setter
    def is_height_matched(self, value : bool):
        ...
    
    @property
    def style(self) -> aspose.cells.Style:
        '''Represents the style of this row.'''
        ...
    
    @property
    def has_custom_style(self) -> bool:
        ...
    
    @property
    def first_cell(self) -> aspose.cells.Cell:
        ...
    
    @property
    def first_data_cell(self) -> aspose.cells.Cell:
        ...
    
    @property
    def last_cell(self) -> aspose.cells.Cell:
        ...
    
    @property
    def last_data_cell(self) -> aspose.cells.Cell:
        ...
    
    def __getitem__(self, key : int) -> aspose.cells.Cell:
        '''Gets the cell.'''
        ...
    
    ...

class RowCollection:
    '''Collects the :py:class:`aspose.cells.Row` objects that represent the individual rows in a worksheet.'''
    
    def get_row_by_index(self, index : int) -> aspose.cells.Row:
        '''Gets the row object by the position in the list.
        
        :param index: The position.
        :returns: The Row object at given position.'''
        ...
    
    def clear(self):
        '''Clear all rows and cells.'''
        ...
    
    def remove_at(self, index : int):
        '''Remove the row at the specified index
        
        :param index: zero-based row index'''
        ...
    
    @property
    def count(self) -> int:
        '''Gets the number of rows in this collection.'''
        ...
    
    def __getitem__(self, key : int) -> aspose.cells.Row:
        '''Gets a :py:class:`aspose.cells.Row` object by given row index. The Row object of given row index will be instantiated if it does not exist before.'''
        ...
    
    ...

class SaveOptions:
    '''Represents all save options'''
    
    @property
    def save_format(self) -> aspose.cells.SaveFormat:
        ...
    
    @property
    def clear_data(self) -> bool:
        ...
    
    @clear_data.setter
    def clear_data(self, value : bool):
        ...
    
    @property
    def cached_file_folder(self) -> str:
        ...
    
    @cached_file_folder.setter
    def cached_file_folder(self, value : str):
        ...
    
    @property
    def validate_merged_areas(self) -> bool:
        ...
    
    @validate_merged_areas.setter
    def validate_merged_areas(self, value : bool):
        ...
    
    @property
    def merge_areas(self) -> bool:
        ...
    
    @merge_areas.setter
    def merge_areas(self, value : bool):
        ...
    
    @property
    def create_directory(self) -> bool:
        ...
    
    @create_directory.setter
    def create_directory(self, value : bool):
        ...
    
    @property
    def sort_names(self) -> bool:
        ...
    
    @sort_names.setter
    def sort_names(self, value : bool):
        ...
    
    @property
    def sort_external_names(self) -> bool:
        ...
    
    @sort_external_names.setter
    def sort_external_names(self, value : bool):
        ...
    
    @property
    def refresh_chart_cache(self) -> bool:
        ...
    
    @refresh_chart_cache.setter
    def refresh_chart_cache(self, value : bool):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def update_smart_art(self) -> bool:
        ...
    
    @update_smart_art.setter
    def update_smart_art(self, value : bool):
        ...
    
    ...

class Scenario:
    '''Represents an individual scenario.'''
    
    @property
    def comment(self) -> str:
        '''Gets and sets the comment of scenario.'''
        ...
    
    @comment.setter
    def comment(self, value : str):
        '''Gets and sets the comment of scenario.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of scenario.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of scenario.'''
        ...
    
    @property
    def user(self) -> str:
        '''Gets name of user who last changed the scenario.'''
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def input_cells(self) -> aspose.cells.ScenarioInputCellCollection:
        ...
    
    ...

class ScenarioCollection:
    '''Represents the list of scenarios.'''
    
    @overload
    def copy_to(self, array : List[aspose.cells.Scenario]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.Scenario], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.Scenario, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.Scenario, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Scenario) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Scenario, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Scenario, index : int, count : int) -> int:
        ...
    
    def add(self, name : str) -> int:
        '''Adds a scenario.
        
        :param name: The name of scenario.
        :returns: The index in the list of scenarios.'''
        ...
    
    def binary_search(self, item : aspose.cells.Scenario) -> int:
        ...
    
    @property
    def active_index(self) -> int:
        ...
    
    @active_index.setter
    def active_index(self, value : int):
        ...
    
    @property
    def last_selected(self) -> int:
        ...
    
    @last_selected.setter
    def last_selected(self, value : int):
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class ScenarioInputCell:
    '''Represents input cell for the scenario.'''
    
    @property
    def row(self) -> int:
        '''Gets and sets the row index of the input cell.'''
        ...
    
    @property
    def column(self) -> int:
        '''Gets and sets the column index of the input cell.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the input cell address.'''
        ...
    
    @property
    def value(self) -> str:
        '''Gets and sets value of the input cell.'''
        ...
    
    @value.setter
    def value(self, value : str):
        '''Gets and sets value of the input cell.'''
        ...
    
    @property
    def is_deleted(self) -> bool:
        ...
    
    @is_deleted.setter
    def is_deleted(self, value : bool):
        ...
    
    ...

class ScenarioInputCellCollection:
    '''Represents the list of the scenario's input cells.'''
    
    @overload
    def copy_to(self, array : List[aspose.cells.ScenarioInputCell]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.ScenarioInputCell], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.ScenarioInputCell, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.ScenarioInputCell, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.ScenarioInputCell) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.ScenarioInputCell, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.ScenarioInputCell, index : int, count : int) -> int:
        ...
    
    def add(self, row : int, column : int, value : str) -> int:
        '''Adds an input cell.
        
        :param row: The row index of input cell.
        :param column: The column index of input cell.
        :param value: The value of input cell.'''
        ...
    
    def binary_search(self, item : aspose.cells.ScenarioInputCell) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class SpreadsheetML2003SaveOptions(SaveOptions):
    '''Represents the options for saving Excel 2003 spreadml file.'''
    
    @property
    def save_format(self) -> aspose.cells.SaveFormat:
        ...
    
    @property
    def clear_data(self) -> bool:
        ...
    
    @clear_data.setter
    def clear_data(self, value : bool):
        ...
    
    @property
    def cached_file_folder(self) -> str:
        ...
    
    @cached_file_folder.setter
    def cached_file_folder(self, value : str):
        ...
    
    @property
    def validate_merged_areas(self) -> bool:
        ...
    
    @validate_merged_areas.setter
    def validate_merged_areas(self, value : bool):
        ...
    
    @property
    def merge_areas(self) -> bool:
        ...
    
    @merge_areas.setter
    def merge_areas(self, value : bool):
        ...
    
    @property
    def create_directory(self) -> bool:
        ...
    
    @create_directory.setter
    def create_directory(self, value : bool):
        ...
    
    @property
    def sort_names(self) -> bool:
        ...
    
    @sort_names.setter
    def sort_names(self, value : bool):
        ...
    
    @property
    def sort_external_names(self) -> bool:
        ...
    
    @sort_external_names.setter
    def sort_external_names(self, value : bool):
        ...
    
    @property
    def refresh_chart_cache(self) -> bool:
        ...
    
    @refresh_chart_cache.setter
    def refresh_chart_cache(self, value : bool):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def update_smart_art(self) -> bool:
        ...
    
    @update_smart_art.setter
    def update_smart_art(self, value : bool):
        ...
    
    @property
    def is_indented_formatting(self) -> bool:
        ...
    
    @is_indented_formatting.setter
    def is_indented_formatting(self, value : bool):
        ...
    
    @property
    def limit_as_xls(self) -> bool:
        ...
    
    @limit_as_xls.setter
    def limit_as_xls(self, value : bool):
        ...
    
    @property
    def export_column_index_of_cell(self) -> bool:
        ...
    
    @export_column_index_of_cell.setter
    def export_column_index_of_cell(self, value : bool):
        ...
    
    ...

class StreamProviderOptions:
    '''Represents the stream options.'''
    
    @property
    def resource_loading_type(self) -> aspose.cells.ResourceLoadingType:
        ...
    
    @resource_loading_type.setter
    def resource_loading_type(self, value : aspose.cells.ResourceLoadingType):
        ...
    
    @property
    def default_path(self) -> str:
        ...
    
    @property
    def custom_path(self) -> str:
        ...
    
    @custom_path.setter
    def custom_path(self, value : str):
        ...
    
    @property
    def stream(self) -> io.RawIOBase:
        '''Gets/Sets the stream'''
        ...
    
    @stream.setter
    def stream(self, value : io.RawIOBase):
        '''Gets/Sets the stream'''
        ...
    
    ...

class Style:
    '''Represents display style of excel document,such as font,color,alignment,border,etc.
    The Style object contains all style attributes (font, number format, alignment, and so on) as properties.'''
    
    @overload
    def set_border(self, border_type : aspose.cells.BorderType, border_style : aspose.cells.CellBorderType, border_color : aspose.pydrawing.Color) -> bool:
        '''Sets the borders of the style.
        
        :param border_type: The border(s) to be set, can be combination of :py:class:`aspose.cells.BorderType`.
        :param border_style: The style of the border.
        :param border_color: The color of the border.
        :returns: Whether current border settings have been changed.'''
        ...
    
    @overload
    def set_border(self, border_type : aspose.cells.BorderType, border_style : aspose.cells.CellBorderType, border_color : aspose.cells.CellsColor) -> bool:
        '''Sets the borders of the style.
        
        :param border_type: The border(s) to be set, can be combination of :py:class:`aspose.cells.BorderType`.
        :param border_style: The style of the border.
        :param border_color: The color of the border.
        :returns: Whether current border settings have been changed.'''
        ...
    
    def set_pattern_color(self, pattern : aspose.cells.BackgroundType, color1 : aspose.pydrawing.Color, color2 : aspose.pydrawing.Color):
        '''Sets the background color.
        
        :param pattern: The pattern.
        :param color1: The foreground color.
        :param color2: The background color. Only works when pattern is not BackgroundType.None and BackgroundType.Solid.'''
        ...
    
    def copy(self, style : aspose.cells.Style):
        '''Copies data from another style object
        
        :param style: Source Style object'''
        ...
    
    def update(self):
        '''Apply the named style to the styles of the cells which use this named style.
        It works like clicking the "ok" button after you finished modifying the style.
        Only applies for named style.'''
        ...
    
    def is_modified(self, modify_flag : aspose.cells.StyleModifyFlag) -> bool:
        '''Checks whether the specified properties of the style have been modified.
        Used for style of ConditionalFormattings to check whether the specified properties of this style should be used when applying the ConditionalFormattings on a cell.
        
        :param modify_flag: Style modified flags
        :returns: true if the specified properties have been modified'''
        ...
    
    def set_custom(self, custom : str, builtin_preference : bool):
        '''Sets the Custom number format string of a cell.
        
        :param custom: Custom number format string, should be InvariantCulture pattern.
        :param builtin_preference: If given Custom number format string matches one of the built-in number formats
        corresponding to current regional settings, whether set the number format as built-in instead of Custom.'''
        ...
    
    def set_two_color_gradient(self, color1 : aspose.pydrawing.Color, color2 : aspose.pydrawing.Color, gradient_style_type : aspose.cells.drawing.GradientStyleType, variant : int):
        '''Sets the specified fill to a two-color gradient.
        
        :param color1: One gradient color.
        :param color2: Two gradient color.
        :param gradient_style_type: Gradient shading style.
        :param variant: The gradient variant. Can be a value from 1 through 4, corresponding to one of the four variants on the Gradient tab in the Fill Effects dialog box. If style is GradientStyle.FromCenter, the Variant argument can only be 1 or 2.'''
        ...
    
    def get_two_color_gradient(self, color1 : aspose.pydrawing.Color&, color2 : aspose.pydrawing.Color&, gradient_style_type : Any, variant : Any):
        '''Get the two-color gradient setting.
        
        :param color1: One gradient color.
        :param color2: Two gradient color.
        :param gradient_style_type: Gradient shading style.
        :param variant: The gradient variant.'''
        ...
    
    def get_two_color_gradient_setting(self) -> aspose.cells.TwoColorGradient:
        '''Get the two-color gradient setting.'''
        ...
    
    def to_json(self) -> str:
        '''Convert :py:class:`aspose.cells.Style` to JSON struct data.'''
        ...
    
    @property
    def background_theme_color(self) -> aspose.cells.ThemeColor:
        ...
    
    @background_theme_color.setter
    def background_theme_color(self, value : aspose.cells.ThemeColor):
        ...
    
    @property
    def foreground_theme_color(self) -> aspose.cells.ThemeColor:
        ...
    
    @foreground_theme_color.setter
    def foreground_theme_color(self, value : aspose.cells.ThemeColor):
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name of the style.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name of the style.'''
        ...
    
    @property
    def pattern(self) -> aspose.cells.BackgroundType:
        '''Gets the cell background pattern type.'''
        ...
    
    @pattern.setter
    def pattern(self, value : aspose.cells.BackgroundType):
        '''Sets the cell background pattern type.'''
        ...
    
    @property
    def borders(self) -> aspose.cells.BorderCollection:
        '''Gets the :py:class:`aspose.cells.BorderCollection` of the style.'''
        ...
    
    @property
    def background_color(self) -> aspose.pydrawing.Color:
        ...
    
    @background_color.setter
    def background_color(self, value : aspose.pydrawing.Color):
        ...
    
    @property
    def background_argb_color(self) -> int:
        ...
    
    @background_argb_color.setter
    def background_argb_color(self, value : int):
        ...
    
    @property
    def foreground_color(self) -> aspose.pydrawing.Color:
        ...
    
    @foreground_color.setter
    def foreground_color(self, value : aspose.pydrawing.Color):
        ...
    
    @property
    def foreground_argb_color(self) -> int:
        ...
    
    @foreground_argb_color.setter
    def foreground_argb_color(self, value : int):
        ...
    
    @property
    def has_borders(self) -> bool:
        ...
    
    @property
    def parent_style(self) -> aspose.cells.Style:
        ...
    
    @property
    def indent_level(self) -> int:
        ...
    
    @indent_level.setter
    def indent_level(self, value : int):
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Gets a :py:attr:`aspose.cells.Style.font` object.'''
        ...
    
    @property
    def rotation_angle(self) -> int:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : int):
        ...
    
    @property
    def horizontal_alignment(self) -> aspose.cells.TextAlignmentType:
        ...
    
    @horizontal_alignment.setter
    def horizontal_alignment(self, value : aspose.cells.TextAlignmentType):
        ...
    
    @property
    def vertical_alignment(self) -> aspose.cells.TextAlignmentType:
        ...
    
    @vertical_alignment.setter
    def vertical_alignment(self, value : aspose.cells.TextAlignmentType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
        ...
    
    @property
    def number(self) -> int:
        '''Gets the display format of numbers and dates. The formatting patterns are different for different regions.'''
        ...
    
    @number.setter
    def number(self, value : int):
        '''Sets the display format of numbers and dates. The formatting patterns are different for different regions.'''
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def custom(self) -> str:
        '''Represents the custom number format string of this style object.
        If the custom number format is not set(For example, the number format is builtin), "" will be returned.'''
        ...
    
    @custom.setter
    def custom(self, value : str):
        '''Represents the custom number format string of this style object.
        If the custom number format is not set(For example, the number format is builtin), "" will be returned.'''
        ...
    
    @property
    def culture_custom(self) -> str:
        ...
    
    @culture_custom.setter
    def culture_custom(self, value : str):
        ...
    
    @property
    def invariant_custom(self) -> str:
        ...
    
    @property
    def is_formula_hidden(self) -> bool:
        ...
    
    @is_formula_hidden.setter
    def is_formula_hidden(self, value : bool):
        ...
    
    @property
    def shrink_to_fit(self) -> bool:
        ...
    
    @shrink_to_fit.setter
    def shrink_to_fit(self, value : bool):
        ...
    
    @property
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def is_justify_distributed(self) -> bool:
        ...
    
    @is_justify_distributed.setter
    def is_justify_distributed(self, value : bool):
        ...
    
    @property
    def quote_prefix(self) -> bool:
        ...
    
    @quote_prefix.setter
    def quote_prefix(self, value : bool):
        ...
    
    @property
    def is_gradient(self) -> bool:
        ...
    
    @is_gradient.setter
    def is_gradient(self, value : bool):
        ...
    
    @property
    def is_percent(self) -> bool:
        ...
    
    @property
    def is_date_time(self) -> bool:
        ...
    
    ...

class StyleFlag:
    '''Represents flags which indicates applied formatting properties.'''
    
    @property
    def all(self) -> bool:
        '''All properties will be applied.'''
        ...
    
    @all.setter
    def all(self, value : bool):
        '''All properties will be applied.'''
        ...
    
    @property
    def borders(self) -> bool:
        '''All borders settings will be applied.'''
        ...
    
    @borders.setter
    def borders(self, value : bool):
        '''All borders settings will be applied.'''
        ...
    
    @property
    def left_border(self) -> bool:
        ...
    
    @left_border.setter
    def left_border(self, value : bool):
        ...
    
    @property
    def right_border(self) -> bool:
        ...
    
    @right_border.setter
    def right_border(self, value : bool):
        ...
    
    @property
    def top_border(self) -> bool:
        ...
    
    @top_border.setter
    def top_border(self, value : bool):
        ...
    
    @property
    def bottom_border(self) -> bool:
        ...
    
    @bottom_border.setter
    def bottom_border(self, value : bool):
        ...
    
    @property
    def diagonal_down_border(self) -> bool:
        ...
    
    @diagonal_down_border.setter
    def diagonal_down_border(self, value : bool):
        ...
    
    @property
    def diagonal_up_border(self) -> bool:
        ...
    
    @diagonal_up_border.setter
    def diagonal_up_border(self, value : bool):
        ...
    
    @property
    def font(self) -> bool:
        '''Font settings will be applied.'''
        ...
    
    @font.setter
    def font(self, value : bool):
        '''Font settings will be applied.'''
        ...
    
    @property
    def font_size(self) -> bool:
        ...
    
    @font_size.setter
    def font_size(self, value : bool):
        ...
    
    @property
    def font_name(self) -> bool:
        ...
    
    @font_name.setter
    def font_name(self, value : bool):
        ...
    
    @property
    def font_color(self) -> bool:
        ...
    
    @font_color.setter
    def font_color(self, value : bool):
        ...
    
    @property
    def font_bold(self) -> bool:
        ...
    
    @font_bold.setter
    def font_bold(self, value : bool):
        ...
    
    @property
    def font_italic(self) -> bool:
        ...
    
    @font_italic.setter
    def font_italic(self, value : bool):
        ...
    
    @property
    def font_underline(self) -> bool:
        ...
    
    @font_underline.setter
    def font_underline(self, value : bool):
        ...
    
    @property
    def font_strike(self) -> bool:
        ...
    
    @font_strike.setter
    def font_strike(self, value : bool):
        ...
    
    @property
    def font_script(self) -> bool:
        ...
    
    @font_script.setter
    def font_script(self, value : bool):
        ...
    
    @property
    def number_format(self) -> bool:
        ...
    
    @number_format.setter
    def number_format(self, value : bool):
        ...
    
    @property
    def alignments(self) -> bool:
        '''Alignment setting will be applied.'''
        ...
    
    @alignments.setter
    def alignments(self, value : bool):
        '''Alignment setting will be applied.'''
        ...
    
    @property
    def horizontal_alignment(self) -> bool:
        ...
    
    @horizontal_alignment.setter
    def horizontal_alignment(self, value : bool):
        ...
    
    @property
    def vertical_alignment(self) -> bool:
        ...
    
    @vertical_alignment.setter
    def vertical_alignment(self, value : bool):
        ...
    
    @property
    def indent(self) -> bool:
        '''Indent level setting will be applied.'''
        ...
    
    @indent.setter
    def indent(self, value : bool):
        '''Indent level setting will be applied.'''
        ...
    
    @property
    def rotation(self) -> bool:
        '''Rotation setting will be applied.'''
        ...
    
    @rotation.setter
    def rotation(self, value : bool):
        '''Rotation setting will be applied.'''
        ...
    
    @property
    def wrap_text(self) -> bool:
        ...
    
    @wrap_text.setter
    def wrap_text(self, value : bool):
        ...
    
    @property
    def shrink_to_fit(self) -> bool:
        ...
    
    @shrink_to_fit.setter
    def shrink_to_fit(self, value : bool):
        ...
    
    @property
    def text_direction(self) -> bool:
        ...
    
    @text_direction.setter
    def text_direction(self, value : bool):
        ...
    
    @property
    def cell_shading(self) -> bool:
        ...
    
    @cell_shading.setter
    def cell_shading(self, value : bool):
        ...
    
    @property
    def locked(self) -> bool:
        '''Locked setting will be applied.'''
        ...
    
    @locked.setter
    def locked(self, value : bool):
        '''Locked setting will be applied.'''
        ...
    
    @property
    def hide_formula(self) -> bool:
        ...
    
    @hide_formula.setter
    def hide_formula(self, value : bool):
        ...
    
    @property
    def quote_prefix(self) -> bool:
        ...
    
    @quote_prefix.setter
    def quote_prefix(self, value : bool):
        ...
    
    ...

class SubtotalSetting:
    '''Represents the setting of the subtotal .'''
    
    @property
    def group_by(self) -> int:
        ...
    
    @property
    def subtotal_function(self) -> aspose.cells.ConsolidationFunction:
        ...
    
    @property
    def total_list(self) -> List[int]:
        ...
    
    @property
    def summary_below_data(self) -> bool:
        ...
    
    ...

class SvgSaveOptions(ImageSaveOptions):
    
    @property
    def save_format(self) -> aspose.cells.SaveFormat:
        ...
    
    @property
    def clear_data(self) -> bool:
        ...
    
    @clear_data.setter
    def clear_data(self, value : bool):
        ...
    
    @property
    def cached_file_folder(self) -> str:
        ...
    
    @cached_file_folder.setter
    def cached_file_folder(self, value : str):
        ...
    
    @property
    def validate_merged_areas(self) -> bool:
        ...
    
    @validate_merged_areas.setter
    def validate_merged_areas(self, value : bool):
        ...
    
    @property
    def merge_areas(self) -> bool:
        ...
    
    @merge_areas.setter
    def merge_areas(self, value : bool):
        ...
    
    @property
    def create_directory(self) -> bool:
        ...
    
    @create_directory.setter
    def create_directory(self, value : bool):
        ...
    
    @property
    def sort_names(self) -> bool:
        ...
    
    @sort_names.setter
    def sort_names(self, value : bool):
        ...
    
    @property
    def sort_external_names(self) -> bool:
        ...
    
    @sort_external_names.setter
    def sort_external_names(self, value : bool):
        ...
    
    @property
    def refresh_chart_cache(self) -> bool:
        ...
    
    @refresh_chart_cache.setter
    def refresh_chart_cache(self, value : bool):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def update_smart_art(self) -> bool:
        ...
    
    @update_smart_art.setter
    def update_smart_art(self, value : bool):
        ...
    
    @property
    def image_or_print_options(self) -> aspose.cells.rendering.ImageOrPrintOptions:
        ...
    
    @property
    def stream_provider(self) -> aspose.cells.IStreamProvider:
        ...
    
    @stream_provider.setter
    def stream_provider(self, value : aspose.cells.IStreamProvider):
        ...
    
    @property
    def sheet_index(self) -> int:
        ...
    
    @sheet_index.setter
    def sheet_index(self, value : int):
        ...
    
    ...

class ThemeColor:
    '''Represents a theme color.'''
    
    @property
    def color_type(self) -> aspose.cells.ThemeColorType:
        ...
    
    @color_type.setter
    def color_type(self, value : aspose.cells.ThemeColorType):
        ...
    
    @property
    def tint(self) -> float:
        '''Gets and sets the tint value.'''
        ...
    
    @tint.setter
    def tint(self, value : float):
        '''Gets and sets the tint value.'''
        ...
    
    ...

class ThreadedComment:
    '''Represents the threaded comment.'''
    
    @property
    def row(self) -> int:
        '''Gets the row index of the comment.'''
        ...
    
    @property
    def column(self) -> int:
        '''Gets the column index of the comment.'''
        ...
    
    @property
    def notes(self) -> str:
        '''Gets and sets the text of the comment.'''
        ...
    
    @notes.setter
    def notes(self, value : str):
        '''Gets and sets the text of the comment.'''
        ...
    
    @property
    def author(self) -> aspose.cells.ThreadedCommentAuthor:
        '''Gets the author of the comment.'''
        ...
    
    @author.setter
    def author(self, value : aspose.cells.ThreadedCommentAuthor):
        '''Gets the author of the comment.'''
        ...
    
    @property
    def created_time(self) -> DateTime:
        ...
    
    @created_time.setter
    def created_time(self, value : DateTime):
        ...
    
    ...

class ThreadedCommentAuthor:
    '''Represents the person who creates the threaded comments;'''
    
    @property
    def name(self) -> str:
        '''Gets and sets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name.'''
        ...
    
    @property
    def user_id(self) -> str:
        ...
    
    @user_id.setter
    def user_id(self, value : str):
        ...
    
    @property
    def provider_id(self) -> str:
        ...
    
    @provider_id.setter
    def provider_id(self, value : str):
        ...
    
    ...

class ThreadedCommentAuthorCollection:
    '''Represents all persons who .'''
    
    @overload
    def copy_to(self, array : List[aspose.cells.ThreadedCommentAuthor]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.ThreadedCommentAuthor], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.ThreadedCommentAuthor, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.ThreadedCommentAuthor, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.ThreadedCommentAuthor) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.ThreadedCommentAuthor, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.ThreadedCommentAuthor, index : int, count : int) -> int:
        ...
    
    def add(self, name : str, user_id : str, provider_id : str) -> int:
        '''Adds one thread comment person.
        
        :param name: The name of the person.
        :param provider_id: The id of the provider'''
        ...
    
    def binary_search(self, item : aspose.cells.ThreadedCommentAuthor) -> int:
        ...
    
    @property
    def current_person(self) -> aspose.cells.ThreadedCommentAuthor:
        ...
    
    @current_person.setter
    def current_person(self, value : aspose.cells.ThreadedCommentAuthor):
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class ThreadedCommentCollection:
    '''Represents the list of threaded comments.'''
    
    @overload
    def copy_to(self, array : List[aspose.cells.ThreadedComment]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.ThreadedComment], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.ThreadedComment, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.ThreadedComment, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.ThreadedComment) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.ThreadedComment, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.ThreadedComment, index : int, count : int) -> int:
        ...
    
    def add(self, text : str, author : aspose.cells.ThreadedCommentAuthor) -> int:
        '''Adds a threaded comment;
        
        :param text: The text of the threaded comment.
        :param author: The author of the threaded comment'''
        ...
    
    def binary_search(self, item : aspose.cells.ThreadedComment) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class Top10:
    '''Describe the Top10 conditional formatting rule.
    This conditional formatting rule highlights cells whose
    values fall in the top N or bottom N bracket, as specified.'''
    
    @property
    def is_percent(self) -> bool:
        ...
    
    @is_percent.setter
    def is_percent(self, value : bool):
        ...
    
    @property
    def is_bottom(self) -> bool:
        ...
    
    @is_bottom.setter
    def is_bottom(self, value : bool):
        ...
    
    @property
    def rank(self) -> int:
        '''Get or set the value of "n" in a "top/bottom n" conditional formatting rule.
        If IsPercent is true, the value must between 0 and 100.
        Otherwise it must between 0 and 1000.
        Default value is 10.'''
        ...
    
    @rank.setter
    def rank(self, value : int):
        '''Get or set the value of "n" in a "top/bottom n" conditional formatting rule.
        If IsPercent is true, the value must between 0 and 100.
        Otherwise it must between 0 and 1000.
        Default value is 10.'''
        ...
    
    ...

class Top10Filter:
    '''Represents the top 10 filter.'''
    
    @property
    def is_top(self) -> bool:
        ...
    
    @is_top.setter
    def is_top(self, value : bool):
        ...
    
    @property
    def is_percent(self) -> bool:
        ...
    
    @is_percent.setter
    def is_percent(self, value : bool):
        ...
    
    @property
    def items(self) -> int:
        '''Gets and sets the items of the filter.'''
        ...
    
    @items.setter
    def items(self, value : int):
        '''Gets and sets the items of the filter.'''
        ...
    
    @property
    def criteria(self) -> any:
        ...
    
    @criteria.setter
    def criteria(self, value : any):
        ...
    
    ...

class TwoColorGradient:
    '''Represents two color gradient.'''
    
    @property
    def color1(self) -> aspose.pydrawing.Color:
        '''Gets and sets the first gradient color.'''
        ...
    
    @color1.setter
    def color1(self, value : aspose.pydrawing.Color):
        '''Gets and sets the first gradient color.'''
        ...
    
    @property
    def color2(self) -> aspose.pydrawing.Color:
        '''Gets and sets the second gradient color.'''
        ...
    
    @color2.setter
    def color2(self, value : aspose.pydrawing.Color):
        '''Gets and sets the second gradient color.'''
        ...
    
    @property
    def gradient_style_type(self) -> aspose.cells.drawing.GradientStyleType:
        ...
    
    @gradient_style_type.setter
    def gradient_style_type(self, value : aspose.cells.drawing.GradientStyleType):
        ...
    
    @property
    def variant(self) -> int:
        '''Gets and sets the gradient variant.'''
        ...
    
    @variant.setter
    def variant(self, value : int):
        '''Gets and sets the gradient variant.'''
        ...
    
    ...

class TxtLoadOptions(AbstractTextLoadOptions):
    '''Represents the options for loading text file.'''
    
    def set_paper_size(self, type : aspose.cells.PaperSizeType):
        '''Sets the default print paper size from default printer's setting.
        
        :param type: The default paper size.'''
        ...
    
    @property
    def load_format(self) -> aspose.cells.LoadFormat:
        ...
    
    @property
    def password(self) -> str:
        '''Gets and set the password of the workbook.'''
        ...
    
    @password.setter
    def password(self, value : str):
        '''Gets and set the password of the workbook.'''
        ...
    
    @property
    def parsing_formula_on_open(self) -> bool:
        ...
    
    @parsing_formula_on_open.setter
    def parsing_formula_on_open(self, value : bool):
        ...
    
    @property
    def parsing_pivot_cached_records(self) -> bool:
        ...
    
    @parsing_pivot_cached_records.setter
    def parsing_pivot_cached_records(self, value : bool):
        ...
    
    @property
    def language_code(self) -> aspose.cells.CountryCode:
        ...
    
    @language_code.setter
    def language_code(self, value : aspose.cells.CountryCode):
        ...
    
    @property
    def region(self) -> aspose.cells.CountryCode:
        '''Gets the system regional settings based on CountryCode at the time the file was loaded.'''
        ...
    
    @region.setter
    def region(self, value : aspose.cells.CountryCode):
        '''Sets the system regional settings based on CountryCode at the time the file was loaded.'''
        ...
    
    @property
    def default_style_settings(self) -> aspose.cells.DefaultStyleSettings:
        ...
    
    @property
    def standard_font(self) -> str:
        ...
    
    @standard_font.setter
    def standard_font(self, value : str):
        ...
    
    @property
    def standard_font_size(self) -> float:
        ...
    
    @standard_font_size.setter
    def standard_font_size(self, value : float):
        ...
    
    @property
    def interrupt_monitor(self) -> aspose.cells.AbstractInterruptMonitor:
        ...
    
    @interrupt_monitor.setter
    def interrupt_monitor(self, value : aspose.cells.AbstractInterruptMonitor):
        ...
    
    @property
    def ignore_not_printed(self) -> bool:
        ...
    
    @ignore_not_printed.setter
    def ignore_not_printed(self, value : bool):
        ...
    
    @property
    def check_data_valid(self) -> bool:
        ...
    
    @check_data_valid.setter
    def check_data_valid(self, value : bool):
        ...
    
    @property
    def check_excel_restriction(self) -> bool:
        ...
    
    @check_excel_restriction.setter
    def check_excel_restriction(self, value : bool):
        ...
    
    @property
    def keep_unparsed_data(self) -> bool:
        ...
    
    @keep_unparsed_data.setter
    def keep_unparsed_data(self, value : bool):
        ...
    
    @property
    def load_filter(self) -> aspose.cells.LoadFilter:
        ...
    
    @load_filter.setter
    def load_filter(self, value : aspose.cells.LoadFilter):
        ...
    
    @property
    def light_cells_data_handler(self) -> aspose.cells.LightCellsDataHandler:
        ...
    
    @light_cells_data_handler.setter
    def light_cells_data_handler(self, value : aspose.cells.LightCellsDataHandler):
        ...
    
    @property
    def memory_setting(self) -> aspose.cells.MemorySetting:
        ...
    
    @memory_setting.setter
    def memory_setting(self, value : aspose.cells.MemorySetting):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def auto_fitter_options(self) -> aspose.cells.AutoFitterOptions:
        ...
    
    @auto_fitter_options.setter
    def auto_fitter_options(self, value : aspose.cells.AutoFitterOptions):
        ...
    
    @property
    def auto_filter(self) -> bool:
        ...
    
    @auto_filter.setter
    def auto_filter(self, value : bool):
        ...
    
    @property
    def font_configs(self) -> aspose.cells.IndividualFontConfigs:
        ...
    
    @font_configs.setter
    def font_configs(self, value : aspose.cells.IndividualFontConfigs):
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets and sets the default encoding. Only applies for csv file.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Gets and sets the default encoding. Only applies for csv file.'''
        ...
    
    @property
    def load_style_strategy(self) -> aspose.cells.TxtLoadStyleStrategy:
        ...
    
    @load_style_strategy.setter
    def load_style_strategy(self, value : aspose.cells.TxtLoadStyleStrategy):
        ...
    
    @property
    def convert_numeric_data(self) -> bool:
        ...
    
    @convert_numeric_data.setter
    def convert_numeric_data(self, value : bool):
        ...
    
    @property
    def convert_date_time_data(self) -> bool:
        ...
    
    @convert_date_time_data.setter
    def convert_date_time_data(self, value : bool):
        ...
    
    @property
    def keep_precision(self) -> bool:
        ...
    
    @keep_precision.setter
    def keep_precision(self, value : bool):
        ...
    
    @property
    def separator(self) -> char:
        '''Gets and sets character separator of text file.'''
        ...
    
    @separator.setter
    def separator(self, value : char):
        '''Gets and sets character separator of text file.'''
        ...
    
    @property
    def separator_string(self) -> str:
        ...
    
    @separator_string.setter
    def separator_string(self, value : str):
        ...
    
    @property
    def is_multi_encoded(self) -> bool:
        ...
    
    @is_multi_encoded.setter
    def is_multi_encoded(self, value : bool):
        ...
    
    @property
    def preferred_parsers(self) -> List[aspose.cells.ICustomParser]:
        ...
    
    @preferred_parsers.setter
    def preferred_parsers(self, value : List[aspose.cells.ICustomParser]):
        ...
    
    @property
    def has_formula(self) -> bool:
        ...
    
    @has_formula.setter
    def has_formula(self, value : bool):
        ...
    
    @property
    def has_text_qualifier(self) -> bool:
        ...
    
    @has_text_qualifier.setter
    def has_text_qualifier(self, value : bool):
        ...
    
    @property
    def text_qualifier(self) -> char:
        ...
    
    @text_qualifier.setter
    def text_qualifier(self, value : char):
        ...
    
    @property
    def treat_consecutive_delimiters_as_one(self) -> bool:
        ...
    
    @treat_consecutive_delimiters_as_one.setter
    def treat_consecutive_delimiters_as_one(self, value : bool):
        ...
    
    @property
    def treat_quote_prefix_as_value(self) -> bool:
        ...
    
    @treat_quote_prefix_as_value.setter
    def treat_quote_prefix_as_value(self, value : bool):
        ...
    
    @property
    def extend_to_next_sheet(self) -> bool:
        ...
    
    @extend_to_next_sheet.setter
    def extend_to_next_sheet(self, value : bool):
        ...
    
    ...

class TxtSaveOptions(SaveOptions):
    '''Represents the save options for csv/tab delimited/other text format.'''
    
    @property
    def save_format(self) -> aspose.cells.SaveFormat:
        ...
    
    @property
    def clear_data(self) -> bool:
        ...
    
    @clear_data.setter
    def clear_data(self, value : bool):
        ...
    
    @property
    def cached_file_folder(self) -> str:
        ...
    
    @cached_file_folder.setter
    def cached_file_folder(self, value : str):
        ...
    
    @property
    def validate_merged_areas(self) -> bool:
        ...
    
    @validate_merged_areas.setter
    def validate_merged_areas(self, value : bool):
        ...
    
    @property
    def merge_areas(self) -> bool:
        ...
    
    @merge_areas.setter
    def merge_areas(self, value : bool):
        ...
    
    @property
    def create_directory(self) -> bool:
        ...
    
    @create_directory.setter
    def create_directory(self, value : bool):
        ...
    
    @property
    def sort_names(self) -> bool:
        ...
    
    @sort_names.setter
    def sort_names(self, value : bool):
        ...
    
    @property
    def sort_external_names(self) -> bool:
        ...
    
    @sort_external_names.setter
    def sort_external_names(self, value : bool):
        ...
    
    @property
    def refresh_chart_cache(self) -> bool:
        ...
    
    @refresh_chart_cache.setter
    def refresh_chart_cache(self, value : bool):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def update_smart_art(self) -> bool:
        ...
    
    @update_smart_art.setter
    def update_smart_art(self, value : bool):
        ...
    
    @property
    def separator(self) -> char:
        '''Gets and sets char Delimiter of text file.'''
        ...
    
    @separator.setter
    def separator(self, value : char):
        '''Gets and sets char Delimiter of text file.'''
        ...
    
    @property
    def separator_string(self) -> str:
        ...
    
    @separator_string.setter
    def separator_string(self, value : str):
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets and sets the default encoding.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Gets and sets the default encoding.'''
        ...
    
    @property
    def always_quoted(self) -> bool:
        ...
    
    @always_quoted.setter
    def always_quoted(self, value : bool):
        ...
    
    @property
    def quote_type(self) -> aspose.cells.TxtValueQuoteType:
        ...
    
    @quote_type.setter
    def quote_type(self, value : aspose.cells.TxtValueQuoteType):
        ...
    
    @property
    def format_strategy(self) -> aspose.cells.CellValueFormatStrategy:
        ...
    
    @format_strategy.setter
    def format_strategy(self, value : aspose.cells.CellValueFormatStrategy):
        ...
    
    @property
    def light_cells_data_provider(self) -> aspose.cells.LightCellsDataProvider:
        ...
    
    @light_cells_data_provider.setter
    def light_cells_data_provider(self, value : aspose.cells.LightCellsDataProvider):
        ...
    
    @property
    def trim_leading_blank_row_and_column(self) -> bool:
        ...
    
    @trim_leading_blank_row_and_column.setter
    def trim_leading_blank_row_and_column(self, value : bool):
        ...
    
    @property
    def trim_tailing_blank_cells(self) -> bool:
        ...
    
    @trim_tailing_blank_cells.setter
    def trim_tailing_blank_cells(self, value : bool):
        ...
    
    @property
    def keep_separators_for_blank_row(self) -> bool:
        ...
    
    @keep_separators_for_blank_row.setter
    def keep_separators_for_blank_row(self, value : bool):
        ...
    
    @property
    def export_area(self) -> aspose.cells.CellArea:
        ...
    
    @export_area.setter
    def export_area(self, value : aspose.cells.CellArea):
        ...
    
    @property
    def export_quote_prefix(self) -> bool:
        ...
    
    @export_quote_prefix.setter
    def export_quote_prefix(self, value : bool):
        ...
    
    @property
    def export_all_sheets(self) -> bool:
        ...
    
    @export_all_sheets.setter
    def export_all_sheets(self, value : bool):
        ...
    
    ...

class UnionRange:
    '''Represents union range.'''
    
    @overload
    def set_outline_borders(self, border_styles : List[aspose.cells.CellBorderType], border_colors : aspose.pydrawing.Color[]):
        '''Sets out line borders around a range of cells.
        
        :param border_styles: Border styles.
        :param border_colors: Border colors.'''
        ...
    
    @overload
    def set_outline_borders(self, border_style : aspose.cells.CellBorderType, border_color : aspose.pydrawing.Color):
        '''Sets the outline borders around a range of cells with same border style and color.
        
        :param border_style: Border style.
        :param border_color: Border color.'''
        ...
    
    @overload
    def intersect(self, range : str) -> aspose.cells.UnionRange:
        '''Intersects another range.
        
        :param range: The range.'''
        ...
    
    @overload
    def intersect(self, union_range : aspose.cells.UnionRange) -> aspose.cells.UnionRange:
        '''Intersects another range.
        
        :param union_range: The range.'''
        ...
    
    @overload
    def intersect(self, ranges : List[aspose.cells.Range]) -> aspose.cells.UnionRange:
        '''Intersects another range.
        
        :param ranges: The range.'''
        ...
    
    @overload
    def union(self, range : str) -> aspose.cells.UnionRange:
        '''Union another range.
        
        :param range: The range.'''
        ...
    
    @overload
    def union(self, union_range : aspose.cells.UnionRange) -> aspose.cells.UnionRange:
        '''Union another range.
        
        :param union_range: The range.'''
        ...
    
    @overload
    def union(self, ranges : List[aspose.cells.Range]) -> aspose.cells.UnionRange:
        '''Union the ranges.
        
        :param ranges: The ranges.'''
        ...
    
    def merge(self):
        '''Combines a range of cells into a single cell.'''
        ...
    
    def un_merge(self):
        '''Unmerges merged cells of this range.'''
        ...
    
    def put_value(self, string_value : str, is_converted : bool, set_style : bool):
        '''Puts a value into the range, if appropriate the value will be converted to other data type and cell's number format will be reset.
        
        :param string_value: Input value
        :param is_converted: True: converted to other data type if appropriate.
        :param set_style: True: set the number format to cell's style when converting to other data type'''
        ...
    
    def set_style(self, style : aspose.cells.Style):
        '''Sets the style of the range.
        
        :param style: The Style object.'''
        ...
    
    def apply_style(self, style : aspose.cells.Style, flag : aspose.cells.StyleFlag):
        '''Applies formats for a whole range.
        
        :param style: The style object which will be applied.
        :param flag: Flags which indicates applied formatting properties.'''
        ...
    
    def copy(self, range : aspose.cells.UnionRange, options : aspose.cells.PasteOptions):
        '''Copying the range with paste special options.
        
        :param range: The source range.
        :param options: The paste special options.'''
        ...
    
    def get_enumerator(self) -> collections.abc.Iterator:
        '''Gets the enumerator for cells in this Range.
        
        :returns: The cells enumerator'''
        ...
    
    @property
    def first_row(self) -> int:
        ...
    
    @property
    def first_column(self) -> int:
        ...
    
    @property
    def row_count(self) -> int:
        ...
    
    @property
    def column_count(self) -> int:
        ...
    
    @property
    def value(self) -> any:
        '''Gets and sets the values of the range.'''
        ...
    
    @value.setter
    def value(self, value : any):
        '''Gets and sets the values of the range.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name of the range.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name of the range.'''
        ...
    
    @property
    def refers_to(self) -> str:
        ...
    
    @property
    def has_range(self) -> bool:
        ...
    
    @property
    def hyperlinks(self) -> List[aspose.cells.Hyperlink]:
        '''Gets all hyperlink in the range.'''
        ...
    
    @property
    def cell_count(self) -> int:
        ...
    
    @property
    def range_count(self) -> int:
        ...
    
    @property
    def ranges(self) -> List[aspose.cells.Range]:
        '''Gets all union ranges.'''
        ...
    
    ...

class Validation:
    '''Represents data validation.settings.'''
    
    @overload
    def get_formula1(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the value or expression associated with this validation.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The value or expression associated with this validation.'''
        ...
    
    @overload
    def get_formula1(self, is_r1c1 : bool, is_local : bool, row : int, column : int) -> str:
        '''Gets the value or expression associated with this validation for specific cell.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :param row: The row index.
        :param column: The column index.
        :returns: The value or expression associated with this validation.'''
        ...
    
    @overload
    def get_formula2(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the value or expression associated with this validation.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The value or expression associated with this validation.'''
        ...
    
    @overload
    def get_formula2(self, is_r1c1 : bool, is_local : bool, row : int, column : int) -> str:
        '''Gets the value or expression associated with this validation for specific cell.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :param row: The row index.
        :param column: The column index.
        :returns: The value or expression associated with this validation.'''
        ...
    
    @overload
    def add_area(self, cell_area : aspose.cells.CellArea):
        '''Applies the validation to the area.
        
        :param cell_area: The area.'''
        ...
    
    @overload
    def add_area(self, cell_area : aspose.cells.CellArea, check_intersection : bool, check_edge : bool):
        '''Applies the validation to the area.
        
        :param cell_area: The area.
        :param check_intersection: Whether check the intersection of given area with existing validations' areas.
        If one validation has been applied in given area(or part of it),
        then the existing validation should be removed at first from given area.
        Otherwise corruption may be caused for the generated Validations.
        If user is sure that the added area does not intersect with any existing area,
        this parameter can be set as false for performance consideration.
        :param check_edge: Whether check the edge of this validation's applied areas.
        Validation's internal settings depend on the top-left one of its applied ranges,
        so if given area will become the new top-left one of the applied ranges,
        the internal settings should be changed and rebuilt, otherwise unexpected result may be caused.
        If user is sure that the added area is not the top-left one,
        this parameter can be set as false for performance consideration.'''
        ...
    
    def set_formula1(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the value or expression associated with this validation.
        
        :param formula: The value or expression associated with this format condition.
        :param is_r1c1: Whether the formula is R1C1 formula.
        :param is_local: Whether the formula is locale formatted.'''
        ...
    
    def set_formula2(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the value or expression associated with this validation.
        
        :param formula: The value or expression associated with this format condition.
        :param is_r1c1: Whether the formula is R1C1 formula.
        :param is_local: Whether the formula is locale formatted.'''
        ...
    
    def get_list_value(self, row : int, column : int) -> any:
        '''Get the value for list of the validation for the specified cell.
        
        :param row: The row index.
        :param column: The column index.
        :returns: The value to produce the list of this validation for the specified cell.
        If the list references to a range, then the returned value will be a :py:class:`aspose.cells.ReferredArea` object;
        Otherwise the returned value may be null, object[], or simple object.'''
        ...
    
    def add_areas(self, areas : List[aspose.cells.CellArea], check_intersection : bool, check_edge : bool):
        '''Applies the validation to given areas.
        
        :param areas: The areas.
        :param check_intersection: Whether check the intersection of given area with existing validations' areas.
        If one validation has been applied in given area(or part of it),
        then the existing validation should be removed at first from given area.
        Otherwise corruption may be caused for the generated Validations.
        If user is sure that all the added areas do not intersect with any existing area,
        this parameter can be set as false for performance consideration.
        :param check_edge: Whether check the edge of this validation's applied areas.
        Validation's internal settings depend on the top-left one of its applied ranges,
        so if one of given areas will become the new top-left one of the applied ranges,
        the internal settings should be changed and rebuilt, otherwise unexpected result may be caused.
        If user is sure that no one of those added areas is the top-left,
        this parameter can be set as false for performance consideration.'''
        ...
    
    def remove_area(self, cell_area : aspose.cells.CellArea):
        '''Remove the validation settings in the range.
        
        :param cell_area: the areas where this validation settings should be removed.'''
        ...
    
    def remove_areas(self, areas : List[aspose.cells.CellArea]):
        '''Removes this validation from given areas.
        
        :param areas: the areas where this validation settings should be removed.'''
        ...
    
    def remove_a_cell(self, row : int, column : int):
        '''Remove the validation settings in the cell.
        
        :param row: The row index.
        :param column: The column index.'''
        ...
    
    def copy(self, source : aspose.cells.Validation, copy_option : aspose.cells.CopyOptions):
        '''Copy validation.
        
        :param source: The source validation.
        :param copy_option: The copy option.'''
        ...
    
    @property
    def operator(self) -> aspose.cells.OperatorType:
        '''Represents the operator for the data validation.'''
        ...
    
    @operator.setter
    def operator(self, value : aspose.cells.OperatorType):
        '''Represents the operator for the data validation.'''
        ...
    
    @property
    def alert_style(self) -> aspose.cells.ValidationAlertType:
        ...
    
    @alert_style.setter
    def alert_style(self, value : aspose.cells.ValidationAlertType):
        ...
    
    @property
    def type(self) -> aspose.cells.ValidationType:
        '''Represents the data validation type.'''
        ...
    
    @type.setter
    def type(self, value : aspose.cells.ValidationType):
        '''Represents the data validation type.'''
        ...
    
    @property
    def input_message(self) -> str:
        ...
    
    @input_message.setter
    def input_message(self, value : str):
        ...
    
    @property
    def input_title(self) -> str:
        ...
    
    @input_title.setter
    def input_title(self, value : str):
        ...
    
    @property
    def error_message(self) -> str:
        ...
    
    @error_message.setter
    def error_message(self, value : str):
        ...
    
    @property
    def error_title(self) -> str:
        ...
    
    @error_title.setter
    def error_title(self, value : str):
        ...
    
    @property
    def show_input(self) -> bool:
        ...
    
    @show_input.setter
    def show_input(self, value : bool):
        ...
    
    @property
    def show_error(self) -> bool:
        ...
    
    @show_error.setter
    def show_error(self, value : bool):
        ...
    
    @property
    def ignore_blank(self) -> bool:
        ...
    
    @ignore_blank.setter
    def ignore_blank(self, value : bool):
        ...
    
    @property
    def formula1(self) -> str:
        '''Represents the value or expression associated with the data validation.'''
        ...
    
    @formula1.setter
    def formula1(self, value : str):
        '''Represents the value or expression associated with the data validation.'''
        ...
    
    @property
    def formula2(self) -> str:
        '''Represents the value or expression associated with the data validation.'''
        ...
    
    @formula2.setter
    def formula2(self, value : str):
        '''Represents the value or expression associated with the data validation.'''
        ...
    
    @property
    def value1(self) -> any:
        '''Represents the first value associated with the data validation.'''
        ...
    
    @value1.setter
    def value1(self, value : any):
        '''Represents the first value associated with the data validation.'''
        ...
    
    @property
    def value2(self) -> any:
        '''Represents the second value associated with the data validation.'''
        ...
    
    @value2.setter
    def value2(self, value : any):
        '''Represents the second value associated with the data validation.'''
        ...
    
    @property
    def in_cell_drop_down(self) -> bool:
        ...
    
    @in_cell_drop_down.setter
    def in_cell_drop_down(self, value : bool):
        ...
    
    @property
    def areas(self) -> List[aspose.cells.CellArea]:
        '''Gets all :py:class:`aspose.cells.CellArea` which contain the data validation settings.'''
        ...
    
    ...

class ValidationCollection:
    '''Represents data validation collection.'''
    
    @overload
    def add(self) -> int:
        '''Adds a data validation to the collection.
        
        :returns: :py:class:`aspose.cells.Validation` object index.'''
        ...
    
    @overload
    def add(self, ca : aspose.cells.CellArea) -> int:
        '''Adds a data validation to the collection.
        
        :param ca: The area contains this validation.
        :returns: :py:class:`aspose.cells.Validation` object index.'''
        ...
    
    @overload
    def copy_to(self, array : List[aspose.cells.Validation]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.Validation], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.Validation, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.Validation, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Validation) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Validation, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Validation, index : int, count : int) -> int:
        ...
    
    def remove_a_cell(self, row : int, column : int):
        '''Removes all validation setting on the cell.
        
        :param row: The row index of the cell.
        :param column: The column index of the cell.'''
        ...
    
    def remove_area(self, ca : aspose.cells.CellArea):
        '''Removes all validation setting on the range..
        
        :param ca: The range which contains the validations setting.'''
        ...
    
    def get_validation_in_cell(self, row : int, column : int) -> aspose.cells.Validation:
        '''Gets the validation applied to given cell.
        
        :param row: The row index.
        :param column: The column index.
        :returns: Returns a :py:class:`aspose.cells.Validation` object or null if there is no validation for given cell'''
        ...
    
    def binary_search(self, item : aspose.cells.Validation) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class VerticalPageBreak:
    '''Encapsulates the object that represents a vertical page break.'''
    
    @property
    def start_row(self) -> int:
        ...
    
    @property
    def end_row(self) -> int:
        ...
    
    @property
    def column(self) -> int:
        '''Gets the column index of the vertical page break.'''
        ...
    
    ...

class VerticalPageBreakCollection:
    '''Encapsulates a collection of :py:class:`aspose.cells.VerticalPageBreak` objects.'''
    
    @overload
    def add(self, start_row : int, end_row : int, column : int) -> int:
        '''Adds a vertical page break to the collection.
        
        :param start_row: Start row index, zero based.
        :param end_row: End row index, zero based.
        :param column: Column index, zero based.
        :returns: :py:class:`aspose.cells.VerticalPageBreak` object index.'''
        ...
    
    @overload
    def add(self, column : int) -> int:
        '''Adds a vertical page break to the collection.
        
        :param column: Cell column index, zero based.
        :returns: :py:class:`aspose.cells.VerticalPageBreak` object index.'''
        ...
    
    @overload
    def add(self, row : int, column : int) -> int:
        '''Adds a vertical page break to the collection.
        
        :param row: Cell row index, zero based.
        :param column: Cell column index, zero based.
        :returns: :py:class:`aspose.cells.VerticalPageBreak` object index.'''
        ...
    
    @overload
    def add(self, cell_name : str) -> int:
        '''Adds a vertical page break to the collection.
        
        :param cell_name: Cell name.
        :returns: :py:class:`aspose.cells.VerticalPageBreak` object index.'''
        ...
    
    @overload
    def copy_to(self, array : List[aspose.cells.VerticalPageBreak]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.VerticalPageBreak], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.VerticalPageBreak, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.VerticalPageBreak, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.VerticalPageBreak) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.VerticalPageBreak, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.VerticalPageBreak, index : int, count : int) -> int:
        ...
    
    def binary_search(self, item : aspose.cells.VerticalPageBreak) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class WarningInfo:
    '''Warning info'''
    
    @property
    def warning_type(self) -> aspose.cells.WarningType:
        ...
    
    @property
    def description(self) -> str:
        '''Get description of warning info.'''
        ...
    
    @property
    def error_object(self) -> any:
        ...
    
    @property
    def corrected_object(self) -> any:
        ...
    
    @corrected_object.setter
    def corrected_object(self, value : any):
        ...
    
    ...

class Workbook:
    '''Represents a root object to create an Excel spreadsheet.'''
    
    @overload
    def save(self, file_name : str, save_format : aspose.cells.SaveFormat):
        '''Saves the workbook to the disk.
        
        :param file_name: The file name.
        :param save_format: The save format type.'''
        ...
    
    @overload
    def save(self, file_name : str):
        '''Save the workbook to the disk.'''
        ...
    
    @overload
    def save(self, file_name : str, save_options : aspose.cells.SaveOptions):
        '''Saves the workbook to the disk.
        
        :param file_name: The file name.
        :param save_options: The save options.'''
        ...
    
    @overload
    def save(self, stream : io.RawIOBase, save_format : aspose.cells.SaveFormat):
        '''Saves the workbook to the stream.
        
        :param stream: The file stream.
        :param save_format: The save file format type.'''
        ...
    
    @overload
    def save(self, stream : io.RawIOBase, save_options : aspose.cells.SaveOptions):
        '''Saves the workbook to the stream.
        
        :param stream: The file stream.
        :param save_options: The save options.'''
        ...
    
    @overload
    def replace(self, place_holder : str, new_value : str) -> int:
        '''Replaces a cell's value with a new string.
        
        :param place_holder: Cell placeholder
        :param new_value: String value to replace'''
        ...
    
    @overload
    def replace(self, place_holder : str, new_value : int) -> int:
        '''Replaces a cell's value with a new integer.
        
        :param place_holder: Cell placeholder
        :param new_value: Integer value to replace'''
        ...
    
    @overload
    def replace(self, place_holder : str, new_value : float) -> int:
        '''Replaces a cell's value with a new double.
        
        :param place_holder: Cell placeholder
        :param new_value: Double value to replace'''
        ...
    
    @overload
    def replace(self, place_holder : str, new_values : List[str], is_vertical : bool) -> int:
        '''Replaces a cell's value with a new string array.
        
        :param place_holder: Cell placeholder
        :param new_values: String array to replace
        :param is_vertical: True - Vertical, False - Horizontal'''
        ...
    
    @overload
    def replace(self, place_holder : str, new_values : List[int], is_vertical : bool) -> int:
        '''Replaces cells' values with an integer array.
        
        :param place_holder: Cell placeholder
        :param new_values: Integer array to replace
        :param is_vertical: True - Vertical, False - Horizontal'''
        ...
    
    @overload
    def replace(self, place_holder : str, new_values : List[float], is_vertical : bool) -> int:
        '''Replaces cells' values with a double array.
        
        :param place_holder: Cell placeholder
        :param new_values: Double array to replace
        :param is_vertical: True - Vertical, False - Horizontal'''
        ...
    
    @overload
    def replace(self, bool_value : bool, new_value : any) -> int:
        '''Replaces cells' values with new data.
        
        :param bool_value: The boolean value to be replaced.
        :param new_value: New value. Can be string, integer, double or DateTime value.'''
        ...
    
    @overload
    def replace(self, int_value : int, new_value : any) -> int:
        '''Replaces cells' values with new data.
        
        :param int_value: The integer value to be replaced.
        :param new_value: New value. Can be string, integer, double or DateTime value.'''
        ...
    
    @overload
    def replace(self, place_holder : str, new_value : str, options : aspose.cells.ReplaceOptions) -> int:
        '''Replaces a cell's value with a new string.
        
        :param place_holder: Cell placeholder
        :param new_value: String value to replace
        :param options: The replace options'''
        ...
    
    @overload
    def copy(self, source : aspose.cells.Workbook, copy_options : aspose.cells.CopyOptions):
        '''Copies data from a source Workbook object.
        
        :param source: Source Workbook object.'''
        ...
    
    @overload
    def copy(self, source : aspose.cells.Workbook):
        '''Copies data from a source Workbook object.
        
        :param source: Source Workbook object.'''
        ...
    
    @overload
    def calculate_formula(self):
        '''Calculates the result of formulas.'''
        ...
    
    @overload
    def calculate_formula(self, ignore_error : bool):
        '''Calculates the result of formulas.
        
        :param ignore_error: Indicates if hide the error in calculating formulas. The error may be unsupported function, external links, etc.'''
        ...
    
    @overload
    def calculate_formula(self, ignore_error : bool, custom_function : aspose.cells.ICustomFunction):
        '''Calculates the result of formulas.
        
        :param ignore_error: Indicates if hide the error in calculating formulas. The error may be unsupported function, external links, etc.
        :param custom_function: The custom formula calculation functions to extend the calculation engine.'''
        ...
    
    @overload
    def calculate_formula(self, options : aspose.cells.CalculationOptions):
        '''Calculating formulas in this workbook.
        
        :param options: Options for calculation'''
        ...
    
    @overload
    def refresh_dynamic_array_formulas(self, calculate : bool):
        '''Refreshes dynamic array formulas(spill into new range of neighboring cells according to current data)
        Other formulas in the workbook will not be calculated recursively even if they were used by dynamic array formulas.
        
        :param calculate: Whether calculates and updates cell values for those dynamic array formulas'''
        ...
    
    @overload
    def refresh_dynamic_array_formulas(self, calculate : bool, copts : aspose.cells.CalculationOptions):
        '''Refreshes dynamic array formulas(spill into new range of neighboring cells according to current data)
        
        :param calculate: Whether calculates and updates cell values for those dynamic array formulas
        :param copts: The options for calculating formulas'''
        ...
    
    @overload
    def import_xml(self, url : str, sheet_name : str, row : int, col : int):
        '''Imports/Updates an XML data file into the workbook.
        
        :param url: the url/path of the xml file.
        :param sheet_name: the destination sheet name.
        :param row: the destination row
        :param col: the destination column'''
        ...
    
    @overload
    def import_xml(self, stream : io.RawIOBase, sheet_name : str, row : int, col : int):
        '''Imports/Updates an XML data file into the workbook.
        
        :param stream: the xml file stream.
        :param sheet_name: the destination sheet name.
        :param row: the destination row.
        :param col: the destination column.'''
        ...
    
    @overload
    def export_xml(self, map_name : str, path : str):
        '''Export XML data linked by the specified XML map.
        
        :param map_name: name of the XML map that need to be exported
        :param path: the export path'''
        ...
    
    @overload
    def export_xml(self, map_name : str, stream : io.RawIOBase):
        '''Export XML data.
        
        :param map_name: name of the XML map that need to be exported
        :param stream: the export stream'''
        ...
    
    def parse_formulas(self, ignore_error : bool):
        '''Parses all formulas which have not been parsed when they were loaded from template file or set to a cell.
        
        :param ignore_error: whether ignore error for invalid formula.
        For one invalid formula, if ignore error then this formula will be ignored
        and the process will continue to parse other formulas, otherwise exception will be thrown.'''
        ...
    
    def start_access_cache(self, opts : aspose.cells.AccessCacheOptions):
        '''Starts the session that uses caches to access data.
        
        :param opts: options of data access'''
        ...
    
    def close_access_cache(self, opts : aspose.cells.AccessCacheOptions):
        '''Closes the session that uses caches to access data.
        
        :param opts: options of data access'''
        ...
    
    def remove_unused_styles(self):
        '''Remove all unused styles.'''
        ...
    
    def create_style(self) -> aspose.cells.Style:
        '''Creates a new style.
        
        :returns: Returns a style object.'''
        ...
    
    def create_builtin_style(self, type : aspose.cells.BuiltinStyleType) -> aspose.cells.Style:
        '''Creates built-in style by given type.
        
        :returns: style object'''
        ...
    
    def create_cells_color(self) -> aspose.cells.CellsColor:
        '''Creates a :py:class:`aspose.cells.CellsColor` object.
        
        :returns: Returns a :py:class:`aspose.cells.CellsColor` object.'''
        ...
    
    def combine(self, second_workbook : aspose.cells.Workbook):
        '''Combines another Workbook object.
        
        :param second_workbook: Another Workbook object.'''
        ...
    
    def get_style_in_pool(self, index : int) -> aspose.cells.Style:
        '''Gets the style in the style pool.
        All styles in the workbook will be gathered into a pool.
        There is only a simple reference index in the cells.
        
        :param index: The index.
        :returns: The style in the pool corresponds to given index, may be null.'''
        ...
    
    def get_fonts(self) -> List[aspose.cells.Font]:
        '''Gets all fonts in the style pool.'''
        ...
    
    def get_named_style(self, name : str) -> aspose.cells.Style:
        '''Gets the named style in the style pool.
        
        :param name: name of the style
        :returns: named style, maybe null.'''
        ...
    
    def change_palette(self, color : aspose.pydrawing.Color, index : int):
        '''Changes the palette for the spreadsheet in the specified index.
        
        :param color: Color structure.
        :param index: Palette index, 0 - 55.'''
        ...
    
    def is_color_in_palette(self, color : aspose.pydrawing.Color) -> bool:
        '''Checks if a color is in the palette for the spreadsheet.
        
        :param color: Color structure.
        :returns: Returns true if this color is in the palette. Otherwise, returns false'''
        ...
    
    def get_matching_color(self, raw_color : aspose.pydrawing.Color) -> aspose.pydrawing.Color:
        '''Find best matching Color in current palette.
        
        :param raw_color: Raw color.
        :returns: Best matching color.'''
        ...
    
    def set_encryption_options(self, encryption_type : aspose.cells.EncryptionType, key_length : int):
        '''Set Encryption Options.
        
        :param encryption_type: The encryption type.
        :param key_length: The key length.'''
        ...
    
    def protect(self, protection_type : aspose.cells.ProtectionType, password : str):
        '''Protects a workbook.
        
        :param protection_type: Protection type.
        :param password: Password to protect the workbook.'''
        ...
    
    def protect_shared_workbook(self, password : str):
        '''Protects a shared workbook.
        
        :param password: Password to protect the workbook.'''
        ...
    
    def unprotect(self, password : str):
        '''Unprotects a workbook.
        
        :param password: Password to unprotect the workbook.'''
        ...
    
    def unprotect_shared_workbook(self, password : str):
        '''Unprotects a shared workbook.
        
        :param password: Password to unprotect the workbook.'''
        ...
    
    def remove_macro(self):
        '''Removes VBA/macro from this spreadsheet.'''
        ...
    
    def remove_digital_signature(self):
        '''Removes digital signature from this spreadsheet.'''
        ...
    
    def accept_all_revisions(self):
        '''Accepts all tracked changes in the workbook.'''
        ...
    
    def remove_external_links(self):
        '''Removes all external links in the workbook.'''
        ...
    
    def get_theme_color(self, type : aspose.cells.ThemeColorType) -> aspose.pydrawing.Color:
        '''Gets theme color.
        
        :param type: The theme color type.
        :returns: The theme color.'''
        ...
    
    def set_theme_color(self, type : aspose.cells.ThemeColorType, color : aspose.pydrawing.Color):
        '''Sets the theme color
        
        :param type: The theme color type.
        :param color: the theme color'''
        ...
    
    def custom_theme(self, theme_name : str, colors : aspose.pydrawing.Color[]):
        '''Customs the theme.
        
        :param theme_name: The theme name
        :param colors: The theme colors'''
        ...
    
    def copy_theme(self, source : aspose.cells.Workbook):
        '''Copies the theme from another workbook.
        
        :param source: Source workbook.'''
        ...
    
    def has_exernal_links(self) -> bool:
        '''Indicates whether this workbook contains external links to other data sources.
        
        :returns: Whether this workbook contains external links to other data sources.'''
        ...
    
    def update_linked_data_source(self, external_workbooks : List[aspose.cells.Workbook]):
        '''If this workbook contains external links to other data source,
        Aspose.Cells will attempt to retrieve the latest data from give sources.
        
        :param external_workbooks: Workbooks that will be used to update data of external links referenced by this workbook.
        The match of those workbooks with external links is determined by :py:attr:`aspose.cells.Workbook.file_name`
        and :py:attr:`aspose.cells.ExternalLink.data_source`. So please make sure :py:attr:`aspose.cells.Workbook.file_name` has
        been specified with the proper value for every workbook so they can be linked to corresponding external link.'''
        ...
    
    def set_digital_signature(self, digital_signature_collection : aspose.cells.digitalsignatures.DigitalSignatureCollection):
        '''Sets digital signature to an spreadsheet file (Excel2007 and later).'''
        ...
    
    def add_digital_signature(self, digital_signature_collection : aspose.cells.digitalsignatures.DigitalSignatureCollection):
        '''Adds digital signature to an OOXML spreadsheet file (Excel2007 and later).'''
        ...
    
    def get_digital_signature(self) -> aspose.cells.digitalsignatures.DigitalSignatureCollection:
        '''Gets digital signature from file.'''
        ...
    
    def remove_personal_information(self):
        '''Removes personal information.'''
        ...
    
    @property
    def settings(self) -> aspose.cells.WorkbookSettings:
        '''Represents the workbook settings.'''
        ...
    
    @property
    def worksheets(self) -> aspose.cells.WorksheetCollection:
        '''Gets the :py:class:`aspose.cells.WorksheetCollection` collection in the spreadsheet.'''
        ...
    
    @property
    def is_licensed(self) -> bool:
        ...
    
    @property
    def colors(self) -> aspose.pydrawing.Color[]:
        '''Returns colors in the palette for the spreadsheet.'''
        ...
    
    @property
    def count_of_styles_in_pool(self) -> int:
        ...
    
    @property
    def default_style(self) -> aspose.cells.Style:
        ...
    
    @default_style.setter
    def default_style(self, value : aspose.cells.Style):
        ...
    
    @property
    def is_digitally_signed(self) -> bool:
        ...
    
    @property
    def is_workbook_protected_with_password(self) -> bool:
        ...
    
    @property
    def vba_project(self) -> aspose.cells.vba.VbaProject:
        ...
    
    @property
    def has_macro(self) -> bool:
        ...
    
    @property
    def has_revisions(self) -> bool:
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def cells_data_table_factory(self) -> aspose.cells.CellsDataTableFactory:
        ...
    
    @property
    def data_sorter(self) -> aspose.cells.DataSorter:
        ...
    
    @property
    def theme(self) -> str:
        '''Gets the theme name.'''
        ...
    
    @property
    def built_in_document_properties(self) -> aspose.cells.properties.BuiltInDocumentPropertyCollection:
        ...
    
    @property
    def custom_document_properties(self) -> aspose.cells.properties.CustomDocumentPropertyCollection:
        ...
    
    @property
    def file_format(self) -> aspose.cells.FileFormatType:
        ...
    
    @file_format.setter
    def file_format(self, value : aspose.cells.FileFormatType):
        ...
    
    @property
    def interrupt_monitor(self) -> aspose.cells.AbstractInterruptMonitor:
        ...
    
    @interrupt_monitor.setter
    def interrupt_monitor(self, value : aspose.cells.AbstractInterruptMonitor):
        ...
    
    @property
    def content_type_properties(self) -> aspose.cells.properties.ContentTypePropertyCollection:
        ...
    
    @property
    def custom_xml_parts(self) -> aspose.cells.markup.CustomXmlPartCollection:
        ...
    
    @property
    def data_mashup(self) -> aspose.cells.querytables.DataMashup:
        ...
    
    @property
    def ribbon_xml(self) -> str:
        ...
    
    @ribbon_xml.setter
    def ribbon_xml(self, value : str):
        ...
    
    @property
    def absolute_path(self) -> str:
        ...
    
    @absolute_path.setter
    def absolute_path(self, value : str):
        ...
    
    @property
    def data_connections(self) -> aspose.cells.externalconnections.ExternalConnectionCollection:
        ...
    
    ...

class WorkbookDesigner:
    '''Encapsulates the object that represents a designer spreadsheet.'''
    
    @overload
    def set_data_source(self, data_source : str, cells_data_table : aspose.cells.ICellsDataTable):
        '''Sets data source of a :py:class:`aspose.cells.ICellsDataTable` object.
        
        :param data_source: The name of the data source.
        :param cells_data_table: data table.'''
        ...
    
    @overload
    def set_data_source(self, variable : str, data : any):
        '''Sets data binding to a variable.
        
        :param variable: Variable name created using smart marker.
        :param data: Source data.'''
        ...
    
    @overload
    def process(self):
        '''Processes the smart markers and populates the data source values.'''
        ...
    
    @overload
    def process(self, is_preserved : bool):
        '''Processes the smart markers and populates the data source values.
        
        :param is_preserved: True if the unrecognized smart marker is preserved.'''
        ...
    
    @overload
    def process(self, sheet_index : int, is_preserved : bool):
        '''Processes the smart markers and populates the data source values.
        
        :param sheet_index: Worksheet index.
        :param is_preserved: True if the unrecognized smart marker is preserved.'''
        ...
    
    def clear_data_source(self):
        '''Clears all data sources.'''
        ...
    
    def get_smart_markers(self) -> List[str]:
        '''Returns a collection of smart markers in a spreadsheet.
        
        :returns: A collection of smart markers'''
        ...
    
    @property
    def workbook(self) -> aspose.cells.Workbook:
        '''Gets and sets the :py:attr:`aspose.cells.WorkbookDesigner.workbook` object.'''
        ...
    
    @workbook.setter
    def workbook(self, value : aspose.cells.Workbook):
        '''Gets and sets the :py:attr:`aspose.cells.WorkbookDesigner.workbook` object.'''
        ...
    
    @property
    def repeat_formulas_with_subtotal(self) -> bool:
        ...
    
    @repeat_formulas_with_subtotal.setter
    def repeat_formulas_with_subtotal(self, value : bool):
        ...
    
    @property
    def update_empty_string_as_null(self) -> bool:
        ...
    
    @update_empty_string_as_null.setter
    def update_empty_string_as_null(self, value : bool):
        ...
    
    @property
    def update_reference(self) -> bool:
        ...
    
    @update_reference.setter
    def update_reference(self, value : bool):
        ...
    
    @property
    def calculate_formula(self) -> bool:
        ...
    
    @calculate_formula.setter
    def calculate_formula(self, value : bool):
        ...
    
    @property
    def call_back(self) -> aspose.cells.ISmartMarkerCallBack:
        ...
    
    @call_back.setter
    def call_back(self, value : aspose.cells.ISmartMarkerCallBack):
        ...
    
    @property
    def line_by_line(self) -> bool:
        ...
    
    @line_by_line.setter
    def line_by_line(self, value : bool):
        ...
    
    ...

class WorkbookSettings:
    '''Represents all settings of the workbook.'''
    
    def get_theme_font(self, type : aspose.cells.FontSchemeType) -> str:
        '''Gets the default theme font name.
        
        :param type: The scheme type of the font.'''
        ...
    
    def set_page_orientation_type(self, page_orientation_type : aspose.cells.PageOrientationType):
        '''Set the type of  print orientation for the whole workbook.
        
        :param page_orientation_type: The :py:class:`aspose.cells.PageOrientationType`'''
        ...
    
    @property
    def stream_provider(self) -> aspose.cells.IStreamProvider:
        ...
    
    @stream_provider.setter
    def stream_provider(self, value : aspose.cells.IStreamProvider):
        ...
    
    @property
    def resource_provider(self) -> aspose.cells.IStreamProvider:
        ...
    
    @resource_provider.setter
    def resource_provider(self, value : aspose.cells.IStreamProvider):
        ...
    
    @property
    def author(self) -> str:
        '''Gets and sets the author of the file.'''
        ...
    
    @author.setter
    def author(self, value : str):
        '''Gets and sets the author of the file.'''
        ...
    
    @property
    def check_custom_number_format(self) -> bool:
        ...
    
    @check_custom_number_format.setter
    def check_custom_number_format(self, value : bool):
        ...
    
    @property
    def enable_macros(self) -> bool:
        ...
    
    @enable_macros.setter
    def enable_macros(self, value : bool):
        ...
    
    @property
    def date1904(self) -> bool:
        '''Gets a value which represents if the workbook uses the 1904 date system.'''
        ...
    
    @date1904.setter
    def date1904(self, value : bool):
        '''Sets a value which represents if the workbook uses the 1904 date system.'''
        ...
    
    @property
    def protection_type(self) -> aspose.cells.ProtectionType:
        ...
    
    @property
    def display_drawing_objects(self) -> aspose.cells.DisplayDrawingObjects:
        ...
    
    @display_drawing_objects.setter
    def display_drawing_objects(self, value : aspose.cells.DisplayDrawingObjects):
        ...
    
    @property
    def sheet_tab_bar_width(self) -> int:
        ...
    
    @sheet_tab_bar_width.setter
    def sheet_tab_bar_width(self, value : int):
        ...
    
    @property
    def show_tabs(self) -> bool:
        ...
    
    @show_tabs.setter
    def show_tabs(self, value : bool):
        ...
    
    @property
    def first_visible_tab(self) -> int:
        ...
    
    @first_visible_tab.setter
    def first_visible_tab(self, value : int):
        ...
    
    @property
    def is_h_scroll_bar_visible(self) -> bool:
        ...
    
    @is_h_scroll_bar_visible.setter
    def is_h_scroll_bar_visible(self, value : bool):
        ...
    
    @property
    def is_v_scroll_bar_visible(self) -> bool:
        ...
    
    @is_v_scroll_bar_visible.setter
    def is_v_scroll_bar_visible(self, value : bool):
        ...
    
    @property
    def shared(self) -> bool:
        '''Gets a value that indicates whether the Workbook is shared.'''
        ...
    
    @shared.setter
    def shared(self, value : bool):
        '''Sets a value that indicates whether the Workbook is shared.'''
        ...
    
    @property
    def language_code(self) -> aspose.cells.CountryCode:
        ...
    
    @language_code.setter
    def language_code(self, value : aspose.cells.CountryCode):
        ...
    
    @property
    def region(self) -> aspose.cells.CountryCode:
        '''Gets the regional settings for workbook.'''
        ...
    
    @region.setter
    def region(self, value : aspose.cells.CountryCode):
        '''Sets the regional settings for workbook.'''
        ...
    
    @property
    def globalization_settings(self) -> aspose.cells.GlobalizationSettings:
        ...
    
    @globalization_settings.setter
    def globalization_settings(self, value : aspose.cells.GlobalizationSettings):
        ...
    
    @property
    def number_decimal_separator(self) -> char:
        ...
    
    @number_decimal_separator.setter
    def number_decimal_separator(self, value : char):
        ...
    
    @property
    def number_group_separator(self) -> char:
        ...
    
    @number_group_separator.setter
    def number_group_separator(self, value : char):
        ...
    
    @property
    def password(self) -> str:
        '''Represents Workbook file encryption password.'''
        ...
    
    @password.setter
    def password(self, value : str):
        '''Represents Workbook file encryption password.'''
        ...
    
    @property
    def write_protection(self) -> aspose.cells.WriteProtection:
        ...
    
    @property
    def is_encrypted(self) -> bool:
        ...
    
    @property
    def is_protected(self) -> bool:
        ...
    
    @property
    def is_default_encrypted(self) -> bool:
        ...
    
    @is_default_encrypted.setter
    def is_default_encrypted(self, value : bool):
        ...
    
    @property
    def is_minimized(self) -> bool:
        ...
    
    @is_minimized.setter
    def is_minimized(self, value : bool):
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def auto_compress_pictures(self) -> bool:
        ...
    
    @auto_compress_pictures.setter
    def auto_compress_pictures(self, value : bool):
        ...
    
    @property
    def remove_personal_information(self) -> bool:
        ...
    
    @remove_personal_information.setter
    def remove_personal_information(self, value : bool):
        ...
    
    @property
    def hide_pivot_field_list(self) -> bool:
        ...
    
    @hide_pivot_field_list.setter
    def hide_pivot_field_list(self, value : bool):
        ...
    
    @property
    def update_links_type(self) -> aspose.cells.UpdateLinksType:
        ...
    
    @update_links_type.setter
    def update_links_type(self, value : aspose.cells.UpdateLinksType):
        ...
    
    @property
    def max_row(self) -> int:
        ...
    
    @property
    def max_column(self) -> int:
        ...
    
    @property
    def parsing_formula_on_open(self) -> bool:
        ...
    
    @parsing_formula_on_open.setter
    def parsing_formula_on_open(self, value : bool):
        ...
    
    @property
    def window_left(self) -> float:
        ...
    
    @window_left.setter
    def window_left(self, value : float):
        ...
    
    @property
    def window_left_inch(self) -> float:
        ...
    
    @window_left_inch.setter
    def window_left_inch(self, value : float):
        ...
    
    @property
    def window_left_cm(self) -> float:
        ...
    
    @window_left_cm.setter
    def window_left_cm(self, value : float):
        ...
    
    @property
    def window_top(self) -> float:
        ...
    
    @window_top.setter
    def window_top(self, value : float):
        ...
    
    @property
    def window_top_inch(self) -> float:
        ...
    
    @window_top_inch.setter
    def window_top_inch(self, value : float):
        ...
    
    @property
    def window_top_cm(self) -> float:
        ...
    
    @window_top_cm.setter
    def window_top_cm(self, value : float):
        ...
    
    @property
    def window_width(self) -> float:
        ...
    
    @window_width.setter
    def window_width(self, value : float):
        ...
    
    @property
    def window_width_inch(self) -> float:
        ...
    
    @window_width_inch.setter
    def window_width_inch(self, value : float):
        ...
    
    @property
    def window_width_cm(self) -> float:
        ...
    
    @window_width_cm.setter
    def window_width_cm(self, value : float):
        ...
    
    @property
    def window_height(self) -> float:
        ...
    
    @window_height.setter
    def window_height(self, value : float):
        ...
    
    @property
    def window_height_inch(self) -> float:
        ...
    
    @window_height_inch.setter
    def window_height_inch(self, value : float):
        ...
    
    @property
    def window_height_cm(self) -> float:
        ...
    
    @window_height_cm.setter
    def window_height_cm(self, value : float):
        ...
    
    @property
    def update_adjacent_cells_border(self) -> bool:
        ...
    
    @update_adjacent_cells_border.setter
    def update_adjacent_cells_border(self, value : bool):
        ...
    
    @property
    def significant_digits(self) -> int:
        ...
    
    @significant_digits.setter
    def significant_digits(self, value : int):
        ...
    
    @property
    def check_compatibility(self) -> bool:
        ...
    
    @check_compatibility.setter
    def check_compatibility(self, value : bool):
        ...
    
    @property
    def check_excel_restriction(self) -> bool:
        ...
    
    @check_excel_restriction.setter
    def check_excel_restriction(self, value : bool):
        ...
    
    @property
    def auto_recover(self) -> bool:
        ...
    
    @auto_recover.setter
    def auto_recover(self, value : bool):
        ...
    
    @property
    def crash_save(self) -> bool:
        ...
    
    @crash_save.setter
    def crash_save(self, value : bool):
        ...
    
    @property
    def data_extract_load(self) -> bool:
        ...
    
    @data_extract_load.setter
    def data_extract_load(self, value : bool):
        ...
    
    @property
    def repair_load(self) -> bool:
        ...
    
    @repair_load.setter
    def repair_load(self, value : bool):
        ...
    
    @property
    def build_version(self) -> str:
        ...
    
    @build_version.setter
    def build_version(self, value : str):
        ...
    
    @property
    def memory_setting(self) -> aspose.cells.MemorySetting:
        ...
    
    @memory_setting.setter
    def memory_setting(self, value : aspose.cells.MemorySetting):
        ...
    
    @property
    def paper_size(self) -> aspose.cells.PaperSizeType:
        ...
    
    @paper_size.setter
    def paper_size(self, value : aspose.cells.PaperSizeType):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def max_rows_of_shared_formula(self) -> int:
        ...
    
    @max_rows_of_shared_formula.setter
    def max_rows_of_shared_formula(self, value : int):
        ...
    
    @property
    def compliance(self) -> aspose.cells.OoxmlCompliance:
        '''Specifies the OOXML version for the output document. The default value is Ecma376_2006.'''
        ...
    
    @compliance.setter
    def compliance(self, value : aspose.cells.OoxmlCompliance):
        '''Specifies the OOXML version for the output document. The default value is Ecma376_2006.'''
        ...
    
    @property
    def quote_prefix_to_style(self) -> bool:
        ...
    
    @quote_prefix_to_style.setter
    def quote_prefix_to_style(self, value : bool):
        ...
    
    @property
    def formula_settings(self) -> aspose.cells.FormulaSettings:
        ...
    
    @property
    def precision_as_displayed(self) -> bool:
        ...
    
    @precision_as_displayed.setter
    def precision_as_displayed(self, value : bool):
        ...
    
    @property
    def re_calculate_on_open(self) -> bool:
        ...
    
    @re_calculate_on_open.setter
    def re_calculate_on_open(self, value : bool):
        ...
    
    @property
    def create_calc_chain(self) -> bool:
        ...
    
    @create_calc_chain.setter
    def create_calc_chain(self, value : bool):
        ...
    
    @property
    def force_full_calculate(self) -> bool:
        ...
    
    @force_full_calculate.setter
    def force_full_calculate(self, value : bool):
        ...
    
    @property
    def iteration(self) -> bool:
        '''Indicates whether enable iterative calculation to resolve circular references.'''
        ...
    
    @iteration.setter
    def iteration(self, value : bool):
        '''Indicates whether enable iterative calculation to resolve circular references.'''
        ...
    
    @property
    def max_iteration(self) -> int:
        ...
    
    @max_iteration.setter
    def max_iteration(self, value : int):
        ...
    
    @property
    def max_change(self) -> float:
        ...
    
    @max_change.setter
    def max_change(self, value : float):
        ...
    
    @property
    def calc_mode(self) -> aspose.cells.CalcModeType:
        ...
    
    @calc_mode.setter
    def calc_mode(self, value : aspose.cells.CalcModeType):
        ...
    
    @property
    def calculation_id(self) -> str:
        ...
    
    @calculation_id.setter
    def calculation_id(self, value : str):
        ...
    
    @property
    def calc_stack_size(self) -> int:
        ...
    
    @calc_stack_size.setter
    def calc_stack_size(self, value : int):
        ...
    
    @property
    def recalculate_before_save(self) -> bool:
        ...
    
    @recalculate_before_save.setter
    def recalculate_before_save(self, value : bool):
        ...
    
    ...

class Worksheet:
    '''Encapsulates the object that represents a single worksheet.'''
    
    @overload
    def freeze_panes(self, row : int, column : int, freezed_rows : int, freezed_columns : int):
        '''Freezes panes at the specified cell in the worksheet.
        
        :param row: Row index.
        :param column: Column index.
        :param freezed_rows: Number of visible rows in top pane, no more than row index.
        :param freezed_columns: Number of visible columns in left pane, no more than column index.'''
        ...
    
    @overload
    def freeze_panes(self, cell_name : str, freezed_rows : int, freezed_columns : int):
        '''Freezes panes at the specified cell in the worksheet.
        
        :param cell_name: Cell name.
        :param freezed_rows: Number of visible rows in top pane, no more than row index.
        :param freezed_columns: Number of visible columns in left pane, no more than column index.'''
        ...
    
    @overload
    def copy(self, source_sheet : aspose.cells.Worksheet):
        '''Copies contents and formats from another worksheet.
        
        :param source_sheet: Source worksheet.'''
        ...
    
    @overload
    def copy(self, source_sheet : aspose.cells.Worksheet, copy_options : aspose.cells.CopyOptions):
        '''Copies contents and formats from another worksheet.
        
        :param source_sheet: Source worksheet.'''
        ...
    
    @overload
    def auto_fit_column(self, column_index : int, first_row : int, last_row : int):
        '''Autofits the column width.
        
        :param column_index: Column index.
        :param first_row: First row index.
        :param last_row: Last row index.'''
        ...
    
    @overload
    def auto_fit_column(self, column_index : int):
        '''Autofits the column width.
        
        :param column_index: Column index.'''
        ...
    
    @overload
    def auto_fit_columns(self):
        '''Autofits all columns in this worksheet.'''
        ...
    
    @overload
    def auto_fit_columns(self, options : aspose.cells.AutoFitterOptions):
        '''Autofits all columns in this worksheet.
        
        :param options: The auto fitting options'''
        ...
    
    @overload
    def auto_fit_columns(self, first_column : int, last_column : int):
        '''Autofits the columns width.
        
        :param first_column: First column index.
        :param last_column: Last column index.'''
        ...
    
    @overload
    def auto_fit_columns(self, first_column : int, last_column : int, options : aspose.cells.AutoFitterOptions):
        '''Autofits the columns width.
        
        :param first_column: First column index.
        :param last_column: Last column index.
        :param options: The auto fitting options'''
        ...
    
    @overload
    def auto_fit_columns(self, first_row : int, first_column : int, last_row : int, last_column : int):
        '''Autofits the columns width.
        
        :param first_row: First row index.
        :param first_column: First column index.
        :param last_row: Last row index.
        :param last_column: Last column index.'''
        ...
    
    @overload
    def auto_fit_columns(self, first_row : int, first_column : int, last_row : int, last_column : int, options : aspose.cells.AutoFitterOptions):
        '''Autofits the columns width.
        
        :param first_row: First row index.
        :param first_column: First column index.
        :param last_row: Last row index.
        :param last_column: Last column index.
        :param options: The auto fitting options'''
        ...
    
    @overload
    def auto_fit_row(self, row_index : int, first_column : int, last_column : int):
        '''Autofits the row height.
        
        :param row_index: Row index.
        :param first_column: First column index.
        :param last_column: Last column index.'''
        ...
    
    @overload
    def auto_fit_row(self, row_index : int, first_column : int, last_column : int, options : aspose.cells.AutoFitterOptions):
        '''Autofits the row height.
        
        :param row_index: Row index.
        :param first_column: First column index.
        :param last_column: Last column index.
        :param options: The auto fitter options'''
        ...
    
    @overload
    def auto_fit_row(self, start_row : int, end_row : int, start_column : int, end_column : int):
        '''Autofits row height in a rectangle range.
        
        :param start_row: Start row index.
        :param end_row: End row index.
        :param start_column: Start column index.
        :param end_column: End column index.'''
        ...
    
    @overload
    def auto_fit_row(self, row_index : int):
        '''Autofits the row height.
        
        :param row_index: Row index.'''
        ...
    
    @overload
    def auto_fit_rows(self):
        '''Autofits all rows in this worksheet.'''
        ...
    
    @overload
    def auto_fit_rows(self, only_auto : bool):
        '''Autofits all rows in this worksheet.
        
        :param only_auto: True,only autofits the row height when row height is not customed.'''
        ...
    
    @overload
    def auto_fit_rows(self, options : aspose.cells.AutoFitterOptions):
        '''Autofits all rows in this worksheet.
        
        :param options: The auto fitter options'''
        ...
    
    @overload
    def auto_fit_rows(self, start_row : int, end_row : int):
        '''Autofits row height in a range.
        
        :param start_row: Start row index.
        :param end_row: End row index.'''
        ...
    
    @overload
    def auto_fit_rows(self, start_row : int, end_row : int, options : aspose.cells.AutoFitterOptions):
        '''Autofits row height in a range.
        
        :param start_row: Start row index.
        :param end_row: End row index.
        :param options: The options of auto fitter.'''
        ...
    
    @overload
    def protect(self, type : aspose.cells.ProtectionType):
        '''Protects worksheet.
        
        :param type: Protection type.'''
        ...
    
    @overload
    def protect(self, type : aspose.cells.ProtectionType, password : str, old_password : str):
        '''Protects worksheet.
        
        :param type: Protection type.
        :param password: Password.
        :param old_password: If the worksheet is already protected by a password, please supply the old password.
        Otherwise, you can set a null value or blank string to this parameter.'''
        ...
    
    @overload
    def unprotect(self):
        '''Unprotects worksheet.'''
        ...
    
    @overload
    def unprotect(self, password : str):
        '''Unprotects worksheet.
        
        :param password: Password'''
        ...
    
    @overload
    def calculate_formula(self, formula : str) -> any:
        '''Calculates a formula.
        
        :param formula: Formula to be calculated.
        :returns: Calculated formula result.'''
        ...
    
    @overload
    def calculate_formula(self, formula : str, opts : aspose.cells.CalculationOptions) -> any:
        '''Calculates a formula.
        
        :param formula: Formula to be calculated.
        :param opts: Options for calculating formula
        :returns: Calculated formula result.'''
        ...
    
    @overload
    def calculate_formula(self, recursive : bool, ignore_error : bool, custom_function : aspose.cells.ICustomFunction):
        '''Calculates all formulas in this worksheet.
        
        :param recursive: True means if the worksheet' cells depend on the cells of other worksheets,
        the dependent cells in other worksheets will be calculated too.
        False means all the formulas in the worksheet have been calculated and the values are right.
        :param ignore_error: Indicates if hide the error in calculating formulas.
        The error may be unsupported function, external links, etc.
        :param custom_function: The custom formula calculation functions to extend the calculation engine.'''
        ...
    
    @overload
    def calculate_formula(self, options : aspose.cells.CalculationOptions, recursive : bool):
        '''Calculates all formulas in this worksheet.
        
        :param options: Options for calculation
        :param recursive: True means if the worksheet' cells depend on the cells of other worksheets,
        the dependent cells in other worksheets will be calculated too.
        False means all the formulas in the worksheet have been calculated and the values are right.'''
        ...
    
    def get_panes(self) -> aspose.cells.PaneCollection:
        '''Gets the window panes.'''
        ...
    
    def get_freezed_panes(self, row : Any, column : Any, freezed_rows : Any, freezed_columns : Any) -> bool:
        '''Gets the freeze panes.
        
        :param row: Row index.
        :param column: Column index.
        :param freezed_rows: Number of visible rows in top pane, no more than row index.
        :param freezed_columns: Number of visible columns in left pane, no more than column index.
        :returns: Return whether the worksheet is frozen'''
        ...
    
    def split(self):
        '''Splits window.'''
        ...
    
    def un_freeze_panes(self):
        '''Unfreezes panes in the worksheet.'''
        ...
    
    def remove_split(self):
        '''Removes split window.'''
        ...
    
    def add_page_breaks(self, cell_name : str):
        '''Adds page break.'''
        ...
    
    def advanced_filter(self, is_filter : bool, list_range : str, criteria_range : str, copy_to : str, unique_record_only : bool):
        '''Filters data using complex criteria.
        
        :param is_filter: Indicates whether filtering the list in place.
        :param list_range: The list range.
        :param criteria_range: The criteria range.
        :param copy_to: The range where copying data to.
        :param unique_record_only: Only displaying or copying unique rows.'''
        ...
    
    def remove_auto_filter(self):
        '''Removes the auto filter of the worksheet.'''
        ...
    
    def set_visible(self, is_visible : bool, ignore_error : bool):
        '''Sets the visible options.
        
        :param is_visible: Whether the worksheet is visible
        :param ignore_error: Whether to ignore error if this option is not valid.'''
        ...
    
    def select_range(self, start_row : int, start_column : int, total_rows : int, total_columns : int, remove_others : bool):
        '''Selects a range.
        
        :param start_row: The start row.
        :param start_column: The start column
        :param total_rows: The number of rows.
        :param total_columns: The number of columns
        :param remove_others: True means removing other selected range and only select this range.'''
        ...
    
    def remove_all_drawing_objects(self):
        '''Removes all drawing objects in this worksheet.'''
        ...
    
    def clear_comments(self):
        '''Clears all comments in designer spreadsheet.'''
        ...
    
    def move_to(self, index : int):
        '''Moves the sheet to another location in the spreadsheet.
        
        :param index: Destination sheet index.'''
        ...
    
    def replace(self, old_string : str, new_string : str) -> int:
        '''Replaces all cells' text with a new string.
        
        :param old_string: Old string value.
        :param new_string: New string value.'''
        ...
    
    def get_selected_ranges(self) -> list:
        '''Gets selected ranges of cells in the designer spreadsheet.
        
        :returns: An :py:class:`list` which contains selected ranges.'''
        ...
    
    def set_background(self, picture_data : bytes):
        '''Sets worksheet background image.
        
        :param picture_data: Picture data.'''
        ...
    
    def get_printing_page_breaks(self, options : aspose.cells.rendering.ImageOrPrintOptions) -> List[aspose.cells.CellArea]:
        '''Gets automatic page breaks.
        
        :param options: The print options
        :returns: The automatic page breaks areas.'''
        ...
    
    def start_access_cache(self, opts : aspose.cells.AccessCacheOptions):
        '''Starts the session that uses caches to access the data in this worksheet.
        
        :param opts: options of data access'''
        ...
    
    def close_access_cache(self, opts : aspose.cells.AccessCacheOptions):
        '''Closes the session that uses caches to access the data in this worksheet.
        
        :param opts: options of data access'''
        ...
    
    def xml_map_query(self, path : str, xml_map : aspose.cells.XmlMap) -> list:
        '''Query cell areas that mapped/linked to the specific path of xml map.
        
        :param path: xml element path
        :param xml_map: Specify an xml map if you want to query for the specific path within a specific map
        :returns: :py:class:`aspose.cells.CellArea` list that mapped/linked to the specific path of xml map, an empty list is returned if nothing is mapped/linked.'''
        ...
    
    def refresh_pivot_tables(self):
        '''Refreshes all the PivotTables in this Worksheet.'''
        ...
    
    @property
    def protection(self) -> aspose.cells.Protection:
        '''Represents the various types of protection options available for a worksheet. Supports advanced protection options in ExcelXP and above version.'''
        ...
    
    @property
    def unique_id(self) -> str:
        ...
    
    @unique_id.setter
    def unique_id(self, value : str):
        ...
    
    @property
    def workbook(self) -> aspose.cells.Workbook:
        '''Gets the workbook object which contains this sheet.'''
        ...
    
    @property
    def cells(self) -> aspose.cells.Cells:
        '''Gets the :py:attr:`aspose.cells.Worksheet.cells` collection.'''
        ...
    
    @property
    def query_tables(self) -> aspose.cells.QueryTableCollection:
        ...
    
    @property
    def pivot_tables(self) -> aspose.cells.pivot.PivotTableCollection:
        ...
    
    @property
    def type(self) -> aspose.cells.SheetType:
        '''Represents worksheet type.'''
        ...
    
    @type.setter
    def type(self, value : aspose.cells.SheetType):
        '''Represents worksheet type.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name of the worksheet.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name of the worksheet.'''
        ...
    
    @property
    def show_formulas(self) -> bool:
        ...
    
    @show_formulas.setter
    def show_formulas(self, value : bool):
        ...
    
    @property
    def is_gridlines_visible(self) -> bool:
        ...
    
    @is_gridlines_visible.setter
    def is_gridlines_visible(self, value : bool):
        ...
    
    @property
    def is_row_column_headers_visible(self) -> bool:
        ...
    
    @is_row_column_headers_visible.setter
    def is_row_column_headers_visible(self, value : bool):
        ...
    
    @property
    def pane_state(self) -> aspose.cells.PaneStateType:
        ...
    
    @property
    def display_zeros(self) -> bool:
        ...
    
    @display_zeros.setter
    def display_zeros(self, value : bool):
        ...
    
    @property
    def display_right_to_left(self) -> bool:
        ...
    
    @display_right_to_left.setter
    def display_right_to_left(self, value : bool):
        ...
    
    @property
    def is_outline_shown(self) -> bool:
        ...
    
    @is_outline_shown.setter
    def is_outline_shown(self, value : bool):
        ...
    
    @property
    def is_selected(self) -> bool:
        ...
    
    @is_selected.setter
    def is_selected(self, value : bool):
        ...
    
    @property
    def list_objects(self) -> aspose.cells.tables.ListObjectCollection:
        ...
    
    @property
    def tab_id(self) -> int:
        ...
    
    @tab_id.setter
    def tab_id(self, value : int):
        ...
    
    @property
    def horizontal_page_breaks(self) -> aspose.cells.HorizontalPageBreakCollection:
        ...
    
    @property
    def vertical_page_breaks(self) -> aspose.cells.VerticalPageBreakCollection:
        ...
    
    @property
    def hyperlinks(self) -> aspose.cells.HyperlinkCollection:
        '''Gets the :py:class:`aspose.cells.HyperlinkCollection` collection.'''
        ...
    
    @property
    def page_setup(self) -> aspose.cells.PageSetup:
        ...
    
    @property
    def auto_filter(self) -> aspose.cells.AutoFilter:
        ...
    
    @property
    def has_autofilter(self) -> bool:
        ...
    
    @property
    def transition_evaluation(self) -> bool:
        ...
    
    @transition_evaluation.setter
    def transition_evaluation(self, value : bool):
        ...
    
    @property
    def transition_entry(self) -> bool:
        ...
    
    @transition_entry.setter
    def transition_entry(self, value : bool):
        ...
    
    @property
    def visibility_type(self) -> aspose.cells.VisibilityType:
        ...
    
    @visibility_type.setter
    def visibility_type(self, value : aspose.cells.VisibilityType):
        ...
    
    @property
    def is_visible(self) -> bool:
        ...
    
    @is_visible.setter
    def is_visible(self, value : bool):
        ...
    
    @property
    def sparkline_group_collection(self) -> aspose.cells.charts.SparklineGroupCollection:
        ...
    
    @property
    def sparkline_groups(self) -> aspose.cells.charts.SparklineGroupCollection:
        ...
    
    @property
    def charts(self) -> aspose.cells.charts.ChartCollection:
        '''Gets a :py:class:`aspose.cells.charts.Chart` collection'''
        ...
    
    @property
    def comments(self) -> aspose.cells.CommentCollection:
        '''Gets the :py:class:`aspose.cells.Comment` collection.'''
        ...
    
    @property
    def pictures(self) -> aspose.cells.drawing.PictureCollection:
        '''Gets a :py:class:`aspose.cells.drawing.Picture` collection.'''
        ...
    
    @property
    def text_boxes(self) -> aspose.cells.drawing.TextBoxCollection:
        ...
    
    @property
    def check_boxes(self) -> aspose.cells.drawing.CheckBoxCollection:
        ...
    
    @property
    def ole_objects(self) -> aspose.cells.drawing.OleObjectCollection:
        ...
    
    @property
    def shapes(self) -> aspose.cells.drawing.ShapeCollection:
        '''Returns all drawing shapes in this worksheet.'''
        ...
    
    @property
    def slicers(self) -> aspose.cells.slicers.SlicerCollection:
        '''Get the Slicer collection in the worksheet'''
        ...
    
    @property
    def timelines(self) -> aspose.cells.timelines.TimelineCollection:
        '''Get the Timeline collection in the worksheet'''
        ...
    
    @property
    def index(self) -> int:
        '''Gets the index of sheet in the worksheet collection.'''
        ...
    
    @property
    def is_protected(self) -> bool:
        ...
    
    @property
    def validations(self) -> aspose.cells.ValidationCollection:
        '''Gets the data validation setting collection in the worksheet.'''
        ...
    
    @property
    def allow_edit_ranges(self) -> aspose.cells.ProtectedRangeCollection:
        ...
    
    @property
    def error_check_options(self) -> aspose.cells.ErrorCheckOptionCollection:
        ...
    
    @property
    def outline(self) -> aspose.cells.Outline:
        '''Gets the outline on this worksheet.'''
        ...
    
    @property
    def first_visible_row(self) -> int:
        ...
    
    @first_visible_row.setter
    def first_visible_row(self, value : int):
        ...
    
    @property
    def first_visible_column(self) -> int:
        ...
    
    @first_visible_column.setter
    def first_visible_column(self, value : int):
        ...
    
    @property
    def zoom(self) -> int:
        '''Represents the scaling factor in percentage. It should be between 10 and 400.'''
        ...
    
    @zoom.setter
    def zoom(self, value : int):
        '''Represents the scaling factor in percentage. It should be between 10 and 400.'''
        ...
    
    @property
    def view_type(self) -> aspose.cells.ViewType:
        ...
    
    @view_type.setter
    def view_type(self, value : aspose.cells.ViewType):
        ...
    
    @property
    def is_page_break_preview(self) -> bool:
        ...
    
    @is_page_break_preview.setter
    def is_page_break_preview(self, value : bool):
        ...
    
    @property
    def is_ruler_visible(self) -> bool:
        ...
    
    @is_ruler_visible.setter
    def is_ruler_visible(self, value : bool):
        ...
    
    @property
    def tab_color(self) -> aspose.pydrawing.Color:
        ...
    
    @tab_color.setter
    def tab_color(self, value : aspose.pydrawing.Color):
        ...
    
    @property
    def code_name(self) -> str:
        ...
    
    @code_name.setter
    def code_name(self, value : str):
        ...
    
    @property
    def background_image(self) -> bytes:
        ...
    
    @background_image.setter
    def background_image(self, value : bytes):
        ...
    
    @property
    def conditional_formattings(self) -> aspose.cells.ConditionalFormattingCollection:
        ...
    
    @property
    def active_cell(self) -> str:
        ...
    
    @active_cell.setter
    def active_cell(self, value : str):
        ...
    
    @property
    def custom_properties(self) -> aspose.cells.properties.CustomPropertyCollection:
        ...
    
    @property
    def smart_tag_setting(self) -> aspose.cells.markup.SmartTagSetting:
        ...
    
    @property
    def scenarios(self) -> aspose.cells.ScenarioCollection:
        '''Gets the collection of :py:class:`aspose.cells.Scenario`.'''
        ...
    
    @property
    def cell_watches(self) -> aspose.cells.CellWatchCollection:
        ...
    
    ...

class WorksheetCollection:
    '''Encapsulates a collection of :py:class:`aspose.cells.Worksheet` objects.'''
    
    @overload
    def get(self, index : int) -> aspose.cells.Worksheet:
        '''Add API for Python Via .Net.since this[int index] is unsupported
        
        :param index: The zero based index of the element.'''
        ...
    
    @overload
    def get(self, sheet_name : str) -> aspose.cells.Worksheet:
        '''Add API for Python Via .Net.since this[string sheetName] is unsupported
        
        :param sheet_name: Worksheet name'''
        ...
    
    @overload
    def add(self, type : aspose.cells.SheetType) -> int:
        '''Adds a worksheet to the collection.
        
        :param type: Worksheet type.
        :returns: :py:class:`aspose.cells.Worksheet` object index.'''
        ...
    
    @overload
    def add(self) -> int:
        '''Adds a worksheet to the collection.
        
        :returns: :py:class:`aspose.cells.Worksheet` object index.'''
        ...
    
    @overload
    def add(self, sheet_name : str) -> aspose.cells.Worksheet:
        '''Adds a worksheet to the collection.
        
        :param sheet_name: Worksheet name
        :returns: :py:class:`aspose.cells.Worksheet` object.'''
        ...
    
    @overload
    def register_add_in_function(self, add_in_file : str, function_name : str, lib : bool) -> int:
        '''Adds addin function into the workbook
        
        :param add_in_file: the file contains the addin functions
        :param function_name: the addin function name
        :param lib: whether the given addin file is in the directory or sub-directory of Workbook Add-In library.
        This flag takes effect and makes difference when given addInFile is of relative path:
        true denotes the path is relative to Add-In library and false denotes the path is relative to this Workbook.
        :returns: ID of the data which contains given addin function'''
        ...
    
    @overload
    def register_add_in_function(self, id : int, function_name : str) -> str:
        '''Adds addin function into the workbook
        
        :param id: ID of the data which contains addin functions,
        can be got by the first call of :py:func:`aspose.cells.WorksheetCollection.register_add_in_function` for the same addin file.
        :param function_name: the addin function name
        :returns: URL of the addin file which contains addin functions'''
        ...
    
    @overload
    def add_copy(self, sheet_name : str) -> int:
        '''Adds a worksheet to the collection and copies data from an existed worksheet.
        
        :param sheet_name: Name of source worksheet.
        :returns: :py:class:`aspose.cells.Worksheet` object index.'''
        ...
    
    @overload
    def add_copy(self, sheet_index : int) -> int:
        '''Adds a worksheet to the collection and copies data from an existed worksheet.
        
        :param sheet_index: Index of source worksheet.
        :returns: :py:class:`aspose.cells.Worksheet` object index.'''
        ...
    
    @overload
    def get_range_by_name(self, range_name : str) -> aspose.cells.Range:
        '''Gets Range object by pre-defined name.
        
        :param range_name: Name of range.
        :returns: Range object.
        
        Returns null if the named range does not exist.'''
        ...
    
    @overload
    def get_range_by_name(self, range_name : str, current_sheet_index : int, include_table : bool) -> aspose.cells.Range:
        '''Gets :py:class:`aspose.cells.Range` by pre-defined name or table's name
        
        :param range_name: Name of range or table's name.
        :param current_sheet_index: The sheet index. -1 represents global .
        :param include_table: Indicates whether checking all tables.'''
        ...
    
    @overload
    def copy_to(self, array : List[aspose.cells.Worksheet]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.Worksheet], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.Worksheet, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.Worksheet, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Worksheet) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Worksheet, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.Worksheet, index : int, count : int) -> int:
        ...
    
    def create_range(self, address : str, sheet_index : int) -> aspose.cells.Range:
        '''Creates a :py:class:`aspose.cells.Range` object from an address of the range.
        
        :param address: The address of the range.
        :param sheet_index: The sheet index.
        :returns: A :py:class:`aspose.cells.Range` object'''
        ...
    
    def create_union_range(self, address : str, sheet_index : int) -> aspose.cells.UnionRange:
        '''Creates a :py:class:`aspose.cells.Range` object from an address of the range.
        
        :param address: The address of the range.
        :param sheet_index: The sheet index.
        :returns: A :py:class:`aspose.cells.Range` object'''
        ...
    
    def get_sheet_by_code_name(self, code_name : str) -> aspose.cells.Worksheet:
        '''Gets the worksheet by the code name.
        
        :param code_name: Worksheet code name.
        :returns: The element with the specified code name.'''
        ...
    
    def sort_names(self):
        '''Sorts the defined names.'''
        ...
    
    def swap_sheet(self, sheet_index1 : int, sheet_index2 : int):
        '''Swaps the two sheets.
        
        :param sheet_index1: The first worksheet.
        :param sheet_index2: The second worksheet.'''
        ...
    
    def remove_at(self, name : str):
        '''Removes the element at a specified name.
        
        :param name: The name of the element to remove.'''
        ...
    
    def get_named_ranges(self) -> List[aspose.cells.Range]:
        '''Gets all pre-defined named ranges in the spreadsheet.
        
        :returns: An array of Range objects.
        If the defined Name's reference is external or has multiple ranges, no Range object will be returned for this Name.
        
        
        Returns null if the named range does not exist.'''
        ...
    
    def get_named_ranges_and_tables(self) -> List[aspose.cells.Range]:
        '''Gets all pre-defined named ranges in the spreadsheet.
        
        :returns: An array of Range objects.
        
        Returns null if the named range does not exist.'''
        ...
    
    def set_ole_size(self, start_row : int, end_row : int, start_column : int, end_column : int):
        '''Sets displayed size when Workbook file is used as an Ole object.
        
        :param start_row: Start row index.
        :param end_row: End row index.
        :param start_column: Start column index.
        :param end_column: End column index.'''
        ...
    
    def clear_pivottables(self):
        '''Clears pivot tables from the spreadsheet.'''
        ...
    
    def refresh_pivot_tables(self):
        '''Refreshes all the PivotTables in the WorksheetCollection.'''
        ...
    
    def binary_search(self, item : aspose.cells.Worksheet) -> int:
        ...
    
    @property
    def web_extension_task_panes(self) -> aspose.cells.webextensions.WebExtensionTaskPaneCollection:
        ...
    
    @property
    def web_extensions(self) -> aspose.cells.webextensions.WebExtensionCollection:
        ...
    
    @property
    def threaded_comment_authors(self) -> aspose.cells.ThreadedCommentAuthorCollection:
        ...
    
    @property
    def is_refresh_all_connections(self) -> bool:
        ...
    
    @is_refresh_all_connections.setter
    def is_refresh_all_connections(self, value : bool):
        ...
    
    @property
    def names(self) -> aspose.cells.NameCollection:
        '''Gets the collection of all the Name objects in the spreadsheet.'''
        ...
    
    @property
    def active_sheet_name(self) -> str:
        ...
    
    @active_sheet_name.setter
    def active_sheet_name(self, value : str):
        ...
    
    @property
    def active_sheet_index(self) -> int:
        ...
    
    @active_sheet_index.setter
    def active_sheet_index(self, value : int):
        ...
    
    @property
    def dxfs(self) -> aspose.cells.DxfCollection:
        '''Gets the master differential formatting records.'''
        ...
    
    @property
    def xml_maps(self) -> aspose.cells.XmlMapCollection:
        ...
    
    @xml_maps.setter
    def xml_maps(self, value : aspose.cells.XmlMapCollection):
        ...
    
    @property
    def built_in_document_properties(self) -> aspose.cells.properties.BuiltInDocumentPropertyCollection:
        ...
    
    @property
    def custom_document_properties(self) -> aspose.cells.properties.CustomDocumentPropertyCollection:
        ...
    
    @property
    def ole_size(self) -> any:
        ...
    
    @ole_size.setter
    def ole_size(self, value : any):
        ...
    
    @property
    def external_links(self) -> aspose.cells.ExternalLinkCollection:
        ...
    
    @property
    def table_styles(self) -> aspose.cells.tables.TableStyleCollection:
        ...
    
    @property
    def revision_logs(self) -> aspose.cells.revisions.RevisionLogCollection:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class WriteProtection:
    '''Specifies write protection settings for a workbook.'''
    
    def validate_password(self, password : str) -> bool:
        '''Returns true if the specified password is the same as the write-protection password the file was protected with.
        
        :param password: The specified password.'''
        ...
    
    @property
    def author(self) -> str:
        '''Gets and sets the author.'''
        ...
    
    @author.setter
    def author(self, value : str):
        '''Gets and sets the author.'''
        ...
    
    @property
    def recommend_read_only(self) -> bool:
        ...
    
    @recommend_read_only.setter
    def recommend_read_only(self, value : bool):
        ...
    
    @property
    def is_write_protected(self) -> bool:
        ...
    
    ...

class XlsSaveOptions(SaveOptions):
    '''Represents the save options for the Excel 97-2003 file format: xls and xlt.'''
    
    @property
    def save_format(self) -> aspose.cells.SaveFormat:
        ...
    
    @property
    def clear_data(self) -> bool:
        ...
    
    @clear_data.setter
    def clear_data(self, value : bool):
        ...
    
    @property
    def cached_file_folder(self) -> str:
        ...
    
    @cached_file_folder.setter
    def cached_file_folder(self, value : str):
        ...
    
    @property
    def validate_merged_areas(self) -> bool:
        ...
    
    @validate_merged_areas.setter
    def validate_merged_areas(self, value : bool):
        ...
    
    @property
    def merge_areas(self) -> bool:
        ...
    
    @merge_areas.setter
    def merge_areas(self, value : bool):
        ...
    
    @property
    def create_directory(self) -> bool:
        ...
    
    @create_directory.setter
    def create_directory(self, value : bool):
        ...
    
    @property
    def sort_names(self) -> bool:
        ...
    
    @sort_names.setter
    def sort_names(self, value : bool):
        ...
    
    @property
    def sort_external_names(self) -> bool:
        ...
    
    @sort_external_names.setter
    def sort_external_names(self, value : bool):
        ...
    
    @property
    def refresh_chart_cache(self) -> bool:
        ...
    
    @refresh_chart_cache.setter
    def refresh_chart_cache(self, value : bool):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def update_smart_art(self) -> bool:
        ...
    
    @update_smart_art.setter
    def update_smart_art(self, value : bool):
        ...
    
    @property
    def light_cells_data_provider(self) -> aspose.cells.LightCellsDataProvider:
        ...
    
    @light_cells_data_provider.setter
    def light_cells_data_provider(self, value : aspose.cells.LightCellsDataProvider):
        ...
    
    @property
    def is_template(self) -> bool:
        ...
    
    @is_template.setter
    def is_template(self, value : bool):
        ...
    
    @property
    def match_color(self) -> bool:
        ...
    
    @match_color.setter
    def match_color(self, value : bool):
        ...
    
    ...

class XlsbSaveOptions(SaveOptions):
    '''Represents the options for saving xlsb file.'''
    
    @property
    def save_format(self) -> aspose.cells.SaveFormat:
        ...
    
    @property
    def clear_data(self) -> bool:
        ...
    
    @clear_data.setter
    def clear_data(self, value : bool):
        ...
    
    @property
    def cached_file_folder(self) -> str:
        ...
    
    @cached_file_folder.setter
    def cached_file_folder(self, value : str):
        ...
    
    @property
    def validate_merged_areas(self) -> bool:
        ...
    
    @validate_merged_areas.setter
    def validate_merged_areas(self, value : bool):
        ...
    
    @property
    def merge_areas(self) -> bool:
        ...
    
    @merge_areas.setter
    def merge_areas(self, value : bool):
        ...
    
    @property
    def create_directory(self) -> bool:
        ...
    
    @create_directory.setter
    def create_directory(self, value : bool):
        ...
    
    @property
    def sort_names(self) -> bool:
        ...
    
    @sort_names.setter
    def sort_names(self, value : bool):
        ...
    
    @property
    def sort_external_names(self) -> bool:
        ...
    
    @sort_external_names.setter
    def sort_external_names(self, value : bool):
        ...
    
    @property
    def refresh_chart_cache(self) -> bool:
        ...
    
    @refresh_chart_cache.setter
    def refresh_chart_cache(self, value : bool):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def update_smart_art(self) -> bool:
        ...
    
    @update_smart_art.setter
    def update_smart_art(self, value : bool):
        ...
    
    @property
    def compression_type(self) -> aspose.cells.OoxmlCompressionType:
        ...
    
    @compression_type.setter
    def compression_type(self, value : aspose.cells.OoxmlCompressionType):
        ...
    
    @property
    def export_all_column_indexes(self) -> bool:
        ...
    
    @export_all_column_indexes.setter
    def export_all_column_indexes(self, value : bool):
        ...
    
    @property
    def light_cells_data_provider(self) -> aspose.cells.LightCellsDataProvider:
        ...
    
    @light_cells_data_provider.setter
    def light_cells_data_provider(self, value : aspose.cells.LightCellsDataProvider):
        ...
    
    ...

class XmlColumnProperty:
    '''Represents Xml Data Binding information.'''
    
    ...

class XmlDataBinding:
    '''Represents Xml Data Binding information.'''
    
    @property
    def url(self) -> str:
        '''Gets source url of this data binding.'''
        ...
    
    ...

class XmlLoadOptions(LoadOptions):
    '''Represents the options of loading xml.'''
    
    def set_paper_size(self, type : aspose.cells.PaperSizeType):
        '''Sets the default print paper size from default printer's setting.
        
        :param type: The default paper size.'''
        ...
    
    @property
    def load_format(self) -> aspose.cells.LoadFormat:
        ...
    
    @property
    def password(self) -> str:
        '''Gets and set the password of the workbook.'''
        ...
    
    @password.setter
    def password(self, value : str):
        '''Gets and set the password of the workbook.'''
        ...
    
    @property
    def parsing_formula_on_open(self) -> bool:
        ...
    
    @parsing_formula_on_open.setter
    def parsing_formula_on_open(self, value : bool):
        ...
    
    @property
    def parsing_pivot_cached_records(self) -> bool:
        ...
    
    @parsing_pivot_cached_records.setter
    def parsing_pivot_cached_records(self, value : bool):
        ...
    
    @property
    def language_code(self) -> aspose.cells.CountryCode:
        ...
    
    @language_code.setter
    def language_code(self, value : aspose.cells.CountryCode):
        ...
    
    @property
    def region(self) -> aspose.cells.CountryCode:
        '''Gets the system regional settings based on CountryCode at the time the file was loaded.'''
        ...
    
    @region.setter
    def region(self, value : aspose.cells.CountryCode):
        '''Sets the system regional settings based on CountryCode at the time the file was loaded.'''
        ...
    
    @property
    def default_style_settings(self) -> aspose.cells.DefaultStyleSettings:
        ...
    
    @property
    def standard_font(self) -> str:
        ...
    
    @standard_font.setter
    def standard_font(self, value : str):
        ...
    
    @property
    def standard_font_size(self) -> float:
        ...
    
    @standard_font_size.setter
    def standard_font_size(self, value : float):
        ...
    
    @property
    def interrupt_monitor(self) -> aspose.cells.AbstractInterruptMonitor:
        ...
    
    @interrupt_monitor.setter
    def interrupt_monitor(self, value : aspose.cells.AbstractInterruptMonitor):
        ...
    
    @property
    def ignore_not_printed(self) -> bool:
        ...
    
    @ignore_not_printed.setter
    def ignore_not_printed(self, value : bool):
        ...
    
    @property
    def check_data_valid(self) -> bool:
        ...
    
    @check_data_valid.setter
    def check_data_valid(self, value : bool):
        ...
    
    @property
    def check_excel_restriction(self) -> bool:
        ...
    
    @check_excel_restriction.setter
    def check_excel_restriction(self, value : bool):
        ...
    
    @property
    def keep_unparsed_data(self) -> bool:
        ...
    
    @keep_unparsed_data.setter
    def keep_unparsed_data(self, value : bool):
        ...
    
    @property
    def load_filter(self) -> aspose.cells.LoadFilter:
        ...
    
    @load_filter.setter
    def load_filter(self, value : aspose.cells.LoadFilter):
        ...
    
    @property
    def light_cells_data_handler(self) -> aspose.cells.LightCellsDataHandler:
        ...
    
    @light_cells_data_handler.setter
    def light_cells_data_handler(self, value : aspose.cells.LightCellsDataHandler):
        ...
    
    @property
    def memory_setting(self) -> aspose.cells.MemorySetting:
        ...
    
    @memory_setting.setter
    def memory_setting(self, value : aspose.cells.MemorySetting):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def auto_fitter_options(self) -> aspose.cells.AutoFitterOptions:
        ...
    
    @auto_fitter_options.setter
    def auto_fitter_options(self, value : aspose.cells.AutoFitterOptions):
        ...
    
    @property
    def auto_filter(self) -> bool:
        ...
    
    @auto_filter.setter
    def auto_filter(self, value : bool):
        ...
    
    @property
    def font_configs(self) -> aspose.cells.IndividualFontConfigs:
        ...
    
    @font_configs.setter
    def font_configs(self, value : aspose.cells.IndividualFontConfigs):
        ...
    
    @property
    def start_cell(self) -> str:
        ...
    
    @start_cell.setter
    def start_cell(self, value : str):
        ...
    
    @property
    def is_xml_map(self) -> bool:
        ...
    
    @is_xml_map.setter
    def is_xml_map(self, value : bool):
        ...
    
    @property
    def contains_multiple_worksheets(self) -> bool:
        ...
    
    @contains_multiple_worksheets.setter
    def contains_multiple_worksheets(self, value : bool):
        ...
    
    ...

class XmlMap:
    '''Represents Xml map information.'''
    
    @property
    def name(self) -> str:
        '''Returns the name of the object.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Returns or sets the name of the object.'''
        ...
    
    @property
    def root_element_name(self) -> str:
        ...
    
    @property
    def data_binding(self) -> aspose.cells.XmlDataBinding:
        ...
    
    ...

class XmlMapCollection:
    '''A collection of :py:class:`aspose.cells.XmlMap` objects that represent XmlMap information.'''
    
    @overload
    def copy_to(self, array : List[aspose.cells.XmlMap]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.XmlMap], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.XmlMap, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.XmlMap, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.XmlMap) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.XmlMap, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.XmlMap, index : int, count : int) -> int:
        ...
    
    def add(self, url : str) -> int:
        '''Add a :py:class:`aspose.cells.XmlMap` by the url/path of a xml/xsd file.
        
        :param url: url/path of a xml/xsd file.
        :returns: :py:class:`aspose.cells.XmlMap` object index.'''
        ...
    
    def binary_search(self, item : aspose.cells.XmlMap) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class XmlSaveOptions(SaveOptions):
    '''Represents the options of saving the workbook as an xml file.'''
    
    @property
    def save_format(self) -> aspose.cells.SaveFormat:
        ...
    
    @property
    def clear_data(self) -> bool:
        ...
    
    @clear_data.setter
    def clear_data(self, value : bool):
        ...
    
    @property
    def cached_file_folder(self) -> str:
        ...
    
    @cached_file_folder.setter
    def cached_file_folder(self, value : str):
        ...
    
    @property
    def validate_merged_areas(self) -> bool:
        ...
    
    @validate_merged_areas.setter
    def validate_merged_areas(self, value : bool):
        ...
    
    @property
    def merge_areas(self) -> bool:
        ...
    
    @merge_areas.setter
    def merge_areas(self, value : bool):
        ...
    
    @property
    def create_directory(self) -> bool:
        ...
    
    @create_directory.setter
    def create_directory(self, value : bool):
        ...
    
    @property
    def sort_names(self) -> bool:
        ...
    
    @sort_names.setter
    def sort_names(self, value : bool):
        ...
    
    @property
    def sort_external_names(self) -> bool:
        ...
    
    @sort_external_names.setter
    def sort_external_names(self, value : bool):
        ...
    
    @property
    def refresh_chart_cache(self) -> bool:
        ...
    
    @refresh_chart_cache.setter
    def refresh_chart_cache(self, value : bool):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def update_smart_art(self) -> bool:
        ...
    
    @update_smart_art.setter
    def update_smart_art(self, value : bool):
        ...
    
    @property
    def sheet_indexes(self) -> List[int]:
        ...
    
    @sheet_indexes.setter
    def sheet_indexes(self, value : List[int]):
        ...
    
    @property
    def export_area(self) -> aspose.cells.CellArea:
        ...
    
    @export_area.setter
    def export_area(self, value : aspose.cells.CellArea):
        ...
    
    @property
    def has_header_row(self) -> bool:
        ...
    
    @has_header_row.setter
    def has_header_row(self, value : bool):
        ...
    
    @property
    def xml_map_name(self) -> str:
        ...
    
    @xml_map_name.setter
    def xml_map_name(self, value : str):
        ...
    
    ...

class XpsSaveOptions(PaginatedSaveOptions):
    '''Represents the additional options when saving the file as the Xps.'''
    
    @property
    def save_format(self) -> aspose.cells.SaveFormat:
        ...
    
    @property
    def clear_data(self) -> bool:
        ...
    
    @clear_data.setter
    def clear_data(self, value : bool):
        ...
    
    @property
    def cached_file_folder(self) -> str:
        ...
    
    @cached_file_folder.setter
    def cached_file_folder(self, value : str):
        ...
    
    @property
    def validate_merged_areas(self) -> bool:
        ...
    
    @validate_merged_areas.setter
    def validate_merged_areas(self, value : bool):
        ...
    
    @property
    def merge_areas(self) -> bool:
        ...
    
    @merge_areas.setter
    def merge_areas(self, value : bool):
        ...
    
    @property
    def create_directory(self) -> bool:
        ...
    
    @create_directory.setter
    def create_directory(self, value : bool):
        ...
    
    @property
    def sort_names(self) -> bool:
        ...
    
    @sort_names.setter
    def sort_names(self, value : bool):
        ...
    
    @property
    def sort_external_names(self) -> bool:
        ...
    
    @sort_external_names.setter
    def sort_external_names(self, value : bool):
        ...
    
    @property
    def refresh_chart_cache(self) -> bool:
        ...
    
    @refresh_chart_cache.setter
    def refresh_chart_cache(self, value : bool):
        ...
    
    @property
    def warning_callback(self) -> aspose.cells.IWarningCallback:
        ...
    
    @warning_callback.setter
    def warning_callback(self, value : aspose.cells.IWarningCallback):
        ...
    
    @property
    def update_smart_art(self) -> bool:
        ...
    
    @update_smart_art.setter
    def update_smart_art(self, value : bool):
        ...
    
    @property
    def default_font(self) -> str:
        ...
    
    @default_font.setter
    def default_font(self, value : str):
        ...
    
    @property
    def check_workbook_default_font(self) -> bool:
        ...
    
    @check_workbook_default_font.setter
    def check_workbook_default_font(self, value : bool):
        ...
    
    @property
    def check_font_compatibility(self) -> bool:
        ...
    
    @check_font_compatibility.setter
    def check_font_compatibility(self, value : bool):
        ...
    
    @property
    def is_font_substitution_char_granularity(self) -> bool:
        ...
    
    @is_font_substitution_char_granularity.setter
    def is_font_substitution_char_granularity(self, value : bool):
        ...
    
    @property
    def one_page_per_sheet(self) -> bool:
        ...
    
    @one_page_per_sheet.setter
    def one_page_per_sheet(self, value : bool):
        ...
    
    @property
    def all_columns_in_one_page_per_sheet(self) -> bool:
        ...
    
    @all_columns_in_one_page_per_sheet.setter
    def all_columns_in_one_page_per_sheet(self, value : bool):
        ...
    
    @property
    def ignore_error(self) -> bool:
        ...
    
    @ignore_error.setter
    def ignore_error(self, value : bool):
        ...
    
    @property
    def output_blank_page_when_nothing_to_print(self) -> bool:
        ...
    
    @output_blank_page_when_nothing_to_print.setter
    def output_blank_page_when_nothing_to_print(self, value : bool):
        ...
    
    @property
    def page_index(self) -> int:
        ...
    
    @page_index.setter
    def page_index(self, value : int):
        ...
    
    @property
    def page_count(self) -> int:
        ...
    
    @page_count.setter
    def page_count(self, value : int):
        ...
    
    @property
    def printing_page_type(self) -> aspose.cells.PrintingPageType:
        ...
    
    @printing_page_type.setter
    def printing_page_type(self, value : aspose.cells.PrintingPageType):
        ...
    
    @property
    def gridline_type(self) -> aspose.cells.GridlineType:
        ...
    
    @gridline_type.setter
    def gridline_type(self, value : aspose.cells.GridlineType):
        ...
    
    @property
    def text_cross_type(self) -> aspose.cells.TextCrossType:
        ...
    
    @text_cross_type.setter
    def text_cross_type(self, value : aspose.cells.TextCrossType):
        ...
    
    @property
    def default_edit_language(self) -> aspose.cells.DefaultEditLanguage:
        ...
    
    @default_edit_language.setter
    def default_edit_language(self, value : aspose.cells.DefaultEditLanguage):
        ...
    
    @property
    def sheet_set(self) -> aspose.cells.rendering.SheetSet:
        ...
    
    @sheet_set.setter
    def sheet_set(self, value : aspose.cells.rendering.SheetSet):
        ...
    
    @property
    def draw_object_event_handler(self) -> aspose.cells.rendering.DrawObjectEventHandler:
        ...
    
    @draw_object_event_handler.setter
    def draw_object_event_handler(self, value : aspose.cells.rendering.DrawObjectEventHandler):
        ...
    
    @property
    def page_saving_callback(self) -> aspose.cells.rendering.IPageSavingCallback:
        ...
    
    @page_saving_callback.setter
    def page_saving_callback(self, value : aspose.cells.rendering.IPageSavingCallback):
        ...
    
    ...

class AccessCacheOptions:
    '''Cache options for data access. Can be combined with | operator for multiple options together.'''
    
    @classmethod
    @property
    def NONE(cls) -> AccessCacheOptions:
        '''No cache for any data access.'''
        ...
    
    @classmethod
    @property
    def ALL(cls) -> AccessCacheOptions:
        '''Apply all possible optimizations for all kinds of data access in the workbook.
        All settings and data should not be changed during the optimized access.'''
        ...
    
    @classmethod
    @property
    def POSITION_AND_SIZE(cls) -> AccessCacheOptions:
        '''Apply possible optimization for getting object(such as Shape)'s position and size.
        Row height and column width settings should not be changed during the optimized access.'''
        ...
    
    @classmethod
    @property
    def CELLS_DATA(cls) -> AccessCacheOptions:
        '''Apply possible optimization for getting cells' values.
        Cells data(data and settings of Cell, Row) should not be changed during
        the optimized access, no new Cell/Row objects should be created either(such as
        by :py:func:`aspose.cells.Cells.__getitem__`).'''
        ...
    
    @classmethod
    @property
    def CELL_DISPLAY(cls) -> AccessCacheOptions:
        '''Apply possible optimization for getting display-related results of
        cells(:py:attr:`aspose.cells.Cell.display_string_value`, :py:func:`aspose.cells.Cell.get_style`, :py:func:`aspose.cells.Cell.get_display_style`, etc.).
        Cells data and style-related objects(Cell/Row/Column styles, column width, etc.) should not be changed
        during the optimized access.'''
        ...
    
    @classmethod
    @property
    def GET_FORMULA(cls) -> AccessCacheOptions:
        '''Apply possible optimization for getting formulas.
        All data and settings which may affect the formula expression(Worksheet's name, Name's text,
        table's column, etc.) should not be changed during the optimized access.'''
        ...
    
    @classmethod
    @property
    def SET_FORMULA(cls) -> AccessCacheOptions:
        '''Apply possible optimization for setting formulas.
        All data and settings which may affect the formula expression(Worksheet's name, Name's text,
        table's column, etc.) should not be changed during the optimized access.'''
        ...
    
    @classmethod
    @property
    def CALCULATE_FORMULA(cls) -> AccessCacheOptions:
        '''Apply possible optimization for calculating formulas.
        Cells data should not be changed during the optimized access, none new objects(Cell, Row, etc.)
        should be created either(such as by :py:func:`aspose.cells.Cells.__getitem__`).'''
        ...
    
    @classmethod
    @property
    def CONDITIONAL_FORMATTING(cls) -> AccessCacheOptions:
        '''Apply possible optimization for getting formatting result of conditional formattings.
        All data and settings which may affect the result of conditional formattings(settings of
        conditional formattings, dependent cell values, etc.) should not be changed during the optimized access.'''
        ...
    
    @classmethod
    @property
    def VALIDATION(cls) -> AccessCacheOptions:
        '''Apply possible optimization for getting validation result.
        All data and settings which may affect the result of validation(settings of the validation,
        dependent cell values, etc.) should not be changed during the optimized access.'''
        ...
    
    ...

class AutoFillType:
    '''Represents the auto fill type.'''
    
    @classmethod
    @property
    def COPY(cls) -> AutoFillType:
        '''Copies the value and format of the source area to the target area'''
        ...
    
    @classmethod
    @property
    def DEFAULT(cls) -> AutoFillType:
        '''Automatically fills the target area with the value and format.'''
        ...
    
    @classmethod
    @property
    def FORMATS(cls) -> AutoFillType:
        '''Copies only the format of the source area to the target area,'''
        ...
    
    @classmethod
    @property
    def SERIES(cls) -> AutoFillType:
        '''Extend the value in the source area to the target area in the form of a series and copy format to the target area.'''
        ...
    
    @classmethod
    @property
    def VALUES(cls) -> AutoFillType:
        '''Copies only the value of the source area to the target area,'''
        ...
    
    ...

class AutoFitMergedCellsType:
    '''Represents the type of auto fitting merged cells.'''
    
    @classmethod
    @property
    def NONE(cls) -> AutoFitMergedCellsType:
        '''Ignore merged cells.'''
        ...
    
    @classmethod
    @property
    def FIRST_LINE(cls) -> AutoFitMergedCellsType:
        '''Only expands the height of the first row.'''
        ...
    
    @classmethod
    @property
    def LAST_LINE(cls) -> AutoFitMergedCellsType:
        '''Only expands the height of the last row.'''
        ...
    
    @classmethod
    @property
    def EACH_LINE(cls) -> AutoFitMergedCellsType:
        '''Only expands the height of each row.'''
        ...
    
    ...

class AutoFitWrappedTextType:
    '''Represents the type of auto fitting wrapped text.'''
    
    @classmethod
    @property
    def DEFAULT(cls) -> AutoFitWrappedTextType:
        '''Works as MS Excel.'''
        ...
    
    @classmethod
    @property
    def PARAGRAPH(cls) -> AutoFitWrappedTextType:
        '''Auto fit width with the longest paragraph.'''
        ...
    
    ...

class BackgroundType:
    '''Enumerates cell background pattern types.'''
    
    @classmethod
    @property
    def DIAGONAL_CROSSHATCH(cls) -> BackgroundType:
        '''Represents diagonal crosshatch pattern.'''
        ...
    
    @classmethod
    @property
    def DIAGONAL_STRIPE(cls) -> BackgroundType:
        '''Represents diagonal stripe pattern.'''
        ...
    
    @classmethod
    @property
    def GRAY6(cls) -> BackgroundType:
        '''Represents 6.25% gray pattern'''
        ...
    
    @classmethod
    @property
    def GRAY12(cls) -> BackgroundType:
        '''Represents 12.5% gray pattern'''
        ...
    
    @classmethod
    @property
    def GRAY25(cls) -> BackgroundType:
        '''Represents 25% gray pattern.'''
        ...
    
    @classmethod
    @property
    def GRAY50(cls) -> BackgroundType:
        '''Represents 50% gray pattern.'''
        ...
    
    @classmethod
    @property
    def GRAY75(cls) -> BackgroundType:
        '''Represents 75% gray pattern.'''
        ...
    
    @classmethod
    @property
    def HORIZONTAL_STRIPE(cls) -> BackgroundType:
        '''Represents horizontal stripe pattern.'''
        ...
    
    @classmethod
    @property
    def NONE(cls) -> BackgroundType:
        '''Represents no background.'''
        ...
    
    @classmethod
    @property
    def REVERSE_DIAGONAL_STRIPE(cls) -> BackgroundType:
        '''Represents reverse diagonal stripe pattern.'''
        ...
    
    @classmethod
    @property
    def SOLID(cls) -> BackgroundType:
        '''Represents solid pattern.'''
        ...
    
    @classmethod
    @property
    def THICK_DIAGONAL_CROSSHATCH(cls) -> BackgroundType:
        '''Represents thick diagonal crosshatch pattern.'''
        ...
    
    @classmethod
    @property
    def THIN_DIAGONAL_CROSSHATCH(cls) -> BackgroundType:
        '''Represents thin diagonal crosshatch pattern.'''
        ...
    
    @classmethod
    @property
    def THIN_DIAGONAL_STRIPE(cls) -> BackgroundType:
        '''Represents thin diagonal stripe pattern.'''
        ...
    
    @classmethod
    @property
    def THIN_HORIZONTAL_CROSSHATCH(cls) -> BackgroundType:
        '''Represents thin horizontal crosshatch pattern.'''
        ...
    
    @classmethod
    @property
    def THIN_HORIZONTAL_STRIPE(cls) -> BackgroundType:
        '''Represents thin horizontal stripe pattern.'''
        ...
    
    @classmethod
    @property
    def THIN_REVERSE_DIAGONAL_STRIPE(cls) -> BackgroundType:
        '''Represents thin reverse diagonal stripe pattern.'''
        ...
    
    @classmethod
    @property
    def THIN_VERTICAL_STRIPE(cls) -> BackgroundType:
        '''Represents thin vertical stripe pattern.'''
        ...
    
    @classmethod
    @property
    def VERTICAL_STRIPE(cls) -> BackgroundType:
        '''Represents vertical stripe pattern.'''
        ...
    
    ...

class BorderType:
    '''Enumerates the border line and diagonal line types.'''
    
    @classmethod
    @property
    def BOTTOM_BORDER(cls) -> BorderType:
        '''Represents bottom border line.'''
        ...
    
    @classmethod
    @property
    def DIAGONAL_DOWN(cls) -> BorderType:
        '''Represents the diagonal line from top left to right bottom.'''
        ...
    
    @classmethod
    @property
    def DIAGONAL_UP(cls) -> BorderType:
        '''Represents the diagonal line from bottom left to right top.'''
        ...
    
    @classmethod
    @property
    def LEFT_BORDER(cls) -> BorderType:
        '''Represents left border line.'''
        ...
    
    @classmethod
    @property
    def RIGHT_BORDER(cls) -> BorderType:
        '''Represents right border line exists.'''
        ...
    
    @classmethod
    @property
    def TOP_BORDER(cls) -> BorderType:
        '''Represents top border line.'''
        ...
    
    @classmethod
    @property
    def HORIZONTAL(cls) -> BorderType:
        '''Only for dynamic style,such as conditional formatting.'''
        ...
    
    @classmethod
    @property
    def VERTICAL(cls) -> BorderType:
        '''Only for dynamic style,such as conditional formatting.'''
        ...
    
    ...

class BuiltinStyleType:
    '''Represents all built-in style types.'''
    
    @classmethod
    @property
    def TWENTY_PERCENT_ACCENT1(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def TWENTY_PERCENT_ACCENT2(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def TWENTY_PERCENT_ACCENT3(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def TWENTY_PERCENT_ACCENT4(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def TWENTY_PERCENT_ACCENT5(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def TWENTY_PERCENT_ACCENT6(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def FORTY_PERCENT_ACCENT1(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def FORTY_PERCENT_ACCENT2(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def FORTY_PERCENT_ACCENT3(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def FORTY_PERCENT_ACCENT4(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def FORTY_PERCENT_ACCENT5(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def FORTY_PERCENT_ACCENT6(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def SIXTY_PERCENT_ACCENT1(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def SIXTY_PERCENT_ACCENT2(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def SIXTY_PERCENT_ACCENT3(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def SIXTY_PERCENT_ACCENT4(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def SIXTY_PERCENT_ACCENT5(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def SIXTY_PERCENT_ACCENT6(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def ACCENT1(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def ACCENT2(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def ACCENT3(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def ACCENT4(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def ACCENT5(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def ACCENT6(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def BAD(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def CALCULATION(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def CHECK_CELL(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def COMMA(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def COMMA1(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def CURRENCY(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def CURRENCY1(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def EXPLANATORY_TEXT(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def GOOD(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def HEADER1(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def HEADER2(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def HEADER3(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def HEADER4(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def HYPERLINK(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def FOLLOWED_HYPERLINK(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def INPUT(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def LINKED_CELL(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def NEUTRAL(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def NORMAL(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def NOTE(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def OUTPUT(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def PERCENT(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def TITLE(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def TOTAL(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def WARNING_TEXT(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def ROW_LEVEL(cls) -> BuiltinStyleType:
        ...
    
    @classmethod
    @property
    def COLUMN_LEVEL(cls) -> BuiltinStyleType:
        ...
    
    ...

class CalcModeType:
    '''Represents the mode type of calculating formulas.'''
    
    @classmethod
    @property
    def AUTOMATIC(cls) -> CalcModeType:
        ...
    
    @classmethod
    @property
    def AUTOMATIC_EXCEPT_TABLE(cls) -> CalcModeType:
        ...
    
    @classmethod
    @property
    def MANUAL(cls) -> CalcModeType:
        ...
    
    ...

class CalculationPrecisionStrategy:
    '''Enumerates strategies for handling calculation precision.
    Because of the precision issue of IEEE 754 Floating-Point Arithmetic, some "seemingly simple" formulas may not be calculated as the expected result.
    Such as formula "=-0.45+0.43+0.02", when calculating operands by '+' operator directly, the result is not zero. For such kind of precision issue,
    some special strategies may give the expected result.'''
    
    @classmethod
    @property
    def NONE(cls) -> CalculationPrecisionStrategy:
        '''No strategy applied on calculation.
        When calculating just use the original double value as operand and return the result directly.
        Most efficient for performance and applicable for most cases.'''
        ...
    
    @classmethod
    @property
    def ROUND(cls) -> CalculationPrecisionStrategy:
        '''Rounds the calculation result according with significant digits.'''
        ...
    
    @classmethod
    @property
    def DECIMAL(cls) -> CalculationPrecisionStrategy:
        '''Uses decimal as operands when possible.
        Most inefficient for performance.'''
        ...
    
    ...

class CellBorderType:
    '''Enumerates a cell's border type.'''
    
    @classmethod
    @property
    def DASH_DOT(cls) -> CellBorderType:
        '''Represents thin dash-dotted line.'''
        ...
    
    @classmethod
    @property
    def DASH_DOT_DOT(cls) -> CellBorderType:
        '''Represents thin dash-dot-dotted line.'''
        ...
    
    @classmethod
    @property
    def DASHED(cls) -> CellBorderType:
        '''Represents dashed line.'''
        ...
    
    @classmethod
    @property
    def DOTTED(cls) -> CellBorderType:
        '''Represents dotted line.'''
        ...
    
    @classmethod
    @property
    def DOUBLE(cls) -> CellBorderType:
        '''Represents double line.'''
        ...
    
    @classmethod
    @property
    def HAIR(cls) -> CellBorderType:
        '''Represents hair line.'''
        ...
    
    @classmethod
    @property
    def MEDIUM_DASH_DOT(cls) -> CellBorderType:
        '''Represents medium dash-dotted line.'''
        ...
    
    @classmethod
    @property
    def MEDIUM_DASH_DOT_DOT(cls) -> CellBorderType:
        '''Represents medium dash-dot-dotted line.'''
        ...
    
    @classmethod
    @property
    def MEDIUM_DASHED(cls) -> CellBorderType:
        '''Represents medium dashed line.'''
        ...
    
    @classmethod
    @property
    def NONE(cls) -> CellBorderType:
        '''Represents no line.'''
        ...
    
    @classmethod
    @property
    def MEDIUM(cls) -> CellBorderType:
        '''Represents medium line.'''
        ...
    
    @classmethod
    @property
    def SLANTED_DASH_DOT(cls) -> CellBorderType:
        '''Represents slanted medium dash-dotted line.'''
        ...
    
    @classmethod
    @property
    def THICK(cls) -> CellBorderType:
        '''Represents thick line.'''
        ...
    
    @classmethod
    @property
    def THIN(cls) -> CellBorderType:
        '''Represents thin line.'''
        ...
    
    ...

class CellValueFormatStrategy:
    '''Specifies how to apply style for the value of the cell.'''
    
    @classmethod
    @property
    def NONE(cls) -> CellValueFormatStrategy:
        '''Not formatted.'''
        ...
    
    @classmethod
    @property
    def CELL_STYLE(cls) -> CellValueFormatStrategy:
        '''Only formatted with the cell's original style.'''
        ...
    
    @classmethod
    @property
    def DISPLAY_STYLE(cls) -> CellValueFormatStrategy:
        '''Formatted with the cell's displayed style.'''
        ...
    
    @classmethod
    @property
    def DISPLAY_STRING(cls) -> CellValueFormatStrategy:
        '''Gets the displayed string shown in ms excel.
        The main difference from :py:attr:`aspose.cells.CellValueFormatStrategy.DISPLAY_STYLE` is this option also considers the effect of column width.
        If the column width is too small to show the formatted string completely,
        "#" may be shown, just like what ms excel does.'''
        ...
    
    ...

class CellValueType:
    '''Specifies a cell value type.'''
    
    @classmethod
    @property
    def IS_BOOL(cls) -> CellValueType:
        '''Cell value is boolean.'''
        ...
    
    @classmethod
    @property
    def IS_DATE_TIME(cls) -> CellValueType:
        '''Cell value is datetime.'''
        ...
    
    @classmethod
    @property
    def IS_ERROR(cls) -> CellValueType:
        '''Cell contains error value'''
        ...
    
    @classmethod
    @property
    def IS_NULL(cls) -> CellValueType:
        '''Blank cell.'''
        ...
    
    @classmethod
    @property
    def IS_NUMERIC(cls) -> CellValueType:
        '''Cell value is numeric.'''
        ...
    
    @classmethod
    @property
    def IS_STRING(cls) -> CellValueType:
        '''Cell value is string.'''
        ...
    
    @classmethod
    @property
    def IS_UNKNOWN(cls) -> CellValueType:
        '''Cell value type is unknown.'''
        ...
    
    ...

class ColorType:
    '''Represents all color type'''
    
    @classmethod
    @property
    def AUTOMATIC(cls) -> ColorType:
        '''Automatic color.'''
        ...
    
    @classmethod
    @property
    def AUTOMATIC_INDEX(cls) -> ColorType:
        '''It's automatic color,but the displayed color depends the setting of the OS System.'''
        ...
    
    @classmethod
    @property
    def RGB(cls) -> ColorType:
        '''The RGB color.'''
        ...
    
    @classmethod
    @property
    def INDEXED_COLOR(cls) -> ColorType:
        '''The color index in the color palette.'''
        ...
    
    @classmethod
    @property
    def THEME(cls) -> ColorType:
        '''The theme color.'''
        ...
    
    ...

class ConsolidationFunction:
    '''Represents consolidation function.'''
    
    @classmethod
    @property
    def SUM(cls) -> ConsolidationFunction:
        '''Represents Sum function.'''
        ...
    
    @classmethod
    @property
    def COUNT(cls) -> ConsolidationFunction:
        '''Represents Count function.'''
        ...
    
    @classmethod
    @property
    def AVERAGE(cls) -> ConsolidationFunction:
        '''Represents Average function.'''
        ...
    
    @classmethod
    @property
    def MAX(cls) -> ConsolidationFunction:
        '''Represents Max function.'''
        ...
    
    @classmethod
    @property
    def MIN(cls) -> ConsolidationFunction:
        '''Represents Min function.'''
        ...
    
    @classmethod
    @property
    def PRODUCT(cls) -> ConsolidationFunction:
        '''Represents Product function.'''
        ...
    
    @classmethod
    @property
    def COUNT_NUMS(cls) -> ConsolidationFunction:
        '''Represents Count Nums function.'''
        ...
    
    @classmethod
    @property
    def STD_DEV(cls) -> ConsolidationFunction:
        '''Represents StdDev function.'''
        ...
    
    @classmethod
    @property
    def STD_DEVP(cls) -> ConsolidationFunction:
        '''Represents StdDevp function.'''
        ...
    
    @classmethod
    @property
    def VAR(cls) -> ConsolidationFunction:
        '''Represents Var function.'''
        ...
    
    @classmethod
    @property
    def VARP(cls) -> ConsolidationFunction:
        '''Represents Varp function.'''
        ...
    
    @classmethod
    @property
    def DISTINCT_COUNT(cls) -> ConsolidationFunction:
        '''Represents Distinct Count function.'''
        ...
    
    ...

class CopyFormatType:
    '''Represents type of copying format when inserting rows.'''
    
    @classmethod
    @property
    def SAME_AS_ABOVE(cls) -> CopyFormatType:
        '''Formats same as above row.'''
        ...
    
    @classmethod
    @property
    def SAME_AS_BELOW(cls) -> CopyFormatType:
        '''Formats same as below row.'''
        ...
    
    @classmethod
    @property
    def CLEAR(cls) -> CopyFormatType:
        '''Clears formatting.'''
        ...
    
    ...

class CountryCode:
    '''Represents Excel country identifiers.'''
    
    @classmethod
    @property
    def DEFAULT(cls) -> CountryCode:
        ...
    
    @classmethod
    @property
    def USA(cls) -> CountryCode:
        '''United States'''
        ...
    
    @classmethod
    @property
    def CANADA(cls) -> CountryCode:
        '''Canada'''
        ...
    
    @classmethod
    @property
    def LATIN_AMERIC(cls) -> CountryCode:
        '''Latin America, except Brazil'''
        ...
    
    @classmethod
    @property
    def RUSSIA(cls) -> CountryCode:
        '''Russia'''
        ...
    
    @classmethod
    @property
    def EGYPT(cls) -> CountryCode:
        '''Egypt'''
        ...
    
    @classmethod
    @property
    def GREECE(cls) -> CountryCode:
        '''Greece'''
        ...
    
    @classmethod
    @property
    def NETHERLANDS(cls) -> CountryCode:
        '''Netherlands'''
        ...
    
    @classmethod
    @property
    def BELGIUM(cls) -> CountryCode:
        '''Belgium'''
        ...
    
    @classmethod
    @property
    def FRANCE(cls) -> CountryCode:
        '''France'''
        ...
    
    @classmethod
    @property
    def SPAIN(cls) -> CountryCode:
        '''Spain'''
        ...
    
    @classmethod
    @property
    def HUNGARY(cls) -> CountryCode:
        '''Hungary'''
        ...
    
    @classmethod
    @property
    def ITALY(cls) -> CountryCode:
        '''Italy'''
        ...
    
    @classmethod
    @property
    def SWITZERLAND(cls) -> CountryCode:
        '''Switzerland'''
        ...
    
    @classmethod
    @property
    def AUSTRIA(cls) -> CountryCode:
        '''Austria'''
        ...
    
    @classmethod
    @property
    def UNITED_KINGDOM(cls) -> CountryCode:
        '''United Kingdom'''
        ...
    
    @classmethod
    @property
    def DENMARK(cls) -> CountryCode:
        '''Denmark'''
        ...
    
    @classmethod
    @property
    def SWEDEN(cls) -> CountryCode:
        '''Sweden'''
        ...
    
    @classmethod
    @property
    def NORWAY(cls) -> CountryCode:
        '''Norway'''
        ...
    
    @classmethod
    @property
    def POLAND(cls) -> CountryCode:
        '''Poland'''
        ...
    
    @classmethod
    @property
    def GERMANY(cls) -> CountryCode:
        '''Germany'''
        ...
    
    @classmethod
    @property
    def MEXICO(cls) -> CountryCode:
        '''Mexico'''
        ...
    
    @classmethod
    @property
    def BRAZIL(cls) -> CountryCode:
        '''Brazil'''
        ...
    
    @classmethod
    @property
    def AUSTRALIA(cls) -> CountryCode:
        '''Australia'''
        ...
    
    @classmethod
    @property
    def NEW_ZEALAND(cls) -> CountryCode:
        '''New Zealand'''
        ...
    
    @classmethod
    @property
    def THAILAND(cls) -> CountryCode:
        '''Thailand'''
        ...
    
    @classmethod
    @property
    def JAPAN(cls) -> CountryCode:
        '''Japan'''
        ...
    
    @classmethod
    @property
    def SOUTH_KOREA(cls) -> CountryCode:
        '''SouthKorea'''
        ...
    
    @classmethod
    @property
    def VIET_NAM(cls) -> CountryCode:
        '''Viet Nam'''
        ...
    
    @classmethod
    @property
    def CHINA(cls) -> CountryCode:
        '''People's Republic of China'''
        ...
    
    @classmethod
    @property
    def TURKEY(cls) -> CountryCode:
        '''Turkey'''
        ...
    
    @classmethod
    @property
    def INDIA(cls) -> CountryCode:
        '''India'''
        ...
    
    @classmethod
    @property
    def ALGERIA(cls) -> CountryCode:
        '''Algeria'''
        ...
    
    @classmethod
    @property
    def MOROCCO(cls) -> CountryCode:
        '''Morocco'''
        ...
    
    @classmethod
    @property
    def LIBYA(cls) -> CountryCode:
        '''Libya'''
        ...
    
    @classmethod
    @property
    def PORTUGAL(cls) -> CountryCode:
        '''Portugal'''
        ...
    
    @classmethod
    @property
    def ICELAND(cls) -> CountryCode:
        '''Iceland'''
        ...
    
    @classmethod
    @property
    def FINLAND(cls) -> CountryCode:
        '''Finland'''
        ...
    
    @classmethod
    @property
    def CZECH(cls) -> CountryCode:
        '''Czech Republic'''
        ...
    
    @classmethod
    @property
    def TAIWAN(cls) -> CountryCode:
        '''Taiwan'''
        ...
    
    @classmethod
    @property
    def LEBANON(cls) -> CountryCode:
        '''Lebanon'''
        ...
    
    @classmethod
    @property
    def JORDAN(cls) -> CountryCode:
        '''Jordan'''
        ...
    
    @classmethod
    @property
    def SYRIA(cls) -> CountryCode:
        '''Syria'''
        ...
    
    @classmethod
    @property
    def IRAQ(cls) -> CountryCode:
        '''Iraq'''
        ...
    
    @classmethod
    @property
    def KUWAIT(cls) -> CountryCode:
        '''Kuwait'''
        ...
    
    @classmethod
    @property
    def SAUDI(cls) -> CountryCode:
        '''Saudi Arabia'''
        ...
    
    @classmethod
    @property
    def UNITED_ARAB_EMIRATES(cls) -> CountryCode:
        '''United Arab Emirates'''
        ...
    
    @classmethod
    @property
    def ISRAEL(cls) -> CountryCode:
        '''Israel'''
        ...
    
    @classmethod
    @property
    def QATAR(cls) -> CountryCode:
        '''Qatar'''
        ...
    
    @classmethod
    @property
    def IRAN(cls) -> CountryCode:
        '''Iran'''
        ...
    
    ...

class DataBarAxisPosition:
    '''Specifies the axis position for a range of cells with conditional formatting as data bars.'''
    
    @classmethod
    @property
    def AUTOMATIC(cls) -> DataBarAxisPosition:
        '''Display the axis at a variable position based on the ratio of the minimum negative value to the maximum positive value in the range.
        Positive values are displayed in a left-to-right direction.
        Negative values are displayed in a right-to-left direction.
        When all values are positive or all values are negative, no axis is displayed.'''
        ...
    
    @classmethod
    @property
    def MIDPOINT(cls) -> DataBarAxisPosition:
        '''Display the axis at the midpoint of the cell regardless of the set of values in the range.
        Positive values are displayed in a left-to-right direction.
        Negative values are displayed in a right-to-left direction.'''
        ...
    
    @classmethod
    @property
    def NONE(cls) -> DataBarAxisPosition:
        '''No axis is displayed, and both positive and negative values are displayed in the left-to-right direction.'''
        ...
    
    ...

class DataBarBorderType:
    '''Specifies the border type of a data bar.'''
    
    @classmethod
    @property
    def NONE(cls) -> DataBarBorderType:
        '''The data bar has no border.'''
        ...
    
    @classmethod
    @property
    def SOLID(cls) -> DataBarBorderType:
        '''The data bar has a solid border.'''
        ...
    
    ...

class DataBarFillType:
    '''Specifies how a data bar is filled with color.'''
    
    @classmethod
    @property
    def SOLID(cls) -> DataBarFillType:
        '''The data bar is filled with solid color.'''
        ...
    
    @classmethod
    @property
    def GRADIENT(cls) -> DataBarFillType:
        '''The data bar is filled with a color gradient.'''
        ...
    
    ...

class DataBarNegativeColorType:
    '''Specifies whether to use the same border and fill color as positive data bars.'''
    
    @classmethod
    @property
    def COLOR(cls) -> DataBarNegativeColorType:
        '''Use the color specified in the Negative Value and Axis Setting dialog box
        or by using the ColorType and BorderColorType properties of the NegativeBarFormat object.'''
        ...
    
    @classmethod
    @property
    def SAME_AS_POSITIVE(cls) -> DataBarNegativeColorType:
        '''Use the same color as positive data bars.'''
        ...
    
    ...

class DateTimeGroupingType:
    '''Specifies how to group dateTime values.'''
    
    @classmethod
    @property
    def DAY(cls) -> DateTimeGroupingType:
        '''Group by day.'''
        ...
    
    @classmethod
    @property
    def HOUR(cls) -> DateTimeGroupingType:
        '''Group by hour.'''
        ...
    
    @classmethod
    @property
    def MINUTE(cls) -> DateTimeGroupingType:
        '''Group by Minute.'''
        ...
    
    @classmethod
    @property
    def MONTH(cls) -> DateTimeGroupingType:
        '''Group by Month.'''
        ...
    
    @classmethod
    @property
    def SECOND(cls) -> DateTimeGroupingType:
        '''Group by Second.'''
        ...
    
    @classmethod
    @property
    def YEAR(cls) -> DateTimeGroupingType:
        '''Group by Year.'''
        ...
    
    ...

class DefaultEditLanguage:
    '''Represents the default edit language.'''
    
    @classmethod
    @property
    def AUTO(cls) -> DefaultEditLanguage:
        '''Represents auto detecting edit language according to the text itself.'''
        ...
    
    @classmethod
    @property
    def ENGLISH(cls) -> DefaultEditLanguage:
        '''Represents English language.'''
        ...
    
    @classmethod
    @property
    def CJK(cls) -> DefaultEditLanguage:
        '''Represents Chinese, Japanese, Korean language.'''
        ...
    
    ...

class DirectoryType:
    '''Represents the directory  type of the file name.'''
    
    @classmethod
    @property
    def VOLUME(cls) -> DirectoryType:
        '''Represents an MS-DOS drive letter. It is followed by the drive letter.
        Or UNC file names, such as \\server\share\myfile.xls'''
        ...
    
    @classmethod
    @property
    def SAME_VOLUME(cls) -> DirectoryType:
        '''Indicates that the source workbook is on the same drive as the dependent workbook (the drive letter is omitted)'''
        ...
    
    @classmethod
    @property
    def DOWN_DIRECTORY(cls) -> DirectoryType:
        '''Indicates that the source workbook is in a subdirectory of the current directory.'''
        ...
    
    @classmethod
    @property
    def UP_DIRECTORY(cls) -> DirectoryType:
        '''Indicates that the source workbook is in the parent directory of the current directory.'''
        ...
    
    ...

class DisplayDrawingObjects:
    '''Represents whether and how to show objects in the workbook.'''
    
    @classmethod
    @property
    def DISPLAY_SHAPES(cls) -> DisplayDrawingObjects:
        '''Show all objects'''
        ...
    
    @classmethod
    @property
    def PLACEHOLDERS(cls) -> DisplayDrawingObjects:
        '''Show placeholders'''
        ...
    
    @classmethod
    @property
    def HIDE(cls) -> DisplayDrawingObjects:
        '''Hide all shapes.'''
        ...
    
    ...

class DynamicFilterType:
    '''Dynamic filter type.'''
    
    @classmethod
    @property
    def ABOVE_AVERAGE(cls) -> DynamicFilterType:
        '''Shows values that are above average.'''
        ...
    
    @classmethod
    @property
    def BELOW_AVERAGE(cls) -> DynamicFilterType:
        '''Shows values that are below average.'''
        ...
    
    @classmethod
    @property
    def LAST_MONTH(cls) -> DynamicFilterType:
        '''Shows last month's dates.'''
        ...
    
    @classmethod
    @property
    def LAST_QUARTER(cls) -> DynamicFilterType:
        '''Shows last quarter's dates.'''
        ...
    
    @classmethod
    @property
    def LAST_WEEK(cls) -> DynamicFilterType:
        '''Shows last week's dates.'''
        ...
    
    @classmethod
    @property
    def LAST_YEAR(cls) -> DynamicFilterType:
        '''Shows last year's dates.'''
        ...
    
    @classmethod
    @property
    def JANUARY(cls) -> DynamicFilterType:
        '''Shows the dates that are in January, regardless of year.'''
        ...
    
    @classmethod
    @property
    def OCTOBER(cls) -> DynamicFilterType:
        '''Shows the dates that are in October, regardless of year.'''
        ...
    
    @classmethod
    @property
    def NOVEMBER(cls) -> DynamicFilterType:
        '''Shows the dates that are in November, regardless of year.'''
        ...
    
    @classmethod
    @property
    def DECEMBER(cls) -> DynamicFilterType:
        '''Shows the dates that are in December, regardless of year.'''
        ...
    
    @classmethod
    @property
    def FEBRUARY(cls) -> DynamicFilterType:
        '''Shows the dates that are in February, regardless of year.'''
        ...
    
    @classmethod
    @property
    def MARCH(cls) -> DynamicFilterType:
        '''Shows the dates that are in March, regardless of year.'''
        ...
    
    @classmethod
    @property
    def APRIL(cls) -> DynamicFilterType:
        '''Shows the dates that are in April, regardless of year.'''
        ...
    
    @classmethod
    @property
    def MAY(cls) -> DynamicFilterType:
        '''Shows the dates that are in May, regardless of year.'''
        ...
    
    @classmethod
    @property
    def JUNE(cls) -> DynamicFilterType:
        '''Shows the dates that are in June, regardless of year.'''
        ...
    
    @classmethod
    @property
    def JULY(cls) -> DynamicFilterType:
        '''Shows the dates that are in July, regardless of year.'''
        ...
    
    @classmethod
    @property
    def AUGUST(cls) -> DynamicFilterType:
        '''Shows the dates that are in August, regardless of year.'''
        ...
    
    @classmethod
    @property
    def SEPTEMBER(cls) -> DynamicFilterType:
        '''Shows the dates that are in September, regardless of year.'''
        ...
    
    @classmethod
    @property
    def NEXT_MONTH(cls) -> DynamicFilterType:
        '''Shows next month's dates.'''
        ...
    
    @classmethod
    @property
    def NEXT_QUARTER(cls) -> DynamicFilterType:
        '''Shows next quarter's dates.'''
        ...
    
    @classmethod
    @property
    def NEXT_WEEK(cls) -> DynamicFilterType:
        '''Shows next week's dates.'''
        ...
    
    @classmethod
    @property
    def NEXT_YEAR(cls) -> DynamicFilterType:
        '''Shows next year's dates.'''
        ...
    
    @classmethod
    @property
    def NONE(cls) -> DynamicFilterType:
        '''None.'''
        ...
    
    @classmethod
    @property
    def QUARTER1(cls) -> DynamicFilterType:
        '''Shows the dates that are in the 1st quarter, regardless of year.'''
        ...
    
    @classmethod
    @property
    def QUARTER2(cls) -> DynamicFilterType:
        '''Shows the dates that are in the 2nd quarter, regardless of year.'''
        ...
    
    @classmethod
    @property
    def QUARTER3(cls) -> DynamicFilterType:
        '''Shows the dates that are in the 3rd quarter, regardless of year.'''
        ...
    
    @classmethod
    @property
    def QUARTER4(cls) -> DynamicFilterType:
        '''Shows the dates that are in the 4th quarter, regardless of year.'''
        ...
    
    @classmethod
    @property
    def THIS_MONTH(cls) -> DynamicFilterType:
        '''Shows this month's dates.'''
        ...
    
    @classmethod
    @property
    def THIS_QUARTER(cls) -> DynamicFilterType:
        '''Shows this quarter's dates.'''
        ...
    
    @classmethod
    @property
    def THIS_WEEK(cls) -> DynamicFilterType:
        '''Shows this week's dates.'''
        ...
    
    @classmethod
    @property
    def THIS_YEAR(cls) -> DynamicFilterType:
        '''Shows this year's dates.'''
        ...
    
    @classmethod
    @property
    def TODAY(cls) -> DynamicFilterType:
        '''Shows today's dates.'''
        ...
    
    @classmethod
    @property
    def TOMORROW(cls) -> DynamicFilterType:
        '''Shows tomorrow's dates.'''
        ...
    
    @classmethod
    @property
    def YEAR_TO_DATE(cls) -> DynamicFilterType:
        '''Shows the dates between the beginning of the year and today, inclusive.'''
        ...
    
    @classmethod
    @property
    def YESTERDAY(cls) -> DynamicFilterType:
        '''Shows yesterday's dates.'''
        ...
    
    ...

class EmfRenderSetting:
    '''Setting for rendering Emf metafile.'''
    
    @classmethod
    @property
    def EMF_ONLY(cls) -> EmfRenderSetting:
        '''Only rendering Emf records.'''
        ...
    
    @classmethod
    @property
    def EMF_PLUS_PREFER(cls) -> EmfRenderSetting:
        '''Prefer rendering EmfPlus records.'''
        ...
    
    ...

class EncryptionType:
    '''Encryption Type.
    Only used by excel2003.
    We will encrypt 2007/2010 workbook using SHA AES the same as Excel does, and this EncryptionType will be ignored.'''
    
    @classmethod
    @property
    def XOR(cls) -> EncryptionType:
        ...
    
    @classmethod
    @property
    def COMPATIBLE(cls) -> EncryptionType:
        '''Office 97/2000 compatible.'''
        ...
    
    @classmethod
    @property
    def ENHANCED_CRYPTOGRAPHIC_PROVIDER_V1(cls) -> EncryptionType:
        ...
    
    @classmethod
    @property
    def STRONG_CRYPTOGRAPHIC_PROVIDER(cls) -> EncryptionType:
        ...
    
    ...

class ErrorCheckType:
    '''Represents all error check type.'''
    
    @classmethod
    @property
    def CALC(cls) -> ErrorCheckType:
        '''check for calculation errors'''
        ...
    
    @classmethod
    @property
    def EMPTY_CELL_REF(cls) -> ErrorCheckType:
        '''check for references to empty cells'''
        ...
    
    @classmethod
    @property
    def TEXT_NUMBER(cls) -> ErrorCheckType:
        '''check the format of numeric values'''
        ...
    
    @classmethod
    @property
    def INCONSIST_RANGE(cls) -> ErrorCheckType:
        '''check formulas with references to less than the entirety
        of a range containing continuous data'''
        ...
    
    @classmethod
    @property
    def INCONSIST_FORMULA(cls) -> ErrorCheckType:
        '''check formulas that are inconsistent with formulas in neighboring cells.'''
        ...
    
    @classmethod
    @property
    def TEXT_DATE(cls) -> ErrorCheckType:
        '''check the format of date/time values'''
        ...
    
    @classmethod
    @property
    def UNPROCTED_FORMULA(cls) -> ErrorCheckType:
        '''check for unprotected formulas'''
        ...
    
    @classmethod
    @property
    def VALIDATION(cls) -> ErrorCheckType:
        '''whether to perform data validation'''
        ...
    
    @classmethod
    @property
    def CALCULATED_COLUMN(cls) -> ErrorCheckType:
        '''Ignore errors when cells contain a value different from a calculated column formula.'''
        ...
    
    ...

class ExceptionType:
    '''Represents custom exception type code.'''
    
    @classmethod
    @property
    def CHART(cls) -> ExceptionType:
        '''Invalid chart setting.'''
        ...
    
    @classmethod
    @property
    def DATA_TYPE(cls) -> ExceptionType:
        '''Invalid data type setting.'''
        ...
    
    @classmethod
    @property
    def DATA_VALIDATION(cls) -> ExceptionType:
        '''Invalid data validation setting.'''
        ...
    
    @classmethod
    @property
    def CONDITIONAL_FORMATTING(cls) -> ExceptionType:
        '''Invalid data validation setting.'''
        ...
    
    @classmethod
    @property
    def FILE_FORMAT(cls) -> ExceptionType:
        '''Invalid file format.'''
        ...
    
    @classmethod
    @property
    def FORMULA(cls) -> ExceptionType:
        '''Invalid formula.'''
        ...
    
    @classmethod
    @property
    def INVALID_DATA(cls) -> ExceptionType:
        '''Invalid data.'''
        ...
    
    @classmethod
    @property
    def INVALID_OPERATOR(cls) -> ExceptionType:
        '''Invalid operator.'''
        ...
    
    @classmethod
    @property
    def INCORRECT_PASSWORD(cls) -> ExceptionType:
        '''Incorrect password.'''
        ...
    
    @classmethod
    @property
    def LICENSE(cls) -> ExceptionType:
        '''License related errors.'''
        ...
    
    @classmethod
    @property
    def LIMITATION(cls) -> ExceptionType:
        '''Out of MS Excel limitation error.'''
        ...
    
    @classmethod
    @property
    def PAGE_SETUP(cls) -> ExceptionType:
        '''Invalid page setup setting.'''
        ...
    
    @classmethod
    @property
    def PIVOT_TABLE(cls) -> ExceptionType:
        '''Invalid pivotTable setting.'''
        ...
    
    @classmethod
    @property
    def SHAPE(cls) -> ExceptionType:
        '''Invalid drawing object setting.'''
        ...
    
    @classmethod
    @property
    def SPARKLINE(cls) -> ExceptionType:
        '''Invalid sparkline object setting.'''
        ...
    
    @classmethod
    @property
    def SHEET_NAME(cls) -> ExceptionType:
        '''Invalid worksheet name.'''
        ...
    
    @classmethod
    @property
    def SHEET_TYPE(cls) -> ExceptionType:
        '''Invalid worksheet type.'''
        ...
    
    @classmethod
    @property
    def INTERRUPTED(cls) -> ExceptionType:
        '''The process is interrupted.'''
        ...
    
    @classmethod
    @property
    def IO(cls) -> ExceptionType:
        '''The file is invalid.'''
        ...
    
    @classmethod
    @property
    def PERMISSION(cls) -> ExceptionType:
        '''Permission is required to open this file.'''
        ...
    
    @classmethod
    @property
    def UNSUPPORTED_FEATURE(cls) -> ExceptionType:
        '''Unsupported feature.'''
        ...
    
    @classmethod
    @property
    def UNSUPPORTED_STREAM(cls) -> ExceptionType:
        '''Unsupported stream to be opened.'''
        ...
    
    @classmethod
    @property
    def UNDISCLOSED_INFORMATION(cls) -> ExceptionType:
        '''Files contains some undisclosed information.'''
        ...
    
    @classmethod
    @property
    def FILE_CORRUPTED(cls) -> ExceptionType:
        '''File content is corrupted.'''
        ...
    
    ...

class ExternalLinkType:
    '''Represents the type of external link.'''
    
    @classmethod
    @property
    def DDE_LINK(cls) -> ExternalLinkType:
        '''Represents the DDE link.'''
        ...
    
    @classmethod
    @property
    def EXTERNAL(cls) -> ExternalLinkType:
        '''Represents external link.'''
        ...
    
    ...

class FileFormatType:
    '''Represents the file format types.'''
    
    @classmethod
    @property
    def CSV(cls) -> FileFormatType:
        '''Comma-Separated Values(CSV) text file.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.FileFormatType.CSV` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def XLSX(cls) -> FileFormatType:
        '''Office Open XML SpreadsheetML file (macro-free).'''
        ...
    
    @classmethod
    @property
    def XLSM(cls) -> FileFormatType:
        '''Office Open XML SpreadsheetML Macro-Enabled file.'''
        ...
    
    @classmethod
    @property
    def XLTX(cls) -> FileFormatType:
        '''Office Open XML SpreadsheetML Template (macro-free).'''
        ...
    
    @classmethod
    @property
    def XLTM(cls) -> FileFormatType:
        '''Office Open XML SpreadsheetML Macro-Enabled Template.'''
        ...
    
    @classmethod
    @property
    def XLAM(cls) -> FileFormatType:
        '''Office Open XML SpreadsheetML addinMacro-Enabled file.'''
        ...
    
    @classmethod
    @property
    def TSV(cls) -> FileFormatType:
        '''Tab-Separated Values(TSV) text file.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.FileFormatType.TSV` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def TAB_DELIMITED(cls) -> FileFormatType:
        '''Tab-Separated Values(TSV) text file, same with :py:attr:`aspose.cells.FileFormatType.TSV`.'''
        ...
    
    @classmethod
    @property
    def HTML(cls) -> FileFormatType:
        '''HTML format.'''
        ...
    
    @classmethod
    @property
    def M_HTML(cls) -> FileFormatType:
        '''MHTML (Web archive) format.'''
        ...
    
    @classmethod
    @property
    def ODS(cls) -> FileFormatType:
        '''Open Document Sheet(ODS) file.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.FileFormatType.ODS` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def EXCEL_97_TO_2003(cls) -> FileFormatType:
        '''Excel97-2003 spreadsheet file.'''
        ...
    
    @classmethod
    @property
    def SPREADSHEET_ML(cls) -> FileFormatType:
        '''Excel 2003 XML Data file.'''
        ...
    
    @classmethod
    @property
    def EXCEL_2003XML(cls) -> FileFormatType:
        '''Excel 2003 XML Data file.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.FileFormatType.SPREADSHEET_ML` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def XLSB(cls) -> FileFormatType:
        '''The Excel Binary File Format (.xlsb)'''
        ...
    
    @classmethod
    @property
    def UNKNOWN(cls) -> FileFormatType:
        '''Represents unrecognized format, cannot be loaded.'''
        ...
    
    @classmethod
    @property
    def PDF(cls) -> FileFormatType:
        '''PDF (Adobe Portable Document) format.'''
        ...
    
    @classmethod
    @property
    def XPS(cls) -> FileFormatType:
        '''XPS (XML Paper Specification) format.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.FileFormatType.XPS` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def TIFF(cls) -> FileFormatType:
        '''Represents a TIFF file.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.FileFormatType.TIFF` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def SVG(cls) -> FileFormatType:
        '''SVG file.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.FileFormatType.SVG` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def EXCEL95(cls) -> FileFormatType:
        '''Represents an Excel95 xls file.'''
        ...
    
    @classmethod
    @property
    def EXCEL4(cls) -> FileFormatType:
        '''Represents an Excel4.0 xls file.'''
        ...
    
    @classmethod
    @property
    def EXCEL3(cls) -> FileFormatType:
        '''Represents an Excel3.0 xls file.'''
        ...
    
    @classmethod
    @property
    def EXCEL2(cls) -> FileFormatType:
        '''Represents an Excel2.1 xls file.'''
        ...
    
    @classmethod
    @property
    def PPTX(cls) -> FileFormatType:
        '''Represents a pptx file.'''
        ...
    
    @classmethod
    @property
    def DOCX(cls) -> FileFormatType:
        '''Represents a docx file.'''
        ...
    
    @classmethod
    @property
    def DIF(cls) -> FileFormatType:
        '''Data Interchange Format.'''
        ...
    
    @classmethod
    @property
    def DOC(cls) -> FileFormatType:
        '''Represents a doc file.'''
        ...
    
    @classmethod
    @property
    def PPT(cls) -> FileFormatType:
        '''Represents a ppt file.'''
        ...
    
    @classmethod
    @property
    def MAPI_MESSAGE(cls) -> FileFormatType:
        '''Represents a email file.'''
        ...
    
    @classmethod
    @property
    def MS_EQUATION(cls) -> FileFormatType:
        '''Represents the MS Equation 3.0 object.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.FileFormatType.MS_EQUATION` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def OLE_10_NATIVE(cls) -> FileFormatType:
        '''Represents the embedded native object.'''
        ...
    
    @classmethod
    @property
    def VSD(cls) -> FileFormatType:
        '''Represents MS Visio VSD binary format.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.FileFormatType.VSD` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def VSDX(cls) -> FileFormatType:
        '''Represents MS Visio 2013 VSDX file format.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.FileFormatType.VSDX` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def DOCM(cls) -> FileFormatType:
        '''Represents a docm file.'''
        ...
    
    @classmethod
    @property
    def DOTX(cls) -> FileFormatType:
        '''Represents a dotx file.'''
        ...
    
    @classmethod
    @property
    def DOTM(cls) -> FileFormatType:
        '''Represents a dotm file.'''
        ...
    
    @classmethod
    @property
    def PPTM(cls) -> FileFormatType:
        '''Represents a pptm file.'''
        ...
    
    @classmethod
    @property
    def POTX(cls) -> FileFormatType:
        '''Represents a Potx file.'''
        ...
    
    @classmethod
    @property
    def POTM(cls) -> FileFormatType:
        '''Represents a Potm file.'''
        ...
    
    @classmethod
    @property
    def PPSX(cls) -> FileFormatType:
        '''Represents a ppsx file.'''
        ...
    
    @classmethod
    @property
    def PPSM(cls) -> FileFormatType:
        '''Represents a ppsm file.'''
        ...
    
    @classmethod
    @property
    def OOXML(cls) -> FileFormatType:
        '''Represents office open xml file(such as xlsx, docx,pptx, etc).'''
        ...
    
    @classmethod
    @property
    def ODT(cls) -> FileFormatType:
        '''Represents an ODT file.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.FileFormatType.ODT` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def ODP(cls) -> FileFormatType:
        '''Represents an ODP file.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.FileFormatType.ODP` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def ODF(cls) -> FileFormatType:
        '''Represents an ODF file.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.FileFormatType.ODF` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def ODG(cls) -> FileFormatType:
        '''Represents an ODG file.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.FileFormatType.ODG` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def XML(cls) -> FileFormatType:
        '''Represents a simple xml file.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.FileFormatType.XML` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def XLT(cls) -> FileFormatType:
        '''Excel97-2003 spreadsheet template.'''
        ...
    
    @classmethod
    @property
    def OTT(cls) -> FileFormatType:
        '''Represents an OTT file.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.FileFormatType.OTT` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def BMP(cls) -> FileFormatType:
        '''Represents an BMP file.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.FileFormatType.BMP` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def OTS(cls) -> FileFormatType:
        '''Represents an OTS file.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.FileFormatType.OTS` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def NUMBERS(cls) -> FileFormatType:
        '''Represents Numbers 9.0 file format by Apple Inc.'''
        ...
    
    @classmethod
    @property
    def NUMBERS09(cls) -> FileFormatType:
        '''Represents Numbers 9.0 file format by Apple Inc.'''
        ...
    
    @classmethod
    @property
    def MARKDOWN(cls) -> FileFormatType:
        '''Represents markdown document.'''
        ...
    
    @classmethod
    @property
    def GRAPH_CHART(cls) -> FileFormatType:
        '''Represents embedded graph chart.'''
        ...
    
    @classmethod
    @property
    def FODS(cls) -> FileFormatType:
        '''Represents OpenDocument Flat XML Spreadsheet (.fods) file format.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.FileFormatType.FODS` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def SXC(cls) -> FileFormatType:
        '''Represents StarOffice Calc Spreadsheet (.sxc) file format.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.FileFormatType.SXC` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def OTP(cls) -> FileFormatType:
        '''Represents a OTP file.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.FileFormatType.OTP` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def NUMBERS35(cls) -> FileFormatType:
        '''Represents Numbers 3.5 file format since 2014 by Apple Inc'''
        ...
    
    @classmethod
    @property
    def EMF(cls) -> FileFormatType:
        '''Windows Enhanced Metafile.'''
        ...
    
    @classmethod
    @property
    def WMF(cls) -> FileFormatType:
        '''Windows Metafile.'''
        ...
    
    @classmethod
    @property
    def JPG(cls) -> FileFormatType:
        '''JPEG JFIF.'''
        ...
    
    @classmethod
    @property
    def PNG(cls) -> FileFormatType:
        '''Portable Network Graphics.'''
        ...
    
    @classmethod
    @property
    def GIF(cls) -> FileFormatType:
        '''Gif'''
        ...
    
    @classmethod
    @property
    def JSON(cls) -> FileFormatType:
        '''Json'''
        ...
    
    @classmethod
    @property
    def SQL_SCRIPT(cls) -> FileFormatType:
        '''Sql'''
        ...
    
    @classmethod
    @property
    def X_HTML(cls) -> FileFormatType:
        '''Rrepesents XHtml file.'''
        ...
    
    ...

class FilterOperatorType:
    '''Custom Filter operator type.'''
    
    @classmethod
    @property
    def LESS_OR_EQUAL(cls) -> FilterOperatorType:
        '''Represents LessOrEqual operator.'''
        ...
    
    @classmethod
    @property
    def LESS_THAN(cls) -> FilterOperatorType:
        '''Represents LessThan operator.'''
        ...
    
    @classmethod
    @property
    def EQUAL(cls) -> FilterOperatorType:
        '''Represents Equal operator.'''
        ...
    
    @classmethod
    @property
    def GREATER_THAN(cls) -> FilterOperatorType:
        '''Represents GreaterThan operator.'''
        ...
    
    @classmethod
    @property
    def NOT_EQUAL(cls) -> FilterOperatorType:
        '''Represents NotEqual operator.'''
        ...
    
    @classmethod
    @property
    def GREATER_OR_EQUAL(cls) -> FilterOperatorType:
        '''Represents GreaterOrEqual operator.'''
        ...
    
    @classmethod
    @property
    def NONE(cls) -> FilterOperatorType:
        '''Represents no comparison.'''
        ...
    
    @classmethod
    @property
    def BEGINS_WITH(cls) -> FilterOperatorType:
        '''Begins with the text.'''
        ...
    
    @classmethod
    @property
    def ENDS_WITH(cls) -> FilterOperatorType:
        '''Ends with the text.'''
        ...
    
    @classmethod
    @property
    def CONTAINS(cls) -> FilterOperatorType:
        '''Contains the text.'''
        ...
    
    @classmethod
    @property
    def NOT_CONTAINS(cls) -> FilterOperatorType:
        '''Not contains the text.'''
        ...
    
    ...

class FilterType:
    '''The filter type.'''
    
    @classmethod
    @property
    def COLOR_FILTER(cls) -> FilterType:
        '''Filter by fill color of the cell.'''
        ...
    
    @classmethod
    @property
    def CUSTOM_FILTERS(cls) -> FilterType:
        '''Custom filter type.'''
        ...
    
    @classmethod
    @property
    def DYNAMIC_FILTER(cls) -> FilterType:
        '''Dynamic filter type.'''
        ...
    
    @classmethod
    @property
    def MULTIPLE_FILTERS(cls) -> FilterType:
        '''When multiple values are chosen to filter by, or when a group of date values are chosen to filter by,
        this element groups those criteria together.'''
        ...
    
    @classmethod
    @property
    def ICON_FILTER(cls) -> FilterType:
        '''Filter by icon of conditional formatting.'''
        ...
    
    @classmethod
    @property
    def TOP10(cls) -> FilterType:
        '''Top 10 filter.'''
        ...
    
    @classmethod
    @property
    def NONE(cls) -> FilterType:
        '''No filter.'''
        ...
    
    ...

class FontSchemeType:
    '''Represents the scheme type of the font.'''
    
    @classmethod
    @property
    def NONE(cls) -> FontSchemeType:
        '''None'''
        ...
    
    @classmethod
    @property
    def MAJOR(cls) -> FontSchemeType:
        '''Major scheme.'''
        ...
    
    @classmethod
    @property
    def MINOR(cls) -> FontSchemeType:
        '''Minor scheme.'''
        ...
    
    ...

class FontSourceType:
    '''Specifies the type of a font source.'''
    
    @classmethod
    @property
    def FONT_FILE(cls) -> FontSourceType:
        '''represents single font file.'''
        ...
    
    @classmethod
    @property
    def FONTS_FOLDER(cls) -> FontSourceType:
        '''represents folder with font files.'''
        ...
    
    @classmethod
    @property
    def MEMORY_FONT(cls) -> FontSourceType:
        '''represents single font in memory.'''
        ...
    
    ...

class FontUnderlineType:
    '''Enumerates the font underline types.'''
    
    @classmethod
    @property
    def NONE(cls) -> FontUnderlineType:
        '''Represents no underline.'''
        ...
    
    @classmethod
    @property
    def SINGLE(cls) -> FontUnderlineType:
        '''Represents single underline.'''
        ...
    
    @classmethod
    @property
    def DOUBLE(cls) -> FontUnderlineType:
        '''Represents double underline.'''
        ...
    
    @classmethod
    @property
    def ACCOUNTING(cls) -> FontUnderlineType:
        '''Represents single accounting underline.'''
        ...
    
    @classmethod
    @property
    def DOUBLE_ACCOUNTING(cls) -> FontUnderlineType:
        '''Represents double accounting underline.'''
        ...
    
    @classmethod
    @property
    def DASH(cls) -> FontUnderlineType:
        '''Represents Dashed Underline'''
        ...
    
    @classmethod
    @property
    def DASH_DOT_DOT_HEAVY(cls) -> FontUnderlineType:
        '''Represents Thick Dash-Dot-Dot Underline'''
        ...
    
    @classmethod
    @property
    def DASH_DOT_HEAVY(cls) -> FontUnderlineType:
        '''Represents Thick Dash-Dot Underline'''
        ...
    
    @classmethod
    @property
    def DASHED_HEAVY(cls) -> FontUnderlineType:
        '''Represents Thick Dashed Underline'''
        ...
    
    @classmethod
    @property
    def DASH_LONG(cls) -> FontUnderlineType:
        '''Represents Long Dashed Underline'''
        ...
    
    @classmethod
    @property
    def DASH_LONG_HEAVY(cls) -> FontUnderlineType:
        '''Represents Thick Long Dashed Underline'''
        ...
    
    @classmethod
    @property
    def DOT_DASH(cls) -> FontUnderlineType:
        '''Represents Dash-Dot Underline'''
        ...
    
    @classmethod
    @property
    def DOT_DOT_DASH(cls) -> FontUnderlineType:
        '''Represents Dash-Dot-Dot Underline'''
        ...
    
    @classmethod
    @property
    def DOTTED(cls) -> FontUnderlineType:
        '''Represents Dotted Underline'''
        ...
    
    @classmethod
    @property
    def DOTTED_HEAVY(cls) -> FontUnderlineType:
        '''Represents Thick Dotted Underline'''
        ...
    
    @classmethod
    @property
    def HEAVY(cls) -> FontUnderlineType:
        '''Represents Thick Underline'''
        ...
    
    @classmethod
    @property
    def WAVE(cls) -> FontUnderlineType:
        '''Represents Wave Underline'''
        ...
    
    @classmethod
    @property
    def WAVY_DOUBLE(cls) -> FontUnderlineType:
        '''Represents Double Wave Underline'''
        ...
    
    @classmethod
    @property
    def WAVY_HEAVY(cls) -> FontUnderlineType:
        '''Represents Heavy Wave Underline'''
        ...
    
    @classmethod
    @property
    def WORDS(cls) -> FontUnderlineType:
        '''Represents Underline Non-Space Characters Only'''
        ...
    
    ...

class FormatConditionType:
    '''Conditional format rule type.'''
    
    @classmethod
    @property
    def CELL_VALUE(cls) -> FormatConditionType:
        '''This conditional formatting rule compares a cell value
        to a formula calculated result, using an operator.'''
        ...
    
    @classmethod
    @property
    def EXPRESSION(cls) -> FormatConditionType:
        '''This conditional formatting rule contains a formula to
        evaluate. When the formula result is true, the cell is
        highlighted.'''
        ...
    
    @classmethod
    @property
    def COLOR_SCALE(cls) -> FormatConditionType:
        '''This conditional formatting rule creates a gradated
        color scale on the cells.'''
        ...
    
    @classmethod
    @property
    def DATA_BAR(cls) -> FormatConditionType:
        '''This conditional formatting rule displays a gradated
        data bar in the range of cells.'''
        ...
    
    @classmethod
    @property
    def ICON_SET(cls) -> FormatConditionType:
        '''This conditional formatting rule applies icons to cells
        according to their values.'''
        ...
    
    @classmethod
    @property
    def TOP10(cls) -> FormatConditionType:
        '''This conditional formatting rule highlights cells whose
        values fall in the top N or bottom N bracket, as
        specified.'''
        ...
    
    @classmethod
    @property
    def UNIQUE_VALUES(cls) -> FormatConditionType:
        '''This conditional formatting rule highlights unique
        values in the range.'''
        ...
    
    @classmethod
    @property
    def DUPLICATE_VALUES(cls) -> FormatConditionType:
        '''This conditional formatting rule highlights duplicated
        values.'''
        ...
    
    @classmethod
    @property
    def CONTAINS_TEXT(cls) -> FormatConditionType:
        '''This conditional formatting rule highlights cells
        containing given text. Equivalent to using the SEARCH()
        sheet function to determine whether the cell contains
        the text.'''
        ...
    
    @classmethod
    @property
    def NOT_CONTAINS_TEXT(cls) -> FormatConditionType:
        '''This conditional formatting rule highlights cells that
        do not contain given text. Equivalent of using SEARCH()
        sheet function to determine whether the cell contains
        the text or not.'''
        ...
    
    @classmethod
    @property
    def BEGINS_WITH(cls) -> FormatConditionType:
        '''This conditional formatting rule highlights cells in the
        range that begin with the given text. Equivalent to
        using the LEFT() sheet function and comparing values.'''
        ...
    
    @classmethod
    @property
    def ENDS_WITH(cls) -> FormatConditionType:
        '''This conditional formatting rule highlights cells ending
        with given text. Equivalent to using the RIGHT() sheet
        function and comparing values.'''
        ...
    
    @classmethod
    @property
    def CONTAINS_BLANKS(cls) -> FormatConditionType:
        '''This conditional formatting rule highlights cells that
        are completely blank. Equivalent of using LEN(TRIM()).
        This means that if the cell contains only characters
        that TRIM() would remove, then it is considered blank.
        An empty cell is also considered blank.'''
        ...
    
    @classmethod
    @property
    def NOT_CONTAINS_BLANKS(cls) -> FormatConditionType:
        '''This conditional formatting rule highlights cells that
        are not blank. Equivalent of using LEN(TRIM()). This
        means that if the cell contains only characters that
        TRIM() would remove, then it is considered blank. An
        empty cell is also considered blank.'''
        ...
    
    @classmethod
    @property
    def CONTAINS_ERRORS(cls) -> FormatConditionType:
        '''This conditional formatting rule highlights cells with
        formula errors. Equivalent to using ISERROR() sheet
        function to determine if there is a formula error.'''
        ...
    
    @classmethod
    @property
    def NOT_CONTAINS_ERRORS(cls) -> FormatConditionType:
        '''This conditional formatting rule highlights cells
        without formula errors. Equivalent to using ISERROR()
        sheet function to determine if there is a formula error.'''
        ...
    
    @classmethod
    @property
    def TIME_PERIOD(cls) -> FormatConditionType:
        '''This conditional formatting rule highlights cells
        containing dates in the specified time period. The
        underlying value of the cell is evaluated, therefore the
        cell does not need to be formatted as a date to be
        evaluated. For example, with a cell containing the
        value 38913 the conditional format shall be applied if
        the rule requires a value of 7/14/2006.'''
        ...
    
    @classmethod
    @property
    def ABOVE_AVERAGE(cls) -> FormatConditionType:
        '''This conditional formatting rule highlights cells that
        are above or below the average for all values in the
        range.'''
        ...
    
    ...

class FormatConditionValueType:
    '''Condition value type.'''
    
    @classmethod
    @property
    def FORMULA(cls) -> FormatConditionValueType:
        '''The minimum/ midpoint / maximum value for the
        gradient is determined by a formula.'''
        ...
    
    @classmethod
    @property
    def MAX(cls) -> FormatConditionValueType:
        '''Indicates that the maximum value in the range shall be
        used as the maximum value for the gradient.'''
        ...
    
    @classmethod
    @property
    def MIN(cls) -> FormatConditionValueType:
        '''Indicates that the minimum value in the range shall be
        used as the minimum value for the gradient.'''
        ...
    
    @classmethod
    @property
    def NUMBER(cls) -> FormatConditionValueType:
        '''Indicates that the minimum / midpoint / maximum
        value for the gradient is specified by a constant
        numeric value.'''
        ...
    
    @classmethod
    @property
    def PERCENT(cls) -> FormatConditionValueType:
        '''Value indicates a percentage between the minimum
        and maximum values in the range shall be used as the
        minimum / midpoint / maximum value for the gradient.'''
        ...
    
    @classmethod
    @property
    def PERCENTILE(cls) -> FormatConditionValueType:
        '''Value indicates a percentile ranking in the range shall
        be used as the minimum / midpoint / maximum value
        for the gradient.'''
        ...
    
    @classmethod
    @property
    def AUTOMATIC_MAX(cls) -> FormatConditionValueType:
        '''Indicates that the Automatic maximum value in the range shall be
        used as the Automatic maximum value for the gradient.'''
        ...
    
    @classmethod
    @property
    def AUTOMATIC_MIN(cls) -> FormatConditionValueType:
        '''Indicates that the Automatic minimum value in the range shall be
        used as the Automatic minimum value for the gradient.'''
        ...
    
    ...

class GridlineType:
    '''Enumerates grid line Type.'''
    
    @classmethod
    @property
    def DOTTED(cls) -> GridlineType:
        '''Represents dotted line.'''
        ...
    
    @classmethod
    @property
    def HAIR(cls) -> GridlineType:
        '''Represents hair line.'''
        ...
    
    ...

class HeaderFooterCommandType:
    '''Represents the command type of header and footer.'''
    
    @classmethod
    @property
    def TEXT(cls) -> HeaderFooterCommandType:
        '''The text.'''
        ...
    
    @classmethod
    @property
    def CURRENT_PAGE(cls) -> HeaderFooterCommandType:
        '''Current page number'''
        ...
    
    @classmethod
    @property
    def PAGECOUNT(cls) -> HeaderFooterCommandType:
        '''Page count'''
        ...
    
    @classmethod
    @property
    def CURRENT_DATE(cls) -> HeaderFooterCommandType:
        '''Current date'''
        ...
    
    @classmethod
    @property
    def CURRENT_TIME(cls) -> HeaderFooterCommandType:
        '''Current time'''
        ...
    
    @classmethod
    @property
    def SHEET_NAME(cls) -> HeaderFooterCommandType:
        '''Sheet name'''
        ...
    
    @classmethod
    @property
    def FILE_NAME(cls) -> HeaderFooterCommandType:
        '''File name without path'''
        ...
    
    @classmethod
    @property
    def FILE_PATH(cls) -> HeaderFooterCommandType:
        '''File path without file name'''
        ...
    
    @classmethod
    @property
    def PICTURE(cls) -> HeaderFooterCommandType:
        '''Picture'''
        ...
    
    ...

class HtmlCrossType:
    '''Represents five types of html cross string.'''
    
    @classmethod
    @property
    def DEFAULT(cls) -> HtmlCrossType:
        '''Display like MS Excel,depends on the next cell.
        If the next cell is null,the string will cross,or it will be truncated'''
        ...
    
    @classmethod
    @property
    def MS_EXPORT(cls) -> HtmlCrossType:
        '''Display the string like MS Excel exporting html.'''
        ...
    
    @classmethod
    @property
    def CROSS(cls) -> HtmlCrossType:
        '''Display HTML cross string, this performance for creating large html files will be more than ten times faster than setting the value to Default or FitToCell.'''
        ...
    
    @classmethod
    @property
    def CROSS_HIDE_RIGHT(cls) -> HtmlCrossType:
        '''Display HTML cross string and hide the right string when the texts overlap.'''
        ...
    
    @classmethod
    @property
    def FIT_TO_CELL(cls) -> HtmlCrossType:
        '''Only displaying the string within the width of cell.'''
        ...
    
    ...

class HtmlExportDataOptions:
    '''Represents the options for exporting html data.'''
    
    @classmethod
    @property
    def TABLE(cls) -> HtmlExportDataOptions:
        '''Export file to html which only contains table part.'''
        ...
    
    @classmethod
    @property
    def ALL(cls) -> HtmlExportDataOptions:
        '''Export all the data to html.'''
        ...
    
    ...

class HtmlHiddenColDisplayType:
    '''Represents two types of showing the hidden columns in html.'''
    
    @classmethod
    @property
    def HIDDEN(cls) -> HtmlHiddenColDisplayType:
        '''Hidden the hidden columns in html page.'''
        ...
    
    @classmethod
    @property
    def REMOVE(cls) -> HtmlHiddenColDisplayType:
        '''Remove the hidden columns in html page.'''
        ...
    
    ...

class HtmlHiddenRowDisplayType:
    '''Represents two types of showing the hidden rows in html.'''
    
    @classmethod
    @property
    def HIDDEN(cls) -> HtmlHiddenRowDisplayType:
        '''Hidden the hidden rows in html page.'''
        ...
    
    @classmethod
    @property
    def REMOVE(cls) -> HtmlHiddenRowDisplayType:
        '''Remove the hidden rows in html page.'''
        ...
    
    ...

class HtmlLinkTargetType:
    '''Represents the type of target attribute in HTML ` <>` tag.'''
    
    @classmethod
    @property
    def BLANK(cls) -> HtmlLinkTargetType:
        '''Opens the linked document in a new window or tab'''
        ...
    
    @classmethod
    @property
    def PARENT(cls) -> HtmlLinkTargetType:
        '''Opens the linked document in the parent frame'''
        ...
    
    @classmethod
    @property
    def SELF(cls) -> HtmlLinkTargetType:
        '''Opens the linked document in the same frame as it was clicked (this is default)'''
        ...
    
    @classmethod
    @property
    def TOP(cls) -> HtmlLinkTargetType:
        '''Opens the linked document in the full body of the window'''
        ...
    
    ...

class IconSetType:
    '''Icon set type for conditional formatting.
    The threshold values for triggering the different icons within a set are
    configurable, and the icon order is reversible.'''
    
    @classmethod
    @property
    def ARROWS3(cls) -> IconSetType:
        '''3 arrows icon set.'''
        ...
    
    @classmethod
    @property
    def ARROWS_GRAY3(cls) -> IconSetType:
        '''3 gray arrows icon set.'''
        ...
    
    @classmethod
    @property
    def FLAGS3(cls) -> IconSetType:
        '''3 flags icon set.'''
        ...
    
    @classmethod
    @property
    def SIGNS3(cls) -> IconSetType:
        '''3 signs icon set.'''
        ...
    
    @classmethod
    @property
    def SYMBOLS3(cls) -> IconSetType:
        '''3 symbols icon set (circled).'''
        ...
    
    @classmethod
    @property
    def SYMBOLS32(cls) -> IconSetType:
        '''3 Symbols icon set (uncircled).'''
        ...
    
    @classmethod
    @property
    def TRAFFIC_LIGHTS31(cls) -> IconSetType:
        '''3 traffic lights icon set (unrimmed).'''
        ...
    
    @classmethod
    @property
    def TRAFFIC_LIGHTS32(cls) -> IconSetType:
        '''3 traffic lights icon set with thick black border.'''
        ...
    
    @classmethod
    @property
    def ARROWS4(cls) -> IconSetType:
        '''4 arrows icon set.'''
        ...
    
    @classmethod
    @property
    def ARROWS_GRAY4(cls) -> IconSetType:
        '''4 gray arrows icon set.'''
        ...
    
    @classmethod
    @property
    def RATING4(cls) -> IconSetType:
        '''4 ratings icon set.'''
        ...
    
    @classmethod
    @property
    def RED_TO_BLACK4(cls) -> IconSetType:
        '''4 'red to black' icon set.'''
        ...
    
    @classmethod
    @property
    def TRAFFIC_LIGHTS4(cls) -> IconSetType:
        '''4 traffic lights icon set.'''
        ...
    
    @classmethod
    @property
    def ARROWS5(cls) -> IconSetType:
        '''5 arrows icon set.'''
        ...
    
    @classmethod
    @property
    def ARROWS_GRAY5(cls) -> IconSetType:
        '''5 gray arrows icon set.'''
        ...
    
    @classmethod
    @property
    def QUARTERS5(cls) -> IconSetType:
        '''5 quarters icon set.'''
        ...
    
    @classmethod
    @property
    def RATING5(cls) -> IconSetType:
        '''5 rating icon set.'''
        ...
    
    @classmethod
    @property
    def STARS3(cls) -> IconSetType:
        '''3 stars set'''
        ...
    
    @classmethod
    @property
    def BOXES5(cls) -> IconSetType:
        '''5 boxes set'''
        ...
    
    @classmethod
    @property
    def TRIANGLES3(cls) -> IconSetType:
        '''3 triangles set'''
        ...
    
    @classmethod
    @property
    def NONE(cls) -> IconSetType:
        '''None'''
        ...
    
    @classmethod
    @property
    def CUSTOM_SET(cls) -> IconSetType:
        '''CustomSet.
        This element is read-only.'''
        ...
    
    @classmethod
    @property
    def SMILIES3(cls) -> IconSetType:
        '''3 smilies.
        Only for .ods.'''
        ...
    
    @classmethod
    @property
    def COLOR_SMILIES3(cls) -> IconSetType:
        '''3 color smilies.
        Only for .ods.'''
        ...
    
    ...

class LoadDataFilterOptions:
    '''Represents the options to filter data when loading workbook from template.'''
    
    @classmethod
    @property
    def NONE(cls) -> LoadDataFilterOptions:
        '''Load nothing for sheet data'''
        ...
    
    @classmethod
    @property
    def ALL(cls) -> LoadDataFilterOptions:
        '''Load all'''
        ...
    
    @classmethod
    @property
    def CELL_BLANK(cls) -> LoadDataFilterOptions:
        '''Load cells whose value is blank'''
        ...
    
    @classmethod
    @property
    def CELL_STRING(cls) -> LoadDataFilterOptions:
        '''Load cells whose value is string'''
        ...
    
    @classmethod
    @property
    def CELL_NUMERIC(cls) -> LoadDataFilterOptions:
        '''Load cells whose value is numeric(including datetime)'''
        ...
    
    @classmethod
    @property
    def CELL_ERROR(cls) -> LoadDataFilterOptions:
        '''Load cells whose value is error'''
        ...
    
    @classmethod
    @property
    def CELL_BOOL(cls) -> LoadDataFilterOptions:
        '''Load cells whose value is bool'''
        ...
    
    @classmethod
    @property
    def CELL_VALUE(cls) -> LoadDataFilterOptions:
        '''Load cells value(all value types) only'''
        ...
    
    @classmethod
    @property
    def FORMULA(cls) -> LoadDataFilterOptions:
        '''Load cell formulas.'''
        ...
    
    @classmethod
    @property
    def CELL_DATA(cls) -> LoadDataFilterOptions:
        '''Load cells data including values, formulas and formatting'''
        ...
    
    @classmethod
    @property
    def CHART(cls) -> LoadDataFilterOptions:
        '''Load charts'''
        ...
    
    @classmethod
    @property
    def SHAPE(cls) -> LoadDataFilterOptions:
        '''Load shapes'''
        ...
    
    @classmethod
    @property
    def DRAWING(cls) -> LoadDataFilterOptions:
        '''Drawing objects(including Chart, Picture, OleObject and all other drawing objects)'''
        ...
    
    @classmethod
    @property
    def MERGED_AREA(cls) -> LoadDataFilterOptions:
        '''Load merged cells'''
        ...
    
    @classmethod
    @property
    def CONDITIONAL_FORMATTING(cls) -> LoadDataFilterOptions:
        '''Load conditional formatting'''
        ...
    
    @classmethod
    @property
    def DATA_VALIDATION(cls) -> LoadDataFilterOptions:
        '''Load data validations'''
        ...
    
    @classmethod
    @property
    def PIVOT_TABLE(cls) -> LoadDataFilterOptions:
        '''Load pivot tables'''
        ...
    
    @classmethod
    @property
    def TABLE(cls) -> LoadDataFilterOptions:
        '''Load tables'''
        ...
    
    @classmethod
    @property
    def HYPERLINKS(cls) -> LoadDataFilterOptions:
        '''Load hyperlinks'''
        ...
    
    @classmethod
    @property
    def SHEET_SETTINGS(cls) -> LoadDataFilterOptions:
        '''Load settings for worksheet'''
        ...
    
    @classmethod
    @property
    def SHEET_DATA(cls) -> LoadDataFilterOptions:
        '''Load all data of worksheet, such as cells data, settings, objects, ...etc.'''
        ...
    
    @classmethod
    @property
    def BOOK_SETTINGS(cls) -> LoadDataFilterOptions:
        '''Load settings for workbook'''
        ...
    
    @classmethod
    @property
    def SETTINGS(cls) -> LoadDataFilterOptions:
        '''Load settings for workbook and worksheet'''
        ...
    
    @classmethod
    @property
    def XML_MAP(cls) -> LoadDataFilterOptions:
        '''Load XmlMap'''
        ...
    
    @classmethod
    @property
    def STRUCTURE(cls) -> LoadDataFilterOptions:
        '''Load structure of the workbook'''
        ...
    
    @classmethod
    @property
    def DOCUMENT_PROPERTIES(cls) -> LoadDataFilterOptions:
        '''Load document properties'''
        ...
    
    @classmethod
    @property
    def DEFINED_NAMES(cls) -> LoadDataFilterOptions:
        '''Load defined Name objects'''
        ...
    
    @classmethod
    @property
    def VBA(cls) -> LoadDataFilterOptions:
        '''Load VBA projects'''
        ...
    
    @classmethod
    @property
    def STYLE(cls) -> LoadDataFilterOptions:
        '''Load styles for cell formatting'''
        ...
    
    @classmethod
    @property
    def PICTURE(cls) -> LoadDataFilterOptions:
        '''Load pictures'''
        ...
    
    @classmethod
    @property
    def OLE_OBJECT(cls) -> LoadDataFilterOptions:
        '''Load OleObjects'''
        ...
    
    @classmethod
    @property
    def REVISION(cls) -> LoadDataFilterOptions:
        '''Load revision logs'''
        ...
    
    ...

class LoadFormat:
    '''Represents the load file format.'''
    
    @classmethod
    @property
    def AUTO(cls) -> LoadFormat:
        '''Represents recognizing the format automatically.'''
        ...
    
    @classmethod
    @property
    def CSV(cls) -> LoadFormat:
        '''Comma-Separated Values(CSV) text file.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.LoadFormat.CSV` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def XLSX(cls) -> LoadFormat:
        '''Represents Office Open XML spreadsheetML workbook or template, with or without macros.'''
        ...
    
    @classmethod
    @property
    def TSV(cls) -> LoadFormat:
        '''Tab-Separated Values(TSV) text file.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.LoadFormat.TSV` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def TAB_DELIMITED(cls) -> LoadFormat:
        '''Represents a tab delimited text file, same with :py:attr:`aspose.cells.LoadFormat.TSV`.'''
        ...
    
    @classmethod
    @property
    def HTML(cls) -> LoadFormat:
        '''Represents a html file.'''
        ...
    
    @classmethod
    @property
    def M_HTML(cls) -> LoadFormat:
        '''Represents a mhtml file.'''
        ...
    
    @classmethod
    @property
    def ODS(cls) -> LoadFormat:
        '''Open Document Sheet(ODS) file.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.LoadFormat.ODS` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def EXCEL_97_TO_2003(cls) -> LoadFormat:
        '''Represents an Excel97-2003 xls file.'''
        ...
    
    @classmethod
    @property
    def SPREADSHEET_ML(cls) -> LoadFormat:
        '''Represents an Excel 2003 xml file.'''
        ...
    
    @classmethod
    @property
    def XLSB(cls) -> LoadFormat:
        '''Represents an xlsb file.'''
        ...
    
    @classmethod
    @property
    def OTS(cls) -> LoadFormat:
        '''Open Document Template Sheet(OTS) file.'''
        ...
    
    @classmethod
    @property
    def NUMBERS(cls) -> LoadFormat:
        '''Represents a numbers file.'''
        ...
    
    @classmethod
    @property
    def FODS(cls) -> LoadFormat:
        '''Represents OpenDocument Flat XML Spreadsheet (.fods) file format.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.LoadFormat.FODS` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def SXC(cls) -> LoadFormat:
        '''Represents StarOffice Calc Spreadsheet (.sxc) file format.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.LoadFormat.SXC` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def XML(cls) -> LoadFormat:
        '''Represents a simple xml file.'''
        ...
    
    @classmethod
    @property
    def UNKNOWN(cls) -> LoadFormat:
        '''Represents unrecognized format, cannot be loaded.'''
        ...
    
    @classmethod
    @property
    def IMAGE(cls) -> LoadFormat:
        '''Image'''
        ...
    
    @classmethod
    @property
    def JSON(cls) -> LoadFormat:
        '''Json'''
        ...
    
    ...

class LookAtType:
    '''Represents look at type.'''
    
    @classmethod
    @property
    def CONTAINS(cls) -> LookAtType:
        '''Cell value Contains the find object.'''
        ...
    
    @classmethod
    @property
    def START_WITH(cls) -> LookAtType:
        '''Cell value Starts with the find object.'''
        ...
    
    @classmethod
    @property
    def END_WITH(cls) -> LookAtType:
        '''Cell value ends with the find object.'''
        ...
    
    @classmethod
    @property
    def ENTIRE_CONTENT(cls) -> LookAtType:
        '''Cell value is same as the find object.'''
        ...
    
    ...

class LookInType:
    '''Represents look in type.'''
    
    @classmethod
    @property
    def FORMULAS(cls) -> LookInType:
        '''If the cell contains a formula, find object from formula, else find it from the value.'''
        ...
    
    @classmethod
    @property
    def VALUES(cls) -> LookInType:
        '''Only find object from the formatted values.'''
        ...
    
    @classmethod
    @property
    def VALUES_EXCLUDE_FORMULA_CELL(cls) -> LookInType:
        '''Only find object from the values of cells which do not contains formula.'''
        ...
    
    @classmethod
    @property
    def COMMENTS(cls) -> LookInType:
        '''Only find object from the comments.'''
        ...
    
    @classmethod
    @property
    def ONLY_FORMULAS(cls) -> LookInType:
        '''Only find object from formulas.'''
        ...
    
    @classmethod
    @property
    def ORIGINAL_VALUES(cls) -> LookInType:
        '''Only find object from the original values.'''
        ...
    
    ...

class MemorySetting:
    '''Memory usage options.'''
    
    @classmethod
    @property
    def NORMAL(cls) -> MemorySetting:
        '''Default option for cells model.'''
        ...
    
    @classmethod
    @property
    def MEMORY_PREFERENCE(cls) -> MemorySetting:
        '''Memory performance preferrable.
        With this option the data will be held in compact format so for common scenarios it may give lower memory cost.
        However, this option also may degrade R/W performance a bit in some special cases.'''
        ...
    
    ...

class NameScopeType:
    '''Represents the scope type of defined names.'''
    
    @classmethod
    @property
    def ALL(cls) -> NameScopeType:
        '''All defined names.'''
        ...
    
    @classmethod
    @property
    def WORKBOOK(cls) -> NameScopeType:
        '''The defined names in the workbook.'''
        ...
    
    @classmethod
    @property
    def WORKSHEET(cls) -> NameScopeType:
        '''The defined names in a worksheet or all worksheets.'''
        ...
    
    ...

class NumberCategoryType:
    '''Represents category type of cell's number formatting.'''
    
    @classmethod
    @property
    def GENERAL(cls) -> NumberCategoryType:
        '''General'''
        ...
    
    @classmethod
    @property
    def TEXT(cls) -> NumberCategoryType:
        '''Text'''
        ...
    
    @classmethod
    @property
    def NUMBER(cls) -> NumberCategoryType:
        '''Number'''
        ...
    
    @classmethod
    @property
    def DATE(cls) -> NumberCategoryType:
        '''Date or Date and Time'''
        ...
    
    @classmethod
    @property
    def TIME(cls) -> NumberCategoryType:
        '''Time'''
        ...
    
    @classmethod
    @property
    def FRACTION(cls) -> NumberCategoryType:
        '''Fraction'''
        ...
    
    @classmethod
    @property
    def SCIENTIFIC(cls) -> NumberCategoryType:
        '''Scientific'''
        ...
    
    ...

class OoxmlCompliance:
    '''Allows to specify which OOXML specification will be used when saving in the Xlsx format.'''
    
    @classmethod
    @property
    def ECMA_376_2006(cls) -> OoxmlCompliance:
        '''ECMA-376 1st Edition, 2006.'''
        ...
    
    @classmethod
    @property
    def ISO_29500_2008_STRICT(cls) -> OoxmlCompliance:
        '''ISO/IEC 29500:2008 Strict compliance level.'''
        ...
    
    ...

class OoxmlCompressionType:
    '''The Ooxml compression type'''
    
    @classmethod
    @property
    def LEVEL1(cls) -> OoxmlCompressionType:
        '''The fastest but least effective compression.'''
        ...
    
    @classmethod
    @property
    def LEVEL2(cls) -> OoxmlCompressionType:
        '''A little slower, but better, than level 1.'''
        ...
    
    @classmethod
    @property
    def LEVEL3(cls) -> OoxmlCompressionType:
        '''A little slower, but better, than level 2.'''
        ...
    
    @classmethod
    @property
    def LEVEL4(cls) -> OoxmlCompressionType:
        '''A little slower, but better, than level 3.'''
        ...
    
    @classmethod
    @property
    def LEVEL5(cls) -> OoxmlCompressionType:
        '''A little slower than level 4, but with better compression.'''
        ...
    
    @classmethod
    @property
    def LEVEL6(cls) -> OoxmlCompressionType:
        '''A good balance of speed and compression efficiency.'''
        ...
    
    @classmethod
    @property
    def LEVEL7(cls) -> OoxmlCompressionType:
        '''Pretty good compression!'''
        ...
    
    @classmethod
    @property
    def LEVEL8(cls) -> OoxmlCompressionType:
        '''Better compression than Level7!'''
        ...
    
    @classmethod
    @property
    def LEVEL9(cls) -> OoxmlCompressionType:
        '''The "best" compression, where best means greatest reduction in size of the input data stream.
        This is also the slowest compression.'''
        ...
    
    ...

class OperatorType:
    '''Represents the operator type of conditional format and data validation.'''
    
    @classmethod
    @property
    def BETWEEN(cls) -> OperatorType:
        '''Represents Between operator of conditional format and data validation.'''
        ...
    
    @classmethod
    @property
    def EQUAL(cls) -> OperatorType:
        '''Represents Equal operator of conditional format and data validation.'''
        ...
    
    @classmethod
    @property
    def GREATER_THAN(cls) -> OperatorType:
        '''Represents GreaterThan operator of conditional format and data validation.'''
        ...
    
    @classmethod
    @property
    def GREATER_OR_EQUAL(cls) -> OperatorType:
        '''Represents GreaterOrEqual operator of conditional format and data validation.'''
        ...
    
    @classmethod
    @property
    def LESS_THAN(cls) -> OperatorType:
        '''Represents LessThan operator of conditional format and data validation.'''
        ...
    
    @classmethod
    @property
    def LESS_OR_EQUAL(cls) -> OperatorType:
        '''Represents LessOrEqual operator of conditional format and data validation.'''
        ...
    
    @classmethod
    @property
    def NONE(cls) -> OperatorType:
        '''Represents no comparison.'''
        ...
    
    @classmethod
    @property
    def NOT_BETWEEN(cls) -> OperatorType:
        '''Represents NotBetween operator of conditional format and data validation.'''
        ...
    
    @classmethod
    @property
    def NOT_EQUAL(cls) -> OperatorType:
        '''Represents NotEqual operator of conditional format and data validation.'''
        ...
    
    ...

class PageLayoutAlignmentType:
    '''Enumerates page layout alignment types.'''
    
    @classmethod
    @property
    def BOTTOM(cls) -> PageLayoutAlignmentType:
        '''Represents bottom page layout alignment.'''
        ...
    
    @classmethod
    @property
    def CENTER(cls) -> PageLayoutAlignmentType:
        '''Represents center page layout alignment.'''
        ...
    
    @classmethod
    @property
    def LEFT(cls) -> PageLayoutAlignmentType:
        '''Represents left page layout alignment.'''
        ...
    
    @classmethod
    @property
    def RIGHT(cls) -> PageLayoutAlignmentType:
        '''Represents right page layout alignment.'''
        ...
    
    @classmethod
    @property
    def TOP(cls) -> PageLayoutAlignmentType:
        '''Represents top page layout alignment.'''
        ...
    
    ...

class PageOrientationType:
    '''Represents print orientation constants.'''
    
    @classmethod
    @property
    def LANDSCAPE(cls) -> PageOrientationType:
        '''Landscape orientation'''
        ...
    
    @classmethod
    @property
    def PORTRAIT(cls) -> PageOrientationType:
        '''Portrait orientation'''
        ...
    
    ...

class PaneStateType:
    '''Represents state of the sheet's pane.'''
    
    @classmethod
    @property
    def FROZEN(cls) -> PaneStateType:
        '''Panes are frozen, but were not before being frozen.'''
        ...
    
    @classmethod
    @property
    def FROZEN_SPLIT(cls) -> PaneStateType:
        '''Panes are frozen and were split before being frozen.'''
        ...
    
    @classmethod
    @property
    def SPLIT(cls) -> PaneStateType:
        '''Panes are split, but not frozen.'''
        ...
    
    @classmethod
    @property
    def NORMAL(cls) -> PaneStateType:
        '''Panes are not frozen and not split.'''
        ...
    
    ...

class PaperSizeType:
    '''Represents paper size constants.'''
    
    @classmethod
    @property
    def PAPER_LETTER(cls) -> PaperSizeType:
        '''Letter (8-1/2 in. x 11 in.)'''
        ...
    
    @classmethod
    @property
    def PAPER_LETTER_SMALL(cls) -> PaperSizeType:
        '''Letter Small (8-1/2 in. x 11 in.)'''
        ...
    
    @classmethod
    @property
    def PAPER_TABLOID(cls) -> PaperSizeType:
        '''Tabloid (11 in. x 17 in.)'''
        ...
    
    @classmethod
    @property
    def PAPER_LEDGER(cls) -> PaperSizeType:
        '''Ledger (17 in. x 11 in.)'''
        ...
    
    @classmethod
    @property
    def PAPER_LEGAL(cls) -> PaperSizeType:
        '''Legal (8-1/2 in. x 14 in.)'''
        ...
    
    @classmethod
    @property
    def PAPER_STATEMENT(cls) -> PaperSizeType:
        '''Statement (5-1/2 in. x 8-1/2 in.)'''
        ...
    
    @classmethod
    @property
    def PAPER_EXECUTIVE(cls) -> PaperSizeType:
        '''Executive (7-1/4 in. x 10-1/2 in.)'''
        ...
    
    @classmethod
    @property
    def PAPER_A3(cls) -> PaperSizeType:
        '''A3 (297 mm x 420 mm)'''
        ...
    
    @classmethod
    @property
    def PAPER_A4(cls) -> PaperSizeType:
        '''A4 (210 mm x 297 mm)'''
        ...
    
    @classmethod
    @property
    def PAPER_A4_SMALL(cls) -> PaperSizeType:
        '''A4 Small (210 mm x 297 mm)'''
        ...
    
    @classmethod
    @property
    def PAPER_A5(cls) -> PaperSizeType:
        '''A5 (148 mm x 210 mm)'''
        ...
    
    @classmethod
    @property
    def PAPER_B4(cls) -> PaperSizeType:
        '''JIS B4 (257 mm x 364 mm)'''
        ...
    
    @classmethod
    @property
    def PAPER_B5(cls) -> PaperSizeType:
        '''JIS B5 (182 mm x 257 mm)'''
        ...
    
    @classmethod
    @property
    def PAPER_FOLIO(cls) -> PaperSizeType:
        '''Folio (8-1/2 in. x 13 in.)'''
        ...
    
    @classmethod
    @property
    def PAPER_QUARTO(cls) -> PaperSizeType:
        '''Quarto (215 mm x 275 mm)'''
        ...
    
    @classmethod
    @property
    def PAPER_10X14(cls) -> PaperSizeType:
        '''10 in. x 14 in.'''
        ...
    
    @classmethod
    @property
    def PAPER_11X17(cls) -> PaperSizeType:
        '''11 in. x 17 in.'''
        ...
    
    @classmethod
    @property
    def PAPER_NOTE(cls) -> PaperSizeType:
        '''Note (8-1/2 in. x 11 in.)'''
        ...
    
    @classmethod
    @property
    def PAPER_ENVELOPE9(cls) -> PaperSizeType:
        '''Envelope #9 (3-7/8 in. x 8-7/8 in.)'''
        ...
    
    @classmethod
    @property
    def PAPER_ENVELOPE10(cls) -> PaperSizeType:
        '''Envelope #10 (4-1/8 in. x 9-1/2 in.)'''
        ...
    
    @classmethod
    @property
    def PAPER_ENVELOPE11(cls) -> PaperSizeType:
        '''Envelope #11 (4-1/2 in. x 10-3/8 in.)'''
        ...
    
    @classmethod
    @property
    def PAPER_ENVELOPE12(cls) -> PaperSizeType:
        '''Envelope #12 (4-1/2 in. x 11 in.)'''
        ...
    
    @classmethod
    @property
    def PAPER_ENVELOPE14(cls) -> PaperSizeType:
        '''Envelope #14 (5 in. x 11-1/2 in.)'''
        ...
    
    @classmethod
    @property
    def PAPER_C_SHEET(cls) -> PaperSizeType:
        '''C size sheet'''
        ...
    
    @classmethod
    @property
    def PAPER_D_SHEET(cls) -> PaperSizeType:
        '''D size sheet'''
        ...
    
    @classmethod
    @property
    def PAPER_E_SHEET(cls) -> PaperSizeType:
        '''E size sheet'''
        ...
    
    @classmethod
    @property
    def PAPER_ENVELOPE_DL(cls) -> PaperSizeType:
        '''Envelope DL (110 mm x 220 mm)'''
        ...
    
    @classmethod
    @property
    def PAPER_ENVELOPE_C5(cls) -> PaperSizeType:
        '''Envelope C5 (162 mm x 229 mm)'''
        ...
    
    @classmethod
    @property
    def PAPER_ENVELOPE_C3(cls) -> PaperSizeType:
        '''Envelope C3 (324 mm x 458 mm)'''
        ...
    
    @classmethod
    @property
    def PAPER_ENVELOPE_C4(cls) -> PaperSizeType:
        '''Envelope C4 (229 mm x 324 mm)'''
        ...
    
    @classmethod
    @property
    def PAPER_ENVELOPE_C6(cls) -> PaperSizeType:
        '''Envelope C6 (114 mm x 162 mm)'''
        ...
    
    @classmethod
    @property
    def PAPER_ENVELOPE_C65(cls) -> PaperSizeType:
        '''Envelope C65 (114 mm x 229 mm)'''
        ...
    
    @classmethod
    @property
    def PAPER_ENVELOPE_B4(cls) -> PaperSizeType:
        '''Envelope B4 (250 mm x 353 mm)'''
        ...
    
    @classmethod
    @property
    def PAPER_ENVELOPE_B5(cls) -> PaperSizeType:
        '''Envelope B5 (176 mm x 250 mm)'''
        ...
    
    @classmethod
    @property
    def PAPER_ENVELOPE_B6(cls) -> PaperSizeType:
        '''Envelope B6 (176 mm x 125 mm)'''
        ...
    
    @classmethod
    @property
    def PAPER_ENVELOPE_ITALY(cls) -> PaperSizeType:
        '''Envelope Italy (110 mm x 230 mm)'''
        ...
    
    @classmethod
    @property
    def PAPER_ENVELOPE_MONARCH(cls) -> PaperSizeType:
        '''Envelope Monarch (3-7/8 in. x 7-1/2 in.)'''
        ...
    
    @classmethod
    @property
    def PAPER_ENVELOPE_PERSONAL(cls) -> PaperSizeType:
        '''Envelope (3-5/8 in. x 6-1/2 in.)'''
        ...
    
    @classmethod
    @property
    def PAPER_FANFOLD_US(cls) -> PaperSizeType:
        '''U.S. Standard Fanfold (14-7/8 in. x 11 in.)'''
        ...
    
    @classmethod
    @property
    def PAPER_FANFOLD_STD_GERMAN(cls) -> PaperSizeType:
        '''German Standard Fanfold (8-1/2 in. x 12 in.)'''
        ...
    
    @classmethod
    @property
    def PAPER_FANFOLD_LEGAL_GERMAN(cls) -> PaperSizeType:
        '''German Legal Fanfold (8-1/2 in. x 13 in.)'''
        ...
    
    @classmethod
    @property
    def PAPER_ISOB4(cls) -> PaperSizeType:
        '''B4 (ISO) 250 x 353 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_JAPANESE_POSTCARD(cls) -> PaperSizeType:
        '''Japanese Postcard (100mm × 148mm)'''
        ...
    
    @classmethod
    @property
    def PAPER_9X11(cls) -> PaperSizeType:
        '''9? × 11?'''
        ...
    
    @classmethod
    @property
    def PAPER_10X11(cls) -> PaperSizeType:
        '''10? × 11?'''
        ...
    
    @classmethod
    @property
    def PAPER_15X11(cls) -> PaperSizeType:
        '''15? × 11?'''
        ...
    
    @classmethod
    @property
    def PAPER_ENVELOPE_INVITE(cls) -> PaperSizeType:
        '''Envelope Invite(220mm × 220mm)'''
        ...
    
    @classmethod
    @property
    def PAPER_LETTER_EXTRA(cls) -> PaperSizeType:
        '''US Letter Extra 9 \275 x 12 in'''
        ...
    
    @classmethod
    @property
    def PAPER_LEGAL_EXTRA(cls) -> PaperSizeType:
        '''US Legal Extra 9 \275 x 15 in'''
        ...
    
    @classmethod
    @property
    def PAPER_TABLOID_EXTRA(cls) -> PaperSizeType:
        '''US Tabloid Extra 11.69 x 18 in'''
        ...
    
    @classmethod
    @property
    def PAPER_A4_EXTRA(cls) -> PaperSizeType:
        '''A4 Extra 9.27 x 12.69 in'''
        ...
    
    @classmethod
    @property
    def PAPER_LETTER_TRANSVERSE(cls) -> PaperSizeType:
        '''Letter Transverse 8 \275 x 11 in'''
        ...
    
    @classmethod
    @property
    def PAPER_A4_TRANSVERSE(cls) -> PaperSizeType:
        '''A4 Transverse 210 x 297 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_LETTER_EXTRA_TRANSVERSE(cls) -> PaperSizeType:
        '''Letter Extra Transverse 9\275 x 12 in'''
        ...
    
    @classmethod
    @property
    def PAPER_SUPER_A(cls) -> PaperSizeType:
        '''SuperA/SuperA/A4 227 x 356 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_SUPER_B(cls) -> PaperSizeType:
        '''SuperB/SuperB/A3 305 x 487 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_LETTER_PLUS(cls) -> PaperSizeType:
        '''US Letter Plus 8.5 x 12.69 in'''
        ...
    
    @classmethod
    @property
    def PAPER_A4_PLUS(cls) -> PaperSizeType:
        '''A4 Plus 210 x 330 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_A5_TRANSVERSE(cls) -> PaperSizeType:
        '''A5 Transverse 148 x 210 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_JISB5_TRANSVERSE(cls) -> PaperSizeType:
        '''B5 (JIS) Transverse 182 x 257 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_A3_EXTRA(cls) -> PaperSizeType:
        '''A3 Extra 322 x 445 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_A5_EXTRA(cls) -> PaperSizeType:
        '''A5 Extra 174 x 235 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_ISOB5_EXTRA(cls) -> PaperSizeType:
        '''B5 (ISO) Extra 201 x 276 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_A2(cls) -> PaperSizeType:
        '''A2 420 x 594 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_A3_TRANSVERSE(cls) -> PaperSizeType:
        '''A3 Transverse 297 x 420 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_A3_EXTRA_TRANSVERSE(cls) -> PaperSizeType:
        '''A3 Extra Transverse 322 x 445 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_JAPANESE_DOUBLE_POSTCARD(cls) -> PaperSizeType:
        '''Japanese Double Postcard 200 x 148 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_A6(cls) -> PaperSizeType:
        '''A6 105 x 148 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_JAPANESE_ENVELOPE_KAKU2(cls) -> PaperSizeType:
        '''Japanese Envelope Kaku #2'''
        ...
    
    @classmethod
    @property
    def PAPER_JAPANESE_ENVELOPE_KAKU3(cls) -> PaperSizeType:
        '''Japanese Envelope Kaku #3'''
        ...
    
    @classmethod
    @property
    def PAPER_JAPANESE_ENVELOPE_CHOU3(cls) -> PaperSizeType:
        '''Japanese Envelope Chou #3'''
        ...
    
    @classmethod
    @property
    def PAPER_JAPANESE_ENVELOPE_CHOU4(cls) -> PaperSizeType:
        '''Japanese Envelope Chou #4'''
        ...
    
    @classmethod
    @property
    def PAPER_LETTER_ROTATED(cls) -> PaperSizeType:
        '''11in × 8.5in'''
        ...
    
    @classmethod
    @property
    def PAPER_A3_ROTATED(cls) -> PaperSizeType:
        '''420mm × 297mm'''
        ...
    
    @classmethod
    @property
    def PAPER_A4_ROTATED(cls) -> PaperSizeType:
        '''297mm × 210mm'''
        ...
    
    @classmethod
    @property
    def PAPER_A5_ROTATED(cls) -> PaperSizeType:
        '''210mm × 148mm'''
        ...
    
    @classmethod
    @property
    def PAPER_JISB4_ROTATED(cls) -> PaperSizeType:
        '''B4 (JIS) Rotated 364 x 257 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_JISB5_ROTATED(cls) -> PaperSizeType:
        '''B5 (JIS) Rotated 257 x 182 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_JAPANESE_POSTCARD_ROTATED(cls) -> PaperSizeType:
        '''Japanese Postcard Rotated 148 x 100 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_JAPANESE_DOUBLE_POSTCARD_ROTATED(cls) -> PaperSizeType:
        '''Double Japanese Postcard Rotated 148 x 200 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_A6_ROTATED(cls) -> PaperSizeType:
        '''A6 Rotated 148 x 105 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_JAPANESE_ENVELOPE_KAKU_2_ROTATED(cls) -> PaperSizeType:
        '''Japanese Envelope Kaku #2 Rotated'''
        ...
    
    @classmethod
    @property
    def PAPER_JAPANESE_ENVELOPE_KAKU_3_ROTATED(cls) -> PaperSizeType:
        '''Japanese Envelope Kaku #3 Rotated'''
        ...
    
    @classmethod
    @property
    def PAPER_JAPANESE_ENVELOPE_CHOU_3_ROTATED(cls) -> PaperSizeType:
        '''Japanese Envelope Chou #3 Rotated'''
        ...
    
    @classmethod
    @property
    def PAPER_JAPANESE_ENVELOPE_CHOU_4_ROTATED(cls) -> PaperSizeType:
        '''Japanese Envelope Chou #4 Rotated'''
        ...
    
    @classmethod
    @property
    def PAPER_JISB6(cls) -> PaperSizeType:
        '''B6 (JIS) 128 x 182 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_JISB6_ROTATED(cls) -> PaperSizeType:
        '''B6 (JIS) Rotated 182 x 128 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_12X11(cls) -> PaperSizeType:
        '''12 x 11 in'''
        ...
    
    @classmethod
    @property
    def PAPER_JAPANESE_ENVELOPE_YOU4(cls) -> PaperSizeType:
        '''Japanese Envelope You #4'''
        ...
    
    @classmethod
    @property
    def PAPER_JAPANESE_ENVELOPE_YOU_4_ROTATED(cls) -> PaperSizeType:
        '''Japanese Envelope You #4 Rotated'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC16K(cls) -> PaperSizeType:
        '''PRC 16K 146 x 215 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC32K(cls) -> PaperSizeType:
        '''PRC 32K 97 x 151 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC_BIG_32K(cls) -> PaperSizeType:
        '''PRC 32K(Big) 97 x 151 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC_ENVELOPE1(cls) -> PaperSizeType:
        '''PRC Envelope #1 102 x 165 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC_ENVELOPE2(cls) -> PaperSizeType:
        '''PRC Envelope #2 102 x 176 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC_ENVELOPE3(cls) -> PaperSizeType:
        '''PRC Envelope #3 125 x 176 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC_ENVELOPE4(cls) -> PaperSizeType:
        '''PRC Envelope #4 110 x 208 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC_ENVELOPE5(cls) -> PaperSizeType:
        '''PRC Envelope #5 110 x 220 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC_ENVELOPE6(cls) -> PaperSizeType:
        '''PRC Envelope #6 120 x 230 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC_ENVELOPE7(cls) -> PaperSizeType:
        '''PRC Envelope #7 160 x 230 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC_ENVELOPE8(cls) -> PaperSizeType:
        '''PRC Envelope #8 120 x 309 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC_ENVELOPE9(cls) -> PaperSizeType:
        '''PRC Envelope #9 229 x 324 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC_ENVELOPE10(cls) -> PaperSizeType:
        '''PRC Envelope #10 324 x 458 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC16K_ROTATED(cls) -> PaperSizeType:
        '''PRC 16K Rotated'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC32K_ROTATED(cls) -> PaperSizeType:
        '''PRC 32K Rotated'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC_BIG_32K_ROTATED(cls) -> PaperSizeType:
        '''PRC 32K(Big) Rotated'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC_ENVELOPE_1_ROTATED(cls) -> PaperSizeType:
        '''PRC Envelope #1 Rotated 165 x 102 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC_ENVELOPE_2_ROTATED(cls) -> PaperSizeType:
        '''PRC Envelope #2 Rotated 176 x 102 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC_ENVELOPE_3_ROTATED(cls) -> PaperSizeType:
        '''PRC Envelope #3 Rotated 176 x 125 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC_ENVELOPE_4_ROTATED(cls) -> PaperSizeType:
        '''PRC Envelope #4 Rotated 208 x 110 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC_ENVELOPE_5_ROTATED(cls) -> PaperSizeType:
        '''PRC Envelope #5 Rotated 220 x 110 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC_ENVELOPE_6_ROTATED(cls) -> PaperSizeType:
        '''PRC Envelope #6 Rotated 230 x 120 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC_ENVELOPE_7_ROTATED(cls) -> PaperSizeType:
        '''PRC Envelope #7 Rotated 230 x 160 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC_ENVELOPE_8_ROTATED(cls) -> PaperSizeType:
        '''PRC Envelope #8 Rotated 309 x 120 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC_ENVELOPE_9_ROTATED(cls) -> PaperSizeType:
        '''PRC Envelope #9 Rotated 324 x 229 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_PRC_ENVELOPE_10_ROTATED(cls) -> PaperSizeType:
        '''PRC Envelope #10 Rotated 458 x 324 mm'''
        ...
    
    @classmethod
    @property
    def PAPER_B3(cls) -> PaperSizeType:
        '''usual B3(13.9 x 19.7 in)'''
        ...
    
    @classmethod
    @property
    def PAPER_BUSINESS_CARD(cls) -> PaperSizeType:
        '''Business Card(90mm x 55 mm)'''
        ...
    
    @classmethod
    @property
    def PAPER_THERMAL(cls) -> PaperSizeType:
        '''Thermal(3 x 11 in)'''
        ...
    
    @classmethod
    @property
    def CUSTOM(cls) -> PaperSizeType:
        '''Represents the custom paper size.'''
        ...
    
    ...

class ParameterType:
    '''Represents all parameters' type or return value type of function.'''
    
    @classmethod
    @property
    def REFERENCE(cls) -> ParameterType:
        ...
    
    @classmethod
    @property
    def VALUE(cls) -> ParameterType:
        ...
    
    @classmethod
    @property
    def ARRAY(cls) -> ParameterType:
        ...
    
    ...

class PasteOperationType:
    '''Represents operation type when pasting range.'''
    
    @classmethod
    @property
    def NONE(cls) -> PasteOperationType:
        '''No operation.'''
        ...
    
    @classmethod
    @property
    def ADD(cls) -> PasteOperationType:
        '''Add'''
        ...
    
    @classmethod
    @property
    def SUBTRACT(cls) -> PasteOperationType:
        '''Subtract'''
        ...
    
    @classmethod
    @property
    def MULTIPLY(cls) -> PasteOperationType:
        '''Multiply'''
        ...
    
    @classmethod
    @property
    def DIVIDE(cls) -> PasteOperationType:
        '''Divide'''
        ...
    
    ...

class PasteType:
    '''Represents the paste special type.'''
    
    @classmethod
    @property
    def ALL(cls) -> PasteType:
        '''Copies all data of the range.'''
        ...
    
    @classmethod
    @property
    def DEFAULT(cls) -> PasteType:
        '''It works as "All" behavior of MS Excel.'''
        ...
    
    @classmethod
    @property
    def ALL_EXCEPT_BORDERS(cls) -> PasteType:
        '''Copies all data of the range without the range.'''
        ...
    
    @classmethod
    @property
    def DEFAULT_EXCEPT_BORDERS(cls) -> PasteType:
        '''It works as "All except borders" behavior of MS Excel.'''
        ...
    
    @classmethod
    @property
    def COLUMN_WIDTHS(cls) -> PasteType:
        '''Only copies the widths of the range.'''
        ...
    
    @classmethod
    @property
    def ROW_HEIGHTS(cls) -> PasteType:
        '''Only copies the heights of the range.'''
        ...
    
    @classmethod
    @property
    def COMMENTS(cls) -> PasteType:
        ...
    
    @classmethod
    @property
    def FORMATS(cls) -> PasteType:
        ...
    
    @classmethod
    @property
    def FORMULAS(cls) -> PasteType:
        ...
    
    @classmethod
    @property
    def FORMULAS_AND_NUMBER_FORMATS(cls) -> PasteType:
        ...
    
    @classmethod
    @property
    def VALIDATION(cls) -> PasteType:
        ...
    
    @classmethod
    @property
    def VALUES(cls) -> PasteType:
        ...
    
    @classmethod
    @property
    def VALUES_AND_FORMATS(cls) -> PasteType:
        ...
    
    @classmethod
    @property
    def VALUES_AND_NUMBER_FORMATS(cls) -> PasteType:
        ...
    
    ...

class PrintCommentsType:
    '''Represents the way comments are printed with the sheet.'''
    
    @classmethod
    @property
    def PRINT_IN_PLACE(cls) -> PrintCommentsType:
        '''Represents to print comments as displayed on sheet.'''
        ...
    
    @classmethod
    @property
    def PRINT_NO_COMMENTS(cls) -> PrintCommentsType:
        '''Represents not to print comments.'''
        ...
    
    @classmethod
    @property
    def PRINT_SHEET_END(cls) -> PrintCommentsType:
        '''Represents to print comments at end of sheet.'''
        ...
    
    ...

class PrintErrorsType:
    '''Represents print errors constants.'''
    
    @classmethod
    @property
    def PRINT_ERRORS_BLANK(cls) -> PrintErrorsType:
        '''Represents not to print errors.'''
        ...
    
    @classmethod
    @property
    def PRINT_ERRORS_DASH(cls) -> PrintErrorsType:
        '''Represents to print errors as "--".'''
        ...
    
    @classmethod
    @property
    def PRINT_ERRORS_DISPLAYED(cls) -> PrintErrorsType:
        '''Represents to print errors as displayed.'''
        ...
    
    @classmethod
    @property
    def PRINT_ERRORS_NA(cls) -> PrintErrorsType:
        '''Represents to print errors as "#N/A".'''
        ...
    
    ...

class PrintOrderType:
    '''Represent print order constants.'''
    
    @classmethod
    @property
    def DOWN_THEN_OVER(cls) -> PrintOrderType:
        '''Down, then over'''
        ...
    
    @classmethod
    @property
    def OVER_THEN_DOWN(cls) -> PrintOrderType:
        '''Over, then down'''
        ...
    
    ...

class PrintSizeType:
    '''Represents the printed chart size.'''
    
    @classmethod
    @property
    def FULL(cls) -> PrintSizeType:
        '''Use full page.'''
        ...
    
    @classmethod
    @property
    def FIT(cls) -> PrintSizeType:
        '''Scale to fit page.'''
        ...
    
    @classmethod
    @property
    def CUSTOM(cls) -> PrintSizeType:
        '''Custom.'''
        ...
    
    ...

class PrintingPageType:
    '''Indicates which pages will not be printed.'''
    
    @classmethod
    @property
    def DEFAULT(cls) -> PrintingPageType:
        '''Prints all pages.'''
        ...
    
    @classmethod
    @property
    def IGNORE_BLANK(cls) -> PrintingPageType:
        '''Don't print the pages which the cells are blank.'''
        ...
    
    @classmethod
    @property
    def IGNORE_STYLE(cls) -> PrintingPageType:
        '''Don't print the pages which cells only contain styles.'''
        ...
    
    ...

class ProtectionType:
    '''Represents workbook/worksheet protection type.'''
    
    @classmethod
    @property
    def ALL(cls) -> ProtectionType:
        '''Represents to protect all.'''
        ...
    
    @classmethod
    @property
    def CONTENTS(cls) -> ProtectionType:
        '''Represents to protect contents, used in Worksheet protection.'''
        ...
    
    @classmethod
    @property
    def OBJECTS(cls) -> ProtectionType:
        '''Represents to protect objects, used in Worksheet protection.'''
        ...
    
    @classmethod
    @property
    def SCENARIOS(cls) -> ProtectionType:
        '''Represents to protect scenarios, used in Worksheet protection.'''
        ...
    
    @classmethod
    @property
    def STRUCTURE(cls) -> ProtectionType:
        '''Represents to protect structure, used in Workbook protection.'''
        ...
    
    @classmethod
    @property
    def WINDOWS(cls) -> ProtectionType:
        '''Represents to protect window, used in Workbook protection.'''
        ...
    
    @classmethod
    @property
    def NONE(cls) -> ProtectionType:
        '''Represents no protection. Only for Reading property.'''
        ...
    
    ...

class RenameStrategy:
    '''Strategy option for duplicate names of columns.'''
    
    @classmethod
    @property
    def EXCEPTION(cls) -> RenameStrategy:
        '''Throws exception.'''
        ...
    
    @classmethod
    @property
    def DIGIT(cls) -> RenameStrategy:
        '''Named with digit. Duplicated names will become ...1, ...2, etc.'''
        ...
    
    @classmethod
    @property
    def LETTER(cls) -> RenameStrategy:
        '''Named with letter.. Duplicated names will become ...A, ...B, etc.'''
        ...
    
    ...

class ResourceLoadingType:
    '''Represents how to loading the linked resource.'''
    
    @classmethod
    @property
    def DEFAULT(cls) -> ResourceLoadingType:
        '''Loads this resource as usual.'''
        ...
    
    @classmethod
    @property
    def SKIP(cls) -> ResourceLoadingType:
        '''Skips loading of this resource.'''
        ...
    
    @classmethod
    @property
    def USER_PROVIDED(cls) -> ResourceLoadingType:
        '''Use stream provided by user'''
        ...
    
    ...

class SaveFormat:
    '''Represents the format in which the workbook is saved.'''
    
    @classmethod
    @property
    def CSV(cls) -> SaveFormat:
        '''Comma-Separated Values(CSV) text file.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.SaveFormat.CSV` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def XLSX(cls) -> SaveFormat:
        '''Represents an xlsx file.'''
        ...
    
    @classmethod
    @property
    def XLSM(cls) -> SaveFormat:
        '''Represents an xlsm file which enable macros.'''
        ...
    
    @classmethod
    @property
    def XLTX(cls) -> SaveFormat:
        '''Represents an xltx file.'''
        ...
    
    @classmethod
    @property
    def XLTM(cls) -> SaveFormat:
        '''Represents an xltm file which enable macros.'''
        ...
    
    @classmethod
    @property
    def XLAM(cls) -> SaveFormat:
        '''Represents an xltm file which enable addin macros.'''
        ...
    
    @classmethod
    @property
    def TSV(cls) -> SaveFormat:
        '''Tab-Separated Values(TSV) text file.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.SaveFormat.TSV` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def TAB_DELIMITED(cls) -> SaveFormat:
        '''Represents a tab delimited text file, same with :py:attr:`aspose.cells.SaveFormat.TSV`.'''
        ...
    
    @classmethod
    @property
    def HTML(cls) -> SaveFormat:
        '''Represents a html file.'''
        ...
    
    @classmethod
    @property
    def M_HTML(cls) -> SaveFormat:
        '''Represents a mhtml file.'''
        ...
    
    @classmethod
    @property
    def ODS(cls) -> SaveFormat:
        '''Open Document Sheet(ODS) file.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.SaveFormat.ODS` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def EXCEL_97_TO_2003(cls) -> SaveFormat:
        '''Represents an Excel97-2003 xls file.'''
        ...
    
    @classmethod
    @property
    def SPREADSHEET_ML(cls) -> SaveFormat:
        '''Represents an Excel 2003 xml file.'''
        ...
    
    @classmethod
    @property
    def XLSB(cls) -> SaveFormat:
        '''Represents an xlsb file.'''
        ...
    
    @classmethod
    @property
    def AUTO(cls) -> SaveFormat:
        '''If saving the file to the disk,the file format accords to the extension of the file name.
        If saving the file to the stream, the file format is xlsx.'''
        ...
    
    @classmethod
    @property
    def UNKNOWN(cls) -> SaveFormat:
        '''Represents unrecognized format, cannot be saved.'''
        ...
    
    @classmethod
    @property
    def PDF(cls) -> SaveFormat:
        '''Represents a Pdf file.'''
        ...
    
    @classmethod
    @property
    def XPS(cls) -> SaveFormat:
        '''XPS (XML Paper Specification) format.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.SaveFormat.XPS` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def TIFF(cls) -> SaveFormat:
        '''Represents a TIFF file.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.SaveFormat.TIFF` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def SVG(cls) -> SaveFormat:
        '''SVG file.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.SaveFormat.SVG` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def DIF(cls) -> SaveFormat:
        '''Data Interchange Format.'''
        ...
    
    @classmethod
    @property
    def OTS(cls) -> SaveFormat:
        '''Open Document Template Sheet(OTS) file.'''
        ...
    
    @classmethod
    @property
    def XLT(cls) -> SaveFormat:
        '''Excel 97-2003 template file.'''
        ...
    
    @classmethod
    @property
    def XML(cls) -> SaveFormat:
        '''Represents a simple xml file.'''
        ...
    
    @classmethod
    @property
    def NUMBERS(cls) -> SaveFormat:
        '''Represents a numbers file.'''
        ...
    
    @classmethod
    @property
    def MARKDOWN(cls) -> SaveFormat:
        '''Represents markdown document.'''
        ...
    
    @classmethod
    @property
    def FODS(cls) -> SaveFormat:
        '''Represents OpenDocument Flat XML Spreadsheet (.fods) file format.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.SaveFormat.FODS` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def SXC(cls) -> SaveFormat:
        '''Represents StarOffice Calc Spreadsheet (.sxc) file format.
        NOTE: This member is now obsolete. Instead,
        please use :py:attr:`aspose.cells.SaveFormat.SXC` property.
        This property will be removed 6 months later since April 2021.
        Aspose apologizes for any inconvenience you may have experienced.'''
        ...
    
    @classmethod
    @property
    def PPTX(cls) -> SaveFormat:
        '''Represents .pptx file.'''
        ...
    
    @classmethod
    @property
    def DOCX(cls) -> SaveFormat:
        '''Represents .docx file.'''
        ...
    
    @classmethod
    @property
    def EMF(cls) -> SaveFormat:
        '''Windows Enhanced Metafile.'''
        ...
    
    @classmethod
    @property
    def JPG(cls) -> SaveFormat:
        '''JPEG JFIF.'''
        ...
    
    @classmethod
    @property
    def PNG(cls) -> SaveFormat:
        '''Portable Network Graphics.'''
        ...
    
    @classmethod
    @property
    def BMP(cls) -> SaveFormat:
        '''Windows Bitmap'''
        ...
    
    @classmethod
    @property
    def GIF(cls) -> SaveFormat:
        '''Gif'''
        ...
    
    @classmethod
    @property
    def JSON(cls) -> SaveFormat:
        '''Json'''
        ...
    
    @classmethod
    @property
    def SQL_SCRIPT(cls) -> SaveFormat:
        '''Sql'''
        ...
    
    @classmethod
    @property
    def X_HTML(cls) -> SaveFormat:
        '''Rrepesents XHtml file.'''
        ...
    
    ...

class SheetType:
    '''Specifies the worksheet type.'''
    
    @classmethod
    @property
    def VB(cls) -> SheetType:
        '''Visual Basic module'''
        ...
    
    @classmethod
    @property
    def WORKSHEET(cls) -> SheetType:
        ...
    
    @classmethod
    @property
    def CHART(cls) -> SheetType:
        '''Chart'''
        ...
    
    @classmethod
    @property
    def BIFF4_MACRO(cls) -> SheetType:
        '''BIFF4 Macro sheet'''
        ...
    
    @classmethod
    @property
    def INTERNATIONAL_MACRO(cls) -> SheetType:
        '''International Macro sheet'''
        ...
    
    @classmethod
    @property
    def OTHER(cls) -> SheetType:
        ...
    
    @classmethod
    @property
    def DIALOG(cls) -> SheetType:
        '''Dialog worksheet'''
        ...
    
    ...

class ShiftType:
    '''Represent the shift options when deleting a range of cells.'''
    
    @classmethod
    @property
    def DOWN(cls) -> ShiftType:
        '''Shift cells down.'''
        ...
    
    @classmethod
    @property
    def LEFT(cls) -> ShiftType:
        '''Shift cells left.'''
        ...
    
    @classmethod
    @property
    def NONE(cls) -> ShiftType:
        '''Do not shift cells.'''
        ...
    
    @classmethod
    @property
    def RIGHT(cls) -> ShiftType:
        '''Shift cells right.'''
        ...
    
    @classmethod
    @property
    def UP(cls) -> ShiftType:
        '''Shift cells up.'''
        ...
    
    ...

class SortOnType:
    '''Sorted value type.'''
    
    @classmethod
    @property
    def VALUE(cls) -> SortOnType:
        '''Sorts by cells' value.'''
        ...
    
    @classmethod
    @property
    def CELL_COLOR(cls) -> SortOnType:
        '''Sorts by cells' color.'''
        ...
    
    @classmethod
    @property
    def FONT_COLOR(cls) -> SortOnType:
        '''Sorts by cells' font color.'''
        ...
    
    @classmethod
    @property
    def ICON(cls) -> SortOnType:
        '''Sorts by conditional icon.'''
        ...
    
    ...

class SortOrder:
    '''Represents sort order for the data range.'''
    
    @classmethod
    @property
    def ASCENDING(cls) -> SortOrder:
        ...
    
    @classmethod
    @property
    def DESCENDING(cls) -> SortOrder:
        ...
    
    ...

class StyleModifyFlag:
    '''The style modified flags.'''
    
    @classmethod
    @property
    def LEFT_BORDER(cls) -> StyleModifyFlag:
        '''Indicates whether left border has been modified for the style.'''
        ...
    
    @classmethod
    @property
    def RIGHT_BORDER(cls) -> StyleModifyFlag:
        '''Indicates whether right border has been modified for the style.'''
        ...
    
    @classmethod
    @property
    def TOP_BORDER(cls) -> StyleModifyFlag:
        '''Indicates whether top border has been modified for the style.'''
        ...
    
    @classmethod
    @property
    def BOTTOM_BORDER(cls) -> StyleModifyFlag:
        '''Indicates whether bottom border has been modified for the style.'''
        ...
    
    @classmethod
    @property
    def DIAGONAL_DOWN_BORDER(cls) -> StyleModifyFlag:
        '''Indicates whether diagonal-down border has been modified for the style.'''
        ...
    
    @classmethod
    @property
    def DIAGONAL_UP_BORDER(cls) -> StyleModifyFlag:
        '''Indicates whether diagonal-up border has been modified for the style.'''
        ...
    
    @classmethod
    @property
    def DIAGONAL(cls) -> StyleModifyFlag:
        '''Indicates whether one or more diagonal borders(:py:attr:`aspose.cells.StyleModifyFlag.DIAGONAL_DOWN_BORDER`,
        :py:attr:`aspose.cells.StyleModifyFlag.DIAGONAL_UP_BORDER`) have been modified for the style.'''
        ...
    
    @classmethod
    @property
    def HORIZONTAL_BORDER(cls) -> StyleModifyFlag:
        '''Indicates whether horizontal border has been modified for the style.
        Only for dynamic style, such as conditional formatting.'''
        ...
    
    @classmethod
    @property
    def VERTICAL_BORDER(cls) -> StyleModifyFlag:
        '''Indicates whether vertical border has been modified for the style.
        Only for dynamic style, such as conditional formatting.'''
        ...
    
    @classmethod
    @property
    def BORDERS(cls) -> StyleModifyFlag:
        '''Indicates whether one or more borders(:py:attr:`aspose.cells.StyleModifyFlag.LEFT_BORDER`,
        :py:attr:`aspose.cells.StyleModifyFlag.RIGHT_BORDER`, :py:attr:`aspose.cells.StyleModifyFlag.TOP_BORDER`, :py:attr:`aspose.cells.StyleModifyFlag.BOTTOM_BORDER`,
        :py:attr:`aspose.cells.StyleModifyFlag.DIAGONAL`, :py:attr:`aspose.cells.StyleModifyFlag.HORIZONTAL_BORDER`, :py:attr:`aspose.cells.StyleModifyFlag.VERTICAL_BORDER`)
        have been modified for the style.'''
        ...
    
    @classmethod
    @property
    def NUMBER_FORMAT(cls) -> StyleModifyFlag:
        '''Indicates whether numberformat has been modified.'''
        ...
    
    @classmethod
    @property
    def HORIZONTAL_ALIGNMENT(cls) -> StyleModifyFlag:
        '''Indicates whether horizontal alignment has been modified.'''
        ...
    
    @classmethod
    @property
    def VERTICAL_ALIGNMENT(cls) -> StyleModifyFlag:
        '''Indicates whether vertical alignment has been modified.'''
        ...
    
    @classmethod
    @property
    def INDENT(cls) -> StyleModifyFlag:
        '''Indicates whether indent property has been modified.'''
        ...
    
    @classmethod
    @property
    def ROTATION(cls) -> StyleModifyFlag:
        '''Indicates whether rotation property has been modified.'''
        ...
    
    @classmethod
    @property
    def WRAP_TEXT(cls) -> StyleModifyFlag:
        '''Indicates whether wrap text property has been modified.'''
        ...
    
    @classmethod
    @property
    def SHRINK_TO_FIT(cls) -> StyleModifyFlag:
        '''Indicates whether shrink to fit property has been modified.'''
        ...
    
    @classmethod
    @property
    def TEXT_DIRECTION(cls) -> StyleModifyFlag:
        '''Indicates whether text direction property has been modified.'''
        ...
    
    @classmethod
    @property
    def RELATIVE_INDENT(cls) -> StyleModifyFlag:
        '''Indicates whether relative indent property has been modified for the style.
        Only for dynamic style, such as conditional formatting.'''
        ...
    
    @classmethod
    @property
    def ALIGNMENT_SETTINGS(cls) -> StyleModifyFlag:
        '''Indicates whether one or more alignment-related properties(:py:attr:`aspose.cells.StyleModifyFlag.HORIZONTAL_ALIGNMENT`,
        :py:attr:`aspose.cells.StyleModifyFlag.VERTICAL_ALIGNMENT`, :py:attr:`aspose.cells.StyleModifyFlag.ROTATION`, :py:attr:`aspose.cells.StyleModifyFlag.WRAP_TEXT`,
        :py:attr:`aspose.cells.StyleModifyFlag.WRAP_TEXT`, :py:attr:`aspose.cells.StyleModifyFlag.INDENT`, :py:attr:`aspose.cells.StyleModifyFlag.SHRINK_TO_FIT`, :py:attr:`aspose.cells.StyleModifyFlag.TEXT_DIRECTION`,
        :py:attr:`aspose.cells.StyleModifyFlag.RELATIVE_INDENT`) have been modified.'''
        ...
    
    @classmethod
    @property
    def PATTERN(cls) -> StyleModifyFlag:
        '''Indicates whether pattern of the shading has been modified.'''
        ...
    
    @classmethod
    @property
    def FOREGROUND_COLOR(cls) -> StyleModifyFlag:
        '''Indicates whether foreground color has been modified.'''
        ...
    
    @classmethod
    @property
    def BACKGROUND_COLOR(cls) -> StyleModifyFlag:
        '''Indicates whether background color has been modified.'''
        ...
    
    @classmethod
    @property
    def CELL_SHADING(cls) -> StyleModifyFlag:
        '''Indicates whether one or more shading-related properties(:py:attr:`aspose.cells.StyleModifyFlag.PATTERN`,
        :py:attr:`aspose.cells.StyleModifyFlag.FOREGROUND_COLOR`, :py:attr:`aspose.cells.StyleModifyFlag.BACKGROUND_COLOR`) have been modified.'''
        ...
    
    @classmethod
    @property
    def LOCKED(cls) -> StyleModifyFlag:
        '''Indicates whether locked property has been modified.'''
        ...
    
    @classmethod
    @property
    def HIDE_FORMULA(cls) -> StyleModifyFlag:
        '''Indicates whether hide formula has been modified.'''
        ...
    
    @classmethod
    @property
    def PROTECTION_SETTINGS(cls) -> StyleModifyFlag:
        '''Indicates whether one or more protection-related properties(:py:attr:`aspose.cells.StyleModifyFlag.LOCKED`,
        :py:attr:`aspose.cells.StyleModifyFlag.HIDE_FORMULA`) have been modified.'''
        ...
    
    @classmethod
    @property
    def FONT_SIZE(cls) -> StyleModifyFlag:
        '''Indicates whether font size has been modified.'''
        ...
    
    @classmethod
    @property
    def FONT_NAME(cls) -> StyleModifyFlag:
        '''Indicates whether font name has been modified.'''
        ...
    
    @classmethod
    @property
    def FONT_COLOR(cls) -> StyleModifyFlag:
        '''Indicates whether font color has been modified.'''
        ...
    
    @classmethod
    @property
    def FONT_WEIGHT(cls) -> StyleModifyFlag:
        '''Indicates whether font weight has been modified.'''
        ...
    
    @classmethod
    @property
    def FONT_ITALIC(cls) -> StyleModifyFlag:
        '''Indicates whether italic property of font has been modified.'''
        ...
    
    @classmethod
    @property
    def FONT_UNDERLINE(cls) -> StyleModifyFlag:
        '''Indicates whether underline property of font has been modified.'''
        ...
    
    @classmethod
    @property
    def FONT_STRIKE(cls) -> StyleModifyFlag:
        '''Indicates whether strike property font has been modified.'''
        ...
    
    @classmethod
    @property
    def FONT_SCRIPT(cls) -> StyleModifyFlag:
        '''Indicates whether subscript or superscript property of font has been modified.'''
        ...
    
    @classmethod
    @property
    def FONT_FAMILY(cls) -> StyleModifyFlag:
        '''Indicates whether font family has been modified.'''
        ...
    
    @classmethod
    @property
    def FONT_CHARSET(cls) -> StyleModifyFlag:
        '''Indicates whether charset of the font has been modified.'''
        ...
    
    @classmethod
    @property
    def FONT_SCHEME(cls) -> StyleModifyFlag:
        '''unused.'''
        ...
    
    @classmethod
    @property
    def FONT_DIRTY(cls) -> StyleModifyFlag:
        '''unused.'''
        ...
    
    @classmethod
    @property
    def FONT_SPELLING_ERROR(cls) -> StyleModifyFlag:
        '''unused.'''
        ...
    
    @classmethod
    @property
    def FONT_U_FILL_TX(cls) -> StyleModifyFlag:
        '''unused.'''
        ...
    
    @classmethod
    @property
    def FONT_SPACING(cls) -> StyleModifyFlag:
        '''unused.'''
        ...
    
    @classmethod
    @property
    def FONT_KERNING(cls) -> StyleModifyFlag:
        '''unused.'''
        ...
    
    @classmethod
    @property
    def FONT_EQUALIZE(cls) -> StyleModifyFlag:
        '''unused.'''
        ...
    
    @classmethod
    @property
    def FONT_CAP(cls) -> StyleModifyFlag:
        '''unused.'''
        ...
    
    @classmethod
    @property
    def FONT_VERTICAL_TEXT(cls) -> StyleModifyFlag:
        ...
    
    @classmethod
    @property
    def FONT(cls) -> StyleModifyFlag:
        '''Indicates whether one or more properties have been modified for the font of the style.'''
        ...
    
    @classmethod
    @property
    def ALL(cls) -> StyleModifyFlag:
        '''Indicates whether one or more properties have been modified for the style.'''
        ...
    
    ...

class TargetModeType:
    '''Represents the type of target mode.'''
    
    @classmethod
    @property
    def EXTERNAL(cls) -> TargetModeType:
        '''External link'''
        ...
    
    @classmethod
    @property
    def FILE_PATH(cls) -> TargetModeType:
        '''Local and full paths to files or folders.'''
        ...
    
    @classmethod
    @property
    def EMAIL(cls) -> TargetModeType:
        '''Email.'''
        ...
    
    @classmethod
    @property
    def CELL_REFERENCE(cls) -> TargetModeType:
        '''Link on cell or named range.'''
        ...
    
    ...

class TextAlignmentType:
    '''Enumerates text alignment types.'''
    
    @classmethod
    @property
    def GENERAL(cls) -> TextAlignmentType:
        '''Represents general text alignment.'''
        ...
    
    @classmethod
    @property
    def BOTTOM(cls) -> TextAlignmentType:
        '''Represents bottom text alignment.'''
        ...
    
    @classmethod
    @property
    def CENTER(cls) -> TextAlignmentType:
        '''Represents center text alignment.'''
        ...
    
    @classmethod
    @property
    def CENTER_ACROSS(cls) -> TextAlignmentType:
        '''Represents center across text alignment.'''
        ...
    
    @classmethod
    @property
    def DISTRIBUTED(cls) -> TextAlignmentType:
        '''Represents distributed text alignment.'''
        ...
    
    @classmethod
    @property
    def FILL(cls) -> TextAlignmentType:
        '''Represents fill text alignment.'''
        ...
    
    @classmethod
    @property
    def JUSTIFY(cls) -> TextAlignmentType:
        '''Represents justify text alignment.'''
        ...
    
    @classmethod
    @property
    def LEFT(cls) -> TextAlignmentType:
        '''Represents left text alignment.'''
        ...
    
    @classmethod
    @property
    def RIGHT(cls) -> TextAlignmentType:
        '''Represents right text alignment.'''
        ...
    
    @classmethod
    @property
    def TOP(cls) -> TextAlignmentType:
        '''Represents top text alignment.'''
        ...
    
    @classmethod
    @property
    def JUSTIFIED_LOW(cls) -> TextAlignmentType:
        '''Aligns the text with an adjusted kashida length for Arabic text.'''
        ...
    
    @classmethod
    @property
    def THAI_DISTRIBUTED(cls) -> TextAlignmentType:
        '''Distributes Thai text specially, because each character is treated as a word.'''
        ...
    
    ...

class TextCapsType:
    '''This type specifies the cap types of the text.'''
    
    @classmethod
    @property
    def NONE(cls) -> TextCapsType:
        '''None caps'''
        ...
    
    @classmethod
    @property
    def ALL(cls) -> TextCapsType:
        '''Apply all caps on the text.'''
        ...
    
    @classmethod
    @property
    def SMALL(cls) -> TextCapsType:
        '''Apply small caps to the text.'''
        ...
    
    ...

class TextCrossType:
    '''Enumerates displaying text type when the text width is larger than cell width.'''
    
    @classmethod
    @property
    def DEFAULT(cls) -> TextCrossType:
        '''Display text like in Microsoft Excel.'''
        ...
    
    @classmethod
    @property
    def CROSS_KEEP(cls) -> TextCrossType:
        '''Display all the text by crossing other cells and keep text of crossed cells.'''
        ...
    
    @classmethod
    @property
    def CROSS_OVERRIDE(cls) -> TextCrossType:
        '''Display all the text by crossing other cells and override text of crossed cells.'''
        ...
    
    @classmethod
    @property
    def STRICT_IN_CELL(cls) -> TextCrossType:
        '''Only display the text within the width of cell.'''
        ...
    
    ...

class TextDirectionType:
    '''Represents the direction of the text flow for this paragraph.'''
    
    @classmethod
    @property
    def CONTEXT(cls) -> TextDirectionType:
        ...
    
    @classmethod
    @property
    def LEFT_TO_RIGHT(cls) -> TextDirectionType:
        ...
    
    @classmethod
    @property
    def RIGHT_TO_LEFT(cls) -> TextDirectionType:
        ...
    
    ...

class TextOrientationType:
    '''Enumerates text orientation types.'''
    
    @classmethod
    @property
    def CLOCK_WISE(cls) -> TextOrientationType:
        '''Rotates text with 90 degrees clockwise.'''
        ...
    
    @classmethod
    @property
    def COUNTER_CLOCK_WISE(cls) -> TextOrientationType:
        '''Rotates text with 90 degrees counterclockwise.'''
        ...
    
    @classmethod
    @property
    def NO_ROTATION(cls) -> TextOrientationType:
        '''Represents the default value.'''
        ...
    
    @classmethod
    @property
    def TOP_TO_BOTTOM(cls) -> TextOrientationType:
        '''Displays text from top to bottom of the cell. Stacked text.'''
        ...
    
    ...

class TextStrikeType:
    '''This type specifies the strike type.'''
    
    @classmethod
    @property
    def SINGLE(cls) -> TextStrikeType:
        '''A single strikethrough applied on the text.'''
        ...
    
    @classmethod
    @property
    def DOUBLE(cls) -> TextStrikeType:
        '''A double strikethrough applied on the text.'''
        ...
    
    @classmethod
    @property
    def NONE(cls) -> TextStrikeType:
        '''No strike is applied to the text.'''
        ...
    
    ...

class ThemeColorType:
    '''Enumerates  the theme color types.'''
    
    @classmethod
    @property
    def BACKGROUND1(cls) -> ThemeColorType:
        ...
    
    @classmethod
    @property
    def TEXT1(cls) -> ThemeColorType:
        ...
    
    @classmethod
    @property
    def BACKGROUND2(cls) -> ThemeColorType:
        ...
    
    @classmethod
    @property
    def TEXT2(cls) -> ThemeColorType:
        ...
    
    @classmethod
    @property
    def ACCENT1(cls) -> ThemeColorType:
        ...
    
    @classmethod
    @property
    def ACCENT2(cls) -> ThemeColorType:
        ...
    
    @classmethod
    @property
    def ACCENT3(cls) -> ThemeColorType:
        ...
    
    @classmethod
    @property
    def ACCENT4(cls) -> ThemeColorType:
        ...
    
    @classmethod
    @property
    def ACCENT5(cls) -> ThemeColorType:
        ...
    
    @classmethod
    @property
    def ACCENT6(cls) -> ThemeColorType:
        ...
    
    @classmethod
    @property
    def HYPERLINK(cls) -> ThemeColorType:
        ...
    
    @classmethod
    @property
    def FOLLOWED_HYPERLINK(cls) -> ThemeColorType:
        ...
    
    @classmethod
    @property
    def STYLE_COLOR(cls) -> ThemeColorType:
        '''Inner used.
        A color used in theme definitions which means to use the color of the style.'''
        ...
    
    ...

class TimePeriodType:
    '''Used in a FormatConditionType.TimePeriod conditional formatting rule.
    These are dynamic time periods, which change based on
    the date the conditional formatting is refreshed / applied.'''
    
    @classmethod
    @property
    def TODAY(cls) -> TimePeriodType:
        '''Today's date.'''
        ...
    
    @classmethod
    @property
    def YESTERDAY(cls) -> TimePeriodType:
        '''Yesterday's date.'''
        ...
    
    @classmethod
    @property
    def TOMORROW(cls) -> TimePeriodType:
        '''Tomorrow's date.'''
        ...
    
    @classmethod
    @property
    def LAST_7_DAYS(cls) -> TimePeriodType:
        '''A date in the last seven days.'''
        ...
    
    @classmethod
    @property
    def THIS_MONTH(cls) -> TimePeriodType:
        '''A date occurring in this calendar month.'''
        ...
    
    @classmethod
    @property
    def LAST_MONTH(cls) -> TimePeriodType:
        '''A date occurring in the last calendar month.'''
        ...
    
    @classmethod
    @property
    def NEXT_MONTH(cls) -> TimePeriodType:
        '''A date occurring in the next calendar month.'''
        ...
    
    @classmethod
    @property
    def THIS_WEEK(cls) -> TimePeriodType:
        '''A date occurring this week.'''
        ...
    
    @classmethod
    @property
    def LAST_WEEK(cls) -> TimePeriodType:
        '''A date occurring last week.'''
        ...
    
    @classmethod
    @property
    def NEXT_WEEK(cls) -> TimePeriodType:
        '''A date occurring next week.'''
        ...
    
    @classmethod
    @property
    def THIS_YEAR(cls) -> TimePeriodType:
        '''A date occurring this year.
        Only for .ods.'''
        ...
    
    @classmethod
    @property
    def LAST_YEAR(cls) -> TimePeriodType:
        '''A date occurring last year.
        Only for .ods.'''
        ...
    
    @classmethod
    @property
    def NEXT_YEAR(cls) -> TimePeriodType:
        '''A date occurring next year.
        Only for .ods.'''
        ...
    
    ...

class TxtLoadStyleStrategy:
    '''Specifies how to apply style for parsed values when converting string value to number or datetime.'''
    
    @classmethod
    @property
    def NONE(cls) -> TxtLoadStyleStrategy:
        '''Does not set style for the parsed value.'''
        ...
    
    @classmethod
    @property
    def BUILT_IN(cls) -> TxtLoadStyleStrategy:
        '''Set the style as built-in number/datetime when the parsed value are plain numeric/datetime values.'''
        ...
    
    @classmethod
    @property
    def EXACT_FORMAT(cls) -> TxtLoadStyleStrategy:
        '''Set the exact custom format for the parsed value to make the formatted value be same with the original input one.'''
        ...
    
    ...

class TxtValueQuoteType:
    '''Specifies the type of using quotation marks for values in text format files.'''
    
    @classmethod
    @property
    def NORMAL(cls) -> TxtValueQuoteType:
        '''All values that contain special characters such as quotation mark, separator character will be quoted.
        Same with the behavior of ms excel for exporting text file.'''
        ...
    
    @classmethod
    @property
    def ALWAYS(cls) -> TxtValueQuoteType:
        '''All values will be quoted always.'''
        ...
    
    @classmethod
    @property
    def MINIMUM(cls) -> TxtValueQuoteType:
        '''Only quote values when needed. Such as, if one value contains quotation mark but the quotation mark is not at the begin of this value, this value will not be quoted.'''
        ...
    
    @classmethod
    @property
    def NEVER(cls) -> TxtValueQuoteType:
        '''All values will not be quoted. The exported text file with this type may not be read back correctly because the needed quotation marks being absent.'''
        ...
    
    ...

class UpdateLinksType:
    '''Represents how to update links to other workbooks when the workbook is opened.'''
    
    @classmethod
    @property
    def USER_SET(cls) -> UpdateLinksType:
        '''Prompt user to update.'''
        ...
    
    @classmethod
    @property
    def NEVER(cls) -> UpdateLinksType:
        '''Do not update, and do not prompt user.'''
        ...
    
    @classmethod
    @property
    def ALWAYS(cls) -> UpdateLinksType:
        '''Always update.'''
        ...
    
    ...

class ValidationAlertType:
    '''Represents the data validation alert style.'''
    
    @classmethod
    @property
    def INFORMATION(cls) -> ValidationAlertType:
        '''Information alert style.'''
        ...
    
    @classmethod
    @property
    def STOP(cls) -> ValidationAlertType:
        '''Stop alert style.'''
        ...
    
    @classmethod
    @property
    def WARNING(cls) -> ValidationAlertType:
        '''Warning alert style.'''
        ...
    
    ...

class ValidationType:
    '''Represents data validation type.'''
    
    @classmethod
    @property
    def ANY_VALUE(cls) -> ValidationType:
        '''Any value validation type.'''
        ...
    
    @classmethod
    @property
    def WHOLE_NUMBER(cls) -> ValidationType:
        '''Whole number validation type.'''
        ...
    
    @classmethod
    @property
    def DECIMAL(cls) -> ValidationType:
        '''Decimal validation type.'''
        ...
    
    @classmethod
    @property
    def LIST(cls) -> ValidationType:
        '''List validation type.'''
        ...
    
    @classmethod
    @property
    def DATE(cls) -> ValidationType:
        '''Date validation type.'''
        ...
    
    @classmethod
    @property
    def TIME(cls) -> ValidationType:
        '''Time validation type.'''
        ...
    
    @classmethod
    @property
    def TEXT_LENGTH(cls) -> ValidationType:
        '''Text length validation type.'''
        ...
    
    @classmethod
    @property
    def CUSTOM(cls) -> ValidationType:
        '''Custom validation type.'''
        ...
    
    ...

class ViewType:
    '''Represents the view type of the worksheet.'''
    
    @classmethod
    @property
    def NORMAL_VIEW(cls) -> ViewType:
        ...
    
    @classmethod
    @property
    def PAGE_BREAK_PREVIEW(cls) -> ViewType:
        ...
    
    @classmethod
    @property
    def PAGE_LAYOUT_VIEW(cls) -> ViewType:
        ...
    
    ...

class VisibilityType:
    '''Represents the states for sheet visibility.'''
    
    @classmethod
    @property
    def VISIBLE(cls) -> VisibilityType:
        '''Indicates the sheet is visible.'''
        ...
    
    @classmethod
    @property
    def HIDDEN(cls) -> VisibilityType:
        '''Indicates the sheet is hidden, but can be shown by the user via the user interface.'''
        ...
    
    @classmethod
    @property
    def VERY_HIDDEN(cls) -> VisibilityType:
        '''Indicates the sheet is hidden and cannot be shown in the user interface (UI).
        This state is only available programmatically.'''
        ...
    
    ...

class WarningType:
    '''WaringType'''
    
    @classmethod
    @property
    def FONT_SUBSTITUTION(cls) -> WarningType:
        '''Font substitution warning type
        when a font has not been found, this warning type can be get.'''
        ...
    
    @classmethod
    @property
    def DUPLICATE_DEFINED_NAME(cls) -> WarningType:
        '''Duplicate defined name is found in the file.'''
        ...
    
    @classmethod
    @property
    def UNSUPPORTED_FILE_FORMAT(cls) -> WarningType:
        '''Unsupported file format.'''
        ...
    
    @classmethod
    @property
    def INVALID_TEXT_OF_DEFINED_NAME(cls) -> WarningType:
        '''Invalid text of the defined name.'''
        ...
    
    @classmethod
    @property
    def INVALID_FONT_NAME(cls) -> WarningType:
        '''Invalid the font name.'''
        ...
    
    @classmethod
    @property
    def INVALID_AUTO_FILTER_RANGE(cls) -> WarningType:
        '''Invalid autofilter range.'''
        ...
    
    @classmethod
    @property
    def IO(cls) -> WarningType:
        '''The file is corrupted.'''
        ...
    
    @classmethod
    @property
    def LIMITATION(cls) -> WarningType:
        '''Out of MS Excel limitation error.'''
        ...
    
    @classmethod
    @property
    def INVALID_DATA(cls) -> WarningType:
        '''Invalid data.'''
        ...
    
    @classmethod
    @property
    def FORMULA(cls) -> WarningType:
        '''Invalid formula.'''
        ...
    
    @classmethod
    @property
    def INVALID_OPERATOR(cls) -> WarningType:
        '''Invalid operator.'''
        ...
    
    ...

