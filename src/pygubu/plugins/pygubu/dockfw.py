import tkinter as tk
import tkinter.ttk as ttk

from pygubu.api.v1 import (
    register_widget,
    register_custom_property,
    BuilderObject,
)
from pygubu.i18n import _

import pygubu.widgets.dockfw.dockwidget as widgets


class DockWidgetBaseBO(BuilderObject):
    def _get_init_args(self, extra_init_args: dict = None):
        args = super()._get_init_args(extra_init_args)
        if "uid" not in args:
            args["uid"] = self.wmeta.identifier
        return args


class DockFrameBO(DockWidgetBaseBO):
    class_ = widgets.DockFrame
    container = True
    container_layout = False
    maxchildren = 1


_builder_id = "pygubu.widgets.dockframe"
register_widget(
    _builder_id, DockFrameBO, "DockFrame", ("ttk", _("Pygubu Widgets"))
)


class DockPaneBO(DockWidgetBaseBO):
    class_ = widgets.DockPane
    container = True
    container_layout = False
    layout_required = False
    properties = ("orient",)
    ro_properties = properties

    @classmethod
    def canbe_child_of(cls, parent_builder, classname):
        allowed = False
        if parent_builder in (DockFrameBO, DockPaneBO):
            allowed = True
        print("canbe_child", parent_builder, classname, allowed)
        return allowed

    def __init__(self, builder, wmeta):
        super().__init__(builder, wmeta)
        self.pane_widget = None

    def realize(self, parent, extra_init_args: dict = None):
        self.widget: widgets.DockFrame = parent.widget
        args = self._get_init_args(extra_init_args)
        if not self.widget.main_pane:
            args["main_pane"] = True
            print("Main pane created.")
        self.pane_widget = self.widget.new_pane(**args)
        if isinstance(parent, DockPaneBO):
            parent.pane_widget.add_pane(self.pane_widget)
        return self.widget

    def configure(self, target=None):
        pass

    def layout(self, target=None):
        pass


_builder_id = "pygubu.widgets.dockpane"
register_widget(
    _builder_id, DockPaneBO, "DockPane", ("ttk", _("Pygubu Widgets"))
)


class DockWidgetBO(DockWidgetBaseBO):
    class_ = widgets.DockWidget
    container = True
    container_layout = True
    layout_required = False

    @classmethod
    def canbe_child_of(cls, parent_builder, classname):
        allowed = False
        if parent_builder is DockPaneBO:
            allowed = True
        print("canbe_child", parent_builder, classname, allowed)
        return allowed

    def realize(self, parent, extra_init_args: dict = None):
        dock = parent.pane_widget.maindock
        args = self._get_init_args(extra_init_args)
        print("Creating new widget. Args: ", args)
        self.widget = dock.new_widget(**args)
        parent.pane_widget.add_widget(self.widget)

    def get_child_master(self):
        return self.widget.fcenter


_builder_id = "pygubu.widgets.dockwidget"
register_widget(
    _builder_id, DockWidgetBO, "DockWidget", ("ttk", _("Pygubu Widgets"))
)
