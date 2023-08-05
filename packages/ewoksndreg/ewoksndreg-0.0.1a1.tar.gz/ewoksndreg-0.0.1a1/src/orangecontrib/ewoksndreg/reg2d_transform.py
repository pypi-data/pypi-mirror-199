from contextlib import contextmanager
from AnyQt import QtWidgets

from silx.gui.plot import Plot2D
from silx.gui.widgets.FrameBrowser import HorizontalSliderWithBrowser

from ewoksorange.bindings import OWEwoksWidgetOneThread
from ewoksorange.bindings import ow_build_opts
from ewoksorange.gui.parameterform import ParameterForm

from ewoksndreg.tasks import Reg2DTransform
from ewoksndreg.io.input_stack import input_context


__all__ = ["OWReg2DTransform"]


class OWReg2DTransform(
    OWEwoksWidgetOneThread, **ow_build_opts, ewokstaskclass=Reg2DTransform
):
    name = "2D Transformation"
    description = "Apply image transformations to a stack of images"

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._init_control_area()
        self._init_main_area()

    def _init_control_area(self):
        super()._init_control_area()
        self._default_inputs_form = ParameterForm(parent=self.controlArea)
        values = self.get_default_input_values(include_missing=True)

        options = {
            "imagestack": {"value_for_type": "", "select": "h5dataset"},
            "inputs_are_stacks": {"value_for_type": False},
            "url": {"value_for_type": ""},
        }

        for name, kw in options.items():
            if name not in options:
                continue
            self._default_inputs_form.addParameter(
                name,
                value=values[name],
                value_change_callback=self._default_inputs_changed,
                **kw,
            )

    def _default_inputs_changed(self):
        self.update_default_inputs(**self._default_inputs_form.get_parameter_values())
        self._update_input_data()

    def handleNewSignals(self) -> None:
        self._update_input_data()
        super().handleNewSignals()

    def task_output_changed(self):
        self._update_output_data()

    def _init_main_area(self):
        super()._init_main_area()
        layout = self._get_main_layout()

        self._tabs = QtWidgets.QTabWidget(parent=self.mainArea)
        layout.addWidget(self._tabs)

        w = QtWidgets.QWidget(parent=self.mainArea)
        layout = QtWidgets.QVBoxLayout()
        w.setLayout(layout)
        self._oplot = Plot2D(parent=w)
        self._oslider = HorizontalSliderWithBrowser(parent=w)
        layout.addWidget(self._oplot)
        layout.addWidget(self._oslider)
        self._tabs.addTab(w, "Aligned")

        w = QtWidgets.QWidget(parent=self.mainArea)
        layout = QtWidgets.QVBoxLayout()
        w.setLayout(layout)
        self._iplot = Plot2D(parent=w)
        self._islider = HorizontalSliderWithBrowser(parent=w)
        layout.addWidget(self._iplot)
        layout.addWidget(self._islider)
        self._tabs.addTab(w, "Original")

        self._islider.valueChanged[int].connect(self._select_input_image)
        self._oslider.valueChanged[int].connect(self._select_output_image)
        self._update_input_data()

    @contextmanager
    def _input_context(self, images=None):
        if images is not None:
            yield images
            return
        try:
            binit = True
            with input_context(self.get_task_input_value("imagestack")) as images:
                binit = False
                yield images
        except TypeError:
            if binit:
                yield list()

    @contextmanager
    def _output_context(self, images=None):
        if images is not None:
            yield images
            return
        try:
            binit = True
            with input_context(self.get_task_output_value("imagestack")) as images:
                binit = False
                yield images
        except TypeError:
            if binit:
                yield list()

    def _update_input_data(self):
        dynamic = self.get_dynamic_input_names()
        for name in self.get_input_names():
            self._default_inputs_form.set_parameter_enabled(name, name not in dynamic)

        with self._input_context() as images:
            self._islider.setMaximum(max(len(images) - 1, 0))
            self._select_input_image(self._islider.value(), images=images)

    def _select_input_image(self, select, images=None):
        with self._input_context(images=images) as images:
            if images:
                self._iplot.addImage(images[select], legend="image")

    def _update_output_data(self):
        with self._output_context() as images:
            self._oslider.setMaximum(max(len(images) - 1, 0))
            self._select_output_image(self._oslider.value(), images=images)

    def _select_output_image(self, select, images=None):
        with self._output_context(images=images) as images:
            if images:
                self._oplot.addImage(images[select], legend="image")
