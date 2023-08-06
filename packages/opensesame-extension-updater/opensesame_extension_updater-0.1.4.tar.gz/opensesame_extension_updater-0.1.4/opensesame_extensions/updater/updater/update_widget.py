"""This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""
from libopensesame.py3compat import *
from libopensesame.oslogging import oslogger
from libqtopensesame.widgets.base_widget import BaseWidget
from libqtopensesame.pyqode_extras.widgets import TextCodeEdit
import os


class UpdateWidget(BaseWidget):
    
    def __init__(self, parent):
        super().__init__(parent, ui='extensions.updater.update_widget')
        self._editor = TextCodeEdit(parent)
        self.ui.vertical_layout.addWidget(self._editor)
        if os.access(os.path.dirname(__file__), os.W_OK):
            self.ui.label_administrator.hide()
        else:
            self.ui.button_update.setEnabled(False)
        self.ui.button_update.clicked.connect(self._run_script)
        self.extension_manager.fire('register_editor', editor=self._editor)
        
    def set_script(self, script):
        self._editor.setPlainText(script)
        
    def _run_script(self):
        self.extension_manager.fire('jupyter_run_code',
                                    code=self._editor.toPlainText())
