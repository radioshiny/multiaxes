# Multiaxes
`Multiaxes` is a python class based on `matplotlib`.  
This script makes easy to draw a figure with multiple axes for the AASTeX manuscript.

## Installation
```bash
pip install git+https://github.com/radioshiny/multiaxes.git
```

### Requirements
Strict requirements:
* `matplotlib`
* `numpy`

Optional :
* `astropy` for WCSAxes

## Getting started
The following is a basic example of plotting an image with the `Multiaxes`:
```python
import numpy as np
from multiaxes import Multiaxes

# make sample data
data = np.random.randn(10000).reshape((100, 100))

# make figure
mx = Multiaxes(col=1, nx=1, ny=1, xyr=1., xlab=0.3, ylab=0.4, tit=0.2, scale=0.7)
fig, ax, _ = mx.drawfig()
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('RMS noise map')
ax.imshow(data, cmap='jet', origin='lower')
fig.savefig('images/rms.pdf')
```
<kbd><img src="./images/rms.png" width="373"/></kbd>


* `col=1` (int) : figure width = width of one column in two column mode
* `nx=1` (int) : number of subplots in the horizontal direction
* `ny=1` (int) : number of subplots in the vertical direction
* `xyr=1.` (float) : x-length to y-length ratio of subplot
* `xlab=0.3` (float) : height of x-label in inch
* `ylab=0.4` (float) : width of y-label in inch
* `tit=0.2` (float) : height of title in inch
* `scale=0.7` (float) : zooming scale in LaTeX


In order for the figure to be inserted at the intended size (width) in your 
AASTeX manuscript, the `scale` parameter should be set to the same value used 
in `Multiaxes`. 
```latex
\begin{figure}
    \includegraphics[scale=0.7]{rms.pdf}
    \caption{The RMS noise map}
    \label{fig:rms}
\end{figure}
```

## Examples

### Subplots in one column
```python
import numpy as np
from astropy.modeling.models import Gaussian2D
from multiaxes import Multiaxes

# make sample data
y, x = np.mgrid[:100, :100]
gauss2d = Gaussian2D(20., 50., 50., 10., 20., -45.)
rms = np.random.randn(10000).reshape((100, 100))
model = gauss2d(x, y)
obs = model+rms

# make figure
mx = Multiaxes(col=1, nx=1, ny=3, xyr=1., xlab=0.3, ylab=0.4, ypad=0.2, tit=0.2, scale=0.7)
fig, ax, _ = mx.drawfig(True)
for p in ax:
    p.set_xlabel('x (px)')
    p.set_ylabel('y (px)')
ax[2].set_title('Intensity map')
ax[2].imshow(obs, cmap='inferno', origin='lower')
ax[1].set_title('Model')
ax[1].imshow(model, cmap='inferno', origin='lower')
ax[0].set_title('Residual map')
ax[0].imshow(obs-model, cmap='jet', origin='lower')
fig.savefig('images/col1_ny3.pdf')
fig.savefig('images/col1_ny3.png', dpi=150)
```
<kbd><img src="./images/col1_ny3.png" width="278"/></kbd>


### Subplots in two column
```python
# make figure
mx = Multiaxes(col=2, nx=3, ny=1, xyr=1., xlab=0.3, ylab=0.4, xpad=0.1, tit=0.2, scale=0.7)
fig, ax, _ = mx.drawfig()
for p in ax:
    p.set_xlabel('x (px)')
    p.set_ylabel('y (px)')
ax[0].set_title('Intensity map')
ax[0].imshow(obs, cmap='inferno', origin='lower')
ax[1].set_title('Model')
ax[1].imshow(model, cmap='inferno', origin='lower')
ax[2].set_title('Residual map')
ax[2].imshow(obs-model, cmap='jet', origin='lower')
fig.savefig('images/col2_nx3.pdf')
fig.savefig('images/col2_nx3.png', dpi=150)
```
<kbd><img src="./images/col2_nx3.png" width="782"/></kbd>


### Color bar

### Axes sharing


