# Multiaxes

`Multiaxes` is a python class based on `matplotlib`.  
This script makes easy to draw a figure with multiple axes for the AASTex manuscript.

## Install

`pip install git+https://github.com/radioshiny/multiaxes.git`

## Examples

### Getting started
The following is a basic example of plotting an image with the `Multiaxes`:
```python
import numpy as np
from multiaxes import Multiaxes

# make sample data
data = np.random.randn(10000).reshape((100, 100))

# make figure
mx = Multiaxes(col=1, nx=1, ny=1, xyr=1., xlab=0.3, ylab=0.4, tit=0.2)
fig, ax, _ = mx.drawfig(True)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('RMS noise map')
ax.imshow(data, cmap='jet', origin='lower')
fig.savefig('images/rms.pdf')
```
<object data="./images/rms.pdf" type="application/pdf"></object>
### Figure width

### Color bar

### Axes sharing


