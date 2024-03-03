
import wifi
wifi.connect()


# Module import and install
try:
    import ulogging
except ImportError as e:
    import upip
    upip.install('pkg_resources')
    upip.install('pycopy-ulogging')
    upip.install('picoweb')

# App run
import webapp