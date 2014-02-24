from distutils.core import setup
import py2exe

includes = ['urllib']

setup(options = {"py2exe": {
                                "includes": includes,
                                "bundle_files": 1,
                                "compressed": True,

                           }
                },
      windows=['frc_gui.py'],
      console=[dict(script="frc_gui.py",
          dest_base="require_admin",
          uac_info="requireAdministrator")])