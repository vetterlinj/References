## <a id="McUtils.Plots.Graphics.Graphics">Graphics</a>
A mini wrapper to matplotlib.pyplot to create a unified interface I know how to work with

### Properties and Methods
```python
plot_label: property
plot_legend: property
axes_labels: property
plot_range: property
ticks: property
ticks_style: property
aspect_ratio: property
image_size: property
background: property
frame: property
colorbar: property
scale: property
```
<a id="McUtils.Plots.Graphics.Graphics.__init__">&nbsp;</a>
```python
__init__(self, *args, figure=None, axes=None, frame=((True, False), (True, False)), subplot_kw=None, event_handlers=None, animate=None, axes_labels=None, plot_label=None, plot_range=None, plot_legend=None, ticks=None, scale=None, image_size=None, background='white', aspect_ratio=1, colorbar=None, **kwargs): 
```

<a id="McUtils.Plots.Graphics.Graphics.set_options">&nbsp;</a>
```python
set_options(self, axes_labels=None, plot_label=None, plot_range=None, plot_legend=None, frame=None, ticks=None, scale=None, ticks_style=None, image_size=None, aspect_ratio=None, background=None, colorbar=None, prolog=None, epilog=None, **parent_opts): 
```

<a id="McUtils.Plots.Graphics.Graphics.add_colorbar">&nbsp;</a>
```python
add_colorbar(self, graphics=None, norm=None, cmap=None, **kw): 
```

### Examples
The `Graphics` object is a simple interface to the [matplotlib.figure.Figure
](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure) class. 
This is bound to the `figure` attribute of the object.

```python
from McUtils.Plots import *

g = Graphics()
type(g.figure)

# Out: matplotlib.figure.Figure
```

Each `Graphics` object also binds an [matplotlib.axes.Axes](https://matplotlib.org/3.1.1/api/axes_api.html#the-axes-class) object.
Because of this, the framework is set up so that multiple `Graphics` objects can
 use the same underlying `figure`:
 
 ```python
g = Graphics()
f = Graphics(figure=g)
g.figure is f.figure

# Out: True
```

Usually one won't use `Graphics` on its own, but will instead use on of the
other plotting functions, such as `Plot` or `ContourPlot` to create a
`Graphics` object.