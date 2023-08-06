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

class ArcShape(Shape):
    '''Represents the arc shape.'''
    
    @overload
    def to_image(self, stream : io.RawIOBase, image_type : aspose.cells.drawing.ImageType):
        '''Creates the shape image and saves it to a stream in the specified format.
        
        :param stream: The output stream.
        :param image_type: The type in which to save the image.'''
        ...
    
    @overload
    def to_image(self, image_file : str, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a file.'''
        ...
    
    @overload
    def to_image(self, stream : io.RawIOBase, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a stream.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.'''
        ...
    
    def get_result_of_smart_art(self) -> aspose.cells.drawing.GroupShape:
        '''Converting smart art to grouped shapes.'''
        ...
    
    def to_front_or_back(self, orders : int):
        '''Brings the shape to the front or sends the shape to back.
        
        :param orders: If it's less than zero, sets the shape to back.
        If it's greater than zero, brings the shape to front.'''
        ...
    
    def get_locked_property(self, type : aspose.cells.drawing.ShapeLockType) -> bool:
        '''Gets the value of locked property.
        
        :param type: The type of the shape locked property.
        :returns: Returns  the value of locked property.'''
        ...
    
    def set_locked_property(self, type : aspose.cells.drawing.ShapeLockType, value : bool):
        '''Set the locked property.
        
        :param type: The locked type.
        :param value: The value of the property.'''
        ...
    
    def add_hyperlink(self, address : str) -> aspose.cells.Hyperlink:
        '''Adds a hyperlink to the shape.
        
        :param address: Address of the hyperlink.
        :returns: Return the new hyperlink object.'''
        ...
    
    def remove_hyperlink(self):
        '''Remove the hyperlink of the shape.'''
        ...
    
    def move_to_range(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int):
        '''Moves the shape to a specified range.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index'''
        ...
    
    def align_top_right_corner(self, top_row : int, right_column : int):
        '''Moves the picture to the top-right corner.
        
        :param top_row: the row index.
        :param right_column: the column index.'''
        ...
    
    def get_connection_points(self) -> List[List[float]]:
        '''Get the connection points
        
        :returns: [X,Y] pairs of the connection point. Every item is a float[2] array, [0] represents x and [1] represents y.'''
        ...
    
    def get_linked_cell(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range linked to the control's value.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range linked to the control's value.'''
        ...
    
    def set_linked_cell(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range linked to the control's value.
        
        :param formula: The range linked to the control's value.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def get_input_range(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range used to fill the control.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range used to fill the control.'''
        ...
    
    def set_input_range(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range used to fill the control.
        
        :param formula: The range used to fill the control.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell.'''
        ...
    
    def calculate_text_size(self) -> List[int]:
        '''Recalculate the text area
        
        :returns: Text's Size in an array(width and height).'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the text .
        
        :returns: All Characters objects'''
        ...
    
    def remove_active_x_control(self):
        '''Remove activeX control.'''
        ...
    
    def is_same_setting(self, obj : any) -> bool:
        '''Returns whether the shape is same.'''
        ...
    
    @property
    def macro_name(self) -> str:
        ...
    
    @macro_name.setter
    def macro_name(self, value : str):
        ...
    
    @property
    def is_equation(self) -> bool:
        ...
    
    @property
    def is_smart_art(self) -> bool:
        ...
    
    @property
    def z_order_position(self) -> int:
        ...
    
    @z_order_position.setter
    def z_order_position(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of the shape.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of the shape.'''
        ...
    
    @property
    def alternative_text(self) -> str:
        ...
    
    @alternative_text.setter
    def alternative_text(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @property
    def line_format(self) -> aspose.cells.drawing.MsoLineFormat:
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.MsoFillFormat:
        ...
    
    @property
    def format(self) -> aspose.cells.drawing.ShapeFormat:
        '''Represents the setting of the shape's formatting.'''
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        '''Gets line style'''
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        '''Returns a :py:attr:`aspose.cells.drawing.Shape.fill_format` object that contains fill formatting properties for the specified shape.'''
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def reflection(self) -> aspose.cells.drawing.ReflectionEffect:
        '''Represents a :py:class:`aspose.cells.drawing.ReflectionEffect` object that specifies reflection effect for the chart element or shape.'''
        ...
    
    @property
    def glow(self) -> aspose.cells.drawing.GlowEffect:
        '''Represents a :py:class:`aspose.cells.drawing.GlowEffect` object that specifies glow effect for the chart element or shape.'''
        ...
    
    @property
    def soft_edges(self) -> float:
        ...
    
    @soft_edges.setter
    def soft_edges(self, value : float):
        ...
    
    @property
    def three_d_format(self) -> aspose.cells.drawing.ThreeDFormat:
        ...
    
    @property
    def text_frame(self) -> aspose.cells.drawing.MsoTextFrame:
        ...
    
    @property
    def format_picture(self) -> aspose.cells.drawing.MsoFormatPicture:
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_lock_aspect_ratio(self) -> bool:
        ...
    
    @is_lock_aspect_ratio.setter
    def is_lock_aspect_ratio(self, value : bool):
        ...
    
    @property
    def rotation_angle(self) -> float:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : float):
        ...
    
    @property
    def hyperlink(self) -> aspose.cells.Hyperlink:
        '''Gets the hyperlink of the shape.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier of this shape.'''
        ...
    
    @property
    def spid(self) -> str:
        '''Specifies an optional string that an application can use to Identify the particular shape.'''
        ...
    
    @property
    def spt(self) -> int:
        '''Specifies an optional number that an application can use to associate the particular shape with a defined shape type.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.drawing.Shape.worksheet` object which contains this shape.'''
        ...
    
    @property
    def is_group(self) -> bool:
        ...
    
    @property
    def is_in_group(self) -> bool:
        ...
    
    @property
    def is_word_art(self) -> bool:
        ...
    
    @property
    def text_effect(self) -> aspose.cells.drawing.TextEffectFormat:
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_printable(self) -> bool:
        ...
    
    @is_printable.setter
    def is_printable(self, value : bool):
        ...
    
    @property
    def mso_drawing_type(self) -> aspose.cells.drawing.MsoDrawingType:
        ...
    
    @property
    def auto_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @auto_shape_type.setter
    def auto_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def anchor_type(self) -> aspose.cells.drawing.ShapeAnchorType:
        ...
    
    @anchor_type.setter
    def anchor_type(self, value : aspose.cells.drawing.ShapeAnchorType):
        ...
    
    @property
    def placement(self) -> aspose.cells.drawing.PlacementType:
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @placement.setter
    def placement(self, value : aspose.cells.drawing.PlacementType):
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @property
    def upper_left_row(self) -> int:
        ...
    
    @upper_left_row.setter
    def upper_left_row(self, value : int):
        ...
    
    @property
    def upper_delta_y(self) -> int:
        ...
    
    @upper_delta_y.setter
    def upper_delta_y(self, value : int):
        ...
    
    @property
    def upper_left_column(self) -> int:
        ...
    
    @upper_left_column.setter
    def upper_left_column(self, value : int):
        ...
    
    @property
    def upper_delta_x(self) -> int:
        ...
    
    @upper_delta_x.setter
    def upper_delta_x(self, value : int):
        ...
    
    @property
    def lower_right_row(self) -> int:
        ...
    
    @lower_right_row.setter
    def lower_right_row(self, value : int):
        ...
    
    @property
    def lower_delta_y(self) -> int:
        ...
    
    @lower_delta_y.setter
    def lower_delta_y(self, value : int):
        ...
    
    @property
    def lower_right_column(self) -> int:
        ...
    
    @lower_right_column.setter
    def lower_right_column(self, value : int):
        ...
    
    @property
    def lower_delta_x(self) -> int:
        ...
    
    @lower_delta_x.setter
    def lower_delta_x(self, value : int):
        ...
    
    @property
    def right(self) -> int:
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def width_pt(self) -> float:
        ...
    
    @width_pt.setter
    def width_pt(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def height(self) -> int:
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    @property
    def height_pt(self) -> float:
        ...
    
    @height_pt.setter
    def height_pt(self, value : float):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def left(self) -> int:
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @property
    def left_inch(self) -> float:
        ...
    
    @left_inch.setter
    def left_inch(self, value : float):
        ...
    
    @property
    def left_cm(self) -> float:
        ...
    
    @left_cm.setter
    def left_cm(self, value : float):
        ...
    
    @property
    def top(self) -> int:
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @property
    def top_inch(self) -> float:
        ...
    
    @top_inch.setter
    def top_inch(self, value : float):
        ...
    
    @property
    def top_cm(self) -> float:
        ...
    
    @top_cm.setter
    def top_cm(self, value : float):
        ...
    
    @property
    def top_to_corner(self) -> int:
        ...
    
    @top_to_corner.setter
    def top_to_corner(self, value : int):
        ...
    
    @property
    def left_to_corner(self) -> int:
        ...
    
    @left_to_corner.setter
    def left_to_corner(self, value : int):
        ...
    
    @property
    def x(self) -> int:
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @property
    def width_scale(self) -> int:
        ...
    
    @width_scale.setter
    def width_scale(self, value : int):
        ...
    
    @property
    def height_scale(self) -> int:
        ...
    
    @height_scale.setter
    def height_scale(self, value : int):
        ...
    
    @property
    def top_in_shape(self) -> int:
        ...
    
    @top_in_shape.setter
    def top_in_shape(self, value : int):
        ...
    
    @property
    def left_in_shape(self) -> int:
        ...
    
    @left_in_shape.setter
    def left_in_shape(self, value : int):
        ...
    
    @property
    def width_in_shape(self) -> int:
        ...
    
    @width_in_shape.setter
    def width_in_shape(self, value : int):
        ...
    
    @property
    def height_in_shape(self) -> int:
        ...
    
    @height_in_shape.setter
    def height_in_shape(self, value : int):
        ...
    
    @property
    def group(self) -> aspose.cells.drawing.GroupShape:
        '''Gets the group shape which contains this shape.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.AutoShapeType:
        '''Gets the auto shape type.'''
        ...
    
    @property
    def has_line(self) -> bool:
        ...
    
    @has_line.setter
    def has_line(self, value : bool):
        ...
    
    @property
    def is_filled(self) -> bool:
        ...
    
    @is_filled.setter
    def is_filled(self, value : bool):
        ...
    
    @property
    def is_flipped_horizontally(self) -> bool:
        ...
    
    @is_flipped_horizontally.setter
    def is_flipped_horizontally(self, value : bool):
        ...
    
    @property
    def is_flipped_vertically(self) -> bool:
        ...
    
    @is_flipped_vertically.setter
    def is_flipped_vertically(self, value : bool):
        ...
    
    @property
    def actual_lower_right_row(self) -> int:
        ...
    
    @property
    def connection_points(self) -> aspose.pydrawing.PointF[]:
        ...
    
    @property
    def relative_to_original_picture_size(self) -> bool:
        ...
    
    @relative_to_original_picture_size.setter
    def relative_to_original_picture_size(self, value : bool):
        ...
    
    @property
    def linked_cell(self) -> str:
        ...
    
    @linked_cell.setter
    def linked_cell(self, value : str):
        ...
    
    @property
    def input_range(self) -> str:
        ...
    
    @input_range.setter
    def input_range(self, value : str):
        ...
    
    @property
    def text_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @text_shape_type.setter
    def text_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def text_body(self) -> aspose.cells.drawing.texts.FontSettingCollection:
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Represents the font of shape.'''
        ...
    
    @font.setter
    def font(self, value : aspose.cells.Font):
        '''Represents the font of shape.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    @text_options.setter
    def text_options(self, value : aspose.cells.drawing.texts.TextOptions):
        ...
    
    @property
    def text(self) -> str:
        '''Represents the string in this TextBox object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Represents the string in this TextBox object.'''
        ...
    
    @property
    def is_rich_text(self) -> bool:
        ...
    
    @property
    def html_text(self) -> str:
        ...
    
    @html_text.setter
    def html_text(self, value : str):
        ...
    
    @property
    def text_vertical_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_vertical_overflow.setter
    def text_vertical_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def text_horizontal_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_horizontal_overflow.setter
    def text_horizontal_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
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
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def control_data(self) -> bytes:
        ...
    
    @property
    def active_x_control(self) -> aspose.cells.drawing.activexcontrols.ActiveXControl:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets the paths of a custom geometric shape.'''
        ...
    
    @property
    def geometry(self) -> aspose.cells.drawing.Geometry:
        '''Gets the geometry'''
        ...
    
    @property
    def create_id(self) -> Guid:
        ...
    
    @create_id.setter
    def create_id(self, value : Guid):
        ...
    
    @property
    def begin_arrowhead_style(self) -> aspose.cells.drawing.MsoArrowheadStyle:
        ...
    
    @begin_arrowhead_style.setter
    def begin_arrowhead_style(self, value : aspose.cells.drawing.MsoArrowheadStyle):
        ...
    
    @property
    def begin_arrowhead_width(self) -> aspose.cells.drawing.MsoArrowheadWidth:
        ...
    
    @begin_arrowhead_width.setter
    def begin_arrowhead_width(self, value : aspose.cells.drawing.MsoArrowheadWidth):
        ...
    
    @property
    def begin_arrowhead_length(self) -> aspose.cells.drawing.MsoArrowheadLength:
        ...
    
    @begin_arrowhead_length.setter
    def begin_arrowhead_length(self, value : aspose.cells.drawing.MsoArrowheadLength):
        ...
    
    @property
    def end_arrowhead_style(self) -> aspose.cells.drawing.MsoArrowheadStyle:
        ...
    
    @end_arrowhead_style.setter
    def end_arrowhead_style(self, value : aspose.cells.drawing.MsoArrowheadStyle):
        ...
    
    @property
    def end_arrowhead_width(self) -> aspose.cells.drawing.MsoArrowheadWidth:
        ...
    
    @end_arrowhead_width.setter
    def end_arrowhead_width(self, value : aspose.cells.drawing.MsoArrowheadWidth):
        ...
    
    @property
    def end_arrowhead_length(self) -> aspose.cells.drawing.MsoArrowheadLength:
        ...
    
    @end_arrowhead_length.setter
    def end_arrowhead_length(self, value : aspose.cells.drawing.MsoArrowheadLength):
        ...
    
    ...

class Area:
    '''Encapsulates the object that represents an area format.'''
    
    @property
    def background_color(self) -> aspose.pydrawing.Color:
        ...
    
    @background_color.setter
    def background_color(self, value : aspose.pydrawing.Color):
        ...
    
    @property
    def foreground_color(self) -> aspose.pydrawing.Color:
        ...
    
    @foreground_color.setter
    def foreground_color(self, value : aspose.pydrawing.Color):
        ...
    
    @property
    def formatting(self) -> aspose.cells.charts.FormattingType:
        '''Represents the formatting of the area.'''
        ...
    
    @formatting.setter
    def formatting(self, value : aspose.cells.charts.FormattingType):
        '''Represents the formatting of the area.'''
        ...
    
    @property
    def invert_if_negative(self) -> bool:
        ...
    
    @invert_if_negative.setter
    def invert_if_negative(self, value : bool):
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.FillFormat:
        ...
    
    @property
    def transparency(self) -> float:
        '''Returns the degree of transparency of the area as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    @transparency.setter
    def transparency(self, value : float):
        '''Returns or sets the degree of transparency of the area as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    ...

class AutomaticFill(Fill):
    '''represents automatic fill.'''
    
    ...

class BaseShapeGuide:
    '''Represents the shape guide.'''
    
    ...

class Bevel:
    '''Represents a bevel of a shape'''
    
    @property
    def width(self) -> float:
        '''Gets and sets the width of the bevel, or how far into the shape it is applied.
        In unit of Points.'''
        ...
    
    @width.setter
    def width(self, value : float):
        '''Gets and sets the width of the bevel, or how far into the shape it is applied.
        In unit of Points.'''
        ...
    
    @property
    def height(self) -> float:
        '''Gets and sets the height of the bevel, or how far above the shape it is applied.
        In unit of Points.'''
        ...
    
    @height.setter
    def height(self, value : float):
        '''Gets and sets the height of the bevel, or how far above the shape it is applied.
        In unit of Points.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.BevelPresetType:
        '''Gets and sets the preset bevel type.'''
        ...
    
    @type.setter
    def type(self, value : aspose.cells.drawing.BevelPresetType):
        '''Gets and sets the preset bevel type.'''
        ...
    
    ...

class Button(Shape):
    '''Represents the Forms control: Button'''
    
    @overload
    def to_image(self, stream : io.RawIOBase, image_type : aspose.cells.drawing.ImageType):
        '''Creates the shape image and saves it to a stream in the specified format.
        
        :param stream: The output stream.
        :param image_type: The type in which to save the image.'''
        ...
    
    @overload
    def to_image(self, image_file : str, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a file.'''
        ...
    
    @overload
    def to_image(self, stream : io.RawIOBase, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a stream.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.'''
        ...
    
    def get_result_of_smart_art(self) -> aspose.cells.drawing.GroupShape:
        '''Converting smart art to grouped shapes.'''
        ...
    
    def to_front_or_back(self, orders : int):
        '''Brings the shape to the front or sends the shape to back.
        
        :param orders: If it's less than zero, sets the shape to back.
        If it's greater than zero, brings the shape to front.'''
        ...
    
    def get_locked_property(self, type : aspose.cells.drawing.ShapeLockType) -> bool:
        '''Gets the value of locked property.
        
        :param type: The type of the shape locked property.
        :returns: Returns  the value of locked property.'''
        ...
    
    def set_locked_property(self, type : aspose.cells.drawing.ShapeLockType, value : bool):
        '''Set the locked property.
        
        :param type: The locked type.
        :param value: The value of the property.'''
        ...
    
    def add_hyperlink(self, address : str) -> aspose.cells.Hyperlink:
        '''Adds a hyperlink to the shape.
        
        :param address: Address of the hyperlink.
        :returns: Return the new hyperlink object.'''
        ...
    
    def remove_hyperlink(self):
        '''Remove the hyperlink of the shape.'''
        ...
    
    def move_to_range(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int):
        '''Moves the shape to a specified range.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index'''
        ...
    
    def align_top_right_corner(self, top_row : int, right_column : int):
        '''Moves the picture to the top-right corner.
        
        :param top_row: the row index.
        :param right_column: the column index.'''
        ...
    
    def get_connection_points(self) -> List[List[float]]:
        '''Get the connection points
        
        :returns: [X,Y] pairs of the connection point. Every item is a float[2] array, [0] represents x and [1] represents y.'''
        ...
    
    def get_linked_cell(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range linked to the control's value.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range linked to the control's value.'''
        ...
    
    def set_linked_cell(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range linked to the control's value.
        
        :param formula: The range linked to the control's value.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def get_input_range(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range used to fill the control.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range used to fill the control.'''
        ...
    
    def set_input_range(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range used to fill the control.
        
        :param formula: The range used to fill the control.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell.'''
        ...
    
    def calculate_text_size(self) -> List[int]:
        '''Recalculate the text area
        
        :returns: Text's Size in an array(width and height).'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the text .
        
        :returns: All Characters objects'''
        ...
    
    def remove_active_x_control(self):
        '''Remove activeX control.'''
        ...
    
    def is_same_setting(self, obj : any) -> bool:
        '''Returns whether the shape is same.'''
        ...
    
    @property
    def macro_name(self) -> str:
        ...
    
    @macro_name.setter
    def macro_name(self, value : str):
        ...
    
    @property
    def is_equation(self) -> bool:
        ...
    
    @property
    def is_smart_art(self) -> bool:
        ...
    
    @property
    def z_order_position(self) -> int:
        ...
    
    @z_order_position.setter
    def z_order_position(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of the shape.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of the shape.'''
        ...
    
    @property
    def alternative_text(self) -> str:
        ...
    
    @alternative_text.setter
    def alternative_text(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @property
    def line_format(self) -> aspose.cells.drawing.MsoLineFormat:
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.MsoFillFormat:
        ...
    
    @property
    def format(self) -> aspose.cells.drawing.ShapeFormat:
        '''Represents the setting of the shape's formatting.'''
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        '''Gets line style'''
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        '''Returns a :py:attr:`aspose.cells.drawing.Shape.fill_format` object that contains fill formatting properties for the specified shape.'''
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def reflection(self) -> aspose.cells.drawing.ReflectionEffect:
        '''Represents a :py:class:`aspose.cells.drawing.ReflectionEffect` object that specifies reflection effect for the chart element or shape.'''
        ...
    
    @property
    def glow(self) -> aspose.cells.drawing.GlowEffect:
        '''Represents a :py:class:`aspose.cells.drawing.GlowEffect` object that specifies glow effect for the chart element or shape.'''
        ...
    
    @property
    def soft_edges(self) -> float:
        ...
    
    @soft_edges.setter
    def soft_edges(self, value : float):
        ...
    
    @property
    def three_d_format(self) -> aspose.cells.drawing.ThreeDFormat:
        ...
    
    @property
    def text_frame(self) -> aspose.cells.drawing.MsoTextFrame:
        ...
    
    @property
    def format_picture(self) -> aspose.cells.drawing.MsoFormatPicture:
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_lock_aspect_ratio(self) -> bool:
        ...
    
    @is_lock_aspect_ratio.setter
    def is_lock_aspect_ratio(self, value : bool):
        ...
    
    @property
    def rotation_angle(self) -> float:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : float):
        ...
    
    @property
    def hyperlink(self) -> aspose.cells.Hyperlink:
        '''Gets the hyperlink of the shape.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier of this shape.'''
        ...
    
    @property
    def spid(self) -> str:
        '''Specifies an optional string that an application can use to Identify the particular shape.'''
        ...
    
    @property
    def spt(self) -> int:
        '''Specifies an optional number that an application can use to associate the particular shape with a defined shape type.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.drawing.Shape.worksheet` object which contains this shape.'''
        ...
    
    @property
    def is_group(self) -> bool:
        ...
    
    @property
    def is_in_group(self) -> bool:
        ...
    
    @property
    def is_word_art(self) -> bool:
        ...
    
    @property
    def text_effect(self) -> aspose.cells.drawing.TextEffectFormat:
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_printable(self) -> bool:
        ...
    
    @is_printable.setter
    def is_printable(self, value : bool):
        ...
    
    @property
    def mso_drawing_type(self) -> aspose.cells.drawing.MsoDrawingType:
        ...
    
    @property
    def auto_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @auto_shape_type.setter
    def auto_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def anchor_type(self) -> aspose.cells.drawing.ShapeAnchorType:
        ...
    
    @anchor_type.setter
    def anchor_type(self, value : aspose.cells.drawing.ShapeAnchorType):
        ...
    
    @property
    def placement(self) -> aspose.cells.drawing.PlacementType:
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @placement.setter
    def placement(self, value : aspose.cells.drawing.PlacementType):
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @property
    def upper_left_row(self) -> int:
        ...
    
    @upper_left_row.setter
    def upper_left_row(self, value : int):
        ...
    
    @property
    def upper_delta_y(self) -> int:
        ...
    
    @upper_delta_y.setter
    def upper_delta_y(self, value : int):
        ...
    
    @property
    def upper_left_column(self) -> int:
        ...
    
    @upper_left_column.setter
    def upper_left_column(self, value : int):
        ...
    
    @property
    def upper_delta_x(self) -> int:
        ...
    
    @upper_delta_x.setter
    def upper_delta_x(self, value : int):
        ...
    
    @property
    def lower_right_row(self) -> int:
        ...
    
    @lower_right_row.setter
    def lower_right_row(self, value : int):
        ...
    
    @property
    def lower_delta_y(self) -> int:
        ...
    
    @lower_delta_y.setter
    def lower_delta_y(self, value : int):
        ...
    
    @property
    def lower_right_column(self) -> int:
        ...
    
    @lower_right_column.setter
    def lower_right_column(self, value : int):
        ...
    
    @property
    def lower_delta_x(self) -> int:
        ...
    
    @lower_delta_x.setter
    def lower_delta_x(self, value : int):
        ...
    
    @property
    def right(self) -> int:
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def width_pt(self) -> float:
        ...
    
    @width_pt.setter
    def width_pt(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def height(self) -> int:
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    @property
    def height_pt(self) -> float:
        ...
    
    @height_pt.setter
    def height_pt(self, value : float):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def left(self) -> int:
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @property
    def left_inch(self) -> float:
        ...
    
    @left_inch.setter
    def left_inch(self, value : float):
        ...
    
    @property
    def left_cm(self) -> float:
        ...
    
    @left_cm.setter
    def left_cm(self, value : float):
        ...
    
    @property
    def top(self) -> int:
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @property
    def top_inch(self) -> float:
        ...
    
    @top_inch.setter
    def top_inch(self, value : float):
        ...
    
    @property
    def top_cm(self) -> float:
        ...
    
    @top_cm.setter
    def top_cm(self, value : float):
        ...
    
    @property
    def top_to_corner(self) -> int:
        ...
    
    @top_to_corner.setter
    def top_to_corner(self, value : int):
        ...
    
    @property
    def left_to_corner(self) -> int:
        ...
    
    @left_to_corner.setter
    def left_to_corner(self, value : int):
        ...
    
    @property
    def x(self) -> int:
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @property
    def width_scale(self) -> int:
        ...
    
    @width_scale.setter
    def width_scale(self, value : int):
        ...
    
    @property
    def height_scale(self) -> int:
        ...
    
    @height_scale.setter
    def height_scale(self, value : int):
        ...
    
    @property
    def top_in_shape(self) -> int:
        ...
    
    @top_in_shape.setter
    def top_in_shape(self, value : int):
        ...
    
    @property
    def left_in_shape(self) -> int:
        ...
    
    @left_in_shape.setter
    def left_in_shape(self, value : int):
        ...
    
    @property
    def width_in_shape(self) -> int:
        ...
    
    @width_in_shape.setter
    def width_in_shape(self, value : int):
        ...
    
    @property
    def height_in_shape(self) -> int:
        ...
    
    @height_in_shape.setter
    def height_in_shape(self, value : int):
        ...
    
    @property
    def group(self) -> aspose.cells.drawing.GroupShape:
        '''Gets the group shape which contains this shape.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.AutoShapeType:
        '''Gets the auto shape type.'''
        ...
    
    @property
    def has_line(self) -> bool:
        ...
    
    @has_line.setter
    def has_line(self, value : bool):
        ...
    
    @property
    def is_filled(self) -> bool:
        ...
    
    @is_filled.setter
    def is_filled(self, value : bool):
        ...
    
    @property
    def is_flipped_horizontally(self) -> bool:
        ...
    
    @is_flipped_horizontally.setter
    def is_flipped_horizontally(self, value : bool):
        ...
    
    @property
    def is_flipped_vertically(self) -> bool:
        ...
    
    @is_flipped_vertically.setter
    def is_flipped_vertically(self, value : bool):
        ...
    
    @property
    def actual_lower_right_row(self) -> int:
        ...
    
    @property
    def connection_points(self) -> aspose.pydrawing.PointF[]:
        ...
    
    @property
    def relative_to_original_picture_size(self) -> bool:
        ...
    
    @relative_to_original_picture_size.setter
    def relative_to_original_picture_size(self, value : bool):
        ...
    
    @property
    def linked_cell(self) -> str:
        ...
    
    @linked_cell.setter
    def linked_cell(self, value : str):
        ...
    
    @property
    def input_range(self) -> str:
        ...
    
    @input_range.setter
    def input_range(self, value : str):
        ...
    
    @property
    def text_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @text_shape_type.setter
    def text_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def text_body(self) -> aspose.cells.drawing.texts.FontSettingCollection:
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Represents the font of shape.'''
        ...
    
    @font.setter
    def font(self, value : aspose.cells.Font):
        '''Represents the font of shape.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    @text_options.setter
    def text_options(self, value : aspose.cells.drawing.texts.TextOptions):
        ...
    
    @property
    def text(self) -> str:
        '''Represents the string in this TextBox object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Represents the string in this TextBox object.'''
        ...
    
    @property
    def is_rich_text(self) -> bool:
        ...
    
    @property
    def html_text(self) -> str:
        ...
    
    @html_text.setter
    def html_text(self, value : str):
        ...
    
    @property
    def text_vertical_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_vertical_overflow.setter
    def text_vertical_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def text_horizontal_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_horizontal_overflow.setter
    def text_horizontal_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
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
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def control_data(self) -> bytes:
        ...
    
    @property
    def active_x_control(self) -> aspose.cells.drawing.activexcontrols.ActiveXControl:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets the paths of a custom geometric shape.'''
        ...
    
    @property
    def geometry(self) -> aspose.cells.drawing.Geometry:
        '''Gets the geometry'''
        ...
    
    @property
    def create_id(self) -> Guid:
        ...
    
    @create_id.setter
    def create_id(self, value : Guid):
        ...
    
    ...

class CellsDrawing(Shape):
    '''Represents the auto shape and drawing object.'''
    
    @overload
    def to_image(self, stream : io.RawIOBase, image_type : aspose.cells.drawing.ImageType):
        '''Creates the shape image and saves it to a stream in the specified format.
        
        :param stream: The output stream.
        :param image_type: The type in which to save the image.'''
        ...
    
    @overload
    def to_image(self, image_file : str, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a file.'''
        ...
    
    @overload
    def to_image(self, stream : io.RawIOBase, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a stream.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.'''
        ...
    
    def get_result_of_smart_art(self) -> aspose.cells.drawing.GroupShape:
        '''Converting smart art to grouped shapes.'''
        ...
    
    def to_front_or_back(self, orders : int):
        '''Brings the shape to the front or sends the shape to back.
        
        :param orders: If it's less than zero, sets the shape to back.
        If it's greater than zero, brings the shape to front.'''
        ...
    
    def get_locked_property(self, type : aspose.cells.drawing.ShapeLockType) -> bool:
        '''Gets the value of locked property.
        
        :param type: The type of the shape locked property.
        :returns: Returns  the value of locked property.'''
        ...
    
    def set_locked_property(self, type : aspose.cells.drawing.ShapeLockType, value : bool):
        '''Set the locked property.
        
        :param type: The locked type.
        :param value: The value of the property.'''
        ...
    
    def add_hyperlink(self, address : str) -> aspose.cells.Hyperlink:
        '''Adds a hyperlink to the shape.
        
        :param address: Address of the hyperlink.
        :returns: Return the new hyperlink object.'''
        ...
    
    def remove_hyperlink(self):
        '''Remove the hyperlink of the shape.'''
        ...
    
    def move_to_range(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int):
        '''Moves the shape to a specified range.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index'''
        ...
    
    def align_top_right_corner(self, top_row : int, right_column : int):
        '''Moves the picture to the top-right corner.
        
        :param top_row: the row index.
        :param right_column: the column index.'''
        ...
    
    def get_connection_points(self) -> List[List[float]]:
        '''Get the connection points
        
        :returns: [X,Y] pairs of the connection point. Every item is a float[2] array, [0] represents x and [1] represents y.'''
        ...
    
    def get_linked_cell(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range linked to the control's value.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range linked to the control's value.'''
        ...
    
    def set_linked_cell(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range linked to the control's value.
        
        :param formula: The range linked to the control's value.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def get_input_range(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range used to fill the control.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range used to fill the control.'''
        ...
    
    def set_input_range(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range used to fill the control.
        
        :param formula: The range used to fill the control.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell.'''
        ...
    
    def calculate_text_size(self) -> List[int]:
        '''Recalculate the text area
        
        :returns: Text's Size in an array(width and height).'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the text .
        
        :returns: All Characters objects'''
        ...
    
    def remove_active_x_control(self):
        '''Remove activeX control.'''
        ...
    
    def is_same_setting(self, obj : any) -> bool:
        '''Returns whether the shape is same.'''
        ...
    
    @property
    def macro_name(self) -> str:
        ...
    
    @macro_name.setter
    def macro_name(self, value : str):
        ...
    
    @property
    def is_equation(self) -> bool:
        ...
    
    @property
    def is_smart_art(self) -> bool:
        ...
    
    @property
    def z_order_position(self) -> int:
        ...
    
    @z_order_position.setter
    def z_order_position(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of the shape.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of the shape.'''
        ...
    
    @property
    def alternative_text(self) -> str:
        ...
    
    @alternative_text.setter
    def alternative_text(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @property
    def line_format(self) -> aspose.cells.drawing.MsoLineFormat:
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.MsoFillFormat:
        ...
    
    @property
    def format(self) -> aspose.cells.drawing.ShapeFormat:
        '''Represents the setting of the shape's formatting.'''
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        '''Gets line style'''
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        '''Returns a :py:attr:`aspose.cells.drawing.Shape.fill_format` object that contains fill formatting properties for the specified shape.'''
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def reflection(self) -> aspose.cells.drawing.ReflectionEffect:
        '''Represents a :py:class:`aspose.cells.drawing.ReflectionEffect` object that specifies reflection effect for the chart element or shape.'''
        ...
    
    @property
    def glow(self) -> aspose.cells.drawing.GlowEffect:
        '''Represents a :py:class:`aspose.cells.drawing.GlowEffect` object that specifies glow effect for the chart element or shape.'''
        ...
    
    @property
    def soft_edges(self) -> float:
        ...
    
    @soft_edges.setter
    def soft_edges(self, value : float):
        ...
    
    @property
    def three_d_format(self) -> aspose.cells.drawing.ThreeDFormat:
        ...
    
    @property
    def text_frame(self) -> aspose.cells.drawing.MsoTextFrame:
        ...
    
    @property
    def format_picture(self) -> aspose.cells.drawing.MsoFormatPicture:
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_lock_aspect_ratio(self) -> bool:
        ...
    
    @is_lock_aspect_ratio.setter
    def is_lock_aspect_ratio(self, value : bool):
        ...
    
    @property
    def rotation_angle(self) -> float:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : float):
        ...
    
    @property
    def hyperlink(self) -> aspose.cells.Hyperlink:
        '''Gets the hyperlink of the shape.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier of this shape.'''
        ...
    
    @property
    def spid(self) -> str:
        '''Specifies an optional string that an application can use to Identify the particular shape.'''
        ...
    
    @property
    def spt(self) -> int:
        '''Specifies an optional number that an application can use to associate the particular shape with a defined shape type.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.drawing.Shape.worksheet` object which contains this shape.'''
        ...
    
    @property
    def is_group(self) -> bool:
        ...
    
    @property
    def is_in_group(self) -> bool:
        ...
    
    @property
    def is_word_art(self) -> bool:
        ...
    
    @property
    def text_effect(self) -> aspose.cells.drawing.TextEffectFormat:
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_printable(self) -> bool:
        ...
    
    @is_printable.setter
    def is_printable(self, value : bool):
        ...
    
    @property
    def mso_drawing_type(self) -> aspose.cells.drawing.MsoDrawingType:
        ...
    
    @property
    def auto_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @auto_shape_type.setter
    def auto_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def anchor_type(self) -> aspose.cells.drawing.ShapeAnchorType:
        ...
    
    @anchor_type.setter
    def anchor_type(self, value : aspose.cells.drawing.ShapeAnchorType):
        ...
    
    @property
    def placement(self) -> aspose.cells.drawing.PlacementType:
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @placement.setter
    def placement(self, value : aspose.cells.drawing.PlacementType):
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @property
    def upper_left_row(self) -> int:
        ...
    
    @upper_left_row.setter
    def upper_left_row(self, value : int):
        ...
    
    @property
    def upper_delta_y(self) -> int:
        ...
    
    @upper_delta_y.setter
    def upper_delta_y(self, value : int):
        ...
    
    @property
    def upper_left_column(self) -> int:
        ...
    
    @upper_left_column.setter
    def upper_left_column(self, value : int):
        ...
    
    @property
    def upper_delta_x(self) -> int:
        ...
    
    @upper_delta_x.setter
    def upper_delta_x(self, value : int):
        ...
    
    @property
    def lower_right_row(self) -> int:
        ...
    
    @lower_right_row.setter
    def lower_right_row(self, value : int):
        ...
    
    @property
    def lower_delta_y(self) -> int:
        ...
    
    @lower_delta_y.setter
    def lower_delta_y(self, value : int):
        ...
    
    @property
    def lower_right_column(self) -> int:
        ...
    
    @lower_right_column.setter
    def lower_right_column(self, value : int):
        ...
    
    @property
    def lower_delta_x(self) -> int:
        ...
    
    @lower_delta_x.setter
    def lower_delta_x(self, value : int):
        ...
    
    @property
    def right(self) -> int:
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def width_pt(self) -> float:
        ...
    
    @width_pt.setter
    def width_pt(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def height(self) -> int:
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    @property
    def height_pt(self) -> float:
        ...
    
    @height_pt.setter
    def height_pt(self, value : float):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def left(self) -> int:
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @property
    def left_inch(self) -> float:
        ...
    
    @left_inch.setter
    def left_inch(self, value : float):
        ...
    
    @property
    def left_cm(self) -> float:
        ...
    
    @left_cm.setter
    def left_cm(self, value : float):
        ...
    
    @property
    def top(self) -> int:
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @property
    def top_inch(self) -> float:
        ...
    
    @top_inch.setter
    def top_inch(self, value : float):
        ...
    
    @property
    def top_cm(self) -> float:
        ...
    
    @top_cm.setter
    def top_cm(self, value : float):
        ...
    
    @property
    def top_to_corner(self) -> int:
        ...
    
    @top_to_corner.setter
    def top_to_corner(self, value : int):
        ...
    
    @property
    def left_to_corner(self) -> int:
        ...
    
    @left_to_corner.setter
    def left_to_corner(self, value : int):
        ...
    
    @property
    def x(self) -> int:
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @property
    def width_scale(self) -> int:
        ...
    
    @width_scale.setter
    def width_scale(self, value : int):
        ...
    
    @property
    def height_scale(self) -> int:
        ...
    
    @height_scale.setter
    def height_scale(self, value : int):
        ...
    
    @property
    def top_in_shape(self) -> int:
        ...
    
    @top_in_shape.setter
    def top_in_shape(self, value : int):
        ...
    
    @property
    def left_in_shape(self) -> int:
        ...
    
    @left_in_shape.setter
    def left_in_shape(self, value : int):
        ...
    
    @property
    def width_in_shape(self) -> int:
        ...
    
    @width_in_shape.setter
    def width_in_shape(self, value : int):
        ...
    
    @property
    def height_in_shape(self) -> int:
        ...
    
    @height_in_shape.setter
    def height_in_shape(self, value : int):
        ...
    
    @property
    def group(self) -> aspose.cells.drawing.GroupShape:
        '''Gets the group shape which contains this shape.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.AutoShapeType:
        '''Gets the auto shape type.'''
        ...
    
    @property
    def has_line(self) -> bool:
        ...
    
    @has_line.setter
    def has_line(self, value : bool):
        ...
    
    @property
    def is_filled(self) -> bool:
        ...
    
    @is_filled.setter
    def is_filled(self, value : bool):
        ...
    
    @property
    def is_flipped_horizontally(self) -> bool:
        ...
    
    @is_flipped_horizontally.setter
    def is_flipped_horizontally(self, value : bool):
        ...
    
    @property
    def is_flipped_vertically(self) -> bool:
        ...
    
    @is_flipped_vertically.setter
    def is_flipped_vertically(self, value : bool):
        ...
    
    @property
    def actual_lower_right_row(self) -> int:
        ...
    
    @property
    def connection_points(self) -> aspose.pydrawing.PointF[]:
        ...
    
    @property
    def relative_to_original_picture_size(self) -> bool:
        ...
    
    @relative_to_original_picture_size.setter
    def relative_to_original_picture_size(self, value : bool):
        ...
    
    @property
    def linked_cell(self) -> str:
        ...
    
    @linked_cell.setter
    def linked_cell(self, value : str):
        ...
    
    @property
    def input_range(self) -> str:
        ...
    
    @input_range.setter
    def input_range(self, value : str):
        ...
    
    @property
    def text_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @text_shape_type.setter
    def text_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def text_body(self) -> aspose.cells.drawing.texts.FontSettingCollection:
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Represents the font of shape.'''
        ...
    
    @font.setter
    def font(self, value : aspose.cells.Font):
        '''Represents the font of shape.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    @text_options.setter
    def text_options(self, value : aspose.cells.drawing.texts.TextOptions):
        ...
    
    @property
    def text(self) -> str:
        '''Represents the string in this TextBox object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Represents the string in this TextBox object.'''
        ...
    
    @property
    def is_rich_text(self) -> bool:
        ...
    
    @property
    def html_text(self) -> str:
        ...
    
    @html_text.setter
    def html_text(self, value : str):
        ...
    
    @property
    def text_vertical_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_vertical_overflow.setter
    def text_vertical_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def text_horizontal_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_horizontal_overflow.setter
    def text_horizontal_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
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
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def control_data(self) -> bytes:
        ...
    
    @property
    def active_x_control(self) -> aspose.cells.drawing.activexcontrols.ActiveXControl:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets the paths of a custom geometric shape.'''
        ...
    
    @property
    def geometry(self) -> aspose.cells.drawing.Geometry:
        '''Gets the geometry'''
        ...
    
    @property
    def create_id(self) -> Guid:
        ...
    
    @create_id.setter
    def create_id(self, value : Guid):
        ...
    
    ...

class ChartShape(Shape):
    '''Represents the shape of the chart.
    Properties and methods for the ChartObject object control the appearance and size of the embedded chart on the worksheet.'''
    
    @overload
    def to_image(self, stream : io.RawIOBase, image_type : aspose.cells.drawing.ImageType):
        '''Creates the shape image and saves it to a stream in the specified format.
        
        :param stream: The output stream.
        :param image_type: The type in which to save the image.'''
        ...
    
    @overload
    def to_image(self, image_file : str, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a file.'''
        ...
    
    @overload
    def to_image(self, stream : io.RawIOBase, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a stream.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.'''
        ...
    
    def get_result_of_smart_art(self) -> aspose.cells.drawing.GroupShape:
        '''Converting smart art to grouped shapes.'''
        ...
    
    def to_front_or_back(self, orders : int):
        '''Brings the shape to the front or sends the shape to back.
        
        :param orders: If it's less than zero, sets the shape to back.
        If it's greater than zero, brings the shape to front.'''
        ...
    
    def get_locked_property(self, type : aspose.cells.drawing.ShapeLockType) -> bool:
        '''Gets the value of locked property.
        
        :param type: The type of the shape locked property.
        :returns: Returns  the value of locked property.'''
        ...
    
    def set_locked_property(self, type : aspose.cells.drawing.ShapeLockType, value : bool):
        '''Set the locked property.
        
        :param type: The locked type.
        :param value: The value of the property.'''
        ...
    
    def add_hyperlink(self, address : str) -> aspose.cells.Hyperlink:
        '''Adds a hyperlink to the shape.
        
        :param address: Address of the hyperlink.
        :returns: Return the new hyperlink object.'''
        ...
    
    def remove_hyperlink(self):
        '''Remove the hyperlink of the shape.'''
        ...
    
    def move_to_range(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int):
        '''Moves the shape to a specified range.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index'''
        ...
    
    def align_top_right_corner(self, top_row : int, right_column : int):
        '''Moves the picture to the top-right corner.
        
        :param top_row: the row index.
        :param right_column: the column index.'''
        ...
    
    def get_connection_points(self) -> List[List[float]]:
        '''Get the connection points
        
        :returns: [X,Y] pairs of the connection point. Every item is a float[2] array, [0] represents x and [1] represents y.'''
        ...
    
    def get_linked_cell(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range linked to the control's value.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range linked to the control's value.'''
        ...
    
    def set_linked_cell(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range linked to the control's value.
        
        :param formula: The range linked to the control's value.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def get_input_range(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range used to fill the control.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range used to fill the control.'''
        ...
    
    def set_input_range(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range used to fill the control.
        
        :param formula: The range used to fill the control.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell.'''
        ...
    
    def calculate_text_size(self) -> List[int]:
        '''Recalculate the text area
        
        :returns: Text's Size in an array(width and height).'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the text .
        
        :returns: All Characters objects'''
        ...
    
    def remove_active_x_control(self):
        '''Remove activeX control.'''
        ...
    
    def is_same_setting(self, obj : any) -> bool:
        '''Returns whether the shape is same.'''
        ...
    
    @property
    def macro_name(self) -> str:
        ...
    
    @macro_name.setter
    def macro_name(self, value : str):
        ...
    
    @property
    def is_equation(self) -> bool:
        ...
    
    @property
    def is_smart_art(self) -> bool:
        ...
    
    @property
    def z_order_position(self) -> int:
        ...
    
    @z_order_position.setter
    def z_order_position(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of the shape.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of the shape.'''
        ...
    
    @property
    def alternative_text(self) -> str:
        ...
    
    @alternative_text.setter
    def alternative_text(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @property
    def line_format(self) -> aspose.cells.drawing.MsoLineFormat:
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.MsoFillFormat:
        ...
    
    @property
    def format(self) -> aspose.cells.drawing.ShapeFormat:
        '''Represents the setting of the shape's formatting.'''
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        '''Gets line style'''
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        '''Returns a :py:attr:`aspose.cells.drawing.Shape.fill_format` object that contains fill formatting properties for the specified shape.'''
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def reflection(self) -> aspose.cells.drawing.ReflectionEffect:
        '''Represents a :py:class:`aspose.cells.drawing.ReflectionEffect` object that specifies reflection effect for the chart element or shape.'''
        ...
    
    @property
    def glow(self) -> aspose.cells.drawing.GlowEffect:
        '''Represents a :py:class:`aspose.cells.drawing.GlowEffect` object that specifies glow effect for the chart element or shape.'''
        ...
    
    @property
    def soft_edges(self) -> float:
        ...
    
    @soft_edges.setter
    def soft_edges(self, value : float):
        ...
    
    @property
    def three_d_format(self) -> aspose.cells.drawing.ThreeDFormat:
        ...
    
    @property
    def text_frame(self) -> aspose.cells.drawing.MsoTextFrame:
        ...
    
    @property
    def format_picture(self) -> aspose.cells.drawing.MsoFormatPicture:
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_lock_aspect_ratio(self) -> bool:
        ...
    
    @is_lock_aspect_ratio.setter
    def is_lock_aspect_ratio(self, value : bool):
        ...
    
    @property
    def rotation_angle(self) -> float:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : float):
        ...
    
    @property
    def hyperlink(self) -> aspose.cells.Hyperlink:
        '''Gets the hyperlink of the shape.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier of this shape.'''
        ...
    
    @property
    def spid(self) -> str:
        '''Specifies an optional string that an application can use to Identify the particular shape.'''
        ...
    
    @property
    def spt(self) -> int:
        '''Specifies an optional number that an application can use to associate the particular shape with a defined shape type.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.drawing.Shape.worksheet` object which contains this shape.'''
        ...
    
    @property
    def is_group(self) -> bool:
        ...
    
    @property
    def is_in_group(self) -> bool:
        ...
    
    @property
    def is_word_art(self) -> bool:
        ...
    
    @property
    def text_effect(self) -> aspose.cells.drawing.TextEffectFormat:
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_printable(self) -> bool:
        ...
    
    @is_printable.setter
    def is_printable(self, value : bool):
        ...
    
    @property
    def mso_drawing_type(self) -> aspose.cells.drawing.MsoDrawingType:
        ...
    
    @property
    def auto_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @auto_shape_type.setter
    def auto_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def anchor_type(self) -> aspose.cells.drawing.ShapeAnchorType:
        ...
    
    @anchor_type.setter
    def anchor_type(self, value : aspose.cells.drawing.ShapeAnchorType):
        ...
    
    @property
    def placement(self) -> aspose.cells.drawing.PlacementType:
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @placement.setter
    def placement(self, value : aspose.cells.drawing.PlacementType):
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @property
    def upper_left_row(self) -> int:
        ...
    
    @upper_left_row.setter
    def upper_left_row(self, value : int):
        ...
    
    @property
    def upper_delta_y(self) -> int:
        ...
    
    @upper_delta_y.setter
    def upper_delta_y(self, value : int):
        ...
    
    @property
    def upper_left_column(self) -> int:
        ...
    
    @upper_left_column.setter
    def upper_left_column(self, value : int):
        ...
    
    @property
    def upper_delta_x(self) -> int:
        ...
    
    @upper_delta_x.setter
    def upper_delta_x(self, value : int):
        ...
    
    @property
    def lower_right_row(self) -> int:
        ...
    
    @lower_right_row.setter
    def lower_right_row(self, value : int):
        ...
    
    @property
    def lower_delta_y(self) -> int:
        ...
    
    @lower_delta_y.setter
    def lower_delta_y(self, value : int):
        ...
    
    @property
    def lower_right_column(self) -> int:
        ...
    
    @lower_right_column.setter
    def lower_right_column(self, value : int):
        ...
    
    @property
    def lower_delta_x(self) -> int:
        ...
    
    @lower_delta_x.setter
    def lower_delta_x(self, value : int):
        ...
    
    @property
    def right(self) -> int:
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def width_pt(self) -> float:
        ...
    
    @width_pt.setter
    def width_pt(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def height(self) -> int:
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    @property
    def height_pt(self) -> float:
        ...
    
    @height_pt.setter
    def height_pt(self, value : float):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def left(self) -> int:
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @property
    def left_inch(self) -> float:
        ...
    
    @left_inch.setter
    def left_inch(self, value : float):
        ...
    
    @property
    def left_cm(self) -> float:
        ...
    
    @left_cm.setter
    def left_cm(self, value : float):
        ...
    
    @property
    def top(self) -> int:
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @property
    def top_inch(self) -> float:
        ...
    
    @top_inch.setter
    def top_inch(self, value : float):
        ...
    
    @property
    def top_cm(self) -> float:
        ...
    
    @top_cm.setter
    def top_cm(self, value : float):
        ...
    
    @property
    def top_to_corner(self) -> int:
        ...
    
    @top_to_corner.setter
    def top_to_corner(self, value : int):
        ...
    
    @property
    def left_to_corner(self) -> int:
        ...
    
    @left_to_corner.setter
    def left_to_corner(self, value : int):
        ...
    
    @property
    def x(self) -> int:
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @property
    def width_scale(self) -> int:
        ...
    
    @width_scale.setter
    def width_scale(self, value : int):
        ...
    
    @property
    def height_scale(self) -> int:
        ...
    
    @height_scale.setter
    def height_scale(self, value : int):
        ...
    
    @property
    def top_in_shape(self) -> int:
        ...
    
    @top_in_shape.setter
    def top_in_shape(self, value : int):
        ...
    
    @property
    def left_in_shape(self) -> int:
        ...
    
    @left_in_shape.setter
    def left_in_shape(self, value : int):
        ...
    
    @property
    def width_in_shape(self) -> int:
        ...
    
    @width_in_shape.setter
    def width_in_shape(self, value : int):
        ...
    
    @property
    def height_in_shape(self) -> int:
        ...
    
    @height_in_shape.setter
    def height_in_shape(self, value : int):
        ...
    
    @property
    def group(self) -> aspose.cells.drawing.GroupShape:
        '''Gets the group shape which contains this shape.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.AutoShapeType:
        '''Gets the auto shape type.'''
        ...
    
    @property
    def has_line(self) -> bool:
        ...
    
    @has_line.setter
    def has_line(self, value : bool):
        ...
    
    @property
    def is_filled(self) -> bool:
        ...
    
    @is_filled.setter
    def is_filled(self, value : bool):
        ...
    
    @property
    def is_flipped_horizontally(self) -> bool:
        ...
    
    @is_flipped_horizontally.setter
    def is_flipped_horizontally(self, value : bool):
        ...
    
    @property
    def is_flipped_vertically(self) -> bool:
        ...
    
    @is_flipped_vertically.setter
    def is_flipped_vertically(self, value : bool):
        ...
    
    @property
    def actual_lower_right_row(self) -> int:
        ...
    
    @property
    def connection_points(self) -> aspose.pydrawing.PointF[]:
        ...
    
    @property
    def relative_to_original_picture_size(self) -> bool:
        ...
    
    @relative_to_original_picture_size.setter
    def relative_to_original_picture_size(self, value : bool):
        ...
    
    @property
    def linked_cell(self) -> str:
        ...
    
    @linked_cell.setter
    def linked_cell(self, value : str):
        ...
    
    @property
    def input_range(self) -> str:
        ...
    
    @input_range.setter
    def input_range(self, value : str):
        ...
    
    @property
    def text_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @text_shape_type.setter
    def text_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def text_body(self) -> aspose.cells.drawing.texts.FontSettingCollection:
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Represents the font of shape.'''
        ...
    
    @font.setter
    def font(self, value : aspose.cells.Font):
        '''Represents the font of shape.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    @text_options.setter
    def text_options(self, value : aspose.cells.drawing.texts.TextOptions):
        ...
    
    @property
    def text(self) -> str:
        '''Represents the string in this TextBox object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Represents the string in this TextBox object.'''
        ...
    
    @property
    def is_rich_text(self) -> bool:
        ...
    
    @property
    def html_text(self) -> str:
        ...
    
    @html_text.setter
    def html_text(self, value : str):
        ...
    
    @property
    def text_vertical_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_vertical_overflow.setter
    def text_vertical_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def text_horizontal_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_horizontal_overflow.setter
    def text_horizontal_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
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
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def control_data(self) -> bytes:
        ...
    
    @property
    def active_x_control(self) -> aspose.cells.drawing.activexcontrols.ActiveXControl:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets the paths of a custom geometric shape.'''
        ...
    
    @property
    def geometry(self) -> aspose.cells.drawing.Geometry:
        '''Gets the geometry'''
        ...
    
    @property
    def create_id(self) -> Guid:
        ...
    
    @create_id.setter
    def create_id(self, value : Guid):
        ...
    
    @property
    def chart(self) -> aspose.cells.charts.Chart:
        '''Returns a Chart object that represents the chart contained in the object.'''
        ...
    
    ...

class CheckBox(Shape):
    '''Represents a check box object in a worksheet.'''
    
    @overload
    def to_image(self, stream : io.RawIOBase, image_type : aspose.cells.drawing.ImageType):
        '''Creates the shape image and saves it to a stream in the specified format.
        
        :param stream: The output stream.
        :param image_type: The type in which to save the image.'''
        ...
    
    @overload
    def to_image(self, image_file : str, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a file.'''
        ...
    
    @overload
    def to_image(self, stream : io.RawIOBase, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a stream.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.'''
        ...
    
    def get_result_of_smart_art(self) -> aspose.cells.drawing.GroupShape:
        '''Converting smart art to grouped shapes.'''
        ...
    
    def to_front_or_back(self, orders : int):
        '''Brings the shape to the front or sends the shape to back.
        
        :param orders: If it's less than zero, sets the shape to back.
        If it's greater than zero, brings the shape to front.'''
        ...
    
    def get_locked_property(self, type : aspose.cells.drawing.ShapeLockType) -> bool:
        '''Gets the value of locked property.
        
        :param type: The type of the shape locked property.
        :returns: Returns  the value of locked property.'''
        ...
    
    def set_locked_property(self, type : aspose.cells.drawing.ShapeLockType, value : bool):
        '''Set the locked property.
        
        :param type: The locked type.
        :param value: The value of the property.'''
        ...
    
    def add_hyperlink(self, address : str) -> aspose.cells.Hyperlink:
        '''Adds a hyperlink to the shape.
        
        :param address: Address of the hyperlink.
        :returns: Return the new hyperlink object.'''
        ...
    
    def remove_hyperlink(self):
        '''Remove the hyperlink of the shape.'''
        ...
    
    def move_to_range(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int):
        '''Moves the shape to a specified range.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index'''
        ...
    
    def align_top_right_corner(self, top_row : int, right_column : int):
        '''Moves the picture to the top-right corner.
        
        :param top_row: the row index.
        :param right_column: the column index.'''
        ...
    
    def get_connection_points(self) -> List[List[float]]:
        '''Get the connection points
        
        :returns: [X,Y] pairs of the connection point. Every item is a float[2] array, [0] represents x and [1] represents y.'''
        ...
    
    def get_linked_cell(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range linked to the control's value.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range linked to the control's value.'''
        ...
    
    def set_linked_cell(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range linked to the control's value.
        
        :param formula: The range linked to the control's value.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def get_input_range(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range used to fill the control.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range used to fill the control.'''
        ...
    
    def set_input_range(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range used to fill the control.
        
        :param formula: The range used to fill the control.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell.'''
        ...
    
    def calculate_text_size(self) -> List[int]:
        '''Recalculate the text area
        
        :returns: Text's Size in an array(width and height).'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the text .
        
        :returns: All Characters objects'''
        ...
    
    def remove_active_x_control(self):
        '''Remove activeX control.'''
        ...
    
    def is_same_setting(self, obj : any) -> bool:
        '''Returns whether the shape is same.'''
        ...
    
    @property
    def macro_name(self) -> str:
        ...
    
    @macro_name.setter
    def macro_name(self, value : str):
        ...
    
    @property
    def is_equation(self) -> bool:
        ...
    
    @property
    def is_smart_art(self) -> bool:
        ...
    
    @property
    def z_order_position(self) -> int:
        ...
    
    @z_order_position.setter
    def z_order_position(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of the shape.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of the shape.'''
        ...
    
    @property
    def alternative_text(self) -> str:
        ...
    
    @alternative_text.setter
    def alternative_text(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @property
    def line_format(self) -> aspose.cells.drawing.MsoLineFormat:
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.MsoFillFormat:
        ...
    
    @property
    def format(self) -> aspose.cells.drawing.ShapeFormat:
        '''Represents the setting of the shape's formatting.'''
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        '''Gets line style'''
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        '''Returns a :py:attr:`aspose.cells.drawing.Shape.fill_format` object that contains fill formatting properties for the specified shape.'''
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def reflection(self) -> aspose.cells.drawing.ReflectionEffect:
        '''Represents a :py:class:`aspose.cells.drawing.ReflectionEffect` object that specifies reflection effect for the chart element or shape.'''
        ...
    
    @property
    def glow(self) -> aspose.cells.drawing.GlowEffect:
        '''Represents a :py:class:`aspose.cells.drawing.GlowEffect` object that specifies glow effect for the chart element or shape.'''
        ...
    
    @property
    def soft_edges(self) -> float:
        ...
    
    @soft_edges.setter
    def soft_edges(self, value : float):
        ...
    
    @property
    def three_d_format(self) -> aspose.cells.drawing.ThreeDFormat:
        ...
    
    @property
    def text_frame(self) -> aspose.cells.drawing.MsoTextFrame:
        ...
    
    @property
    def format_picture(self) -> aspose.cells.drawing.MsoFormatPicture:
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_lock_aspect_ratio(self) -> bool:
        ...
    
    @is_lock_aspect_ratio.setter
    def is_lock_aspect_ratio(self, value : bool):
        ...
    
    @property
    def rotation_angle(self) -> float:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : float):
        ...
    
    @property
    def hyperlink(self) -> aspose.cells.Hyperlink:
        '''Gets the hyperlink of the shape.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier of this shape.'''
        ...
    
    @property
    def spid(self) -> str:
        '''Specifies an optional string that an application can use to Identify the particular shape.'''
        ...
    
    @property
    def spt(self) -> int:
        '''Specifies an optional number that an application can use to associate the particular shape with a defined shape type.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.drawing.Shape.worksheet` object which contains this shape.'''
        ...
    
    @property
    def is_group(self) -> bool:
        ...
    
    @property
    def is_in_group(self) -> bool:
        ...
    
    @property
    def is_word_art(self) -> bool:
        ...
    
    @property
    def text_effect(self) -> aspose.cells.drawing.TextEffectFormat:
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_printable(self) -> bool:
        ...
    
    @is_printable.setter
    def is_printable(self, value : bool):
        ...
    
    @property
    def mso_drawing_type(self) -> aspose.cells.drawing.MsoDrawingType:
        ...
    
    @property
    def auto_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @auto_shape_type.setter
    def auto_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def anchor_type(self) -> aspose.cells.drawing.ShapeAnchorType:
        ...
    
    @anchor_type.setter
    def anchor_type(self, value : aspose.cells.drawing.ShapeAnchorType):
        ...
    
    @property
    def placement(self) -> aspose.cells.drawing.PlacementType:
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @placement.setter
    def placement(self, value : aspose.cells.drawing.PlacementType):
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @property
    def upper_left_row(self) -> int:
        ...
    
    @upper_left_row.setter
    def upper_left_row(self, value : int):
        ...
    
    @property
    def upper_delta_y(self) -> int:
        ...
    
    @upper_delta_y.setter
    def upper_delta_y(self, value : int):
        ...
    
    @property
    def upper_left_column(self) -> int:
        ...
    
    @upper_left_column.setter
    def upper_left_column(self, value : int):
        ...
    
    @property
    def upper_delta_x(self) -> int:
        ...
    
    @upper_delta_x.setter
    def upper_delta_x(self, value : int):
        ...
    
    @property
    def lower_right_row(self) -> int:
        ...
    
    @lower_right_row.setter
    def lower_right_row(self, value : int):
        ...
    
    @property
    def lower_delta_y(self) -> int:
        ...
    
    @lower_delta_y.setter
    def lower_delta_y(self, value : int):
        ...
    
    @property
    def lower_right_column(self) -> int:
        ...
    
    @lower_right_column.setter
    def lower_right_column(self, value : int):
        ...
    
    @property
    def lower_delta_x(self) -> int:
        ...
    
    @lower_delta_x.setter
    def lower_delta_x(self, value : int):
        ...
    
    @property
    def right(self) -> int:
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def width_pt(self) -> float:
        ...
    
    @width_pt.setter
    def width_pt(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def height(self) -> int:
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    @property
    def height_pt(self) -> float:
        ...
    
    @height_pt.setter
    def height_pt(self, value : float):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def left(self) -> int:
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @property
    def left_inch(self) -> float:
        ...
    
    @left_inch.setter
    def left_inch(self, value : float):
        ...
    
    @property
    def left_cm(self) -> float:
        ...
    
    @left_cm.setter
    def left_cm(self, value : float):
        ...
    
    @property
    def top(self) -> int:
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @property
    def top_inch(self) -> float:
        ...
    
    @top_inch.setter
    def top_inch(self, value : float):
        ...
    
    @property
    def top_cm(self) -> float:
        ...
    
    @top_cm.setter
    def top_cm(self, value : float):
        ...
    
    @property
    def top_to_corner(self) -> int:
        ...
    
    @top_to_corner.setter
    def top_to_corner(self, value : int):
        ...
    
    @property
    def left_to_corner(self) -> int:
        ...
    
    @left_to_corner.setter
    def left_to_corner(self, value : int):
        ...
    
    @property
    def x(self) -> int:
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @property
    def width_scale(self) -> int:
        ...
    
    @width_scale.setter
    def width_scale(self, value : int):
        ...
    
    @property
    def height_scale(self) -> int:
        ...
    
    @height_scale.setter
    def height_scale(self, value : int):
        ...
    
    @property
    def top_in_shape(self) -> int:
        ...
    
    @top_in_shape.setter
    def top_in_shape(self, value : int):
        ...
    
    @property
    def left_in_shape(self) -> int:
        ...
    
    @left_in_shape.setter
    def left_in_shape(self, value : int):
        ...
    
    @property
    def width_in_shape(self) -> int:
        ...
    
    @width_in_shape.setter
    def width_in_shape(self, value : int):
        ...
    
    @property
    def height_in_shape(self) -> int:
        ...
    
    @height_in_shape.setter
    def height_in_shape(self, value : int):
        ...
    
    @property
    def group(self) -> aspose.cells.drawing.GroupShape:
        '''Gets the group shape which contains this shape.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.AutoShapeType:
        '''Gets the auto shape type.'''
        ...
    
    @property
    def has_line(self) -> bool:
        ...
    
    @has_line.setter
    def has_line(self, value : bool):
        ...
    
    @property
    def is_filled(self) -> bool:
        ...
    
    @is_filled.setter
    def is_filled(self, value : bool):
        ...
    
    @property
    def is_flipped_horizontally(self) -> bool:
        ...
    
    @is_flipped_horizontally.setter
    def is_flipped_horizontally(self, value : bool):
        ...
    
    @property
    def is_flipped_vertically(self) -> bool:
        ...
    
    @is_flipped_vertically.setter
    def is_flipped_vertically(self, value : bool):
        ...
    
    @property
    def actual_lower_right_row(self) -> int:
        ...
    
    @property
    def connection_points(self) -> aspose.pydrawing.PointF[]:
        ...
    
    @property
    def relative_to_original_picture_size(self) -> bool:
        ...
    
    @relative_to_original_picture_size.setter
    def relative_to_original_picture_size(self, value : bool):
        ...
    
    @property
    def linked_cell(self) -> str:
        ...
    
    @linked_cell.setter
    def linked_cell(self, value : str):
        ...
    
    @property
    def input_range(self) -> str:
        ...
    
    @input_range.setter
    def input_range(self, value : str):
        ...
    
    @property
    def text_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @text_shape_type.setter
    def text_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def text_body(self) -> aspose.cells.drawing.texts.FontSettingCollection:
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Represents the font of shape.'''
        ...
    
    @font.setter
    def font(self, value : aspose.cells.Font):
        '''Represents the font of shape.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    @text_options.setter
    def text_options(self, value : aspose.cells.drawing.texts.TextOptions):
        ...
    
    @property
    def text(self) -> str:
        '''Represents the string in this TextBox object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Represents the string in this TextBox object.'''
        ...
    
    @property
    def is_rich_text(self) -> bool:
        ...
    
    @property
    def html_text(self) -> str:
        ...
    
    @html_text.setter
    def html_text(self, value : str):
        ...
    
    @property
    def text_vertical_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_vertical_overflow.setter
    def text_vertical_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def text_horizontal_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_horizontal_overflow.setter
    def text_horizontal_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
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
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def control_data(self) -> bytes:
        ...
    
    @property
    def active_x_control(self) -> aspose.cells.drawing.activexcontrols.ActiveXControl:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets the paths of a custom geometric shape.'''
        ...
    
    @property
    def geometry(self) -> aspose.cells.drawing.Geometry:
        '''Gets the geometry'''
        ...
    
    @property
    def create_id(self) -> Guid:
        ...
    
    @create_id.setter
    def create_id(self, value : Guid):
        ...
    
    @property
    def value(self) -> bool:
        '''Indicates if the checkbox is checked or not.'''
        ...
    
    @value.setter
    def value(self, value : bool):
        '''Indicates if the checkbox is checked or not.'''
        ...
    
    @property
    def check_value(self) -> aspose.cells.drawing.CheckValueType:
        ...
    
    @check_value.setter
    def check_value(self, value : aspose.cells.drawing.CheckValueType):
        ...
    
    @property
    def checked_value(self) -> aspose.cells.drawing.CheckValueType:
        ...
    
    @checked_value.setter
    def checked_value(self, value : aspose.cells.drawing.CheckValueType):
        ...
    
    @property
    def shadow(self) -> bool:
        '''Indicates whether the combobox has 3-D shading.'''
        ...
    
    @shadow.setter
    def shadow(self, value : bool):
        '''Indicates whether the combobox has 3-D shading.'''
        ...
    
    ...

class CheckBoxCollection:
    '''Represents a collection of :py:class:`aspose.cells.drawing.CheckBox` objects in a worksheet.'''
    
    @overload
    def copy_to(self, array : List[aspose.cells.drawing.CheckBox]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.drawing.CheckBox], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.drawing.CheckBox, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.drawing.CheckBox, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.CheckBox) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.CheckBox, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.CheckBox, index : int, count : int) -> int:
        ...
    
    def add(self, upper_left_row : int, upper_left_column : int, height : int, width : int) -> int:
        '''Adds a checkBox to the collection.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param height: Height of checkBox, in unit of pixel.
        :param width: Width of checkBox, in unit of pixel.
        :returns: :py:class:`aspose.cells.drawing.CheckBox` object index.'''
        ...
    
    def binary_search(self, item : aspose.cells.drawing.CheckBox) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class ColorHelper:
    '''Provides helper functions about color.'''
    
    @staticmethod
    def from_ole_color(ole_color : int) -> aspose.pydrawing.Color:
        '''Convert OLE_COLOR.
        
        :param ole_color: The value of OLE_COLOR.
        :returns: The :py:class:`aspose.pydrawing.Color` object.'''
        ...
    
    @staticmethod
    def to_ole_color(color : aspose.pydrawing.Colorworkbook : aspose.cells.Workbook) -> int:
        '''Convert color to OLE_COLOR
        
        :param color: The :py:class:`aspose.pydrawing.Color` object.
        :returns: The value of OLE_COLOR'''
        ...
    
    ...

class ComboBox(Shape):
    '''Represents the control form ComboBox.'''
    
    @overload
    def to_image(self, stream : io.RawIOBase, image_type : aspose.cells.drawing.ImageType):
        '''Creates the shape image and saves it to a stream in the specified format.
        
        :param stream: The output stream.
        :param image_type: The type in which to save the image.'''
        ...
    
    @overload
    def to_image(self, image_file : str, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a file.'''
        ...
    
    @overload
    def to_image(self, stream : io.RawIOBase, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a stream.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.'''
        ...
    
    def get_result_of_smart_art(self) -> aspose.cells.drawing.GroupShape:
        '''Converting smart art to grouped shapes.'''
        ...
    
    def to_front_or_back(self, orders : int):
        '''Brings the shape to the front or sends the shape to back.
        
        :param orders: If it's less than zero, sets the shape to back.
        If it's greater than zero, brings the shape to front.'''
        ...
    
    def get_locked_property(self, type : aspose.cells.drawing.ShapeLockType) -> bool:
        '''Gets the value of locked property.
        
        :param type: The type of the shape locked property.
        :returns: Returns  the value of locked property.'''
        ...
    
    def set_locked_property(self, type : aspose.cells.drawing.ShapeLockType, value : bool):
        '''Set the locked property.
        
        :param type: The locked type.
        :param value: The value of the property.'''
        ...
    
    def add_hyperlink(self, address : str) -> aspose.cells.Hyperlink:
        '''Adds a hyperlink to the shape.
        
        :param address: Address of the hyperlink.
        :returns: Return the new hyperlink object.'''
        ...
    
    def remove_hyperlink(self):
        '''Remove the hyperlink of the shape.'''
        ...
    
    def move_to_range(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int):
        '''Moves the shape to a specified range.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index'''
        ...
    
    def align_top_right_corner(self, top_row : int, right_column : int):
        '''Moves the picture to the top-right corner.
        
        :param top_row: the row index.
        :param right_column: the column index.'''
        ...
    
    def get_connection_points(self) -> List[List[float]]:
        '''Get the connection points
        
        :returns: [X,Y] pairs of the connection point. Every item is a float[2] array, [0] represents x and [1] represents y.'''
        ...
    
    def get_linked_cell(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range linked to the control's value.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range linked to the control's value.'''
        ...
    
    def set_linked_cell(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range linked to the control's value.
        
        :param formula: The range linked to the control's value.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def get_input_range(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range used to fill the control.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range used to fill the control.'''
        ...
    
    def set_input_range(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range used to fill the control.
        
        :param formula: The range used to fill the control.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell.'''
        ...
    
    def calculate_text_size(self) -> List[int]:
        '''Recalculate the text area
        
        :returns: Text's Size in an array(width and height).'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the text .
        
        :returns: All Characters objects'''
        ...
    
    def remove_active_x_control(self):
        '''Remove activeX control.'''
        ...
    
    def is_same_setting(self, obj : any) -> bool:
        '''Returns whether the shape is same.'''
        ...
    
    @property
    def macro_name(self) -> str:
        ...
    
    @macro_name.setter
    def macro_name(self, value : str):
        ...
    
    @property
    def is_equation(self) -> bool:
        ...
    
    @property
    def is_smart_art(self) -> bool:
        ...
    
    @property
    def z_order_position(self) -> int:
        ...
    
    @z_order_position.setter
    def z_order_position(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of the shape.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of the shape.'''
        ...
    
    @property
    def alternative_text(self) -> str:
        ...
    
    @alternative_text.setter
    def alternative_text(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @property
    def line_format(self) -> aspose.cells.drawing.MsoLineFormat:
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.MsoFillFormat:
        ...
    
    @property
    def format(self) -> aspose.cells.drawing.ShapeFormat:
        '''Represents the setting of the shape's formatting.'''
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        '''Gets line style'''
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        '''Returns a :py:attr:`aspose.cells.drawing.Shape.fill_format` object that contains fill formatting properties for the specified shape.'''
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def reflection(self) -> aspose.cells.drawing.ReflectionEffect:
        '''Represents a :py:class:`aspose.cells.drawing.ReflectionEffect` object that specifies reflection effect for the chart element or shape.'''
        ...
    
    @property
    def glow(self) -> aspose.cells.drawing.GlowEffect:
        '''Represents a :py:class:`aspose.cells.drawing.GlowEffect` object that specifies glow effect for the chart element or shape.'''
        ...
    
    @property
    def soft_edges(self) -> float:
        ...
    
    @soft_edges.setter
    def soft_edges(self, value : float):
        ...
    
    @property
    def three_d_format(self) -> aspose.cells.drawing.ThreeDFormat:
        ...
    
    @property
    def text_frame(self) -> aspose.cells.drawing.MsoTextFrame:
        ...
    
    @property
    def format_picture(self) -> aspose.cells.drawing.MsoFormatPicture:
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_lock_aspect_ratio(self) -> bool:
        ...
    
    @is_lock_aspect_ratio.setter
    def is_lock_aspect_ratio(self, value : bool):
        ...
    
    @property
    def rotation_angle(self) -> float:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : float):
        ...
    
    @property
    def hyperlink(self) -> aspose.cells.Hyperlink:
        '''Gets the hyperlink of the shape.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier of this shape.'''
        ...
    
    @property
    def spid(self) -> str:
        '''Specifies an optional string that an application can use to Identify the particular shape.'''
        ...
    
    @property
    def spt(self) -> int:
        '''Specifies an optional number that an application can use to associate the particular shape with a defined shape type.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.drawing.Shape.worksheet` object which contains this shape.'''
        ...
    
    @property
    def is_group(self) -> bool:
        ...
    
    @property
    def is_in_group(self) -> bool:
        ...
    
    @property
    def is_word_art(self) -> bool:
        ...
    
    @property
    def text_effect(self) -> aspose.cells.drawing.TextEffectFormat:
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_printable(self) -> bool:
        ...
    
    @is_printable.setter
    def is_printable(self, value : bool):
        ...
    
    @property
    def mso_drawing_type(self) -> aspose.cells.drawing.MsoDrawingType:
        ...
    
    @property
    def auto_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @auto_shape_type.setter
    def auto_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def anchor_type(self) -> aspose.cells.drawing.ShapeAnchorType:
        ...
    
    @anchor_type.setter
    def anchor_type(self, value : aspose.cells.drawing.ShapeAnchorType):
        ...
    
    @property
    def placement(self) -> aspose.cells.drawing.PlacementType:
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @placement.setter
    def placement(self, value : aspose.cells.drawing.PlacementType):
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @property
    def upper_left_row(self) -> int:
        ...
    
    @upper_left_row.setter
    def upper_left_row(self, value : int):
        ...
    
    @property
    def upper_delta_y(self) -> int:
        ...
    
    @upper_delta_y.setter
    def upper_delta_y(self, value : int):
        ...
    
    @property
    def upper_left_column(self) -> int:
        ...
    
    @upper_left_column.setter
    def upper_left_column(self, value : int):
        ...
    
    @property
    def upper_delta_x(self) -> int:
        ...
    
    @upper_delta_x.setter
    def upper_delta_x(self, value : int):
        ...
    
    @property
    def lower_right_row(self) -> int:
        ...
    
    @lower_right_row.setter
    def lower_right_row(self, value : int):
        ...
    
    @property
    def lower_delta_y(self) -> int:
        ...
    
    @lower_delta_y.setter
    def lower_delta_y(self, value : int):
        ...
    
    @property
    def lower_right_column(self) -> int:
        ...
    
    @lower_right_column.setter
    def lower_right_column(self, value : int):
        ...
    
    @property
    def lower_delta_x(self) -> int:
        ...
    
    @lower_delta_x.setter
    def lower_delta_x(self, value : int):
        ...
    
    @property
    def right(self) -> int:
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def width_pt(self) -> float:
        ...
    
    @width_pt.setter
    def width_pt(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def height(self) -> int:
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    @property
    def height_pt(self) -> float:
        ...
    
    @height_pt.setter
    def height_pt(self, value : float):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def left(self) -> int:
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @property
    def left_inch(self) -> float:
        ...
    
    @left_inch.setter
    def left_inch(self, value : float):
        ...
    
    @property
    def left_cm(self) -> float:
        ...
    
    @left_cm.setter
    def left_cm(self, value : float):
        ...
    
    @property
    def top(self) -> int:
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @property
    def top_inch(self) -> float:
        ...
    
    @top_inch.setter
    def top_inch(self, value : float):
        ...
    
    @property
    def top_cm(self) -> float:
        ...
    
    @top_cm.setter
    def top_cm(self, value : float):
        ...
    
    @property
    def top_to_corner(self) -> int:
        ...
    
    @top_to_corner.setter
    def top_to_corner(self, value : int):
        ...
    
    @property
    def left_to_corner(self) -> int:
        ...
    
    @left_to_corner.setter
    def left_to_corner(self, value : int):
        ...
    
    @property
    def x(self) -> int:
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @property
    def width_scale(self) -> int:
        ...
    
    @width_scale.setter
    def width_scale(self, value : int):
        ...
    
    @property
    def height_scale(self) -> int:
        ...
    
    @height_scale.setter
    def height_scale(self, value : int):
        ...
    
    @property
    def top_in_shape(self) -> int:
        ...
    
    @top_in_shape.setter
    def top_in_shape(self, value : int):
        ...
    
    @property
    def left_in_shape(self) -> int:
        ...
    
    @left_in_shape.setter
    def left_in_shape(self, value : int):
        ...
    
    @property
    def width_in_shape(self) -> int:
        ...
    
    @width_in_shape.setter
    def width_in_shape(self, value : int):
        ...
    
    @property
    def height_in_shape(self) -> int:
        ...
    
    @height_in_shape.setter
    def height_in_shape(self, value : int):
        ...
    
    @property
    def group(self) -> aspose.cells.drawing.GroupShape:
        '''Gets the group shape which contains this shape.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.AutoShapeType:
        '''Gets the auto shape type.'''
        ...
    
    @property
    def has_line(self) -> bool:
        ...
    
    @has_line.setter
    def has_line(self, value : bool):
        ...
    
    @property
    def is_filled(self) -> bool:
        ...
    
    @is_filled.setter
    def is_filled(self, value : bool):
        ...
    
    @property
    def is_flipped_horizontally(self) -> bool:
        ...
    
    @is_flipped_horizontally.setter
    def is_flipped_horizontally(self, value : bool):
        ...
    
    @property
    def is_flipped_vertically(self) -> bool:
        ...
    
    @is_flipped_vertically.setter
    def is_flipped_vertically(self, value : bool):
        ...
    
    @property
    def actual_lower_right_row(self) -> int:
        ...
    
    @property
    def connection_points(self) -> aspose.pydrawing.PointF[]:
        ...
    
    @property
    def relative_to_original_picture_size(self) -> bool:
        ...
    
    @relative_to_original_picture_size.setter
    def relative_to_original_picture_size(self, value : bool):
        ...
    
    @property
    def linked_cell(self) -> str:
        ...
    
    @linked_cell.setter
    def linked_cell(self, value : str):
        ...
    
    @property
    def input_range(self) -> str:
        ...
    
    @input_range.setter
    def input_range(self, value : str):
        ...
    
    @property
    def text_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @text_shape_type.setter
    def text_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def text_body(self) -> aspose.cells.drawing.texts.FontSettingCollection:
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Represents the font of shape.'''
        ...
    
    @font.setter
    def font(self, value : aspose.cells.Font):
        '''Represents the font of shape.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    @text_options.setter
    def text_options(self, value : aspose.cells.drawing.texts.TextOptions):
        ...
    
    @property
    def text(self) -> str:
        '''Represents the string in this TextBox object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Represents the string in this TextBox object.'''
        ...
    
    @property
    def is_rich_text(self) -> bool:
        ...
    
    @property
    def html_text(self) -> str:
        ...
    
    @html_text.setter
    def html_text(self, value : str):
        ...
    
    @property
    def text_vertical_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_vertical_overflow.setter
    def text_vertical_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def text_horizontal_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_horizontal_overflow.setter
    def text_horizontal_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
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
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def control_data(self) -> bytes:
        ...
    
    @property
    def active_x_control(self) -> aspose.cells.drawing.activexcontrols.ActiveXControl:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets the paths of a custom geometric shape.'''
        ...
    
    @property
    def geometry(self) -> aspose.cells.drawing.Geometry:
        '''Gets the geometry'''
        ...
    
    @property
    def create_id(self) -> Guid:
        ...
    
    @create_id.setter
    def create_id(self, value : Guid):
        ...
    
    @property
    def selected_index(self) -> int:
        ...
    
    @selected_index.setter
    def selected_index(self, value : int):
        ...
    
    @property
    def selected_value(self) -> str:
        ...
    
    @property
    def selected_cell(self) -> aspose.cells.Cell:
        ...
    
    @property
    def shadow(self) -> bool:
        '''Indicates whether the combobox has 3-D shading.'''
        ...
    
    @shadow.setter
    def shadow(self, value : bool):
        '''Indicates whether the combobox has 3-D shading.'''
        ...
    
    @property
    def drop_down_lines(self) -> int:
        ...
    
    @drop_down_lines.setter
    def drop_down_lines(self, value : int):
        ...
    
    ...

class CommentShape(Shape):
    '''Represents the shape of the comment.'''
    
    @overload
    def to_image(self, stream : io.RawIOBase, image_type : aspose.cells.drawing.ImageType):
        '''Creates the shape image and saves it to a stream in the specified format.
        
        :param stream: The output stream.
        :param image_type: The type in which to save the image.'''
        ...
    
    @overload
    def to_image(self, image_file : str, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a file.'''
        ...
    
    @overload
    def to_image(self, stream : io.RawIOBase, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a stream.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.'''
        ...
    
    def get_result_of_smart_art(self) -> aspose.cells.drawing.GroupShape:
        '''Converting smart art to grouped shapes.'''
        ...
    
    def to_front_or_back(self, orders : int):
        '''Brings the shape to the front or sends the shape to back.
        
        :param orders: If it's less than zero, sets the shape to back.
        If it's greater than zero, brings the shape to front.'''
        ...
    
    def get_locked_property(self, type : aspose.cells.drawing.ShapeLockType) -> bool:
        '''Gets the value of locked property.
        
        :param type: The type of the shape locked property.
        :returns: Returns  the value of locked property.'''
        ...
    
    def set_locked_property(self, type : aspose.cells.drawing.ShapeLockType, value : bool):
        '''Set the locked property.
        
        :param type: The locked type.
        :param value: The value of the property.'''
        ...
    
    def add_hyperlink(self, address : str) -> aspose.cells.Hyperlink:
        '''Adds a hyperlink to the shape.
        
        :param address: Address of the hyperlink.
        :returns: Return the new hyperlink object.'''
        ...
    
    def remove_hyperlink(self):
        '''Remove the hyperlink of the shape.'''
        ...
    
    def move_to_range(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int):
        '''Moves the shape to a specified range.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index'''
        ...
    
    def align_top_right_corner(self, top_row : int, right_column : int):
        '''Moves the picture to the top-right corner.
        
        :param top_row: the row index.
        :param right_column: the column index.'''
        ...
    
    def get_connection_points(self) -> List[List[float]]:
        '''Get the connection points
        
        :returns: [X,Y] pairs of the connection point. Every item is a float[2] array, [0] represents x and [1] represents y.'''
        ...
    
    def get_linked_cell(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range linked to the control's value.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range linked to the control's value.'''
        ...
    
    def set_linked_cell(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range linked to the control's value.
        
        :param formula: The range linked to the control's value.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def get_input_range(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range used to fill the control.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range used to fill the control.'''
        ...
    
    def set_input_range(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range used to fill the control.
        
        :param formula: The range used to fill the control.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell.'''
        ...
    
    def calculate_text_size(self) -> List[int]:
        '''Recalculate the text area
        
        :returns: Text's Size in an array(width and height).'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the text .
        
        :returns: All Characters objects'''
        ...
    
    def remove_active_x_control(self):
        '''Remove activeX control.'''
        ...
    
    def is_same_setting(self, obj : any) -> bool:
        '''Returns whether the shape is same.'''
        ...
    
    @property
    def macro_name(self) -> str:
        ...
    
    @macro_name.setter
    def macro_name(self, value : str):
        ...
    
    @property
    def is_equation(self) -> bool:
        ...
    
    @property
    def is_smart_art(self) -> bool:
        ...
    
    @property
    def z_order_position(self) -> int:
        ...
    
    @z_order_position.setter
    def z_order_position(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of the shape.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of the shape.'''
        ...
    
    @property
    def alternative_text(self) -> str:
        ...
    
    @alternative_text.setter
    def alternative_text(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @property
    def line_format(self) -> aspose.cells.drawing.MsoLineFormat:
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.MsoFillFormat:
        ...
    
    @property
    def format(self) -> aspose.cells.drawing.ShapeFormat:
        '''Represents the setting of the shape's formatting.'''
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        '''Gets line style'''
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        '''Returns a :py:attr:`aspose.cells.drawing.Shape.fill_format` object that contains fill formatting properties for the specified shape.'''
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def reflection(self) -> aspose.cells.drawing.ReflectionEffect:
        '''Represents a :py:class:`aspose.cells.drawing.ReflectionEffect` object that specifies reflection effect for the chart element or shape.'''
        ...
    
    @property
    def glow(self) -> aspose.cells.drawing.GlowEffect:
        '''Represents a :py:class:`aspose.cells.drawing.GlowEffect` object that specifies glow effect for the chart element or shape.'''
        ...
    
    @property
    def soft_edges(self) -> float:
        ...
    
    @soft_edges.setter
    def soft_edges(self, value : float):
        ...
    
    @property
    def three_d_format(self) -> aspose.cells.drawing.ThreeDFormat:
        ...
    
    @property
    def text_frame(self) -> aspose.cells.drawing.MsoTextFrame:
        ...
    
    @property
    def format_picture(self) -> aspose.cells.drawing.MsoFormatPicture:
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_lock_aspect_ratio(self) -> bool:
        ...
    
    @is_lock_aspect_ratio.setter
    def is_lock_aspect_ratio(self, value : bool):
        ...
    
    @property
    def rotation_angle(self) -> float:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : float):
        ...
    
    @property
    def hyperlink(self) -> aspose.cells.Hyperlink:
        '''Gets the hyperlink of the shape.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier of this shape.'''
        ...
    
    @property
    def spid(self) -> str:
        '''Specifies an optional string that an application can use to Identify the particular shape.'''
        ...
    
    @property
    def spt(self) -> int:
        '''Specifies an optional number that an application can use to associate the particular shape with a defined shape type.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.drawing.Shape.worksheet` object which contains this shape.'''
        ...
    
    @property
    def is_group(self) -> bool:
        ...
    
    @property
    def is_in_group(self) -> bool:
        ...
    
    @property
    def is_word_art(self) -> bool:
        ...
    
    @property
    def text_effect(self) -> aspose.cells.drawing.TextEffectFormat:
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_printable(self) -> bool:
        ...
    
    @is_printable.setter
    def is_printable(self, value : bool):
        ...
    
    @property
    def mso_drawing_type(self) -> aspose.cells.drawing.MsoDrawingType:
        ...
    
    @property
    def auto_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @auto_shape_type.setter
    def auto_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def anchor_type(self) -> aspose.cells.drawing.ShapeAnchorType:
        ...
    
    @anchor_type.setter
    def anchor_type(self, value : aspose.cells.drawing.ShapeAnchorType):
        ...
    
    @property
    def placement(self) -> aspose.cells.drawing.PlacementType:
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @placement.setter
    def placement(self, value : aspose.cells.drawing.PlacementType):
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @property
    def upper_left_row(self) -> int:
        ...
    
    @upper_left_row.setter
    def upper_left_row(self, value : int):
        ...
    
    @property
    def upper_delta_y(self) -> int:
        ...
    
    @upper_delta_y.setter
    def upper_delta_y(self, value : int):
        ...
    
    @property
    def upper_left_column(self) -> int:
        ...
    
    @upper_left_column.setter
    def upper_left_column(self, value : int):
        ...
    
    @property
    def upper_delta_x(self) -> int:
        ...
    
    @upper_delta_x.setter
    def upper_delta_x(self, value : int):
        ...
    
    @property
    def lower_right_row(self) -> int:
        ...
    
    @lower_right_row.setter
    def lower_right_row(self, value : int):
        ...
    
    @property
    def lower_delta_y(self) -> int:
        ...
    
    @lower_delta_y.setter
    def lower_delta_y(self, value : int):
        ...
    
    @property
    def lower_right_column(self) -> int:
        ...
    
    @lower_right_column.setter
    def lower_right_column(self, value : int):
        ...
    
    @property
    def lower_delta_x(self) -> int:
        ...
    
    @lower_delta_x.setter
    def lower_delta_x(self, value : int):
        ...
    
    @property
    def right(self) -> int:
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def width_pt(self) -> float:
        ...
    
    @width_pt.setter
    def width_pt(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def height(self) -> int:
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    @property
    def height_pt(self) -> float:
        ...
    
    @height_pt.setter
    def height_pt(self, value : float):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def left(self) -> int:
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @property
    def left_inch(self) -> float:
        ...
    
    @left_inch.setter
    def left_inch(self, value : float):
        ...
    
    @property
    def left_cm(self) -> float:
        ...
    
    @left_cm.setter
    def left_cm(self, value : float):
        ...
    
    @property
    def top(self) -> int:
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @property
    def top_inch(self) -> float:
        ...
    
    @top_inch.setter
    def top_inch(self, value : float):
        ...
    
    @property
    def top_cm(self) -> float:
        ...
    
    @top_cm.setter
    def top_cm(self, value : float):
        ...
    
    @property
    def top_to_corner(self) -> int:
        ...
    
    @top_to_corner.setter
    def top_to_corner(self, value : int):
        ...
    
    @property
    def left_to_corner(self) -> int:
        ...
    
    @left_to_corner.setter
    def left_to_corner(self, value : int):
        ...
    
    @property
    def x(self) -> int:
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @property
    def width_scale(self) -> int:
        ...
    
    @width_scale.setter
    def width_scale(self, value : int):
        ...
    
    @property
    def height_scale(self) -> int:
        ...
    
    @height_scale.setter
    def height_scale(self, value : int):
        ...
    
    @property
    def top_in_shape(self) -> int:
        ...
    
    @top_in_shape.setter
    def top_in_shape(self, value : int):
        ...
    
    @property
    def left_in_shape(self) -> int:
        ...
    
    @left_in_shape.setter
    def left_in_shape(self, value : int):
        ...
    
    @property
    def width_in_shape(self) -> int:
        ...
    
    @width_in_shape.setter
    def width_in_shape(self, value : int):
        ...
    
    @property
    def height_in_shape(self) -> int:
        ...
    
    @height_in_shape.setter
    def height_in_shape(self, value : int):
        ...
    
    @property
    def group(self) -> aspose.cells.drawing.GroupShape:
        '''Gets the group shape which contains this shape.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.AutoShapeType:
        '''Gets the auto shape type.'''
        ...
    
    @property
    def has_line(self) -> bool:
        ...
    
    @has_line.setter
    def has_line(self, value : bool):
        ...
    
    @property
    def is_filled(self) -> bool:
        ...
    
    @is_filled.setter
    def is_filled(self, value : bool):
        ...
    
    @property
    def is_flipped_horizontally(self) -> bool:
        ...
    
    @is_flipped_horizontally.setter
    def is_flipped_horizontally(self, value : bool):
        ...
    
    @property
    def is_flipped_vertically(self) -> bool:
        ...
    
    @is_flipped_vertically.setter
    def is_flipped_vertically(self, value : bool):
        ...
    
    @property
    def actual_lower_right_row(self) -> int:
        ...
    
    @property
    def connection_points(self) -> aspose.pydrawing.PointF[]:
        ...
    
    @property
    def relative_to_original_picture_size(self) -> bool:
        ...
    
    @relative_to_original_picture_size.setter
    def relative_to_original_picture_size(self, value : bool):
        ...
    
    @property
    def linked_cell(self) -> str:
        ...
    
    @linked_cell.setter
    def linked_cell(self, value : str):
        ...
    
    @property
    def input_range(self) -> str:
        ...
    
    @input_range.setter
    def input_range(self, value : str):
        ...
    
    @property
    def text_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @text_shape_type.setter
    def text_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def text_body(self) -> aspose.cells.drawing.texts.FontSettingCollection:
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Represents the font of shape.'''
        ...
    
    @font.setter
    def font(self, value : aspose.cells.Font):
        '''Represents the font of shape.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    @text_options.setter
    def text_options(self, value : aspose.cells.drawing.texts.TextOptions):
        ...
    
    @property
    def text(self) -> str:
        '''Represents the string in this TextBox object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Represents the string in this TextBox object.'''
        ...
    
    @property
    def is_rich_text(self) -> bool:
        ...
    
    @property
    def html_text(self) -> str:
        ...
    
    @html_text.setter
    def html_text(self, value : str):
        ...
    
    @property
    def text_vertical_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_vertical_overflow.setter
    def text_vertical_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def text_horizontal_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_horizontal_overflow.setter
    def text_horizontal_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
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
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def control_data(self) -> bytes:
        ...
    
    @property
    def active_x_control(self) -> aspose.cells.drawing.activexcontrols.ActiveXControl:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets the paths of a custom geometric shape.'''
        ...
    
    @property
    def geometry(self) -> aspose.cells.drawing.Geometry:
        '''Gets the geometry'''
        ...
    
    @property
    def create_id(self) -> Guid:
        ...
    
    @create_id.setter
    def create_id(self, value : Guid):
        ...
    
    @property
    def comment(self) -> aspose.cells.Comment:
        '''Gets the comment object.'''
        ...
    
    ...

class CustomGeometry(Geometry):
    '''Represents a custom geometric shape.'''
    
    @property
    def shape_adjust_values(self) -> aspose.cells.drawing.ShapeGuideCollection:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets path collection information when shape is a NotPrimitive autoshape'''
        ...
    
    ...

class CustomXmlShape(Shape):
    '''Represents Custom xml shape ,such as Ink.'''
    
    @overload
    def to_image(self, stream : io.RawIOBase, image_type : aspose.cells.drawing.ImageType):
        '''Creates the shape image and saves it to a stream in the specified format.
        
        :param stream: The output stream.
        :param image_type: The type in which to save the image.'''
        ...
    
    @overload
    def to_image(self, image_file : str, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a file.'''
        ...
    
    @overload
    def to_image(self, stream : io.RawIOBase, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a stream.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.'''
        ...
    
    def get_result_of_smart_art(self) -> aspose.cells.drawing.GroupShape:
        '''Converting smart art to grouped shapes.'''
        ...
    
    def to_front_or_back(self, orders : int):
        '''Brings the shape to the front or sends the shape to back.
        
        :param orders: If it's less than zero, sets the shape to back.
        If it's greater than zero, brings the shape to front.'''
        ...
    
    def get_locked_property(self, type : aspose.cells.drawing.ShapeLockType) -> bool:
        '''Gets the value of locked property.
        
        :param type: The type of the shape locked property.
        :returns: Returns  the value of locked property.'''
        ...
    
    def set_locked_property(self, type : aspose.cells.drawing.ShapeLockType, value : bool):
        '''Set the locked property.
        
        :param type: The locked type.
        :param value: The value of the property.'''
        ...
    
    def add_hyperlink(self, address : str) -> aspose.cells.Hyperlink:
        '''Adds a hyperlink to the shape.
        
        :param address: Address of the hyperlink.
        :returns: Return the new hyperlink object.'''
        ...
    
    def remove_hyperlink(self):
        '''Remove the hyperlink of the shape.'''
        ...
    
    def move_to_range(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int):
        '''Moves the shape to a specified range.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index'''
        ...
    
    def align_top_right_corner(self, top_row : int, right_column : int):
        '''Moves the picture to the top-right corner.
        
        :param top_row: the row index.
        :param right_column: the column index.'''
        ...
    
    def get_connection_points(self) -> List[List[float]]:
        '''Get the connection points
        
        :returns: [X,Y] pairs of the connection point. Every item is a float[2] array, [0] represents x and [1] represents y.'''
        ...
    
    def get_linked_cell(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range linked to the control's value.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range linked to the control's value.'''
        ...
    
    def set_linked_cell(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range linked to the control's value.
        
        :param formula: The range linked to the control's value.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def get_input_range(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range used to fill the control.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range used to fill the control.'''
        ...
    
    def set_input_range(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range used to fill the control.
        
        :param formula: The range used to fill the control.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell.'''
        ...
    
    def calculate_text_size(self) -> List[int]:
        '''Recalculate the text area
        
        :returns: Text's Size in an array(width and height).'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the text .
        
        :returns: All Characters objects'''
        ...
    
    def remove_active_x_control(self):
        '''Remove activeX control.'''
        ...
    
    def is_same_setting(self, obj : any) -> bool:
        '''Returns whether the shape is same.'''
        ...
    
    @property
    def macro_name(self) -> str:
        ...
    
    @macro_name.setter
    def macro_name(self, value : str):
        ...
    
    @property
    def is_equation(self) -> bool:
        ...
    
    @property
    def is_smart_art(self) -> bool:
        ...
    
    @property
    def z_order_position(self) -> int:
        ...
    
    @z_order_position.setter
    def z_order_position(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of the shape.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of the shape.'''
        ...
    
    @property
    def alternative_text(self) -> str:
        ...
    
    @alternative_text.setter
    def alternative_text(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @property
    def line_format(self) -> aspose.cells.drawing.MsoLineFormat:
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.MsoFillFormat:
        ...
    
    @property
    def format(self) -> aspose.cells.drawing.ShapeFormat:
        '''Represents the setting of the shape's formatting.'''
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        '''Gets line style'''
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        '''Returns a :py:attr:`aspose.cells.drawing.Shape.fill_format` object that contains fill formatting properties for the specified shape.'''
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def reflection(self) -> aspose.cells.drawing.ReflectionEffect:
        '''Represents a :py:class:`aspose.cells.drawing.ReflectionEffect` object that specifies reflection effect for the chart element or shape.'''
        ...
    
    @property
    def glow(self) -> aspose.cells.drawing.GlowEffect:
        '''Represents a :py:class:`aspose.cells.drawing.GlowEffect` object that specifies glow effect for the chart element or shape.'''
        ...
    
    @property
    def soft_edges(self) -> float:
        ...
    
    @soft_edges.setter
    def soft_edges(self, value : float):
        ...
    
    @property
    def three_d_format(self) -> aspose.cells.drawing.ThreeDFormat:
        ...
    
    @property
    def text_frame(self) -> aspose.cells.drawing.MsoTextFrame:
        ...
    
    @property
    def format_picture(self) -> aspose.cells.drawing.MsoFormatPicture:
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_lock_aspect_ratio(self) -> bool:
        ...
    
    @is_lock_aspect_ratio.setter
    def is_lock_aspect_ratio(self, value : bool):
        ...
    
    @property
    def rotation_angle(self) -> float:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : float):
        ...
    
    @property
    def hyperlink(self) -> aspose.cells.Hyperlink:
        '''Gets the hyperlink of the shape.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier of this shape.'''
        ...
    
    @property
    def spid(self) -> str:
        '''Specifies an optional string that an application can use to Identify the particular shape.'''
        ...
    
    @property
    def spt(self) -> int:
        '''Specifies an optional number that an application can use to associate the particular shape with a defined shape type.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.drawing.Shape.worksheet` object which contains this shape.'''
        ...
    
    @property
    def is_group(self) -> bool:
        ...
    
    @property
    def is_in_group(self) -> bool:
        ...
    
    @property
    def is_word_art(self) -> bool:
        ...
    
    @property
    def text_effect(self) -> aspose.cells.drawing.TextEffectFormat:
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_printable(self) -> bool:
        ...
    
    @is_printable.setter
    def is_printable(self, value : bool):
        ...
    
    @property
    def mso_drawing_type(self) -> aspose.cells.drawing.MsoDrawingType:
        ...
    
    @property
    def auto_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @auto_shape_type.setter
    def auto_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def anchor_type(self) -> aspose.cells.drawing.ShapeAnchorType:
        ...
    
    @anchor_type.setter
    def anchor_type(self, value : aspose.cells.drawing.ShapeAnchorType):
        ...
    
    @property
    def placement(self) -> aspose.cells.drawing.PlacementType:
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @placement.setter
    def placement(self, value : aspose.cells.drawing.PlacementType):
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @property
    def upper_left_row(self) -> int:
        ...
    
    @upper_left_row.setter
    def upper_left_row(self, value : int):
        ...
    
    @property
    def upper_delta_y(self) -> int:
        ...
    
    @upper_delta_y.setter
    def upper_delta_y(self, value : int):
        ...
    
    @property
    def upper_left_column(self) -> int:
        ...
    
    @upper_left_column.setter
    def upper_left_column(self, value : int):
        ...
    
    @property
    def upper_delta_x(self) -> int:
        ...
    
    @upper_delta_x.setter
    def upper_delta_x(self, value : int):
        ...
    
    @property
    def lower_right_row(self) -> int:
        ...
    
    @lower_right_row.setter
    def lower_right_row(self, value : int):
        ...
    
    @property
    def lower_delta_y(self) -> int:
        ...
    
    @lower_delta_y.setter
    def lower_delta_y(self, value : int):
        ...
    
    @property
    def lower_right_column(self) -> int:
        ...
    
    @lower_right_column.setter
    def lower_right_column(self, value : int):
        ...
    
    @property
    def lower_delta_x(self) -> int:
        ...
    
    @lower_delta_x.setter
    def lower_delta_x(self, value : int):
        ...
    
    @property
    def right(self) -> int:
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def width_pt(self) -> float:
        ...
    
    @width_pt.setter
    def width_pt(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def height(self) -> int:
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    @property
    def height_pt(self) -> float:
        ...
    
    @height_pt.setter
    def height_pt(self, value : float):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def left(self) -> int:
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @property
    def left_inch(self) -> float:
        ...
    
    @left_inch.setter
    def left_inch(self, value : float):
        ...
    
    @property
    def left_cm(self) -> float:
        ...
    
    @left_cm.setter
    def left_cm(self, value : float):
        ...
    
    @property
    def top(self) -> int:
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @property
    def top_inch(self) -> float:
        ...
    
    @top_inch.setter
    def top_inch(self, value : float):
        ...
    
    @property
    def top_cm(self) -> float:
        ...
    
    @top_cm.setter
    def top_cm(self, value : float):
        ...
    
    @property
    def top_to_corner(self) -> int:
        ...
    
    @top_to_corner.setter
    def top_to_corner(self, value : int):
        ...
    
    @property
    def left_to_corner(self) -> int:
        ...
    
    @left_to_corner.setter
    def left_to_corner(self, value : int):
        ...
    
    @property
    def x(self) -> int:
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @property
    def width_scale(self) -> int:
        ...
    
    @width_scale.setter
    def width_scale(self, value : int):
        ...
    
    @property
    def height_scale(self) -> int:
        ...
    
    @height_scale.setter
    def height_scale(self, value : int):
        ...
    
    @property
    def top_in_shape(self) -> int:
        ...
    
    @top_in_shape.setter
    def top_in_shape(self, value : int):
        ...
    
    @property
    def left_in_shape(self) -> int:
        ...
    
    @left_in_shape.setter
    def left_in_shape(self, value : int):
        ...
    
    @property
    def width_in_shape(self) -> int:
        ...
    
    @width_in_shape.setter
    def width_in_shape(self, value : int):
        ...
    
    @property
    def height_in_shape(self) -> int:
        ...
    
    @height_in_shape.setter
    def height_in_shape(self, value : int):
        ...
    
    @property
    def group(self) -> aspose.cells.drawing.GroupShape:
        '''Gets the group shape which contains this shape.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.AutoShapeType:
        '''Gets the auto shape type.'''
        ...
    
    @property
    def has_line(self) -> bool:
        ...
    
    @has_line.setter
    def has_line(self, value : bool):
        ...
    
    @property
    def is_filled(self) -> bool:
        ...
    
    @is_filled.setter
    def is_filled(self, value : bool):
        ...
    
    @property
    def is_flipped_horizontally(self) -> bool:
        ...
    
    @is_flipped_horizontally.setter
    def is_flipped_horizontally(self, value : bool):
        ...
    
    @property
    def is_flipped_vertically(self) -> bool:
        ...
    
    @is_flipped_vertically.setter
    def is_flipped_vertically(self, value : bool):
        ...
    
    @property
    def actual_lower_right_row(self) -> int:
        ...
    
    @property
    def connection_points(self) -> aspose.pydrawing.PointF[]:
        ...
    
    @property
    def relative_to_original_picture_size(self) -> bool:
        ...
    
    @relative_to_original_picture_size.setter
    def relative_to_original_picture_size(self, value : bool):
        ...
    
    @property
    def linked_cell(self) -> str:
        ...
    
    @linked_cell.setter
    def linked_cell(self, value : str):
        ...
    
    @property
    def input_range(self) -> str:
        ...
    
    @input_range.setter
    def input_range(self, value : str):
        ...
    
    @property
    def text_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @text_shape_type.setter
    def text_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def text_body(self) -> aspose.cells.drawing.texts.FontSettingCollection:
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Represents the font of shape.'''
        ...
    
    @font.setter
    def font(self, value : aspose.cells.Font):
        '''Represents the font of shape.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    @text_options.setter
    def text_options(self, value : aspose.cells.drawing.texts.TextOptions):
        ...
    
    @property
    def text(self) -> str:
        '''Represents the string in this TextBox object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Represents the string in this TextBox object.'''
        ...
    
    @property
    def is_rich_text(self) -> bool:
        ...
    
    @property
    def html_text(self) -> str:
        ...
    
    @html_text.setter
    def html_text(self, value : str):
        ...
    
    @property
    def text_vertical_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_vertical_overflow.setter
    def text_vertical_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def text_horizontal_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_horizontal_overflow.setter
    def text_horizontal_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
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
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def control_data(self) -> bytes:
        ...
    
    @property
    def active_x_control(self) -> aspose.cells.drawing.activexcontrols.ActiveXControl:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets the paths of a custom geometric shape.'''
        ...
    
    @property
    def geometry(self) -> aspose.cells.drawing.Geometry:
        '''Gets the geometry'''
        ...
    
    @property
    def create_id(self) -> Guid:
        ...
    
    @create_id.setter
    def create_id(self, value : Guid):
        ...
    
    ...

class DialogBox(Shape):
    '''Represents the dialog box.'''
    
    @overload
    def to_image(self, stream : io.RawIOBase, image_type : aspose.cells.drawing.ImageType):
        '''Creates the shape image and saves it to a stream in the specified format.
        
        :param stream: The output stream.
        :param image_type: The type in which to save the image.'''
        ...
    
    @overload
    def to_image(self, image_file : str, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a file.'''
        ...
    
    @overload
    def to_image(self, stream : io.RawIOBase, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a stream.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.'''
        ...
    
    def get_result_of_smart_art(self) -> aspose.cells.drawing.GroupShape:
        '''Converting smart art to grouped shapes.'''
        ...
    
    def to_front_or_back(self, orders : int):
        '''Brings the shape to the front or sends the shape to back.
        
        :param orders: If it's less than zero, sets the shape to back.
        If it's greater than zero, brings the shape to front.'''
        ...
    
    def get_locked_property(self, type : aspose.cells.drawing.ShapeLockType) -> bool:
        '''Gets the value of locked property.
        
        :param type: The type of the shape locked property.
        :returns: Returns  the value of locked property.'''
        ...
    
    def set_locked_property(self, type : aspose.cells.drawing.ShapeLockType, value : bool):
        '''Set the locked property.
        
        :param type: The locked type.
        :param value: The value of the property.'''
        ...
    
    def add_hyperlink(self, address : str) -> aspose.cells.Hyperlink:
        '''Adds a hyperlink to the shape.
        
        :param address: Address of the hyperlink.
        :returns: Return the new hyperlink object.'''
        ...
    
    def remove_hyperlink(self):
        '''Remove the hyperlink of the shape.'''
        ...
    
    def move_to_range(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int):
        '''Moves the shape to a specified range.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index'''
        ...
    
    def align_top_right_corner(self, top_row : int, right_column : int):
        '''Moves the picture to the top-right corner.
        
        :param top_row: the row index.
        :param right_column: the column index.'''
        ...
    
    def get_connection_points(self) -> List[List[float]]:
        '''Get the connection points
        
        :returns: [X,Y] pairs of the connection point. Every item is a float[2] array, [0] represents x and [1] represents y.'''
        ...
    
    def get_linked_cell(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range linked to the control's value.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range linked to the control's value.'''
        ...
    
    def set_linked_cell(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range linked to the control's value.
        
        :param formula: The range linked to the control's value.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def get_input_range(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range used to fill the control.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range used to fill the control.'''
        ...
    
    def set_input_range(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range used to fill the control.
        
        :param formula: The range used to fill the control.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell.'''
        ...
    
    def calculate_text_size(self) -> List[int]:
        '''Recalculate the text area
        
        :returns: Text's Size in an array(width and height).'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the text .
        
        :returns: All Characters objects'''
        ...
    
    def remove_active_x_control(self):
        '''Remove activeX control.'''
        ...
    
    def is_same_setting(self, obj : any) -> bool:
        '''Returns whether the shape is same.'''
        ...
    
    @property
    def macro_name(self) -> str:
        ...
    
    @macro_name.setter
    def macro_name(self, value : str):
        ...
    
    @property
    def is_equation(self) -> bool:
        ...
    
    @property
    def is_smart_art(self) -> bool:
        ...
    
    @property
    def z_order_position(self) -> int:
        ...
    
    @z_order_position.setter
    def z_order_position(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of the shape.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of the shape.'''
        ...
    
    @property
    def alternative_text(self) -> str:
        ...
    
    @alternative_text.setter
    def alternative_text(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @property
    def line_format(self) -> aspose.cells.drawing.MsoLineFormat:
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.MsoFillFormat:
        ...
    
    @property
    def format(self) -> aspose.cells.drawing.ShapeFormat:
        '''Represents the setting of the shape's formatting.'''
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        '''Gets line style'''
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        '''Returns a :py:attr:`aspose.cells.drawing.Shape.fill_format` object that contains fill formatting properties for the specified shape.'''
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def reflection(self) -> aspose.cells.drawing.ReflectionEffect:
        '''Represents a :py:class:`aspose.cells.drawing.ReflectionEffect` object that specifies reflection effect for the chart element or shape.'''
        ...
    
    @property
    def glow(self) -> aspose.cells.drawing.GlowEffect:
        '''Represents a :py:class:`aspose.cells.drawing.GlowEffect` object that specifies glow effect for the chart element or shape.'''
        ...
    
    @property
    def soft_edges(self) -> float:
        ...
    
    @soft_edges.setter
    def soft_edges(self, value : float):
        ...
    
    @property
    def three_d_format(self) -> aspose.cells.drawing.ThreeDFormat:
        ...
    
    @property
    def text_frame(self) -> aspose.cells.drawing.MsoTextFrame:
        ...
    
    @property
    def format_picture(self) -> aspose.cells.drawing.MsoFormatPicture:
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_lock_aspect_ratio(self) -> bool:
        ...
    
    @is_lock_aspect_ratio.setter
    def is_lock_aspect_ratio(self, value : bool):
        ...
    
    @property
    def rotation_angle(self) -> float:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : float):
        ...
    
    @property
    def hyperlink(self) -> aspose.cells.Hyperlink:
        '''Gets the hyperlink of the shape.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier of this shape.'''
        ...
    
    @property
    def spid(self) -> str:
        '''Specifies an optional string that an application can use to Identify the particular shape.'''
        ...
    
    @property
    def spt(self) -> int:
        '''Specifies an optional number that an application can use to associate the particular shape with a defined shape type.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.drawing.Shape.worksheet` object which contains this shape.'''
        ...
    
    @property
    def is_group(self) -> bool:
        ...
    
    @property
    def is_in_group(self) -> bool:
        ...
    
    @property
    def is_word_art(self) -> bool:
        ...
    
    @property
    def text_effect(self) -> aspose.cells.drawing.TextEffectFormat:
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_printable(self) -> bool:
        ...
    
    @is_printable.setter
    def is_printable(self, value : bool):
        ...
    
    @property
    def mso_drawing_type(self) -> aspose.cells.drawing.MsoDrawingType:
        ...
    
    @property
    def auto_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @auto_shape_type.setter
    def auto_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def anchor_type(self) -> aspose.cells.drawing.ShapeAnchorType:
        ...
    
    @anchor_type.setter
    def anchor_type(self, value : aspose.cells.drawing.ShapeAnchorType):
        ...
    
    @property
    def placement(self) -> aspose.cells.drawing.PlacementType:
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @placement.setter
    def placement(self, value : aspose.cells.drawing.PlacementType):
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @property
    def upper_left_row(self) -> int:
        ...
    
    @upper_left_row.setter
    def upper_left_row(self, value : int):
        ...
    
    @property
    def upper_delta_y(self) -> int:
        ...
    
    @upper_delta_y.setter
    def upper_delta_y(self, value : int):
        ...
    
    @property
    def upper_left_column(self) -> int:
        ...
    
    @upper_left_column.setter
    def upper_left_column(self, value : int):
        ...
    
    @property
    def upper_delta_x(self) -> int:
        ...
    
    @upper_delta_x.setter
    def upper_delta_x(self, value : int):
        ...
    
    @property
    def lower_right_row(self) -> int:
        ...
    
    @lower_right_row.setter
    def lower_right_row(self, value : int):
        ...
    
    @property
    def lower_delta_y(self) -> int:
        ...
    
    @lower_delta_y.setter
    def lower_delta_y(self, value : int):
        ...
    
    @property
    def lower_right_column(self) -> int:
        ...
    
    @lower_right_column.setter
    def lower_right_column(self, value : int):
        ...
    
    @property
    def lower_delta_x(self) -> int:
        ...
    
    @lower_delta_x.setter
    def lower_delta_x(self, value : int):
        ...
    
    @property
    def right(self) -> int:
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def width_pt(self) -> float:
        ...
    
    @width_pt.setter
    def width_pt(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def height(self) -> int:
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    @property
    def height_pt(self) -> float:
        ...
    
    @height_pt.setter
    def height_pt(self, value : float):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def left(self) -> int:
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @property
    def left_inch(self) -> float:
        ...
    
    @left_inch.setter
    def left_inch(self, value : float):
        ...
    
    @property
    def left_cm(self) -> float:
        ...
    
    @left_cm.setter
    def left_cm(self, value : float):
        ...
    
    @property
    def top(self) -> int:
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @property
    def top_inch(self) -> float:
        ...
    
    @top_inch.setter
    def top_inch(self, value : float):
        ...
    
    @property
    def top_cm(self) -> float:
        ...
    
    @top_cm.setter
    def top_cm(self, value : float):
        ...
    
    @property
    def top_to_corner(self) -> int:
        ...
    
    @top_to_corner.setter
    def top_to_corner(self, value : int):
        ...
    
    @property
    def left_to_corner(self) -> int:
        ...
    
    @left_to_corner.setter
    def left_to_corner(self, value : int):
        ...
    
    @property
    def x(self) -> int:
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @property
    def width_scale(self) -> int:
        ...
    
    @width_scale.setter
    def width_scale(self, value : int):
        ...
    
    @property
    def height_scale(self) -> int:
        ...
    
    @height_scale.setter
    def height_scale(self, value : int):
        ...
    
    @property
    def top_in_shape(self) -> int:
        ...
    
    @top_in_shape.setter
    def top_in_shape(self, value : int):
        ...
    
    @property
    def left_in_shape(self) -> int:
        ...
    
    @left_in_shape.setter
    def left_in_shape(self, value : int):
        ...
    
    @property
    def width_in_shape(self) -> int:
        ...
    
    @width_in_shape.setter
    def width_in_shape(self, value : int):
        ...
    
    @property
    def height_in_shape(self) -> int:
        ...
    
    @height_in_shape.setter
    def height_in_shape(self, value : int):
        ...
    
    @property
    def group(self) -> aspose.cells.drawing.GroupShape:
        '''Gets the group shape which contains this shape.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.AutoShapeType:
        '''Gets the auto shape type.'''
        ...
    
    @property
    def has_line(self) -> bool:
        ...
    
    @has_line.setter
    def has_line(self, value : bool):
        ...
    
    @property
    def is_filled(self) -> bool:
        ...
    
    @is_filled.setter
    def is_filled(self, value : bool):
        ...
    
    @property
    def is_flipped_horizontally(self) -> bool:
        ...
    
    @is_flipped_horizontally.setter
    def is_flipped_horizontally(self, value : bool):
        ...
    
    @property
    def is_flipped_vertically(self) -> bool:
        ...
    
    @is_flipped_vertically.setter
    def is_flipped_vertically(self, value : bool):
        ...
    
    @property
    def actual_lower_right_row(self) -> int:
        ...
    
    @property
    def connection_points(self) -> aspose.pydrawing.PointF[]:
        ...
    
    @property
    def relative_to_original_picture_size(self) -> bool:
        ...
    
    @relative_to_original_picture_size.setter
    def relative_to_original_picture_size(self, value : bool):
        ...
    
    @property
    def linked_cell(self) -> str:
        ...
    
    @linked_cell.setter
    def linked_cell(self, value : str):
        ...
    
    @property
    def input_range(self) -> str:
        ...
    
    @input_range.setter
    def input_range(self, value : str):
        ...
    
    @property
    def text_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @text_shape_type.setter
    def text_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def text_body(self) -> aspose.cells.drawing.texts.FontSettingCollection:
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Represents the font of shape.'''
        ...
    
    @font.setter
    def font(self, value : aspose.cells.Font):
        '''Represents the font of shape.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    @text_options.setter
    def text_options(self, value : aspose.cells.drawing.texts.TextOptions):
        ...
    
    @property
    def text(self) -> str:
        '''Represents the string in this TextBox object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Represents the string in this TextBox object.'''
        ...
    
    @property
    def is_rich_text(self) -> bool:
        ...
    
    @property
    def html_text(self) -> str:
        ...
    
    @html_text.setter
    def html_text(self, value : str):
        ...
    
    @property
    def text_vertical_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_vertical_overflow.setter
    def text_vertical_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def text_horizontal_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_horizontal_overflow.setter
    def text_horizontal_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
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
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def control_data(self) -> bytes:
        ...
    
    @property
    def active_x_control(self) -> aspose.cells.drawing.activexcontrols.ActiveXControl:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets the paths of a custom geometric shape.'''
        ...
    
    @property
    def geometry(self) -> aspose.cells.drawing.Geometry:
        '''Gets the geometry'''
        ...
    
    @property
    def create_id(self) -> Guid:
        ...
    
    @create_id.setter
    def create_id(self, value : Guid):
        ...
    
    ...

class Fill:
    '''Represents the fill format of the shape.'''
    
    ...

class FillFormat:
    '''Encapsulates the object that represents fill formatting for a shape.'''
    
    @overload
    def set_two_color_gradient(self, color1 : aspose.pydrawing.Color, color2 : aspose.pydrawing.Color, style : aspose.cells.drawing.GradientStyleType, variant : int):
        '''Sets the specified fill to a two-color gradient.
        Only applies for Excel 2007.
        
        :param color1: One gradient color.
        :param color2: Two gradient color.
        :param style: Gradient shading style.
        :param variant: The gradient variant. Can be a value from 1 through 4, corresponding to one of the four variants on the Gradient tab in the Fill Effects dialog box. If style is GradientStyle.FromCenter, the Variant argument can only be 1 or 2.'''
        ...
    
    @overload
    def set_two_color_gradient(self, color1 : aspose.pydrawing.Color, transparency1 : float, color2 : aspose.pydrawing.Color, transparency2 : float, style : aspose.cells.drawing.GradientStyleType, variant : int):
        '''Sets the specified fill to a two-color gradient.
        Only applies for Excel 2007.
        
        :param color1: One gradient color.
        :param transparency1: The degree of transparency of the color1 as a value from 0.0 (opaque) through 1.0 (clear).
        :param color2: Two gradient color.
        :param transparency2: The degree of transparency of the color2 as a value from 0.0 (opaque) through 1.0 (clear).
        :param style: Gradient shading style.
        :param variant: The gradient variant. Can be a value from 1 through 4, corresponding to one of the four variants on the Gradient tab in the Fill Effects dialog box. If style is GradientStyle.FromCenter, the Variant argument can only be 1 or 2.'''
        ...
    
    def set_one_color_gradient(self, color : aspose.pydrawing.Color, degree : float, style : aspose.cells.drawing.GradientStyleType, variant : int):
        '''Sets the specified fill to a one-color gradient.
        Only applies for Excel 2007.
        
        :param color: One gradient color.
        :param degree: The gradient degree. Can be a value from 0.0 (dark) through 1.0 (light).
        :param style: Gradient shading style.
        :param variant: The gradient variant. Can be a value from 1 through 4, corresponding to one of the four variants on the Gradient tab in the Fill Effects dialog box. If style is GradientStyle.FromCenter, the Variant argument can only be 1 or 2.'''
        ...
    
    def set_preset_color_gradient(self, preset_color : aspose.cells.drawing.GradientPresetType, style : aspose.cells.drawing.GradientStyleType, variant : int):
        '''Sets the specified fill to a preset-color gradient.
        Only applies for Excel 2007.
        
        :param preset_color: Preset color type
        :param style: Gradient shading style.
        :param variant: The gradient variant. Can be a value from 1 through 4, corresponding to one of the four variants on the Gradient tab in the Fill Effects dialog box. If style is GradientStyle.FromCenter, the Variant argument can only be 1 or 2.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.FillType:
        '''Gets and sets the fill type.'''
        ...
    
    @type.setter
    def type(self, value : aspose.cells.drawing.FillType):
        '''Gets and sets the fill type.'''
        ...
    
    @property
    def fill_type(self) -> aspose.cells.drawing.FillType:
        ...
    
    @fill_type.setter
    def fill_type(self, value : aspose.cells.drawing.FillType):
        ...
    
    @property
    def transparency(self) -> float:
        '''Returns the degree of transparency of the area as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    @transparency.setter
    def transparency(self, value : float):
        '''Returns or sets the degree of transparency of the area as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    @property
    def set_type(self) -> aspose.cells.drawing.FormatSetType:
        ...
    
    @set_type.setter
    def set_type(self, value : aspose.cells.drawing.FormatSetType):
        ...
    
    @property
    def gradient_fill(self) -> aspose.cells.drawing.GradientFill:
        ...
    
    @property
    def texture_fill(self) -> aspose.cells.drawing.TextureFill:
        ...
    
    @property
    def solid_fill(self) -> aspose.cells.drawing.SolidFill:
        ...
    
    @property
    def pattern_fill(self) -> aspose.cells.drawing.PatternFill:
        ...
    
    @property
    def gradient_color_type(self) -> aspose.cells.drawing.GradientColorType:
        ...
    
    @property
    def gradient_style(self) -> aspose.cells.drawing.GradientStyleType:
        ...
    
    @property
    def gradient_color1(self) -> aspose.pydrawing.Color:
        ...
    
    @property
    def gradient_color2(self) -> aspose.pydrawing.Color:
        ...
    
    @property
    def gradient_degree(self) -> float:
        ...
    
    @property
    def gradient_variant(self) -> int:
        ...
    
    @property
    def preset_color(self) -> aspose.cells.drawing.GradientPresetType:
        ...
    
    @property
    def texture(self) -> aspose.cells.drawing.TextureType:
        '''Represents the texture type for the specified fill.'''
        ...
    
    @texture.setter
    def texture(self, value : aspose.cells.drawing.TextureType):
        '''Represents the texture type for the specified fill.'''
        ...
    
    @property
    def pattern(self) -> aspose.cells.drawing.FillPattern:
        '''Represents an area's display pattern.'''
        ...
    
    @pattern.setter
    def pattern(self, value : aspose.cells.drawing.FillPattern):
        '''Represents an area's display pattern.'''
        ...
    
    @property
    def picture_format_type(self) -> aspose.cells.drawing.FillPictureType:
        ...
    
    @picture_format_type.setter
    def picture_format_type(self, value : aspose.cells.drawing.FillPictureType):
        ...
    
    @property
    def scale(self) -> float:
        '''Gets and sets the picture format scale.'''
        ...
    
    @scale.setter
    def scale(self, value : float):
        '''Gets and sets the picture format scale.'''
        ...
    
    @property
    def image_data(self) -> bytes:
        ...
    
    @image_data.setter
    def image_data(self, value : bytes):
        ...
    
    ...

class Format3D:
    '''This class specifies the 3D shape properties for a chart element or shape.'''
    
    def has_top_bevel_data(self) -> bool:
        '''Indicates if the shape has top bevel data.'''
        ...
    
    @property
    def top_bevel(self) -> aspose.cells.drawing.Bevel:
        ...
    
    @property
    def surface_material_type(self) -> aspose.cells.drawing.PresetMaterialType:
        ...
    
    @surface_material_type.setter
    def surface_material_type(self, value : aspose.cells.drawing.PresetMaterialType):
        ...
    
    @property
    def surface_lighting_type(self) -> aspose.cells.drawing.LightRigType:
        ...
    
    @surface_lighting_type.setter
    def surface_lighting_type(self, value : aspose.cells.drawing.LightRigType):
        ...
    
    @property
    def lighting_angle(self) -> float:
        ...
    
    @lighting_angle.setter
    def lighting_angle(self, value : float):
        ...
    
    ...

class Geometry:
    '''Represents a geometric shape.'''
    
    @property
    def shape_adjust_values(self) -> aspose.cells.drawing.ShapeGuideCollection:
        ...
    
    ...

class GlowEffect:
    '''This class specifies a glow effect, in which a color blurred outline
    is added outside the edges of the object.'''
    
    @property
    def color(self) -> aspose.cells.CellsColor:
        '''Gets the color of the glow effect.'''
        ...
    
    @color.setter
    def color(self, value : aspose.cells.CellsColor):
        '''Gets the color of the glow effect.'''
        ...
    
    @property
    def radius(self) -> float:
        '''Gets and sets the radius of the glow, in unit of points.'''
        ...
    
    @radius.setter
    def radius(self, value : float):
        '''Gets and sets the radius of the glow, in unit of points.'''
        ...
    
    @property
    def size(self) -> float:
        '''Gets and sets the radius of the glow, in unit of points.'''
        ...
    
    @size.setter
    def size(self, value : float):
        '''Gets and sets the radius of the glow, in unit of points.'''
        ...
    
    @property
    def transparency(self) -> float:
        '''Gets and sets the degree of transparency of the glow effect. Range from 0.0 (opaque) to 1.0 (clear).'''
        ...
    
    @transparency.setter
    def transparency(self, value : float):
        '''Gets and sets the degree of transparency of the glow effect. Range from 0.0 (opaque) to 1.0 (clear).'''
        ...
    
    ...

class GradientFill(Fill):
    '''Represents the gradient fill.'''
    
    @overload
    def set_two_color_gradient(self, color1 : aspose.pydrawing.Color, color2 : aspose.pydrawing.Color, style : aspose.cells.drawing.GradientStyleType, variant : int):
        '''Sets the specified fill to a two-color gradient.
        Only applies for Excel 2007.
        
        :param color1: One gradient color.
        :param color2: Two gradient color.
        :param style: Gradient shading style.
        :param variant: The gradient variant. Can be a value from 1 through 4, corresponding to one of the four variants on the Gradient tab in the Fill Effects dialog box. If style is GradientStyle.FromCenter, the Variant argument can only be 1 or 2.'''
        ...
    
    @overload
    def set_two_color_gradient(self, color1 : aspose.pydrawing.Color, transparency1 : float, color2 : aspose.pydrawing.Color, transparency2 : float, style : aspose.cells.drawing.GradientStyleType, variant : int):
        '''Sets the specified fill to a two-color gradient.
        Only applies for Excel 2007.
        
        :param color1: One gradient color.
        :param transparency1: The degree of transparency of the color1 as a value from 0.0 (opaque) through 1.0 (clear).
        :param color2: Two gradient color.
        :param transparency2: The degree of transparency of the color2 as a value from 0.0 (opaque) through 1.0 (clear).
        :param style: Gradient shading style.
        :param variant: The gradient variant. Can be a value from 1 through 4, corresponding to one of the four variants on the Gradient tab in the Fill Effects dialog box. If style is GradientStyle.FromCenter, the Variant argument can only be 1 or 2.'''
        ...
    
    def set_gradient(self, type : aspose.cells.drawing.GradientFillType, angle : float, direction : aspose.cells.drawing.GradientDirectionType):
        '''Set the gradient fill type and direction.
        
        :param type: Gradient fill type.
        :param angle: The angle. Only applies for GradientFillType.Linear.
        :param direction: The direction type. Only applies for GradientFillType.Radial and GradientFillType.Rectangle.'''
        ...
    
    def set_preset_theme_gradient(self, gradient_type : aspose.cells.drawing.PresetThemeGradientType, theme_color_type : aspose.cells.ThemeColorType):
        '''Sets preset theme gradient fill.
        
        :param gradient_type: The preset gradient type.
        :param theme_color_type: The theme color type.'''
        ...
    
    def set_one_color_gradient(self, color : aspose.pydrawing.Color, degree : float, style : aspose.cells.drawing.GradientStyleType, variant : int):
        '''Sets the specified fill to a one-color gradient.
        Only applies for Excel 2007.
        
        :param color: One gradient color.
        :param degree: The gradient degree. Can be a value from 0.0 (dark) through 1.0 (light).
        :param style: Gradient shading style.
        :param variant: The gradient variant. Can be a value from 1 through 4, corresponding to one of the four variants on the Gradient tab in the Fill Effects dialog box. If style is GradientStyle.FromCenter, the Variant argument can only be 1 or 2.'''
        ...
    
    @property
    def gradient_stops(self) -> aspose.cells.drawing.GradientStopCollection:
        ...
    
    @property
    def fill_type(self) -> aspose.cells.drawing.GradientFillType:
        ...
    
    @property
    def direction_type(self) -> aspose.cells.drawing.GradientDirectionType:
        ...
    
    @property
    def angle(self) -> float:
        '''The angle of linear fill.'''
        ...
    
    @angle.setter
    def angle(self, value : float):
        '''The angle of linear fill.'''
        ...
    
    ...

class GradientStop:
    '''Represents the gradient stop.'''
    
    @property
    def position(self) -> float:
        '''The position of the stop.'''
        ...
    
    @position.setter
    def position(self, value : float):
        '''The position of the stop.'''
        ...
    
    @property
    def cells_color(self) -> aspose.cells.CellsColor:
        ...
    
    @property
    def transparency(self) -> float:
        '''Returns the degree of transparency of the area as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    @transparency.setter
    def transparency(self, value : float):
        '''Returns or sets the degree of transparency of the area as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    ...

class GradientStopCollection:
    '''Represents the gradient stop collection.'''
    
    @overload
    def add(self, position : float, color : aspose.cells.CellsColor, alpha : int):
        '''Add a gradient stop.
        
        :param position: The position of the stop,in unit of percentage.
        :param color: The color of the stop.
        :param alpha: The alpha of the color.'''
        ...
    
    @overload
    def add(self, position : float, color : aspose.pydrawing.Color, alpha : int):
        '''Add a gradient stop.
        
        :param position: The position of the stop,in unit of percentage.
        :param color: The color of the stop.
        :param alpha: The alpha of the color.'''
        ...
    
    @overload
    def copy_to(self, array : List[aspose.cells.drawing.GradientStop]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.drawing.GradientStop], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.drawing.GradientStop, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.drawing.GradientStop, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.GradientStop) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.GradientStop, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.GradientStop, index : int, count : int) -> int:
        ...
    
    def binary_search(self, item : aspose.cells.drawing.GradientStop) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class GroupBox(Shape):
    '''Encapsulates the object that represents a groupbox in a spreadsheet.'''
    
    @overload
    def to_image(self, stream : io.RawIOBase, image_type : aspose.cells.drawing.ImageType):
        '''Creates the shape image and saves it to a stream in the specified format.
        
        :param stream: The output stream.
        :param image_type: The type in which to save the image.'''
        ...
    
    @overload
    def to_image(self, image_file : str, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a file.'''
        ...
    
    @overload
    def to_image(self, stream : io.RawIOBase, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a stream.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.'''
        ...
    
    def get_result_of_smart_art(self) -> aspose.cells.drawing.GroupShape:
        '''Converting smart art to grouped shapes.'''
        ...
    
    def to_front_or_back(self, orders : int):
        '''Brings the shape to the front or sends the shape to back.
        
        :param orders: If it's less than zero, sets the shape to back.
        If it's greater than zero, brings the shape to front.'''
        ...
    
    def get_locked_property(self, type : aspose.cells.drawing.ShapeLockType) -> bool:
        '''Gets the value of locked property.
        
        :param type: The type of the shape locked property.
        :returns: Returns  the value of locked property.'''
        ...
    
    def set_locked_property(self, type : aspose.cells.drawing.ShapeLockType, value : bool):
        '''Set the locked property.
        
        :param type: The locked type.
        :param value: The value of the property.'''
        ...
    
    def add_hyperlink(self, address : str) -> aspose.cells.Hyperlink:
        '''Adds a hyperlink to the shape.
        
        :param address: Address of the hyperlink.
        :returns: Return the new hyperlink object.'''
        ...
    
    def remove_hyperlink(self):
        '''Remove the hyperlink of the shape.'''
        ...
    
    def move_to_range(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int):
        '''Moves the shape to a specified range.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index'''
        ...
    
    def align_top_right_corner(self, top_row : int, right_column : int):
        '''Moves the picture to the top-right corner.
        
        :param top_row: the row index.
        :param right_column: the column index.'''
        ...
    
    def get_connection_points(self) -> List[List[float]]:
        '''Get the connection points
        
        :returns: [X,Y] pairs of the connection point. Every item is a float[2] array, [0] represents x and [1] represents y.'''
        ...
    
    def get_linked_cell(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range linked to the control's value.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range linked to the control's value.'''
        ...
    
    def set_linked_cell(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range linked to the control's value.
        
        :param formula: The range linked to the control's value.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def get_input_range(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range used to fill the control.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range used to fill the control.'''
        ...
    
    def set_input_range(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range used to fill the control.
        
        :param formula: The range used to fill the control.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell.'''
        ...
    
    def calculate_text_size(self) -> List[int]:
        '''Recalculate the text area
        
        :returns: Text's Size in an array(width and height).'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the text .
        
        :returns: All Characters objects'''
        ...
    
    def remove_active_x_control(self):
        '''Remove activeX control.'''
        ...
    
    def is_same_setting(self, obj : any) -> bool:
        '''Returns whether the shape is same.'''
        ...
    
    @property
    def macro_name(self) -> str:
        ...
    
    @macro_name.setter
    def macro_name(self, value : str):
        ...
    
    @property
    def is_equation(self) -> bool:
        ...
    
    @property
    def is_smart_art(self) -> bool:
        ...
    
    @property
    def z_order_position(self) -> int:
        ...
    
    @z_order_position.setter
    def z_order_position(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of the shape.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of the shape.'''
        ...
    
    @property
    def alternative_text(self) -> str:
        ...
    
    @alternative_text.setter
    def alternative_text(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @property
    def line_format(self) -> aspose.cells.drawing.MsoLineFormat:
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.MsoFillFormat:
        ...
    
    @property
    def format(self) -> aspose.cells.drawing.ShapeFormat:
        '''Represents the setting of the shape's formatting.'''
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        '''Gets line style'''
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        '''Returns a :py:attr:`aspose.cells.drawing.Shape.fill_format` object that contains fill formatting properties for the specified shape.'''
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def reflection(self) -> aspose.cells.drawing.ReflectionEffect:
        '''Represents a :py:class:`aspose.cells.drawing.ReflectionEffect` object that specifies reflection effect for the chart element or shape.'''
        ...
    
    @property
    def glow(self) -> aspose.cells.drawing.GlowEffect:
        '''Represents a :py:class:`aspose.cells.drawing.GlowEffect` object that specifies glow effect for the chart element or shape.'''
        ...
    
    @property
    def soft_edges(self) -> float:
        ...
    
    @soft_edges.setter
    def soft_edges(self, value : float):
        ...
    
    @property
    def three_d_format(self) -> aspose.cells.drawing.ThreeDFormat:
        ...
    
    @property
    def text_frame(self) -> aspose.cells.drawing.MsoTextFrame:
        ...
    
    @property
    def format_picture(self) -> aspose.cells.drawing.MsoFormatPicture:
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_lock_aspect_ratio(self) -> bool:
        ...
    
    @is_lock_aspect_ratio.setter
    def is_lock_aspect_ratio(self, value : bool):
        ...
    
    @property
    def rotation_angle(self) -> float:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : float):
        ...
    
    @property
    def hyperlink(self) -> aspose.cells.Hyperlink:
        '''Gets the hyperlink of the shape.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier of this shape.'''
        ...
    
    @property
    def spid(self) -> str:
        '''Specifies an optional string that an application can use to Identify the particular shape.'''
        ...
    
    @property
    def spt(self) -> int:
        '''Specifies an optional number that an application can use to associate the particular shape with a defined shape type.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.drawing.Shape.worksheet` object which contains this shape.'''
        ...
    
    @property
    def is_group(self) -> bool:
        ...
    
    @property
    def is_in_group(self) -> bool:
        ...
    
    @property
    def is_word_art(self) -> bool:
        ...
    
    @property
    def text_effect(self) -> aspose.cells.drawing.TextEffectFormat:
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_printable(self) -> bool:
        ...
    
    @is_printable.setter
    def is_printable(self, value : bool):
        ...
    
    @property
    def mso_drawing_type(self) -> aspose.cells.drawing.MsoDrawingType:
        ...
    
    @property
    def auto_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @auto_shape_type.setter
    def auto_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def anchor_type(self) -> aspose.cells.drawing.ShapeAnchorType:
        ...
    
    @anchor_type.setter
    def anchor_type(self, value : aspose.cells.drawing.ShapeAnchorType):
        ...
    
    @property
    def placement(self) -> aspose.cells.drawing.PlacementType:
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @placement.setter
    def placement(self, value : aspose.cells.drawing.PlacementType):
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @property
    def upper_left_row(self) -> int:
        ...
    
    @upper_left_row.setter
    def upper_left_row(self, value : int):
        ...
    
    @property
    def upper_delta_y(self) -> int:
        ...
    
    @upper_delta_y.setter
    def upper_delta_y(self, value : int):
        ...
    
    @property
    def upper_left_column(self) -> int:
        ...
    
    @upper_left_column.setter
    def upper_left_column(self, value : int):
        ...
    
    @property
    def upper_delta_x(self) -> int:
        ...
    
    @upper_delta_x.setter
    def upper_delta_x(self, value : int):
        ...
    
    @property
    def lower_right_row(self) -> int:
        ...
    
    @lower_right_row.setter
    def lower_right_row(self, value : int):
        ...
    
    @property
    def lower_delta_y(self) -> int:
        ...
    
    @lower_delta_y.setter
    def lower_delta_y(self, value : int):
        ...
    
    @property
    def lower_right_column(self) -> int:
        ...
    
    @lower_right_column.setter
    def lower_right_column(self, value : int):
        ...
    
    @property
    def lower_delta_x(self) -> int:
        ...
    
    @lower_delta_x.setter
    def lower_delta_x(self, value : int):
        ...
    
    @property
    def right(self) -> int:
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def width_pt(self) -> float:
        ...
    
    @width_pt.setter
    def width_pt(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def height(self) -> int:
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    @property
    def height_pt(self) -> float:
        ...
    
    @height_pt.setter
    def height_pt(self, value : float):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def left(self) -> int:
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @property
    def left_inch(self) -> float:
        ...
    
    @left_inch.setter
    def left_inch(self, value : float):
        ...
    
    @property
    def left_cm(self) -> float:
        ...
    
    @left_cm.setter
    def left_cm(self, value : float):
        ...
    
    @property
    def top(self) -> int:
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @property
    def top_inch(self) -> float:
        ...
    
    @top_inch.setter
    def top_inch(self, value : float):
        ...
    
    @property
    def top_cm(self) -> float:
        ...
    
    @top_cm.setter
    def top_cm(self, value : float):
        ...
    
    @property
    def top_to_corner(self) -> int:
        ...
    
    @top_to_corner.setter
    def top_to_corner(self, value : int):
        ...
    
    @property
    def left_to_corner(self) -> int:
        ...
    
    @left_to_corner.setter
    def left_to_corner(self, value : int):
        ...
    
    @property
    def x(self) -> int:
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @property
    def width_scale(self) -> int:
        ...
    
    @width_scale.setter
    def width_scale(self, value : int):
        ...
    
    @property
    def height_scale(self) -> int:
        ...
    
    @height_scale.setter
    def height_scale(self, value : int):
        ...
    
    @property
    def top_in_shape(self) -> int:
        ...
    
    @top_in_shape.setter
    def top_in_shape(self, value : int):
        ...
    
    @property
    def left_in_shape(self) -> int:
        ...
    
    @left_in_shape.setter
    def left_in_shape(self, value : int):
        ...
    
    @property
    def width_in_shape(self) -> int:
        ...
    
    @width_in_shape.setter
    def width_in_shape(self, value : int):
        ...
    
    @property
    def height_in_shape(self) -> int:
        ...
    
    @height_in_shape.setter
    def height_in_shape(self, value : int):
        ...
    
    @property
    def group(self) -> aspose.cells.drawing.GroupShape:
        '''Gets the group shape which contains this shape.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.AutoShapeType:
        '''Gets the auto shape type.'''
        ...
    
    @property
    def has_line(self) -> bool:
        ...
    
    @has_line.setter
    def has_line(self, value : bool):
        ...
    
    @property
    def is_filled(self) -> bool:
        ...
    
    @is_filled.setter
    def is_filled(self, value : bool):
        ...
    
    @property
    def is_flipped_horizontally(self) -> bool:
        ...
    
    @is_flipped_horizontally.setter
    def is_flipped_horizontally(self, value : bool):
        ...
    
    @property
    def is_flipped_vertically(self) -> bool:
        ...
    
    @is_flipped_vertically.setter
    def is_flipped_vertically(self, value : bool):
        ...
    
    @property
    def actual_lower_right_row(self) -> int:
        ...
    
    @property
    def connection_points(self) -> aspose.pydrawing.PointF[]:
        ...
    
    @property
    def relative_to_original_picture_size(self) -> bool:
        ...
    
    @relative_to_original_picture_size.setter
    def relative_to_original_picture_size(self, value : bool):
        ...
    
    @property
    def linked_cell(self) -> str:
        ...
    
    @linked_cell.setter
    def linked_cell(self, value : str):
        ...
    
    @property
    def input_range(self) -> str:
        ...
    
    @input_range.setter
    def input_range(self, value : str):
        ...
    
    @property
    def text_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @text_shape_type.setter
    def text_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def text_body(self) -> aspose.cells.drawing.texts.FontSettingCollection:
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Represents the font of shape.'''
        ...
    
    @font.setter
    def font(self, value : aspose.cells.Font):
        '''Represents the font of shape.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    @text_options.setter
    def text_options(self, value : aspose.cells.drawing.texts.TextOptions):
        ...
    
    @property
    def text(self) -> str:
        '''Represents the string in this TextBox object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Represents the string in this TextBox object.'''
        ...
    
    @property
    def is_rich_text(self) -> bool:
        ...
    
    @property
    def html_text(self) -> str:
        ...
    
    @html_text.setter
    def html_text(self, value : str):
        ...
    
    @property
    def text_vertical_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_vertical_overflow.setter
    def text_vertical_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def text_horizontal_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_horizontal_overflow.setter
    def text_horizontal_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
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
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def control_data(self) -> bytes:
        ...
    
    @property
    def active_x_control(self) -> aspose.cells.drawing.activexcontrols.ActiveXControl:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets the paths of a custom geometric shape.'''
        ...
    
    @property
    def geometry(self) -> aspose.cells.drawing.Geometry:
        '''Gets the geometry'''
        ...
    
    @property
    def create_id(self) -> Guid:
        ...
    
    @create_id.setter
    def create_id(self, value : Guid):
        ...
    
    @property
    def shadow(self) -> bool:
        '''Indicates whether the groupbox has shadow.'''
        ...
    
    @shadow.setter
    def shadow(self, value : bool):
        '''Indicates whether the groupbox has shadow.'''
        ...
    
    ...

class GroupFill(Fill):
    '''Represents this fill format should inherit the fill properties of the group.'''
    
    ...

class GroupShape(Shape):
    '''Represents the group shape which contains the individual shapes.'''
    
    @overload
    def to_image(self, stream : io.RawIOBase, image_type : aspose.cells.drawing.ImageType):
        '''Creates the shape image and saves it to a stream in the specified format.
        
        :param stream: The output stream.
        :param image_type: The type in which to save the image.'''
        ...
    
    @overload
    def to_image(self, image_file : str, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a file.'''
        ...
    
    @overload
    def to_image(self, stream : io.RawIOBase, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a stream.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.'''
        ...
    
    def get_result_of_smart_art(self) -> aspose.cells.drawing.GroupShape:
        '''Converting smart art to grouped shapes.'''
        ...
    
    def to_front_or_back(self, orders : int):
        '''Brings the shape to the front or sends the shape to back.
        
        :param orders: If it's less than zero, sets the shape to back.
        If it's greater than zero, brings the shape to front.'''
        ...
    
    def get_locked_property(self, type : aspose.cells.drawing.ShapeLockType) -> bool:
        '''Gets the value of locked property.
        
        :param type: The type of the shape locked property.
        :returns: Returns  the value of locked property.'''
        ...
    
    def set_locked_property(self, type : aspose.cells.drawing.ShapeLockType, value : bool):
        '''Set the locked property.
        
        :param type: The locked type.
        :param value: The value of the property.'''
        ...
    
    def add_hyperlink(self, address : str) -> aspose.cells.Hyperlink:
        '''Adds a hyperlink to the shape.
        
        :param address: Address of the hyperlink.
        :returns: Return the new hyperlink object.'''
        ...
    
    def remove_hyperlink(self):
        '''Remove the hyperlink of the shape.'''
        ...
    
    def move_to_range(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int):
        '''Moves the shape to a specified range.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index'''
        ...
    
    def align_top_right_corner(self, top_row : int, right_column : int):
        '''Moves the picture to the top-right corner.
        
        :param top_row: the row index.
        :param right_column: the column index.'''
        ...
    
    def get_connection_points(self) -> List[List[float]]:
        '''Get the connection points
        
        :returns: [X,Y] pairs of the connection point. Every item is a float[2] array, [0] represents x and [1] represents y.'''
        ...
    
    def get_linked_cell(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range linked to the control's value.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range linked to the control's value.'''
        ...
    
    def set_linked_cell(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range linked to the control's value.
        
        :param formula: The range linked to the control's value.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def get_input_range(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range used to fill the control.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range used to fill the control.'''
        ...
    
    def set_input_range(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range used to fill the control.
        
        :param formula: The range used to fill the control.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell.'''
        ...
    
    def calculate_text_size(self) -> List[int]:
        '''Recalculate the text area
        
        :returns: Text's Size in an array(width and height).'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the text .
        
        :returns: All Characters objects'''
        ...
    
    def remove_active_x_control(self):
        '''Remove activeX control.'''
        ...
    
    def is_same_setting(self, obj : any) -> bool:
        '''Returns whether the shape is same.'''
        ...
    
    def ungroup(self):
        '''Ungroups the shape items.'''
        ...
    
    def get_grouped_shapes(self) -> List[aspose.cells.drawing.Shape]:
        '''Gets the shapes grouped by this shape.'''
        ...
    
    @property
    def macro_name(self) -> str:
        ...
    
    @macro_name.setter
    def macro_name(self, value : str):
        ...
    
    @property
    def is_equation(self) -> bool:
        ...
    
    @property
    def is_smart_art(self) -> bool:
        ...
    
    @property
    def z_order_position(self) -> int:
        ...
    
    @z_order_position.setter
    def z_order_position(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of the shape.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of the shape.'''
        ...
    
    @property
    def alternative_text(self) -> str:
        ...
    
    @alternative_text.setter
    def alternative_text(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @property
    def line_format(self) -> aspose.cells.drawing.MsoLineFormat:
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.MsoFillFormat:
        ...
    
    @property
    def format(self) -> aspose.cells.drawing.ShapeFormat:
        '''Represents the setting of the shape's formatting.'''
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        '''Gets line style'''
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        '''Returns a :py:attr:`aspose.cells.drawing.Shape.fill_format` object that contains fill formatting properties for the specified shape.'''
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def reflection(self) -> aspose.cells.drawing.ReflectionEffect:
        '''Represents a :py:class:`aspose.cells.drawing.ReflectionEffect` object that specifies reflection effect for the chart element or shape.'''
        ...
    
    @property
    def glow(self) -> aspose.cells.drawing.GlowEffect:
        '''Represents a :py:class:`aspose.cells.drawing.GlowEffect` object that specifies glow effect for the chart element or shape.'''
        ...
    
    @property
    def soft_edges(self) -> float:
        ...
    
    @soft_edges.setter
    def soft_edges(self, value : float):
        ...
    
    @property
    def three_d_format(self) -> aspose.cells.drawing.ThreeDFormat:
        ...
    
    @property
    def text_frame(self) -> aspose.cells.drawing.MsoTextFrame:
        ...
    
    @property
    def format_picture(self) -> aspose.cells.drawing.MsoFormatPicture:
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_lock_aspect_ratio(self) -> bool:
        ...
    
    @is_lock_aspect_ratio.setter
    def is_lock_aspect_ratio(self, value : bool):
        ...
    
    @property
    def rotation_angle(self) -> float:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : float):
        ...
    
    @property
    def hyperlink(self) -> aspose.cells.Hyperlink:
        '''Gets the hyperlink of the shape.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier of this shape.'''
        ...
    
    @property
    def spid(self) -> str:
        '''Specifies an optional string that an application can use to Identify the particular shape.'''
        ...
    
    @property
    def spt(self) -> int:
        '''Specifies an optional number that an application can use to associate the particular shape with a defined shape type.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.drawing.Shape.worksheet` object which contains this shape.'''
        ...
    
    @property
    def is_group(self) -> bool:
        ...
    
    @property
    def is_in_group(self) -> bool:
        ...
    
    @property
    def is_word_art(self) -> bool:
        ...
    
    @property
    def text_effect(self) -> aspose.cells.drawing.TextEffectFormat:
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_printable(self) -> bool:
        ...
    
    @is_printable.setter
    def is_printable(self, value : bool):
        ...
    
    @property
    def mso_drawing_type(self) -> aspose.cells.drawing.MsoDrawingType:
        ...
    
    @property
    def auto_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @auto_shape_type.setter
    def auto_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def anchor_type(self) -> aspose.cells.drawing.ShapeAnchorType:
        ...
    
    @anchor_type.setter
    def anchor_type(self, value : aspose.cells.drawing.ShapeAnchorType):
        ...
    
    @property
    def placement(self) -> aspose.cells.drawing.PlacementType:
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @placement.setter
    def placement(self, value : aspose.cells.drawing.PlacementType):
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @property
    def upper_left_row(self) -> int:
        ...
    
    @upper_left_row.setter
    def upper_left_row(self, value : int):
        ...
    
    @property
    def upper_delta_y(self) -> int:
        ...
    
    @upper_delta_y.setter
    def upper_delta_y(self, value : int):
        ...
    
    @property
    def upper_left_column(self) -> int:
        ...
    
    @upper_left_column.setter
    def upper_left_column(self, value : int):
        ...
    
    @property
    def upper_delta_x(self) -> int:
        ...
    
    @upper_delta_x.setter
    def upper_delta_x(self, value : int):
        ...
    
    @property
    def lower_right_row(self) -> int:
        ...
    
    @lower_right_row.setter
    def lower_right_row(self, value : int):
        ...
    
    @property
    def lower_delta_y(self) -> int:
        ...
    
    @lower_delta_y.setter
    def lower_delta_y(self, value : int):
        ...
    
    @property
    def lower_right_column(self) -> int:
        ...
    
    @lower_right_column.setter
    def lower_right_column(self, value : int):
        ...
    
    @property
    def lower_delta_x(self) -> int:
        ...
    
    @lower_delta_x.setter
    def lower_delta_x(self, value : int):
        ...
    
    @property
    def right(self) -> int:
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def width_pt(self) -> float:
        ...
    
    @width_pt.setter
    def width_pt(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def height(self) -> int:
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    @property
    def height_pt(self) -> float:
        ...
    
    @height_pt.setter
    def height_pt(self, value : float):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def left(self) -> int:
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @property
    def left_inch(self) -> float:
        ...
    
    @left_inch.setter
    def left_inch(self, value : float):
        ...
    
    @property
    def left_cm(self) -> float:
        ...
    
    @left_cm.setter
    def left_cm(self, value : float):
        ...
    
    @property
    def top(self) -> int:
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @property
    def top_inch(self) -> float:
        ...
    
    @top_inch.setter
    def top_inch(self, value : float):
        ...
    
    @property
    def top_cm(self) -> float:
        ...
    
    @top_cm.setter
    def top_cm(self, value : float):
        ...
    
    @property
    def top_to_corner(self) -> int:
        ...
    
    @top_to_corner.setter
    def top_to_corner(self, value : int):
        ...
    
    @property
    def left_to_corner(self) -> int:
        ...
    
    @left_to_corner.setter
    def left_to_corner(self, value : int):
        ...
    
    @property
    def x(self) -> int:
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @property
    def width_scale(self) -> int:
        ...
    
    @width_scale.setter
    def width_scale(self, value : int):
        ...
    
    @property
    def height_scale(self) -> int:
        ...
    
    @height_scale.setter
    def height_scale(self, value : int):
        ...
    
    @property
    def top_in_shape(self) -> int:
        ...
    
    @top_in_shape.setter
    def top_in_shape(self, value : int):
        ...
    
    @property
    def left_in_shape(self) -> int:
        ...
    
    @left_in_shape.setter
    def left_in_shape(self, value : int):
        ...
    
    @property
    def width_in_shape(self) -> int:
        ...
    
    @width_in_shape.setter
    def width_in_shape(self, value : int):
        ...
    
    @property
    def height_in_shape(self) -> int:
        ...
    
    @height_in_shape.setter
    def height_in_shape(self, value : int):
        ...
    
    @property
    def group(self) -> aspose.cells.drawing.GroupShape:
        '''Gets the group shape which contains this shape.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.AutoShapeType:
        '''Gets the auto shape type.'''
        ...
    
    @property
    def has_line(self) -> bool:
        ...
    
    @has_line.setter
    def has_line(self, value : bool):
        ...
    
    @property
    def is_filled(self) -> bool:
        ...
    
    @is_filled.setter
    def is_filled(self, value : bool):
        ...
    
    @property
    def is_flipped_horizontally(self) -> bool:
        ...
    
    @is_flipped_horizontally.setter
    def is_flipped_horizontally(self, value : bool):
        ...
    
    @property
    def is_flipped_vertically(self) -> bool:
        ...
    
    @is_flipped_vertically.setter
    def is_flipped_vertically(self, value : bool):
        ...
    
    @property
    def actual_lower_right_row(self) -> int:
        ...
    
    @property
    def connection_points(self) -> aspose.pydrawing.PointF[]:
        ...
    
    @property
    def relative_to_original_picture_size(self) -> bool:
        ...
    
    @relative_to_original_picture_size.setter
    def relative_to_original_picture_size(self, value : bool):
        ...
    
    @property
    def linked_cell(self) -> str:
        ...
    
    @linked_cell.setter
    def linked_cell(self, value : str):
        ...
    
    @property
    def input_range(self) -> str:
        ...
    
    @input_range.setter
    def input_range(self, value : str):
        ...
    
    @property
    def text_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @text_shape_type.setter
    def text_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def text_body(self) -> aspose.cells.drawing.texts.FontSettingCollection:
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Represents the font of shape.'''
        ...
    
    @font.setter
    def font(self, value : aspose.cells.Font):
        '''Represents the font of shape.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    @text_options.setter
    def text_options(self, value : aspose.cells.drawing.texts.TextOptions):
        ...
    
    @property
    def text(self) -> str:
        '''Represents the string in this TextBox object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Represents the string in this TextBox object.'''
        ...
    
    @property
    def is_rich_text(self) -> bool:
        ...
    
    @property
    def html_text(self) -> str:
        ...
    
    @html_text.setter
    def html_text(self, value : str):
        ...
    
    @property
    def text_vertical_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_vertical_overflow.setter
    def text_vertical_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def text_horizontal_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_horizontal_overflow.setter
    def text_horizontal_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
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
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def control_data(self) -> bytes:
        ...
    
    @property
    def active_x_control(self) -> aspose.cells.drawing.activexcontrols.ActiveXControl:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets the paths of a custom geometric shape.'''
        ...
    
    @property
    def geometry(self) -> aspose.cells.drawing.Geometry:
        '''Gets the geometry'''
        ...
    
    @property
    def create_id(self) -> Guid:
        ...
    
    @create_id.setter
    def create_id(self, value : Guid):
        ...
    
    def __getitem__(self, key : int) -> aspose.cells.drawing.Shape:
        '''Gets the child shape by index.'''
        ...
    
    ...

class Label(Shape):
    '''Encapsulates the object that represents a label in a spreadsheet.'''
    
    @overload
    def to_image(self, stream : io.RawIOBase, image_type : aspose.cells.drawing.ImageType):
        '''Creates the shape image and saves it to a stream in the specified format.
        
        :param stream: The output stream.
        :param image_type: The type in which to save the image.'''
        ...
    
    @overload
    def to_image(self, image_file : str, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a file.'''
        ...
    
    @overload
    def to_image(self, stream : io.RawIOBase, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a stream.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.'''
        ...
    
    def get_result_of_smart_art(self) -> aspose.cells.drawing.GroupShape:
        '''Converting smart art to grouped shapes.'''
        ...
    
    def to_front_or_back(self, orders : int):
        '''Brings the shape to the front or sends the shape to back.
        
        :param orders: If it's less than zero, sets the shape to back.
        If it's greater than zero, brings the shape to front.'''
        ...
    
    def get_locked_property(self, type : aspose.cells.drawing.ShapeLockType) -> bool:
        '''Gets the value of locked property.
        
        :param type: The type of the shape locked property.
        :returns: Returns  the value of locked property.'''
        ...
    
    def set_locked_property(self, type : aspose.cells.drawing.ShapeLockType, value : bool):
        '''Set the locked property.
        
        :param type: The locked type.
        :param value: The value of the property.'''
        ...
    
    def add_hyperlink(self, address : str) -> aspose.cells.Hyperlink:
        '''Adds a hyperlink to the shape.
        
        :param address: Address of the hyperlink.
        :returns: Return the new hyperlink object.'''
        ...
    
    def remove_hyperlink(self):
        '''Remove the hyperlink of the shape.'''
        ...
    
    def move_to_range(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int):
        '''Moves the shape to a specified range.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index'''
        ...
    
    def align_top_right_corner(self, top_row : int, right_column : int):
        '''Moves the picture to the top-right corner.
        
        :param top_row: the row index.
        :param right_column: the column index.'''
        ...
    
    def get_connection_points(self) -> List[List[float]]:
        '''Get the connection points
        
        :returns: [X,Y] pairs of the connection point. Every item is a float[2] array, [0] represents x and [1] represents y.'''
        ...
    
    def get_linked_cell(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range linked to the control's value.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range linked to the control's value.'''
        ...
    
    def set_linked_cell(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range linked to the control's value.
        
        :param formula: The range linked to the control's value.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def get_input_range(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range used to fill the control.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range used to fill the control.'''
        ...
    
    def set_input_range(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range used to fill the control.
        
        :param formula: The range used to fill the control.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell.'''
        ...
    
    def calculate_text_size(self) -> List[int]:
        '''Recalculate the text area
        
        :returns: Text's Size in an array(width and height).'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the text .
        
        :returns: All Characters objects'''
        ...
    
    def remove_active_x_control(self):
        '''Remove activeX control.'''
        ...
    
    def is_same_setting(self, obj : any) -> bool:
        '''Returns whether the shape is same.'''
        ...
    
    @property
    def macro_name(self) -> str:
        ...
    
    @macro_name.setter
    def macro_name(self, value : str):
        ...
    
    @property
    def is_equation(self) -> bool:
        ...
    
    @property
    def is_smart_art(self) -> bool:
        ...
    
    @property
    def z_order_position(self) -> int:
        ...
    
    @z_order_position.setter
    def z_order_position(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of the shape.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of the shape.'''
        ...
    
    @property
    def alternative_text(self) -> str:
        ...
    
    @alternative_text.setter
    def alternative_text(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @property
    def line_format(self) -> aspose.cells.drawing.MsoLineFormat:
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.MsoFillFormat:
        ...
    
    @property
    def format(self) -> aspose.cells.drawing.ShapeFormat:
        '''Represents the setting of the shape's formatting.'''
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        '''Gets line style'''
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        '''Returns a :py:attr:`aspose.cells.drawing.Shape.fill_format` object that contains fill formatting properties for the specified shape.'''
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def reflection(self) -> aspose.cells.drawing.ReflectionEffect:
        '''Represents a :py:class:`aspose.cells.drawing.ReflectionEffect` object that specifies reflection effect for the chart element or shape.'''
        ...
    
    @property
    def glow(self) -> aspose.cells.drawing.GlowEffect:
        '''Represents a :py:class:`aspose.cells.drawing.GlowEffect` object that specifies glow effect for the chart element or shape.'''
        ...
    
    @property
    def soft_edges(self) -> float:
        ...
    
    @soft_edges.setter
    def soft_edges(self, value : float):
        ...
    
    @property
    def three_d_format(self) -> aspose.cells.drawing.ThreeDFormat:
        ...
    
    @property
    def text_frame(self) -> aspose.cells.drawing.MsoTextFrame:
        ...
    
    @property
    def format_picture(self) -> aspose.cells.drawing.MsoFormatPicture:
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_lock_aspect_ratio(self) -> bool:
        ...
    
    @is_lock_aspect_ratio.setter
    def is_lock_aspect_ratio(self, value : bool):
        ...
    
    @property
    def rotation_angle(self) -> float:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : float):
        ...
    
    @property
    def hyperlink(self) -> aspose.cells.Hyperlink:
        '''Gets the hyperlink of the shape.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier of this shape.'''
        ...
    
    @property
    def spid(self) -> str:
        '''Specifies an optional string that an application can use to Identify the particular shape.'''
        ...
    
    @property
    def spt(self) -> int:
        '''Specifies an optional number that an application can use to associate the particular shape with a defined shape type.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.drawing.Shape.worksheet` object which contains this shape.'''
        ...
    
    @property
    def is_group(self) -> bool:
        ...
    
    @property
    def is_in_group(self) -> bool:
        ...
    
    @property
    def is_word_art(self) -> bool:
        ...
    
    @property
    def text_effect(self) -> aspose.cells.drawing.TextEffectFormat:
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_printable(self) -> bool:
        ...
    
    @is_printable.setter
    def is_printable(self, value : bool):
        ...
    
    @property
    def mso_drawing_type(self) -> aspose.cells.drawing.MsoDrawingType:
        ...
    
    @property
    def auto_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @auto_shape_type.setter
    def auto_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def anchor_type(self) -> aspose.cells.drawing.ShapeAnchorType:
        ...
    
    @anchor_type.setter
    def anchor_type(self, value : aspose.cells.drawing.ShapeAnchorType):
        ...
    
    @property
    def placement(self) -> aspose.cells.drawing.PlacementType:
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @placement.setter
    def placement(self, value : aspose.cells.drawing.PlacementType):
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @property
    def upper_left_row(self) -> int:
        ...
    
    @upper_left_row.setter
    def upper_left_row(self, value : int):
        ...
    
    @property
    def upper_delta_y(self) -> int:
        ...
    
    @upper_delta_y.setter
    def upper_delta_y(self, value : int):
        ...
    
    @property
    def upper_left_column(self) -> int:
        ...
    
    @upper_left_column.setter
    def upper_left_column(self, value : int):
        ...
    
    @property
    def upper_delta_x(self) -> int:
        ...
    
    @upper_delta_x.setter
    def upper_delta_x(self, value : int):
        ...
    
    @property
    def lower_right_row(self) -> int:
        ...
    
    @lower_right_row.setter
    def lower_right_row(self, value : int):
        ...
    
    @property
    def lower_delta_y(self) -> int:
        ...
    
    @lower_delta_y.setter
    def lower_delta_y(self, value : int):
        ...
    
    @property
    def lower_right_column(self) -> int:
        ...
    
    @lower_right_column.setter
    def lower_right_column(self, value : int):
        ...
    
    @property
    def lower_delta_x(self) -> int:
        ...
    
    @lower_delta_x.setter
    def lower_delta_x(self, value : int):
        ...
    
    @property
    def right(self) -> int:
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def width_pt(self) -> float:
        ...
    
    @width_pt.setter
    def width_pt(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def height(self) -> int:
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    @property
    def height_pt(self) -> float:
        ...
    
    @height_pt.setter
    def height_pt(self, value : float):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def left(self) -> int:
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @property
    def left_inch(self) -> float:
        ...
    
    @left_inch.setter
    def left_inch(self, value : float):
        ...
    
    @property
    def left_cm(self) -> float:
        ...
    
    @left_cm.setter
    def left_cm(self, value : float):
        ...
    
    @property
    def top(self) -> int:
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @property
    def top_inch(self) -> float:
        ...
    
    @top_inch.setter
    def top_inch(self, value : float):
        ...
    
    @property
    def top_cm(self) -> float:
        ...
    
    @top_cm.setter
    def top_cm(self, value : float):
        ...
    
    @property
    def top_to_corner(self) -> int:
        ...
    
    @top_to_corner.setter
    def top_to_corner(self, value : int):
        ...
    
    @property
    def left_to_corner(self) -> int:
        ...
    
    @left_to_corner.setter
    def left_to_corner(self, value : int):
        ...
    
    @property
    def x(self) -> int:
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @property
    def width_scale(self) -> int:
        ...
    
    @width_scale.setter
    def width_scale(self, value : int):
        ...
    
    @property
    def height_scale(self) -> int:
        ...
    
    @height_scale.setter
    def height_scale(self, value : int):
        ...
    
    @property
    def top_in_shape(self) -> int:
        ...
    
    @top_in_shape.setter
    def top_in_shape(self, value : int):
        ...
    
    @property
    def left_in_shape(self) -> int:
        ...
    
    @left_in_shape.setter
    def left_in_shape(self, value : int):
        ...
    
    @property
    def width_in_shape(self) -> int:
        ...
    
    @width_in_shape.setter
    def width_in_shape(self, value : int):
        ...
    
    @property
    def height_in_shape(self) -> int:
        ...
    
    @height_in_shape.setter
    def height_in_shape(self, value : int):
        ...
    
    @property
    def group(self) -> aspose.cells.drawing.GroupShape:
        '''Gets the group shape which contains this shape.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.AutoShapeType:
        '''Gets the auto shape type.'''
        ...
    
    @property
    def has_line(self) -> bool:
        ...
    
    @has_line.setter
    def has_line(self, value : bool):
        ...
    
    @property
    def is_filled(self) -> bool:
        ...
    
    @is_filled.setter
    def is_filled(self, value : bool):
        ...
    
    @property
    def is_flipped_horizontally(self) -> bool:
        ...
    
    @is_flipped_horizontally.setter
    def is_flipped_horizontally(self, value : bool):
        ...
    
    @property
    def is_flipped_vertically(self) -> bool:
        ...
    
    @is_flipped_vertically.setter
    def is_flipped_vertically(self, value : bool):
        ...
    
    @property
    def actual_lower_right_row(self) -> int:
        ...
    
    @property
    def connection_points(self) -> aspose.pydrawing.PointF[]:
        ...
    
    @property
    def relative_to_original_picture_size(self) -> bool:
        ...
    
    @relative_to_original_picture_size.setter
    def relative_to_original_picture_size(self, value : bool):
        ...
    
    @property
    def linked_cell(self) -> str:
        ...
    
    @linked_cell.setter
    def linked_cell(self, value : str):
        ...
    
    @property
    def input_range(self) -> str:
        ...
    
    @input_range.setter
    def input_range(self, value : str):
        ...
    
    @property
    def text_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @text_shape_type.setter
    def text_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def text_body(self) -> aspose.cells.drawing.texts.FontSettingCollection:
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Represents the font of shape.'''
        ...
    
    @font.setter
    def font(self, value : aspose.cells.Font):
        '''Represents the font of shape.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    @text_options.setter
    def text_options(self, value : aspose.cells.drawing.texts.TextOptions):
        ...
    
    @property
    def text(self) -> str:
        '''Represents the string in this TextBox object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Represents the string in this TextBox object.'''
        ...
    
    @property
    def is_rich_text(self) -> bool:
        ...
    
    @property
    def html_text(self) -> str:
        ...
    
    @html_text.setter
    def html_text(self, value : str):
        ...
    
    @property
    def text_vertical_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_vertical_overflow.setter
    def text_vertical_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def text_horizontal_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_horizontal_overflow.setter
    def text_horizontal_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
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
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def control_data(self) -> bytes:
        ...
    
    @property
    def active_x_control(self) -> aspose.cells.drawing.activexcontrols.ActiveXControl:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets the paths of a custom geometric shape.'''
        ...
    
    @property
    def geometry(self) -> aspose.cells.drawing.Geometry:
        '''Gets the geometry'''
        ...
    
    @property
    def create_id(self) -> Guid:
        ...
    
    @create_id.setter
    def create_id(self, value : Guid):
        ...
    
    ...

class Line:
    '''Encapsulates the object that represents the line format.'''
    
    @property
    def compound_type(self) -> aspose.cells.drawing.MsoLineStyle:
        ...
    
    @compound_type.setter
    def compound_type(self, value : aspose.cells.drawing.MsoLineStyle):
        ...
    
    @property
    def dash_type(self) -> aspose.cells.drawing.MsoLineDashStyle:
        ...
    
    @dash_type.setter
    def dash_type(self, value : aspose.cells.drawing.MsoLineDashStyle):
        ...
    
    @property
    def cap_type(self) -> aspose.cells.drawing.LineCapType:
        ...
    
    @cap_type.setter
    def cap_type(self, value : aspose.cells.drawing.LineCapType):
        ...
    
    @property
    def join_type(self) -> aspose.cells.drawing.LineJoinType:
        ...
    
    @join_type.setter
    def join_type(self, value : aspose.cells.drawing.LineJoinType):
        ...
    
    @property
    def begin_type(self) -> aspose.cells.drawing.MsoArrowheadStyle:
        ...
    
    @begin_type.setter
    def begin_type(self, value : aspose.cells.drawing.MsoArrowheadStyle):
        ...
    
    @property
    def end_type(self) -> aspose.cells.drawing.MsoArrowheadStyle:
        ...
    
    @end_type.setter
    def end_type(self, value : aspose.cells.drawing.MsoArrowheadStyle):
        ...
    
    @property
    def begin_arrow_length(self) -> aspose.cells.drawing.MsoArrowheadLength:
        ...
    
    @begin_arrow_length.setter
    def begin_arrow_length(self, value : aspose.cells.drawing.MsoArrowheadLength):
        ...
    
    @property
    def end_arrow_length(self) -> aspose.cells.drawing.MsoArrowheadLength:
        ...
    
    @end_arrow_length.setter
    def end_arrow_length(self, value : aspose.cells.drawing.MsoArrowheadLength):
        ...
    
    @property
    def begin_arrow_width(self) -> aspose.cells.drawing.MsoArrowheadWidth:
        ...
    
    @begin_arrow_width.setter
    def begin_arrow_width(self, value : aspose.cells.drawing.MsoArrowheadWidth):
        ...
    
    @property
    def end_arrow_width(self) -> aspose.cells.drawing.MsoArrowheadWidth:
        ...
    
    @end_arrow_width.setter
    def end_arrow_width(self, value : aspose.cells.drawing.MsoArrowheadWidth):
        ...
    
    @property
    def theme_color(self) -> aspose.cells.ThemeColor:
        ...
    
    @theme_color.setter
    def theme_color(self, value : aspose.cells.ThemeColor):
        ...
    
    @property
    def color(self) -> aspose.pydrawing.Color:
        '''Represents the :py:class:`aspose.pydrawing.Color` of the line.'''
        ...
    
    @color.setter
    def color(self, value : aspose.pydrawing.Color):
        '''Represents the :py:class:`aspose.pydrawing.Color` of the line.'''
        ...
    
    @property
    def transparency(self) -> float:
        '''Returns the degree of transparency of the line as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    @transparency.setter
    def transparency(self, value : float):
        '''Returns or sets the degree of transparency of the line as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    @property
    def style(self) -> aspose.cells.drawing.LineType:
        '''Represents the style of the line.'''
        ...
    
    @style.setter
    def style(self, value : aspose.cells.drawing.LineType):
        '''Represents the style of the line.'''
        ...
    
    @property
    def weight(self) -> aspose.cells.drawing.WeightType:
        '''Gets the :py:class:`aspose.cells.drawing.WeightType` of the line.'''
        ...
    
    @weight.setter
    def weight(self, value : aspose.cells.drawing.WeightType):
        '''Sets the :py:class:`aspose.cells.drawing.WeightType` of the line.'''
        ...
    
    @property
    def weight_pt(self) -> float:
        ...
    
    @weight_pt.setter
    def weight_pt(self, value : float):
        ...
    
    @property
    def weight_px(self) -> float:
        ...
    
    @weight_px.setter
    def weight_px(self, value : float):
        ...
    
    @property
    def formatting_type(self) -> aspose.cells.charts.ChartLineFormattingType:
        ...
    
    @formatting_type.setter
    def formatting_type(self, value : aspose.cells.charts.ChartLineFormattingType):
        ...
    
    @property
    def is_automatic_color(self) -> bool:
        ...
    
    @property
    def is_visible(self) -> bool:
        ...
    
    @is_visible.setter
    def is_visible(self, value : bool):
        ...
    
    @property
    def is_auto(self) -> bool:
        ...
    
    @is_auto.setter
    def is_auto(self, value : bool):
        ...
    
    @property
    def gradient_fill(self) -> aspose.cells.drawing.GradientFill:
        ...
    
    ...

class LineFormat(FillFormat):
    '''Represents all setting of the line.'''
    
    @overload
    def set_two_color_gradient(self, color1 : aspose.pydrawing.Color, color2 : aspose.pydrawing.Color, style : aspose.cells.drawing.GradientStyleType, variant : int):
        '''Sets the specified fill to a two-color gradient.
        Only applies for Excel 2007.
        
        :param color1: One gradient color.
        :param color2: Two gradient color.
        :param style: Gradient shading style.
        :param variant: The gradient variant. Can be a value from 1 through 4, corresponding to one of the four variants on the Gradient tab in the Fill Effects dialog box. If style is GradientStyle.FromCenter, the Variant argument can only be 1 or 2.'''
        ...
    
    @overload
    def set_two_color_gradient(self, color1 : aspose.pydrawing.Color, transparency1 : float, color2 : aspose.pydrawing.Color, transparency2 : float, style : aspose.cells.drawing.GradientStyleType, variant : int):
        '''Sets the specified fill to a two-color gradient.
        Only applies for Excel 2007.
        
        :param color1: One gradient color.
        :param transparency1: The degree of transparency of the color1 as a value from 0.0 (opaque) through 1.0 (clear).
        :param color2: Two gradient color.
        :param transparency2: The degree of transparency of the color2 as a value from 0.0 (opaque) through 1.0 (clear).
        :param style: Gradient shading style.
        :param variant: The gradient variant. Can be a value from 1 through 4, corresponding to one of the four variants on the Gradient tab in the Fill Effects dialog box. If style is GradientStyle.FromCenter, the Variant argument can only be 1 or 2.'''
        ...
    
    def set_one_color_gradient(self, color : aspose.pydrawing.Color, degree : float, style : aspose.cells.drawing.GradientStyleType, variant : int):
        '''Sets the specified fill to a one-color gradient.
        Only applies for Excel 2007.
        
        :param color: One gradient color.
        :param degree: The gradient degree. Can be a value from 0.0 (dark) through 1.0 (light).
        :param style: Gradient shading style.
        :param variant: The gradient variant. Can be a value from 1 through 4, corresponding to one of the four variants on the Gradient tab in the Fill Effects dialog box. If style is GradientStyle.FromCenter, the Variant argument can only be 1 or 2.'''
        ...
    
    def set_preset_color_gradient(self, preset_color : aspose.cells.drawing.GradientPresetType, style : aspose.cells.drawing.GradientStyleType, variant : int):
        '''Sets the specified fill to a preset-color gradient.
        Only applies for Excel 2007.
        
        :param preset_color: Preset color type
        :param style: Gradient shading style.
        :param variant: The gradient variant. Can be a value from 1 through 4, corresponding to one of the four variants on the Gradient tab in the Fill Effects dialog box. If style is GradientStyle.FromCenter, the Variant argument can only be 1 or 2.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.FillType:
        '''Gets and sets the fill type.'''
        ...
    
    @type.setter
    def type(self, value : aspose.cells.drawing.FillType):
        '''Gets and sets the fill type.'''
        ...
    
    @property
    def fill_type(self) -> aspose.cells.drawing.FillType:
        ...
    
    @fill_type.setter
    def fill_type(self, value : aspose.cells.drawing.FillType):
        ...
    
    @property
    def transparency(self) -> float:
        '''Returns the degree of transparency of the area as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    @transparency.setter
    def transparency(self, value : float):
        '''Returns or sets the degree of transparency of the area as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    @property
    def set_type(self) -> aspose.cells.drawing.FormatSetType:
        ...
    
    @set_type.setter
    def set_type(self, value : aspose.cells.drawing.FormatSetType):
        ...
    
    @property
    def gradient_fill(self) -> aspose.cells.drawing.GradientFill:
        ...
    
    @property
    def texture_fill(self) -> aspose.cells.drawing.TextureFill:
        ...
    
    @property
    def solid_fill(self) -> aspose.cells.drawing.SolidFill:
        ...
    
    @property
    def pattern_fill(self) -> aspose.cells.drawing.PatternFill:
        ...
    
    @property
    def gradient_color_type(self) -> aspose.cells.drawing.GradientColorType:
        ...
    
    @property
    def gradient_style(self) -> aspose.cells.drawing.GradientStyleType:
        ...
    
    @property
    def gradient_color1(self) -> aspose.pydrawing.Color:
        ...
    
    @property
    def gradient_color2(self) -> aspose.pydrawing.Color:
        ...
    
    @property
    def gradient_degree(self) -> float:
        ...
    
    @property
    def gradient_variant(self) -> int:
        ...
    
    @property
    def preset_color(self) -> aspose.cells.drawing.GradientPresetType:
        ...
    
    @property
    def texture(self) -> aspose.cells.drawing.TextureType:
        '''Represents the texture type for the specified fill.'''
        ...
    
    @texture.setter
    def texture(self, value : aspose.cells.drawing.TextureType):
        '''Represents the texture type for the specified fill.'''
        ...
    
    @property
    def pattern(self) -> aspose.cells.drawing.FillPattern:
        '''Represents an area's display pattern.'''
        ...
    
    @pattern.setter
    def pattern(self, value : aspose.cells.drawing.FillPattern):
        '''Represents an area's display pattern.'''
        ...
    
    @property
    def picture_format_type(self) -> aspose.cells.drawing.FillPictureType:
        ...
    
    @picture_format_type.setter
    def picture_format_type(self, value : aspose.cells.drawing.FillPictureType):
        ...
    
    @property
    def scale(self) -> float:
        '''Gets and sets the picture format scale.'''
        ...
    
    @scale.setter
    def scale(self, value : float):
        '''Gets and sets the picture format scale.'''
        ...
    
    @property
    def image_data(self) -> bytes:
        ...
    
    @image_data.setter
    def image_data(self, value : bytes):
        ...
    
    @property
    def compound_type(self) -> aspose.cells.drawing.MsoLineStyle:
        ...
    
    @compound_type.setter
    def compound_type(self, value : aspose.cells.drawing.MsoLineStyle):
        ...
    
    @property
    def dash_style(self) -> aspose.cells.drawing.MsoLineDashStyle:
        ...
    
    @dash_style.setter
    def dash_style(self, value : aspose.cells.drawing.MsoLineDashStyle):
        ...
    
    @property
    def cap_type(self) -> aspose.cells.drawing.LineCapType:
        ...
    
    @cap_type.setter
    def cap_type(self, value : aspose.cells.drawing.LineCapType):
        ...
    
    @property
    def join_type(self) -> aspose.cells.drawing.LineJoinType:
        ...
    
    @join_type.setter
    def join_type(self, value : aspose.cells.drawing.LineJoinType):
        ...
    
    @property
    def begin_arrowhead_style(self) -> aspose.cells.drawing.MsoArrowheadStyle:
        ...
    
    @begin_arrowhead_style.setter
    def begin_arrowhead_style(self, value : aspose.cells.drawing.MsoArrowheadStyle):
        ...
    
    @property
    def begin_arrowhead_width(self) -> aspose.cells.drawing.MsoArrowheadWidth:
        ...
    
    @begin_arrowhead_width.setter
    def begin_arrowhead_width(self, value : aspose.cells.drawing.MsoArrowheadWidth):
        ...
    
    @property
    def begin_arrowhead_length(self) -> aspose.cells.drawing.MsoArrowheadLength:
        ...
    
    @begin_arrowhead_length.setter
    def begin_arrowhead_length(self, value : aspose.cells.drawing.MsoArrowheadLength):
        ...
    
    @property
    def end_arrowhead_style(self) -> aspose.cells.drawing.MsoArrowheadStyle:
        ...
    
    @end_arrowhead_style.setter
    def end_arrowhead_style(self, value : aspose.cells.drawing.MsoArrowheadStyle):
        ...
    
    @property
    def end_arrowhead_width(self) -> aspose.cells.drawing.MsoArrowheadWidth:
        ...
    
    @end_arrowhead_width.setter
    def end_arrowhead_width(self, value : aspose.cells.drawing.MsoArrowheadWidth):
        ...
    
    @property
    def end_arrowhead_length(self) -> aspose.cells.drawing.MsoArrowheadLength:
        ...
    
    @end_arrowhead_length.setter
    def end_arrowhead_length(self, value : aspose.cells.drawing.MsoArrowheadLength):
        ...
    
    @property
    def weight(self) -> float:
        '''Gets the weight of the line in unit of points.'''
        ...
    
    @weight.setter
    def weight(self, value : float):
        '''Sets the weight of the line in unit of points.'''
        ...
    
    ...

class LineShape(Shape):
    '''Represents the line shape.'''
    
    @overload
    def to_image(self, stream : io.RawIOBase, image_type : aspose.cells.drawing.ImageType):
        '''Creates the shape image and saves it to a stream in the specified format.
        
        :param stream: The output stream.
        :param image_type: The type in which to save the image.'''
        ...
    
    @overload
    def to_image(self, image_file : str, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a file.'''
        ...
    
    @overload
    def to_image(self, stream : io.RawIOBase, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a stream.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.'''
        ...
    
    def get_result_of_smart_art(self) -> aspose.cells.drawing.GroupShape:
        '''Converting smart art to grouped shapes.'''
        ...
    
    def to_front_or_back(self, orders : int):
        '''Brings the shape to the front or sends the shape to back.
        
        :param orders: If it's less than zero, sets the shape to back.
        If it's greater than zero, brings the shape to front.'''
        ...
    
    def get_locked_property(self, type : aspose.cells.drawing.ShapeLockType) -> bool:
        '''Gets the value of locked property.
        
        :param type: The type of the shape locked property.
        :returns: Returns  the value of locked property.'''
        ...
    
    def set_locked_property(self, type : aspose.cells.drawing.ShapeLockType, value : bool):
        '''Set the locked property.
        
        :param type: The locked type.
        :param value: The value of the property.'''
        ...
    
    def add_hyperlink(self, address : str) -> aspose.cells.Hyperlink:
        '''Adds a hyperlink to the shape.
        
        :param address: Address of the hyperlink.
        :returns: Return the new hyperlink object.'''
        ...
    
    def remove_hyperlink(self):
        '''Remove the hyperlink of the shape.'''
        ...
    
    def move_to_range(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int):
        '''Moves the shape to a specified range.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index'''
        ...
    
    def align_top_right_corner(self, top_row : int, right_column : int):
        '''Moves the picture to the top-right corner.
        
        :param top_row: the row index.
        :param right_column: the column index.'''
        ...
    
    def get_connection_points(self) -> List[List[float]]:
        '''Get the connection points
        
        :returns: [X,Y] pairs of the connection point. Every item is a float[2] array, [0] represents x and [1] represents y.'''
        ...
    
    def get_linked_cell(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range linked to the control's value.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range linked to the control's value.'''
        ...
    
    def set_linked_cell(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range linked to the control's value.
        
        :param formula: The range linked to the control's value.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def get_input_range(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range used to fill the control.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range used to fill the control.'''
        ...
    
    def set_input_range(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range used to fill the control.
        
        :param formula: The range used to fill the control.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell.'''
        ...
    
    def calculate_text_size(self) -> List[int]:
        '''Recalculate the text area
        
        :returns: Text's Size in an array(width and height).'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the text .
        
        :returns: All Characters objects'''
        ...
    
    def remove_active_x_control(self):
        '''Remove activeX control.'''
        ...
    
    def is_same_setting(self, obj : any) -> bool:
        '''Returns whether the shape is same.'''
        ...
    
    @property
    def macro_name(self) -> str:
        ...
    
    @macro_name.setter
    def macro_name(self, value : str):
        ...
    
    @property
    def is_equation(self) -> bool:
        ...
    
    @property
    def is_smart_art(self) -> bool:
        ...
    
    @property
    def z_order_position(self) -> int:
        ...
    
    @z_order_position.setter
    def z_order_position(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of the shape.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of the shape.'''
        ...
    
    @property
    def alternative_text(self) -> str:
        ...
    
    @alternative_text.setter
    def alternative_text(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @property
    def line_format(self) -> aspose.cells.drawing.MsoLineFormat:
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.MsoFillFormat:
        ...
    
    @property
    def format(self) -> aspose.cells.drawing.ShapeFormat:
        '''Represents the setting of the shape's formatting.'''
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        '''Gets line style'''
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        '''Returns a :py:attr:`aspose.cells.drawing.Shape.fill_format` object that contains fill formatting properties for the specified shape.'''
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def reflection(self) -> aspose.cells.drawing.ReflectionEffect:
        '''Represents a :py:class:`aspose.cells.drawing.ReflectionEffect` object that specifies reflection effect for the chart element or shape.'''
        ...
    
    @property
    def glow(self) -> aspose.cells.drawing.GlowEffect:
        '''Represents a :py:class:`aspose.cells.drawing.GlowEffect` object that specifies glow effect for the chart element or shape.'''
        ...
    
    @property
    def soft_edges(self) -> float:
        ...
    
    @soft_edges.setter
    def soft_edges(self, value : float):
        ...
    
    @property
    def three_d_format(self) -> aspose.cells.drawing.ThreeDFormat:
        ...
    
    @property
    def text_frame(self) -> aspose.cells.drawing.MsoTextFrame:
        ...
    
    @property
    def format_picture(self) -> aspose.cells.drawing.MsoFormatPicture:
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_lock_aspect_ratio(self) -> bool:
        ...
    
    @is_lock_aspect_ratio.setter
    def is_lock_aspect_ratio(self, value : bool):
        ...
    
    @property
    def rotation_angle(self) -> float:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : float):
        ...
    
    @property
    def hyperlink(self) -> aspose.cells.Hyperlink:
        '''Gets the hyperlink of the shape.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier of this shape.'''
        ...
    
    @property
    def spid(self) -> str:
        '''Specifies an optional string that an application can use to Identify the particular shape.'''
        ...
    
    @property
    def spt(self) -> int:
        '''Specifies an optional number that an application can use to associate the particular shape with a defined shape type.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.drawing.Shape.worksheet` object which contains this shape.'''
        ...
    
    @property
    def is_group(self) -> bool:
        ...
    
    @property
    def is_in_group(self) -> bool:
        ...
    
    @property
    def is_word_art(self) -> bool:
        ...
    
    @property
    def text_effect(self) -> aspose.cells.drawing.TextEffectFormat:
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_printable(self) -> bool:
        ...
    
    @is_printable.setter
    def is_printable(self, value : bool):
        ...
    
    @property
    def mso_drawing_type(self) -> aspose.cells.drawing.MsoDrawingType:
        ...
    
    @property
    def auto_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @auto_shape_type.setter
    def auto_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def anchor_type(self) -> aspose.cells.drawing.ShapeAnchorType:
        ...
    
    @anchor_type.setter
    def anchor_type(self, value : aspose.cells.drawing.ShapeAnchorType):
        ...
    
    @property
    def placement(self) -> aspose.cells.drawing.PlacementType:
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @placement.setter
    def placement(self, value : aspose.cells.drawing.PlacementType):
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @property
    def upper_left_row(self) -> int:
        ...
    
    @upper_left_row.setter
    def upper_left_row(self, value : int):
        ...
    
    @property
    def upper_delta_y(self) -> int:
        ...
    
    @upper_delta_y.setter
    def upper_delta_y(self, value : int):
        ...
    
    @property
    def upper_left_column(self) -> int:
        ...
    
    @upper_left_column.setter
    def upper_left_column(self, value : int):
        ...
    
    @property
    def upper_delta_x(self) -> int:
        ...
    
    @upper_delta_x.setter
    def upper_delta_x(self, value : int):
        ...
    
    @property
    def lower_right_row(self) -> int:
        ...
    
    @lower_right_row.setter
    def lower_right_row(self, value : int):
        ...
    
    @property
    def lower_delta_y(self) -> int:
        ...
    
    @lower_delta_y.setter
    def lower_delta_y(self, value : int):
        ...
    
    @property
    def lower_right_column(self) -> int:
        ...
    
    @lower_right_column.setter
    def lower_right_column(self, value : int):
        ...
    
    @property
    def lower_delta_x(self) -> int:
        ...
    
    @lower_delta_x.setter
    def lower_delta_x(self, value : int):
        ...
    
    @property
    def right(self) -> int:
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def width_pt(self) -> float:
        ...
    
    @width_pt.setter
    def width_pt(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def height(self) -> int:
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    @property
    def height_pt(self) -> float:
        ...
    
    @height_pt.setter
    def height_pt(self, value : float):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def left(self) -> int:
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @property
    def left_inch(self) -> float:
        ...
    
    @left_inch.setter
    def left_inch(self, value : float):
        ...
    
    @property
    def left_cm(self) -> float:
        ...
    
    @left_cm.setter
    def left_cm(self, value : float):
        ...
    
    @property
    def top(self) -> int:
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @property
    def top_inch(self) -> float:
        ...
    
    @top_inch.setter
    def top_inch(self, value : float):
        ...
    
    @property
    def top_cm(self) -> float:
        ...
    
    @top_cm.setter
    def top_cm(self, value : float):
        ...
    
    @property
    def top_to_corner(self) -> int:
        ...
    
    @top_to_corner.setter
    def top_to_corner(self, value : int):
        ...
    
    @property
    def left_to_corner(self) -> int:
        ...
    
    @left_to_corner.setter
    def left_to_corner(self, value : int):
        ...
    
    @property
    def x(self) -> int:
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @property
    def width_scale(self) -> int:
        ...
    
    @width_scale.setter
    def width_scale(self, value : int):
        ...
    
    @property
    def height_scale(self) -> int:
        ...
    
    @height_scale.setter
    def height_scale(self, value : int):
        ...
    
    @property
    def top_in_shape(self) -> int:
        ...
    
    @top_in_shape.setter
    def top_in_shape(self, value : int):
        ...
    
    @property
    def left_in_shape(self) -> int:
        ...
    
    @left_in_shape.setter
    def left_in_shape(self, value : int):
        ...
    
    @property
    def width_in_shape(self) -> int:
        ...
    
    @width_in_shape.setter
    def width_in_shape(self, value : int):
        ...
    
    @property
    def height_in_shape(self) -> int:
        ...
    
    @height_in_shape.setter
    def height_in_shape(self, value : int):
        ...
    
    @property
    def group(self) -> aspose.cells.drawing.GroupShape:
        '''Gets the group shape which contains this shape.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.AutoShapeType:
        '''Gets the auto shape type.'''
        ...
    
    @property
    def has_line(self) -> bool:
        ...
    
    @has_line.setter
    def has_line(self, value : bool):
        ...
    
    @property
    def is_filled(self) -> bool:
        ...
    
    @is_filled.setter
    def is_filled(self, value : bool):
        ...
    
    @property
    def is_flipped_horizontally(self) -> bool:
        ...
    
    @is_flipped_horizontally.setter
    def is_flipped_horizontally(self, value : bool):
        ...
    
    @property
    def is_flipped_vertically(self) -> bool:
        ...
    
    @is_flipped_vertically.setter
    def is_flipped_vertically(self, value : bool):
        ...
    
    @property
    def actual_lower_right_row(self) -> int:
        ...
    
    @property
    def connection_points(self) -> aspose.pydrawing.PointF[]:
        ...
    
    @property
    def relative_to_original_picture_size(self) -> bool:
        ...
    
    @relative_to_original_picture_size.setter
    def relative_to_original_picture_size(self, value : bool):
        ...
    
    @property
    def linked_cell(self) -> str:
        ...
    
    @linked_cell.setter
    def linked_cell(self, value : str):
        ...
    
    @property
    def input_range(self) -> str:
        ...
    
    @input_range.setter
    def input_range(self, value : str):
        ...
    
    @property
    def text_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @text_shape_type.setter
    def text_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def text_body(self) -> aspose.cells.drawing.texts.FontSettingCollection:
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Represents the font of shape.'''
        ...
    
    @font.setter
    def font(self, value : aspose.cells.Font):
        '''Represents the font of shape.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    @text_options.setter
    def text_options(self, value : aspose.cells.drawing.texts.TextOptions):
        ...
    
    @property
    def text(self) -> str:
        '''Represents the string in this TextBox object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Represents the string in this TextBox object.'''
        ...
    
    @property
    def is_rich_text(self) -> bool:
        ...
    
    @property
    def html_text(self) -> str:
        ...
    
    @html_text.setter
    def html_text(self, value : str):
        ...
    
    @property
    def text_vertical_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_vertical_overflow.setter
    def text_vertical_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def text_horizontal_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_horizontal_overflow.setter
    def text_horizontal_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
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
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def control_data(self) -> bytes:
        ...
    
    @property
    def active_x_control(self) -> aspose.cells.drawing.activexcontrols.ActiveXControl:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets the paths of a custom geometric shape.'''
        ...
    
    @property
    def geometry(self) -> aspose.cells.drawing.Geometry:
        '''Gets the geometry'''
        ...
    
    @property
    def create_id(self) -> Guid:
        ...
    
    @create_id.setter
    def create_id(self, value : Guid):
        ...
    
    @property
    def begin_arrowhead_style(self) -> aspose.cells.drawing.MsoArrowheadStyle:
        ...
    
    @begin_arrowhead_style.setter
    def begin_arrowhead_style(self, value : aspose.cells.drawing.MsoArrowheadStyle):
        ...
    
    @property
    def begin_arrowhead_width(self) -> aspose.cells.drawing.MsoArrowheadWidth:
        ...
    
    @begin_arrowhead_width.setter
    def begin_arrowhead_width(self, value : aspose.cells.drawing.MsoArrowheadWidth):
        ...
    
    @property
    def begin_arrowhead_length(self) -> aspose.cells.drawing.MsoArrowheadLength:
        ...
    
    @begin_arrowhead_length.setter
    def begin_arrowhead_length(self, value : aspose.cells.drawing.MsoArrowheadLength):
        ...
    
    @property
    def end_arrowhead_style(self) -> aspose.cells.drawing.MsoArrowheadStyle:
        ...
    
    @end_arrowhead_style.setter
    def end_arrowhead_style(self, value : aspose.cells.drawing.MsoArrowheadStyle):
        ...
    
    @property
    def end_arrowhead_width(self) -> aspose.cells.drawing.MsoArrowheadWidth:
        ...
    
    @end_arrowhead_width.setter
    def end_arrowhead_width(self, value : aspose.cells.drawing.MsoArrowheadWidth):
        ...
    
    @property
    def end_arrowhead_length(self) -> aspose.cells.drawing.MsoArrowheadLength:
        ...
    
    @end_arrowhead_length.setter
    def end_arrowhead_length(self, value : aspose.cells.drawing.MsoArrowheadLength):
        ...
    
    ...

class ListBox(Shape):
    '''Represents a list box object.'''
    
    @overload
    def to_image(self, stream : io.RawIOBase, image_type : aspose.cells.drawing.ImageType):
        '''Creates the shape image and saves it to a stream in the specified format.
        
        :param stream: The output stream.
        :param image_type: The type in which to save the image.'''
        ...
    
    @overload
    def to_image(self, image_file : str, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a file.'''
        ...
    
    @overload
    def to_image(self, stream : io.RawIOBase, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a stream.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.'''
        ...
    
    def get_result_of_smart_art(self) -> aspose.cells.drawing.GroupShape:
        '''Converting smart art to grouped shapes.'''
        ...
    
    def to_front_or_back(self, orders : int):
        '''Brings the shape to the front or sends the shape to back.
        
        :param orders: If it's less than zero, sets the shape to back.
        If it's greater than zero, brings the shape to front.'''
        ...
    
    def get_locked_property(self, type : aspose.cells.drawing.ShapeLockType) -> bool:
        '''Gets the value of locked property.
        
        :param type: The type of the shape locked property.
        :returns: Returns  the value of locked property.'''
        ...
    
    def set_locked_property(self, type : aspose.cells.drawing.ShapeLockType, value : bool):
        '''Set the locked property.
        
        :param type: The locked type.
        :param value: The value of the property.'''
        ...
    
    def add_hyperlink(self, address : str) -> aspose.cells.Hyperlink:
        '''Adds a hyperlink to the shape.
        
        :param address: Address of the hyperlink.
        :returns: Return the new hyperlink object.'''
        ...
    
    def remove_hyperlink(self):
        '''Remove the hyperlink of the shape.'''
        ...
    
    def move_to_range(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int):
        '''Moves the shape to a specified range.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index'''
        ...
    
    def align_top_right_corner(self, top_row : int, right_column : int):
        '''Moves the picture to the top-right corner.
        
        :param top_row: the row index.
        :param right_column: the column index.'''
        ...
    
    def get_connection_points(self) -> List[List[float]]:
        '''Get the connection points
        
        :returns: [X,Y] pairs of the connection point. Every item is a float[2] array, [0] represents x and [1] represents y.'''
        ...
    
    def get_linked_cell(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range linked to the control's value.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range linked to the control's value.'''
        ...
    
    def set_linked_cell(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range linked to the control's value.
        
        :param formula: The range linked to the control's value.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def get_input_range(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range used to fill the control.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range used to fill the control.'''
        ...
    
    def set_input_range(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range used to fill the control.
        
        :param formula: The range used to fill the control.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell.'''
        ...
    
    def calculate_text_size(self) -> List[int]:
        '''Recalculate the text area
        
        :returns: Text's Size in an array(width and height).'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the text .
        
        :returns: All Characters objects'''
        ...
    
    def remove_active_x_control(self):
        '''Remove activeX control.'''
        ...
    
    def is_same_setting(self, obj : any) -> bool:
        '''Returns whether the shape is same.'''
        ...
    
    def selected_item(self, item_index : int, is_selected : bool):
        '''Sets whether the item is selected
        
        :param item_index: The item index
        :param is_selected: Whether the item is selected.
        True means that this item should be selected.
        False means that this item should be unselected.'''
        ...
    
    def is_selected(self, item_index : int) -> bool:
        '''Indicates whether the item is selected.
        
        :param item_index: The item index.
        :returns: whether the item is selected.'''
        ...
    
    @property
    def macro_name(self) -> str:
        ...
    
    @macro_name.setter
    def macro_name(self, value : str):
        ...
    
    @property
    def is_equation(self) -> bool:
        ...
    
    @property
    def is_smart_art(self) -> bool:
        ...
    
    @property
    def z_order_position(self) -> int:
        ...
    
    @z_order_position.setter
    def z_order_position(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of the shape.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of the shape.'''
        ...
    
    @property
    def alternative_text(self) -> str:
        ...
    
    @alternative_text.setter
    def alternative_text(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @property
    def line_format(self) -> aspose.cells.drawing.MsoLineFormat:
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.MsoFillFormat:
        ...
    
    @property
    def format(self) -> aspose.cells.drawing.ShapeFormat:
        '''Represents the setting of the shape's formatting.'''
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        '''Gets line style'''
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        '''Returns a :py:attr:`aspose.cells.drawing.Shape.fill_format` object that contains fill formatting properties for the specified shape.'''
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def reflection(self) -> aspose.cells.drawing.ReflectionEffect:
        '''Represents a :py:class:`aspose.cells.drawing.ReflectionEffect` object that specifies reflection effect for the chart element or shape.'''
        ...
    
    @property
    def glow(self) -> aspose.cells.drawing.GlowEffect:
        '''Represents a :py:class:`aspose.cells.drawing.GlowEffect` object that specifies glow effect for the chart element or shape.'''
        ...
    
    @property
    def soft_edges(self) -> float:
        ...
    
    @soft_edges.setter
    def soft_edges(self, value : float):
        ...
    
    @property
    def three_d_format(self) -> aspose.cells.drawing.ThreeDFormat:
        ...
    
    @property
    def text_frame(self) -> aspose.cells.drawing.MsoTextFrame:
        ...
    
    @property
    def format_picture(self) -> aspose.cells.drawing.MsoFormatPicture:
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_lock_aspect_ratio(self) -> bool:
        ...
    
    @is_lock_aspect_ratio.setter
    def is_lock_aspect_ratio(self, value : bool):
        ...
    
    @property
    def rotation_angle(self) -> float:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : float):
        ...
    
    @property
    def hyperlink(self) -> aspose.cells.Hyperlink:
        '''Gets the hyperlink of the shape.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier of this shape.'''
        ...
    
    @property
    def spid(self) -> str:
        '''Specifies an optional string that an application can use to Identify the particular shape.'''
        ...
    
    @property
    def spt(self) -> int:
        '''Specifies an optional number that an application can use to associate the particular shape with a defined shape type.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.drawing.Shape.worksheet` object which contains this shape.'''
        ...
    
    @property
    def is_group(self) -> bool:
        ...
    
    @property
    def is_in_group(self) -> bool:
        ...
    
    @property
    def is_word_art(self) -> bool:
        ...
    
    @property
    def text_effect(self) -> aspose.cells.drawing.TextEffectFormat:
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_printable(self) -> bool:
        ...
    
    @is_printable.setter
    def is_printable(self, value : bool):
        ...
    
    @property
    def mso_drawing_type(self) -> aspose.cells.drawing.MsoDrawingType:
        ...
    
    @property
    def auto_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @auto_shape_type.setter
    def auto_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def anchor_type(self) -> aspose.cells.drawing.ShapeAnchorType:
        ...
    
    @anchor_type.setter
    def anchor_type(self, value : aspose.cells.drawing.ShapeAnchorType):
        ...
    
    @property
    def placement(self) -> aspose.cells.drawing.PlacementType:
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @placement.setter
    def placement(self, value : aspose.cells.drawing.PlacementType):
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @property
    def upper_left_row(self) -> int:
        ...
    
    @upper_left_row.setter
    def upper_left_row(self, value : int):
        ...
    
    @property
    def upper_delta_y(self) -> int:
        ...
    
    @upper_delta_y.setter
    def upper_delta_y(self, value : int):
        ...
    
    @property
    def upper_left_column(self) -> int:
        ...
    
    @upper_left_column.setter
    def upper_left_column(self, value : int):
        ...
    
    @property
    def upper_delta_x(self) -> int:
        ...
    
    @upper_delta_x.setter
    def upper_delta_x(self, value : int):
        ...
    
    @property
    def lower_right_row(self) -> int:
        ...
    
    @lower_right_row.setter
    def lower_right_row(self, value : int):
        ...
    
    @property
    def lower_delta_y(self) -> int:
        ...
    
    @lower_delta_y.setter
    def lower_delta_y(self, value : int):
        ...
    
    @property
    def lower_right_column(self) -> int:
        ...
    
    @lower_right_column.setter
    def lower_right_column(self, value : int):
        ...
    
    @property
    def lower_delta_x(self) -> int:
        ...
    
    @lower_delta_x.setter
    def lower_delta_x(self, value : int):
        ...
    
    @property
    def right(self) -> int:
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def width_pt(self) -> float:
        ...
    
    @width_pt.setter
    def width_pt(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def height(self) -> int:
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    @property
    def height_pt(self) -> float:
        ...
    
    @height_pt.setter
    def height_pt(self, value : float):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def left(self) -> int:
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @property
    def left_inch(self) -> float:
        ...
    
    @left_inch.setter
    def left_inch(self, value : float):
        ...
    
    @property
    def left_cm(self) -> float:
        ...
    
    @left_cm.setter
    def left_cm(self, value : float):
        ...
    
    @property
    def top(self) -> int:
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @property
    def top_inch(self) -> float:
        ...
    
    @top_inch.setter
    def top_inch(self, value : float):
        ...
    
    @property
    def top_cm(self) -> float:
        ...
    
    @top_cm.setter
    def top_cm(self, value : float):
        ...
    
    @property
    def top_to_corner(self) -> int:
        ...
    
    @top_to_corner.setter
    def top_to_corner(self, value : int):
        ...
    
    @property
    def left_to_corner(self) -> int:
        ...
    
    @left_to_corner.setter
    def left_to_corner(self, value : int):
        ...
    
    @property
    def x(self) -> int:
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @property
    def width_scale(self) -> int:
        ...
    
    @width_scale.setter
    def width_scale(self, value : int):
        ...
    
    @property
    def height_scale(self) -> int:
        ...
    
    @height_scale.setter
    def height_scale(self, value : int):
        ...
    
    @property
    def top_in_shape(self) -> int:
        ...
    
    @top_in_shape.setter
    def top_in_shape(self, value : int):
        ...
    
    @property
    def left_in_shape(self) -> int:
        ...
    
    @left_in_shape.setter
    def left_in_shape(self, value : int):
        ...
    
    @property
    def width_in_shape(self) -> int:
        ...
    
    @width_in_shape.setter
    def width_in_shape(self, value : int):
        ...
    
    @property
    def height_in_shape(self) -> int:
        ...
    
    @height_in_shape.setter
    def height_in_shape(self, value : int):
        ...
    
    @property
    def group(self) -> aspose.cells.drawing.GroupShape:
        '''Gets the group shape which contains this shape.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.AutoShapeType:
        '''Gets the auto shape type.'''
        ...
    
    @property
    def has_line(self) -> bool:
        ...
    
    @has_line.setter
    def has_line(self, value : bool):
        ...
    
    @property
    def is_filled(self) -> bool:
        ...
    
    @is_filled.setter
    def is_filled(self, value : bool):
        ...
    
    @property
    def is_flipped_horizontally(self) -> bool:
        ...
    
    @is_flipped_horizontally.setter
    def is_flipped_horizontally(self, value : bool):
        ...
    
    @property
    def is_flipped_vertically(self) -> bool:
        ...
    
    @is_flipped_vertically.setter
    def is_flipped_vertically(self, value : bool):
        ...
    
    @property
    def actual_lower_right_row(self) -> int:
        ...
    
    @property
    def connection_points(self) -> aspose.pydrawing.PointF[]:
        ...
    
    @property
    def relative_to_original_picture_size(self) -> bool:
        ...
    
    @relative_to_original_picture_size.setter
    def relative_to_original_picture_size(self, value : bool):
        ...
    
    @property
    def linked_cell(self) -> str:
        ...
    
    @linked_cell.setter
    def linked_cell(self, value : str):
        ...
    
    @property
    def input_range(self) -> str:
        ...
    
    @input_range.setter
    def input_range(self, value : str):
        ...
    
    @property
    def text_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @text_shape_type.setter
    def text_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def text_body(self) -> aspose.cells.drawing.texts.FontSettingCollection:
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Represents the font of shape.'''
        ...
    
    @font.setter
    def font(self, value : aspose.cells.Font):
        '''Represents the font of shape.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    @text_options.setter
    def text_options(self, value : aspose.cells.drawing.texts.TextOptions):
        ...
    
    @property
    def text(self) -> str:
        '''Represents the string in this TextBox object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Represents the string in this TextBox object.'''
        ...
    
    @property
    def is_rich_text(self) -> bool:
        ...
    
    @property
    def html_text(self) -> str:
        ...
    
    @html_text.setter
    def html_text(self, value : str):
        ...
    
    @property
    def text_vertical_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_vertical_overflow.setter
    def text_vertical_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def text_horizontal_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_horizontal_overflow.setter
    def text_horizontal_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
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
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def control_data(self) -> bytes:
        ...
    
    @property
    def active_x_control(self) -> aspose.cells.drawing.activexcontrols.ActiveXControl:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets the paths of a custom geometric shape.'''
        ...
    
    @property
    def geometry(self) -> aspose.cells.drawing.Geometry:
        '''Gets the geometry'''
        ...
    
    @property
    def create_id(self) -> Guid:
        ...
    
    @create_id.setter
    def create_id(self, value : Guid):
        ...
    
    @property
    def item_count(self) -> int:
        ...
    
    @property
    def selected_index(self) -> int:
        ...
    
    @selected_index.setter
    def selected_index(self, value : int):
        ...
    
    @property
    def selected_cells(self) -> List[aspose.cells.Cell]:
        ...
    
    @property
    def shadow(self) -> bool:
        '''Indicates whether the combobox has 3-D shading.'''
        ...
    
    @shadow.setter
    def shadow(self, value : bool):
        '''Indicates whether the combobox has 3-D shading.'''
        ...
    
    @property
    def selection_type(self) -> aspose.cells.drawing.SelectionType:
        ...
    
    @selection_type.setter
    def selection_type(self, value : aspose.cells.drawing.SelectionType):
        ...
    
    @property
    def page_change(self) -> int:
        ...
    
    @page_change.setter
    def page_change(self, value : int):
        ...
    
    ...

class MsoFillFormat:
    '''Represents fill formatting for a shape.'''
    
    def set_one_color_gradient(self, color : aspose.pydrawing.Color, degree : float, style : aspose.cells.drawing.GradientStyleType, variant : int):
        '''Sets the specified fill to a one-color gradient.
        
        :param color: One gradient color.
        :param degree: The gradient degree. Can be a value from 0.0 (dark) through 1.0 (light).
        :param style: Gradient shading style.
        :param variant: The gradient variant. Can be a value from 1 through 4, corresponding to one of the four variants on the Gradient tab in the Fill Effects dialog box. If style is GradientStyle.FromCenter, the Variant argument can only be 1 or 2.'''
        ...
    
    @property
    def fore_color(self) -> aspose.pydrawing.Color:
        ...
    
    @fore_color.setter
    def fore_color(self, value : aspose.pydrawing.Color):
        ...
    
    @property
    def transparency(self) -> float:
        '''Returns the degree of transparency of the specified fill as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    @transparency.setter
    def transparency(self, value : float):
        '''Returns or sets the degree of transparency of the specified fill as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    @property
    def back_color(self) -> aspose.pydrawing.Color:
        ...
    
    @back_color.setter
    def back_color(self, value : aspose.pydrawing.Color):
        ...
    
    @property
    def image_data(self) -> bytes:
        ...
    
    @image_data.setter
    def image_data(self, value : bytes):
        ...
    
    @property
    def texture(self) -> aspose.cells.drawing.TextureType:
        '''Gets the texture fill type.'''
        ...
    
    @property
    def is_visible(self) -> bool:
        ...
    
    @is_visible.setter
    def is_visible(self, value : bool):
        ...
    
    ...

class MsoFillFormatHelper:
    '''Represents fill formatting for a shape.'''
    
    def set_one_color_gradient(self, color : aspose.pydrawing.Color, degree : float, style : aspose.cells.drawing.GradientStyleType, variant : int):
        '''Sets the specified fill to a one-color gradient.
        
        :param color: One gradient color.
        :param degree: The gradient degree. Can be a value from 0.0 (dark) through 1.0 (light).
        :param style: Gradient shading style.
        :param variant: The gradient variant. Can be a value from 1 through 4, corresponding to one of the four variants on the Gradient tab in the Fill Effects dialog box. If style is GradientStyle.FromCenter, the Variant argument can only be 1 or 2.'''
        ...
    
    @property
    def fore_color(self) -> aspose.pydrawing.Color:
        ...
    
    @fore_color.setter
    def fore_color(self, value : aspose.pydrawing.Color):
        ...
    
    @property
    def fore_color_transparency(self) -> float:
        ...
    
    @fore_color_transparency.setter
    def fore_color_transparency(self, value : float):
        ...
    
    @property
    def back_color(self) -> aspose.pydrawing.Color:
        ...
    
    @back_color.setter
    def back_color(self, value : aspose.pydrawing.Color):
        ...
    
    @property
    def image_data(self) -> bytes:
        ...
    
    @image_data.setter
    def image_data(self, value : bytes):
        ...
    
    @property
    def texture(self) -> aspose.cells.drawing.TextureType:
        '''Gets the texture fill type.'''
        ...
    
    @property
    def is_visible(self) -> bool:
        ...
    
    @is_visible.setter
    def is_visible(self, value : bool):
        ...
    
    ...

class MsoFormatPicture:
    '''Represents the picture format.'''
    
    @property
    def top_crop(self) -> float:
        ...
    
    @top_crop.setter
    def top_crop(self, value : float):
        ...
    
    @property
    def bottom_crop(self) -> float:
        ...
    
    @bottom_crop.setter
    def bottom_crop(self, value : float):
        ...
    
    @property
    def left_crop(self) -> float:
        ...
    
    @left_crop.setter
    def left_crop(self, value : float):
        ...
    
    @property
    def right_crop(self) -> float:
        ...
    
    @right_crop.setter
    def right_crop(self, value : float):
        ...
    
    @property
    def transparency(self) -> float:
        '''Returns the degree of transparency of the area as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    @transparency.setter
    def transparency(self, value : float):
        '''Returns or sets the degree of transparency of the area as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    @property
    def transparent_color(self) -> aspose.cells.CellsColor:
        ...
    
    @transparent_color.setter
    def transparent_color(self, value : aspose.cells.CellsColor):
        ...
    
    @property
    def contrast(self) -> float:
        '''Represents the contrast modification for the picture.in unit of percentage.'''
        ...
    
    @contrast.setter
    def contrast(self, value : float):
        '''Represents the contrast modification for the picture.in unit of percentage.'''
        ...
    
    @property
    def brightness(self) -> float:
        '''Represents the brightness modification for the picture in unit of percentage.'''
        ...
    
    @brightness.setter
    def brightness(self, value : float):
        '''Represents the brightness modification for the picture in unit of percentage.'''
        ...
    
    @property
    def gamma(self) -> float:
        '''Represents gamma of the picture.'''
        ...
    
    @gamma.setter
    def gamma(self, value : float):
        '''Represents gamma of the picture.'''
        ...
    
    @property
    def is_bi_level(self) -> bool:
        ...
    
    @is_bi_level.setter
    def is_bi_level(self, value : bool):
        ...
    
    @property
    def is_gray(self) -> bool:
        ...
    
    @is_gray.setter
    def is_gray(self, value : bool):
        ...
    
    ...

class MsoLineFormat:
    '''Represents line and arrowhead formatting.'''
    
    @property
    def is_visible(self) -> bool:
        ...
    
    @is_visible.setter
    def is_visible(self, value : bool):
        ...
    
    @property
    def style(self) -> aspose.cells.drawing.MsoLineStyle:
        '''Returns a Style object that represents the style of the specified range.'''
        ...
    
    @style.setter
    def style(self, value : aspose.cells.drawing.MsoLineStyle):
        '''Returns a Style object that represents the style of the specified range.'''
        ...
    
    @property
    def fore_color(self) -> aspose.pydrawing.Color:
        ...
    
    @fore_color.setter
    def fore_color(self, value : aspose.pydrawing.Color):
        ...
    
    @property
    def back_color(self) -> aspose.pydrawing.Color:
        ...
    
    @back_color.setter
    def back_color(self, value : aspose.pydrawing.Color):
        ...
    
    @property
    def dash_style(self) -> aspose.cells.drawing.MsoLineDashStyle:
        ...
    
    @dash_style.setter
    def dash_style(self, value : aspose.cells.drawing.MsoLineDashStyle):
        ...
    
    @property
    def transparency(self) -> float:
        '''Returns the degree of transparency of the specified fill as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    @transparency.setter
    def transparency(self, value : float):
        '''Returns or sets the degree of transparency of the specified fill as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    @property
    def weight(self) -> float:
        '''Returns the weight of the line ,in units of pt.'''
        ...
    
    @weight.setter
    def weight(self, value : float):
        '''Returns or sets the weight of the line ,in units of pt.'''
        ...
    
    ...

class MsoLineFormatHelper:
    '''Represents line and arrowhead formatting.'''
    
    @property
    def is_visible(self) -> bool:
        ...
    
    @is_visible.setter
    def is_visible(self, value : bool):
        ...
    
    @property
    def style(self) -> aspose.cells.drawing.MsoLineStyle:
        '''Returns a Style object that represents the style of the specified range.'''
        ...
    
    @style.setter
    def style(self, value : aspose.cells.drawing.MsoLineStyle):
        '''Returns a Style object that represents the style of the specified range.'''
        ...
    
    @property
    def fore_color(self) -> aspose.pydrawing.Color:
        ...
    
    @fore_color.setter
    def fore_color(self, value : aspose.pydrawing.Color):
        ...
    
    @property
    def back_color(self) -> aspose.pydrawing.Color:
        ...
    
    @back_color.setter
    def back_color(self, value : aspose.pydrawing.Color):
        ...
    
    @property
    def dash_style(self) -> aspose.cells.drawing.MsoLineDashStyle:
        ...
    
    @dash_style.setter
    def dash_style(self, value : aspose.cells.drawing.MsoLineDashStyle):
        ...
    
    @property
    def transparency(self) -> float:
        '''Returns the degree of transparency of the specified fill as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    @transparency.setter
    def transparency(self, value : float):
        '''Returns or sets the degree of transparency of the specified fill as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    @property
    def weight(self) -> float:
        '''Returns the weight of the line ,in units of pt.'''
        ...
    
    @weight.setter
    def weight(self, value : float):
        '''Returns or sets the weight of the line ,in units of pt.'''
        ...
    
    ...

class MsoTextFrame:
    '''Represents the text frame in a Shape object.'''
    
    @property
    def auto_size(self) -> bool:
        ...
    
    @auto_size.setter
    def auto_size(self, value : bool):
        ...
    
    @property
    def is_auto_margin(self) -> bool:
        ...
    
    @is_auto_margin.setter
    def is_auto_margin(self, value : bool):
        ...
    
    @property
    def rotate_text_with_shape(self) -> bool:
        ...
    
    @rotate_text_with_shape.setter
    def rotate_text_with_shape(self, value : bool):
        ...
    
    @property
    def left_margin_pt(self) -> float:
        ...
    
    @left_margin_pt.setter
    def left_margin_pt(self, value : float):
        ...
    
    @property
    def right_margin_pt(self) -> float:
        ...
    
    @right_margin_pt.setter
    def right_margin_pt(self, value : float):
        ...
    
    @property
    def top_margin_pt(self) -> float:
        ...
    
    @top_margin_pt.setter
    def top_margin_pt(self, value : float):
        ...
    
    @property
    def bottom_margin_pt(self) -> float:
        ...
    
    @bottom_margin_pt.setter
    def bottom_margin_pt(self, value : float):
        ...
    
    ...

class NoneFill(Fill):
    '''Represents no fill.'''
    
    ...

class OleObject(Shape):
    '''Represents an OleObject in a worksheet.'''
    
    @overload
    def to_image(self, stream : io.RawIOBase, image_type : aspose.cells.drawing.ImageType):
        '''Creates the shape image and saves it to a stream in the specified format.
        
        :param stream: The output stream.
        :param image_type: The type in which to save the image.'''
        ...
    
    @overload
    def to_image(self, image_file : str, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a file.'''
        ...
    
    @overload
    def to_image(self, stream : io.RawIOBase, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a stream.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.'''
        ...
    
    @overload
    def set_embedded_object(self, link_to_file : bool, object_data : bytes, source_file_name : str, display_as_icon : bool, label : str):
        '''Sets embedded object data.
        
        :param link_to_file: Indicates whether the object links to the file. If true, the parameter objectData is ignored.
        :param object_data: The embedded object data.
        :param source_file_name: The file name.
        :param display_as_icon: Indicates whether diplaying object as an icon.
        If true, the orginal image data will be covered by icon.
        :param label: The icon label. Only works when displayAsIcon as true.'''
        ...
    
    @overload
    def set_embedded_object(self, link_to_file : bool, object_data : bytes, source_file_name : str, display_as_icon : bool, label : str, update_icon : bool):
        '''Sets embedded object data.
        
        :param link_to_file: Indicates whether the object links to the file. If true, the parameter objectData is ignored.
        :param object_data: The embedded object data.
        :param source_file_name: The file name.
        :param display_as_icon: Indicates whether diplaying object as an icon.
        If true, the orginal image data will be covered by icon.
        :param label: The icon label. Only works when displayAsIcon as true.
        :param update_icon: Indicates whether automatically updating icon.'''
        ...
    
    def get_result_of_smart_art(self) -> aspose.cells.drawing.GroupShape:
        '''Converting smart art to grouped shapes.'''
        ...
    
    def to_front_or_back(self, orders : int):
        '''Brings the shape to the front or sends the shape to back.
        
        :param orders: If it's less than zero, sets the shape to back.
        If it's greater than zero, brings the shape to front.'''
        ...
    
    def get_locked_property(self, type : aspose.cells.drawing.ShapeLockType) -> bool:
        '''Gets the value of locked property.
        
        :param type: The type of the shape locked property.
        :returns: Returns  the value of locked property.'''
        ...
    
    def set_locked_property(self, type : aspose.cells.drawing.ShapeLockType, value : bool):
        '''Set the locked property.
        
        :param type: The locked type.
        :param value: The value of the property.'''
        ...
    
    def add_hyperlink(self, address : str) -> aspose.cells.Hyperlink:
        '''Adds a hyperlink to the shape.
        
        :param address: Address of the hyperlink.
        :returns: Return the new hyperlink object.'''
        ...
    
    def remove_hyperlink(self):
        '''Remove the hyperlink of the shape.'''
        ...
    
    def move_to_range(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int):
        '''Moves the shape to a specified range.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index'''
        ...
    
    def align_top_right_corner(self, top_row : int, right_column : int):
        '''Moves the picture to the top-right corner.
        
        :param top_row: the row index.
        :param right_column: the column index.'''
        ...
    
    def get_connection_points(self) -> List[List[float]]:
        '''Get the connection points
        
        :returns: [X,Y] pairs of the connection point. Every item is a float[2] array, [0] represents x and [1] represents y.'''
        ...
    
    def get_linked_cell(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range linked to the control's value.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range linked to the control's value.'''
        ...
    
    def set_linked_cell(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range linked to the control's value.
        
        :param formula: The range linked to the control's value.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def get_input_range(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range used to fill the control.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range used to fill the control.'''
        ...
    
    def set_input_range(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range used to fill the control.
        
        :param formula: The range used to fill the control.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell.'''
        ...
    
    def calculate_text_size(self) -> List[int]:
        '''Recalculate the text area
        
        :returns: Text's Size in an array(width and height).'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the text .
        
        :returns: All Characters objects'''
        ...
    
    def remove_active_x_control(self):
        '''Remove activeX control.'''
        ...
    
    def is_same_setting(self, obj : any) -> bool:
        '''Returns whether the shape is same.'''
        ...
    
    def set_native_source_full_name(self, source_full_name : str):
        '''Sets the ole native source full file name with path.
        
        :param source_full_name: the ole native source full file name'''
        ...
    
    @property
    def macro_name(self) -> str:
        ...
    
    @macro_name.setter
    def macro_name(self, value : str):
        ...
    
    @property
    def is_equation(self) -> bool:
        ...
    
    @property
    def is_smart_art(self) -> bool:
        ...
    
    @property
    def z_order_position(self) -> int:
        ...
    
    @z_order_position.setter
    def z_order_position(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of the shape.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of the shape.'''
        ...
    
    @property
    def alternative_text(self) -> str:
        ...
    
    @alternative_text.setter
    def alternative_text(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @property
    def line_format(self) -> aspose.cells.drawing.MsoLineFormat:
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.MsoFillFormat:
        ...
    
    @property
    def format(self) -> aspose.cells.drawing.ShapeFormat:
        '''Represents the setting of the shape's formatting.'''
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        '''Gets line style'''
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        '''Returns a :py:attr:`aspose.cells.drawing.Shape.fill_format` object that contains fill formatting properties for the specified shape.'''
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def reflection(self) -> aspose.cells.drawing.ReflectionEffect:
        '''Represents a :py:class:`aspose.cells.drawing.ReflectionEffect` object that specifies reflection effect for the chart element or shape.'''
        ...
    
    @property
    def glow(self) -> aspose.cells.drawing.GlowEffect:
        '''Represents a :py:class:`aspose.cells.drawing.GlowEffect` object that specifies glow effect for the chart element or shape.'''
        ...
    
    @property
    def soft_edges(self) -> float:
        ...
    
    @soft_edges.setter
    def soft_edges(self, value : float):
        ...
    
    @property
    def three_d_format(self) -> aspose.cells.drawing.ThreeDFormat:
        ...
    
    @property
    def text_frame(self) -> aspose.cells.drawing.MsoTextFrame:
        ...
    
    @property
    def format_picture(self) -> aspose.cells.drawing.MsoFormatPicture:
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_lock_aspect_ratio(self) -> bool:
        ...
    
    @is_lock_aspect_ratio.setter
    def is_lock_aspect_ratio(self, value : bool):
        ...
    
    @property
    def rotation_angle(self) -> float:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : float):
        ...
    
    @property
    def hyperlink(self) -> aspose.cells.Hyperlink:
        '''Gets the hyperlink of the shape.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier of this shape.'''
        ...
    
    @property
    def spid(self) -> str:
        '''Specifies an optional string that an application can use to Identify the particular shape.'''
        ...
    
    @property
    def spt(self) -> int:
        '''Specifies an optional number that an application can use to associate the particular shape with a defined shape type.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.drawing.Shape.worksheet` object which contains this shape.'''
        ...
    
    @property
    def is_group(self) -> bool:
        ...
    
    @property
    def is_in_group(self) -> bool:
        ...
    
    @property
    def is_word_art(self) -> bool:
        ...
    
    @property
    def text_effect(self) -> aspose.cells.drawing.TextEffectFormat:
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_printable(self) -> bool:
        ...
    
    @is_printable.setter
    def is_printable(self, value : bool):
        ...
    
    @property
    def mso_drawing_type(self) -> aspose.cells.drawing.MsoDrawingType:
        ...
    
    @property
    def auto_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @auto_shape_type.setter
    def auto_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def anchor_type(self) -> aspose.cells.drawing.ShapeAnchorType:
        ...
    
    @anchor_type.setter
    def anchor_type(self, value : aspose.cells.drawing.ShapeAnchorType):
        ...
    
    @property
    def placement(self) -> aspose.cells.drawing.PlacementType:
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @placement.setter
    def placement(self, value : aspose.cells.drawing.PlacementType):
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @property
    def upper_left_row(self) -> int:
        ...
    
    @upper_left_row.setter
    def upper_left_row(self, value : int):
        ...
    
    @property
    def upper_delta_y(self) -> int:
        ...
    
    @upper_delta_y.setter
    def upper_delta_y(self, value : int):
        ...
    
    @property
    def upper_left_column(self) -> int:
        ...
    
    @upper_left_column.setter
    def upper_left_column(self, value : int):
        ...
    
    @property
    def upper_delta_x(self) -> int:
        ...
    
    @upper_delta_x.setter
    def upper_delta_x(self, value : int):
        ...
    
    @property
    def lower_right_row(self) -> int:
        ...
    
    @lower_right_row.setter
    def lower_right_row(self, value : int):
        ...
    
    @property
    def lower_delta_y(self) -> int:
        ...
    
    @lower_delta_y.setter
    def lower_delta_y(self, value : int):
        ...
    
    @property
    def lower_right_column(self) -> int:
        ...
    
    @lower_right_column.setter
    def lower_right_column(self, value : int):
        ...
    
    @property
    def lower_delta_x(self) -> int:
        ...
    
    @lower_delta_x.setter
    def lower_delta_x(self, value : int):
        ...
    
    @property
    def right(self) -> int:
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def width_pt(self) -> float:
        ...
    
    @width_pt.setter
    def width_pt(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def height(self) -> int:
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    @property
    def height_pt(self) -> float:
        ...
    
    @height_pt.setter
    def height_pt(self, value : float):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def left(self) -> int:
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @property
    def left_inch(self) -> float:
        ...
    
    @left_inch.setter
    def left_inch(self, value : float):
        ...
    
    @property
    def left_cm(self) -> float:
        ...
    
    @left_cm.setter
    def left_cm(self, value : float):
        ...
    
    @property
    def top(self) -> int:
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @property
    def top_inch(self) -> float:
        ...
    
    @top_inch.setter
    def top_inch(self, value : float):
        ...
    
    @property
    def top_cm(self) -> float:
        ...
    
    @top_cm.setter
    def top_cm(self, value : float):
        ...
    
    @property
    def top_to_corner(self) -> int:
        ...
    
    @top_to_corner.setter
    def top_to_corner(self, value : int):
        ...
    
    @property
    def left_to_corner(self) -> int:
        ...
    
    @left_to_corner.setter
    def left_to_corner(self, value : int):
        ...
    
    @property
    def x(self) -> int:
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @property
    def width_scale(self) -> int:
        ...
    
    @width_scale.setter
    def width_scale(self, value : int):
        ...
    
    @property
    def height_scale(self) -> int:
        ...
    
    @height_scale.setter
    def height_scale(self, value : int):
        ...
    
    @property
    def top_in_shape(self) -> int:
        ...
    
    @top_in_shape.setter
    def top_in_shape(self, value : int):
        ...
    
    @property
    def left_in_shape(self) -> int:
        ...
    
    @left_in_shape.setter
    def left_in_shape(self, value : int):
        ...
    
    @property
    def width_in_shape(self) -> int:
        ...
    
    @width_in_shape.setter
    def width_in_shape(self, value : int):
        ...
    
    @property
    def height_in_shape(self) -> int:
        ...
    
    @height_in_shape.setter
    def height_in_shape(self, value : int):
        ...
    
    @property
    def group(self) -> aspose.cells.drawing.GroupShape:
        '''Gets the group shape which contains this shape.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.AutoShapeType:
        '''Gets the auto shape type.'''
        ...
    
    @property
    def has_line(self) -> bool:
        ...
    
    @has_line.setter
    def has_line(self, value : bool):
        ...
    
    @property
    def is_filled(self) -> bool:
        ...
    
    @is_filled.setter
    def is_filled(self, value : bool):
        ...
    
    @property
    def is_flipped_horizontally(self) -> bool:
        ...
    
    @is_flipped_horizontally.setter
    def is_flipped_horizontally(self, value : bool):
        ...
    
    @property
    def is_flipped_vertically(self) -> bool:
        ...
    
    @is_flipped_vertically.setter
    def is_flipped_vertically(self, value : bool):
        ...
    
    @property
    def actual_lower_right_row(self) -> int:
        ...
    
    @property
    def connection_points(self) -> aspose.pydrawing.PointF[]:
        ...
    
    @property
    def relative_to_original_picture_size(self) -> bool:
        ...
    
    @relative_to_original_picture_size.setter
    def relative_to_original_picture_size(self, value : bool):
        ...
    
    @property
    def linked_cell(self) -> str:
        ...
    
    @linked_cell.setter
    def linked_cell(self, value : str):
        ...
    
    @property
    def input_range(self) -> str:
        ...
    
    @input_range.setter
    def input_range(self, value : str):
        ...
    
    @property
    def text_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @text_shape_type.setter
    def text_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def text_body(self) -> aspose.cells.drawing.texts.FontSettingCollection:
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Represents the font of shape.'''
        ...
    
    @font.setter
    def font(self, value : aspose.cells.Font):
        '''Represents the font of shape.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    @text_options.setter
    def text_options(self, value : aspose.cells.drawing.texts.TextOptions):
        ...
    
    @property
    def text(self) -> str:
        '''Represents the string in this TextBox object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Represents the string in this TextBox object.'''
        ...
    
    @property
    def is_rich_text(self) -> bool:
        ...
    
    @property
    def html_text(self) -> str:
        ...
    
    @html_text.setter
    def html_text(self, value : str):
        ...
    
    @property
    def text_vertical_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_vertical_overflow.setter
    def text_vertical_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def text_horizontal_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_horizontal_overflow.setter
    def text_horizontal_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
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
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def control_data(self) -> bytes:
        ...
    
    @property
    def active_x_control(self) -> aspose.cells.drawing.activexcontrols.ActiveXControl:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets the paths of a custom geometric shape.'''
        ...
    
    @property
    def geometry(self) -> aspose.cells.drawing.Geometry:
        '''Gets the geometry'''
        ...
    
    @property
    def create_id(self) -> Guid:
        ...
    
    @create_id.setter
    def create_id(self, value : Guid):
        ...
    
    @property
    def is_auto_size(self) -> bool:
        ...
    
    @is_auto_size.setter
    def is_auto_size(self, value : bool):
        ...
    
    @property
    def is_link(self) -> bool:
        ...
    
    @is_link.setter
    def is_link(self, value : bool):
        ...
    
    @property
    def display_as_icon(self) -> bool:
        ...
    
    @display_as_icon.setter
    def display_as_icon(self, value : bool):
        ...
    
    @property
    def image_data(self) -> bytes:
        ...
    
    @image_data.setter
    def image_data(self, value : bytes):
        ...
    
    @property
    def object_data(self) -> bytes:
        ...
    
    @object_data.setter
    def object_data(self, value : bytes):
        ...
    
    @property
    def full_object_bin(self) -> bytes:
        ...
    
    @property
    def image_source_full_name(self) -> str:
        ...
    
    @image_source_full_name.setter
    def image_source_full_name(self, value : str):
        ...
    
    @property
    def prog_id(self) -> str:
        ...
    
    @prog_id.setter
    def prog_id(self, value : str):
        ...
    
    @property
    def file_format_type(self) -> aspose.cells.FileFormatType:
        ...
    
    @file_format_type.setter
    def file_format_type(self, value : aspose.cells.FileFormatType):
        ...
    
    @property
    def object_source_full_name(self) -> str:
        ...
    
    @object_source_full_name.setter
    def object_source_full_name(self, value : str):
        ...
    
    @property
    def label(self) -> str:
        '''Gets and sets the display label of the linked ole object.'''
        ...
    
    @label.setter
    def label(self, value : str):
        '''Gets and sets the display label of the linked ole object.'''
        ...
    
    @property
    def source_full_name(self) -> str:
        ...
    
    @source_full_name.setter
    def source_full_name(self, value : str):
        ...
    
    @property
    def auto_update(self) -> bool:
        ...
    
    @auto_update.setter
    def auto_update(self, value : bool):
        ...
    
    @property
    def auto_load(self) -> bool:
        ...
    
    @auto_load.setter
    def auto_load(self, value : bool):
        ...
    
    @property
    def class_identifier(self) -> bytes:
        ...
    
    @class_identifier.setter
    def class_identifier(self, value : bytes):
        ...
    
    @property
    def image_type(self) -> aspose.cells.drawing.ImageType:
        ...
    
    ...

class OleObjectCollection:
    '''Represents embedded OLE objects.'''
    
    @overload
    def add(self, upper_left_row : int, upper_left_column : int, height : int, width : int, image_data : bytes) -> int:
        '''Adds an OleObject to the collection.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param height: Height of oleObject, in unit of pixel.
        :param width: Width of oleObject, in unit of pixel.
        :param image_data: Image of ole object as byte array.
        :returns: :py:class:`aspose.cells.drawing.OleObject` object index.'''
        ...
    
    @overload
    def add(self, upper_left_row : int, upper_left_column : int, height : int, width : int, image_data : bytes, linked_file : str) -> int:
        '''Adds a linked OleObject to the collection.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param height: Height of oleObject, in unit of pixel.
        :param width: Width of oleObject, in unit of pixel.
        :param image_data: Image of ole object as byte array.
        :returns: :py:class:`aspose.cells.drawing.OleObject` object index.'''
        ...
    
    @overload
    def copy_to(self, array : List[aspose.cells.drawing.OleObject]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.drawing.OleObject], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.drawing.OleObject, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.drawing.OleObject, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.OleObject) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.OleObject, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.OleObject, index : int, count : int) -> int:
        ...
    
    def binary_search(self, item : aspose.cells.drawing.OleObject) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class Oval(Shape):
    '''Represents the oval shape.'''
    
    @overload
    def to_image(self, stream : io.RawIOBase, image_type : aspose.cells.drawing.ImageType):
        '''Creates the shape image and saves it to a stream in the specified format.
        
        :param stream: The output stream.
        :param image_type: The type in which to save the image.'''
        ...
    
    @overload
    def to_image(self, image_file : str, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a file.'''
        ...
    
    @overload
    def to_image(self, stream : io.RawIOBase, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a stream.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.'''
        ...
    
    def get_result_of_smart_art(self) -> aspose.cells.drawing.GroupShape:
        '''Converting smart art to grouped shapes.'''
        ...
    
    def to_front_or_back(self, orders : int):
        '''Brings the shape to the front or sends the shape to back.
        
        :param orders: If it's less than zero, sets the shape to back.
        If it's greater than zero, brings the shape to front.'''
        ...
    
    def get_locked_property(self, type : aspose.cells.drawing.ShapeLockType) -> bool:
        '''Gets the value of locked property.
        
        :param type: The type of the shape locked property.
        :returns: Returns  the value of locked property.'''
        ...
    
    def set_locked_property(self, type : aspose.cells.drawing.ShapeLockType, value : bool):
        '''Set the locked property.
        
        :param type: The locked type.
        :param value: The value of the property.'''
        ...
    
    def add_hyperlink(self, address : str) -> aspose.cells.Hyperlink:
        '''Adds a hyperlink to the shape.
        
        :param address: Address of the hyperlink.
        :returns: Return the new hyperlink object.'''
        ...
    
    def remove_hyperlink(self):
        '''Remove the hyperlink of the shape.'''
        ...
    
    def move_to_range(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int):
        '''Moves the shape to a specified range.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index'''
        ...
    
    def align_top_right_corner(self, top_row : int, right_column : int):
        '''Moves the picture to the top-right corner.
        
        :param top_row: the row index.
        :param right_column: the column index.'''
        ...
    
    def get_connection_points(self) -> List[List[float]]:
        '''Get the connection points
        
        :returns: [X,Y] pairs of the connection point. Every item is a float[2] array, [0] represents x and [1] represents y.'''
        ...
    
    def get_linked_cell(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range linked to the control's value.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range linked to the control's value.'''
        ...
    
    def set_linked_cell(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range linked to the control's value.
        
        :param formula: The range linked to the control's value.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def get_input_range(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range used to fill the control.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range used to fill the control.'''
        ...
    
    def set_input_range(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range used to fill the control.
        
        :param formula: The range used to fill the control.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell.'''
        ...
    
    def calculate_text_size(self) -> List[int]:
        '''Recalculate the text area
        
        :returns: Text's Size in an array(width and height).'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the text .
        
        :returns: All Characters objects'''
        ...
    
    def remove_active_x_control(self):
        '''Remove activeX control.'''
        ...
    
    def is_same_setting(self, obj : any) -> bool:
        '''Returns whether the shape is same.'''
        ...
    
    @property
    def macro_name(self) -> str:
        ...
    
    @macro_name.setter
    def macro_name(self, value : str):
        ...
    
    @property
    def is_equation(self) -> bool:
        ...
    
    @property
    def is_smart_art(self) -> bool:
        ...
    
    @property
    def z_order_position(self) -> int:
        ...
    
    @z_order_position.setter
    def z_order_position(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of the shape.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of the shape.'''
        ...
    
    @property
    def alternative_text(self) -> str:
        ...
    
    @alternative_text.setter
    def alternative_text(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @property
    def line_format(self) -> aspose.cells.drawing.MsoLineFormat:
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.MsoFillFormat:
        ...
    
    @property
    def format(self) -> aspose.cells.drawing.ShapeFormat:
        '''Represents the setting of the shape's formatting.'''
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        '''Gets line style'''
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        '''Returns a :py:attr:`aspose.cells.drawing.Shape.fill_format` object that contains fill formatting properties for the specified shape.'''
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def reflection(self) -> aspose.cells.drawing.ReflectionEffect:
        '''Represents a :py:class:`aspose.cells.drawing.ReflectionEffect` object that specifies reflection effect for the chart element or shape.'''
        ...
    
    @property
    def glow(self) -> aspose.cells.drawing.GlowEffect:
        '''Represents a :py:class:`aspose.cells.drawing.GlowEffect` object that specifies glow effect for the chart element or shape.'''
        ...
    
    @property
    def soft_edges(self) -> float:
        ...
    
    @soft_edges.setter
    def soft_edges(self, value : float):
        ...
    
    @property
    def three_d_format(self) -> aspose.cells.drawing.ThreeDFormat:
        ...
    
    @property
    def text_frame(self) -> aspose.cells.drawing.MsoTextFrame:
        ...
    
    @property
    def format_picture(self) -> aspose.cells.drawing.MsoFormatPicture:
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_lock_aspect_ratio(self) -> bool:
        ...
    
    @is_lock_aspect_ratio.setter
    def is_lock_aspect_ratio(self, value : bool):
        ...
    
    @property
    def rotation_angle(self) -> float:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : float):
        ...
    
    @property
    def hyperlink(self) -> aspose.cells.Hyperlink:
        '''Gets the hyperlink of the shape.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier of this shape.'''
        ...
    
    @property
    def spid(self) -> str:
        '''Specifies an optional string that an application can use to Identify the particular shape.'''
        ...
    
    @property
    def spt(self) -> int:
        '''Specifies an optional number that an application can use to associate the particular shape with a defined shape type.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.drawing.Shape.worksheet` object which contains this shape.'''
        ...
    
    @property
    def is_group(self) -> bool:
        ...
    
    @property
    def is_in_group(self) -> bool:
        ...
    
    @property
    def is_word_art(self) -> bool:
        ...
    
    @property
    def text_effect(self) -> aspose.cells.drawing.TextEffectFormat:
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_printable(self) -> bool:
        ...
    
    @is_printable.setter
    def is_printable(self, value : bool):
        ...
    
    @property
    def mso_drawing_type(self) -> aspose.cells.drawing.MsoDrawingType:
        ...
    
    @property
    def auto_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @auto_shape_type.setter
    def auto_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def anchor_type(self) -> aspose.cells.drawing.ShapeAnchorType:
        ...
    
    @anchor_type.setter
    def anchor_type(self, value : aspose.cells.drawing.ShapeAnchorType):
        ...
    
    @property
    def placement(self) -> aspose.cells.drawing.PlacementType:
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @placement.setter
    def placement(self, value : aspose.cells.drawing.PlacementType):
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @property
    def upper_left_row(self) -> int:
        ...
    
    @upper_left_row.setter
    def upper_left_row(self, value : int):
        ...
    
    @property
    def upper_delta_y(self) -> int:
        ...
    
    @upper_delta_y.setter
    def upper_delta_y(self, value : int):
        ...
    
    @property
    def upper_left_column(self) -> int:
        ...
    
    @upper_left_column.setter
    def upper_left_column(self, value : int):
        ...
    
    @property
    def upper_delta_x(self) -> int:
        ...
    
    @upper_delta_x.setter
    def upper_delta_x(self, value : int):
        ...
    
    @property
    def lower_right_row(self) -> int:
        ...
    
    @lower_right_row.setter
    def lower_right_row(self, value : int):
        ...
    
    @property
    def lower_delta_y(self) -> int:
        ...
    
    @lower_delta_y.setter
    def lower_delta_y(self, value : int):
        ...
    
    @property
    def lower_right_column(self) -> int:
        ...
    
    @lower_right_column.setter
    def lower_right_column(self, value : int):
        ...
    
    @property
    def lower_delta_x(self) -> int:
        ...
    
    @lower_delta_x.setter
    def lower_delta_x(self, value : int):
        ...
    
    @property
    def right(self) -> int:
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def width_pt(self) -> float:
        ...
    
    @width_pt.setter
    def width_pt(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def height(self) -> int:
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    @property
    def height_pt(self) -> float:
        ...
    
    @height_pt.setter
    def height_pt(self, value : float):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def left(self) -> int:
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @property
    def left_inch(self) -> float:
        ...
    
    @left_inch.setter
    def left_inch(self, value : float):
        ...
    
    @property
    def left_cm(self) -> float:
        ...
    
    @left_cm.setter
    def left_cm(self, value : float):
        ...
    
    @property
    def top(self) -> int:
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @property
    def top_inch(self) -> float:
        ...
    
    @top_inch.setter
    def top_inch(self, value : float):
        ...
    
    @property
    def top_cm(self) -> float:
        ...
    
    @top_cm.setter
    def top_cm(self, value : float):
        ...
    
    @property
    def top_to_corner(self) -> int:
        ...
    
    @top_to_corner.setter
    def top_to_corner(self, value : int):
        ...
    
    @property
    def left_to_corner(self) -> int:
        ...
    
    @left_to_corner.setter
    def left_to_corner(self, value : int):
        ...
    
    @property
    def x(self) -> int:
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @property
    def width_scale(self) -> int:
        ...
    
    @width_scale.setter
    def width_scale(self, value : int):
        ...
    
    @property
    def height_scale(self) -> int:
        ...
    
    @height_scale.setter
    def height_scale(self, value : int):
        ...
    
    @property
    def top_in_shape(self) -> int:
        ...
    
    @top_in_shape.setter
    def top_in_shape(self, value : int):
        ...
    
    @property
    def left_in_shape(self) -> int:
        ...
    
    @left_in_shape.setter
    def left_in_shape(self, value : int):
        ...
    
    @property
    def width_in_shape(self) -> int:
        ...
    
    @width_in_shape.setter
    def width_in_shape(self, value : int):
        ...
    
    @property
    def height_in_shape(self) -> int:
        ...
    
    @height_in_shape.setter
    def height_in_shape(self, value : int):
        ...
    
    @property
    def group(self) -> aspose.cells.drawing.GroupShape:
        '''Gets the group shape which contains this shape.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.AutoShapeType:
        '''Gets the auto shape type.'''
        ...
    
    @property
    def has_line(self) -> bool:
        ...
    
    @has_line.setter
    def has_line(self, value : bool):
        ...
    
    @property
    def is_filled(self) -> bool:
        ...
    
    @is_filled.setter
    def is_filled(self, value : bool):
        ...
    
    @property
    def is_flipped_horizontally(self) -> bool:
        ...
    
    @is_flipped_horizontally.setter
    def is_flipped_horizontally(self, value : bool):
        ...
    
    @property
    def is_flipped_vertically(self) -> bool:
        ...
    
    @is_flipped_vertically.setter
    def is_flipped_vertically(self, value : bool):
        ...
    
    @property
    def actual_lower_right_row(self) -> int:
        ...
    
    @property
    def connection_points(self) -> aspose.pydrawing.PointF[]:
        ...
    
    @property
    def relative_to_original_picture_size(self) -> bool:
        ...
    
    @relative_to_original_picture_size.setter
    def relative_to_original_picture_size(self, value : bool):
        ...
    
    @property
    def linked_cell(self) -> str:
        ...
    
    @linked_cell.setter
    def linked_cell(self, value : str):
        ...
    
    @property
    def input_range(self) -> str:
        ...
    
    @input_range.setter
    def input_range(self, value : str):
        ...
    
    @property
    def text_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @text_shape_type.setter
    def text_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def text_body(self) -> aspose.cells.drawing.texts.FontSettingCollection:
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Represents the font of shape.'''
        ...
    
    @font.setter
    def font(self, value : aspose.cells.Font):
        '''Represents the font of shape.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    @text_options.setter
    def text_options(self, value : aspose.cells.drawing.texts.TextOptions):
        ...
    
    @property
    def text(self) -> str:
        '''Represents the string in this TextBox object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Represents the string in this TextBox object.'''
        ...
    
    @property
    def is_rich_text(self) -> bool:
        ...
    
    @property
    def html_text(self) -> str:
        ...
    
    @html_text.setter
    def html_text(self, value : str):
        ...
    
    @property
    def text_vertical_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_vertical_overflow.setter
    def text_vertical_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def text_horizontal_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_horizontal_overflow.setter
    def text_horizontal_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
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
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def control_data(self) -> bytes:
        ...
    
    @property
    def active_x_control(self) -> aspose.cells.drawing.activexcontrols.ActiveXControl:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets the paths of a custom geometric shape.'''
        ...
    
    @property
    def geometry(self) -> aspose.cells.drawing.Geometry:
        '''Gets the geometry'''
        ...
    
    @property
    def create_id(self) -> Guid:
        ...
    
    @create_id.setter
    def create_id(self, value : Guid):
        ...
    
    ...

class PatternFill(Fill):
    '''Encapsulates the object that represents pattern fill format'''
    
    @property
    def pattern(self) -> aspose.cells.drawing.FillPattern:
        '''Gets the fill pattern type'''
        ...
    
    @pattern.setter
    def pattern(self, value : aspose.cells.drawing.FillPattern):
        '''Sets the fill pattern type'''
        ...
    
    @property
    def background_color(self) -> aspose.pydrawing.Color:
        ...
    
    @background_color.setter
    def background_color(self, value : aspose.pydrawing.Color):
        ...
    
    @property
    def background_cells_color(self) -> aspose.cells.CellsColor:
        ...
    
    @background_cells_color.setter
    def background_cells_color(self, value : aspose.cells.CellsColor):
        ...
    
    @property
    def foreground_color(self) -> aspose.pydrawing.Color:
        ...
    
    @foreground_color.setter
    def foreground_color(self, value : aspose.pydrawing.Color):
        ...
    
    @property
    def foreground_cells_color(self) -> aspose.cells.CellsColor:
        ...
    
    @foreground_cells_color.setter
    def foreground_cells_color(self, value : aspose.cells.CellsColor):
        ...
    
    @property
    def fore_transparency(self) -> float:
        ...
    
    @fore_transparency.setter
    def fore_transparency(self, value : float):
        ...
    
    @property
    def back_transparency(self) -> float:
        ...
    
    @back_transparency.setter
    def back_transparency(self, value : float):
        ...
    
    ...

class PicFormatOption:
    '''Represents picture format option'''
    
    @property
    def type(self) -> aspose.cells.drawing.FillPictureType:
        '''Gets the picture fill type.'''
        ...
    
    @type.setter
    def type(self, value : aspose.cells.drawing.FillPictureType):
        '''Sets the picture fill type.'''
        ...
    
    @property
    def scale(self) -> float:
        '''Gets how many the picture stack and scale with.'''
        ...
    
    @scale.setter
    def scale(self, value : float):
        '''Sets how many the picture stack and scale with.'''
        ...
    
    @property
    def left(self) -> float:
        '''Gets the left offset for stretching picture.'''
        ...
    
    @left.setter
    def left(self, value : float):
        '''Sets the left offset for stretching picture.'''
        ...
    
    @property
    def top(self) -> float:
        '''Gets the top offset for stretching picture.'''
        ...
    
    @top.setter
    def top(self, value : float):
        '''Sets the top offset for stretching picture.'''
        ...
    
    @property
    def bottom(self) -> float:
        '''Gets the bottom offset for stretching picture.'''
        ...
    
    @bottom.setter
    def bottom(self, value : float):
        '''Sets the bottom offset for stretching picture.'''
        ...
    
    @property
    def right(self) -> float:
        '''Gets the right offset for stretching picture.'''
        ...
    
    @right.setter
    def right(self, value : float):
        '''Sets the right offset for stretching picture.'''
        ...
    
    ...

class Picture(Shape):
    '''Encapsulates the object that represents a single picture in a spreadsheet.'''
    
    @overload
    def to_image(self, stream : io.RawIOBase, image_type : aspose.cells.drawing.ImageType):
        '''Creates the shape image and saves it to a stream in the specified format.
        
        :param stream: The output stream.
        :param image_type: The type in which to save the image.'''
        ...
    
    @overload
    def to_image(self, image_file : str, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a file.'''
        ...
    
    @overload
    def to_image(self, stream : io.RawIOBase, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a stream.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.'''
        ...
    
    def get_result_of_smart_art(self) -> aspose.cells.drawing.GroupShape:
        '''Converting smart art to grouped shapes.'''
        ...
    
    def to_front_or_back(self, orders : int):
        '''Brings the shape to the front or sends the shape to back.
        
        :param orders: If it's less than zero, sets the shape to back.
        If it's greater than zero, brings the shape to front.'''
        ...
    
    def get_locked_property(self, type : aspose.cells.drawing.ShapeLockType) -> bool:
        '''Gets the value of locked property.
        
        :param type: The type of the shape locked property.
        :returns: Returns  the value of locked property.'''
        ...
    
    def set_locked_property(self, type : aspose.cells.drawing.ShapeLockType, value : bool):
        '''Set the locked property.
        
        :param type: The locked type.
        :param value: The value of the property.'''
        ...
    
    def add_hyperlink(self, address : str) -> aspose.cells.Hyperlink:
        '''Adds a hyperlink to the shape.
        
        :param address: Address of the hyperlink.
        :returns: Return the new hyperlink object.'''
        ...
    
    def remove_hyperlink(self):
        '''Remove the hyperlink of the shape.'''
        ...
    
    def move_to_range(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int):
        '''Moves the shape to a specified range.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index'''
        ...
    
    def align_top_right_corner(self, top_row : int, right_column : int):
        '''Moves the picture to the top-right corner.
        
        :param top_row: the row index.
        :param right_column: the column index.'''
        ...
    
    def get_connection_points(self) -> List[List[float]]:
        '''Get the connection points
        
        :returns: [X,Y] pairs of the connection point. Every item is a float[2] array, [0] represents x and [1] represents y.'''
        ...
    
    def get_linked_cell(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range linked to the control's value.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range linked to the control's value.'''
        ...
    
    def set_linked_cell(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range linked to the control's value.
        
        :param formula: The range linked to the control's value.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def get_input_range(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range used to fill the control.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range used to fill the control.'''
        ...
    
    def set_input_range(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range used to fill the control.
        
        :param formula: The range used to fill the control.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell.'''
        ...
    
    def calculate_text_size(self) -> List[int]:
        '''Recalculate the text area
        
        :returns: Text's Size in an array(width and height).'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the text .
        
        :returns: All Characters objects'''
        ...
    
    def remove_active_x_control(self):
        '''Remove activeX control.'''
        ...
    
    def is_same_setting(self, obj : any) -> bool:
        '''Returns whether the shape is same.'''
        ...
    
    def copy(self, source : aspose.cells.drawing.Picture, options : aspose.cells.CopyOptions):
        '''Copy the picture.
        
        :param source: The source picture.
        :param options: The copy options.'''
        ...
    
    def move(self, upper_left_row : int, upper_left_column : int):
        '''Moves the picture to a specified location.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.'''
        ...
    
    @property
    def macro_name(self) -> str:
        ...
    
    @macro_name.setter
    def macro_name(self, value : str):
        ...
    
    @property
    def is_equation(self) -> bool:
        ...
    
    @property
    def is_smart_art(self) -> bool:
        ...
    
    @property
    def z_order_position(self) -> int:
        ...
    
    @z_order_position.setter
    def z_order_position(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of the shape.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of the shape.'''
        ...
    
    @property
    def alternative_text(self) -> str:
        ...
    
    @alternative_text.setter
    def alternative_text(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @property
    def line_format(self) -> aspose.cells.drawing.MsoLineFormat:
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.MsoFillFormat:
        ...
    
    @property
    def format(self) -> aspose.cells.drawing.ShapeFormat:
        '''Represents the setting of the shape's formatting.'''
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        '''Gets line style'''
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        '''Returns a :py:attr:`aspose.cells.drawing.Shape.fill_format` object that contains fill formatting properties for the specified shape.'''
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def reflection(self) -> aspose.cells.drawing.ReflectionEffect:
        '''Represents a :py:class:`aspose.cells.drawing.ReflectionEffect` object that specifies reflection effect for the chart element or shape.'''
        ...
    
    @property
    def glow(self) -> aspose.cells.drawing.GlowEffect:
        '''Represents a :py:class:`aspose.cells.drawing.GlowEffect` object that specifies glow effect for the chart element or shape.'''
        ...
    
    @property
    def soft_edges(self) -> float:
        ...
    
    @soft_edges.setter
    def soft_edges(self, value : float):
        ...
    
    @property
    def three_d_format(self) -> aspose.cells.drawing.ThreeDFormat:
        ...
    
    @property
    def text_frame(self) -> aspose.cells.drawing.MsoTextFrame:
        ...
    
    @property
    def format_picture(self) -> aspose.cells.drawing.MsoFormatPicture:
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_lock_aspect_ratio(self) -> bool:
        ...
    
    @is_lock_aspect_ratio.setter
    def is_lock_aspect_ratio(self, value : bool):
        ...
    
    @property
    def rotation_angle(self) -> float:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : float):
        ...
    
    @property
    def hyperlink(self) -> aspose.cells.Hyperlink:
        '''Gets the hyperlink of the shape.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier of this shape.'''
        ...
    
    @property
    def spid(self) -> str:
        '''Specifies an optional string that an application can use to Identify the particular shape.'''
        ...
    
    @property
    def spt(self) -> int:
        '''Specifies an optional number that an application can use to associate the particular shape with a defined shape type.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.drawing.Shape.worksheet` object which contains this shape.'''
        ...
    
    @property
    def is_group(self) -> bool:
        ...
    
    @property
    def is_in_group(self) -> bool:
        ...
    
    @property
    def is_word_art(self) -> bool:
        ...
    
    @property
    def text_effect(self) -> aspose.cells.drawing.TextEffectFormat:
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_printable(self) -> bool:
        ...
    
    @is_printable.setter
    def is_printable(self, value : bool):
        ...
    
    @property
    def mso_drawing_type(self) -> aspose.cells.drawing.MsoDrawingType:
        ...
    
    @property
    def auto_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @auto_shape_type.setter
    def auto_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def anchor_type(self) -> aspose.cells.drawing.ShapeAnchorType:
        ...
    
    @anchor_type.setter
    def anchor_type(self, value : aspose.cells.drawing.ShapeAnchorType):
        ...
    
    @property
    def placement(self) -> aspose.cells.drawing.PlacementType:
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @placement.setter
    def placement(self, value : aspose.cells.drawing.PlacementType):
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @property
    def upper_left_row(self) -> int:
        ...
    
    @upper_left_row.setter
    def upper_left_row(self, value : int):
        ...
    
    @property
    def upper_delta_y(self) -> int:
        ...
    
    @upper_delta_y.setter
    def upper_delta_y(self, value : int):
        ...
    
    @property
    def upper_left_column(self) -> int:
        ...
    
    @upper_left_column.setter
    def upper_left_column(self, value : int):
        ...
    
    @property
    def upper_delta_x(self) -> int:
        ...
    
    @upper_delta_x.setter
    def upper_delta_x(self, value : int):
        ...
    
    @property
    def lower_right_row(self) -> int:
        ...
    
    @lower_right_row.setter
    def lower_right_row(self, value : int):
        ...
    
    @property
    def lower_delta_y(self) -> int:
        ...
    
    @lower_delta_y.setter
    def lower_delta_y(self, value : int):
        ...
    
    @property
    def lower_right_column(self) -> int:
        ...
    
    @lower_right_column.setter
    def lower_right_column(self, value : int):
        ...
    
    @property
    def lower_delta_x(self) -> int:
        ...
    
    @lower_delta_x.setter
    def lower_delta_x(self, value : int):
        ...
    
    @property
    def right(self) -> int:
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def width_pt(self) -> float:
        ...
    
    @width_pt.setter
    def width_pt(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def height(self) -> int:
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    @property
    def height_pt(self) -> float:
        ...
    
    @height_pt.setter
    def height_pt(self, value : float):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def left(self) -> int:
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @property
    def left_inch(self) -> float:
        ...
    
    @left_inch.setter
    def left_inch(self, value : float):
        ...
    
    @property
    def left_cm(self) -> float:
        ...
    
    @left_cm.setter
    def left_cm(self, value : float):
        ...
    
    @property
    def top(self) -> int:
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @property
    def top_inch(self) -> float:
        ...
    
    @top_inch.setter
    def top_inch(self, value : float):
        ...
    
    @property
    def top_cm(self) -> float:
        ...
    
    @top_cm.setter
    def top_cm(self, value : float):
        ...
    
    @property
    def top_to_corner(self) -> int:
        ...
    
    @top_to_corner.setter
    def top_to_corner(self, value : int):
        ...
    
    @property
    def left_to_corner(self) -> int:
        ...
    
    @left_to_corner.setter
    def left_to_corner(self, value : int):
        ...
    
    @property
    def x(self) -> int:
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @property
    def width_scale(self) -> int:
        ...
    
    @width_scale.setter
    def width_scale(self, value : int):
        ...
    
    @property
    def height_scale(self) -> int:
        ...
    
    @height_scale.setter
    def height_scale(self, value : int):
        ...
    
    @property
    def top_in_shape(self) -> int:
        ...
    
    @top_in_shape.setter
    def top_in_shape(self, value : int):
        ...
    
    @property
    def left_in_shape(self) -> int:
        ...
    
    @left_in_shape.setter
    def left_in_shape(self, value : int):
        ...
    
    @property
    def width_in_shape(self) -> int:
        ...
    
    @width_in_shape.setter
    def width_in_shape(self, value : int):
        ...
    
    @property
    def height_in_shape(self) -> int:
        ...
    
    @height_in_shape.setter
    def height_in_shape(self, value : int):
        ...
    
    @property
    def group(self) -> aspose.cells.drawing.GroupShape:
        '''Gets the group shape which contains this shape.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.AutoShapeType:
        '''Gets the auto shape type.'''
        ...
    
    @property
    def has_line(self) -> bool:
        ...
    
    @has_line.setter
    def has_line(self, value : bool):
        ...
    
    @property
    def is_filled(self) -> bool:
        ...
    
    @is_filled.setter
    def is_filled(self, value : bool):
        ...
    
    @property
    def is_flipped_horizontally(self) -> bool:
        ...
    
    @is_flipped_horizontally.setter
    def is_flipped_horizontally(self, value : bool):
        ...
    
    @property
    def is_flipped_vertically(self) -> bool:
        ...
    
    @is_flipped_vertically.setter
    def is_flipped_vertically(self, value : bool):
        ...
    
    @property
    def actual_lower_right_row(self) -> int:
        ...
    
    @property
    def connection_points(self) -> aspose.pydrawing.PointF[]:
        ...
    
    @property
    def relative_to_original_picture_size(self) -> bool:
        ...
    
    @relative_to_original_picture_size.setter
    def relative_to_original_picture_size(self, value : bool):
        ...
    
    @property
    def linked_cell(self) -> str:
        ...
    
    @linked_cell.setter
    def linked_cell(self, value : str):
        ...
    
    @property
    def input_range(self) -> str:
        ...
    
    @input_range.setter
    def input_range(self, value : str):
        ...
    
    @property
    def text_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @text_shape_type.setter
    def text_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def text_body(self) -> aspose.cells.drawing.texts.FontSettingCollection:
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Represents the font of shape.'''
        ...
    
    @font.setter
    def font(self, value : aspose.cells.Font):
        '''Represents the font of shape.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    @text_options.setter
    def text_options(self, value : aspose.cells.drawing.texts.TextOptions):
        ...
    
    @property
    def text(self) -> str:
        '''Represents the string in this TextBox object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Represents the string in this TextBox object.'''
        ...
    
    @property
    def is_rich_text(self) -> bool:
        ...
    
    @property
    def html_text(self) -> str:
        ...
    
    @html_text.setter
    def html_text(self, value : str):
        ...
    
    @property
    def text_vertical_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_vertical_overflow.setter
    def text_vertical_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def text_horizontal_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_horizontal_overflow.setter
    def text_horizontal_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
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
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def control_data(self) -> bytes:
        ...
    
    @property
    def active_x_control(self) -> aspose.cells.drawing.activexcontrols.ActiveXControl:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets the paths of a custom geometric shape.'''
        ...
    
    @property
    def geometry(self) -> aspose.cells.drawing.Geometry:
        '''Gets the geometry'''
        ...
    
    @property
    def create_id(self) -> Guid:
        ...
    
    @create_id.setter
    def create_id(self, value : Guid):
        ...
    
    @property
    def original_height(self) -> int:
        ...
    
    @property
    def original_width(self) -> int:
        ...
    
    @property
    def border_line_color(self) -> aspose.pydrawing.Color:
        ...
    
    @border_line_color.setter
    def border_line_color(self, value : aspose.pydrawing.Color):
        ...
    
    @property
    def border_weight(self) -> float:
        ...
    
    @border_weight.setter
    def border_weight(self, value : float):
        ...
    
    @property
    def data(self) -> bytes:
        '''Gets the data of the picture.'''
        ...
    
    @data.setter
    def data(self, value : bytes):
        '''Gets the data of the picture.'''
        ...
    
    @property
    def source_full_name(self) -> str:
        ...
    
    @source_full_name.setter
    def source_full_name(self, value : str):
        ...
    
    @property
    def formula(self) -> str:
        '''Gets and sets the data of the formula.'''
        ...
    
    @formula.setter
    def formula(self, value : str):
        '''Gets and sets the data of the formula.'''
        ...
    
    @property
    def is_auto_size(self) -> bool:
        ...
    
    @is_auto_size.setter
    def is_auto_size(self, value : bool):
        ...
    
    @property
    def is_link(self) -> bool:
        ...
    
    @is_link.setter
    def is_link(self, value : bool):
        ...
    
    @property
    def is_dynamic_data_exchange(self) -> bool:
        ...
    
    @is_dynamic_data_exchange.setter
    def is_dynamic_data_exchange(self, value : bool):
        ...
    
    @property
    def display_as_icon(self) -> bool:
        ...
    
    @display_as_icon.setter
    def display_as_icon(self, value : bool):
        ...
    
    @property
    def image_type(self) -> aspose.cells.drawing.ImageType:
        ...
    
    @property
    def original_height_cm(self) -> float:
        ...
    
    @property
    def original_width_cm(self) -> float:
        ...
    
    @property
    def original_height_inch(self) -> float:
        ...
    
    @property
    def original_width_inch(self) -> float:
        ...
    
    @property
    def signature_line(self) -> aspose.cells.drawing.SignatureLine:
        ...
    
    @signature_line.setter
    def signature_line(self, value : aspose.cells.drawing.SignatureLine):
        ...
    
    ...

class PictureCollection:
    '''Encapsulates a collection of :py:class:`aspose.cells.drawing.Picture` objects.'''
    
    @overload
    def add(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int, stream : io.RawIOBase) -> int:
        '''Adds a picture to the collection.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index
        :param stream: Stream object which contains the image data.
        :returns: :py:class:`aspose.cells.drawing.Picture` object index.'''
        ...
    
    @overload
    def add(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int, file_name : str) -> int:
        '''Adds a picture to the collection.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index
        :param file_name: Image filename.
        :returns: :py:class:`aspose.cells.drawing.Picture` object index.'''
        ...
    
    @overload
    def add(self, upper_left_row : int, upper_left_column : int, stream : io.RawIOBase) -> int:
        '''Adds a picture to the collection.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param stream: Stream object which contains the image data.
        :returns: :py:class:`aspose.cells.drawing.Picture` object index.'''
        ...
    
    @overload
    def add(self, upper_left_row : int, upper_left_column : int, file_name : str) -> int:
        '''Adds a picture to the collection.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param file_name: Image filename.
        :returns: :py:class:`aspose.cells.drawing.Picture` object index.'''
        ...
    
    @overload
    def add(self, upper_left_row : int, upper_left_column : int, stream : io.RawIOBase, width_scale : int, height_scale : int) -> int:
        '''Adds a picture to the collection.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param stream: Stream object which contains the image data.
        :param width_scale: Scale of image width, a percentage.
        :param height_scale: Scale of image height, a percentage.
        :returns: :py:class:`aspose.cells.drawing.Picture` object index.'''
        ...
    
    @overload
    def add(self, upper_left_row : int, upper_left_column : int, file_name : str, width_scale : int, height_scale : int) -> int:
        '''Adds a picture to the collection.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param file_name: Image filename.
        :param width_scale: Scale of image width, a percentage.
        :param height_scale: Scale of image height, a percentage.
        :returns: :py:class:`aspose.cells.drawing.Picture` object index.'''
        ...
    
    @overload
    def copy_to(self, array : List[aspose.cells.drawing.Picture]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.drawing.Picture], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.drawing.Picture, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.drawing.Picture, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.Picture) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.Picture, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.Picture, index : int, count : int) -> int:
        ...
    
    def binary_search(self, item : aspose.cells.drawing.Picture) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class RadioButton(Shape):
    '''Represents a radio button.'''
    
    @overload
    def to_image(self, stream : io.RawIOBase, image_type : aspose.cells.drawing.ImageType):
        '''Creates the shape image and saves it to a stream in the specified format.
        
        :param stream: The output stream.
        :param image_type: The type in which to save the image.'''
        ...
    
    @overload
    def to_image(self, image_file : str, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a file.'''
        ...
    
    @overload
    def to_image(self, stream : io.RawIOBase, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a stream.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.'''
        ...
    
    def get_result_of_smart_art(self) -> aspose.cells.drawing.GroupShape:
        '''Converting smart art to grouped shapes.'''
        ...
    
    def to_front_or_back(self, orders : int):
        '''Brings the shape to the front or sends the shape to back.
        
        :param orders: If it's less than zero, sets the shape to back.
        If it's greater than zero, brings the shape to front.'''
        ...
    
    def get_locked_property(self, type : aspose.cells.drawing.ShapeLockType) -> bool:
        '''Gets the value of locked property.
        
        :param type: The type of the shape locked property.
        :returns: Returns  the value of locked property.'''
        ...
    
    def set_locked_property(self, type : aspose.cells.drawing.ShapeLockType, value : bool):
        '''Set the locked property.
        
        :param type: The locked type.
        :param value: The value of the property.'''
        ...
    
    def add_hyperlink(self, address : str) -> aspose.cells.Hyperlink:
        '''Adds a hyperlink to the shape.
        
        :param address: Address of the hyperlink.
        :returns: Return the new hyperlink object.'''
        ...
    
    def remove_hyperlink(self):
        '''Remove the hyperlink of the shape.'''
        ...
    
    def move_to_range(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int):
        '''Moves the shape to a specified range.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index'''
        ...
    
    def align_top_right_corner(self, top_row : int, right_column : int):
        '''Moves the picture to the top-right corner.
        
        :param top_row: the row index.
        :param right_column: the column index.'''
        ...
    
    def get_connection_points(self) -> List[List[float]]:
        '''Get the connection points
        
        :returns: [X,Y] pairs of the connection point. Every item is a float[2] array, [0] represents x and [1] represents y.'''
        ...
    
    def get_linked_cell(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range linked to the control's value.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range linked to the control's value.'''
        ...
    
    def set_linked_cell(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range linked to the control's value.
        
        :param formula: The range linked to the control's value.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def get_input_range(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range used to fill the control.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range used to fill the control.'''
        ...
    
    def set_input_range(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range used to fill the control.
        
        :param formula: The range used to fill the control.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell.'''
        ...
    
    def calculate_text_size(self) -> List[int]:
        '''Recalculate the text area
        
        :returns: Text's Size in an array(width and height).'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the text .
        
        :returns: All Characters objects'''
        ...
    
    def remove_active_x_control(self):
        '''Remove activeX control.'''
        ...
    
    def is_same_setting(self, obj : any) -> bool:
        '''Returns whether the shape is same.'''
        ...
    
    @property
    def macro_name(self) -> str:
        ...
    
    @macro_name.setter
    def macro_name(self, value : str):
        ...
    
    @property
    def is_equation(self) -> bool:
        ...
    
    @property
    def is_smart_art(self) -> bool:
        ...
    
    @property
    def z_order_position(self) -> int:
        ...
    
    @z_order_position.setter
    def z_order_position(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of the shape.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of the shape.'''
        ...
    
    @property
    def alternative_text(self) -> str:
        ...
    
    @alternative_text.setter
    def alternative_text(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @property
    def line_format(self) -> aspose.cells.drawing.MsoLineFormat:
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.MsoFillFormat:
        ...
    
    @property
    def format(self) -> aspose.cells.drawing.ShapeFormat:
        '''Represents the setting of the shape's formatting.'''
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        '''Gets line style'''
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        '''Returns a :py:attr:`aspose.cells.drawing.Shape.fill_format` object that contains fill formatting properties for the specified shape.'''
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def reflection(self) -> aspose.cells.drawing.ReflectionEffect:
        '''Represents a :py:class:`aspose.cells.drawing.ReflectionEffect` object that specifies reflection effect for the chart element or shape.'''
        ...
    
    @property
    def glow(self) -> aspose.cells.drawing.GlowEffect:
        '''Represents a :py:class:`aspose.cells.drawing.GlowEffect` object that specifies glow effect for the chart element or shape.'''
        ...
    
    @property
    def soft_edges(self) -> float:
        ...
    
    @soft_edges.setter
    def soft_edges(self, value : float):
        ...
    
    @property
    def three_d_format(self) -> aspose.cells.drawing.ThreeDFormat:
        ...
    
    @property
    def text_frame(self) -> aspose.cells.drawing.MsoTextFrame:
        ...
    
    @property
    def format_picture(self) -> aspose.cells.drawing.MsoFormatPicture:
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_lock_aspect_ratio(self) -> bool:
        ...
    
    @is_lock_aspect_ratio.setter
    def is_lock_aspect_ratio(self, value : bool):
        ...
    
    @property
    def rotation_angle(self) -> float:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : float):
        ...
    
    @property
    def hyperlink(self) -> aspose.cells.Hyperlink:
        '''Gets the hyperlink of the shape.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier of this shape.'''
        ...
    
    @property
    def spid(self) -> str:
        '''Specifies an optional string that an application can use to Identify the particular shape.'''
        ...
    
    @property
    def spt(self) -> int:
        '''Specifies an optional number that an application can use to associate the particular shape with a defined shape type.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.drawing.Shape.worksheet` object which contains this shape.'''
        ...
    
    @property
    def is_group(self) -> bool:
        ...
    
    @property
    def is_in_group(self) -> bool:
        ...
    
    @property
    def is_word_art(self) -> bool:
        ...
    
    @property
    def text_effect(self) -> aspose.cells.drawing.TextEffectFormat:
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_printable(self) -> bool:
        ...
    
    @is_printable.setter
    def is_printable(self, value : bool):
        ...
    
    @property
    def mso_drawing_type(self) -> aspose.cells.drawing.MsoDrawingType:
        ...
    
    @property
    def auto_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @auto_shape_type.setter
    def auto_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def anchor_type(self) -> aspose.cells.drawing.ShapeAnchorType:
        ...
    
    @anchor_type.setter
    def anchor_type(self, value : aspose.cells.drawing.ShapeAnchorType):
        ...
    
    @property
    def placement(self) -> aspose.cells.drawing.PlacementType:
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @placement.setter
    def placement(self, value : aspose.cells.drawing.PlacementType):
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @property
    def upper_left_row(self) -> int:
        ...
    
    @upper_left_row.setter
    def upper_left_row(self, value : int):
        ...
    
    @property
    def upper_delta_y(self) -> int:
        ...
    
    @upper_delta_y.setter
    def upper_delta_y(self, value : int):
        ...
    
    @property
    def upper_left_column(self) -> int:
        ...
    
    @upper_left_column.setter
    def upper_left_column(self, value : int):
        ...
    
    @property
    def upper_delta_x(self) -> int:
        ...
    
    @upper_delta_x.setter
    def upper_delta_x(self, value : int):
        ...
    
    @property
    def lower_right_row(self) -> int:
        ...
    
    @lower_right_row.setter
    def lower_right_row(self, value : int):
        ...
    
    @property
    def lower_delta_y(self) -> int:
        ...
    
    @lower_delta_y.setter
    def lower_delta_y(self, value : int):
        ...
    
    @property
    def lower_right_column(self) -> int:
        ...
    
    @lower_right_column.setter
    def lower_right_column(self, value : int):
        ...
    
    @property
    def lower_delta_x(self) -> int:
        ...
    
    @lower_delta_x.setter
    def lower_delta_x(self, value : int):
        ...
    
    @property
    def right(self) -> int:
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def width_pt(self) -> float:
        ...
    
    @width_pt.setter
    def width_pt(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def height(self) -> int:
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    @property
    def height_pt(self) -> float:
        ...
    
    @height_pt.setter
    def height_pt(self, value : float):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def left(self) -> int:
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @property
    def left_inch(self) -> float:
        ...
    
    @left_inch.setter
    def left_inch(self, value : float):
        ...
    
    @property
    def left_cm(self) -> float:
        ...
    
    @left_cm.setter
    def left_cm(self, value : float):
        ...
    
    @property
    def top(self) -> int:
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @property
    def top_inch(self) -> float:
        ...
    
    @top_inch.setter
    def top_inch(self, value : float):
        ...
    
    @property
    def top_cm(self) -> float:
        ...
    
    @top_cm.setter
    def top_cm(self, value : float):
        ...
    
    @property
    def top_to_corner(self) -> int:
        ...
    
    @top_to_corner.setter
    def top_to_corner(self, value : int):
        ...
    
    @property
    def left_to_corner(self) -> int:
        ...
    
    @left_to_corner.setter
    def left_to_corner(self, value : int):
        ...
    
    @property
    def x(self) -> int:
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @property
    def width_scale(self) -> int:
        ...
    
    @width_scale.setter
    def width_scale(self, value : int):
        ...
    
    @property
    def height_scale(self) -> int:
        ...
    
    @height_scale.setter
    def height_scale(self, value : int):
        ...
    
    @property
    def top_in_shape(self) -> int:
        ...
    
    @top_in_shape.setter
    def top_in_shape(self, value : int):
        ...
    
    @property
    def left_in_shape(self) -> int:
        ...
    
    @left_in_shape.setter
    def left_in_shape(self, value : int):
        ...
    
    @property
    def width_in_shape(self) -> int:
        ...
    
    @width_in_shape.setter
    def width_in_shape(self, value : int):
        ...
    
    @property
    def height_in_shape(self) -> int:
        ...
    
    @height_in_shape.setter
    def height_in_shape(self, value : int):
        ...
    
    @property
    def group(self) -> aspose.cells.drawing.GroupShape:
        '''Gets the group shape which contains this shape.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.AutoShapeType:
        '''Gets the auto shape type.'''
        ...
    
    @property
    def has_line(self) -> bool:
        ...
    
    @has_line.setter
    def has_line(self, value : bool):
        ...
    
    @property
    def is_filled(self) -> bool:
        ...
    
    @is_filled.setter
    def is_filled(self, value : bool):
        ...
    
    @property
    def is_flipped_horizontally(self) -> bool:
        ...
    
    @is_flipped_horizontally.setter
    def is_flipped_horizontally(self, value : bool):
        ...
    
    @property
    def is_flipped_vertically(self) -> bool:
        ...
    
    @is_flipped_vertically.setter
    def is_flipped_vertically(self, value : bool):
        ...
    
    @property
    def actual_lower_right_row(self) -> int:
        ...
    
    @property
    def connection_points(self) -> aspose.pydrawing.PointF[]:
        ...
    
    @property
    def relative_to_original_picture_size(self) -> bool:
        ...
    
    @relative_to_original_picture_size.setter
    def relative_to_original_picture_size(self, value : bool):
        ...
    
    @property
    def linked_cell(self) -> str:
        ...
    
    @linked_cell.setter
    def linked_cell(self, value : str):
        ...
    
    @property
    def input_range(self) -> str:
        ...
    
    @input_range.setter
    def input_range(self, value : str):
        ...
    
    @property
    def text_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @text_shape_type.setter
    def text_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def text_body(self) -> aspose.cells.drawing.texts.FontSettingCollection:
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Represents the font of shape.'''
        ...
    
    @font.setter
    def font(self, value : aspose.cells.Font):
        '''Represents the font of shape.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    @text_options.setter
    def text_options(self, value : aspose.cells.drawing.texts.TextOptions):
        ...
    
    @property
    def text(self) -> str:
        '''Represents the string in this TextBox object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Represents the string in this TextBox object.'''
        ...
    
    @property
    def is_rich_text(self) -> bool:
        ...
    
    @property
    def html_text(self) -> str:
        ...
    
    @html_text.setter
    def html_text(self, value : str):
        ...
    
    @property
    def text_vertical_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_vertical_overflow.setter
    def text_vertical_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def text_horizontal_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_horizontal_overflow.setter
    def text_horizontal_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
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
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def control_data(self) -> bytes:
        ...
    
    @property
    def active_x_control(self) -> aspose.cells.drawing.activexcontrols.ActiveXControl:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets the paths of a custom geometric shape.'''
        ...
    
    @property
    def geometry(self) -> aspose.cells.drawing.Geometry:
        '''Gets the geometry'''
        ...
    
    @property
    def create_id(self) -> Guid:
        ...
    
    @create_id.setter
    def create_id(self, value : Guid):
        ...
    
    @property
    def is_checked(self) -> bool:
        ...
    
    @is_checked.setter
    def is_checked(self, value : bool):
        ...
    
    @property
    def shadow(self) -> bool:
        '''Indicates whether the combobox has 3-D shading.'''
        ...
    
    @shadow.setter
    def shadow(self, value : bool):
        '''Indicates whether the combobox has 3-D shading.'''
        ...
    
    @property
    def group_box(self) -> aspose.cells.drawing.GroupBox:
        ...
    
    ...

class RectangleShape(Shape):
    '''Represents the rectangle shape.'''
    
    @overload
    def to_image(self, stream : io.RawIOBase, image_type : aspose.cells.drawing.ImageType):
        '''Creates the shape image and saves it to a stream in the specified format.
        
        :param stream: The output stream.
        :param image_type: The type in which to save the image.'''
        ...
    
    @overload
    def to_image(self, image_file : str, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a file.'''
        ...
    
    @overload
    def to_image(self, stream : io.RawIOBase, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a stream.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.'''
        ...
    
    def get_result_of_smart_art(self) -> aspose.cells.drawing.GroupShape:
        '''Converting smart art to grouped shapes.'''
        ...
    
    def to_front_or_back(self, orders : int):
        '''Brings the shape to the front or sends the shape to back.
        
        :param orders: If it's less than zero, sets the shape to back.
        If it's greater than zero, brings the shape to front.'''
        ...
    
    def get_locked_property(self, type : aspose.cells.drawing.ShapeLockType) -> bool:
        '''Gets the value of locked property.
        
        :param type: The type of the shape locked property.
        :returns: Returns  the value of locked property.'''
        ...
    
    def set_locked_property(self, type : aspose.cells.drawing.ShapeLockType, value : bool):
        '''Set the locked property.
        
        :param type: The locked type.
        :param value: The value of the property.'''
        ...
    
    def add_hyperlink(self, address : str) -> aspose.cells.Hyperlink:
        '''Adds a hyperlink to the shape.
        
        :param address: Address of the hyperlink.
        :returns: Return the new hyperlink object.'''
        ...
    
    def remove_hyperlink(self):
        '''Remove the hyperlink of the shape.'''
        ...
    
    def move_to_range(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int):
        '''Moves the shape to a specified range.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index'''
        ...
    
    def align_top_right_corner(self, top_row : int, right_column : int):
        '''Moves the picture to the top-right corner.
        
        :param top_row: the row index.
        :param right_column: the column index.'''
        ...
    
    def get_connection_points(self) -> List[List[float]]:
        '''Get the connection points
        
        :returns: [X,Y] pairs of the connection point. Every item is a float[2] array, [0] represents x and [1] represents y.'''
        ...
    
    def get_linked_cell(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range linked to the control's value.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range linked to the control's value.'''
        ...
    
    def set_linked_cell(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range linked to the control's value.
        
        :param formula: The range linked to the control's value.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def get_input_range(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range used to fill the control.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range used to fill the control.'''
        ...
    
    def set_input_range(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range used to fill the control.
        
        :param formula: The range used to fill the control.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell.'''
        ...
    
    def calculate_text_size(self) -> List[int]:
        '''Recalculate the text area
        
        :returns: Text's Size in an array(width and height).'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the text .
        
        :returns: All Characters objects'''
        ...
    
    def remove_active_x_control(self):
        '''Remove activeX control.'''
        ...
    
    def is_same_setting(self, obj : any) -> bool:
        '''Returns whether the shape is same.'''
        ...
    
    @property
    def macro_name(self) -> str:
        ...
    
    @macro_name.setter
    def macro_name(self, value : str):
        ...
    
    @property
    def is_equation(self) -> bool:
        ...
    
    @property
    def is_smart_art(self) -> bool:
        ...
    
    @property
    def z_order_position(self) -> int:
        ...
    
    @z_order_position.setter
    def z_order_position(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of the shape.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of the shape.'''
        ...
    
    @property
    def alternative_text(self) -> str:
        ...
    
    @alternative_text.setter
    def alternative_text(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @property
    def line_format(self) -> aspose.cells.drawing.MsoLineFormat:
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.MsoFillFormat:
        ...
    
    @property
    def format(self) -> aspose.cells.drawing.ShapeFormat:
        '''Represents the setting of the shape's formatting.'''
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        '''Gets line style'''
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        '''Returns a :py:attr:`aspose.cells.drawing.Shape.fill_format` object that contains fill formatting properties for the specified shape.'''
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def reflection(self) -> aspose.cells.drawing.ReflectionEffect:
        '''Represents a :py:class:`aspose.cells.drawing.ReflectionEffect` object that specifies reflection effect for the chart element or shape.'''
        ...
    
    @property
    def glow(self) -> aspose.cells.drawing.GlowEffect:
        '''Represents a :py:class:`aspose.cells.drawing.GlowEffect` object that specifies glow effect for the chart element or shape.'''
        ...
    
    @property
    def soft_edges(self) -> float:
        ...
    
    @soft_edges.setter
    def soft_edges(self, value : float):
        ...
    
    @property
    def three_d_format(self) -> aspose.cells.drawing.ThreeDFormat:
        ...
    
    @property
    def text_frame(self) -> aspose.cells.drawing.MsoTextFrame:
        ...
    
    @property
    def format_picture(self) -> aspose.cells.drawing.MsoFormatPicture:
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_lock_aspect_ratio(self) -> bool:
        ...
    
    @is_lock_aspect_ratio.setter
    def is_lock_aspect_ratio(self, value : bool):
        ...
    
    @property
    def rotation_angle(self) -> float:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : float):
        ...
    
    @property
    def hyperlink(self) -> aspose.cells.Hyperlink:
        '''Gets the hyperlink of the shape.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier of this shape.'''
        ...
    
    @property
    def spid(self) -> str:
        '''Specifies an optional string that an application can use to Identify the particular shape.'''
        ...
    
    @property
    def spt(self) -> int:
        '''Specifies an optional number that an application can use to associate the particular shape with a defined shape type.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.drawing.Shape.worksheet` object which contains this shape.'''
        ...
    
    @property
    def is_group(self) -> bool:
        ...
    
    @property
    def is_in_group(self) -> bool:
        ...
    
    @property
    def is_word_art(self) -> bool:
        ...
    
    @property
    def text_effect(self) -> aspose.cells.drawing.TextEffectFormat:
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_printable(self) -> bool:
        ...
    
    @is_printable.setter
    def is_printable(self, value : bool):
        ...
    
    @property
    def mso_drawing_type(self) -> aspose.cells.drawing.MsoDrawingType:
        ...
    
    @property
    def auto_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @auto_shape_type.setter
    def auto_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def anchor_type(self) -> aspose.cells.drawing.ShapeAnchorType:
        ...
    
    @anchor_type.setter
    def anchor_type(self, value : aspose.cells.drawing.ShapeAnchorType):
        ...
    
    @property
    def placement(self) -> aspose.cells.drawing.PlacementType:
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @placement.setter
    def placement(self, value : aspose.cells.drawing.PlacementType):
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @property
    def upper_left_row(self) -> int:
        ...
    
    @upper_left_row.setter
    def upper_left_row(self, value : int):
        ...
    
    @property
    def upper_delta_y(self) -> int:
        ...
    
    @upper_delta_y.setter
    def upper_delta_y(self, value : int):
        ...
    
    @property
    def upper_left_column(self) -> int:
        ...
    
    @upper_left_column.setter
    def upper_left_column(self, value : int):
        ...
    
    @property
    def upper_delta_x(self) -> int:
        ...
    
    @upper_delta_x.setter
    def upper_delta_x(self, value : int):
        ...
    
    @property
    def lower_right_row(self) -> int:
        ...
    
    @lower_right_row.setter
    def lower_right_row(self, value : int):
        ...
    
    @property
    def lower_delta_y(self) -> int:
        ...
    
    @lower_delta_y.setter
    def lower_delta_y(self, value : int):
        ...
    
    @property
    def lower_right_column(self) -> int:
        ...
    
    @lower_right_column.setter
    def lower_right_column(self, value : int):
        ...
    
    @property
    def lower_delta_x(self) -> int:
        ...
    
    @lower_delta_x.setter
    def lower_delta_x(self, value : int):
        ...
    
    @property
    def right(self) -> int:
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def width_pt(self) -> float:
        ...
    
    @width_pt.setter
    def width_pt(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def height(self) -> int:
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    @property
    def height_pt(self) -> float:
        ...
    
    @height_pt.setter
    def height_pt(self, value : float):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def left(self) -> int:
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @property
    def left_inch(self) -> float:
        ...
    
    @left_inch.setter
    def left_inch(self, value : float):
        ...
    
    @property
    def left_cm(self) -> float:
        ...
    
    @left_cm.setter
    def left_cm(self, value : float):
        ...
    
    @property
    def top(self) -> int:
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @property
    def top_inch(self) -> float:
        ...
    
    @top_inch.setter
    def top_inch(self, value : float):
        ...
    
    @property
    def top_cm(self) -> float:
        ...
    
    @top_cm.setter
    def top_cm(self, value : float):
        ...
    
    @property
    def top_to_corner(self) -> int:
        ...
    
    @top_to_corner.setter
    def top_to_corner(self, value : int):
        ...
    
    @property
    def left_to_corner(self) -> int:
        ...
    
    @left_to_corner.setter
    def left_to_corner(self, value : int):
        ...
    
    @property
    def x(self) -> int:
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @property
    def width_scale(self) -> int:
        ...
    
    @width_scale.setter
    def width_scale(self, value : int):
        ...
    
    @property
    def height_scale(self) -> int:
        ...
    
    @height_scale.setter
    def height_scale(self, value : int):
        ...
    
    @property
    def top_in_shape(self) -> int:
        ...
    
    @top_in_shape.setter
    def top_in_shape(self, value : int):
        ...
    
    @property
    def left_in_shape(self) -> int:
        ...
    
    @left_in_shape.setter
    def left_in_shape(self, value : int):
        ...
    
    @property
    def width_in_shape(self) -> int:
        ...
    
    @width_in_shape.setter
    def width_in_shape(self, value : int):
        ...
    
    @property
    def height_in_shape(self) -> int:
        ...
    
    @height_in_shape.setter
    def height_in_shape(self, value : int):
        ...
    
    @property
    def group(self) -> aspose.cells.drawing.GroupShape:
        '''Gets the group shape which contains this shape.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.AutoShapeType:
        '''Gets the auto shape type.'''
        ...
    
    @property
    def has_line(self) -> bool:
        ...
    
    @has_line.setter
    def has_line(self, value : bool):
        ...
    
    @property
    def is_filled(self) -> bool:
        ...
    
    @is_filled.setter
    def is_filled(self, value : bool):
        ...
    
    @property
    def is_flipped_horizontally(self) -> bool:
        ...
    
    @is_flipped_horizontally.setter
    def is_flipped_horizontally(self, value : bool):
        ...
    
    @property
    def is_flipped_vertically(self) -> bool:
        ...
    
    @is_flipped_vertically.setter
    def is_flipped_vertically(self, value : bool):
        ...
    
    @property
    def actual_lower_right_row(self) -> int:
        ...
    
    @property
    def connection_points(self) -> aspose.pydrawing.PointF[]:
        ...
    
    @property
    def relative_to_original_picture_size(self) -> bool:
        ...
    
    @relative_to_original_picture_size.setter
    def relative_to_original_picture_size(self, value : bool):
        ...
    
    @property
    def linked_cell(self) -> str:
        ...
    
    @linked_cell.setter
    def linked_cell(self, value : str):
        ...
    
    @property
    def input_range(self) -> str:
        ...
    
    @input_range.setter
    def input_range(self, value : str):
        ...
    
    @property
    def text_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @text_shape_type.setter
    def text_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def text_body(self) -> aspose.cells.drawing.texts.FontSettingCollection:
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Represents the font of shape.'''
        ...
    
    @font.setter
    def font(self, value : aspose.cells.Font):
        '''Represents the font of shape.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    @text_options.setter
    def text_options(self, value : aspose.cells.drawing.texts.TextOptions):
        ...
    
    @property
    def text(self) -> str:
        '''Represents the string in this TextBox object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Represents the string in this TextBox object.'''
        ...
    
    @property
    def is_rich_text(self) -> bool:
        ...
    
    @property
    def html_text(self) -> str:
        ...
    
    @html_text.setter
    def html_text(self, value : str):
        ...
    
    @property
    def text_vertical_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_vertical_overflow.setter
    def text_vertical_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def text_horizontal_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_horizontal_overflow.setter
    def text_horizontal_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
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
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def control_data(self) -> bytes:
        ...
    
    @property
    def active_x_control(self) -> aspose.cells.drawing.activexcontrols.ActiveXControl:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets the paths of a custom geometric shape.'''
        ...
    
    @property
    def geometry(self) -> aspose.cells.drawing.Geometry:
        '''Gets the geometry'''
        ...
    
    @property
    def create_id(self) -> Guid:
        ...
    
    @create_id.setter
    def create_id(self, value : Guid):
        ...
    
    ...

class ReflectionEffect:
    '''This class specifies a reflection effect.'''
    
    @property
    def type(self) -> aspose.cells.drawing.ReflectionEffectType:
        '''Gets and sets the preset reflection effect.'''
        ...
    
    @type.setter
    def type(self, value : aspose.cells.drawing.ReflectionEffectType):
        '''Gets and sets the preset reflection effect.'''
        ...
    
    @property
    def transparency(self) -> float:
        '''Gets and sets the degree of the starting reflection transparency as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    @transparency.setter
    def transparency(self, value : float):
        '''Gets and sets the degree of the starting reflection transparency as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    @property
    def size(self) -> float:
        '''Gets and sets the end position (along the alpha gradient ramp) of the end alpha value,in unit of percentage'''
        ...
    
    @size.setter
    def size(self, value : float):
        '''Gets and sets the end position (along the alpha gradient ramp) of the end alpha value,in unit of percentage'''
        ...
    
    @property
    def blur(self) -> float:
        '''Gets and sets the blur radius,in unit of points.'''
        ...
    
    @blur.setter
    def blur(self, value : float):
        '''Gets and sets the blur radius,in unit of points.'''
        ...
    
    @property
    def direction(self) -> float:
        '''Gets and sets the direction of the alpha gradient ramp relative to the shape itself.'''
        ...
    
    @direction.setter
    def direction(self, value : float):
        '''Gets and sets the direction of the alpha gradient ramp relative to the shape itself.'''
        ...
    
    @property
    def distance(self) -> float:
        '''Gets and sets how far to distance the shadow,in unit of points.'''
        ...
    
    @distance.setter
    def distance(self, value : float):
        '''Gets and sets how far to distance the shadow,in unit of points.'''
        ...
    
    @property
    def fade_direction(self) -> float:
        ...
    
    @fade_direction.setter
    def fade_direction(self, value : float):
        ...
    
    @property
    def rot_with_shape(self) -> bool:
        ...
    
    @rot_with_shape.setter
    def rot_with_shape(self, value : bool):
        ...
    
    ...

class ScrollBar(Shape):
    '''Represents a scroll bar object.'''
    
    @overload
    def to_image(self, stream : io.RawIOBase, image_type : aspose.cells.drawing.ImageType):
        '''Creates the shape image and saves it to a stream in the specified format.
        
        :param stream: The output stream.
        :param image_type: The type in which to save the image.'''
        ...
    
    @overload
    def to_image(self, image_file : str, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a file.'''
        ...
    
    @overload
    def to_image(self, stream : io.RawIOBase, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a stream.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.'''
        ...
    
    def get_result_of_smart_art(self) -> aspose.cells.drawing.GroupShape:
        '''Converting smart art to grouped shapes.'''
        ...
    
    def to_front_or_back(self, orders : int):
        '''Brings the shape to the front or sends the shape to back.
        
        :param orders: If it's less than zero, sets the shape to back.
        If it's greater than zero, brings the shape to front.'''
        ...
    
    def get_locked_property(self, type : aspose.cells.drawing.ShapeLockType) -> bool:
        '''Gets the value of locked property.
        
        :param type: The type of the shape locked property.
        :returns: Returns  the value of locked property.'''
        ...
    
    def set_locked_property(self, type : aspose.cells.drawing.ShapeLockType, value : bool):
        '''Set the locked property.
        
        :param type: The locked type.
        :param value: The value of the property.'''
        ...
    
    def add_hyperlink(self, address : str) -> aspose.cells.Hyperlink:
        '''Adds a hyperlink to the shape.
        
        :param address: Address of the hyperlink.
        :returns: Return the new hyperlink object.'''
        ...
    
    def remove_hyperlink(self):
        '''Remove the hyperlink of the shape.'''
        ...
    
    def move_to_range(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int):
        '''Moves the shape to a specified range.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index'''
        ...
    
    def align_top_right_corner(self, top_row : int, right_column : int):
        '''Moves the picture to the top-right corner.
        
        :param top_row: the row index.
        :param right_column: the column index.'''
        ...
    
    def get_connection_points(self) -> List[List[float]]:
        '''Get the connection points
        
        :returns: [X,Y] pairs of the connection point. Every item is a float[2] array, [0] represents x and [1] represents y.'''
        ...
    
    def get_linked_cell(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range linked to the control's value.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range linked to the control's value.'''
        ...
    
    def set_linked_cell(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range linked to the control's value.
        
        :param formula: The range linked to the control's value.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def get_input_range(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range used to fill the control.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range used to fill the control.'''
        ...
    
    def set_input_range(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range used to fill the control.
        
        :param formula: The range used to fill the control.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell.'''
        ...
    
    def calculate_text_size(self) -> List[int]:
        '''Recalculate the text area
        
        :returns: Text's Size in an array(width and height).'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the text .
        
        :returns: All Characters objects'''
        ...
    
    def remove_active_x_control(self):
        '''Remove activeX control.'''
        ...
    
    def is_same_setting(self, obj : any) -> bool:
        '''Returns whether the shape is same.'''
        ...
    
    @property
    def macro_name(self) -> str:
        ...
    
    @macro_name.setter
    def macro_name(self, value : str):
        ...
    
    @property
    def is_equation(self) -> bool:
        ...
    
    @property
    def is_smart_art(self) -> bool:
        ...
    
    @property
    def z_order_position(self) -> int:
        ...
    
    @z_order_position.setter
    def z_order_position(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of the shape.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of the shape.'''
        ...
    
    @property
    def alternative_text(self) -> str:
        ...
    
    @alternative_text.setter
    def alternative_text(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @property
    def line_format(self) -> aspose.cells.drawing.MsoLineFormat:
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.MsoFillFormat:
        ...
    
    @property
    def format(self) -> aspose.cells.drawing.ShapeFormat:
        '''Represents the setting of the shape's formatting.'''
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        '''Gets line style'''
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        '''Returns a :py:attr:`aspose.cells.drawing.Shape.fill_format` object that contains fill formatting properties for the specified shape.'''
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def reflection(self) -> aspose.cells.drawing.ReflectionEffect:
        '''Represents a :py:class:`aspose.cells.drawing.ReflectionEffect` object that specifies reflection effect for the chart element or shape.'''
        ...
    
    @property
    def glow(self) -> aspose.cells.drawing.GlowEffect:
        '''Represents a :py:class:`aspose.cells.drawing.GlowEffect` object that specifies glow effect for the chart element or shape.'''
        ...
    
    @property
    def soft_edges(self) -> float:
        ...
    
    @soft_edges.setter
    def soft_edges(self, value : float):
        ...
    
    @property
    def three_d_format(self) -> aspose.cells.drawing.ThreeDFormat:
        ...
    
    @property
    def text_frame(self) -> aspose.cells.drawing.MsoTextFrame:
        ...
    
    @property
    def format_picture(self) -> aspose.cells.drawing.MsoFormatPicture:
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_lock_aspect_ratio(self) -> bool:
        ...
    
    @is_lock_aspect_ratio.setter
    def is_lock_aspect_ratio(self, value : bool):
        ...
    
    @property
    def rotation_angle(self) -> float:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : float):
        ...
    
    @property
    def hyperlink(self) -> aspose.cells.Hyperlink:
        '''Gets the hyperlink of the shape.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier of this shape.'''
        ...
    
    @property
    def spid(self) -> str:
        '''Specifies an optional string that an application can use to Identify the particular shape.'''
        ...
    
    @property
    def spt(self) -> int:
        '''Specifies an optional number that an application can use to associate the particular shape with a defined shape type.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.drawing.Shape.worksheet` object which contains this shape.'''
        ...
    
    @property
    def is_group(self) -> bool:
        ...
    
    @property
    def is_in_group(self) -> bool:
        ...
    
    @property
    def is_word_art(self) -> bool:
        ...
    
    @property
    def text_effect(self) -> aspose.cells.drawing.TextEffectFormat:
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_printable(self) -> bool:
        ...
    
    @is_printable.setter
    def is_printable(self, value : bool):
        ...
    
    @property
    def mso_drawing_type(self) -> aspose.cells.drawing.MsoDrawingType:
        ...
    
    @property
    def auto_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @auto_shape_type.setter
    def auto_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def anchor_type(self) -> aspose.cells.drawing.ShapeAnchorType:
        ...
    
    @anchor_type.setter
    def anchor_type(self, value : aspose.cells.drawing.ShapeAnchorType):
        ...
    
    @property
    def placement(self) -> aspose.cells.drawing.PlacementType:
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @placement.setter
    def placement(self, value : aspose.cells.drawing.PlacementType):
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @property
    def upper_left_row(self) -> int:
        ...
    
    @upper_left_row.setter
    def upper_left_row(self, value : int):
        ...
    
    @property
    def upper_delta_y(self) -> int:
        ...
    
    @upper_delta_y.setter
    def upper_delta_y(self, value : int):
        ...
    
    @property
    def upper_left_column(self) -> int:
        ...
    
    @upper_left_column.setter
    def upper_left_column(self, value : int):
        ...
    
    @property
    def upper_delta_x(self) -> int:
        ...
    
    @upper_delta_x.setter
    def upper_delta_x(self, value : int):
        ...
    
    @property
    def lower_right_row(self) -> int:
        ...
    
    @lower_right_row.setter
    def lower_right_row(self, value : int):
        ...
    
    @property
    def lower_delta_y(self) -> int:
        ...
    
    @lower_delta_y.setter
    def lower_delta_y(self, value : int):
        ...
    
    @property
    def lower_right_column(self) -> int:
        ...
    
    @lower_right_column.setter
    def lower_right_column(self, value : int):
        ...
    
    @property
    def lower_delta_x(self) -> int:
        ...
    
    @lower_delta_x.setter
    def lower_delta_x(self, value : int):
        ...
    
    @property
    def right(self) -> int:
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def width_pt(self) -> float:
        ...
    
    @width_pt.setter
    def width_pt(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def height(self) -> int:
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    @property
    def height_pt(self) -> float:
        ...
    
    @height_pt.setter
    def height_pt(self, value : float):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def left(self) -> int:
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @property
    def left_inch(self) -> float:
        ...
    
    @left_inch.setter
    def left_inch(self, value : float):
        ...
    
    @property
    def left_cm(self) -> float:
        ...
    
    @left_cm.setter
    def left_cm(self, value : float):
        ...
    
    @property
    def top(self) -> int:
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @property
    def top_inch(self) -> float:
        ...
    
    @top_inch.setter
    def top_inch(self, value : float):
        ...
    
    @property
    def top_cm(self) -> float:
        ...
    
    @top_cm.setter
    def top_cm(self, value : float):
        ...
    
    @property
    def top_to_corner(self) -> int:
        ...
    
    @top_to_corner.setter
    def top_to_corner(self, value : int):
        ...
    
    @property
    def left_to_corner(self) -> int:
        ...
    
    @left_to_corner.setter
    def left_to_corner(self, value : int):
        ...
    
    @property
    def x(self) -> int:
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @property
    def width_scale(self) -> int:
        ...
    
    @width_scale.setter
    def width_scale(self, value : int):
        ...
    
    @property
    def height_scale(self) -> int:
        ...
    
    @height_scale.setter
    def height_scale(self, value : int):
        ...
    
    @property
    def top_in_shape(self) -> int:
        ...
    
    @top_in_shape.setter
    def top_in_shape(self, value : int):
        ...
    
    @property
    def left_in_shape(self) -> int:
        ...
    
    @left_in_shape.setter
    def left_in_shape(self, value : int):
        ...
    
    @property
    def width_in_shape(self) -> int:
        ...
    
    @width_in_shape.setter
    def width_in_shape(self, value : int):
        ...
    
    @property
    def height_in_shape(self) -> int:
        ...
    
    @height_in_shape.setter
    def height_in_shape(self, value : int):
        ...
    
    @property
    def group(self) -> aspose.cells.drawing.GroupShape:
        '''Gets the group shape which contains this shape.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.AutoShapeType:
        '''Gets the auto shape type.'''
        ...
    
    @property
    def has_line(self) -> bool:
        ...
    
    @has_line.setter
    def has_line(self, value : bool):
        ...
    
    @property
    def is_filled(self) -> bool:
        ...
    
    @is_filled.setter
    def is_filled(self, value : bool):
        ...
    
    @property
    def is_flipped_horizontally(self) -> bool:
        ...
    
    @is_flipped_horizontally.setter
    def is_flipped_horizontally(self, value : bool):
        ...
    
    @property
    def is_flipped_vertically(self) -> bool:
        ...
    
    @is_flipped_vertically.setter
    def is_flipped_vertically(self, value : bool):
        ...
    
    @property
    def actual_lower_right_row(self) -> int:
        ...
    
    @property
    def connection_points(self) -> aspose.pydrawing.PointF[]:
        ...
    
    @property
    def relative_to_original_picture_size(self) -> bool:
        ...
    
    @relative_to_original_picture_size.setter
    def relative_to_original_picture_size(self, value : bool):
        ...
    
    @property
    def linked_cell(self) -> str:
        ...
    
    @linked_cell.setter
    def linked_cell(self, value : str):
        ...
    
    @property
    def input_range(self) -> str:
        ...
    
    @input_range.setter
    def input_range(self, value : str):
        ...
    
    @property
    def text_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @text_shape_type.setter
    def text_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def text_body(self) -> aspose.cells.drawing.texts.FontSettingCollection:
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Represents the font of shape.'''
        ...
    
    @font.setter
    def font(self, value : aspose.cells.Font):
        '''Represents the font of shape.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    @text_options.setter
    def text_options(self, value : aspose.cells.drawing.texts.TextOptions):
        ...
    
    @property
    def text(self) -> str:
        '''Represents the string in this TextBox object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Represents the string in this TextBox object.'''
        ...
    
    @property
    def is_rich_text(self) -> bool:
        ...
    
    @property
    def html_text(self) -> str:
        ...
    
    @html_text.setter
    def html_text(self, value : str):
        ...
    
    @property
    def text_vertical_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_vertical_overflow.setter
    def text_vertical_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def text_horizontal_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_horizontal_overflow.setter
    def text_horizontal_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
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
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def control_data(self) -> bytes:
        ...
    
    @property
    def active_x_control(self) -> aspose.cells.drawing.activexcontrols.ActiveXControl:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets the paths of a custom geometric shape.'''
        ...
    
    @property
    def geometry(self) -> aspose.cells.drawing.Geometry:
        '''Gets the geometry'''
        ...
    
    @property
    def create_id(self) -> Guid:
        ...
    
    @create_id.setter
    def create_id(self, value : Guid):
        ...
    
    @property
    def current_value(self) -> int:
        ...
    
    @current_value.setter
    def current_value(self, value : int):
        ...
    
    @property
    def min(self) -> int:
        '''Gets the minimum value of a scroll bar or spinner range.'''
        ...
    
    @min.setter
    def min(self, value : int):
        '''Sets the minimum value of a scroll bar or spinner range.'''
        ...
    
    @property
    def max(self) -> int:
        '''Gets the maximum value of a scroll bar or spinner range.'''
        ...
    
    @max.setter
    def max(self, value : int):
        '''Sets the maximum value of a scroll bar or spinner range.'''
        ...
    
    @property
    def incremental_change(self) -> int:
        ...
    
    @incremental_change.setter
    def incremental_change(self, value : int):
        ...
    
    @property
    def page_change(self) -> int:
        ...
    
    @page_change.setter
    def page_change(self, value : int):
        ...
    
    @property
    def shadow(self) -> bool:
        '''Indicates whether the shape has 3-D shading.'''
        ...
    
    @shadow.setter
    def shadow(self, value : bool):
        '''Indicates whether the shape has 3-D shading.'''
        ...
    
    @property
    def is_horizontal(self) -> bool:
        ...
    
    @is_horizontal.setter
    def is_horizontal(self, value : bool):
        ...
    
    ...

class ShadowEffect:
    '''This class specifies the shadow effect of the chart element or shape.'''
    
    @property
    def preset_type(self) -> aspose.cells.drawing.PresetShadowType:
        ...
    
    @preset_type.setter
    def preset_type(self, value : aspose.cells.drawing.PresetShadowType):
        ...
    
    @property
    def color(self) -> aspose.cells.CellsColor:
        '''Gets and sets the color of the shadow.'''
        ...
    
    @color.setter
    def color(self, value : aspose.cells.CellsColor):
        '''Gets and sets the color of the shadow.'''
        ...
    
    @property
    def transparency(self) -> float:
        '''Gets and sets the degree of transparency of the shadow. Range from 0.0 (opaque) to 1.0 (clear).'''
        ...
    
    @transparency.setter
    def transparency(self, value : float):
        '''Gets and sets the degree of transparency of the shadow. Range from 0.0 (opaque) to 1.0 (clear).'''
        ...
    
    @property
    def size(self) -> float:
        '''Gets and sets the size of the shadow. Range from 0 to 2.0.
        Meaningless in inner shadow.'''
        ...
    
    @size.setter
    def size(self, value : float):
        '''Gets and sets the size of the shadow. Range from 0 to 2.0.
        Meaningless in inner shadow.'''
        ...
    
    @property
    def blur(self) -> float:
        '''Gets and sets the blur of the shadow. Range from 0 to 100 points.'''
        ...
    
    @blur.setter
    def blur(self, value : float):
        '''Gets and sets the blur of the shadow. Range from 0 to 100 points.'''
        ...
    
    @property
    def angle(self) -> float:
        '''Gets and sets the lighting angle. Range from 0 to 359.9 degrees.'''
        ...
    
    @angle.setter
    def angle(self, value : float):
        '''Gets and sets the lighting angle. Range from 0 to 359.9 degrees.'''
        ...
    
    @property
    def distance(self) -> float:
        '''Gets and sets the distance of the shadow. Range from 0 to 200 points.'''
        ...
    
    @distance.setter
    def distance(self, value : float):
        '''Gets and sets the distance of the shadow. Range from 0 to 200 points.'''
        ...
    
    ...

class Shape:
    '''Represents the msodrawing object.'''
    
    @overload
    def to_image(self, stream : io.RawIOBase, image_type : aspose.cells.drawing.ImageType):
        '''Creates the shape image and saves it to a stream in the specified format.
        
        :param stream: The output stream.
        :param image_type: The type in which to save the image.'''
        ...
    
    @overload
    def to_image(self, image_file : str, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a file.'''
        ...
    
    @overload
    def to_image(self, stream : io.RawIOBase, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a stream.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.'''
        ...
    
    def get_result_of_smart_art(self) -> aspose.cells.drawing.GroupShape:
        '''Converting smart art to grouped shapes.'''
        ...
    
    def to_front_or_back(self, orders : int):
        '''Brings the shape to the front or sends the shape to back.
        
        :param orders: If it's less than zero, sets the shape to back.
        If it's greater than zero, brings the shape to front.'''
        ...
    
    def get_locked_property(self, type : aspose.cells.drawing.ShapeLockType) -> bool:
        '''Gets the value of locked property.
        
        :param type: The type of the shape locked property.
        :returns: Returns  the value of locked property.'''
        ...
    
    def set_locked_property(self, type : aspose.cells.drawing.ShapeLockType, value : bool):
        '''Set the locked property.
        
        :param type: The locked type.
        :param value: The value of the property.'''
        ...
    
    def add_hyperlink(self, address : str) -> aspose.cells.Hyperlink:
        '''Adds a hyperlink to the shape.
        
        :param address: Address of the hyperlink.
        :returns: Return the new hyperlink object.'''
        ...
    
    def remove_hyperlink(self):
        '''Remove the hyperlink of the shape.'''
        ...
    
    def move_to_range(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int):
        '''Moves the shape to a specified range.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index'''
        ...
    
    def align_top_right_corner(self, top_row : int, right_column : int):
        '''Moves the picture to the top-right corner.
        
        :param top_row: the row index.
        :param right_column: the column index.'''
        ...
    
    def get_connection_points(self) -> List[List[float]]:
        '''Get the connection points
        
        :returns: [X,Y] pairs of the connection point. Every item is a float[2] array, [0] represents x and [1] represents y.'''
        ...
    
    def get_linked_cell(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range linked to the control's value.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range linked to the control's value.'''
        ...
    
    def set_linked_cell(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range linked to the control's value.
        
        :param formula: The range linked to the control's value.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def get_input_range(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range used to fill the control.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range used to fill the control.'''
        ...
    
    def set_input_range(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range used to fill the control.
        
        :param formula: The range used to fill the control.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell.'''
        ...
    
    def calculate_text_size(self) -> List[int]:
        '''Recalculate the text area
        
        :returns: Text's Size in an array(width and height).'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the text .
        
        :returns: All Characters objects'''
        ...
    
    def remove_active_x_control(self):
        '''Remove activeX control.'''
        ...
    
    def is_same_setting(self, obj : any) -> bool:
        '''Returns whether the shape is same.'''
        ...
    
    @property
    def macro_name(self) -> str:
        ...
    
    @macro_name.setter
    def macro_name(self, value : str):
        ...
    
    @property
    def is_equation(self) -> bool:
        ...
    
    @property
    def is_smart_art(self) -> bool:
        ...
    
    @property
    def z_order_position(self) -> int:
        ...
    
    @z_order_position.setter
    def z_order_position(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of the shape.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of the shape.'''
        ...
    
    @property
    def alternative_text(self) -> str:
        ...
    
    @alternative_text.setter
    def alternative_text(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @property
    def line_format(self) -> aspose.cells.drawing.MsoLineFormat:
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.MsoFillFormat:
        ...
    
    @property
    def format(self) -> aspose.cells.drawing.ShapeFormat:
        '''Represents the setting of the shape's formatting.'''
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        '''Gets line style'''
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        '''Returns a :py:attr:`aspose.cells.drawing.Shape.fill_format` object that contains fill formatting properties for the specified shape.'''
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def reflection(self) -> aspose.cells.drawing.ReflectionEffect:
        '''Represents a :py:class:`aspose.cells.drawing.ReflectionEffect` object that specifies reflection effect for the chart element or shape.'''
        ...
    
    @property
    def glow(self) -> aspose.cells.drawing.GlowEffect:
        '''Represents a :py:class:`aspose.cells.drawing.GlowEffect` object that specifies glow effect for the chart element or shape.'''
        ...
    
    @property
    def soft_edges(self) -> float:
        ...
    
    @soft_edges.setter
    def soft_edges(self, value : float):
        ...
    
    @property
    def three_d_format(self) -> aspose.cells.drawing.ThreeDFormat:
        ...
    
    @property
    def text_frame(self) -> aspose.cells.drawing.MsoTextFrame:
        ...
    
    @property
    def format_picture(self) -> aspose.cells.drawing.MsoFormatPicture:
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_lock_aspect_ratio(self) -> bool:
        ...
    
    @is_lock_aspect_ratio.setter
    def is_lock_aspect_ratio(self, value : bool):
        ...
    
    @property
    def rotation_angle(self) -> float:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : float):
        ...
    
    @property
    def hyperlink(self) -> aspose.cells.Hyperlink:
        '''Gets the hyperlink of the shape.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier of this shape.'''
        ...
    
    @property
    def spid(self) -> str:
        '''Specifies an optional string that an application can use to Identify the particular shape.'''
        ...
    
    @property
    def spt(self) -> int:
        '''Specifies an optional number that an application can use to associate the particular shape with a defined shape type.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.drawing.Shape.worksheet` object which contains this shape.'''
        ...
    
    @property
    def is_group(self) -> bool:
        ...
    
    @property
    def is_in_group(self) -> bool:
        ...
    
    @property
    def is_word_art(self) -> bool:
        ...
    
    @property
    def text_effect(self) -> aspose.cells.drawing.TextEffectFormat:
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_printable(self) -> bool:
        ...
    
    @is_printable.setter
    def is_printable(self, value : bool):
        ...
    
    @property
    def mso_drawing_type(self) -> aspose.cells.drawing.MsoDrawingType:
        ...
    
    @property
    def auto_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @auto_shape_type.setter
    def auto_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def anchor_type(self) -> aspose.cells.drawing.ShapeAnchorType:
        ...
    
    @anchor_type.setter
    def anchor_type(self, value : aspose.cells.drawing.ShapeAnchorType):
        ...
    
    @property
    def placement(self) -> aspose.cells.drawing.PlacementType:
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @placement.setter
    def placement(self, value : aspose.cells.drawing.PlacementType):
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @property
    def upper_left_row(self) -> int:
        ...
    
    @upper_left_row.setter
    def upper_left_row(self, value : int):
        ...
    
    @property
    def upper_delta_y(self) -> int:
        ...
    
    @upper_delta_y.setter
    def upper_delta_y(self, value : int):
        ...
    
    @property
    def upper_left_column(self) -> int:
        ...
    
    @upper_left_column.setter
    def upper_left_column(self, value : int):
        ...
    
    @property
    def upper_delta_x(self) -> int:
        ...
    
    @upper_delta_x.setter
    def upper_delta_x(self, value : int):
        ...
    
    @property
    def lower_right_row(self) -> int:
        ...
    
    @lower_right_row.setter
    def lower_right_row(self, value : int):
        ...
    
    @property
    def lower_delta_y(self) -> int:
        ...
    
    @lower_delta_y.setter
    def lower_delta_y(self, value : int):
        ...
    
    @property
    def lower_right_column(self) -> int:
        ...
    
    @lower_right_column.setter
    def lower_right_column(self, value : int):
        ...
    
    @property
    def lower_delta_x(self) -> int:
        ...
    
    @lower_delta_x.setter
    def lower_delta_x(self, value : int):
        ...
    
    @property
    def right(self) -> int:
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def width_pt(self) -> float:
        ...
    
    @width_pt.setter
    def width_pt(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def height(self) -> int:
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    @property
    def height_pt(self) -> float:
        ...
    
    @height_pt.setter
    def height_pt(self, value : float):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def left(self) -> int:
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @property
    def left_inch(self) -> float:
        ...
    
    @left_inch.setter
    def left_inch(self, value : float):
        ...
    
    @property
    def left_cm(self) -> float:
        ...
    
    @left_cm.setter
    def left_cm(self, value : float):
        ...
    
    @property
    def top(self) -> int:
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @property
    def top_inch(self) -> float:
        ...
    
    @top_inch.setter
    def top_inch(self, value : float):
        ...
    
    @property
    def top_cm(self) -> float:
        ...
    
    @top_cm.setter
    def top_cm(self, value : float):
        ...
    
    @property
    def top_to_corner(self) -> int:
        ...
    
    @top_to_corner.setter
    def top_to_corner(self, value : int):
        ...
    
    @property
    def left_to_corner(self) -> int:
        ...
    
    @left_to_corner.setter
    def left_to_corner(self, value : int):
        ...
    
    @property
    def x(self) -> int:
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @property
    def width_scale(self) -> int:
        ...
    
    @width_scale.setter
    def width_scale(self, value : int):
        ...
    
    @property
    def height_scale(self) -> int:
        ...
    
    @height_scale.setter
    def height_scale(self, value : int):
        ...
    
    @property
    def top_in_shape(self) -> int:
        ...
    
    @top_in_shape.setter
    def top_in_shape(self, value : int):
        ...
    
    @property
    def left_in_shape(self) -> int:
        ...
    
    @left_in_shape.setter
    def left_in_shape(self, value : int):
        ...
    
    @property
    def width_in_shape(self) -> int:
        ...
    
    @width_in_shape.setter
    def width_in_shape(self, value : int):
        ...
    
    @property
    def height_in_shape(self) -> int:
        ...
    
    @height_in_shape.setter
    def height_in_shape(self, value : int):
        ...
    
    @property
    def group(self) -> aspose.cells.drawing.GroupShape:
        '''Gets the group shape which contains this shape.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.AutoShapeType:
        '''Gets the auto shape type.'''
        ...
    
    @property
    def has_line(self) -> bool:
        ...
    
    @has_line.setter
    def has_line(self, value : bool):
        ...
    
    @property
    def is_filled(self) -> bool:
        ...
    
    @is_filled.setter
    def is_filled(self, value : bool):
        ...
    
    @property
    def is_flipped_horizontally(self) -> bool:
        ...
    
    @is_flipped_horizontally.setter
    def is_flipped_horizontally(self, value : bool):
        ...
    
    @property
    def is_flipped_vertically(self) -> bool:
        ...
    
    @is_flipped_vertically.setter
    def is_flipped_vertically(self, value : bool):
        ...
    
    @property
    def actual_lower_right_row(self) -> int:
        ...
    
    @property
    def connection_points(self) -> aspose.pydrawing.PointF[]:
        ...
    
    @property
    def relative_to_original_picture_size(self) -> bool:
        ...
    
    @relative_to_original_picture_size.setter
    def relative_to_original_picture_size(self, value : bool):
        ...
    
    @property
    def linked_cell(self) -> str:
        ...
    
    @linked_cell.setter
    def linked_cell(self, value : str):
        ...
    
    @property
    def input_range(self) -> str:
        ...
    
    @input_range.setter
    def input_range(self, value : str):
        ...
    
    @property
    def text_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @text_shape_type.setter
    def text_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def text_body(self) -> aspose.cells.drawing.texts.FontSettingCollection:
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Represents the font of shape.'''
        ...
    
    @font.setter
    def font(self, value : aspose.cells.Font):
        '''Represents the font of shape.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    @text_options.setter
    def text_options(self, value : aspose.cells.drawing.texts.TextOptions):
        ...
    
    @property
    def text(self) -> str:
        '''Represents the string in this TextBox object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Represents the string in this TextBox object.'''
        ...
    
    @property
    def is_rich_text(self) -> bool:
        ...
    
    @property
    def html_text(self) -> str:
        ...
    
    @html_text.setter
    def html_text(self, value : str):
        ...
    
    @property
    def text_vertical_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_vertical_overflow.setter
    def text_vertical_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def text_horizontal_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_horizontal_overflow.setter
    def text_horizontal_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
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
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def control_data(self) -> bytes:
        ...
    
    @property
    def active_x_control(self) -> aspose.cells.drawing.activexcontrols.ActiveXControl:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets the paths of a custom geometric shape.'''
        ...
    
    @property
    def geometry(self) -> aspose.cells.drawing.Geometry:
        '''Gets the geometry'''
        ...
    
    @property
    def create_id(self) -> Guid:
        ...
    
    @create_id.setter
    def create_id(self, value : Guid):
        ...
    
    ...

class ShapeCollection:
    '''Represents all the shape in a worksheet/chart.'''
    
    @overload
    def add_shape_in_chart(self, type : aspose.cells.drawing.MsoDrawingType, placement : aspose.cells.drawing.PlacementType, left : int, top : int, right : int, bottom : int, image_data : bytes) -> aspose.cells.drawing.Shape:
        '''Add a shape to chart .All unit is 1/4000 of chart area.
        
        :param type: The drawing type.
        :param placement: the placement type.
        :param left: In unit of 1/4000 chart area width.
        :param top: In unit of 1/4000 chart area height.
        :param right: In unit of 1/4000 chart area width.
        :param bottom: In unit of 1/4000 chart area height.
        :param image_data: If the shape is not a picture or ole object,imageData should be null.'''
        ...
    
    @overload
    def add_shape_in_chart(self, type : aspose.cells.drawing.MsoDrawingType, placement : aspose.cells.drawing.PlacementType, left : int, top : int, right : int, bottom : int) -> aspose.cells.drawing.Shape:
        '''Add a shape to chart .All unit is 1/4000 of chart area.
        
        :param type: The drawing type.
        :param placement: the placement type.
        :param left: In unit of 1/4000 chart area width.
        :param top: In unit of 1/4000 chart area height.
        :param right: In unit of 1/4000 chart area width.
        :param bottom: In unit of 1/4000 chart area height.'''
        ...
    
    @overload
    def add_shape_in_chart_by_scale(self, type : aspose.cells.drawing.MsoDrawingType, placement : aspose.cells.drawing.PlacementType, left : float, top : float, right : float, bottom : float) -> aspose.cells.drawing.Shape:
        '''Add a shape to chart. All unit is percent scale of chart area.
        
        :param type: The drawing type.
        :param placement: the placement type.
        :param left: Unit is percent scale of chart area width.
        :param top: Unit is percent scale of chart area height.
        :param right: Unit is percent scale of chart area width.
        :param bottom: Unit is percent scale of chart area height.'''
        ...
    
    @overload
    def add_shape_in_chart_by_scale(self, type : aspose.cells.drawing.MsoDrawingType, placement : aspose.cells.drawing.PlacementType, left : float, top : float, right : float, bottom : float, image_data : bytes) -> aspose.cells.drawing.Shape:
        '''Add a shape to chart .All unit is 1/4000 of chart area.
        
        :param type: The drawing type.
        :param placement: the placement type.
        :param left: Unit is percent scale of chart area width.
        :param top: Unit is percent scale of chart area height.
        :param right: Unit is percent scale of chart area width.
        :param bottom: Unit is percent scale of chart area height.
        :param image_data: If the shape is not a picture or ole object,imageData should be null.'''
        ...
    
    @overload
    def add_picture(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int, stream : io.RawIOBase) -> aspose.cells.drawing.Picture:
        '''Adds a picture to the collection.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index
        :param stream: Stream object which contains the image data.
        :returns: :py:class:`aspose.cells.drawing.Picture` Picture object.'''
        ...
    
    @overload
    def add_picture(self, upper_left_row : int, upper_left_column : int, stream : io.RawIOBase, width_scale : int, height_scale : int) -> aspose.cells.drawing.Picture:
        '''Adds a picture to the collection.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param stream: Stream object which contains the image data.
        :param width_scale: Scale of image width, a percentage.
        :param height_scale: Scale of image height, a percentage.
        :returns: :py:class:`aspose.cells.drawing.Picture` Picture object.'''
        ...
    
    @overload
    def copy_to(self, array : List[aspose.cells.drawing.Shape]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.drawing.Shape], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.drawing.Shape, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.drawing.Shape, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.Shape) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.Shape, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.Shape, index : int, count : int) -> int:
        ...
    
    def add_copy(self, source_shape : aspose.cells.drawing.Shape, upper_left_row : int, top : int, upper_left_column : int, left : int) -> aspose.cells.drawing.Shape:
        '''Adds and copy a shape to the worksheet.
        
        :param source_shape: Source shape.
        :param upper_left_row: Upper left row index.
        :param top: Represents the vertical  offset of checkbox from its left row, in unit of pixel.
        :param upper_left_column: Upper left column index.
        :param left: Represents the horizontal offset of textbox from its left column, in unit of pixel.
        :returns: The new shape object index.'''
        ...
    
    def add_check_box(self, upper_left_row : int, top : int, upper_left_column : int, left : int, height : int, width : int) -> aspose.cells.drawing.CheckBox:
        '''Adds a checkbox to the worksheet.
        
        :param upper_left_row: Upper left row index.
        :param top: Represents the vertical  offset of checkbox from its left row, in unit of pixel.
        :param upper_left_column: Upper left column index.
        :param left: Represents the horizontal offset of textbox from its left column, in unit of pixel.
        :param height: Height of textbox, in unit of pixel.
        :param width: Width of textbox, in unit of pixel.
        :returns: The new CheckBox object index.'''
        ...
    
    def add_text_box(self, upper_left_row : int, top : int, upper_left_column : int, left : int, height : int, width : int) -> aspose.cells.drawing.TextBox:
        '''Adds a text box to the worksheet.
        
        :param upper_left_row: Upper left row index.
        :param top: Represents the vertical  offset of textbox from its left row, in unit of pixel.
        :param upper_left_column: Upper left column index.
        :param left: Represents the horizontal offset of textbox from its left column, in unit of pixel.
        :param height: Represents the height of textbox, in unit of pixel.
        :param width: Represents the width of textbox, in unit of pixel.
        :returns: A :py:class:`aspose.cells.drawing.TextBox` object.'''
        ...
    
    def add_equation(self, upper_left_row : int, top : int, upper_left_column : int, left : int, height : int, width : int) -> aspose.cells.drawing.TextBox:
        '''Add an equation object to the worksheet.'''
        ...
    
    def add_spinner(self, upper_left_row : int, top : int, upper_left_column : int, left : int, height : int, width : int) -> aspose.cells.drawing.Spinner:
        '''Adds a Spinner to the worksheet.
        
        :param upper_left_row: Upper left row index.
        :param top: Represents the vertical  offset of Spinner from its left row, in unit of pixel.
        :param upper_left_column: Upper left column index.
        :param left: Represents the horizontal offset of Spinner from its left column, in unit of pixel.
        :param height: Represents the height of Spinner, in unit of pixel.
        :param width: Represents the width of Spinner, in unit of pixel.
        :returns: A Spinner object.'''
        ...
    
    def add_scroll_bar(self, upper_left_row : int, top : int, upper_left_column : int, left : int, height : int, width : int) -> aspose.cells.drawing.ScrollBar:
        '''Adds a ScrollBar to the worksheet.
        
        :param upper_left_row: Upper left row index.
        :param top: Represents the vertical  offset of ScrollBar from its left row, in unit of pixel.
        :param upper_left_column: Upper left column index.
        :param left: Represents the horizontal offset of ScrollBar from its left column, in unit of pixel.
        :param height: Represents the height of ScrollBar, in unit of pixel.
        :param width: Represents the width of ScrollBar, in unit of pixel.
        :returns: A ScrollBar object.'''
        ...
    
    def add_radio_button(self, upper_left_row : int, top : int, upper_left_column : int, left : int, height : int, width : int) -> aspose.cells.drawing.RadioButton:
        '''Adds a RadioButton to the worksheet.
        
        :param upper_left_row: Upper left row index.
        :param top: Represents the vertical  offset of RadioButton from its left row, in unit of pixel.
        :param upper_left_column: Upper left column index.
        :param left: Represents the horizontal offset of RadioButton from its left column, in unit of pixel.
        :param height: Represents the height of RadioButton, in unit of pixel.
        :param width: Represents the width of RadioButton, in unit of pixel.
        :returns: A RadioButton object.'''
        ...
    
    def add_list_box(self, upper_left_row : int, top : int, upper_left_column : int, left : int, height : int, width : int) -> aspose.cells.drawing.ListBox:
        '''Adds a ListBox to the worksheet.
        
        :param upper_left_row: Upper left row index.
        :param top: Represents the vertical  offset of ListBox from its left row, in unit of pixel.
        :param upper_left_column: Upper left column index.
        :param left: Represents the horizontal offset of ListBox from its left column, in unit of pixel.
        :param height: Represents the height of ListBox, in unit of pixel.
        :param width: Represents the width of ListBox, in unit of pixel.
        :returns: A ListBox object.'''
        ...
    
    def add_combo_box(self, upper_left_row : int, top : int, upper_left_column : int, left : int, height : int, width : int) -> aspose.cells.drawing.ComboBox:
        '''Adds a ComboBox to the worksheet.
        
        :param upper_left_row: Upper left row index.
        :param top: Represents the vertical  offset of ComboBox from its left row, in unit of pixel.
        :param upper_left_column: Upper left column index.
        :param left: Represents the horizontal offset of ComboBox from its left column, in unit of pixel.
        :param height: Represents the height of ComboBox, in unit of pixel.
        :param width: Represents the width of ComboBox, in unit of pixel.
        :returns: A ComboBox object.'''
        ...
    
    def add_group_box(self, upper_left_row : int, top : int, upper_left_column : int, left : int, height : int, width : int) -> aspose.cells.drawing.GroupBox:
        '''Adds a GroupBox to the worksheet.
        
        :param upper_left_row: Upper left row index.
        :param top: Represents the vertical  offset of GroupBox from its left row, in unit of pixel.
        :param upper_left_column: Upper left column index.
        :param left: Represents the horizontal offset of GroupBox from its left column, in unit of pixel.
        :param height: Represents the height of GroupBox, in unit of pixel.
        :param width: Represents the width of GroupBox, in unit of pixel.
        :returns: A GroupBox object.'''
        ...
    
    def add_button(self, upper_left_row : int, top : int, upper_left_column : int, left : int, height : int, width : int) -> aspose.cells.drawing.Button:
        '''Adds a Button to the worksheet.
        
        :param upper_left_row: Upper left row index.
        :param top: Represents the vertical  offset of Button from its left row, in unit of pixel.
        :param upper_left_column: Upper left column index.
        :param left: Represents the horizontal offset of Button from its left column, in unit of pixel.
        :param height: Represents the height of Button, in unit of pixel.
        :param width: Represents the width of Button, in unit of pixel.
        :returns: A Button object.'''
        ...
    
    def add_label(self, upper_left_row : int, top : int, upper_left_column : int, left : int, height : int, width : int) -> aspose.cells.drawing.Label:
        '''Adds a Label to the worksheet.
        
        :param upper_left_row: Upper left row index.
        :param top: Represents the vertical  offset of Label from its left row, in unit of pixel.
        :param upper_left_column: Upper left column index.
        :param left: Represents the horizontal offset of Label from its left column, in unit of pixel.
        :param height: Represents the height of Label, in unit of pixel.
        :param width: Represents the width of Label, in unit of pixel.
        :returns: A Label object.'''
        ...
    
    def add_label_in_chart(self, top : int, left : int, height : int, width : int) -> aspose.cells.drawing.Label:
        '''Adds a label to the chart.
        
        :param top: Represents the vertical offset of label from the upper left corner in units of 1/4000 of the chart area.
        :param left: Represents the vertical offset of label from the upper left corner in units of 1/4000 of the chart area.
        :param height: Represents the height of label, in units of 1/4000 of the chart area.
        :param width: Represents the width of label, in units of 1/4000 of the chart area.
        :returns: A new Label object.'''
        ...
    
    def add_text_box_in_chart(self, top : int, left : int, height : int, width : int) -> aspose.cells.drawing.TextBox:
        '''Adds a textbox to the chart.
        
        :param top: Represents the vertical offset of textbox from the upper left corner in units of 1/4000 of the chart area.
        :param left: Represents the vertical offset of textbox from the upper left corner in units of 1/4000 of the chart area.
        :param height: Represents the height of textbox, in units of 1/4000 of the chart area.
        :param width: Represents the width of textbox, in units of 1/4000 of the chart area.
        :returns: A TextBox object.'''
        ...
    
    def add_text_effect_in_chart(self, effect : aspose.cells.drawing.MsoPresetTextEffect, text : str, font_name : str, size : int, font_bold : bool, font_italic : bool, top : int, left : int, height : int, width : int) -> aspose.cells.drawing.Shape:
        '''Inserts a WordArt object to the chart
        
        :param effect: The mso preset text effect type.
        :param text: The WordArt text.
        :param font_name: The font name.
        :param size: The font size
        :param font_bold: Indicates whether font is bold.
        :param font_italic: Indicates whether font is italic.
        :param top: Represents the vertical offset of shape from the upper left corner in units of 1/4000 of the chart area.
        :param left: Represents the vertical offset of shape from the upper left corner in units of 1/4000 of the chart area.
        :param height: Represents the height of shape, in units of 1/4000 of the chart area.
        :param width: Represents the width of shape, in units of 1/4000 of the chart area.
        :returns: Returns a Shape object that represents the new WordArt object.'''
        ...
    
    def add_text_effect(self, effect : aspose.cells.drawing.MsoPresetTextEffect, text : str, font_name : str, size : int, font_bold : bool, font_italic : bool, upper_left_row : int, top : int, upper_left_column : int, left : int, height : int, width : int) -> aspose.cells.drawing.Shape:
        '''Inserts a WordArt object.
        
        :param effect: The mso preset text effect type.
        :param text: The WordArt text.
        :param font_name: The font name.
        :param size: The font size
        :param font_bold: Indicates whether font is bold.
        :param font_italic: Indicates whether font is italic.
        :param upper_left_row: Upper left row index.
        :param top: Represents the vertical  offset of shape from its left row, in unit of pixel.
        :param upper_left_column: Upper left column index.
        :param left: Represents the horizontal offset of shape from its left column, in unit of pixel.
        :param height: Represents the height of shape, in unit of pixel.
        :param width: Represents the width of shape, in unit of pixel.
        :returns: Returns a Shape object that represents the new WordArt object.'''
        ...
    
    def add_word_art(self, style : aspose.cells.drawing.PresetWordArtStyle, text : str, upper_left_row : int, top : int, upper_left_column : int, left : int, height : int, width : int) -> aspose.cells.drawing.Shape:
        '''Adds preset WordArt since Excel 2007.s
        
        :param style: The preset WordArt Style.
        :param text: The text.
        :param upper_left_row: Upper left row index.
        :param top: Represents the vertical  offset of shape from its left row, in unit of pixel.
        :param upper_left_column: Upper left column index.
        :param left: Represents the horizontal offset of shape from its left column, in unit of pixel.
        :param height: Represents the height of shape, in unit of pixel.
        :param width: Represents the width of shape, in unit of pixel.'''
        ...
    
    def add_rectangle(self, upper_left_row : int, top : int, upper_left_column : int, left : int, height : int, width : int) -> aspose.cells.drawing.RectangleShape:
        '''Adds a RectangleShape to the worksheet.
        
        :param upper_left_row: Upper left row index.
        :param top: Represents the vertical  offset of RectangleShape from its left row, in unit of pixel.
        :param upper_left_column: Upper left column index.
        :param left: Represents the horizontal offset of RectangleShape from its left column, in unit of pixel.
        :param height: Represents the height of RectangleShape, in unit of pixel.
        :param width: Represents the width of RectangleShape, in unit of pixel.
        :returns: A RectangleShape object.'''
        ...
    
    def add_oval(self, upper_left_row : int, top : int, upper_left_column : int, left : int, height : int, width : int) -> aspose.cells.drawing.Oval:
        '''Adds a Oval to the worksheet.
        
        :param upper_left_row: Upper left row index.
        :param top: Represents the vertical  offset of Oval from its left row, in unit of pixel.
        :param upper_left_column: Upper left column index.
        :param left: Represents the horizontal offset of Oval from its left column, in unit of pixel.
        :param height: Represents the height of Oval, in unit of pixel.
        :param width: Represents the width of Oval, in unit of pixel.
        :returns: A Oval object.'''
        ...
    
    def add_line(self, upper_left_row : int, top : int, upper_left_column : int, left : int, height : int, width : int) -> aspose.cells.drawing.LineShape:
        '''Adds a LineShape to the worksheet.
        
        :param upper_left_row: Upper left row index.
        :param top: Represents the vertical  offset of LineShape from its left row, in unit of pixel.
        :param upper_left_column: Upper left column index.
        :param left: Represents the horizontal offset of LineShape from its left column, in unit of pixel.
        :param height: Represents the height of LineShape, in unit of pixel.
        :param width: Represents the width of LineShape, in unit of pixel.
        :returns: A LineShape object.'''
        ...
    
    def add_free_floating_shape(self, type : aspose.cells.drawing.MsoDrawingType, top : int, left : int, height : int, width : int, image_data : bytes, is_original_size : bool) -> aspose.cells.drawing.Shape:
        '''Adds a free floating shape to the worksheet.Only applies for line/image shape.
        
        :param type: The shape type.
        :param top: Represents the vertical  offset of shape from the worksheet's top row, in unit of pixel.
        :param left: Represents the horizontal offset of shape from the worksheet's left column, in unit of pixel.
        :param height: Represents the height of LineShape, in unit of pixel.
        :param width: Represents the width of LineShape, in unit of pixel.
        :param image_data: The image data,only applies for the picture.
        :param is_original_size: Whether the shape use original size if the shape is image.'''
        ...
    
    def add_arc(self, upper_left_row : int, top : int, upper_left_column : int, left : int, height : int, width : int) -> aspose.cells.drawing.ArcShape:
        '''Adds a ArcShape to the worksheet.
        
        :param upper_left_row: Upper left row index.
        :param top: Represents the vertical  offset of ArcShape from its left row, in unit of pixel.
        :param upper_left_column: Upper left column index.
        :param left: Represents the horizontal offset of ArcShape from its left column, in unit of pixel.
        :param height: Represents the height of ArcShape, in unit of pixel.
        :param width: Represents the width of ArcShape, in unit of pixel.
        :returns: A ArcShape object.'''
        ...
    
    def add_shape(self, type : aspose.cells.drawing.MsoDrawingType, upper_left_row : int, top : int, upper_left_column : int, left : int, height : int, width : int) -> aspose.cells.drawing.Shape:
        '''Adds a Shape to the worksheet.
        
        :param type: Mso drawing type.
        :param upper_left_row: Upper left row index.
        :param top: Represents the vertical  offset of Shape from its left row, in unit of pixel.
        :param upper_left_column: Upper left column index.
        :param left: Represents the horizontal offset of Shape from its left column, in unit of pixel.
        :param height: Represents the height of Shape, in unit of pixel.
        :param width: Represents the width of Shape, in unit of pixel.
        :returns: A Shape object.'''
        ...
    
    def add_auto_shape(self, type : aspose.cells.drawing.AutoShapeType, upper_left_row : int, top : int, upper_left_column : int, left : int, height : int, width : int) -> aspose.cells.drawing.Shape:
        '''Adds a AutoShape to the worksheet.
        
        :param type: Auto shape type.
        :param upper_left_row: Upper left row index.
        :param top: Represents the vertical  offset of Shape from its left row, in unit of pixel.
        :param upper_left_column: Upper left column index.
        :param left: Represents the horizontal offset of Shape from its left column, in unit of pixel.
        :param height: Represents the height of Shape, in unit of pixel.
        :param width: Represents the width of Shape, in unit of pixel.
        :returns: A Shape object.'''
        ...
    
    def add_auto_shape_in_chart(self, type : aspose.cells.drawing.AutoShapeType, top : int, left : int, height : int, width : int) -> aspose.cells.drawing.Shape:
        '''Adds a AutoShape to the chart.
        
        :param type: Auto shape type.
        :param top: Represents the vertical offset of textbox from the upper left corner in units of 1/4000 of the chart area.
        :param left: Represents the vertical offset of textbox from the upper left corner in units of 1/4000 of the chart area.
        :param height: Represents the height of textbox, in units of 1/4000 of the chart area.
        :param width: Represents the width of textbox, in units of 1/4000 of the chart area.
        :returns: Returns a shape object.'''
        ...
    
    def add_active_x_control(self, type : aspose.cells.drawing.activexcontrols.ControlType, top_row : int, top : int, left_column : int, left : int, width : int, height : int) -> aspose.cells.drawing.Shape:
        '''Creates an Activex Control.
        
        :param type: The type of the control.
        :param top_row: Upper left row index.
        :param top: Represents the vertical  offset of Shape from its left row, in unit of pixel.
        :param left_column: Upper left column index.
        :param left: Represents the horizontal offset of Shape from its left column, in unit of pixel.
        :param height: Represents the height of Shape, in unit of pixel.
        :param width: Represents the width of Shape, in unit of pixel.'''
        ...
    
    def add_svg(self, upper_left_row : int, top : int, upper_left_column : int, left : int, height : int, width : int, svg_data : bytes, compatible_image_data : bytes) -> aspose.cells.drawing.Picture:
        '''Adds svg image.
        
        :param upper_left_row: Upper left row index.
        :param top: Represents the vertical  offset of shape from its left row, in unit of pixel.
        :param upper_left_column: Upper left column index.
        :param left: The horizontal offset of shape from its left column, in unit of pixel.
        :param height: The height of shape, in unit of pixel.
        :param width: The width of shape, in unit of pixel.
        :param svg_data: The svg image data.
        :param compatible_image_data: Converted image data from svg in order to be compatible with Excel 2016 or lower versions.'''
        ...
    
    def add_icons(self, upper_left_row : int, top : int, upper_left_column : int, left : int, height : int, width : int, image_byte_data : bytes, compatible_image_data : bytes) -> aspose.cells.drawing.Picture:
        '''Adds svg image.
        
        :param upper_left_row: Upper left row index.
        :param top: Represents the vertical offset of shape from its left row, in unit of pixel.
        :param upper_left_column: Upper left column index.
        :param left: The horizontal offset of shape from its left column, in unit of pixel.
        :param height: The height of shape, in unit of pixel.
        :param width: The width of shape, in unit of pixel.
        :param image_byte_data: The image byte data.
        :param compatible_image_data: Converted image data from svg in order to be compatible with Excel 2016 or lower versions.'''
        ...
    
    def add_linked_picture(self, upper_left_row : int, upper_left_column : int, height : int, width : int, source_full_name : str) -> aspose.cells.drawing.Picture:
        '''Add a linked picture.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param height: The height of the shape. In unit of pixels
        :param width: The width of the shape. In unit of pixels
        :param source_full_name: The path and name of the source file for the linked image
        :returns: :py:class:`aspose.cells.drawing.Picture` Picture object.'''
        ...
    
    def add_ole_object_with_linked_image(self, upper_left_row : int, upper_left_column : int, height : int, width : int, source_full_name : str) -> aspose.cells.drawing.OleObject:
        '''Add a linked picture.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param height: The height of the shape. In unit of pixels
        :param width: The width of the shape. In unit of pixels
        :param source_full_name: The path and name of the source file for the linked image
        :returns: :py:class:`aspose.cells.drawing.Picture` Picture object.'''
        ...
    
    def add_picture_in_chart(self, top : int, left : int, stream : io.RawIOBase, width_scale : int, height_scale : int) -> aspose.cells.drawing.Picture:
        '''Adds a picture to the chart.
        
        :param top: Represents the vertical offset of shape from the upper left corner in units of 1/4000 of the chart area.
        :param left: Represents the horizontal offset of shape from the upper left corner in units of 1/4000 of the chart area.
        :param stream: Stream object which contains the image data.
        :param width_scale: Scale of image width, a percentage.
        :param height_scale: Scale of image height, a percentage.
        :returns: Returns a Picture object.'''
        ...
    
    def add_ole_object(self, upper_left_row : int, top : int, upper_left_column : int, left : int, height : int, width : int, image_data : bytes) -> aspose.cells.drawing.OleObject:
        '''Adds an OleObject.'''
        ...
    
    def copy_comments_in_range(self, shapes : aspose.cells.drawing.ShapeCollection, ca : aspose.cells.CellArea, dest_row : int, dest_column : int):
        '''Copy all comments in the range.
        
        :param shapes: The source shapes.
        :param ca: The source range.
        :param dest_row: The dest range start row.
        :param dest_column: The dest range start column.'''
        ...
    
    def copy_in_range(self, source_shapes : aspose.cells.drawing.ShapeCollection, ca : aspose.cells.CellArea, dest_row : int, dest_column : int, is_contained : bool):
        '''Copy shapes in the range to destination range.
        
        :param source_shapes: Source shapes.
        :param ca: The source range.
        :param dest_row: The dest row index of the dest range.
        :param dest_column: The dest column of the dest range.
        :param is_contained: Whether only copy the shapes which are contained in the range.
        If true,only copies the shapes in the range.
        Otherwise,it works as MS Office.'''
        ...
    
    def delete_in_range(self, ca : aspose.cells.CellArea):
        '''Delete shapes in the range.Comment shapes will not be deleted.
        
        :param ca: The range.If the shapes are contained in the range, they will be removed.'''
        ...
    
    def delete_shape(self, shape : aspose.cells.drawing.Shape):
        '''Delete a shape. If the shape is in the group or is a comment shape, it will not be deleted.'''
        ...
    
    def group(self, group_items : List[aspose.cells.drawing.Shape]) -> aspose.cells.drawing.GroupShape:
        '''Group the shapes.
        
        :param group_items: the group items.
        :returns: Return the group shape.'''
        ...
    
    def ungroup(self, group : aspose.cells.drawing.GroupShape):
        '''Ungroups the shape items.
        
        :param group: The group shape.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell of the shapes.'''
        ...
    
    def binary_search(self, item : aspose.cells.drawing.Shape) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class ShapeFormat:
    
    def clear_glow_effect(self):
        ...
    
    def has_glow_effect(self) -> bool:
        ...
    
    def has_format_3d(self) -> bool:
        ...
    
    def clear_format_3d(self):
        ...
    
    def clear_shadow_effect(self):
        ...
    
    def has_shadow_effect(self) -> bool:
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def glow_effect(self) -> aspose.cells.drawing.GlowEffect:
        ...
    
    @property
    def soft_edge_radius(self) -> float:
        ...
    
    @soft_edge_radius.setter
    def soft_edge_radius(self, value : float):
        ...
    
    ...

class ShapeGuide(BaseShapeGuide):
    '''Encapsulates a shape guide specifies the presence of a shape guide that will be used to
    govern the geometry of the specified shape'''
    
    @property
    def value(self) -> float:
        '''Gets value of this guide'''
        ...
    
    @value.setter
    def value(self, value : float):
        '''Sets value of this guide'''
        ...
    
    ...

class ShapeGuideCollection:
    '''Encapsulates a collection of shape guide'''
    
    @overload
    def copy_to(self, array : List[aspose.cells.drawing.ShapeGuide]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.drawing.ShapeGuide], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.drawing.ShapeGuide, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.drawing.ShapeGuide, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.ShapeGuide) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.ShapeGuide, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.ShapeGuide, index : int, count : int) -> int:
        ...
    
    def add(self, name : str, val : float) -> int:
        '''Adds a shape guide.(Important: This feature is currently only available for Excel07 and above)
        
        :param name: the name of adjust. It's as "adj(Used when there is only one adjustment value)", "adj1", "adj2", "adj3" and so on.
        :param val: the value of adjust'''
        ...
    
    def binary_search(self, item : aspose.cells.drawing.ShapeGuide) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class ShapePath:
    '''Represents a creation path consisting of a series of moves, lines and curves that when combined will form a geometric shape.'''
    
    @property
    def path_segement_list(self) -> aspose.cells.drawing.ShapeSegmentPathCollection:
        ...
    
    ...

class ShapePathCollection:
    '''Represents path collection information in NotPrimitive autoshape'''
    
    @overload
    def copy_to(self, array : List[aspose.cells.drawing.ShapePath]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.drawing.ShapePath], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.drawing.ShapePath, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.drawing.ShapePath, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.ShapePath) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.ShapePath, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.ShapePath, index : int, count : int) -> int:
        ...
    
    def add(self) -> int:
        '''Add a creation path.
        
        :returns: Returns :py:class:`aspose.cells.drawing.ShapePath` object.'''
        ...
    
    def binary_search(self, item : aspose.cells.drawing.ShapePath) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class ShapePathPoint:
    '''Represents an x-y coordinate within the path coordinate space.'''
    
    @property
    def x(self) -> int:
        '''Gets and sets x coordinate for this position coordinate.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets x coordinate for this position coordinate.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets y coordinate for this position coordinate.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets y coordinate for this position coordinate.'''
        ...
    
    ...

class ShapePathPointCollection:
    '''Represents all shape path points.'''
    
    @overload
    def copy_to(self, array : List[aspose.cells.drawing.ShapePathPoint]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.drawing.ShapePathPoint], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.drawing.ShapePathPoint, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.drawing.ShapePathPoint, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.ShapePathPoint) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.ShapePathPoint, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.ShapePathPoint, index : int, count : int) -> int:
        ...
    
    def add(self, x : int, y : int) -> int:
        '''Adds a path point.
        
        :param x: The x coordinate.
        :param y: The y coordinate.'''
        ...
    
    def binary_search(self, item : aspose.cells.drawing.ShapePathPoint) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class ShapePropertyCollection:
    '''This class specifies the visual shape properties for a chart element or shape.'''
    
    def clear_glow_effect(self):
        '''Clears the glow effect of the shape.'''
        ...
    
    def has_glow_effect(self) -> bool:
        '''Indicates if the shape has glow effect data.'''
        ...
    
    def has_format_3d(self) -> bool:
        '''Indicates if the shape has 3d format data.'''
        ...
    
    def clear_format_3d(self):
        '''Clears the 3D shape properties of the shape.'''
        ...
    
    def clear_shadow_effect(self):
        '''Clears the shadow effect of the chart element or shape.'''
        ...
    
    def has_shadow_effect(self) -> bool:
        '''Indicates if the shape has shadow effect data.'''
        ...
    
    @property
    def glow_effect(self) -> aspose.cells.drawing.GlowEffect:
        ...
    
    @property
    def format_3d(self) -> aspose.cells.drawing.Format3D:
        ...
    
    @property
    def soft_edge_radius(self) -> float:
        ...
    
    @soft_edge_radius.setter
    def soft_edge_radius(self, value : float):
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    ...

class ShapeSegmentPath:
    '''Represents a segment path in a path of the freeform.'''
    
    @property
    def type(self) -> aspose.cells.drawing.ShapePathType:
        '''Gets the path segment type'''
        ...
    
    @property
    def points(self) -> aspose.cells.drawing.ShapePathPointCollection:
        '''Gets the points in path segment'''
        ...
    
    ...

class ShapeSegmentPathCollection:
    '''Represents a creation path consisting of a series of moves, lines and curves that when combined will form a geometric shape.'''
    
    @overload
    def copy_to(self, array : List[aspose.cells.drawing.ShapeSegmentPath]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.drawing.ShapeSegmentPath], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.drawing.ShapeSegmentPath, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.drawing.ShapeSegmentPath, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.ShapeSegmentPath) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.ShapeSegmentPath, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.ShapeSegmentPath, index : int, count : int) -> int:
        ...
    
    def add(self, type : aspose.cells.drawing.ShapePathType) -> int:
        '''Add a segment path in creation path.
        
        :param type: The path type.
        :returns: Returns the position of :py:class:`aspose.cells.drawing.ShapeSegmentPath` object in the list.'''
        ...
    
    def binary_search(self, item : aspose.cells.drawing.ShapeSegmentPath) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class SignatureLine:
    '''Represent the signature line.'''
    
    @property
    def id(self) -> Guid:
        '''Gets identifier for this signature line.'''
        ...
    
    @id.setter
    def id(self, value : Guid):
        '''Sets identifier for this signature line.'''
        ...
    
    @property
    def provider_id(self) -> Guid:
        ...
    
    @provider_id.setter
    def provider_id(self, value : Guid):
        ...
    
    @property
    def signer(self) -> str:
        '''Gets and sets the signer.'''
        ...
    
    @signer.setter
    def signer(self, value : str):
        '''Gets and sets the signer.'''
        ...
    
    @property
    def title(self) -> str:
        '''Gets and sets the title of singer.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Gets and sets the title of singer.'''
        ...
    
    @property
    def email(self) -> str:
        '''Gets and sets the email of singer.'''
        ...
    
    @email.setter
    def email(self, value : str):
        '''Gets and sets the email of singer.'''
        ...
    
    @property
    def is_line(self) -> bool:
        ...
    
    @is_line.setter
    def is_line(self, value : bool):
        ...
    
    @property
    def allow_comments(self) -> bool:
        ...
    
    @allow_comments.setter
    def allow_comments(self, value : bool):
        ...
    
    @property
    def show_signed_date(self) -> bool:
        ...
    
    @show_signed_date.setter
    def show_signed_date(self, value : bool):
        ...
    
    @property
    def instructions(self) -> str:
        '''Gets and sets the text shown to user at signing time.'''
        ...
    
    @instructions.setter
    def instructions(self, value : str):
        '''Gets and sets the text shown to user at signing time.'''
        ...
    
    ...

class SmartArtShape(Shape):
    '''Represents the smart art.'''
    
    @overload
    def to_image(self, stream : io.RawIOBase, image_type : aspose.cells.drawing.ImageType):
        '''Creates the shape image and saves it to a stream in the specified format.
        
        :param stream: The output stream.
        :param image_type: The type in which to save the image.'''
        ...
    
    @overload
    def to_image(self, image_file : str, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a file.'''
        ...
    
    @overload
    def to_image(self, stream : io.RawIOBase, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a stream.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.'''
        ...
    
    def get_result_of_smart_art(self) -> aspose.cells.drawing.GroupShape:
        '''Converting smart art to grouped shapes.'''
        ...
    
    def to_front_or_back(self, orders : int):
        '''Brings the shape to the front or sends the shape to back.
        
        :param orders: If it's less than zero, sets the shape to back.
        If it's greater than zero, brings the shape to front.'''
        ...
    
    def get_locked_property(self, type : aspose.cells.drawing.ShapeLockType) -> bool:
        '''Gets the value of locked property.
        
        :param type: The type of the shape locked property.
        :returns: Returns  the value of locked property.'''
        ...
    
    def set_locked_property(self, type : aspose.cells.drawing.ShapeLockType, value : bool):
        '''Set the locked property.
        
        :param type: The locked type.
        :param value: The value of the property.'''
        ...
    
    def add_hyperlink(self, address : str) -> aspose.cells.Hyperlink:
        '''Adds a hyperlink to the shape.
        
        :param address: Address of the hyperlink.
        :returns: Return the new hyperlink object.'''
        ...
    
    def remove_hyperlink(self):
        '''Remove the hyperlink of the shape.'''
        ...
    
    def move_to_range(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int):
        '''Moves the shape to a specified range.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index'''
        ...
    
    def align_top_right_corner(self, top_row : int, right_column : int):
        '''Moves the picture to the top-right corner.
        
        :param top_row: the row index.
        :param right_column: the column index.'''
        ...
    
    def get_connection_points(self) -> List[List[float]]:
        '''Get the connection points
        
        :returns: [X,Y] pairs of the connection point. Every item is a float[2] array, [0] represents x and [1] represents y.'''
        ...
    
    def get_linked_cell(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range linked to the control's value.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range linked to the control's value.'''
        ...
    
    def set_linked_cell(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range linked to the control's value.
        
        :param formula: The range linked to the control's value.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def get_input_range(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range used to fill the control.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range used to fill the control.'''
        ...
    
    def set_input_range(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range used to fill the control.
        
        :param formula: The range used to fill the control.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell.'''
        ...
    
    def calculate_text_size(self) -> List[int]:
        '''Recalculate the text area
        
        :returns: Text's Size in an array(width and height).'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the text .
        
        :returns: All Characters objects'''
        ...
    
    def remove_active_x_control(self):
        '''Remove activeX control.'''
        ...
    
    def is_same_setting(self, obj : any) -> bool:
        '''Returns whether the shape is same.'''
        ...
    
    @property
    def macro_name(self) -> str:
        ...
    
    @macro_name.setter
    def macro_name(self, value : str):
        ...
    
    @property
    def is_equation(self) -> bool:
        ...
    
    @property
    def is_smart_art(self) -> bool:
        ...
    
    @property
    def z_order_position(self) -> int:
        ...
    
    @z_order_position.setter
    def z_order_position(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of the shape.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of the shape.'''
        ...
    
    @property
    def alternative_text(self) -> str:
        ...
    
    @alternative_text.setter
    def alternative_text(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @property
    def line_format(self) -> aspose.cells.drawing.MsoLineFormat:
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.MsoFillFormat:
        ...
    
    @property
    def format(self) -> aspose.cells.drawing.ShapeFormat:
        '''Represents the setting of the shape's formatting.'''
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        '''Gets line style'''
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        '''Returns a :py:attr:`aspose.cells.drawing.Shape.fill_format` object that contains fill formatting properties for the specified shape.'''
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def reflection(self) -> aspose.cells.drawing.ReflectionEffect:
        '''Represents a :py:class:`aspose.cells.drawing.ReflectionEffect` object that specifies reflection effect for the chart element or shape.'''
        ...
    
    @property
    def glow(self) -> aspose.cells.drawing.GlowEffect:
        '''Represents a :py:class:`aspose.cells.drawing.GlowEffect` object that specifies glow effect for the chart element or shape.'''
        ...
    
    @property
    def soft_edges(self) -> float:
        ...
    
    @soft_edges.setter
    def soft_edges(self, value : float):
        ...
    
    @property
    def three_d_format(self) -> aspose.cells.drawing.ThreeDFormat:
        ...
    
    @property
    def text_frame(self) -> aspose.cells.drawing.MsoTextFrame:
        ...
    
    @property
    def format_picture(self) -> aspose.cells.drawing.MsoFormatPicture:
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_lock_aspect_ratio(self) -> bool:
        ...
    
    @is_lock_aspect_ratio.setter
    def is_lock_aspect_ratio(self, value : bool):
        ...
    
    @property
    def rotation_angle(self) -> float:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : float):
        ...
    
    @property
    def hyperlink(self) -> aspose.cells.Hyperlink:
        '''Gets the hyperlink of the shape.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier of this shape.'''
        ...
    
    @property
    def spid(self) -> str:
        '''Specifies an optional string that an application can use to Identify the particular shape.'''
        ...
    
    @property
    def spt(self) -> int:
        '''Specifies an optional number that an application can use to associate the particular shape with a defined shape type.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.drawing.Shape.worksheet` object which contains this shape.'''
        ...
    
    @property
    def is_group(self) -> bool:
        ...
    
    @property
    def is_in_group(self) -> bool:
        ...
    
    @property
    def is_word_art(self) -> bool:
        ...
    
    @property
    def text_effect(self) -> aspose.cells.drawing.TextEffectFormat:
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_printable(self) -> bool:
        ...
    
    @is_printable.setter
    def is_printable(self, value : bool):
        ...
    
    @property
    def mso_drawing_type(self) -> aspose.cells.drawing.MsoDrawingType:
        ...
    
    @property
    def auto_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @auto_shape_type.setter
    def auto_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def anchor_type(self) -> aspose.cells.drawing.ShapeAnchorType:
        ...
    
    @anchor_type.setter
    def anchor_type(self, value : aspose.cells.drawing.ShapeAnchorType):
        ...
    
    @property
    def placement(self) -> aspose.cells.drawing.PlacementType:
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @placement.setter
    def placement(self, value : aspose.cells.drawing.PlacementType):
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @property
    def upper_left_row(self) -> int:
        ...
    
    @upper_left_row.setter
    def upper_left_row(self, value : int):
        ...
    
    @property
    def upper_delta_y(self) -> int:
        ...
    
    @upper_delta_y.setter
    def upper_delta_y(self, value : int):
        ...
    
    @property
    def upper_left_column(self) -> int:
        ...
    
    @upper_left_column.setter
    def upper_left_column(self, value : int):
        ...
    
    @property
    def upper_delta_x(self) -> int:
        ...
    
    @upper_delta_x.setter
    def upper_delta_x(self, value : int):
        ...
    
    @property
    def lower_right_row(self) -> int:
        ...
    
    @lower_right_row.setter
    def lower_right_row(self, value : int):
        ...
    
    @property
    def lower_delta_y(self) -> int:
        ...
    
    @lower_delta_y.setter
    def lower_delta_y(self, value : int):
        ...
    
    @property
    def lower_right_column(self) -> int:
        ...
    
    @lower_right_column.setter
    def lower_right_column(self, value : int):
        ...
    
    @property
    def lower_delta_x(self) -> int:
        ...
    
    @lower_delta_x.setter
    def lower_delta_x(self, value : int):
        ...
    
    @property
    def right(self) -> int:
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def width_pt(self) -> float:
        ...
    
    @width_pt.setter
    def width_pt(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def height(self) -> int:
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    @property
    def height_pt(self) -> float:
        ...
    
    @height_pt.setter
    def height_pt(self, value : float):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def left(self) -> int:
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @property
    def left_inch(self) -> float:
        ...
    
    @left_inch.setter
    def left_inch(self, value : float):
        ...
    
    @property
    def left_cm(self) -> float:
        ...
    
    @left_cm.setter
    def left_cm(self, value : float):
        ...
    
    @property
    def top(self) -> int:
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @property
    def top_inch(self) -> float:
        ...
    
    @top_inch.setter
    def top_inch(self, value : float):
        ...
    
    @property
    def top_cm(self) -> float:
        ...
    
    @top_cm.setter
    def top_cm(self, value : float):
        ...
    
    @property
    def top_to_corner(self) -> int:
        ...
    
    @top_to_corner.setter
    def top_to_corner(self, value : int):
        ...
    
    @property
    def left_to_corner(self) -> int:
        ...
    
    @left_to_corner.setter
    def left_to_corner(self, value : int):
        ...
    
    @property
    def x(self) -> int:
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @property
    def width_scale(self) -> int:
        ...
    
    @width_scale.setter
    def width_scale(self, value : int):
        ...
    
    @property
    def height_scale(self) -> int:
        ...
    
    @height_scale.setter
    def height_scale(self, value : int):
        ...
    
    @property
    def top_in_shape(self) -> int:
        ...
    
    @top_in_shape.setter
    def top_in_shape(self, value : int):
        ...
    
    @property
    def left_in_shape(self) -> int:
        ...
    
    @left_in_shape.setter
    def left_in_shape(self, value : int):
        ...
    
    @property
    def width_in_shape(self) -> int:
        ...
    
    @width_in_shape.setter
    def width_in_shape(self, value : int):
        ...
    
    @property
    def height_in_shape(self) -> int:
        ...
    
    @height_in_shape.setter
    def height_in_shape(self, value : int):
        ...
    
    @property
    def group(self) -> aspose.cells.drawing.GroupShape:
        '''Gets the group shape which contains this shape.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.AutoShapeType:
        '''Gets the auto shape type.'''
        ...
    
    @property
    def has_line(self) -> bool:
        ...
    
    @has_line.setter
    def has_line(self, value : bool):
        ...
    
    @property
    def is_filled(self) -> bool:
        ...
    
    @is_filled.setter
    def is_filled(self, value : bool):
        ...
    
    @property
    def is_flipped_horizontally(self) -> bool:
        ...
    
    @is_flipped_horizontally.setter
    def is_flipped_horizontally(self, value : bool):
        ...
    
    @property
    def is_flipped_vertically(self) -> bool:
        ...
    
    @is_flipped_vertically.setter
    def is_flipped_vertically(self, value : bool):
        ...
    
    @property
    def actual_lower_right_row(self) -> int:
        ...
    
    @property
    def connection_points(self) -> aspose.pydrawing.PointF[]:
        ...
    
    @property
    def relative_to_original_picture_size(self) -> bool:
        ...
    
    @relative_to_original_picture_size.setter
    def relative_to_original_picture_size(self, value : bool):
        ...
    
    @property
    def linked_cell(self) -> str:
        ...
    
    @linked_cell.setter
    def linked_cell(self, value : str):
        ...
    
    @property
    def input_range(self) -> str:
        ...
    
    @input_range.setter
    def input_range(self, value : str):
        ...
    
    @property
    def text_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @text_shape_type.setter
    def text_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def text_body(self) -> aspose.cells.drawing.texts.FontSettingCollection:
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Represents the font of shape.'''
        ...
    
    @font.setter
    def font(self, value : aspose.cells.Font):
        '''Represents the font of shape.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    @text_options.setter
    def text_options(self, value : aspose.cells.drawing.texts.TextOptions):
        ...
    
    @property
    def text(self) -> str:
        '''Represents the string in this TextBox object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Represents the string in this TextBox object.'''
        ...
    
    @property
    def is_rich_text(self) -> bool:
        ...
    
    @property
    def html_text(self) -> str:
        ...
    
    @html_text.setter
    def html_text(self, value : str):
        ...
    
    @property
    def text_vertical_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_vertical_overflow.setter
    def text_vertical_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def text_horizontal_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_horizontal_overflow.setter
    def text_horizontal_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
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
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def control_data(self) -> bytes:
        ...
    
    @property
    def active_x_control(self) -> aspose.cells.drawing.activexcontrols.ActiveXControl:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets the paths of a custom geometric shape.'''
        ...
    
    @property
    def geometry(self) -> aspose.cells.drawing.Geometry:
        '''Gets the geometry'''
        ...
    
    @property
    def create_id(self) -> Guid:
        ...
    
    @create_id.setter
    def create_id(self, value : Guid):
        ...
    
    ...

class SolidFill(Fill):
    '''Encapsulates the object that represents solid fill format'''
    
    @property
    def color(self) -> aspose.pydrawing.Color:
        '''Gets the :py:class:`aspose.pydrawing.Color`.'''
        ...
    
    @color.setter
    def color(self, value : aspose.pydrawing.Color):
        '''Sets the :py:class:`aspose.pydrawing.Color`.'''
        ...
    
    @property
    def cells_color(self) -> aspose.cells.CellsColor:
        ...
    
    @cells_color.setter
    def cells_color(self, value : aspose.cells.CellsColor):
        ...
    
    @property
    def transparency(self) -> float:
        '''Returns the degree of transparency of the area as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    @transparency.setter
    def transparency(self, value : float):
        '''Returns or sets the degree of transparency of the area as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    ...

class Spinner(Shape):
    '''Represents the Forms control: Spinner.'''
    
    @overload
    def to_image(self, stream : io.RawIOBase, image_type : aspose.cells.drawing.ImageType):
        '''Creates the shape image and saves it to a stream in the specified format.
        
        :param stream: The output stream.
        :param image_type: The type in which to save the image.'''
        ...
    
    @overload
    def to_image(self, image_file : str, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a file.'''
        ...
    
    @overload
    def to_image(self, stream : io.RawIOBase, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a stream.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.'''
        ...
    
    def get_result_of_smart_art(self) -> aspose.cells.drawing.GroupShape:
        '''Converting smart art to grouped shapes.'''
        ...
    
    def to_front_or_back(self, orders : int):
        '''Brings the shape to the front or sends the shape to back.
        
        :param orders: If it's less than zero, sets the shape to back.
        If it's greater than zero, brings the shape to front.'''
        ...
    
    def get_locked_property(self, type : aspose.cells.drawing.ShapeLockType) -> bool:
        '''Gets the value of locked property.
        
        :param type: The type of the shape locked property.
        :returns: Returns  the value of locked property.'''
        ...
    
    def set_locked_property(self, type : aspose.cells.drawing.ShapeLockType, value : bool):
        '''Set the locked property.
        
        :param type: The locked type.
        :param value: The value of the property.'''
        ...
    
    def add_hyperlink(self, address : str) -> aspose.cells.Hyperlink:
        '''Adds a hyperlink to the shape.
        
        :param address: Address of the hyperlink.
        :returns: Return the new hyperlink object.'''
        ...
    
    def remove_hyperlink(self):
        '''Remove the hyperlink of the shape.'''
        ...
    
    def move_to_range(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int):
        '''Moves the shape to a specified range.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index'''
        ...
    
    def align_top_right_corner(self, top_row : int, right_column : int):
        '''Moves the picture to the top-right corner.
        
        :param top_row: the row index.
        :param right_column: the column index.'''
        ...
    
    def get_connection_points(self) -> List[List[float]]:
        '''Get the connection points
        
        :returns: [X,Y] pairs of the connection point. Every item is a float[2] array, [0] represents x and [1] represents y.'''
        ...
    
    def get_linked_cell(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range linked to the control's value.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range linked to the control's value.'''
        ...
    
    def set_linked_cell(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range linked to the control's value.
        
        :param formula: The range linked to the control's value.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def get_input_range(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range used to fill the control.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range used to fill the control.'''
        ...
    
    def set_input_range(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range used to fill the control.
        
        :param formula: The range used to fill the control.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell.'''
        ...
    
    def calculate_text_size(self) -> List[int]:
        '''Recalculate the text area
        
        :returns: Text's Size in an array(width and height).'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the text .
        
        :returns: All Characters objects'''
        ...
    
    def remove_active_x_control(self):
        '''Remove activeX control.'''
        ...
    
    def is_same_setting(self, obj : any) -> bool:
        '''Returns whether the shape is same.'''
        ...
    
    @property
    def macro_name(self) -> str:
        ...
    
    @macro_name.setter
    def macro_name(self, value : str):
        ...
    
    @property
    def is_equation(self) -> bool:
        ...
    
    @property
    def is_smart_art(self) -> bool:
        ...
    
    @property
    def z_order_position(self) -> int:
        ...
    
    @z_order_position.setter
    def z_order_position(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of the shape.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of the shape.'''
        ...
    
    @property
    def alternative_text(self) -> str:
        ...
    
    @alternative_text.setter
    def alternative_text(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @property
    def line_format(self) -> aspose.cells.drawing.MsoLineFormat:
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.MsoFillFormat:
        ...
    
    @property
    def format(self) -> aspose.cells.drawing.ShapeFormat:
        '''Represents the setting of the shape's formatting.'''
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        '''Gets line style'''
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        '''Returns a :py:attr:`aspose.cells.drawing.Shape.fill_format` object that contains fill formatting properties for the specified shape.'''
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def reflection(self) -> aspose.cells.drawing.ReflectionEffect:
        '''Represents a :py:class:`aspose.cells.drawing.ReflectionEffect` object that specifies reflection effect for the chart element or shape.'''
        ...
    
    @property
    def glow(self) -> aspose.cells.drawing.GlowEffect:
        '''Represents a :py:class:`aspose.cells.drawing.GlowEffect` object that specifies glow effect for the chart element or shape.'''
        ...
    
    @property
    def soft_edges(self) -> float:
        ...
    
    @soft_edges.setter
    def soft_edges(self, value : float):
        ...
    
    @property
    def three_d_format(self) -> aspose.cells.drawing.ThreeDFormat:
        ...
    
    @property
    def text_frame(self) -> aspose.cells.drawing.MsoTextFrame:
        ...
    
    @property
    def format_picture(self) -> aspose.cells.drawing.MsoFormatPicture:
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_lock_aspect_ratio(self) -> bool:
        ...
    
    @is_lock_aspect_ratio.setter
    def is_lock_aspect_ratio(self, value : bool):
        ...
    
    @property
    def rotation_angle(self) -> float:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : float):
        ...
    
    @property
    def hyperlink(self) -> aspose.cells.Hyperlink:
        '''Gets the hyperlink of the shape.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier of this shape.'''
        ...
    
    @property
    def spid(self) -> str:
        '''Specifies an optional string that an application can use to Identify the particular shape.'''
        ...
    
    @property
    def spt(self) -> int:
        '''Specifies an optional number that an application can use to associate the particular shape with a defined shape type.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.drawing.Shape.worksheet` object which contains this shape.'''
        ...
    
    @property
    def is_group(self) -> bool:
        ...
    
    @property
    def is_in_group(self) -> bool:
        ...
    
    @property
    def is_word_art(self) -> bool:
        ...
    
    @property
    def text_effect(self) -> aspose.cells.drawing.TextEffectFormat:
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_printable(self) -> bool:
        ...
    
    @is_printable.setter
    def is_printable(self, value : bool):
        ...
    
    @property
    def mso_drawing_type(self) -> aspose.cells.drawing.MsoDrawingType:
        ...
    
    @property
    def auto_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @auto_shape_type.setter
    def auto_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def anchor_type(self) -> aspose.cells.drawing.ShapeAnchorType:
        ...
    
    @anchor_type.setter
    def anchor_type(self, value : aspose.cells.drawing.ShapeAnchorType):
        ...
    
    @property
    def placement(self) -> aspose.cells.drawing.PlacementType:
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @placement.setter
    def placement(self, value : aspose.cells.drawing.PlacementType):
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @property
    def upper_left_row(self) -> int:
        ...
    
    @upper_left_row.setter
    def upper_left_row(self, value : int):
        ...
    
    @property
    def upper_delta_y(self) -> int:
        ...
    
    @upper_delta_y.setter
    def upper_delta_y(self, value : int):
        ...
    
    @property
    def upper_left_column(self) -> int:
        ...
    
    @upper_left_column.setter
    def upper_left_column(self, value : int):
        ...
    
    @property
    def upper_delta_x(self) -> int:
        ...
    
    @upper_delta_x.setter
    def upper_delta_x(self, value : int):
        ...
    
    @property
    def lower_right_row(self) -> int:
        ...
    
    @lower_right_row.setter
    def lower_right_row(self, value : int):
        ...
    
    @property
    def lower_delta_y(self) -> int:
        ...
    
    @lower_delta_y.setter
    def lower_delta_y(self, value : int):
        ...
    
    @property
    def lower_right_column(self) -> int:
        ...
    
    @lower_right_column.setter
    def lower_right_column(self, value : int):
        ...
    
    @property
    def lower_delta_x(self) -> int:
        ...
    
    @lower_delta_x.setter
    def lower_delta_x(self, value : int):
        ...
    
    @property
    def right(self) -> int:
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def width_pt(self) -> float:
        ...
    
    @width_pt.setter
    def width_pt(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def height(self) -> int:
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    @property
    def height_pt(self) -> float:
        ...
    
    @height_pt.setter
    def height_pt(self, value : float):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def left(self) -> int:
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @property
    def left_inch(self) -> float:
        ...
    
    @left_inch.setter
    def left_inch(self, value : float):
        ...
    
    @property
    def left_cm(self) -> float:
        ...
    
    @left_cm.setter
    def left_cm(self, value : float):
        ...
    
    @property
    def top(self) -> int:
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @property
    def top_inch(self) -> float:
        ...
    
    @top_inch.setter
    def top_inch(self, value : float):
        ...
    
    @property
    def top_cm(self) -> float:
        ...
    
    @top_cm.setter
    def top_cm(self, value : float):
        ...
    
    @property
    def top_to_corner(self) -> int:
        ...
    
    @top_to_corner.setter
    def top_to_corner(self, value : int):
        ...
    
    @property
    def left_to_corner(self) -> int:
        ...
    
    @left_to_corner.setter
    def left_to_corner(self, value : int):
        ...
    
    @property
    def x(self) -> int:
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @property
    def width_scale(self) -> int:
        ...
    
    @width_scale.setter
    def width_scale(self, value : int):
        ...
    
    @property
    def height_scale(self) -> int:
        ...
    
    @height_scale.setter
    def height_scale(self, value : int):
        ...
    
    @property
    def top_in_shape(self) -> int:
        ...
    
    @top_in_shape.setter
    def top_in_shape(self, value : int):
        ...
    
    @property
    def left_in_shape(self) -> int:
        ...
    
    @left_in_shape.setter
    def left_in_shape(self, value : int):
        ...
    
    @property
    def width_in_shape(self) -> int:
        ...
    
    @width_in_shape.setter
    def width_in_shape(self, value : int):
        ...
    
    @property
    def height_in_shape(self) -> int:
        ...
    
    @height_in_shape.setter
    def height_in_shape(self, value : int):
        ...
    
    @property
    def group(self) -> aspose.cells.drawing.GroupShape:
        '''Gets the group shape which contains this shape.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.AutoShapeType:
        '''Gets the auto shape type.'''
        ...
    
    @property
    def has_line(self) -> bool:
        ...
    
    @has_line.setter
    def has_line(self, value : bool):
        ...
    
    @property
    def is_filled(self) -> bool:
        ...
    
    @is_filled.setter
    def is_filled(self, value : bool):
        ...
    
    @property
    def is_flipped_horizontally(self) -> bool:
        ...
    
    @is_flipped_horizontally.setter
    def is_flipped_horizontally(self, value : bool):
        ...
    
    @property
    def is_flipped_vertically(self) -> bool:
        ...
    
    @is_flipped_vertically.setter
    def is_flipped_vertically(self, value : bool):
        ...
    
    @property
    def actual_lower_right_row(self) -> int:
        ...
    
    @property
    def connection_points(self) -> aspose.pydrawing.PointF[]:
        ...
    
    @property
    def relative_to_original_picture_size(self) -> bool:
        ...
    
    @relative_to_original_picture_size.setter
    def relative_to_original_picture_size(self, value : bool):
        ...
    
    @property
    def linked_cell(self) -> str:
        ...
    
    @linked_cell.setter
    def linked_cell(self, value : str):
        ...
    
    @property
    def input_range(self) -> str:
        ...
    
    @input_range.setter
    def input_range(self, value : str):
        ...
    
    @property
    def text_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @text_shape_type.setter
    def text_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def text_body(self) -> aspose.cells.drawing.texts.FontSettingCollection:
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Represents the font of shape.'''
        ...
    
    @font.setter
    def font(self, value : aspose.cells.Font):
        '''Represents the font of shape.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    @text_options.setter
    def text_options(self, value : aspose.cells.drawing.texts.TextOptions):
        ...
    
    @property
    def text(self) -> str:
        '''Represents the string in this TextBox object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Represents the string in this TextBox object.'''
        ...
    
    @property
    def is_rich_text(self) -> bool:
        ...
    
    @property
    def html_text(self) -> str:
        ...
    
    @html_text.setter
    def html_text(self, value : str):
        ...
    
    @property
    def text_vertical_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_vertical_overflow.setter
    def text_vertical_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def text_horizontal_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_horizontal_overflow.setter
    def text_horizontal_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
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
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def control_data(self) -> bytes:
        ...
    
    @property
    def active_x_control(self) -> aspose.cells.drawing.activexcontrols.ActiveXControl:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets the paths of a custom geometric shape.'''
        ...
    
    @property
    def geometry(self) -> aspose.cells.drawing.Geometry:
        '''Gets the geometry'''
        ...
    
    @property
    def create_id(self) -> Guid:
        ...
    
    @create_id.setter
    def create_id(self, value : Guid):
        ...
    
    @property
    def current_value(self) -> int:
        ...
    
    @current_value.setter
    def current_value(self, value : int):
        ...
    
    @property
    def min(self) -> int:
        '''Gets the minimum value of a scroll bar or spinner range.'''
        ...
    
    @min.setter
    def min(self, value : int):
        '''Sets the minimum value of a scroll bar or spinner range.'''
        ...
    
    @property
    def max(self) -> int:
        '''Gets the maximum value of a scroll bar or spinner range.'''
        ...
    
    @max.setter
    def max(self, value : int):
        '''Sets the maximum value of a scroll bar or spinner range.'''
        ...
    
    @property
    def incremental_change(self) -> int:
        ...
    
    @incremental_change.setter
    def incremental_change(self, value : int):
        ...
    
    @property
    def shadow(self) -> bool:
        '''Indicates whether the shape has 3-D shading.'''
        ...
    
    @shadow.setter
    def shadow(self, value : bool):
        '''Indicates whether the shape has 3-D shading.'''
        ...
    
    @property
    def is_horizontal(self) -> bool:
        ...
    
    @is_horizontal.setter
    def is_horizontal(self, value : bool):
        ...
    
    ...

class TextBox(Shape):
    '''Encapsulates the object that represents a textbox in a spreadsheet.'''
    
    @overload
    def to_image(self, stream : io.RawIOBase, image_type : aspose.cells.drawing.ImageType):
        '''Creates the shape image and saves it to a stream in the specified format.
        
        :param stream: The output stream.
        :param image_type: The type in which to save the image.'''
        ...
    
    @overload
    def to_image(self, image_file : str, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a file.'''
        ...
    
    @overload
    def to_image(self, stream : io.RawIOBase, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a stream.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.'''
        ...
    
    @overload
    def get_equation_paragraph(self, index : int) -> aspose.cells.drawing.equations.EquationNode:
        '''Get the specified math paragraph from the TextBody property of the TextBox object.
        Notice:
        (1) Returns NULL when the index is out of bounds or not found.
        (2) Also returns NULL if the specified index position is not a math paragraph.
        
        :param index: The position index of the math paragraph, starting from 0.
        :returns: Returns the math paragraph specified by index.'''
        ...
    
    @overload
    def get_equation_paragraph(self) -> aspose.cells.drawing.equations.EquationNode:
        '''Gets the first math paragraph from the TextBody property of the TextBox object.
        
        :returns: If there has math paragraph, returns the first one, otherwise returns null.'''
        ...
    
    def get_result_of_smart_art(self) -> aspose.cells.drawing.GroupShape:
        '''Converting smart art to grouped shapes.'''
        ...
    
    def to_front_or_back(self, orders : int):
        '''Brings the shape to the front or sends the shape to back.
        
        :param orders: If it's less than zero, sets the shape to back.
        If it's greater than zero, brings the shape to front.'''
        ...
    
    def get_locked_property(self, type : aspose.cells.drawing.ShapeLockType) -> bool:
        '''Gets the value of locked property.
        
        :param type: The type of the shape locked property.
        :returns: Returns  the value of locked property.'''
        ...
    
    def set_locked_property(self, type : aspose.cells.drawing.ShapeLockType, value : bool):
        '''Set the locked property.
        
        :param type: The locked type.
        :param value: The value of the property.'''
        ...
    
    def add_hyperlink(self, address : str) -> aspose.cells.Hyperlink:
        '''Adds a hyperlink to the shape.
        
        :param address: Address of the hyperlink.
        :returns: Return the new hyperlink object.'''
        ...
    
    def remove_hyperlink(self):
        '''Remove the hyperlink of the shape.'''
        ...
    
    def move_to_range(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int):
        '''Moves the shape to a specified range.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index'''
        ...
    
    def align_top_right_corner(self, top_row : int, right_column : int):
        '''Moves the picture to the top-right corner.
        
        :param top_row: the row index.
        :param right_column: the column index.'''
        ...
    
    def get_connection_points(self) -> List[List[float]]:
        '''Get the connection points
        
        :returns: [X,Y] pairs of the connection point. Every item is a float[2] array, [0] represents x and [1] represents y.'''
        ...
    
    def get_linked_cell(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range linked to the control's value.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range linked to the control's value.'''
        ...
    
    def set_linked_cell(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range linked to the control's value.
        
        :param formula: The range linked to the control's value.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def get_input_range(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range used to fill the control.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range used to fill the control.'''
        ...
    
    def set_input_range(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range used to fill the control.
        
        :param formula: The range used to fill the control.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell.'''
        ...
    
    def calculate_text_size(self) -> List[int]:
        '''Recalculate the text area
        
        :returns: Text's Size in an array(width and height).'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the text .
        
        :returns: All Characters objects'''
        ...
    
    def remove_active_x_control(self):
        '''Remove activeX control.'''
        ...
    
    def is_same_setting(self, obj : any) -> bool:
        '''Returns whether the shape is same.'''
        ...
    
    @property
    def macro_name(self) -> str:
        ...
    
    @macro_name.setter
    def macro_name(self, value : str):
        ...
    
    @property
    def is_equation(self) -> bool:
        ...
    
    @property
    def is_smart_art(self) -> bool:
        ...
    
    @property
    def z_order_position(self) -> int:
        ...
    
    @z_order_position.setter
    def z_order_position(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of the shape.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of the shape.'''
        ...
    
    @property
    def alternative_text(self) -> str:
        ...
    
    @alternative_text.setter
    def alternative_text(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @property
    def line_format(self) -> aspose.cells.drawing.MsoLineFormat:
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.MsoFillFormat:
        ...
    
    @property
    def format(self) -> aspose.cells.drawing.ShapeFormat:
        '''Represents the setting of the shape's formatting.'''
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        '''Gets line style'''
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        '''Returns a :py:attr:`aspose.cells.drawing.Shape.fill_format` object that contains fill formatting properties for the specified shape.'''
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def reflection(self) -> aspose.cells.drawing.ReflectionEffect:
        '''Represents a :py:class:`aspose.cells.drawing.ReflectionEffect` object that specifies reflection effect for the chart element or shape.'''
        ...
    
    @property
    def glow(self) -> aspose.cells.drawing.GlowEffect:
        '''Represents a :py:class:`aspose.cells.drawing.GlowEffect` object that specifies glow effect for the chart element or shape.'''
        ...
    
    @property
    def soft_edges(self) -> float:
        ...
    
    @soft_edges.setter
    def soft_edges(self, value : float):
        ...
    
    @property
    def three_d_format(self) -> aspose.cells.drawing.ThreeDFormat:
        ...
    
    @property
    def text_frame(self) -> aspose.cells.drawing.MsoTextFrame:
        ...
    
    @property
    def format_picture(self) -> aspose.cells.drawing.MsoFormatPicture:
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_lock_aspect_ratio(self) -> bool:
        ...
    
    @is_lock_aspect_ratio.setter
    def is_lock_aspect_ratio(self, value : bool):
        ...
    
    @property
    def rotation_angle(self) -> float:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : float):
        ...
    
    @property
    def hyperlink(self) -> aspose.cells.Hyperlink:
        '''Gets the hyperlink of the shape.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier of this shape.'''
        ...
    
    @property
    def spid(self) -> str:
        '''Specifies an optional string that an application can use to Identify the particular shape.'''
        ...
    
    @property
    def spt(self) -> int:
        '''Specifies an optional number that an application can use to associate the particular shape with a defined shape type.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.drawing.Shape.worksheet` object which contains this shape.'''
        ...
    
    @property
    def is_group(self) -> bool:
        ...
    
    @property
    def is_in_group(self) -> bool:
        ...
    
    @property
    def is_word_art(self) -> bool:
        ...
    
    @property
    def text_effect(self) -> aspose.cells.drawing.TextEffectFormat:
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_printable(self) -> bool:
        ...
    
    @is_printable.setter
    def is_printable(self, value : bool):
        ...
    
    @property
    def mso_drawing_type(self) -> aspose.cells.drawing.MsoDrawingType:
        ...
    
    @property
    def auto_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @auto_shape_type.setter
    def auto_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def anchor_type(self) -> aspose.cells.drawing.ShapeAnchorType:
        ...
    
    @anchor_type.setter
    def anchor_type(self, value : aspose.cells.drawing.ShapeAnchorType):
        ...
    
    @property
    def placement(self) -> aspose.cells.drawing.PlacementType:
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @placement.setter
    def placement(self, value : aspose.cells.drawing.PlacementType):
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @property
    def upper_left_row(self) -> int:
        ...
    
    @upper_left_row.setter
    def upper_left_row(self, value : int):
        ...
    
    @property
    def upper_delta_y(self) -> int:
        ...
    
    @upper_delta_y.setter
    def upper_delta_y(self, value : int):
        ...
    
    @property
    def upper_left_column(self) -> int:
        ...
    
    @upper_left_column.setter
    def upper_left_column(self, value : int):
        ...
    
    @property
    def upper_delta_x(self) -> int:
        ...
    
    @upper_delta_x.setter
    def upper_delta_x(self, value : int):
        ...
    
    @property
    def lower_right_row(self) -> int:
        ...
    
    @lower_right_row.setter
    def lower_right_row(self, value : int):
        ...
    
    @property
    def lower_delta_y(self) -> int:
        ...
    
    @lower_delta_y.setter
    def lower_delta_y(self, value : int):
        ...
    
    @property
    def lower_right_column(self) -> int:
        ...
    
    @lower_right_column.setter
    def lower_right_column(self, value : int):
        ...
    
    @property
    def lower_delta_x(self) -> int:
        ...
    
    @lower_delta_x.setter
    def lower_delta_x(self, value : int):
        ...
    
    @property
    def right(self) -> int:
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def width_pt(self) -> float:
        ...
    
    @width_pt.setter
    def width_pt(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def height(self) -> int:
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    @property
    def height_pt(self) -> float:
        ...
    
    @height_pt.setter
    def height_pt(self, value : float):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def left(self) -> int:
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @property
    def left_inch(self) -> float:
        ...
    
    @left_inch.setter
    def left_inch(self, value : float):
        ...
    
    @property
    def left_cm(self) -> float:
        ...
    
    @left_cm.setter
    def left_cm(self, value : float):
        ...
    
    @property
    def top(self) -> int:
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @property
    def top_inch(self) -> float:
        ...
    
    @top_inch.setter
    def top_inch(self, value : float):
        ...
    
    @property
    def top_cm(self) -> float:
        ...
    
    @top_cm.setter
    def top_cm(self, value : float):
        ...
    
    @property
    def top_to_corner(self) -> int:
        ...
    
    @top_to_corner.setter
    def top_to_corner(self, value : int):
        ...
    
    @property
    def left_to_corner(self) -> int:
        ...
    
    @left_to_corner.setter
    def left_to_corner(self, value : int):
        ...
    
    @property
    def x(self) -> int:
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @property
    def width_scale(self) -> int:
        ...
    
    @width_scale.setter
    def width_scale(self, value : int):
        ...
    
    @property
    def height_scale(self) -> int:
        ...
    
    @height_scale.setter
    def height_scale(self, value : int):
        ...
    
    @property
    def top_in_shape(self) -> int:
        ...
    
    @top_in_shape.setter
    def top_in_shape(self, value : int):
        ...
    
    @property
    def left_in_shape(self) -> int:
        ...
    
    @left_in_shape.setter
    def left_in_shape(self, value : int):
        ...
    
    @property
    def width_in_shape(self) -> int:
        ...
    
    @width_in_shape.setter
    def width_in_shape(self, value : int):
        ...
    
    @property
    def height_in_shape(self) -> int:
        ...
    
    @height_in_shape.setter
    def height_in_shape(self, value : int):
        ...
    
    @property
    def group(self) -> aspose.cells.drawing.GroupShape:
        '''Gets the group shape which contains this shape.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.AutoShapeType:
        '''Gets the auto shape type.'''
        ...
    
    @property
    def has_line(self) -> bool:
        ...
    
    @has_line.setter
    def has_line(self, value : bool):
        ...
    
    @property
    def is_filled(self) -> bool:
        ...
    
    @is_filled.setter
    def is_filled(self, value : bool):
        ...
    
    @property
    def is_flipped_horizontally(self) -> bool:
        ...
    
    @is_flipped_horizontally.setter
    def is_flipped_horizontally(self, value : bool):
        ...
    
    @property
    def is_flipped_vertically(self) -> bool:
        ...
    
    @is_flipped_vertically.setter
    def is_flipped_vertically(self, value : bool):
        ...
    
    @property
    def actual_lower_right_row(self) -> int:
        ...
    
    @property
    def connection_points(self) -> aspose.pydrawing.PointF[]:
        ...
    
    @property
    def relative_to_original_picture_size(self) -> bool:
        ...
    
    @relative_to_original_picture_size.setter
    def relative_to_original_picture_size(self, value : bool):
        ...
    
    @property
    def linked_cell(self) -> str:
        ...
    
    @linked_cell.setter
    def linked_cell(self, value : str):
        ...
    
    @property
    def input_range(self) -> str:
        ...
    
    @input_range.setter
    def input_range(self, value : str):
        ...
    
    @property
    def text_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @text_shape_type.setter
    def text_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def text_body(self) -> aspose.cells.drawing.texts.FontSettingCollection:
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Represents the font of shape.'''
        ...
    
    @font.setter
    def font(self, value : aspose.cells.Font):
        '''Represents the font of shape.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    @text_options.setter
    def text_options(self, value : aspose.cells.drawing.texts.TextOptions):
        ...
    
    @property
    def text(self) -> str:
        '''Represents the string in this TextBox object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Represents the string in this TextBox object.'''
        ...
    
    @property
    def is_rich_text(self) -> bool:
        ...
    
    @property
    def html_text(self) -> str:
        ...
    
    @html_text.setter
    def html_text(self, value : str):
        ...
    
    @property
    def text_vertical_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_vertical_overflow.setter
    def text_vertical_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def text_horizontal_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_horizontal_overflow.setter
    def text_horizontal_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
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
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def control_data(self) -> bytes:
        ...
    
    @property
    def active_x_control(self) -> aspose.cells.drawing.activexcontrols.ActiveXControl:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets the paths of a custom geometric shape.'''
        ...
    
    @property
    def geometry(self) -> aspose.cells.drawing.Geometry:
        '''Gets the geometry'''
        ...
    
    @property
    def create_id(self) -> Guid:
        ...
    
    @create_id.setter
    def create_id(self, value : Guid):
        ...
    
    ...

class TextBoxCollection:
    '''Encapsulates a collection of :py:class:`aspose.cells.drawing.TextBox` objects.'''
    
    @overload
    def copy_to(self, array : List[aspose.cells.drawing.TextBox]):
        ...
    
    @overload
    def copy_to(self, index : int, array : List[aspose.cells.drawing.TextBox], array_index : int, count : int):
        ...
    
    @overload
    def index_of(self, item : aspose.cells.drawing.TextBox, index : int) -> int:
        ...
    
    @overload
    def index_of(self, item : aspose.cells.drawing.TextBox, index : int, count : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.TextBox) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.TextBox, index : int) -> int:
        ...
    
    @overload
    def last_index_of(self, item : aspose.cells.drawing.TextBox, index : int, count : int) -> int:
        ...
    
    def add(self, upper_left_row : int, upper_left_column : int, height : int, width : int) -> int:
        '''Adds a textbox to the collection.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param height: Height of textbox, in unit of pixel.
        :param width: Width of textbox, in unit of pixel.
        :returns: :py:class:`aspose.cells.drawing.TextBox` object index.'''
        ...
    
    def binary_search(self, item : aspose.cells.drawing.TextBox) -> int:
        ...
    
    @property
    def capacity(self) -> int:
        ...
    
    @capacity.setter
    def capacity(self, value : int):
        ...
    
    ...

class TextEffectFormat:
    '''Contains properties and methods that apply to WordArt objects.'''
    
    def set_text_effect(self, effect : aspose.cells.drawing.MsoPresetTextEffect):
        '''Sets the preset text effect.
        
        :param effect: The preset text effect.'''
        ...
    
    @property
    def text(self) -> str:
        '''The text in the WordArt.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''The text in the WordArt.'''
        ...
    
    @property
    def font_name(self) -> str:
        ...
    
    @font_name.setter
    def font_name(self, value : str):
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
    def rotated_chars(self) -> bool:
        ...
    
    @rotated_chars.setter
    def rotated_chars(self, value : bool):
        ...
    
    @property
    def font_size(self) -> int:
        ...
    
    @font_size.setter
    def font_size(self, value : int):
        ...
    
    @property
    def preset_shape(self) -> aspose.cells.drawing.MsoPresetTextEffectShape:
        ...
    
    @preset_shape.setter
    def preset_shape(self, value : aspose.cells.drawing.MsoPresetTextEffectShape):
        ...
    
    ...

class TextureFill(Fill):
    '''Encapsulates the object that represents texture fill format'''
    
    @property
    def type(self) -> aspose.cells.drawing.TextureType:
        '''Gets and sets the texture type'''
        ...
    
    @type.setter
    def type(self, value : aspose.cells.drawing.TextureType):
        '''Gets and sets the texture type'''
        ...
    
    @property
    def image_data(self) -> bytes:
        ...
    
    @image_data.setter
    def image_data(self, value : bytes):
        ...
    
    @property
    def is_tiling(self) -> bool:
        ...
    
    @is_tiling.setter
    def is_tiling(self, value : bool):
        ...
    
    @property
    def pic_format_option(self) -> aspose.cells.drawing.PicFormatOption:
        ...
    
    @pic_format_option.setter
    def pic_format_option(self, value : aspose.cells.drawing.PicFormatOption):
        ...
    
    @property
    def tile_pic_option(self) -> aspose.cells.drawing.TilePicOption:
        ...
    
    @tile_pic_option.setter
    def tile_pic_option(self, value : aspose.cells.drawing.TilePicOption):
        ...
    
    @property
    def picture_format_type(self) -> aspose.cells.drawing.FillPictureType:
        ...
    
    @picture_format_type.setter
    def picture_format_type(self, value : aspose.cells.drawing.FillPictureType):
        ...
    
    @property
    def scale(self) -> float:
        '''Gets and sets the picture format scale.'''
        ...
    
    @scale.setter
    def scale(self, value : float):
        '''Gets and sets the picture format scale.'''
        ...
    
    @property
    def transparency(self) -> float:
        '''Returns the degree of transparency of the area as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    @transparency.setter
    def transparency(self, value : float):
        '''Returns or sets the degree of transparency of the area as a value from 0.0 (opaque) through 1.0 (clear).'''
        ...
    
    ...

class ThreeDFormat:
    '''Represents a shape's three-dimensional formatting.'''
    
    @property
    def bottom_bevel_width(self) -> float:
        ...
    
    @bottom_bevel_width.setter
    def bottom_bevel_width(self, value : float):
        ...
    
    @property
    def bottom_bevel_height(self) -> float:
        ...
    
    @bottom_bevel_height.setter
    def bottom_bevel_height(self, value : float):
        ...
    
    @property
    def bottom_bevel_type(self) -> aspose.cells.drawing.BevelType:
        ...
    
    @bottom_bevel_type.setter
    def bottom_bevel_type(self, value : aspose.cells.drawing.BevelType):
        ...
    
    @property
    def top_bevel_width(self) -> float:
        ...
    
    @top_bevel_width.setter
    def top_bevel_width(self, value : float):
        ...
    
    @property
    def top_bevel_height(self) -> float:
        ...
    
    @top_bevel_height.setter
    def top_bevel_height(self, value : float):
        ...
    
    @property
    def top_bevel_type(self) -> aspose.cells.drawing.BevelType:
        ...
    
    @top_bevel_type.setter
    def top_bevel_type(self, value : aspose.cells.drawing.BevelType):
        ...
    
    @property
    def material(self) -> aspose.cells.drawing.PresetMaterialType:
        '''Represents the preset material which is combined with the lighting properties to give the
        final look and feel of a shape.'''
        ...
    
    @material.setter
    def material(self, value : aspose.cells.drawing.PresetMaterialType):
        '''Represents the preset material which is combined with the lighting properties to give the
        final look and feel of a shape.'''
        ...
    
    @property
    def contour_color(self) -> aspose.cells.CellsColor:
        ...
    
    @contour_color.setter
    def contour_color(self, value : aspose.cells.CellsColor):
        ...
    
    @property
    def contour_width(self) -> float:
        ...
    
    @contour_width.setter
    def contour_width(self, value : float):
        ...
    
    @property
    def extrusion_color(self) -> aspose.cells.CellsColor:
        ...
    
    @extrusion_color.setter
    def extrusion_color(self, value : aspose.cells.CellsColor):
        ...
    
    @property
    def extrusion_height(self) -> float:
        ...
    
    @extrusion_height.setter
    def extrusion_height(self, value : float):
        ...
    
    @property
    def z(self) -> float:
        '''Defines the distance from ground for the 3D shape.'''
        ...
    
    @z.setter
    def z(self, value : float):
        '''Defines the distance from ground for the 3D shape.'''
        ...
    
    @property
    def light_angle(self) -> float:
        ...
    
    @light_angle.setter
    def light_angle(self, value : float):
        ...
    
    @property
    def lighting(self) -> aspose.cells.drawing.LightRigType:
        '''Gets and sets type of light rig.'''
        ...
    
    @lighting.setter
    def lighting(self, value : aspose.cells.drawing.LightRigType):
        '''Gets and sets type of light rig.'''
        ...
    
    @property
    def lighting_direction(self) -> aspose.cells.drawing.LightRigDirectionType:
        ...
    
    @lighting_direction.setter
    def lighting_direction(self, value : aspose.cells.drawing.LightRigDirectionType):
        ...
    
    @property
    def perspective(self) -> float:
        '''Gets and sets the angle at which a ThreeDFormat object can be viewed.'''
        ...
    
    @perspective.setter
    def perspective(self, value : float):
        '''Gets and sets the angle at which a ThreeDFormat object can be viewed.'''
        ...
    
    @property
    def rotation_x(self) -> float:
        ...
    
    @rotation_x.setter
    def rotation_x(self, value : float):
        ...
    
    @property
    def rotation_y(self) -> float:
        ...
    
    @rotation_y.setter
    def rotation_y(self, value : float):
        ...
    
    @property
    def rotation_z(self) -> float:
        ...
    
    @rotation_z.setter
    def rotation_z(self, value : float):
        ...
    
    @property
    def preset_camera_type(self) -> aspose.cells.drawing.PresetCameraType:
        ...
    
    @preset_camera_type.setter
    def preset_camera_type(self, value : aspose.cells.drawing.PresetCameraType):
        ...
    
    ...

class TilePicOption:
    '''Represents tile picture as texture.'''
    
    @property
    def offset_x(self) -> float:
        ...
    
    @offset_x.setter
    def offset_x(self, value : float):
        ...
    
    @property
    def offset_y(self) -> float:
        ...
    
    @offset_y.setter
    def offset_y(self, value : float):
        ...
    
    @property
    def scale_x(self) -> float:
        ...
    
    @scale_x.setter
    def scale_x(self, value : float):
        ...
    
    @property
    def scale_y(self) -> float:
        ...
    
    @scale_y.setter
    def scale_y(self, value : float):
        ...
    
    @property
    def mirror_type(self) -> aspose.cells.drawing.MirrorType:
        ...
    
    @mirror_type.setter
    def mirror_type(self, value : aspose.cells.drawing.MirrorType):
        ...
    
    @property
    def alignment_type(self) -> aspose.cells.drawing.RectangleAlignmentType:
        ...
    
    @alignment_type.setter
    def alignment_type(self, value : aspose.cells.drawing.RectangleAlignmentType):
        ...
    
    ...

class VmlShapeGuide(BaseShapeGuide):
    '''just for vml
    Encapsulates a shape guide specifies the presence of a shape
    guide that will be used to govern the geometry of the specified shape'''
    
    ...

class WebExtensionShape(Shape):
    '''Represents the shape of web extension.'''
    
    @overload
    def to_image(self, stream : io.RawIOBase, image_type : aspose.cells.drawing.ImageType):
        '''Creates the shape image and saves it to a stream in the specified format.
        
        :param stream: The output stream.
        :param image_type: The type in which to save the image.'''
        ...
    
    @overload
    def to_image(self, image_file : str, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a file.'''
        ...
    
    @overload
    def to_image(self, stream : io.RawIOBase, options : aspose.cells.rendering.ImageOrPrintOptions):
        '''Saves the shape to a stream.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font, flag : aspose.cells.StyleFlag):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.
        :param flag: The flag of the font setting.'''
        ...
    
    @overload
    def format_characters(self, start_index : int, length : int, font : aspose.cells.Font):
        '''Formats some characters with the font setting.
        
        :param start_index: The start index.
        :param length: The length.
        :param font: The font setting.'''
        ...
    
    def get_result_of_smart_art(self) -> aspose.cells.drawing.GroupShape:
        '''Converting smart art to grouped shapes.'''
        ...
    
    def to_front_or_back(self, orders : int):
        '''Brings the shape to the front or sends the shape to back.
        
        :param orders: If it's less than zero, sets the shape to back.
        If it's greater than zero, brings the shape to front.'''
        ...
    
    def get_locked_property(self, type : aspose.cells.drawing.ShapeLockType) -> bool:
        '''Gets the value of locked property.
        
        :param type: The type of the shape locked property.
        :returns: Returns  the value of locked property.'''
        ...
    
    def set_locked_property(self, type : aspose.cells.drawing.ShapeLockType, value : bool):
        '''Set the locked property.
        
        :param type: The locked type.
        :param value: The value of the property.'''
        ...
    
    def add_hyperlink(self, address : str) -> aspose.cells.Hyperlink:
        '''Adds a hyperlink to the shape.
        
        :param address: Address of the hyperlink.
        :returns: Return the new hyperlink object.'''
        ...
    
    def remove_hyperlink(self):
        '''Remove the hyperlink of the shape.'''
        ...
    
    def move_to_range(self, upper_left_row : int, upper_left_column : int, lower_right_row : int, lower_right_column : int):
        '''Moves the shape to a specified range.
        
        :param upper_left_row: Upper left row index.
        :param upper_left_column: Upper left column index.
        :param lower_right_row: Lower right row index
        :param lower_right_column: Lower right column index'''
        ...
    
    def align_top_right_corner(self, top_row : int, right_column : int):
        '''Moves the picture to the top-right corner.
        
        :param top_row: the row index.
        :param right_column: the column index.'''
        ...
    
    def get_connection_points(self) -> List[List[float]]:
        '''Get the connection points
        
        :returns: [X,Y] pairs of the connection point. Every item is a float[2] array, [0] represents x and [1] represents y.'''
        ...
    
    def get_linked_cell(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range linked to the control's value.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range linked to the control's value.'''
        ...
    
    def set_linked_cell(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range linked to the control's value.
        
        :param formula: The range linked to the control's value.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def get_input_range(self, is_r1c1 : bool, is_local : bool) -> str:
        '''Gets the range used to fill the control.
        
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.
        :returns: The range used to fill the control.'''
        ...
    
    def set_input_range(self, formula : str, is_r1c1 : bool, is_local : bool):
        '''Sets the range used to fill the control.
        
        :param formula: The range used to fill the control.
        :param is_r1c1: Whether the formula needs to be formatted as R1C1.
        :param is_local: Whether the formula needs to be formatted by locale.'''
        ...
    
    def update_selected_value(self):
        '''Update the selected value by the value of the linked cell.'''
        ...
    
    def calculate_text_size(self) -> List[int]:
        '''Recalculate the text area
        
        :returns: Text's Size in an array(width and height).'''
        ...
    
    def characters(self, start_index : int, length : int) -> aspose.cells.FontSetting:
        '''Returns a Characters object that represents a range of characters within the text.
        
        :param start_index: The index of the start of the character.
        :param length: The number of characters.
        :returns: Characters object.'''
        ...
    
    def get_characters(self) -> list:
        '''Returns all Characters objects
        that represents a range of characters within the text .
        
        :returns: All Characters objects'''
        ...
    
    def remove_active_x_control(self):
        '''Remove activeX control.'''
        ...
    
    def is_same_setting(self, obj : any) -> bool:
        '''Returns whether the shape is same.'''
        ...
    
    @property
    def macro_name(self) -> str:
        ...
    
    @macro_name.setter
    def macro_name(self, value : str):
        ...
    
    @property
    def is_equation(self) -> bool:
        ...
    
    @property
    def is_smart_art(self) -> bool:
        ...
    
    @property
    def z_order_position(self) -> int:
        ...
    
    @z_order_position.setter
    def z_order_position(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets and sets the name of the shape.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Gets and sets the name of the shape.'''
        ...
    
    @property
    def alternative_text(self) -> str:
        ...
    
    @alternative_text.setter
    def alternative_text(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Specifies the title (caption) of the current shape object.'''
        ...
    
    @property
    def line_format(self) -> aspose.cells.drawing.MsoLineFormat:
        ...
    
    @property
    def fill_format(self) -> aspose.cells.drawing.MsoFillFormat:
        ...
    
    @property
    def format(self) -> aspose.cells.drawing.ShapeFormat:
        '''Represents the setting of the shape's formatting.'''
        ...
    
    @property
    def line(self) -> aspose.cells.drawing.LineFormat:
        '''Gets line style'''
        ...
    
    @property
    def fill(self) -> aspose.cells.drawing.FillFormat:
        '''Returns a :py:attr:`aspose.cells.drawing.Shape.fill_format` object that contains fill formatting properties for the specified shape.'''
        ...
    
    @property
    def shadow_effect(self) -> aspose.cells.drawing.ShadowEffect:
        ...
    
    @property
    def reflection(self) -> aspose.cells.drawing.ReflectionEffect:
        '''Represents a :py:class:`aspose.cells.drawing.ReflectionEffect` object that specifies reflection effect for the chart element or shape.'''
        ...
    
    @property
    def glow(self) -> aspose.cells.drawing.GlowEffect:
        '''Represents a :py:class:`aspose.cells.drawing.GlowEffect` object that specifies glow effect for the chart element or shape.'''
        ...
    
    @property
    def soft_edges(self) -> float:
        ...
    
    @soft_edges.setter
    def soft_edges(self, value : float):
        ...
    
    @property
    def three_d_format(self) -> aspose.cells.drawing.ThreeDFormat:
        ...
    
    @property
    def text_frame(self) -> aspose.cells.drawing.MsoTextFrame:
        ...
    
    @property
    def format_picture(self) -> aspose.cells.drawing.MsoFormatPicture:
        ...
    
    @property
    def is_hidden(self) -> bool:
        ...
    
    @is_hidden.setter
    def is_hidden(self, value : bool):
        ...
    
    @property
    def is_lock_aspect_ratio(self) -> bool:
        ...
    
    @is_lock_aspect_ratio.setter
    def is_lock_aspect_ratio(self, value : bool):
        ...
    
    @property
    def rotation_angle(self) -> float:
        ...
    
    @rotation_angle.setter
    def rotation_angle(self, value : float):
        ...
    
    @property
    def hyperlink(self) -> aspose.cells.Hyperlink:
        '''Gets the hyperlink of the shape.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier of this shape.'''
        ...
    
    @property
    def spid(self) -> str:
        '''Specifies an optional string that an application can use to Identify the particular shape.'''
        ...
    
    @property
    def spt(self) -> int:
        '''Specifies an optional number that an application can use to associate the particular shape with a defined shape type.'''
        ...
    
    @property
    def worksheet(self) -> aspose.cells.Worksheet:
        '''Gets the :py:attr:`aspose.cells.drawing.Shape.worksheet` object which contains this shape.'''
        ...
    
    @property
    def is_group(self) -> bool:
        ...
    
    @property
    def is_in_group(self) -> bool:
        ...
    
    @property
    def is_word_art(self) -> bool:
        ...
    
    @property
    def text_effect(self) -> aspose.cells.drawing.TextEffectFormat:
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_printable(self) -> bool:
        ...
    
    @is_printable.setter
    def is_printable(self, value : bool):
        ...
    
    @property
    def mso_drawing_type(self) -> aspose.cells.drawing.MsoDrawingType:
        ...
    
    @property
    def auto_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @auto_shape_type.setter
    def auto_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def anchor_type(self) -> aspose.cells.drawing.ShapeAnchorType:
        ...
    
    @anchor_type.setter
    def anchor_type(self, value : aspose.cells.drawing.ShapeAnchorType):
        ...
    
    @property
    def placement(self) -> aspose.cells.drawing.PlacementType:
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @placement.setter
    def placement(self, value : aspose.cells.drawing.PlacementType):
        '''Represents the way the drawing object is attached to the cells below it.
        The property controls the placement of an object on a worksheet.'''
        ...
    
    @property
    def upper_left_row(self) -> int:
        ...
    
    @upper_left_row.setter
    def upper_left_row(self, value : int):
        ...
    
    @property
    def upper_delta_y(self) -> int:
        ...
    
    @upper_delta_y.setter
    def upper_delta_y(self, value : int):
        ...
    
    @property
    def upper_left_column(self) -> int:
        ...
    
    @upper_left_column.setter
    def upper_left_column(self, value : int):
        ...
    
    @property
    def upper_delta_x(self) -> int:
        ...
    
    @upper_delta_x.setter
    def upper_delta_x(self, value : int):
        ...
    
    @property
    def lower_right_row(self) -> int:
        ...
    
    @lower_right_row.setter
    def lower_right_row(self, value : int):
        ...
    
    @property
    def lower_delta_y(self) -> int:
        ...
    
    @lower_delta_y.setter
    def lower_delta_y(self, value : int):
        ...
    
    @property
    def lower_right_column(self) -> int:
        ...
    
    @lower_right_column.setter
    def lower_right_column(self, value : int):
        ...
    
    @property
    def lower_delta_x(self) -> int:
        ...
    
    @lower_delta_x.setter
    def lower_delta_x(self, value : int):
        ...
    
    @property
    def right(self) -> int:
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Represents the width of the shape's horizontal  offset from its lower right corner column, in unit of pixels.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Represents the width of the shape's vertical offset from its lower bottom corner row, in unit of pixels.'''
        ...
    
    @property
    def width(self) -> int:
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Represents the width of shape, in unit of pixels.'''
        ...
    
    @property
    def width_inch(self) -> float:
        ...
    
    @width_inch.setter
    def width_inch(self, value : float):
        ...
    
    @property
    def width_pt(self) -> float:
        ...
    
    @width_pt.setter
    def width_pt(self, value : float):
        ...
    
    @property
    def width_cm(self) -> float:
        ...
    
    @width_cm.setter
    def width_cm(self, value : float):
        ...
    
    @property
    def height(self) -> int:
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Represents the height of shape, in unit of pixel.'''
        ...
    
    @property
    def height_inch(self) -> float:
        ...
    
    @height_inch.setter
    def height_inch(self, value : float):
        ...
    
    @property
    def height_pt(self) -> float:
        ...
    
    @height_pt.setter
    def height_pt(self, value : float):
        ...
    
    @property
    def height_cm(self) -> float:
        ...
    
    @height_cm.setter
    def height_cm(self, value : float):
        ...
    
    @property
    def left(self) -> int:
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Represents the horizontal offset of shape from its left column, in unit of pixels.'''
        ...
    
    @property
    def left_inch(self) -> float:
        ...
    
    @left_inch.setter
    def left_inch(self, value : float):
        ...
    
    @property
    def left_cm(self) -> float:
        ...
    
    @left_cm.setter
    def left_cm(self, value : float):
        ...
    
    @property
    def top(self) -> int:
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Represents the vertical offset of shape from its top row, in unit of pixels.'''
        ...
    
    @property
    def top_inch(self) -> float:
        ...
    
    @top_inch.setter
    def top_inch(self, value : float):
        ...
    
    @property
    def top_cm(self) -> float:
        ...
    
    @top_cm.setter
    def top_cm(self, value : float):
        ...
    
    @property
    def top_to_corner(self) -> int:
        ...
    
    @top_to_corner.setter
    def top_to_corner(self, value : int):
        ...
    
    @property
    def left_to_corner(self) -> int:
        ...
    
    @left_to_corner.setter
    def left_to_corner(self, value : int):
        ...
    
    @property
    def x(self) -> int:
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Gets and sets the horizontal offset of shape from worksheet left border,in unit of pixels.'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Gets and sets the vertical offset of shape from worksheet top border,in unit of pixels.'''
        ...
    
    @property
    def width_scale(self) -> int:
        ...
    
    @width_scale.setter
    def width_scale(self, value : int):
        ...
    
    @property
    def height_scale(self) -> int:
        ...
    
    @height_scale.setter
    def height_scale(self, value : int):
        ...
    
    @property
    def top_in_shape(self) -> int:
        ...
    
    @top_in_shape.setter
    def top_in_shape(self, value : int):
        ...
    
    @property
    def left_in_shape(self) -> int:
        ...
    
    @left_in_shape.setter
    def left_in_shape(self, value : int):
        ...
    
    @property
    def width_in_shape(self) -> int:
        ...
    
    @width_in_shape.setter
    def width_in_shape(self, value : int):
        ...
    
    @property
    def height_in_shape(self) -> int:
        ...
    
    @height_in_shape.setter
    def height_in_shape(self, value : int):
        ...
    
    @property
    def group(self) -> aspose.cells.drawing.GroupShape:
        '''Gets the group shape which contains this shape.'''
        ...
    
    @property
    def type(self) -> aspose.cells.drawing.AutoShapeType:
        '''Gets the auto shape type.'''
        ...
    
    @property
    def has_line(self) -> bool:
        ...
    
    @has_line.setter
    def has_line(self, value : bool):
        ...
    
    @property
    def is_filled(self) -> bool:
        ...
    
    @is_filled.setter
    def is_filled(self, value : bool):
        ...
    
    @property
    def is_flipped_horizontally(self) -> bool:
        ...
    
    @is_flipped_horizontally.setter
    def is_flipped_horizontally(self, value : bool):
        ...
    
    @property
    def is_flipped_vertically(self) -> bool:
        ...
    
    @is_flipped_vertically.setter
    def is_flipped_vertically(self, value : bool):
        ...
    
    @property
    def actual_lower_right_row(self) -> int:
        ...
    
    @property
    def connection_points(self) -> aspose.pydrawing.PointF[]:
        ...
    
    @property
    def relative_to_original_picture_size(self) -> bool:
        ...
    
    @relative_to_original_picture_size.setter
    def relative_to_original_picture_size(self, value : bool):
        ...
    
    @property
    def linked_cell(self) -> str:
        ...
    
    @linked_cell.setter
    def linked_cell(self, value : str):
        ...
    
    @property
    def input_range(self) -> str:
        ...
    
    @input_range.setter
    def input_range(self, value : str):
        ...
    
    @property
    def text_shape_type(self) -> aspose.cells.drawing.AutoShapeType:
        ...
    
    @text_shape_type.setter
    def text_shape_type(self, value : aspose.cells.drawing.AutoShapeType):
        ...
    
    @property
    def text_body(self) -> aspose.cells.drawing.texts.FontSettingCollection:
        ...
    
    @property
    def font(self) -> aspose.cells.Font:
        '''Represents the font of shape.'''
        ...
    
    @font.setter
    def font(self, value : aspose.cells.Font):
        '''Represents the font of shape.'''
        ...
    
    @property
    def text_options(self) -> aspose.cells.drawing.texts.TextOptions:
        ...
    
    @text_options.setter
    def text_options(self, value : aspose.cells.drawing.texts.TextOptions):
        ...
    
    @property
    def text(self) -> str:
        '''Represents the string in this TextBox object.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Represents the string in this TextBox object.'''
        ...
    
    @property
    def is_rich_text(self) -> bool:
        ...
    
    @property
    def html_text(self) -> str:
        ...
    
    @html_text.setter
    def html_text(self, value : str):
        ...
    
    @property
    def text_vertical_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_vertical_overflow.setter
    def text_vertical_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def text_horizontal_overflow(self) -> aspose.cells.drawing.TextOverflowType:
        ...
    
    @text_horizontal_overflow.setter
    def text_horizontal_overflow(self, value : aspose.cells.drawing.TextOverflowType):
        ...
    
    @property
    def is_text_wrapped(self) -> bool:
        ...
    
    @is_text_wrapped.setter
    def is_text_wrapped(self, value : bool):
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
    def text_direction(self) -> aspose.cells.TextDirectionType:
        ...
    
    @text_direction.setter
    def text_direction(self, value : aspose.cells.TextDirectionType):
        ...
    
    @property
    def control_data(self) -> bytes:
        ...
    
    @property
    def active_x_control(self) -> aspose.cells.drawing.activexcontrols.ActiveXControl:
        ...
    
    @property
    def paths(self) -> aspose.cells.drawing.ShapePathCollection:
        '''Gets the paths of a custom geometric shape.'''
        ...
    
    @property
    def geometry(self) -> aspose.cells.drawing.Geometry:
        '''Gets the geometry'''
        ...
    
    @property
    def create_id(self) -> Guid:
        ...
    
    @create_id.setter
    def create_id(self, value : Guid):
        ...
    
    @property
    def web_extension(self) -> aspose.cells.webextensions.WebExtension:
        ...
    
    @web_extension.setter
    def web_extension(self, value : aspose.cells.webextensions.WebExtension):
        ...
    
    ...

class AutoShapeType:
    '''Represents all built-in auto shape type.'''
    
    @classmethod
    @property
    def NOT_PRIMITIVE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def RECTANGLE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def ROUNDED_RECTANGLE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def OVAL(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def DIAMOND(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def ISOSCELES_TRIANGLE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def RIGHT_TRIANGLE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def PARALLELOGRAM(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def TRAPEZOID(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def HEXAGON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def OCTAGON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def CROSS(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def STAR5(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def RIGHT_ARROW(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def HOME_PLATE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def CUBE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def BALLOON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def SEAL(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def ARC(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LINE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def PLAQUE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def CAN(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def DONUT(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def TEXT_SIMPLE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def TEXT_OCTAGON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def TEXT_HEXAGON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def TEXT_CURVE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def TEXT_WAVE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def TEXT_RING(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def TEXT_ON_CURVE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def MSOSPT_TEXT_ON_RING(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def STRAIGHT_CONNECTOR(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def BENT_CONNECTOR2(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def ELBOW_CONNECTOR(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def BENT_CONNECTOR4(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def BENT_CONNECTOR5(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def CURVED_CONNECTOR2(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def CURVED_CONNECTOR(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def CURVED_CONNECTOR4(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def CURVED_CONNECTOR5(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LINE_CALLOUT_NO_BORDER2(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LINE_CALLOUT_NO_BORDER3(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LINE_CALLOUT_NO_BORDER4(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LINE_CALLOUT_WITH_ACCENT_BAR2(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LINE_CALLOUT_WITH_ACCENT_BAR3(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LINE_CALLOUT_WITH_ACCENT_BAR4(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LINE_CALLOUT_WITH_BORDER2(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LINE_CALLOUT_WITH_BORDER3(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LINE_CALLOUT_WITH_BORDER4(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LINE_CALLOUT_WITH_BORDER_AND_ACCENT_BAR2(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LINE_CALLOUT_WITH_BORDER_AND_ACCENT_BAR3(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LINE_CALLOUT_WITH_BORDER_AND_ACCENT_BAR4(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def DOWN_RIBBON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def UP_RIBBON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def CHEVRON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def REGULAR_PENTAGON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def NO_SYMBOL(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def STAR8(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def STAR16(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def STAR32(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def RECTANGULAR_CALLOUT(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def ROUNDED_RECTANGULAR_CALLOUT(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def OVAL_CALLOUT(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def WAVE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FOLDED_CORNER(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LEFT_ARROW(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def DOWN_ARROW(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def UP_ARROW(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LEFT_RIGHT_ARROW(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def UP_DOWN_ARROW(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def EXPLOSION1(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def EXPLOSION2(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LIGHTNING_BOLT(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def HEART(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def PICTURE_FRAME(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def QUAD_ARROW(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LEFT_ARROW_CALLOUT(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def RIGHT_ARROW_CALLOUT(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def UP_ARROW_CALLOUT(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def DOWN_ARROW_CALLOUT(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LEFT_RIGHT_ARROW_CALLOUT(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def UP_DOWN_ARROW_CALLOUT(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def QUAD_ARROW_CALLOUT(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def BEVEL(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LEFT_BRACKET(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def RIGHT_BRACKET(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LEFT_BRACE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def RIGHT_BRACE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LEFT_UP_ARROW(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def BENT_UP_ARROW(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def BENT_ARROW(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def STAR24(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def STRIPED_RIGHT_ARROW(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def NOTCHED_RIGHT_ARROW(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def BLOCK_ARC(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def SMILEY_FACE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def VERTICAL_SCROLL(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def HORIZONTAL_SCROLL(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def CIRCULAR_ARROW(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def NOTCHED_CIRCULAR_ARROW(cls) -> AutoShapeType:
        '''A value that SHOULD NOT be used.'''
        ...
    
    @classmethod
    @property
    def U_TURN_ARROW(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def CURVED_RIGHT_ARROW(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def CURVED_LEFT_ARROW(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def CURVED_UP_ARROW(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def CURVED_DOWN_ARROW(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def CLOUD_CALLOUT(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def CURVED_DOWN_RIBBON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def CURVED_UP_RIBBON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_PROCESS(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_DECISION(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_DATA(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_PREDEFINED_PROCESS(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_INTERNAL_STORAGE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_DOCUMENT(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_MULTIDOCUMENT(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_TERMINATOR(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_PREPARATION(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_MANUAL_INPUT(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_MANUAL_OPERATION(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_CONNECTOR(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_CARD(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_PUNCHED_TAPE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_SUMMING_JUNCTION(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_OR(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_COLLATE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_SORT(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_EXTRACT(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_MERGE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_OFFLINE_STORAGE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_STORED_DATA(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_SEQUENTIAL_ACCESS_STORAGE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_MAGNETIC_DISK(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_DIRECT_ACCESS_STORAGE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_DISPLAY(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_DELAY(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def TEXT_PLAIN_TEXT(cls) -> AutoShapeType:
        '''A plain text shape.'''
        ...
    
    @classmethod
    @property
    def TEXT_STOP(cls) -> AutoShapeType:
        '''An octagonal text shape.'''
        ...
    
    @classmethod
    @property
    def TEXT_TRIANGLE(cls) -> AutoShapeType:
        '''A triangular text shape pointing upwards.'''
        ...
    
    @classmethod
    @property
    def TEXT_TRIANGLE_INVERTED(cls) -> AutoShapeType:
        '''A triangular text shape pointing downwards.'''
        ...
    
    @classmethod
    @property
    def TEXT_CHEVRON(cls) -> AutoShapeType:
        '''A chevron text shape pointing upwards.'''
        ...
    
    @classmethod
    @property
    def TEXT_CHEVRON_INVERTED(cls) -> AutoShapeType:
        '''A chevron text shape pointing downwards.'''
        ...
    
    @classmethod
    @property
    def TEXT_RING_INSIDE(cls) -> AutoShapeType:
        '''A circular text shape, as if reading an inscription on the inside of a ring.'''
        ...
    
    @classmethod
    @property
    def TEXT_RING_OUTSIDE(cls) -> AutoShapeType:
        '''A circular text shape, as if reading an inscription on the outside of a ring.'''
        ...
    
    @classmethod
    @property
    def TEXT_ARCH_UP_CURVE(cls) -> AutoShapeType:
        '''An upward arching curved text shape.'''
        ...
    
    @classmethod
    @property
    def TEXT_ARCH_DOWN_CURVE(cls) -> AutoShapeType:
        '''A downward arching curved text shape.'''
        ...
    
    @classmethod
    @property
    def TEXT_CIRCLE_CURVE(cls) -> AutoShapeType:
        '''A circular text shape.'''
        ...
    
    @classmethod
    @property
    def TEXT_BUTTON_CURVE(cls) -> AutoShapeType:
        '''A text shape that resembles a button.'''
        ...
    
    @classmethod
    @property
    def TEXT_ARCH_UP_POUR(cls) -> AutoShapeType:
        '''An upward arching text shape.'''
        ...
    
    @classmethod
    @property
    def TEXT_ARCH_DOWN_POUR(cls) -> AutoShapeType:
        '''A downward arching text shape.'''
        ...
    
    @classmethod
    @property
    def TEXT_CIRCLE_POUR(cls) -> AutoShapeType:
        '''A circular text shape.'''
        ...
    
    @classmethod
    @property
    def TEXT_BUTTON_POUR(cls) -> AutoShapeType:
        '''A text shape that resembles a button.'''
        ...
    
    @classmethod
    @property
    def TEXT_CURVE_UP(cls) -> AutoShapeType:
        '''An upward curving text shape.'''
        ...
    
    @classmethod
    @property
    def TEXT_CURVE_DOWN(cls) -> AutoShapeType:
        '''A downward curving text shape.'''
        ...
    
    @classmethod
    @property
    def TEXT_CASCADE_UP(cls) -> AutoShapeType:
        '''A cascading text shape pointed upwards.'''
        ...
    
    @classmethod
    @property
    def TEXT_CASCADE_DOWN(cls) -> AutoShapeType:
        '''A cascading text shape pointed downwards.'''
        ...
    
    @classmethod
    @property
    def TEXT_WAVE1(cls) -> AutoShapeType:
        '''A wavy text shape.'''
        ...
    
    @classmethod
    @property
    def TEXT_WAVE2(cls) -> AutoShapeType:
        '''A wavy text shape.'''
        ...
    
    @classmethod
    @property
    def TEXT_DOUBLE_WAVE1(cls) -> AutoShapeType:
        '''A wavy text shape.'''
        ...
    
    @classmethod
    @property
    def TEXT_DOUBLE_WAVE2(cls) -> AutoShapeType:
        '''A wavy text shape.'''
        ...
    
    @classmethod
    @property
    def TEXT_INFLATE(cls) -> AutoShapeType:
        '''A text shape that expands vertically in the middle.'''
        ...
    
    @classmethod
    @property
    def TEXT_DEFLATE(cls) -> AutoShapeType:
        '''A text shape that shrinks vertically in the middle.'''
        ...
    
    @classmethod
    @property
    def TEXT_INFLATE_BOTTOM(cls) -> AutoShapeType:
        '''A text shape that expands downward in the middle.'''
        ...
    
    @classmethod
    @property
    def TEXT_DEFLATE_BOTTOM(cls) -> AutoShapeType:
        '''A text shape that shrinks upwards in the middle.'''
        ...
    
    @classmethod
    @property
    def TEXT_INFLATE_TOP(cls) -> AutoShapeType:
        '''A text shape that expands upward in the middle.'''
        ...
    
    @classmethod
    @property
    def TEXT_DEFLATE_TOP(cls) -> AutoShapeType:
        '''A text shape that shrinks downward in the middle.'''
        ...
    
    @classmethod
    @property
    def TEXT_DEFLATE_INFLATE(cls) -> AutoShapeType:
        '''A text shape where lower lines expand upward. Upper lines shrink to compensate.'''
        ...
    
    @classmethod
    @property
    def TEXT_DEFLATE_INFLATE_DEFLATE(cls) -> AutoShapeType:
        '''A text shape where lines in the center expand vertically. Upper and lower lines shrink to compensate.'''
        ...
    
    @classmethod
    @property
    def TEXT_FADE_RIGHT(cls) -> AutoShapeType:
        '''A text shape that shrinks vertically on the right side.'''
        ...
    
    @classmethod
    @property
    def TEXT_FADE_LEFT(cls) -> AutoShapeType:
        '''A text shape that shrinks vertically on the left side.'''
        ...
    
    @classmethod
    @property
    def TEXT_FADE_UP(cls) -> AutoShapeType:
        '''A text shape that shrinks horizontally on top.'''
        ...
    
    @classmethod
    @property
    def TEXT_FADE_DOWN(cls) -> AutoShapeType:
        '''A text shape that shrinks horizontally on bottom.'''
        ...
    
    @classmethod
    @property
    def TEXT_SLANT_UP(cls) -> AutoShapeType:
        '''An upward slanted text shape.'''
        ...
    
    @classmethod
    @property
    def TEXT_SLANT_DOWN(cls) -> AutoShapeType:
        '''A downward slanted text shape.'''
        ...
    
    @classmethod
    @property
    def TEXT_CAN_UP(cls) -> AutoShapeType:
        '''A text shape that is curved upwards as if being read on the side of a can.'''
        ...
    
    @classmethod
    @property
    def TEXT_CAN_DOWN(cls) -> AutoShapeType:
        '''A text shape that is curved downwards as if being read on the side of a can.'''
        ...
    
    @classmethod
    @property
    def FLOW_CHART_ALTERNATE_PROCESS(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FLOW_CHART_OFFPAGE_CONNECTOR(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LINE_CALLOUT_NO_BORDER1(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LINE_CALLOUT_WITH_ACCENT_BAR1(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LINE_CALLOUT_WITH_BORDER1(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LINE_CALLOUT_WITH_BORDER_AND_ACCENT_BAR1(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LEFT_RIGHT_UP_ARROW(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def SUN(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def MOON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def DOUBLE_BRACKET(cls) -> AutoShapeType:
        '''A shape enclosed in brackets.'''
        ...
    
    @classmethod
    @property
    def DOUBLE_BRACE(cls) -> AutoShapeType:
        '''A shape enclosed in braces.'''
        ...
    
    @classmethod
    @property
    def STAR4(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def DOUBLE_WAVE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def BLANK_ACTION_BUTTON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def HOME_ACTION_BUTTON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def HELP_ACTION_BUTTON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def INFORMATION_ACTION_BUTTON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FORWARD_NEXT_ACTION_BUTTON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def BACK_PREVIOUS_ACTION_BUTTON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def END_ACTION_BUTTON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def BEGINNING_ACTION_BUTTON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def RETURN_ACTION_BUTTON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def DOCUMENT_ACTION_BUTTON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def SOUND_ACTION_BUTTON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def MOVIE_ACTION_BUTTON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def HOST_CONTROL(cls) -> AutoShapeType:
        '''This value SHOULD NOT be used.'''
        ...
    
    @classmethod
    @property
    def TEXT_BOX(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def HEPTAGON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def DECAGON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def DODECAGON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def STAR6(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def STAR7(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def STAR10(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def STAR12(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def ROUND_SINGLE_CORNER_RECTANGLE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def ROUND_SAME_SIDE_CORNER_RECTANGLE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def ROUND_DIAGONAL_CORNER_RECTANGLE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def SNIP_ROUND_SINGLE_CORNER_RECTANGLE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def SNIP_SINGLE_CORNER_RECTANGLE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def SNIP_SAME_SIDE_CORNER_RECTANGLE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def SNIP_DIAGONAL_CORNER_RECTANGLE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def TEARDROP(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def PIE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def HALF_FRAME(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def L_SHAPE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def DIAGONAL_STRIPE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def CHORD(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def CLOUD(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def MATH_PLUS(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def MATH_MINUS(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def MATH_MULTIPLY(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def MATH_DIVIDE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def MATH_EQUAL(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def MATH_NOT_EQUAL(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LINE_INV(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def NON_ISOSCELES_TRAPEZOID(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def PIE_WEDGE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LEFT_CIRCULAR_ARROW(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LEFT_RIGHT_CIRCULAR_ARROW(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def SWOOSH_ARROW(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def LEFT_RIGHT_RIBBON(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def TEXT_NO_SHAPE(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def GEAR6(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def GEAR9(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FUNNEL(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def CORNER_TABS(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def SQUARE_TABS(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def PLAQUE_TABS(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def CHART_X(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def CHART_STAR(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def CHART_PLUS(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def FRAME(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def MODEL_3D(cls) -> AutoShapeType:
        ...
    
    @classmethod
    @property
    def ROUND_CALLOUT(cls) -> AutoShapeType:
        '''There is no such type in Excel'''
        ...
    
    @classmethod
    @property
    def TEXT_ARCH_LEFT_POUR(cls) -> AutoShapeType:
        '''There is no such type in Excel'''
        ...
    
    @classmethod
    @property
    def TEXT_ARCH_RIGHT_POUR(cls) -> AutoShapeType:
        '''There is no such type in Excel'''
        ...
    
    @classmethod
    @property
    def TEXT_ARCH_LEFT_CURVE(cls) -> AutoShapeType:
        '''There is no such type in Excel'''
        ...
    
    @classmethod
    @property
    def TEXT_ARCH_RIGHT_CURVE(cls) -> AutoShapeType:
        '''There is no such type in Excel'''
        ...
    
    @classmethod
    @property
    def UNKNOWN(cls) -> AutoShapeType:
        ...
    
    ...

class BevelPresetType:
    '''Represents a preset for a type of bevel which can be applied to a shape in 3D.'''
    
    @classmethod
    @property
    def NONE(cls) -> BevelPresetType:
        '''No bevel'''
        ...
    
    @classmethod
    @property
    def ANGLE(cls) -> BevelPresetType:
        '''Angle'''
        ...
    
    @classmethod
    @property
    def ART_DECO(cls) -> BevelPresetType:
        '''Art deco'''
        ...
    
    @classmethod
    @property
    def CIRCLE(cls) -> BevelPresetType:
        '''Circle'''
        ...
    
    @classmethod
    @property
    def CONVEX(cls) -> BevelPresetType:
        '''Convex'''
        ...
    
    @classmethod
    @property
    def COOL_SLANT(cls) -> BevelPresetType:
        '''Cool slant'''
        ...
    
    @classmethod
    @property
    def CROSS(cls) -> BevelPresetType:
        '''Cross'''
        ...
    
    @classmethod
    @property
    def DIVOT(cls) -> BevelPresetType:
        '''Divot'''
        ...
    
    @classmethod
    @property
    def HARD_EDGE(cls) -> BevelPresetType:
        '''Hard edge'''
        ...
    
    @classmethod
    @property
    def RELAXED_INSET(cls) -> BevelPresetType:
        '''Relaxed inset'''
        ...
    
    @classmethod
    @property
    def RIBLET(cls) -> BevelPresetType:
        '''Riblet'''
        ...
    
    @classmethod
    @property
    def SLOPE(cls) -> BevelPresetType:
        '''Slope'''
        ...
    
    @classmethod
    @property
    def SOFT_ROUND(cls) -> BevelPresetType:
        '''Soft round'''
        ...
    
    ...

class BevelType:
    '''Represents a preset for a type of bevel which can be applied to a shape in 3D.'''
    
    @classmethod
    @property
    def NONE(cls) -> BevelType:
        '''No bevel'''
        ...
    
    @classmethod
    @property
    def ANGLE(cls) -> BevelType:
        '''Angle'''
        ...
    
    @classmethod
    @property
    def ART_DECO(cls) -> BevelType:
        '''Art deco'''
        ...
    
    @classmethod
    @property
    def CIRCLE(cls) -> BevelType:
        '''Circle'''
        ...
    
    @classmethod
    @property
    def CONVEX(cls) -> BevelType:
        '''Convex'''
        ...
    
    @classmethod
    @property
    def COOL_SLANT(cls) -> BevelType:
        '''Cool slant'''
        ...
    
    @classmethod
    @property
    def CROSS(cls) -> BevelType:
        '''Cross'''
        ...
    
    @classmethod
    @property
    def DIVOT(cls) -> BevelType:
        '''Divot'''
        ...
    
    @classmethod
    @property
    def HARD_EDGE(cls) -> BevelType:
        '''Hard edge'''
        ...
    
    @classmethod
    @property
    def RELAXED_INSET(cls) -> BevelType:
        '''Relaxed inset'''
        ...
    
    @classmethod
    @property
    def RIBLET(cls) -> BevelType:
        '''Riblet'''
        ...
    
    @classmethod
    @property
    def SLOPE(cls) -> BevelType:
        '''Slope'''
        ...
    
    @classmethod
    @property
    def SOFT_ROUND(cls) -> BevelType:
        '''Soft round'''
        ...
    
    ...

class CheckValueType:
    '''Represents the check value type of the check box.'''
    
    @classmethod
    @property
    def UN_CHECKED(cls) -> CheckValueType:
        '''UnChecked'''
        ...
    
    @classmethod
    @property
    def CHECKED(cls) -> CheckValueType:
        '''Checked'''
        ...
    
    @classmethod
    @property
    def MIXED(cls) -> CheckValueType:
        '''Mixed'''
        ...
    
    ...

class DataLabelShapeType:
    '''Specifies the preset shape geometry that is to be used for a chart.'''
    
    @classmethod
    @property
    def RECT(cls) -> DataLabelShapeType:
        '''Represents the rectangle shape.'''
        ...
    
    @classmethod
    @property
    def ROUND_RECT(cls) -> DataLabelShapeType:
        '''Represents the round rectangle shape.'''
        ...
    
    @classmethod
    @property
    def ELLIPSE(cls) -> DataLabelShapeType:
        '''Represents the ellipse shape.'''
        ...
    
    @classmethod
    @property
    def RIGHT_ARROW_CALLOUT(cls) -> DataLabelShapeType:
        '''Represents the right arrow callout shape.'''
        ...
    
    @classmethod
    @property
    def DOWN_ARROW_CALLOUT(cls) -> DataLabelShapeType:
        '''Represents the down arrow callout shape.'''
        ...
    
    @classmethod
    @property
    def LEFT_ARROW_CALLOUT(cls) -> DataLabelShapeType:
        '''Represents the left arrow callout shape.'''
        ...
    
    @classmethod
    @property
    def UP_ARROW_CALLOUT(cls) -> DataLabelShapeType:
        '''Represents the up arrow callout shape.'''
        ...
    
    @classmethod
    @property
    def WEDGE_RECT_CALLOUT(cls) -> DataLabelShapeType:
        '''Represents the wedge rectangle callout shape.'''
        ...
    
    @classmethod
    @property
    def WEDGE_ROUND_RECT_CALLOUT(cls) -> DataLabelShapeType:
        '''Represents the wedge round rectangle callout shape.'''
        ...
    
    @classmethod
    @property
    def WEDGE_ELLIPSE_CALLOUT(cls) -> DataLabelShapeType:
        '''Represents the wedge ellipse callout shape.'''
        ...
    
    @classmethod
    @property
    def LINE_CALLOUT(cls) -> DataLabelShapeType:
        '''Represents the line callout shape.'''
        ...
    
    @classmethod
    @property
    def BENT_LINE_CALLOUT(cls) -> DataLabelShapeType:
        '''Represents the bent line callout  shape.'''
        ...
    
    @classmethod
    @property
    def LINE_WITH_ACCENT_BAR_CALLOUT(cls) -> DataLabelShapeType:
        '''Represents the line with accent bar callout shape.'''
        ...
    
    @classmethod
    @property
    def BENT_LINE_WITH_ACCENT_BAR_CALLOUT(cls) -> DataLabelShapeType:
        '''Represents the bent line with accent bar callout shape.'''
        ...
    
    @classmethod
    @property
    def LINE(cls) -> DataLabelShapeType:
        '''This type is only used for special file processing'''
        ...
    
    ...

class FillPattern:
    '''Enumerates shape fill pattern types.'''
    
    @classmethod
    @property
    def NONE(cls) -> FillPattern:
        '''Represents no background.'''
        ...
    
    @classmethod
    @property
    def SOLID(cls) -> FillPattern:
        '''Represents solid pattern.'''
        ...
    
    @classmethod
    @property
    def GRAY5(cls) -> FillPattern:
        '''Represents 5% gray pattern.'''
        ...
    
    @classmethod
    @property
    def GRAY10(cls) -> FillPattern:
        '''Represents 10% gray pattern.'''
        ...
    
    @classmethod
    @property
    def GRAY20(cls) -> FillPattern:
        '''Represents 20% gray pattern.'''
        ...
    
    @classmethod
    @property
    def GRAY30(cls) -> FillPattern:
        '''Represents 30% gray pattern.'''
        ...
    
    @classmethod
    @property
    def GRAY40(cls) -> FillPattern:
        '''Represents 40% gray pattern.'''
        ...
    
    @classmethod
    @property
    def GRAY50(cls) -> FillPattern:
        '''Represents 50% gray pattern.'''
        ...
    
    @classmethod
    @property
    def GRAY60(cls) -> FillPattern:
        '''Represents 60% gray pattern.'''
        ...
    
    @classmethod
    @property
    def GRAY70(cls) -> FillPattern:
        '''Represents 70% gray pattern.'''
        ...
    
    @classmethod
    @property
    def GRAY75(cls) -> FillPattern:
        '''Represents 75% gray pattern.'''
        ...
    
    @classmethod
    @property
    def GRAY80(cls) -> FillPattern:
        '''Represents 80% gray pattern.'''
        ...
    
    @classmethod
    @property
    def GRAY90(cls) -> FillPattern:
        '''Represents 90% gray pattern.'''
        ...
    
    @classmethod
    @property
    def GRAY25(cls) -> FillPattern:
        '''Represents 25% gray pattern.'''
        ...
    
    @classmethod
    @property
    def LIGHT_DOWNWARD_DIAGONAL(cls) -> FillPattern:
        '''Represents light downward diagonal pattern.'''
        ...
    
    @classmethod
    @property
    def LIGHT_UPWARD_DIAGONAL(cls) -> FillPattern:
        '''Represents light upward diagonal pattern.'''
        ...
    
    @classmethod
    @property
    def DARK_DOWNWARD_DIAGONAL(cls) -> FillPattern:
        '''Represents dark downward diagonal pattern.'''
        ...
    
    @classmethod
    @property
    def DARK_UPWARD_DIAGONAL(cls) -> FillPattern:
        '''Represents dark upward diagonal pattern.'''
        ...
    
    @classmethod
    @property
    def WIDE_DOWNWARD_DIAGONAL(cls) -> FillPattern:
        '''Represents wide downward diagonal pattern.'''
        ...
    
    @classmethod
    @property
    def WIDE_UPWARD_DIAGONAL(cls) -> FillPattern:
        '''Represents wide upward diagonal pattern.'''
        ...
    
    @classmethod
    @property
    def LIGHT_VERTICAL(cls) -> FillPattern:
        '''Represents light vertical pattern.'''
        ...
    
    @classmethod
    @property
    def LIGHT_HORIZONTAL(cls) -> FillPattern:
        '''Represents light horizontal pattern.'''
        ...
    
    @classmethod
    @property
    def NARROW_VERTICAL(cls) -> FillPattern:
        '''Represents narrow vertical pattern.'''
        ...
    
    @classmethod
    @property
    def NARROW_HORIZONTAL(cls) -> FillPattern:
        '''Represents narrow horizontal pattern.'''
        ...
    
    @classmethod
    @property
    def DARK_VERTICAL(cls) -> FillPattern:
        '''Represents dark vertical pattern.'''
        ...
    
    @classmethod
    @property
    def DARK_HORIZONTAL(cls) -> FillPattern:
        '''Represents dark horizontal pattern.'''
        ...
    
    @classmethod
    @property
    def DASHED_DOWNWARD_DIAGONAL(cls) -> FillPattern:
        '''Represents dashed downward diagonal pattern.'''
        ...
    
    @classmethod
    @property
    def DASHED_UPWARD_DIAGONAL(cls) -> FillPattern:
        '''Represents dashed upward diagonal pattern.'''
        ...
    
    @classmethod
    @property
    def DASHED_VERTICAL(cls) -> FillPattern:
        '''Represents dashed vertical pattern.'''
        ...
    
    @classmethod
    @property
    def DASHED_HORIZONTAL(cls) -> FillPattern:
        '''Represents dashed horizontal pattern.'''
        ...
    
    @classmethod
    @property
    def SMALL_CONFETTI(cls) -> FillPattern:
        '''Represents small confetti pattern.'''
        ...
    
    @classmethod
    @property
    def LARGE_CONFETTI(cls) -> FillPattern:
        '''Represents large confetti pattern.'''
        ...
    
    @classmethod
    @property
    def ZIG_ZAG(cls) -> FillPattern:
        '''Represents zig zag pattern.'''
        ...
    
    @classmethod
    @property
    def WAVE(cls) -> FillPattern:
        '''Represents wave pattern.'''
        ...
    
    @classmethod
    @property
    def DIAGONAL_BRICK(cls) -> FillPattern:
        '''Represents diagonal brick pattern.'''
        ...
    
    @classmethod
    @property
    def HORIZONTAL_BRICK(cls) -> FillPattern:
        '''Represents horizontal brick pattern.'''
        ...
    
    @classmethod
    @property
    def WEAVE(cls) -> FillPattern:
        '''Represents weave pattern.'''
        ...
    
    @classmethod
    @property
    def PLAID(cls) -> FillPattern:
        '''Represents plaid pattern.'''
        ...
    
    @classmethod
    @property
    def DIVOT(cls) -> FillPattern:
        '''Represents divot pattern.'''
        ...
    
    @classmethod
    @property
    def DOTTED_GRID(cls) -> FillPattern:
        '''Represents dotted grid pattern.'''
        ...
    
    @classmethod
    @property
    def DOTTED_DIAMOND(cls) -> FillPattern:
        '''Represents dotted diamond pattern.'''
        ...
    
    @classmethod
    @property
    def SHINGLE(cls) -> FillPattern:
        '''Represents shingle pattern.'''
        ...
    
    @classmethod
    @property
    def TRELLIS(cls) -> FillPattern:
        '''Represents trellis pattern.'''
        ...
    
    @classmethod
    @property
    def SPHERE(cls) -> FillPattern:
        '''Represents sphere pattern.'''
        ...
    
    @classmethod
    @property
    def SMALL_GRID(cls) -> FillPattern:
        '''Represents small grid pattern.'''
        ...
    
    @classmethod
    @property
    def LARGE_GRID(cls) -> FillPattern:
        '''Represents large grid pattern.'''
        ...
    
    @classmethod
    @property
    def SMALL_CHECKER_BOARD(cls) -> FillPattern:
        '''Represents small checker board pattern.'''
        ...
    
    @classmethod
    @property
    def LARGE_CHECKER_BOARD(cls) -> FillPattern:
        '''Represents large checker board pattern.'''
        ...
    
    @classmethod
    @property
    def OUTLINED_DIAMOND(cls) -> FillPattern:
        '''Represents outlined diamond pattern.'''
        ...
    
    @classmethod
    @property
    def SOLID_DIAMOND(cls) -> FillPattern:
        '''Represents solid diamond pattern.'''
        ...
    
    @classmethod
    @property
    def UNKNOWN(cls) -> FillPattern:
        '''Represents unknown pattern.'''
        ...
    
    ...

class FillPictureType:
    '''Represents the picture fill type.'''
    
    @classmethod
    @property
    def STRETCH(cls) -> FillPictureType:
        '''Stretch'''
        ...
    
    @classmethod
    @property
    def STACK(cls) -> FillPictureType:
        '''Stack'''
        ...
    
    @classmethod
    @property
    def STACK_AND_SCALE(cls) -> FillPictureType:
        '''StackAndScale'''
        ...
    
    ...

class FillType:
    '''Fill format type.'''
    
    @classmethod
    @property
    def AUTOMATIC(cls) -> FillType:
        '''Represents automatic formatting type.'''
        ...
    
    @classmethod
    @property
    def NONE(cls) -> FillType:
        '''Represents none formatting type.'''
        ...
    
    @classmethod
    @property
    def SOLID(cls) -> FillType:
        '''Solid fill format.'''
        ...
    
    @classmethod
    @property
    def GRADIENT(cls) -> FillType:
        '''Gradient fill format.'''
        ...
    
    @classmethod
    @property
    def TEXTURE(cls) -> FillType:
        '''Texture fill format(includes picture fill).'''
        ...
    
    @classmethod
    @property
    def PATTERN(cls) -> FillType:
        '''Pattern fill format.'''
        ...
    
    @classmethod
    @property
    def GROUP(cls) -> FillType:
        '''Inherit the fill properties of the group.'''
        ...
    
    ...

class FormatSetType:
    '''Fill format set type.'''
    
    @classmethod
    @property
    def NONE(cls) -> FormatSetType:
        '''No Fill format.'''
        ...
    
    @classmethod
    @property
    def IS_GRADIENT_SET(cls) -> FormatSetType:
        '''Gradient fill format.'''
        ...
    
    @classmethod
    @property
    def IS_TEXTURE_SET(cls) -> FormatSetType:
        '''Texture fill format.'''
        ...
    
    @classmethod
    @property
    def IS_PATTERN_SET(cls) -> FormatSetType:
        '''Pattern fill format.'''
        ...
    
    ...

class GradientColorType:
    '''Represents the gradient color type for the specified fill.'''
    
    @classmethod
    @property
    def NONE(cls) -> GradientColorType:
        '''No gradient color'''
        ...
    
    @classmethod
    @property
    def ONE_COLOR(cls) -> GradientColorType:
        '''One gradient color'''
        ...
    
    @classmethod
    @property
    def PRESET_COLORS(cls) -> GradientColorType:
        '''Preset gradient colors'''
        ...
    
    @classmethod
    @property
    def TWO_COLORS(cls) -> GradientColorType:
        '''Two gradient colors'''
        ...
    
    ...

class GradientDirectionType:
    '''Represents all direction type of gradient.'''
    
    @classmethod
    @property
    def FROM_UPPER_LEFT_CORNER(cls) -> GradientDirectionType:
        '''FromUpperLeftCorner'''
        ...
    
    @classmethod
    @property
    def FROM_UPPER_RIGHT_CORNER(cls) -> GradientDirectionType:
        '''FromUpperRightCorner'''
        ...
    
    @classmethod
    @property
    def FROM_LOWER_LEFT_CORNER(cls) -> GradientDirectionType:
        '''FromLowerLeftCorner'''
        ...
    
    @classmethod
    @property
    def FROM_LOWER_RIGHT_CORNER(cls) -> GradientDirectionType:
        '''FromLowerRightCorner'''
        ...
    
    @classmethod
    @property
    def FROM_CENTER(cls) -> GradientDirectionType:
        '''FromCenter'''
        ...
    
    @classmethod
    @property
    def UNKNOWN(cls) -> GradientDirectionType:
        '''Unknown'''
        ...
    
    ...

class GradientFillType:
    '''Represents all Gradient fill type.'''
    
    @classmethod
    @property
    def LINEAR(cls) -> GradientFillType:
        '''Linear'''
        ...
    
    @classmethod
    @property
    def RADIAL(cls) -> GradientFillType:
        '''Radial'''
        ...
    
    @classmethod
    @property
    def RECTANGLE(cls) -> GradientFillType:
        '''Rectangle'''
        ...
    
    @classmethod
    @property
    def PATH(cls) -> GradientFillType:
        '''Path'''
        ...
    
    ...

class GradientPresetType:
    '''Represents gradient preset color type.'''
    
    @classmethod
    @property
    def BRASS(cls) -> GradientPresetType:
        '''Brass preset color'''
        ...
    
    @classmethod
    @property
    def CALM_WATER(cls) -> GradientPresetType:
        '''Calm Water preset color'''
        ...
    
    @classmethod
    @property
    def CHROME(cls) -> GradientPresetType:
        '''Chrome preset color'''
        ...
    
    @classmethod
    @property
    def CHROME_II(cls) -> GradientPresetType:
        '''Chrome II preset color'''
        ...
    
    @classmethod
    @property
    def DAYBREAK(cls) -> GradientPresetType:
        '''Daybreak preset color'''
        ...
    
    @classmethod
    @property
    def DESERT(cls) -> GradientPresetType:
        '''Desert preset color'''
        ...
    
    @classmethod
    @property
    def EARLY_SUNSET(cls) -> GradientPresetType:
        '''Early Sunset preset color'''
        ...
    
    @classmethod
    @property
    def FIRE(cls) -> GradientPresetType:
        '''Fire preset color'''
        ...
    
    @classmethod
    @property
    def FOG(cls) -> GradientPresetType:
        '''Fog preset color'''
        ...
    
    @classmethod
    @property
    def GOLD(cls) -> GradientPresetType:
        '''Gold preset color'''
        ...
    
    @classmethod
    @property
    def GOLD_II(cls) -> GradientPresetType:
        '''Gold II preset color'''
        ...
    
    @classmethod
    @property
    def HORIZON(cls) -> GradientPresetType:
        '''Horizon preset color'''
        ...
    
    @classmethod
    @property
    def LATE_SUNSET(cls) -> GradientPresetType:
        '''Late Sunset preset color'''
        ...
    
    @classmethod
    @property
    def MAHOGANY(cls) -> GradientPresetType:
        '''Mahogany preset color'''
        ...
    
    @classmethod
    @property
    def MOSS(cls) -> GradientPresetType:
        '''Moss preset color'''
        ...
    
    @classmethod
    @property
    def NIGHTFALL(cls) -> GradientPresetType:
        '''Nightfall preset color'''
        ...
    
    @classmethod
    @property
    def OCEAN(cls) -> GradientPresetType:
        '''Ocean preset color'''
        ...
    
    @classmethod
    @property
    def PARCHMENT(cls) -> GradientPresetType:
        '''Parchment preset color'''
        ...
    
    @classmethod
    @property
    def PEACOCK(cls) -> GradientPresetType:
        '''Peacock preset color'''
        ...
    
    @classmethod
    @property
    def RAINBOW(cls) -> GradientPresetType:
        '''Rainbow preset color'''
        ...
    
    @classmethod
    @property
    def RAINBOW_II(cls) -> GradientPresetType:
        '''Rainbow II preset color'''
        ...
    
    @classmethod
    @property
    def SAPPHIRE(cls) -> GradientPresetType:
        '''Sapphire preset color'''
        ...
    
    @classmethod
    @property
    def SILVER(cls) -> GradientPresetType:
        '''Silver preset color'''
        ...
    
    @classmethod
    @property
    def WHEAT(cls) -> GradientPresetType:
        '''Wheat preset color'''
        ...
    
    @classmethod
    @property
    def UNKNOWN(cls) -> GradientPresetType:
        '''Unknown preset color.
        Only for the preset color (which is not same as any known preset color) in the template workbook.'''
        ...
    
    ...

class GradientStyleType:
    '''Represents gradient shading style.'''
    
    @classmethod
    @property
    def DIAGONAL_DOWN(cls) -> GradientStyleType:
        '''Diagonal down shading style'''
        ...
    
    @classmethod
    @property
    def DIAGONAL_UP(cls) -> GradientStyleType:
        '''Diagonal up shading style'''
        ...
    
    @classmethod
    @property
    def FROM_CENTER(cls) -> GradientStyleType:
        '''From center shading style'''
        ...
    
    @classmethod
    @property
    def FROM_CORNER(cls) -> GradientStyleType:
        '''From corner shading style'''
        ...
    
    @classmethod
    @property
    def HORIZONTAL(cls) -> GradientStyleType:
        '''Horizontal shading style'''
        ...
    
    @classmethod
    @property
    def VERTICAL(cls) -> GradientStyleType:
        '''Vertical shading style'''
        ...
    
    @classmethod
    @property
    def UNKNOWN(cls) -> GradientStyleType:
        '''Unknown shading style.Only for the shading style(which is not for any member of the GradientStyleType) in the template file.'''
        ...
    
    ...

class ImageType:
    '''Specifies the type (format) of an image.'''
    
    @classmethod
    @property
    def UNKNOWN(cls) -> ImageType:
        '''An unknown image type.'''
        ...
    
    @classmethod
    @property
    def EMF(cls) -> ImageType:
        '''Windows Enhanced Metafile.'''
        ...
    
    @classmethod
    @property
    def WMF(cls) -> ImageType:
        '''Windows Metafile.'''
        ...
    
    @classmethod
    @property
    def PICT(cls) -> ImageType:
        '''Macintosh PICT.'''
        ...
    
    @classmethod
    @property
    def JPEG(cls) -> ImageType:
        '''JPEG JFIF.'''
        ...
    
    @classmethod
    @property
    def PNG(cls) -> ImageType:
        '''Portable Network Graphics.'''
        ...
    
    @classmethod
    @property
    def BMP(cls) -> ImageType:
        '''Windows Bitmap'''
        ...
    
    @classmethod
    @property
    def GIF(cls) -> ImageType:
        '''Gif'''
        ...
    
    @classmethod
    @property
    def TIFF(cls) -> ImageType:
        '''Tiff'''
        ...
    
    @classmethod
    @property
    def SVG(cls) -> ImageType:
        '''Svg'''
        ...
    
    @classmethod
    @property
    def SVM(cls) -> ImageType:
        '''Svm'''
        ...
    
    @classmethod
    @property
    def GLTF(cls) -> ImageType:
        '''glTF'''
        ...
    
    @classmethod
    @property
    def OFFICE_COMPATIBLE_EMF(cls) -> ImageType:
        '''Windows Enhanced Metafile which is more compatible with Office.'''
        ...
    
    @classmethod
    @property
    def WEB_P(cls) -> ImageType:
        '''Weppy image format'''
        ...
    
    ...

class LightRigDirectionType:
    '''Represents the light rig direction type.'''
    
    @classmethod
    @property
    def BOTTOM(cls) -> LightRigDirectionType:
        '''Bottom'''
        ...
    
    @classmethod
    @property
    def BOTTOM_LEFT(cls) -> LightRigDirectionType:
        '''Bottom left.'''
        ...
    
    @classmethod
    @property
    def BOTTOM_RIGHT(cls) -> LightRigDirectionType:
        '''Bottom Right.'''
        ...
    
    @classmethod
    @property
    def LEFT(cls) -> LightRigDirectionType:
        '''Left.'''
        ...
    
    @classmethod
    @property
    def RIGHT(cls) -> LightRigDirectionType:
        '''Right.'''
        ...
    
    @classmethod
    @property
    def TOP(cls) -> LightRigDirectionType:
        '''Top.'''
        ...
    
    @classmethod
    @property
    def TOP_LEFT(cls) -> LightRigDirectionType:
        '''Top left.'''
        ...
    
    @classmethod
    @property
    def TOP_RIGHT(cls) -> LightRigDirectionType:
        '''Top Right.'''
        ...
    
    ...

class LightRigType:
    '''Represents a preset light right that can be applied to a shape'''
    
    @classmethod
    @property
    def BALANCED(cls) -> LightRigType:
        '''Balanced'''
        ...
    
    @classmethod
    @property
    def BRIGHT_ROOM(cls) -> LightRigType:
        '''Bright room'''
        ...
    
    @classmethod
    @property
    def CHILLY(cls) -> LightRigType:
        '''Chilly'''
        ...
    
    @classmethod
    @property
    def CONTRASTING(cls) -> LightRigType:
        '''Contrasting'''
        ...
    
    @classmethod
    @property
    def FLAT(cls) -> LightRigType:
        '''Flat'''
        ...
    
    @classmethod
    @property
    def FLOOD(cls) -> LightRigType:
        '''Flood'''
        ...
    
    @classmethod
    @property
    def FREEZING(cls) -> LightRigType:
        '''Freezing'''
        ...
    
    @classmethod
    @property
    def GLOW(cls) -> LightRigType:
        '''Glow'''
        ...
    
    @classmethod
    @property
    def HARSH(cls) -> LightRigType:
        '''Harsh'''
        ...
    
    @classmethod
    @property
    def LEGACY_FLAT1(cls) -> LightRigType:
        '''LegacyFlat1'''
        ...
    
    @classmethod
    @property
    def LEGACY_FLAT2(cls) -> LightRigType:
        '''LegacyFlat2'''
        ...
    
    @classmethod
    @property
    def LEGACY_FLAT3(cls) -> LightRigType:
        '''LegacyFlat3'''
        ...
    
    @classmethod
    @property
    def LEGACY_FLAT4(cls) -> LightRigType:
        '''LegacyFlat4'''
        ...
    
    @classmethod
    @property
    def LEGACY_HARSH1(cls) -> LightRigType:
        '''LegacyHarsh1'''
        ...
    
    @classmethod
    @property
    def LEGACY_HARSH2(cls) -> LightRigType:
        '''LegacyHarsh2'''
        ...
    
    @classmethod
    @property
    def LEGACY_HARSH3(cls) -> LightRigType:
        '''LegacyHarsh3'''
        ...
    
    @classmethod
    @property
    def LEGACY_HARSH4(cls) -> LightRigType:
        '''LegacyHarsh4'''
        ...
    
    @classmethod
    @property
    def LEGACY_NORMAL1(cls) -> LightRigType:
        '''LegacyNormal1'''
        ...
    
    @classmethod
    @property
    def LEGACY_NORMAL2(cls) -> LightRigType:
        '''LegacyNormal2'''
        ...
    
    @classmethod
    @property
    def LEGACY_NORMAL3(cls) -> LightRigType:
        '''LegacyNormal3'''
        ...
    
    @classmethod
    @property
    def LEGACY_NORMAL4(cls) -> LightRigType:
        '''LegacyNormal4'''
        ...
    
    @classmethod
    @property
    def MORNING(cls) -> LightRigType:
        '''Morning'''
        ...
    
    @classmethod
    @property
    def SOFT(cls) -> LightRigType:
        '''Soft'''
        ...
    
    @classmethod
    @property
    def SUNRISE(cls) -> LightRigType:
        '''Sunrise'''
        ...
    
    @classmethod
    @property
    def SUNSET(cls) -> LightRigType:
        '''Sunset'''
        ...
    
    @classmethod
    @property
    def THREE_POINT(cls) -> LightRigType:
        '''Three point'''
        ...
    
    @classmethod
    @property
    def TWO_POINT(cls) -> LightRigType:
        '''Two point'''
        ...
    
    @classmethod
    @property
    def NONE(cls) -> LightRigType:
        '''No light rig.'''
        ...
    
    ...

class LineCapType:
    '''Represents the caps of a line'''
    
    @classmethod
    @property
    def SQUARE(cls) -> LineCapType:
        '''Square protrudes by half line width.'''
        ...
    
    @classmethod
    @property
    def ROUND(cls) -> LineCapType:
        '''Rounded ends.'''
        ...
    
    @classmethod
    @property
    def FLAT(cls) -> LineCapType:
        '''Line ends at end point.'''
        ...
    
    @classmethod
    @property
    def NONE(cls) -> LineCapType:
        '''None cap'''
        ...
    
    ...

class LineJoinType:
    '''Represents the join styles of a line.'''
    
    @classmethod
    @property
    def ROUND(cls) -> LineJoinType:
        '''Round joint'''
        ...
    
    @classmethod
    @property
    def BEVEL(cls) -> LineJoinType:
        '''Bevel joint'''
        ...
    
    @classmethod
    @property
    def MITER(cls) -> LineJoinType:
        '''Miter joint'''
        ...
    
    @classmethod
    @property
    def NONE(cls) -> LineJoinType:
        '''None joint'''
        ...
    
    ...

class LineType:
    '''Enumerates the type of :py:class:`aspose.cells.drawing.Picture` border or :py:class:`aspose.cells.charts.Chart` line.'''
    
    @classmethod
    @property
    def DARK_GRAY(cls) -> LineType:
        '''Represents a dark gray line.'''
        ...
    
    @classmethod
    @property
    def DASH(cls) -> LineType:
        '''Represent a dash line.'''
        ...
    
    @classmethod
    @property
    def DASH_DOT(cls) -> LineType:
        '''Represents a dash-dot line'''
        ...
    
    @classmethod
    @property
    def DASH_DOT_DOT(cls) -> LineType:
        '''Represents a dash-dot-dot line.'''
        ...
    
    @classmethod
    @property
    def DOT(cls) -> LineType:
        '''Represents a dotted line.'''
        ...
    
    @classmethod
    @property
    def LIGHT_GRAY(cls) -> LineType:
        '''Represents a light gray line.'''
        ...
    
    @classmethod
    @property
    def MEDIUM_GRAY(cls) -> LineType:
        '''Represents a medium gray line.'''
        ...
    
    @classmethod
    @property
    def SOLID(cls) -> LineType:
        '''Represent a solid line.'''
        ...
    
    ...

class MirrorType:
    '''Represents mirror type of texture fill'''
    
    @classmethod
    @property
    def NONE(cls) -> MirrorType:
        '''None'''
        ...
    
    @classmethod
    @property
    def HORIZONAL(cls) -> MirrorType:
        '''Horizonal'''
        ...
    
    @classmethod
    @property
    def VERTICAL(cls) -> MirrorType:
        '''Vertical'''
        ...
    
    @classmethod
    @property
    def BOTH(cls) -> MirrorType:
        '''Both'''
        ...
    
    ...

class MsoArrowheadLength:
    '''Enumerates the line end width of the shape border line.'''
    
    @classmethod
    @property
    def SHORT(cls) -> MsoArrowheadLength:
        '''Short line end length'''
        ...
    
    @classmethod
    @property
    def MEDIUM(cls) -> MsoArrowheadLength:
        '''Medium line end length'''
        ...
    
    @classmethod
    @property
    def LONG(cls) -> MsoArrowheadLength:
        '''Long line end length'''
        ...
    
    ...

class MsoArrowheadStyle:
    '''Enumerates the line end type of the shape border line.'''
    
    @classmethod
    @property
    def NONE(cls) -> MsoArrowheadStyle:
        '''No line end type.'''
        ...
    
    @classmethod
    @property
    def ARROW(cls) -> MsoArrowheadStyle:
        '''Arrow line end type.'''
        ...
    
    @classmethod
    @property
    def ARROW_STEALTH(cls) -> MsoArrowheadStyle:
        '''Arrow Stealth line end type.'''
        ...
    
    @classmethod
    @property
    def ARROW_DIAMOND(cls) -> MsoArrowheadStyle:
        '''Arrow Diamond Line end type.'''
        ...
    
    @classmethod
    @property
    def ARROW_OVAL(cls) -> MsoArrowheadStyle:
        '''Arrow Oval line end type.'''
        ...
    
    @classmethod
    @property
    def ARROW_OPEN(cls) -> MsoArrowheadStyle:
        '''Arrow Open line end type.'''
        ...
    
    ...

class MsoArrowheadWidth:
    '''Enumerates the line end width of the shape border line.'''
    
    @classmethod
    @property
    def NARROW(cls) -> MsoArrowheadWidth:
        '''Short line end width.'''
        ...
    
    @classmethod
    @property
    def MEDIUM(cls) -> MsoArrowheadWidth:
        '''Medium line end width.'''
        ...
    
    @classmethod
    @property
    def WIDE(cls) -> MsoArrowheadWidth:
        '''Wide line end width.'''
        ...
    
    ...

class MsoDrawingType:
    '''Represents office drawing objects type.'''
    
    @classmethod
    @property
    def GROUP(cls) -> MsoDrawingType:
        '''Group'''
        ...
    
    @classmethod
    @property
    def LINE(cls) -> MsoDrawingType:
        '''Line'''
        ...
    
    @classmethod
    @property
    def RECTANGLE(cls) -> MsoDrawingType:
        '''Rectangle'''
        ...
    
    @classmethod
    @property
    def OVAL(cls) -> MsoDrawingType:
        '''Oval'''
        ...
    
    @classmethod
    @property
    def ARC(cls) -> MsoDrawingType:
        '''Arc'''
        ...
    
    @classmethod
    @property
    def CHART(cls) -> MsoDrawingType:
        '''Chart'''
        ...
    
    @classmethod
    @property
    def TEXT_BOX(cls) -> MsoDrawingType:
        '''TextBox'''
        ...
    
    @classmethod
    @property
    def BUTTON(cls) -> MsoDrawingType:
        '''Button'''
        ...
    
    @classmethod
    @property
    def PICTURE(cls) -> MsoDrawingType:
        '''Picture'''
        ...
    
    @classmethod
    @property
    def POLYGON(cls) -> MsoDrawingType:
        '''Polygon'''
        ...
    
    @classmethod
    @property
    def CHECK_BOX(cls) -> MsoDrawingType:
        '''CheckBox'''
        ...
    
    @classmethod
    @property
    def RADIO_BUTTON(cls) -> MsoDrawingType:
        '''RadioButton'''
        ...
    
    @classmethod
    @property
    def LABEL(cls) -> MsoDrawingType:
        '''Label'''
        ...
    
    @classmethod
    @property
    def DIALOG_BOX(cls) -> MsoDrawingType:
        '''DialogBox'''
        ...
    
    @classmethod
    @property
    def SPINNER(cls) -> MsoDrawingType:
        '''Spinner'''
        ...
    
    @classmethod
    @property
    def SCROLL_BAR(cls) -> MsoDrawingType:
        '''ScrollBar'''
        ...
    
    @classmethod
    @property
    def LIST_BOX(cls) -> MsoDrawingType:
        '''ListBox'''
        ...
    
    @classmethod
    @property
    def GROUP_BOX(cls) -> MsoDrawingType:
        '''GroupBox'''
        ...
    
    @classmethod
    @property
    def COMBO_BOX(cls) -> MsoDrawingType:
        '''ComboBox'''
        ...
    
    @classmethod
    @property
    def COMMENT(cls) -> MsoDrawingType:
        '''Comment'''
        ...
    
    @classmethod
    @property
    def OLE_OBJECT(cls) -> MsoDrawingType:
        '''OleObject'''
        ...
    
    @classmethod
    @property
    def CELLS_DRAWING(cls) -> MsoDrawingType:
        '''Only for preserving the drawing object in the template file.'''
        ...
    
    @classmethod
    @property
    def UNKNOWN(cls) -> MsoDrawingType:
        '''Only for preserving the drawing object in the xlsx file.'''
        ...
    
    @classmethod
    @property
    def SLICER(cls) -> MsoDrawingType:
        '''Slicer'''
        ...
    
    @classmethod
    @property
    def WEB_EXTENSION(cls) -> MsoDrawingType:
        '''Web extension'''
        ...
    
    @classmethod
    @property
    def SMART_ART(cls) -> MsoDrawingType:
        '''Smart Art'''
        ...
    
    @classmethod
    @property
    def CUSTOM_XML(cls) -> MsoDrawingType:
        '''Custom xml shape ,such as Ink.'''
        ...
    
    @classmethod
    @property
    def TIMELINE(cls) -> MsoDrawingType:
        '''Timeline'''
        ...
    
    @classmethod
    @property
    def MODEL_3D(cls) -> MsoDrawingType:
        '''3D Model'''
        ...
    
    ...

class MsoLineDashStyle:
    '''Represents style of dash drawing lines.'''
    
    @classmethod
    @property
    def DASH(cls) -> MsoLineDashStyle:
        '''Represent a dash line.'''
        ...
    
    @classmethod
    @property
    def DASH_DOT(cls) -> MsoLineDashStyle:
        '''Represents a dash-dot line.'''
        ...
    
    @classmethod
    @property
    def DASH_DOT_DOT(cls) -> MsoLineDashStyle:
        '''Represents a dash-dot-dot line.'''
        ...
    
    @classmethod
    @property
    def DASH_LONG_DASH(cls) -> MsoLineDashStyle:
        '''Represents a long dash-short dash line.'''
        ...
    
    @classmethod
    @property
    def DASH_LONG_DASH_DOT(cls) -> MsoLineDashStyle:
        '''Represents a long dash-short dash-dot line.'''
        ...
    
    @classmethod
    @property
    def ROUND_DOT(cls) -> MsoLineDashStyle:
        '''Represents a round-dot line.'''
        ...
    
    @classmethod
    @property
    def SOLID(cls) -> MsoLineDashStyle:
        '''Represent a solid line.'''
        ...
    
    @classmethod
    @property
    def SQUARE_DOT(cls) -> MsoLineDashStyle:
        '''Represents a square-dot line.'''
        ...
    
    @classmethod
    @property
    def CUSTOM(cls) -> MsoLineDashStyle:
        '''Custom dash style.'''
        ...
    
    ...

class MsoLineStyle:
    '''Represents style of drawing lines.'''
    
    @classmethod
    @property
    def SINGLE(cls) -> MsoLineStyle:
        '''Single line (of width lineWidth)'''
        ...
    
    @classmethod
    @property
    def THICK_BETWEEN_THIN(cls) -> MsoLineStyle:
        '''Three lines, thin, thick, thin'''
        ...
    
    @classmethod
    @property
    def THIN_THICK(cls) -> MsoLineStyle:
        '''Double lines, one thin, one thick'''
        ...
    
    @classmethod
    @property
    def THICK_THIN(cls) -> MsoLineStyle:
        '''Double lines, one thick, one thin'''
        ...
    
    @classmethod
    @property
    def THIN_THIN(cls) -> MsoLineStyle:
        '''Double lines of equal width'''
        ...
    
    ...

class MsoPresetTextEffect:
    '''Represents preset text effect type of WordArt.'''
    
    @classmethod
    @property
    def TEXT_EFFECT1(cls) -> MsoPresetTextEffect:
        '''TextEffect1'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT2(cls) -> MsoPresetTextEffect:
        '''TextEffect2'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT3(cls) -> MsoPresetTextEffect:
        '''TextEffect3'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT4(cls) -> MsoPresetTextEffect:
        '''TextEffect4'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT5(cls) -> MsoPresetTextEffect:
        '''TextEffect5'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT6(cls) -> MsoPresetTextEffect:
        '''TextEffect6'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT7(cls) -> MsoPresetTextEffect:
        '''TextEffect7'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT8(cls) -> MsoPresetTextEffect:
        '''TextEffect8'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT9(cls) -> MsoPresetTextEffect:
        '''TextEffect9'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT10(cls) -> MsoPresetTextEffect:
        '''TextEffect10'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT11(cls) -> MsoPresetTextEffect:
        '''TextEffect11'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT12(cls) -> MsoPresetTextEffect:
        '''TextEffect12'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT13(cls) -> MsoPresetTextEffect:
        '''TextEffect13'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT14(cls) -> MsoPresetTextEffect:
        '''TextEffect14'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT15(cls) -> MsoPresetTextEffect:
        '''TextEffect15'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT16(cls) -> MsoPresetTextEffect:
        '''TextEffect16'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT17(cls) -> MsoPresetTextEffect:
        '''TextEffect17'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT18(cls) -> MsoPresetTextEffect:
        '''TextEffect18'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT19(cls) -> MsoPresetTextEffect:
        '''TextEffect19'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT20(cls) -> MsoPresetTextEffect:
        '''TextEffect20'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT21(cls) -> MsoPresetTextEffect:
        '''TextEffect21'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT22(cls) -> MsoPresetTextEffect:
        '''TextEffect22'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT23(cls) -> MsoPresetTextEffect:
        '''TextEffect23'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT24(cls) -> MsoPresetTextEffect:
        '''TextEffect24'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT25(cls) -> MsoPresetTextEffect:
        '''TextEffect25'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT26(cls) -> MsoPresetTextEffect:
        '''TextEffect26'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT27(cls) -> MsoPresetTextEffect:
        '''TextEffect27'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT28(cls) -> MsoPresetTextEffect:
        '''TextEffect28'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT29(cls) -> MsoPresetTextEffect:
        '''TextEffect29'''
        ...
    
    @classmethod
    @property
    def TEXT_EFFECT30(cls) -> MsoPresetTextEffect:
        '''TextEffect30'''
        ...
    
    ...

class MsoPresetTextEffectShape:
    '''Represents preset text effect shape type of WordArt.'''
    
    @classmethod
    @property
    def PLAIN_TEXT(cls) -> MsoPresetTextEffectShape:
        '''PlainText'''
        ...
    
    @classmethod
    @property
    def STOP(cls) -> MsoPresetTextEffectShape:
        '''Stop'''
        ...
    
    @classmethod
    @property
    def TRIANGLE_UP(cls) -> MsoPresetTextEffectShape:
        '''TriangleUp'''
        ...
    
    @classmethod
    @property
    def TRIANGLE_DOWN(cls) -> MsoPresetTextEffectShape:
        '''TriangleDown'''
        ...
    
    @classmethod
    @property
    def CHEVRON_UP(cls) -> MsoPresetTextEffectShape:
        '''ChevronUp'''
        ...
    
    @classmethod
    @property
    def CHEVRON_DOWN(cls) -> MsoPresetTextEffectShape:
        '''ChevronDown'''
        ...
    
    @classmethod
    @property
    def RING_INSIDE(cls) -> MsoPresetTextEffectShape:
        '''RingInside'''
        ...
    
    @classmethod
    @property
    def RING_OUTSIDE(cls) -> MsoPresetTextEffectShape:
        '''RingOutside'''
        ...
    
    @classmethod
    @property
    def ARCH_UP_CURVE(cls) -> MsoPresetTextEffectShape:
        '''ArchUpCurve'''
        ...
    
    @classmethod
    @property
    def ARCH_DOWN_CURVE(cls) -> MsoPresetTextEffectShape:
        '''ArchDownCurve'''
        ...
    
    @classmethod
    @property
    def CIRCLE_CURVE(cls) -> MsoPresetTextEffectShape:
        '''CircleCurve'''
        ...
    
    @classmethod
    @property
    def BUTTON_CURVE(cls) -> MsoPresetTextEffectShape:
        '''ButtonCurve'''
        ...
    
    @classmethod
    @property
    def ARCH_UP_POUR(cls) -> MsoPresetTextEffectShape:
        '''ArchUpPour'''
        ...
    
    @classmethod
    @property
    def ARCH_DOWN_POUR(cls) -> MsoPresetTextEffectShape:
        '''ArchDownPour'''
        ...
    
    @classmethod
    @property
    def CIRCLE_POUR(cls) -> MsoPresetTextEffectShape:
        '''CirclePour'''
        ...
    
    @classmethod
    @property
    def BUTTON_POUR(cls) -> MsoPresetTextEffectShape:
        '''ButtonPour'''
        ...
    
    @classmethod
    @property
    def CURVE_UP(cls) -> MsoPresetTextEffectShape:
        '''CurveUp'''
        ...
    
    @classmethod
    @property
    def CURVE_DOWN(cls) -> MsoPresetTextEffectShape:
        '''CurveDown'''
        ...
    
    @classmethod
    @property
    def CAN_UP(cls) -> MsoPresetTextEffectShape:
        '''CanUp'''
        ...
    
    @classmethod
    @property
    def CAN_DOWN(cls) -> MsoPresetTextEffectShape:
        '''CanDown'''
        ...
    
    @classmethod
    @property
    def WAVE1(cls) -> MsoPresetTextEffectShape:
        '''Wave1'''
        ...
    
    @classmethod
    @property
    def WAVE2(cls) -> MsoPresetTextEffectShape:
        '''Wave2'''
        ...
    
    @classmethod
    @property
    def DOUBLE_WAVE1(cls) -> MsoPresetTextEffectShape:
        '''DoubleWave1'''
        ...
    
    @classmethod
    @property
    def DOUBLE_WAVE2(cls) -> MsoPresetTextEffectShape:
        '''DoubleWave2'''
        ...
    
    @classmethod
    @property
    def INFLATE(cls) -> MsoPresetTextEffectShape:
        '''Inflate'''
        ...
    
    @classmethod
    @property
    def DEFLATE(cls) -> MsoPresetTextEffectShape:
        '''Deflate'''
        ...
    
    @classmethod
    @property
    def INFLATE_BOTTOM(cls) -> MsoPresetTextEffectShape:
        '''InflateBottom'''
        ...
    
    @classmethod
    @property
    def DEFLATE_BOTTOM(cls) -> MsoPresetTextEffectShape:
        '''DeflateBottom'''
        ...
    
    @classmethod
    @property
    def INFLATE_TOP(cls) -> MsoPresetTextEffectShape:
        '''InflateTop'''
        ...
    
    @classmethod
    @property
    def DEFLATE_TOP(cls) -> MsoPresetTextEffectShape:
        '''DeflateTop'''
        ...
    
    @classmethod
    @property
    def DEFLATE_INFLATE(cls) -> MsoPresetTextEffectShape:
        '''DeflateInflate'''
        ...
    
    @classmethod
    @property
    def DEFLATE_INFLATE_DEFLATE(cls) -> MsoPresetTextEffectShape:
        '''DeflateInflateDeflate'''
        ...
    
    @classmethod
    @property
    def FADE_RIGHT(cls) -> MsoPresetTextEffectShape:
        '''FadeRight'''
        ...
    
    @classmethod
    @property
    def FADE_LEFT(cls) -> MsoPresetTextEffectShape:
        '''FadeLeft'''
        ...
    
    @classmethod
    @property
    def FADE_UP(cls) -> MsoPresetTextEffectShape:
        '''FadeUp'''
        ...
    
    @classmethod
    @property
    def FADE_DOWN(cls) -> MsoPresetTextEffectShape:
        '''FadeDown'''
        ...
    
    @classmethod
    @property
    def SLANT_UP(cls) -> MsoPresetTextEffectShape:
        '''SlantUp'''
        ...
    
    @classmethod
    @property
    def SLANT_DOWN(cls) -> MsoPresetTextEffectShape:
        '''SlantDown'''
        ...
    
    @classmethod
    @property
    def CASCADE_UP(cls) -> MsoPresetTextEffectShape:
        '''CascadeUp'''
        ...
    
    @classmethod
    @property
    def CASCADE_DOWN(cls) -> MsoPresetTextEffectShape:
        '''CascadeDown'''
        ...
    
    @classmethod
    @property
    def MIXED(cls) -> MsoPresetTextEffectShape:
        '''Mixed'''
        ...
    
    ...

class PlacementType:
    '''Represents the way the drawing object is attached to the cells below it.'''
    
    @classmethod
    @property
    def FREE_FLOATING(cls) -> PlacementType:
        '''Don't move or size with cells.'''
        ...
    
    @classmethod
    @property
    def MOVE(cls) -> PlacementType:
        '''Move but don't size with cells.'''
        ...
    
    @classmethod
    @property
    def MOVE_AND_SIZE(cls) -> PlacementType:
        '''Move and size with cells.'''
        ...
    
    ...

class PresetCameraType:
    '''Represent different algorithmic methods for setting all camera properties, including position.'''
    
    @classmethod
    @property
    def ISOMETRIC_BOTTOM_DOWN(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def ISOMETRIC_BOTTOM_UP(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def ISOMETRIC_LEFT_DOWN(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def ISOMETRIC_LEFT_UP(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def ISOMETRIC_OFF_AXIS_1_LEFT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def ISOMETRIC_OFF_AXIS_1_RIGHT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def ISOMETRIC_OFF_AXIS_1_TOP(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def ISOMETRIC_OFF_AXIS_2_LEFT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def ISOMETRIC_OFF_AXIS_2_RIGHT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def ISOMETRIC_OFF_AXIS_2_TOP(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def ISOMETRIC_OFF_AXIS_3_BOTTOM(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def ISOMETRIC_OFF_AXIS_3_LEFT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def ISOMETRIC_OFF_AXIS_3_RIGHT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def ISOMETRIC_OFF_AXIS_4_BOTTOM(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def ISOMETRIC_OFF_AXIS_4_LEFT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def ISOMETRIC_OFF_AXIS_4_RIGHT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def ISOMETRIC_RIGHT_DOWN(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def ISOMETRIC_RIGHT_UP(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def ISOMETRIC_TOP_DOWN(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def ISOMETRIC_TOP_UP(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def LEGACY_OBLIQUE_BOTTOM(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def LEGACY_OBLIQUE_BOTTOM_LEFT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def LEGACY_OBLIQUE_BOTTOM_RIGHT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def LEGACY_OBLIQUE_FRONT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def LEGACY_OBLIQUE_LEFT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def LEGACY_OBLIQUE_RIGHT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def LEGACY_OBLIQUE_TOP(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def LEGACY_OBLIQUE_TOP_LEFT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def LEGACY_OBLIQUE_TOP_RIGHT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def LEGACY_PERSPECTIVE_BOTTOM(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def LEGACY_PERSPECTIVE_BOTTOM_LEFT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def LEGACY_PERSPECTIVE_BOTTOM_RIGHT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def LEGACY_PERSPECTIVE_FRONT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def LEGACY_PERSPECTIVE_LEFT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def LEGACY_PERSPECTIVE_RIGHT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def LEGACY_PERSPECTIVE_TOP(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def LEGACY_PERSPECTIVE_TOP_LEFT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def LEGACY_PERSPECTIVE_TOP_RIGHT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def OBLIQUE_BOTTOM(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def OBLIQUE_BOTTOM_LEFT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def OBLIQUE_BOTTOM_RIGHT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def OBLIQUE_LEFT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def OBLIQUE_RIGHT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def OBLIQUE_TOP(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def OBLIQUE_TOP_LEFT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def OBLIQUE_TOP_RIGHT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def ORTHOGRAPHIC_FRONT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def PERSPECTIVE_ABOVE(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def PERSPECTIVE_ABOVE_LEFT_FACING(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def PERSPECTIVE_ABOVE_RIGHT_FACING(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def PERSPECTIVE_BELOW(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def PERSPECTIVE_CONTRASTING_LEFT_FACING(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def PERSPECTIVE_CONTRASTING_RIGHT_FACING(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def PERSPECTIVE_FRONT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def PERSPECTIVE_HEROIC_EXTREME_LEFT_FACING(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def PERSPECTIVE_HEROIC_EXTREME_RIGHT_FACING(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def PERSPECTIVE_HEROIC_LEFT_FACING(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def PERSPECTIVE_HEROIC_RIGHT_FACING(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def PERSPECTIVE_LEFT(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def PERSPECTIVE_RELAXED(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def PERSPECTIVE_RELAXED_MODERATELY(cls) -> PresetCameraType:
        ...
    
    @classmethod
    @property
    def PERSPECTIVE_RIGHT(cls) -> PresetCameraType:
        ...
    
    ...

class PresetMaterialType:
    '''Describes surface appearance of a shape.'''
    
    @classmethod
    @property
    def CLEAR(cls) -> PresetMaterialType:
        '''Clear'''
        ...
    
    @classmethod
    @property
    def DARK_EDGE(cls) -> PresetMaterialType:
        '''Dark edge'''
        ...
    
    @classmethod
    @property
    def FLAT(cls) -> PresetMaterialType:
        '''Flat'''
        ...
    
    @classmethod
    @property
    def LEGACY_MATTE(cls) -> PresetMaterialType:
        '''Legacy matte'''
        ...
    
    @classmethod
    @property
    def LEGACY_METAL(cls) -> PresetMaterialType:
        '''Legacy metal'''
        ...
    
    @classmethod
    @property
    def LEGACY_PLASTIC(cls) -> PresetMaterialType:
        '''Legacy plastic'''
        ...
    
    @classmethod
    @property
    def LEGACY_WIREFRAME(cls) -> PresetMaterialType:
        '''Legacy wireframe'''
        ...
    
    @classmethod
    @property
    def MATTE(cls) -> PresetMaterialType:
        '''Matte'''
        ...
    
    @classmethod
    @property
    def METAL(cls) -> PresetMaterialType:
        '''Metal'''
        ...
    
    @classmethod
    @property
    def PLASTIC(cls) -> PresetMaterialType:
        '''Plastic'''
        ...
    
    @classmethod
    @property
    def POWDER(cls) -> PresetMaterialType:
        '''Powder'''
        ...
    
    @classmethod
    @property
    def SOFT_EDGE(cls) -> PresetMaterialType:
        '''Soft edge'''
        ...
    
    @classmethod
    @property
    def SOFT_METAL(cls) -> PresetMaterialType:
        '''Soft metal'''
        ...
    
    @classmethod
    @property
    def TRANSLUCENT_POWDER(cls) -> PresetMaterialType:
        '''Translucent powder'''
        ...
    
    @classmethod
    @property
    def WARM_MATTE(cls) -> PresetMaterialType:
        '''Warm matte'''
        ...
    
    ...

class PresetShadowType:
    '''Represents preset shadow type.'''
    
    @classmethod
    @property
    def NO_SHADOW(cls) -> PresetShadowType:
        '''No shadow.'''
        ...
    
    @classmethod
    @property
    def CUSTOM(cls) -> PresetShadowType:
        '''Custom shadow.'''
        ...
    
    @classmethod
    @property
    def OFFSET_DIAGONAL_BOTTOM_RIGHT(cls) -> PresetShadowType:
        '''Outer shadow offset diagonal bottom right.'''
        ...
    
    @classmethod
    @property
    def OFFSET_BOTTOM(cls) -> PresetShadowType:
        '''Outer shadow offset bottom.'''
        ...
    
    @classmethod
    @property
    def OFFSET_DIAGONAL_BOTTOM_LEFT(cls) -> PresetShadowType:
        '''Outer shadow offset diagonal bottom left.'''
        ...
    
    @classmethod
    @property
    def OFFSET_RIGHT(cls) -> PresetShadowType:
        '''Outer shadow offset right.'''
        ...
    
    @classmethod
    @property
    def OFFSET_CENTER(cls) -> PresetShadowType:
        '''Outer shadow offset center.'''
        ...
    
    @classmethod
    @property
    def OFFSET_LEFT(cls) -> PresetShadowType:
        '''Outer shadow offset left.'''
        ...
    
    @classmethod
    @property
    def OFFSET_DIAGONAL_TOP_RIGHT(cls) -> PresetShadowType:
        '''Outer shadow offset diagonal top right.'''
        ...
    
    @classmethod
    @property
    def OFFSET_TOP(cls) -> PresetShadowType:
        '''Outer shadow offset top.'''
        ...
    
    @classmethod
    @property
    def OFFSET_DIAGONAL_TOP_LEFT(cls) -> PresetShadowType:
        '''Outer shadow offset diagonal top left.'''
        ...
    
    @classmethod
    @property
    def INSIDE_DIAGONAL_TOP_LEFT(cls) -> PresetShadowType:
        '''Inner shadow inside diagonal top Left.'''
        ...
    
    @classmethod
    @property
    def INSIDE_TOP(cls) -> PresetShadowType:
        '''Inner shadow inside top.'''
        ...
    
    @classmethod
    @property
    def INSIDE_DIAGONAL_TOP_RIGHT(cls) -> PresetShadowType:
        '''Inner shadow inside diagonal top right.'''
        ...
    
    @classmethod
    @property
    def INSIDE_LEFT(cls) -> PresetShadowType:
        '''Inner shadow inside left.'''
        ...
    
    @classmethod
    @property
    def INSIDE_CENTER(cls) -> PresetShadowType:
        '''Inner shadow inside center.'''
        ...
    
    @classmethod
    @property
    def INSIDE_RIGHT(cls) -> PresetShadowType:
        '''Inner shadow inside right.'''
        ...
    
    @classmethod
    @property
    def INSIDE_DIAGONAL_BOTTOM_LEFT(cls) -> PresetShadowType:
        '''Inner shadow inside diagonal bottom left.'''
        ...
    
    @classmethod
    @property
    def INSIDE_BOTTOM(cls) -> PresetShadowType:
        '''Inner shadow inside bottom.'''
        ...
    
    @classmethod
    @property
    def INSIDE_DIAGONAL_BOTTOM_RIGHT(cls) -> PresetShadowType:
        '''Inner shadow inside diagonal bottom right.'''
        ...
    
    @classmethod
    @property
    def PERSPECTIVE_DIAGONAL_UPPER_LEFT(cls) -> PresetShadowType:
        '''Outer shadow perspective diagonal upper left.'''
        ...
    
    @classmethod
    @property
    def PERSPECTIVE_DIAGONAL_UPPER_RIGHT(cls) -> PresetShadowType:
        '''Outer shadow perspective diagonal upper right.'''
        ...
    
    @classmethod
    @property
    def BELOW(cls) -> PresetShadowType:
        '''Outer shadow below.'''
        ...
    
    @classmethod
    @property
    def PERSPECTIVE_DIAGONAL_LOWER_LEFT(cls) -> PresetShadowType:
        '''Outer shadow perspective diagonal lower left.'''
        ...
    
    @classmethod
    @property
    def PERSPECTIVE_DIAGONAL_LOWER_RIGHT(cls) -> PresetShadowType:
        '''Outer shadow perspective diagonal lower right.'''
        ...
    
    ...

class PresetThemeGradientType:
    '''Represents the preset theme gradient type.'''
    
    @classmethod
    @property
    def LIGHT_GRADIENT(cls) -> PresetThemeGradientType:
        '''Light gradient'''
        ...
    
    @classmethod
    @property
    def TOP_SPOTLIGHT(cls) -> PresetThemeGradientType:
        '''Top spotlight'''
        ...
    
    @classmethod
    @property
    def MEDIUM_GRADIENT(cls) -> PresetThemeGradientType:
        '''Medium gradient'''
        ...
    
    @classmethod
    @property
    def BOTTOM_SPOTLIGHT(cls) -> PresetThemeGradientType:
        '''Bottom spotlight'''
        ...
    
    @classmethod
    @property
    def RADIAL_GRADIENT(cls) -> PresetThemeGradientType:
        '''Radial gradient'''
        ...
    
    ...

class PresetWordArtStyle:
    '''Represents the preset WordArt styles.'''
    
    @classmethod
    @property
    def WORD_ART_STYLE1(cls) -> PresetWordArtStyle:
        '''Fill - Black, Text 1, Shadow'''
        ...
    
    @classmethod
    @property
    def WORD_ART_STYLE2(cls) -> PresetWordArtStyle:
        '''Fill - Blue, Accent 1, Shadow'''
        ...
    
    @classmethod
    @property
    def WORD_ART_STYLE3(cls) -> PresetWordArtStyle:
        '''Fill - Orange, Accent 2, Outline - Accent 2'''
        ...
    
    @classmethod
    @property
    def WORD_ART_STYLE4(cls) -> PresetWordArtStyle:
        '''Fill - White, Outline - Accent 1, Shadow'''
        ...
    
    @classmethod
    @property
    def WORD_ART_STYLE5(cls) -> PresetWordArtStyle:
        '''Fill - Gold, Accent 4, Soft Bevel'''
        ...
    
    @classmethod
    @property
    def WORD_ART_STYLE6(cls) -> PresetWordArtStyle:
        '''Gradient Fill - Gray'''
        ...
    
    @classmethod
    @property
    def WORD_ART_STYLE7(cls) -> PresetWordArtStyle:
        '''Gradient Fill - Blue, Accent 1, Reflection'''
        ...
    
    @classmethod
    @property
    def WORD_ART_STYLE8(cls) -> PresetWordArtStyle:
        '''Gradient Fill - Gold, Accent 4, Outline - Accent 4'''
        ...
    
    @classmethod
    @property
    def WORD_ART_STYLE9(cls) -> PresetWordArtStyle:
        '''Fill - White, Outline - Accent 1, Glow - Accent 1'''
        ...
    
    @classmethod
    @property
    def WORD_ART_STYLE10(cls) -> PresetWordArtStyle:
        '''Fill - Gray-50%, Accent 3, Sharp Bevel'''
        ...
    
    @classmethod
    @property
    def WORD_ART_STYLE11(cls) -> PresetWordArtStyle:
        '''Fill - Black, Text 1, Outline - Background 1, Hard Shadow - Background 1'''
        ...
    
    @classmethod
    @property
    def WORD_ART_STYLE12(cls) -> PresetWordArtStyle:
        '''Fill - Black, Text 1, Outline - Background 1, Hard Shadow - Accent 1'''
        ...
    
    @classmethod
    @property
    def WORD_ART_STYLE13(cls) -> PresetWordArtStyle:
        '''Fill - Blue, Accent 1, Outline - Background 1, Hard Shadow - Accent 1'''
        ...
    
    @classmethod
    @property
    def WORD_ART_STYLE14(cls) -> PresetWordArtStyle:
        '''Fill - White, Outline - Accent 2, Hard Shadow - Accent 2'''
        ...
    
    @classmethod
    @property
    def WORD_ART_STYLE15(cls) -> PresetWordArtStyle:
        '''Fill - Gray-25%, Background 2, Inner Shadow'''
        ...
    
    @classmethod
    @property
    def WORD_ART_STYLE16(cls) -> PresetWordArtStyle:
        '''Pattern Fill - White, Text 2, Dark Upward Diagonal, Shadow'''
        ...
    
    @classmethod
    @property
    def WORD_ART_STYLE17(cls) -> PresetWordArtStyle:
        '''Pattern Fill - Gray-50%, Accent 3, Narrow Horizontal, Inner Shadow'''
        ...
    
    @classmethod
    @property
    def WORD_ART_STYLE18(cls) -> PresetWordArtStyle:
        '''Fill - Blue, Accent 1, 50%, Hard Shadow - Accent 1'''
        ...
    
    @classmethod
    @property
    def WORD_ART_STYLE19(cls) -> PresetWordArtStyle:
        '''Pattern Fill - Blue, Accent 1, Light Downward Diagonal, Outline - Accent 1'''
        ...
    
    @classmethod
    @property
    def WORD_ART_STYLE20(cls) -> PresetWordArtStyle:
        '''Pattern Fill - Blue-Gray, Text 2, Dark Upward Diagonal, Hard Shadow - Text 2'''
        ...
    
    ...

class RectangleAlignmentType:
    '''Represents how to position two rectangles relative to each other.'''
    
    @classmethod
    @property
    def BOTTOM(cls) -> RectangleAlignmentType:
        '''Bottom'''
        ...
    
    @classmethod
    @property
    def BOTTOM_LEFT(cls) -> RectangleAlignmentType:
        '''BottomLeft'''
        ...
    
    @classmethod
    @property
    def BOTTOM_RIGHT(cls) -> RectangleAlignmentType:
        '''BottomRight'''
        ...
    
    @classmethod
    @property
    def CENTER(cls) -> RectangleAlignmentType:
        '''Center'''
        ...
    
    @classmethod
    @property
    def LEFT(cls) -> RectangleAlignmentType:
        '''Left'''
        ...
    
    @classmethod
    @property
    def RIGHT(cls) -> RectangleAlignmentType:
        '''Right'''
        ...
    
    @classmethod
    @property
    def TOP(cls) -> RectangleAlignmentType:
        '''Top'''
        ...
    
    @classmethod
    @property
    def TOP_LEFT(cls) -> RectangleAlignmentType:
        '''TopLeft'''
        ...
    
    @classmethod
    @property
    def TOP_RIGHT(cls) -> RectangleAlignmentType:
        '''TopRight'''
        ...
    
    ...

class ReflectionEffectType:
    '''Represents the effect type of reflection.'''
    
    @classmethod
    @property
    def NONE(cls) -> ReflectionEffectType:
        '''No reflection effect.'''
        ...
    
    @classmethod
    @property
    def CUSTOM(cls) -> ReflectionEffectType:
        '''Custom reflection effect.'''
        ...
    
    @classmethod
    @property
    def TIGHT_REFLECTION_TOUCHING(cls) -> ReflectionEffectType:
        '''Tight reflection, touching.'''
        ...
    
    @classmethod
    @property
    def HALF_REFLECTION_TOUCHING(cls) -> ReflectionEffectType:
        '''Half reflection, touching.'''
        ...
    
    @classmethod
    @property
    def FULL_REFLECTION_TOUCHING(cls) -> ReflectionEffectType:
        '''Full reflection, touching.'''
        ...
    
    @classmethod
    @property
    def TIGHT_REFLECTION_4_PT_OFFSET(cls) -> ReflectionEffectType:
        '''Tight reflection, 4 pt offset.'''
        ...
    
    @classmethod
    @property
    def HALF_REFLECTION_4_PT_OFFSET(cls) -> ReflectionEffectType:
        '''Half reflection, 4 pt offset.'''
        ...
    
    @classmethod
    @property
    def FULL_REFLECTION_4_PT_OFFSET(cls) -> ReflectionEffectType:
        '''Full reflection, 4 pt offset.'''
        ...
    
    @classmethod
    @property
    def TIGHT_REFLECTION_8_PT_OFFSET(cls) -> ReflectionEffectType:
        '''Tight reflection, 8 pt offset.'''
        ...
    
    @classmethod
    @property
    def HALF_REFLECTION_8_PT_OFFSET(cls) -> ReflectionEffectType:
        '''Half reflection, 8 pt offset.'''
        ...
    
    @classmethod
    @property
    def FULL_REFLECTION_8_PT_OFFSET(cls) -> ReflectionEffectType:
        '''Full reflection, 8 pt offset.'''
        ...
    
    ...

class SelectionType:
    '''The selection type of list box.'''
    
    @classmethod
    @property
    def SINGLE(cls) -> SelectionType:
        '''Sigle selection type.'''
        ...
    
    @classmethod
    @property
    def MULTI(cls) -> SelectionType:
        '''Multiple selection type.'''
        ...
    
    @classmethod
    @property
    def EXTEND(cls) -> SelectionType:
        '''Extend selection type.'''
        ...
    
    ...

class ShapeAnchorType:
    '''Represents the anchor type.'''
    
    @classmethod
    @property
    def TWO_CELL_ANCHOR(cls) -> ShapeAnchorType:
        '''Represents a two cell anchor placeholder'''
        ...
    
    @classmethod
    @property
    def ONE_CELL_ANCHOR(cls) -> ShapeAnchorType:
        '''Represents a one cell anchor placeholder'''
        ...
    
    ...

class ShapeLockType:
    '''Represents type of the property to be locked.'''
    
    @classmethod
    @property
    def GROUP(cls) -> ShapeLockType:
        '''Group'''
        ...
    
    @classmethod
    @property
    def ADJUST_HANDLES(cls) -> ShapeLockType:
        '''AdjustHandles'''
        ...
    
    @classmethod
    @property
    def TEXT(cls) -> ShapeLockType:
        '''Text'''
        ...
    
    @classmethod
    @property
    def POINTS(cls) -> ShapeLockType:
        '''Points'''
        ...
    
    @classmethod
    @property
    def CROP(cls) -> ShapeLockType:
        '''Crop'''
        ...
    
    @classmethod
    @property
    def SELECTION(cls) -> ShapeLockType:
        '''Selection'''
        ...
    
    @classmethod
    @property
    def MOVE(cls) -> ShapeLockType:
        '''Move'''
        ...
    
    @classmethod
    @property
    def ASPECT_RATIO(cls) -> ShapeLockType:
        '''AspectRatio'''
        ...
    
    @classmethod
    @property
    def ROTATION(cls) -> ShapeLockType:
        '''Rotation'''
        ...
    
    @classmethod
    @property
    def UNGROUP(cls) -> ShapeLockType:
        '''Ungroup'''
        ...
    
    @classmethod
    @property
    def RESIZE(cls) -> ShapeLockType:
        '''Resize'''
        ...
    
    @classmethod
    @property
    def SHAPE_TYPE(cls) -> ShapeLockType:
        '''ShapeType'''
        ...
    
    @classmethod
    @property
    def ARROWHEAD(cls) -> ShapeLockType:
        '''Arrowhead'''
        ...
    
    ...

class ShapePathType:
    '''Represents path segment type.'''
    
    @classmethod
    @property
    def LINE_TO(cls) -> ShapePathType:
        '''Straight line segment'''
        ...
    
    @classmethod
    @property
    def CUBIC_BEZIER_CURVE_TO(cls) -> ShapePathType:
        '''Cubic Bezier curve'''
        ...
    
    @classmethod
    @property
    def MOVE_TO(cls) -> ShapePathType:
        '''Start a new path'''
        ...
    
    @classmethod
    @property
    def CLOSE(cls) -> ShapePathType:
        '''If the starting POINT and the end POINT are not the same, a single
        straight line is drawn to connect the starting POINT and ending POINT of the path.'''
        ...
    
    @classmethod
    @property
    def END(cls) -> ShapePathType:
        '''The end of the current path'''
        ...
    
    @classmethod
    @property
    def ESCAPE(cls) -> ShapePathType:
        '''Escape'''
        ...
    
    @classmethod
    @property
    def ARC_TO(cls) -> ShapePathType:
        '''An arc'''
        ...
    
    @classmethod
    @property
    def UNKNOWN(cls) -> ShapePathType:
        '''Unknown'''
        ...
    
    ...

class TextOverflowType:
    '''Represents the way the text vertical or horizontal overflow.'''
    
    @classmethod
    @property
    def CLIP(cls) -> TextOverflowType:
        '''Pay attention to top and bottom barriers.
        Provide no indication that there is text which is not visible.'''
        ...
    
    @classmethod
    @property
    def ELLIPSIS(cls) -> TextOverflowType:
        '''Pay attention to top and bottom barriers.
        Use an ellipsis to denote that there is text which is not visible.
        Only for vertical overflow.'''
        ...
    
    @classmethod
    @property
    def OVERFLOW(cls) -> TextOverflowType:
        '''Overflow the text and pay no attention to top and bottom barriers.'''
        ...
    
    ...

class TextureType:
    '''Represents the preset texture type.'''
    
    @classmethod
    @property
    def BLUE_TISSUE_PAPER(cls) -> TextureType:
        '''Represents Blue Tissue Paper texture type.'''
        ...
    
    @classmethod
    @property
    def BOUQUET(cls) -> TextureType:
        '''Represents Bouquet texture type.'''
        ...
    
    @classmethod
    @property
    def BROWN_MARBLE(cls) -> TextureType:
        '''Represents Brown Marble texture type.'''
        ...
    
    @classmethod
    @property
    def CANVAS(cls) -> TextureType:
        '''Represents Canvas texture type.'''
        ...
    
    @classmethod
    @property
    def CORK(cls) -> TextureType:
        '''Represents Cork texture type.'''
        ...
    
    @classmethod
    @property
    def DENIM(cls) -> TextureType:
        '''Represents Denim texture type.'''
        ...
    
    @classmethod
    @property
    def FISH_FOSSIL(cls) -> TextureType:
        '''Represents Fish Fossil texture type.'''
        ...
    
    @classmethod
    @property
    def GRANITE(cls) -> TextureType:
        '''Represents Granite texture type.'''
        ...
    
    @classmethod
    @property
    def GREEN_MARBLE(cls) -> TextureType:
        '''Represents Green Marble texture type.'''
        ...
    
    @classmethod
    @property
    def MEDIUM_WOOD(cls) -> TextureType:
        '''Represents Medium Wood texture type.'''
        ...
    
    @classmethod
    @property
    def NEWSPRINT(cls) -> TextureType:
        '''Represents Newsprint texture type.'''
        ...
    
    @classmethod
    @property
    def OAK(cls) -> TextureType:
        '''Represents Oak texture type.'''
        ...
    
    @classmethod
    @property
    def PAPER_BAG(cls) -> TextureType:
        '''Represents Paper Bag texture type.'''
        ...
    
    @classmethod
    @property
    def PAPYRUS(cls) -> TextureType:
        '''Represents Papyrus texture type.'''
        ...
    
    @classmethod
    @property
    def PARCHMENT(cls) -> TextureType:
        '''Represents Parchment texture type.'''
        ...
    
    @classmethod
    @property
    def PINK_TISSUE_PAPER(cls) -> TextureType:
        '''Represents Pink Tissue Paper texture type.'''
        ...
    
    @classmethod
    @property
    def PURPLE_MESH(cls) -> TextureType:
        '''Represents Purple Mesh texture type.'''
        ...
    
    @classmethod
    @property
    def RECYCLED_PAPER(cls) -> TextureType:
        '''Represents Recycled Paper texture type.'''
        ...
    
    @classmethod
    @property
    def SAND(cls) -> TextureType:
        '''Represents Sand texture type.'''
        ...
    
    @classmethod
    @property
    def STATIONERY(cls) -> TextureType:
        '''Represents Stationery texture type.'''
        ...
    
    @classmethod
    @property
    def WALNUT(cls) -> TextureType:
        '''Represents Walnut Droplets texture type.'''
        ...
    
    @classmethod
    @property
    def WATER_DROPLETS(cls) -> TextureType:
        '''Represents Water Droplets texture type.'''
        ...
    
    @classmethod
    @property
    def WHITE_MARBLE(cls) -> TextureType:
        '''Represents White Marble texture type.'''
        ...
    
    @classmethod
    @property
    def WOVEN_MAT(cls) -> TextureType:
        '''Represents Woven Mat texture type.'''
        ...
    
    @classmethod
    @property
    def UNKNOWN(cls) -> TextureType:
        '''Represents Unknown texture type.'''
        ...
    
    ...

class WeightType:
    '''Enumerates the weight types for a picture border or a chart line.'''
    
    @classmethod
    @property
    def HAIR_LINE(cls) -> WeightType:
        '''Represents the weight of hair line.'''
        ...
    
    @classmethod
    @property
    def MEDIUM_LINE(cls) -> WeightType:
        '''Represents the weight of medium line.'''
        ...
    
    @classmethod
    @property
    def SINGLE_LINE(cls) -> WeightType:
        '''Represents the weight of single line.'''
        ...
    
    @classmethod
    @property
    def WIDE_LINE(cls) -> WeightType:
        '''Represents the weight of wide line.'''
        ...
    
    ...

