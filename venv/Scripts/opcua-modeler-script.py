#!c:\users\ches\desktop\university\709\individual_files_group03\venv\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'opcua-modeler==0.5.9','console_scripts','opcua-modeler'
__requires__ = 'opcua-modeler==0.5.9'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('opcua-modeler==0.5.9', 'console_scripts', 'opcua-modeler')()
    )
