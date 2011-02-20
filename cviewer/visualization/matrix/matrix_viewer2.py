""" Matrix Viewer Extension
* Left-drag pans the plot
* Mousewheel up and down zooms the plot in and out
* Pressing "z" brings up the Zoom Box, and you can click-drag a rectangular 
   region to zoom.  If you use a sequence of zoom boxes, pressing alt-left-arrow
   and alt-right-arrow moves you forwards and backwards through the "zoom 
   history".
* Right-click on the colorbar selects highlighted value range
"""
# Copyright (C) 2009-2010, Ecole Polytechnique Federale de Lausanne (EPFL) and
# University Hospital Center and University of Lausanne (UNIL-CHUV)
#
# Modified BSD License


# Major library imports
from enthought.enable.api import BaseTool

# Enthought library imports
from enthought.enable.api import Component, ComponentEditor, Window
from enthought.traits.api import HasTraits, Instance, Str, Enum, Float, Int, Property, Any
from enthought.traits.ui.api import Item, Group, View, HGroup, Handler

# Chaco imports
from enthought.chaco.api import ArrayPlotData, ColorBar, HPlotContainer, jet, LinearMapper, Plot
from enthought.chaco.tools.api import PanTool, RangeSelection, RangeSelectionOverlay, ZoomTool

class CustomHandler(Handler):
    """ Handler used to set NetworkName in TraitsTitle """
    
    def object_data_name_changed(self, info):
        if not info.initialized:
            info.ui.title = info.object.data_name


class CustomTool(BaseTool):
    
    xval = Float
    yval = Float
    
    def normal_mouse_move(self, event):
        xval, yval = self.component.map_data((event.x, event.y))
        
        self.xval = xval
        self.yval = yval

class MatrixViewer(HasTraits):
    
    tplot = Instance(Plot)
    plot = Instance(Component)
    custtool = Instance(CustomTool)
    colorbar = Instance(ColorBar)
    
    fro = Any
    to = Any
    data = None
    val = Float
    nodelabels = Any

    traits_view = View(
                    Group(
                        Item('plot', editor=ComponentEditor(size=(800,600)),
                             show_label=False),
                        HGroup(
                        Item('fro', label="From", style = 'readonly', springy=True),
                        Item('to', label="To", style = 'readonly', springy=True),
                        Item('val', label="Value", style = 'readonly', springy=True),
                        ),
                        orientation = "vertical"),
                    Item('data_name', label="Image data"),
                    handler=CustomHandler(),
                    resizable=True, title="Matrix Viewer"
                    )

    
    def __init__(self, nodelabels, matdict, **traits):
        """ Starts a matrix inspector
        
        Parameters
        ----------
        nodelables : list
            List of strings of labels for the rows of the matrix
        matdict : dictionary
            Keys are the edge type and values are NxN Numpy arrays """
        super(HasTraits, self).__init__(**traits)
        
        self.add_trait('data_name', Enum(matdict.keys()))
        
        self.data_name = matdict.keys()[0]
        self.data = matdict
        self.nodelables = nodelabels
        self.plot = self._create_plot_component()
        
        # set trait notification on customtool
        self.custtool.on_trait_change(self._update_fields, "xval")
        self.custtool.on_trait_change(self._update_fields, "yval")

    def _data_name_changed(self, old, new):
        self.pd.set_data("imagedata", self.data[self.data_name])
        #self.my_plot.set_value_selection((0, 2))
        self.tplot.title = "Matrix for %s" % self.data_name
        
    def _update_fields(self):
        from numpy import trunc
        
        # map mouse location to array index
        frotmp = int(trunc(self.custtool.yval))
        totmp = int(trunc(self.custtool.xval))
        
        # check if within range
        sh = self.data[self.data_name].shape
        # assume matrix whose shape is (# of rows, # of columns)
        if frotmp >= 0 and frotmp < sh[0] and totmp >= 0 and totmp < sh[1]:
            self.fro = self.nodelables[frotmp]
            self.to = self.nodelables[totmp]
            self.val = self.data[self.data_name][frotmp, totmp]
        
    def _create_plot_component(self):
        
        # Create a plot data object and give it this data
        self.pd = ArrayPlotData()
        self.pd.set_data("imagedata", self.data[self.data_name])
    
        # Create the plot
        self.tplot = Plot(self.pd, default_origin="top left")
        self.tplot.x_axis.orientation = "top"
        self.tplot.img_plot("imagedata", 
                      name="my_plot",
                      #xbounds=(0,10),
                      #ybounds=(0,10),
                      colormap=jet)
    
        # Tweak some of the plot properties
        self.tplot.title = "Matrix for %s" % self.data_name
        self.tplot.padding = 50
    
        # Right now, some of the tools are a little invasive, and we need the 
        # actual CMapImage object to give to them
        self.my_plot = self.tplot.plots["my_plot"][0]
    
        # Attach some tools to the plot
        self.tplot.tools.append(PanTool(self.tplot))
        zoom = ZoomTool(component=self.tplot, tool_mode="box", always_on=False)
        self.tplot.overlays.append(zoom)
        
        # my custom tool to get the connection information
        self.custtool = CustomTool(self.tplot)
        self.tplot.tools.append(self.custtool)
    
        # Create the colorbar, handing in the appropriate range and colormap
        colormap = self.my_plot.color_mapper
        self.colorbar = ColorBar(index_mapper=LinearMapper(range=colormap.range),
                            color_mapper=colormap,
                            plot=self.my_plot,
                            orientation='v',
                            resizable='v',
                            width=30,
                            padding=20)
            
        self.colorbar.padding_top = self.tplot.padding_top
        self.colorbar.padding_bottom = self.tplot.padding_bottom
        
        # create a range selection for the colorbar
        self.range_selection = RangeSelection(component=self.colorbar)
        self.colorbar.tools.append(self.range_selection)
        self.colorbar.overlays.append(RangeSelectionOverlay(component=self.colorbar,
                                                       border_color="white",
                                                       alpha=0.8,
                                                       fill_color="lightgray"))
    
        # we also want to the range selection to inform the cmap plot of
        # the selection, so set that up as well
        self.range_selection.listeners.append(self.my_plot)
    
        # Create a container to position the plot and the colorbar side-by-side
        container = HPlotContainer(use_backbuffer = True)
        container.add(self.tplot)
        container.add(self.colorbar)
        container.bgcolor = "white"
    
        return container

if __name__ == "__main__":
    import numpy as np
    
    nodelabels = [str(e) for e in range(300)]
    matdict = {'edgval1':np.random.random( (300,300) ), 'edgval2': np.random.random( (300,300) )}
    
    demo = MatrixViewer(nodelabels, matdict)
    demo.configure_traits()



