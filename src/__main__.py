import os
import logging
import PasswordManager

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

if __name__ == '__main__':
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    PasswordManager.main()
