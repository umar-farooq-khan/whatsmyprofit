#!C:\Users\umar\PycharmProjects\whatsmyprofit\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'autoflake==1.3.1','console_scripts','autoflake'
__requires__ = 'autoflake==1.3.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('autoflake==1.3.1', 'console_scripts', 'autoflake')()
    )
