
from pyface.api import GUI, OK, FileDialog, DirectoryDialog, ProgressDialog

def task_func(t):
    progress = ProgressDialog(title="progress", message="counting to %d",
                max=t, show_time=True, can_cancel=True)
    progress.open()

for i in range(0,30):
    time.sleep(1)
    print i
    (cont, skip) = progress.update(i)
    if not cont or skip:
        break

progress.update(t)
