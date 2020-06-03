# Multiaxes

`Multiaxes` is a python class based on `matplotlib`.  
This script makes easy to draw a figure with multiple axes for the AASTex manuscript.

## Install

`pip install git+https://github.com/radioshiny/multiaxes.git`

## Examples

### Single plot
```python
from multiaxes import Multiaxes
import numpy as np
data = np.random.randn(10000).reshape((100, 100))
mx = Multiaxes(col=1, nx=1, ny=1, xyr=1., xlab=0.5, ylab=0.5, tit=0.3)
fig, ax, _ = mx.drawfig(True)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('RMS noise map')
ax.imshow(data, cmap='jet', origin='lower')


```

### Figure width

### Color bar

### Axes sharing


