import sgtk
import hou
import os


class TkHoudiniTemplateHandler(object):
    def __init__(self, app):
        self.app = app

    def check_file(self):
        # Check if the file is empty and in a specific step, and if so, merge from template files.
        try:
            current_filepath = hou.hipFile.path()
            if "untitled" in current_filepath:
                categories = hou.node("/").children()
                nodes = hou.node("/").allSubChildren()

                difference = len(set(categories) ^ set(nodes))

                if difference != 0:
                    self.app.logger.debug(
                        "File is not empty, skipping template merging."
                    )
                    return

                else:
                    self.app.logger.debug(
                        "File is empty, checking if pipeline step is valid to merge files."
                    )
                    pipeline_steps = self.app.get_setting("pipeline_steps")
                    step = self.app.context.step.get("name")

                    if step in pipeline_steps:
                        self.app.logger.debug(
                            "Pipeline step corresponds to pipeline steps configuration, executing merging."
                        )
                        self.merge_file(step)

                    else:
                        self.app.logger.debug(
                            "Pipeline step is not specified in configuration, skipping template merging."
                        )

        except Exception as e:
            self.app.logger.debug("Checking file failed because %s." % str(e))

    def merge_file(self, step):
        try:
            # Building path to template file
            current_filepath = hou.hipFile.path()

            template_directory = self.app.get_template("templates_directory")
            template_directory = template_directory.apply_fields(current_filepath)

            file_extension = self.app.get_setting("file_extension")
            # Replace pipeline step name spaces with underscores
            filename = step.replace(" ", "_") + file_extension

            template_filepath = os.path.join(template_directory, filename).replace(
                os.sep, "/"
            )

            # Check if template file exists
            if os.path.isfile(template_filepath):
                try:
                    # Merging template file
                    self.app.logger.debug(
                        "Merging template file %s into current file."
                        % template_filepath
                    )
                    hou.hipFile.merge(template_filepath)
                except Exception as e:
                    hou.ui.displayMessage(str(e), severity=hou.severityType.Error)

            else:
                self.app.logger.debug(
                    "Could not find template file %s, skipping template file merging."
                    % template_filepath
                )

        except Exception as e:
            self.app.logger.debug("Merging file failed because %s" % str(e))
