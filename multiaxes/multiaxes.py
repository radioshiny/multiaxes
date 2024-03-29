import numpy as np
from matplotlib import pyplot as plt
from astropy.visualization.wcsaxes.core import WCSAxes
from warnings import warn

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.right'] = True
plt.rcParams['xtick.major.size'] = 5
plt.rcParams['ytick.major.size'] = 5
plt.rcParams['xtick.minor.size'] = 3
plt.rcParams['ytick.minor.size'] = 3
# plt.rcParams['xtick.minor.visible'] = True
# plt.rcParams['ytick.minor.visible'] = True
plt.rcParams['xtick.labelsize'] = 'small'
plt.rcParams['ytick.labelsize'] = 'small'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'dejavusans'
plt.rcParams['image.interpolation'] = 'nearest'


class Multiaxes:
    def __init__(self, col=1, nx=1, ny=1, xyr=1., xlab=0.5, ylab=0.5, xpad=0.2, ypad=0.2, tit=0.,
                 cb=None, clab=0.4, cpad=0.05, xxr=1., scale=0.7, margin=0.02, proj=None, cpos='top'):
        if col in [1, 2]:
            self._col = int(col)
        else:
            warn("col = {}, figure width doesn't match with column or page width.")
            self._col = float(col)
        if int(nx) in range(1, 20):
            self._nx = int(nx)
        else:
            raise ValueError("'nx' is number of column in figure, (1 to 19)")
        if int(ny) in range(1, 20):
            self._ny = int(ny)
        else:
            raise ValueError("'ny' is number of line in figure, (1 to 19)")
        self._yr = np.zeros(ny, dtype=float)
        self._xr = np.zeros(nx, dtype=float)
        self._xl = np.zeros(ny, dtype=float)
        self._yl = np.zeros(nx, dtype=float)
        self._tp = np.zeros(ny, dtype=float)
        if cpos == 'top':
            self._cb = 't'
            self._cw = np.zeros(ny, dtype=float)
            self._cl = np.zeros(ny, dtype=float)
            self._cp = np.zeros(ny, dtype=float)
        elif cpos == 'right':
            self._cb = 'r'
            self._cw = np.zeros(nx, dtype=float)
            self._cl = np.zeros(nx, dtype=float)
            self._cp = np.zeros(nx, dtype=float)
        else:
            raise ValueError("'cpos' should be in ['top', 'right']")
        self._pj = np.zeros((ny, nx), dtype=object)
        if nx > 1:
            self._xp = np.zeros(nx-1, dtype=float)
        else:
            self._xp = np.zeros(1, dtype=float)
        if ny > 1:
            self._yp = np.zeros(ny-1, dtype=float)
        else:
            self._yp = np.zeros(1, dtype=float)
        self._yr[:] = xyr
        self._xr[:] = xxr
        self._xl[:] = xlab
        self._yl[:] = ylab
        self._xp[:] = xpad
        self._yp[:] = ypad
        if nx == 1:
            self._xp[:] = 0.
        if ny == 1:
            self._yp[:] = 0.
        self._tp[:] = tit
        self._pj[:, :] = proj
        if cb is None:
            self._cw[:] = 0.
            self._cl[:] = 0.
            self._cp[:] = 0.
        else:
            self._cw[:] = cb
            self._cl[:] = clab
            self._cp[:] = cpad
        self._sc = 1./float(scale)
        self._mg = np.zeros(4, dtype=float)
        self._mg[:] = margin
        self._mg[2] *= 1.5

    _fig = None
    _ax = None
    _cax = None
    _sharex = False
    _sharey = False
    _apj_width = 7.3
    _apj_col = 3.485
    _apj_height = 8.

    @property
    def fig(self):
        if self._fig is None:
            self.drawfig(False)
        return self._fig

    @property
    def ax(self):
        if self._ax is None:
            self.drawfig(False)
        return self._ax

    @property
    def cax(self):
        if self._cax is None:
            self.drawfig(False)
        return self._cax

    @property
    def col(self):
        return self._col

    def title(self, height=None):
        print('Original title height =', self._tp)
        if height is None:
            self._tp[:] = 0.
        else:
            self._tp[:] = height
        print('Modified title height =', self._tp)
        return

    def shareaxes(self, xy=(True, True), pad=0.05):
        if xy[0] and self._ny > 1:
            self._sharex = True
            self._xl[1:] = 0.
            self._yp[:] = pad
            self._tp[:-1] = 0.
            if self._cb == 't':
                self._cw[:-1] = 0.
                self._cl[:-1] = 0.
                self._cp[:-1] = 0.
        if xy[1] and self._nx > 1:
            self._sharey = True
            self._yl[1:] = 0.
            self._xp[:] = pad
            if self._cb == 'r':
                self._cw[:-1] = 0.
                self._cl[:-1] = 0.
                self._cp[:-1] = 0.
        return

    def drawfig(self, verbose=False, border=False):
        if self._col == int(1):
            fig_width = self._apj_col*self._sc
        elif self._col == int(2):
            fig_width = self._apj_width*self._sc
        else:
            fig_width = self._apj_col*self._col*self._sc
        page_height = self._apj_height*self._sc
        if self._cb == 't':
            outx = self._yl.sum()+self._xp.sum()+self._mg[[0, 2]].sum()
            outy = self._xl.sum()+self._yp.sum()+self._tp.sum()+self._cw.sum()+self._cl.sum()+self._cp.sum()+self._mg[[1, 3]].sum()
        else:
            outx = self._yl.sum()+self._xp.sum()+self._cw.sum()+self._cl.sum()+self._cp.sum()+self._mg[[0, 2]].sum()
            outy = self._xl.sum()+self._yp.sum()+self._tp.sum()+self._mg[[1, 3]].sum()
        remain_width = fig_width-outx
        xs = self._xr/self._xr.sum()*remain_width
        ys = xs[0]/self._yr
        remain_height = page_height-outy
        if ys.sum() > remain_height:
            xs *= remain_height/ys.sum()
            ys *= remain_height/ys.sum()
            fig_width = xs.sum()+outx
        fig_height = ys.sum()+outy
        if verbose:
            print('x-label height =', self._xl)
            print('y-label width =', self._yl)
            print('x-pad width =', self._xp)
            print('y-pad height =', self._yp)
            if self._cb == 't':
                print('colorbar height =', self._cw)
                print('colorbar label height =', self._cl)
                print('colorbar pad height =', self._cp)
            else:
                print('colorbar width =', self._cw)
                print('colorbar label width =', self._cl)
                print('colorbar pad width =', self._cp)
            print('outside x width =', outx)
            print('outside y height =', outy)
            print('remain width =', remain_width)
            print('remain height =', remain_height)
            print('x-size width =', xs)
            print('y-size height =', ys)
            print('figure width =', fig_width)
            print('figure height =', fig_height)
        self._fig = plt.figure(figsize=(fig_width, fig_height))
        self._fw, self._fh = fig_width, fig_height
        self._ax = np.zeros((self._ny, self._nx), dtype=object)
        self._cax = np.zeros((self._ny, self._nx), dtype=object)
        if border:
            x0 = self._mg[0]/fig_width
            y0 = self._mg[1]/fig_height
            x1 = (fig_width-self._mg[[0, 2]].sum())/fig_width
            y1 = (fig_height-self._mg[[1, 3]].sum())/fig_height
            bd = self._fig.add_axes([x0, y0, x1, y1])
            bd.axes.get_xaxis().set_visible(False)
            bd.axes.get_yaxis().set_visible(False)
        for yi in range(self._ny):
            for xi in range(self._nx):
                if self._cb == 't':
                    x0 = (self._mg[0]+self._yl[:xi+1].sum()+xs[:xi].sum()+self._xp[:xi].sum())/fig_width
                    y0 = (self._mg[1]+self._xl[:yi+1].sum()+ys[:yi].sum()+self._tp[:yi].sum()+self._yp[:yi].sum()
                          +self._cw[:yi].sum()+self._cl[:yi].sum()+self._cp[:yi].sum())/fig_height
                else:
                    x0 = (self._mg[0]+self._yl[:xi+1].sum()+xs[:xi].sum()+self._xp[:xi].sum()
                          +self._cw[:xi].sum()+self._cl[:xi].sum()+self._cp[:xi].sum())/fig_width
                    y0 = (self._mg[1]+self._xl[:yi+1].sum()+ys[:yi].sum()+self._tp[:yi].sum()
                          +self._yp[:yi].sum())/fig_height
                x1 = xs[xi]/fig_width
                y1 = ys[yi]/fig_height
                if verbose:
                    print('ax[{}, {}] = ({:.3f}, {:.3f}, {:.3f}, {:.3f})'.format(yi, xi, x0, y0, x1, y1))
                self._ax[yi, xi] = self._fig.add_axes([x0, y0, x1, y1], projection=self._pj[yi, xi])
                if self._sharey and xi > 0:
                    if isinstance(self._ax[yi, xi], WCSAxes):
                        self._ax[yi, xi].coords[1].set_ticklabel_visible(False)
                        self._ax[yi, xi].coords[1].set_axislabel('')
                    else:
                        self._ax[yi, xi].yaxis.set_major_formatter(plt.NullFormatter())
                        self._ax[yi, xi].yaxis.set_minor_formatter(plt.NullFormatter())
                if self._sharex and yi > 0:
                    if isinstance(self._ax[yi, xi], WCSAxes):
                        self._ax[yi, xi].coords[0].set_ticklabel_visible(False)
                        self._ax[yi, xi].coords[0].set_axislabel('')
                    else:
                        self._ax[yi, xi].xaxis.set_major_formatter(plt.NullFormatter())
                        self._ax[yi, xi].xaxis.set_minor_formatter(plt.NullFormatter())
        for yi in range(self._ny):
            for xi in range(self._nx):
                if self._cb == 't':
                    x0 = (self._mg[0]+self._yl[:xi+1].sum()+xs[:xi].sum()+self._xp[:xi].sum())/fig_width
                    y0 = (self._mg[1]+self._xl[:yi+1].sum()+ys[:yi+1].sum()+self._tp[:yi].sum()+self._yp[:yi].sum()
                          +self._cw[:yi].sum()+self._cl[:yi].sum()+self._cp[:yi+1].sum())/fig_height
                    x1 = xs[xi]/fig_width
                    y1 = self._cw[yi]/fig_height
                else:
                    x0 = (self._mg[0]+self._yl[:xi+1].sum()+xs[:xi+1].sum()+self._xp[:xi].sum()
                          +self._cw[:xi].sum()+self._cl[:xi].sum()+self._cp[:xi+1].sum())/fig_width
                    y0 = (self._mg[1]+self._xl[:yi+1].sum()+ys[:yi].sum()+self._tp[:yi].sum()
                          +self._yp[:yi].sum())/fig_height
                    x1 = self._cw[xi]/fig_width
                    y1 = ys[yi]/fig_height
                if verbose:
                    print('cax[{}, {}] = ({:.3f}, {:.3f}, {:.3f}, {:.3f})'.format(yi, xi, x0, y0, x1, y1))
                if (x1 > 0.) and (y1 > 0.):
                    self._cax[yi, xi] = self._fig.add_axes([x0, y0, x1, y1])
                    if self._cb == 't':
                        self._cax[yi, xi].xaxis.tick_top()
                else:
                    self._cax[yi, xi] = None
        if self._nx == 1 or self._ny == 1:
            self._ax = self._ax.flatten()
            self._cax = self._cax.flatten()
        if self._nx == 1 and self._ny == 1:
            self._ax = self.ax[0]
            self._cax = self._cax[0]
        if self._ny > 1:
            self._ax = np.flip(self._ax, axis=0)
            self._cax = np.flip(self._cax, axis=0)
        return self._fig, self._ax, self._cax

    def subaxes(self, ax, box):
        x0, y0, x1, y1 = ax._position.get_points().flatten()
        x1, y1 = x1-x0, y1-y0
        x2, y2, x3, y3 = box
        return self._fig.add_axes([x0+x1*x2, y0+y1*y2, x1*x3, y1*y3])

    def subgrid(self, ax, grid, pad=0., frame=False, repr=None):
        x0, y0, x1, y1 = ax._position.get_points().flatten()
        x1, y1 = x1-x0, y1-y0
        nx, ny = grid
        xw, yh = x1/nx, y1/ny
        sg = np.zeros((ny, nx), dtype=object)
        for yi in range(ny):
            for xi in range(nx):
                sg[yi, xi] = self._fig.add_axes([x0+xw*xi+pad/2., y0+yh*yi+pad/2., xw-pad, yh-pad], fc='None')
                if frame:
                    sg[yi, xi].axes.get_xaxis().set_visible(False)
                    sg[yi, xi].axes.get_yaxis().set_visible(False)
                else:
                    sg[yi, xi].set_axis_off()
                if repr is not None:
                    if (xi == repr[0]) and (yi == repr[1]):
                        if frame:
                            sg[yi, xi].axes.get_xaxis().set_visible(True)
                            sg[yi, xi].axes.get_yaxis().set_visible(True)
                        else:
                            sg[yi, xi].set_axis_on()
        return sg

    def colorbar(self, mappable=None, cax=None, ax=None, **kwargs):
        return plt.colorbar(mappable, cax, ax, **kwargs)

    def sharecolorbar(self, loc='right', width=0.1, pad=0.):
        if loc == 'right':
            if len(self._ax.shape) == 1:
                x0, y0 = self._ax[-1].get_position().get_points().flatten()[[2, 1]]
                y1 = self._ax[-1].get_position().get_points().flatten()[3]-y0
            else:
                x0, y0 = self._ax[-1, -1].get_position().get_points().flatten()[[2, 1]]
                y1 = self._ax[0, -1].get_position().get_points().flatten()[3]-y0
            x1 = width/self._fw
            xp = pad/self._fw
            self._cax = self._fig.add_axes([x0+xp, y0, x1, y1])
        elif loc == 'top':
            if len(self._ax.shape) == 1:
                x0, y0 = self._ax[0].get_position().get_points().flatten()[[0, 3]]
                x1 = self._ax[-1].get_position().get_points().flatten()[2]-x0
            else:
                x0, y0 = self._ax[0, 0].get_position().get_points().flatten()[[0, 3]]
                x1 = self._ax[0, -1].get_position().get_points().flatten()[2]-x0
            y1 = width/self._fh
            yp = pad/self._fh
            self._cax = self._fig.add_axes([x0, y0+yp, x1, y1])
            self._cax.xaxis.tick_top()
            self._cax.xaxis.set_label_position('top')
        else:
            raise ValueError("Shared color bar can be located 'right' or 'top'.")
        return self._cax

    def topcolorbar(self, cax):
        cax.xaxis.tick_top()
        cax.xaxis.set_label_position('top')

    def removeticklabel(self, ax, xy=(True, True)):
        for ix in ax.flatten():
            if isinstance(ix, WCSAxes):
                if xy[0]:
                    ix.coords[0].set_ticklabel_visible(False)
                    ix.coords[0].set_axislabel('')
                if xy[1]:
                    ix.coords[1].set_ticklabel_visible(False)
                    ix.coords[1].set_axislabel('')
            else:
                if xy[0]:
                    ix.xaxis.set_major_formatter(plt.NullFormatter())
                    ix.xaxis.set_minor_formatter(plt.NullFormatter())
                if xy[1]:
                    ix.yaxis.set_major_formatter(plt.NullFormatter())
                    ix.yaxis.set_minor_formatter(plt.NullFormatter())
        return
