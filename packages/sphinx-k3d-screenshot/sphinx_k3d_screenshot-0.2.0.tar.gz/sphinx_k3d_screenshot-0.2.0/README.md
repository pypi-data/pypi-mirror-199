# sphinx_k3d_screenshot

[![PyPI version](https://badge.fury.io/py/sphinx-k3d-screenshot.svg)](https://badge.fury.io/py/sphinx-k3d-screenshot)
[![Conda (channel only)](https://img.shields.io/conda/vn/davide_sd/sphinx_k3d_screenshot?color=%2340BA12&label=conda%20package)](https://anaconda.org/Davide_sd/sphinx_k3d_screenshot)
[![Documentation Status](https://readthedocs.org/projects/sphinx-k3d-screenshot/badge/?version=latest)](https://sphinx-k3d-screenshot.readthedocs.io/en/latest/?badge=latest)

A Sphinx directive for including the screenshot of a K3D Jupyter plot
into a Sphinx document.

_**This package is based on [matplotlib's plot directive](https://matplotlib.org/stable/api/sphinxext_plot_directive_api.html).**_

## Install

```
pip install sphinx_k3d_screenshot
```

or:

```
conda install -c davide_sd sphinx_k3d_screenshot 
```

Take a look at the [Installation page](https://sphinx-k3d-screenshot.readthedocs.io/en/latest/install.html)
to understand how to configure the extension to run on [readthedocs.org server](https://readthedocs.org).

## Usage

```python
.. k3d-screenshot::

   f = lambda r, d: 5 * np.cos(r) * np.exp(-r * d)
   x, y = np.mgrid[-7:7:100j, -7:7:100j]
   r = np.sqrt(x**2 + y**2)
   z = f(r, 0.1)

   fig = k3d.plot()
   surface = surface = k3d.surface(
      z.astype(np.float32), bounds=[-7, 7, -7, 7],
      attribute=z.astype(np.float32),
      color_map=k3d.colormaps.matplotlib_color_maps.viridis)
   fig += surface

   fig
```

<img src="https://raw.githubusercontent.com/Davide-sd/sphinx_k3d_screenshot/master/imgs/screenshot-1.png">

Take a look at the [Examples page](https://sphinx-k3d-screenshot.readthedocs.io/en/latest/examples/index.html)
to visualize the available customization options.
