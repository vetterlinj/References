## <a id="McUtils.Plots.Plots.DataPlot">DataPlot</a>
Makes a 2D plot of arbitrary data using a plot method that handles that data type

### Properties and Methods
<a id="McUtils.Plots.Plots.DataPlot.__init__">&nbsp;</a>
```python
__init__(self, *params, plot_style=None, method=None, figure=None, axes=None, subplot_kw=None, colorbar=None, **opts): 
```

- `params`: `Any`
    >_empty_ or _data_
- `plot_style`: `dict | None`
    >the plot styling options to be fed into the plot method
- `method`: `str`
    >the method name as a string
- `figure`: `Graphics | None`
    >the Graphics object on which to plot (None means make a new one)
- `axes`: `None`
    >the axes on which to plot (used in constructing a Graphics, None means make a new one)
- `subplot_kw`: `dict | None`
    >the keywords to pass on when initializing the plot
- `colorbar`: `None | bool | dict`
    >whether to use a colorbar or what options to pass to the colorbar
- `opts`: `Any`
    >options to be fed in when initializing the Graphics

### Examples
