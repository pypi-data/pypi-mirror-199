from PySide2 import QtCore, QtWidgets
from maya import OpenMayaUI
from shiboken2 import wrapInstance

from . import workspace, mayagpt


def getWorkSpace(name='femtoMayaGPT_workspace'):
    return workspace.WorkspaceControl(name, mayagpt.ChatGPTMayaUI)


def show(docked=True, autoReload=True):
    """
    run app in mayagpt
    """

    mayaWindow = wrapInstance(int(OpenMayaUI.MQtUtil.mainWindow()), QtWidgets.QWidget)

    # check if a ride windows has already been created
    mainWindow = getWindow()
    isNewWindow = False

    if not mainWindow:
        # create a main window object to attach our widget to.
        # This is more stable in Maya
        mainWindow = mayagpt.ChatGPTMayaUI(mayaWindow)
        isNewWindow = True

    if docked:
        ui_script = ''

        # mainWindow.toggleAutoReload(autoReload)
        if autoReload:
            ui_script = "from maya import cmds\nimport mayagpt\ncmds.evalDeferred('mayagpt.show(True,True)')"

        workspaceWidget = getWorkSpace()

        if isNewWindow and workspaceWidget.exists():
            # clear previous widgets
            workspaceWidget.deleteWidget()
            workspaceWidget.add_widget_to_layout(mainWindow)
            workspaceWidget.set_visible(True)
        elif workspaceWidget.exists():
            workspaceWidget.set_visible(True)
            workspaceWidget.add_widget_to_layout(mainWindow)
            mainWindow.show()
        else:
            workspaceWidget.create('MayaGPT', mainWindow, ui_script=ui_script)

        return mainWindow
    else:
        mainWindow.show()
        return mainWindow


def close():
    # print('new close')
    workspaceWidget = getWorkSpace()
    if workspaceWidget:
        workspaceWidget.deleteUI()
        return

    w = getWindow()
    if w:
        w.close()
        w.setParent(None)
        w.deleteLater()
        workspaceWidget = getWorkSpace()
        workspaceWidget.deleteUI()


def getWindow():
    # if there's a workspace widget, get the window from it
    workspaceWidget = getWorkSpace()
    if workspaceWidget.exists() and workspaceWidget.widget:
        return workspaceWidget.widget

    ptr = OpenMayaUI.MQtUtil.mainWindow()
    mayaWindow = wrapInstance(int(ptr), QtCore.QObject)
    windows = mayaWindow.findChildren(mayagpt.ChatGPTMayaUI)
    if windows:
        return windows[0]


if __name__ == '__main__':
    show()
