import sys
from PyQt5.QtWidgets import QApplication
import asyncio
import quamash

from modules.mainwindow import MainWindow
from modules.User import User


ICON = "img/emotiv_icon.png"

# set icons everywhere

if __name__ == "__main__":
    # root = Tk()
    # icon = PhotoImage(file=ICON)
    # root.tk.call('wm', 'iconphoto', root._w, icon)
    # root.title("Biomeh")
    user = User()
    # ss = StartScreen(root, user)
    # root.mainloop()

    loop = asyncio.get_event_loop()
    # pyqt
    app = QApplication(sys.argv)
    loop = quamash.QEventLoop(app)
    asyncio.set_event_loop(loop) 

    main_window = MainWindow(user, loop)
    loop.run_until_complete(main_window.setup_device())
    try:
        loop_tasks = [
            asyncio.ensure_future(main_window.device.read_data()),
            asyncio.ensure_future(main_window.device.update_console()),
            asyncio.ensure_future(main_window.read_data()),
            asyncio.ensure_future(main_window.update_curves())
        ]
        finished, pending = loop.run_until_complete(
            asyncio.wait(loop_tasks))

    except KeyboardInterrupt:
        main_window.device.running = False
        for task in pending:
            task.cancel()
    main_window.device.close()
    sys.exit(app.exec_())
    loop.close()
