import subprocess
import win32gui
import win32con
import time
import sys

def hide():
  while True:
    window_list = []
    enum_callback = lambda hwnd, x: window_list.append((hwnd, win32gui.GetWindowText(hwnd)))
    win32gui.EnumWindows(enum_callback, None)
    
    windows = [(hwnd, title) for hwnd, title in window_list if "\Left 4 Dead 2\left4dead2.exe" in title]

    if len(windows) > 0:
      game_window = windows[0][0]
      
      try:
        win32gui.ShowWindow(game_window, win32con.SW_MINIMIZE)

      except Exception:
        pass

    time.sleep(0.2)

if __name__ == "__main__":
  try:
    hide()
  except (KeyboardInterrupt, SystemExit):
    print("Canceled by user, no longer hiding L4D2 windows.")

  sys.exit()