
import wifi
wifi.connect()


# Module import and install
try:
    import logging
except ImportError as e:
    import mip
    mip.install('pkg_resources')
    mip.install('logging')



# App run
import webapp
