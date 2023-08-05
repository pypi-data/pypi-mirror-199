import pytest
from unittest.mock import MagicMock

from glue.core import Data, DataCollection
from glue.core.component_id import ComponentID
from echo.selection import SelectionCallbackProperty
from glue.core.state_objects import State
from glue.core.coordinates import IdentityCoordinates

from glue.core.data_combo_helper import (ComponentIDComboHelper, ManualDataComboHelper,
                                 DataCollectionComboHelper)
def selection_choices(state, property):
    items = getattr(type(state), property).get_choice_labels(state)

    return ":".join(items).replace('Coordinate components', 'coord').replace('Main components', 'main').replace('Derived components', 'derived')

class ExampleState(State):
    combo = SelectionCallbackProperty()

class ExampleStateDefaultIndex(State):
    combo = SelectionCallbackProperty(default_index=1)


def test_default_index():
    state = ExampleStateDefaultIndex()
    data = Data(x=[1, 2, 3], y=[2, 3, 4], z=['a','b','c'], label='data1')
    dc = DataCollection([data])

    helper = ComponentIDComboHelper(state, 'combo', dc)
    helper.append_data(data)
    assert state.combo == data.id['y']

def test_component_id_combo_helper_none():

    # Make sure the none=True option works

    state = ExampleState()

    data = Data(x=[1, 2, 3], y=[2, 3, 4], label='data1')
    dc = DataCollection([data])

    helper = ComponentIDComboHelper(state, 'combo', dc)
    helper.append_data(data)

    assert selection_choices(state, 'combo') == "x:y"

    helper.none = True

    assert selection_choices(state, 'combo') == ":x:y"

    helper.none = 'banana'

    assert selection_choices(state, 'combo') == "banana:x:y"

    # Try with initializing none=... from the start

    helper = ComponentIDComboHelper(state, 'combo', dc, none=True)
    helper.append_data(data)
    assert selection_choices(state, 'combo') == ":x:y"

    helper = ComponentIDComboHelper(state, 'combo', dc, none='banana')
    helper.append_data(data)
    assert selection_choices(state, 'combo') == "banana:x:y"


def test_component_id_combo_helper_none_default():

    state = ExampleStateDefaultIndex()
    data = Data(x=[1, 2, 3], y=[2, 3, 4], label='data1')
    dc = DataCollection([data])

    helper = ComponentIDComboHelper(state, 'combo', dc)
    helper.append_data(data)
    assert state.combo == data.id['y']

    state = ExampleState()
    helper = ComponentIDComboHelper(state, 'combo', dc, none=True)
    helper.append_data(data)
    assert selection_choices(state, 'combo') == ":x:y"
    assert state.combo == data.id['y']