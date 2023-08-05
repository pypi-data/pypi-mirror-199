import pdb

import os
from collections import Counter

import pytest
import numpy as np
from numpy.testing import assert_allclose, assert_equal
from glue.core import data_factories as df
from glue.app.qt import GlueApplication
from glue.core.subset import AndState
from glue.core.roi import RectangularROI
from glue.config import colormaps
from glue.utils.qt import process_events
from glue.core.state import GlueUnSerializer

from glue_small_multiples.qt.viewer import SmallMultiplesViewer

DATA = os.path.join(os.path.dirname(__file__), 'data')
NUM_ADELIE = 152
NUM_CHINSTRAP = 68
NUM_GENTOO = 124
CMAP_PROPERTIES = set(['cmap_mode', 'cmap_att', 'cmap_vmin', 'cmap_vmax', 'cmap'])
MARKER_PROPERTIES = set(['size_mode', 'size_att', 'size_vmin', 'size_vmax', 'size_scaling', 'size', 'fill'])
LINE_PROPERTIES = set(['linewidth', 'linestyle'])


app = GlueApplication()
session = app.session
hub = session.hub
data_collection = session.data_collection
penguins = df.load_data(os.path.join(DATA, 'penguins.csv'))
penguin_data = penguins
data_collection.append(penguin_data)
print("@@@@@ making a new_data viewer @@@@@")
viewer = app.new_data_viewer(SmallMultiplesViewer)
print("@@@@@ adding data to the viewer @@@@@")
viewer.add_data(penguin_data)
viewer_state = viewer.state