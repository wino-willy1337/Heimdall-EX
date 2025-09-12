# file: util/spinner.py

import sys
import time
import threading

class Spinner:
    """A simple command line spinner."""
    def __init__(self, message="Scanning..."):
        self.spinner_chars = "|/-\\"
        self.message = message
        self.running = False
        self.thread = None

    def start(self):
        """Starts the spinner in a separate thread."""
        self.running = True
        self.thread = threading.Thread(target=self._spin)
        self.thread.start()

    def _spin(self):
        """The private method that does the spinning."""
        while self.running:
            for char in self.spinner_chars:
                if not self.running:
                    break
                sys.stdout.write(f'\r{self.message} {char}')
                sys.stdout.flush()
                time.sleep(0.1)
        # Clear the spinner line when done
        sys.stdout.write('\r' + ' ' * (len(self.message) + 2) + '\r')
        sys.stdout.flush()

    def stop(self):
        """Stops the spinner."""
        self.running = False
        if self.thread:
            self.thread.join()