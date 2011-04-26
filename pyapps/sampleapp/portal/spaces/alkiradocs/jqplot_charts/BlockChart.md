[jqplot options]:http://www.jqplot.com/docs/files/jqPlotOptions-txt.html#jqPlot_Options
# Block Chart

The Block chart is an example with explanation of the JqPlot Block Chart

######The body of the macro is the parameters that JqPlot uses to initialize the block chart.
    1- width:- The width of the canvas where the chart is drawn. An optional parameter.  
    2- height:- The height of the canvas where the chart is drawn. An optional parameter.  
    3- chart_data:- A list of the block set(s) that will be drawn where each block set is a list of  
       points. The points must be a list of [x, y, 'value'] as x, y are the axes of the point and  
       'value' is what is written in the block. A mandatory parameter.  
    4- chart_div:- The HTML div that will contain the chart. A mandatory parameter.  
    5- renderer:- the shape which jqPlot will draw that is the Block in this macro. If this parameter  
       is not passed jqPlot will draw the default shape the Line chart.

##Example
    <div class="macro macro_jqplot">
        {"width" : 400,
         "height" : 400,
         "chart_data" : [[[1, 2, "red"],[2, 4, "blue"],[3, 6, "blach"],[4, 8,"green"]]],
         "chart_div" : "block_div",
         "renderer" :"$.jqplot.BlockRenderer"
        }
    </div>

If you want to create a macro with a more complicated block chart please see [How to Create a Macro](/sampleapp/#/alkiradocs/Macros_HOWTO) and [jqPlot options page][jqplot options].
  
## Sample Block Chart

<div class="macro macro_jqplot">
{"width" : 400,
 "height" : 400,
 "chart_data" : [[[1, 2, "red"],[2, 4, "blue"],[3, 6, "blach"],[4, 8,"green"]]],
 "chart_div" : "block_div",
 "renderer" :"$.jqplot.BlockRenderer"
}
</div>