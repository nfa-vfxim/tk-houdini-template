"""
File Cache node App for use with Toolkit's Houdini engine.
"""

import sgtk
import hou


class TkHoudiniTemplate(sgtk.platform.Application):
    def init_app(self):
        """Initialize the app."""
        tk_houdini_template = self.import_module("tk_houdini_template")
        self.handler = tk_houdini_template.TkHoudiniTemplateHandler(self)

        self.handler.check_file()
