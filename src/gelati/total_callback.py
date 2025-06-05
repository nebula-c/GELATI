
def total_callback(ctx):
    print_terminal              = ctx.terminal_handler.print_terminal
    print_terminal_colored      = ctx.terminal_handler.print_terminal_colored
    get_filename                = ctx.fileloader_handler.get_filename
    get_raw_data_from_file      = ctx.fileloader_handler.get_raw_data
    get_filetype                = ctx.fileloader_handler.get_filetype
    set_raw_chart_title         = ctx.rawchart_handler.set_raw_chart_title        
    Show_raw_chart              = ctx.rawchart_handler.Show_raw_chart        
    set_rawchart_raw_data       = ctx.rawchart_handler.set_raw_data
    get_raw_chart_range         = ctx.rawchart_handler.get_raw_chart_range
    set_axis_range              = ctx.rawchart_handler.set_axis_range
    show_peaks                  = ctx.rawchart_handler.show_peaks
    show_sel                    = ctx.rawchart_handler.show_sel
    reset_raw_chart             = ctx.rawchart_handler.reset_raw_chart
    set_modeling_yaix_range_new = ctx.modelingchart_handler.set_modeling_yaix_range_new
    set_modeling_yaix_range_raw = ctx.modelingchart_handler.set_modeling_yaix_range_raw
    Show_modeling_chart         = ctx.modelingchart_handler.Show_modeling_chart
    Change_phase                = ctx.modelingchart_handler.Change_phase
    reset_modeling_chart        = ctx.modelingchart_handler.reset_modeling_chart
    set_lineedit_raw_range      = ctx.control_handler.set_lineedit_raw_range
    get_sliced_range            = ctx.control_handler.get_sliced_range
    get_new_yrange              = ctx.control_handler.get_new_yrange
    set_bridge_raw_data         = ctx.Bridge.set_raw_data
    range_slicing               = ctx.Bridge.range_slicing
    get_raw_yrange              = ctx.Bridge.get_raw_yrange
    guide_modeling_run          = ctx.Bridge.guide_modeling_run
    get_guide_data              = ctx.Bridge.get_guide_data
    get_raw_xyrange             = ctx.Bridge.get_raw_xyrange
    reset_slicing               = ctx.Bridge.reset_slicing
    seeking_peak                = ctx.Bridge.seeking_peak
    get_raw_peaks               = ctx.Bridge.get_raw_peaks
    get_selected_data           = ctx.Bridge.get_selected_data
    get_parameter               = ctx.Bridge.get_parameter
    open_setting_window         = ctx.setting_handler.open_setting_window

    ctx.fileloader_handler.set_callback("print_terminal",print_terminal)
    ctx.fileloader_handler.set_callback("print_terminal_colored",print_terminal_colored)
    ctx.fileloader_handler.set_callback("set_raw_chart_title",set_raw_chart_title)
    ctx.fileloader_handler.set_callback("Show_raw_chart",Show_raw_chart)
    ctx.fileloader_handler.set_callback("set_bridge_raw_data",set_bridge_raw_data)
    ctx.fileloader_handler.set_callback("set_rawchart_raw_data",set_rawchart_raw_data)
    ctx.rawchart_handler.set_callback("print_terminal",print_terminal)
    ctx.rawchart_handler.set_callback("print_terminal_colored",print_terminal_colored)
    ctx.rawchart_handler.set_callback("get_filename",get_filename)
    ctx.rawchart_handler.set_callback("get_raw_data_from_file",get_raw_data_from_file)
    ctx.rawchart_handler.set_callback("set_lineedit_raw_range",set_lineedit_raw_range)
    ctx.rawchart_handler.set_callback("get_sliced_range",get_sliced_range)
    ctx.rawchart_handler.set_callback("get_raw_peaks",get_raw_peaks)
    ctx.rawchart_handler.set_callback("get_selected_data",get_selected_data)
    ctx.modelingchart_handler.set_callback("print_terminal",print_terminal)
    ctx.modelingchart_handler.set_callback("print_terminal_colored",print_terminal_colored)
    ctx.modelingchart_handler.set_callback("get_raw_chart_range",get_raw_chart_range)
    ctx.modelingchart_handler.set_callback("get_raw_yrange",get_raw_yrange)
    ctx.modelingchart_handler.set_callback("get_new_yrange",get_new_yrange)
    ctx.modelingchart_handler.set_callback("get_guide_data",get_guide_data)
    ctx.control_handler.set_callback("print_terminal",print_terminal)
    ctx.control_handler.set_callback("print_terminal_colored",print_terminal_colored)
    ctx.control_handler.set_callback("open_setting_window",open_setting_window)
    ctx.control_handler.set_callback("get_raw_chart_range",get_raw_chart_range)
    ctx.control_handler.set_callback("set_axis_range",set_axis_range)
    ctx.control_handler.set_callback("range_slicing",range_slicing)
    ctx.control_handler.set_callback("set_modeling_yaix_range_new",set_modeling_yaix_range_new)
    ctx.control_handler.set_callback("set_modeling_yaix_range_raw",set_modeling_yaix_range_raw)
    ctx.control_handler.set_callback("guide_modeling_run",guide_modeling_run)
    ctx.control_handler.set_callback("get_raw_xyrange",get_raw_xyrange)
    ctx.control_handler.set_callback("reset_slicing",reset_slicing)
    ctx.control_handler.set_callback("Change_phase",Change_phase)
    ctx.control_handler.set_callback("seeking_peak",seeking_peak)
    ctx.control_handler.set_callback("reset_modeling_chart",reset_modeling_chart)
    ctx.control_handler.set_callback("show_sel",show_sel)
    ctx.control_handler.set_callback("reset_raw_chart",reset_raw_chart)
    ctx.control_handler.set_callback("Show_raw_chart",Show_raw_chart)
    ctx.control_handler.set_callback("set_bridge_raw_data",set_bridge_raw_data)
    ctx.control_handler.set_callback("get_guide_data",get_guide_data)
    ctx.Bridge.set_callback("print_terminal",print_terminal)
    ctx.Bridge.set_callback("print_terminal_colored",print_terminal_colored)
    ctx.Bridge.set_callback("get_raw_data_from_file",get_raw_data_from_file)
    ctx.Bridge.set_callback("get_filetype",get_filetype)
    ctx.Bridge.set_callback("Show_modeling_chart",Show_modeling_chart)
    ctx.Bridge.set_callback("show_peaks",show_peaks)
    ctx.setting_handler.set_callback("print_terminal",print_terminal)
    ctx.setting_handler.set_callback("print_terminal_colored",print_terminal_colored)
    ctx.setting_handler.set_callback("not_dev",ctx.not_dev)
    ctx.setting_handler.set_callback("get_parameter",get_parameter)
    
    