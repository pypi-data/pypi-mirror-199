from plugin.plugin_manager import PluginManager
from tests.plugs.shape_plug_point import ShapePlugPoint


class Editor:
    # this class represents a graphical editor that has to
    # deal wth different shapes. It uses a generic shape plug point
    # to interact with "all kinds" of shapes.
    @staticmethod
    def draw():
        return _get_shape_plugin().draw()


def test_happy_path():
    # ###################### this part is done in MONADS #################### #
    # core monads define plug points and the default plugins
    # this definition goes into a file. (like plug_point_config.py at the root of monad repo)
    shapes_plug_point_configuration = {
        "shape_plug_point": {
            "plug_point_class": "ShapePlugPoint",  # the default plugin
            "plugin_module": "tests.plugs.rectangle_plug_in",  # the default plugin
            "plugin_class": "RectanglePlugIn",  # the default plugin
            "description": "provides rectangle implementation of shape plug point",
            "pluggable": "test_plugin_framework"  # python module that uses the plug point
        },
    }
    # core will call this to initialize core plugins.
    PluginManager.setup_core_plugins(shapes_plug_point_configuration)
    assert Editor.draw() == "rectangle"

    # ###################### this part is done in MICROSERVICES #################### #
    #
    shape_override_plugin_dict = {
        "shape_plug_point": "tests.plugs.circle_plug_in"
    }
    PluginManager.override_plugins(shape_override_plugin_dict)
    assert Editor.draw() == "circle"


def _get_shape_plugin() -> ShapePlugPoint:
    """
    convinence method to get the plugin for this plug point
    :return:
    """
    # tip: don't save this in this class. when core initializes/imports this module
    # infrastructure code would not have had opportunity to override. this why it is
    # important to always go to plugin manager for the most current plugin
    return PluginManager.get_plugin("shape_plug_point")
