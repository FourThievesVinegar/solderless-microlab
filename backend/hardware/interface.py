from hardware import package

exec('from hardware.' + package + ' import interface as hw')

def heat():
    global package
    print(package)
    hw.heat()
