import shiboken2
from PySide2 import QtWidgets
from maya import OpenMayaUI as omui
from maya import cmds


class WorkspaceControl(object):

    def __init__(self, name, windowType):
        self.name = name
        self.workspaceWidget = self.getWorkspaceWidget()
        self.widget = self.getShapeEditorWidget(windowType)

    def create(self, label, widget, ui_script=None):
        cmds.workspaceControl(self.name, label=label, retain=True)
        if ui_script:
            cmds.workspaceControl(self.name, e=True, uiScript=ui_script, minimumWidth=300, initialWidth=300)

        self.add_widget_to_layout(widget)
        self.set_visible(True)

    def restore(self, widget):
        if self.widget:

            if self.widget != widget:
                self.widget.close()
                self.widget.setParent(None)
                self.widget.deleteLater()
                self.add_widget_to_layout(widget)

            self.set_visible(True)
        else:
            self.add_widget_to_layout(widget)
            self.set_visible(True)

    def add_widget_to_layout(self, widget):
        if widget:
            self.widget = widget
            # self.widget.setAttribute(QtCore.Qt.WA_DontCreateNativeAncestors)

            workspace_control_ptr = int(omui.MQtUtil.findControl(self.name))
            widget_ptr = int(shiboken2.getCppPointer(self.widget)[0])  # to support PySide2

            omui.MQtUtil.addWidgetToMayaLayout(widget_ptr, workspace_control_ptr)

    def exists(self):
        return cmds.workspaceControl(self.name, q=True, exists=True)

    def is_visible(self):
        return cmds.workspaceControl(self.name, q=True, visible=True)

    def set_visible(self, visible):
        if visible:
            cmds.workspaceControl(self.name, e=True, restore=True)
        else:
            cmds.workspaceControl(self.name, e=True, visible=False)

    def set_label(self, label):
        cmds.workspaceControl(self.name, e=True, label=label)

    def is_floating(self):
        return cmds.workspaceControl(self.name, q=True, floating=True)

    def is_collapsed(self):
        return cmds.workspaceControl(self.name, q=True, collapse=True)

    def deleteUI(self):
        if self.exists():
            cmds.deleteUI(self.name)
        self.deleteWidget()

    def deleteWidget(self):
        w = self.getWorkspaceWidget()
        if not w:
            return
        for child in w.children():
            if not isinstance(child, QtWidgets.QLayout):
                try:
                    child.close()
                    child.setParent(None)
                    child.deleteLater()
                except Exception:
                    pass

    def getShapeEditorWidget(self, windowType):
        if self.workspaceWidget:
            shapeEditorWidget = self.workspaceWidget.findChildren(windowType)
            if shapeEditorWidget:
                return shapeEditorWidget[0]

    def getWorkspaceWidget(self):
        workspaceC = omui.MQtUtil.findControl(self.name)
        if workspaceC:
            return shiboken2.wrapInstance(int(workspaceC), QtWidgets.QWidget)
