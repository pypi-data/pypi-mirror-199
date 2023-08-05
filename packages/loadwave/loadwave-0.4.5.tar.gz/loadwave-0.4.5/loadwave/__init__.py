import sys
import threading
import time
from colorama import Fore, Style

class Loader:
    def __init__(self, bar_length=30):
        self.stop_flag = None
        self.loader_thread = None
        self.progress = 0
        self.bar_length = bar_length

    def start(self):
        self.stop_flag = False
        self.loader_thread = threading.Thread(target=self.loader)
        self.loader_thread.start()

    def stop(self):
        self.stop_flag = True
        self.loader_thread.join()

    def loader(self):
        while not self.stop_flag:
            progress_bar = self.progress_bar()
            sys.stdout.write(f"\r[{progress_bar}]")
            sys.stdout.flush()
            if self.progress >= self.bar_length:
                break
            time.sleep(0.1)
            self.progress += 1

        if not self.stop_flag:
            self.animate()

    def progress_bar(self, bar_length=30):
        filled = int(self.progress / bar_length * bar_length)
        empty = bar_length - filled
        filled_bar = Fore.RED + '-' * filled + Style.RESET_ALL
        empty_bar = Fore.LIGHTBLACK_EX + '-' * empty + Style.RESET_ALL
        progress_bar = f"{filled_bar}{empty_bar}"
        
        # Eğer bar dolarsa animasyon başlat
        if self.progress >= bar_length:
            animation = "/" if self.progress % 2 == 0 else "\\"
            progress_bar = f"{progress_bar[2:]}[{Fore.YELLOW}{Style.RESET_ALL}]"
        
        return progress_bar

    def animate(self):
        sys.stdout.write("\n")
        animation = ['/', '|', '\\', '-']
        idx = 0
        while not self.stop_flag:
            sys.stdout.write(f"\r[{Fore.YELLOW}{animation[idx]}{Style.RESET_ALL}]")
            sys.stdout.flush()
            idx = (idx + 1) % len(animation)
            time.sleep(0.1)
        sys.stdout.write("\n")
        sys.stdout.write('\r' + ' ' * (self.bar_length + 4) + '\r')
        sys.stdout.flush()

class Process:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        loader = Loader()
        loader.start()
        result = self.func(*args, **kwargs)
        loader.stop()
        return result

def process(func):
    return Process(func)
