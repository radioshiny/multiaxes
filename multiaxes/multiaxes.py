import numpy as np
from matplotlib import pyplot as plt

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.right'] = True
plt.rcParams['xtick.major.size'] = 5
plt.rcParams['ytick.major.size'] = 5
plt.rcParams['xtick.minor.size'] = 3
plt.rcParams['ytick.minor.size'] = 3
plt.rcParams['xtick.minor.visible'] = True
plt.rcParams['ytick.minor.visible'] = True
plt.rcParams['xtick.labelsize'] = 'small'
plt.rcParams['ytick.labelsize'] = 'small'

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'dejavusans'


class Multiaxes:
    def __init__(self, col=1, nx=1, ny=1, xyr=1., xlab=0.5, ylab=0.5, xpad=0.2, ypad=0.2, tit=0., cb=None, cblab=0.4,
                 xxr=1., scale=0.7, margin=0.1, proj=None):
        if int(col) in [1, 2]:
            self._col = int(col)
        else:
            raise ValueError("'col' is column size of figure, (1 or 2)")
        if int(nx) in range(1, 10):
            self._nx = int(nx)
        else:
            raise ValueError("'nx' is number of column in figure, (1 to 9)")
        if int(ny) in range(1, 10):
            self._ny = int(ny)
        else:
            raise ValueError("'ny' is number of line in figure, (1 to 9)")
        self._yr = np.zeros(ny, dtype=float)
        self._xr = np.zeros(nx, dtype=float)
        self._xl = np.zeros(ny, dtype=float)
        self._yl = np.zeros(nx, dtype=float)
        self._tp = np.zeros(ny, dtype=float)
        self._cbw = np.zeros(nx, dtype=float)
        self._cbl = np.zeros(nx, dtype=float)
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
            self._cbw[:] = 0.
            self._cbl[:] = 0.
        else:
            self._cbw[:] = cb
            self._cbl[:] = cblab
        self._sc = 1./float(scale)
        self._mg = np.zeros(4, dtype=float)
        self._mg[:] = margin

    _fig = None
    _ax = None
    _cax = None
    _sharex = False
    _sharey = False

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

    def shareaxes(self, xy=None, pad=0.):
        if xy is None:
            xy = (True, True)
        else:
            try:
                xy = (xy[0], xy[1])
            except:
                raise ValueError("ex) xy=(True, False)")
        if xy[0] and self._ny > 1:
            self._sharex = True
            self._xl[1:] = 0.
            self._yp[:] = pad
            self._tp[:-1] = 0.
        if xy[1] and self._nx > 1:
            self._sharey = True
            self._yl[1:] = 0.
            self._xp[:] = pad
            self._cbw[:-1] = 0.
            self._cbl[:-1] = 0.

    def drawfig(self, verbose=False):
        page_width = 7.3*self._sc
        col_width = 3.485*self._sc
        page_height = 8.0*self._sc
        outx = self._yl.sum()+self._xp.sum()+self._cbw.sum()+self._cbl.sum()+self._mg[[0, 2]].sum()
        outy = self._xl.sum()+self._yp.sum()+self._tp.sum()+self._mg[[1, 3]].sum()
        if self._col == 1:
            fig_width = col_width
        else:
            fig_width = page_width
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
            print('page width =', page_width)
            print('page height =', page_height)
            print('column width =', col_width)
            print('x-label height =', self._xl)
            print('y-label width =', self._yl)
            print('x-pad width =', self._xp)
            print('y-pad height =', self._yp)
            print('colorbar width =', self._cbw)
            print('colorbar label width =', self._cbl)
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
        for yi in range(self._ny):
            for xi in range(self._nx):
                x0 = (self._mg[0]+self._yl[:xi+1].sum()+xs[:xi].sum()+self._xp[:xi].sum()
                      +self._cbw[:xi].sum()+self._cbl[:xi].sum())/fig_width
                y0 = (self._mg[1]+self._xl[:yi+1].sum()+ys[:yi].sum()+self._tp[:yi].sum()
                      +self._yp[:yi].sum())/fig_height
                x1 = xs[xi]/fig_width
                y1 = ys[yi]/fig_height
                if verbose:
                    print('ax[{}, {}] = ({:.3f}, {:.3f}, {:.3f}, {:.3f})'.format(yi, xi, x0, y0, x1, y1))
                self._ax[yi, xi] = self._fig.add_axes([x0, y0, x1, y1], projection=self._pj[yi, xi])
                if self._sharey and xi > 0:
                    self._ax[yi, xi].yaxis.set_major_formatter(plt.NullFormatter())
                    self._ax[yi, xi].yaxis.set_minor_formatter(plt.NullFormatter())
                if self._sharex and yi > 0:
                    self._ax[yi, xi].xaxis.set_major_formatter(plt.NullFormatter())
                    self._ax[yi, xi].xaxis.set_minor_formatter(plt.NullFormatter())
        for yi in range(self._ny):
            for xi in range(self._nx):
                x0 = (self._mg[0]+self._yl[:xi+1].sum()+xs[:xi+1].sum()+self._xp[:xi].sum()
                      +self._cbw[:xi].sum()+self._cbl[:xi].sum())/fig_width
                y0 = (self._mg[1]+self._xl[:yi+1].sum()+ys[:yi].sum()+self._tp[:yi].sum()
                      +self._yp[:yi].sum())/fig_height
                x1 = self._cbw[xi]/fig_width
                y1 = ys[yi]/fig_height
                if verbose:
                    print('cax[{}, {}] = ({:.3f}, {:.3f}, {:.3f}, {:.3f})'.format(yi, xi, x0, y0, x1, y1))
                if x1 > 0.:
                    self._cax[yi, xi] = self._fig.add_axes([x0, y0, x1, y1])
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

    def sharecolorbar(self, loc='right', width=0.1):
        if loc == 'right':
            x0, y0 = self._ax[0, -1]._position.get_points().flatten()[[2, 1]]
            x1 = width/self._fw
            y1 = self._ax[-1, -1]._position.get_points().flatten()[3]-y0
            self._cax = self._fig.add_axes([x0, y0, x1, y1])
        elif loc == 'bottom':
            pass
        else:
            raise ValueError("Shared color bar can be located 'right' or 'bottom'.")
        return self._cax
