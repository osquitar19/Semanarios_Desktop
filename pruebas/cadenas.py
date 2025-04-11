#       "012345"
kilos = "020406"
print("1: "+kilos[0:2]+"\n")
print("2: "+kilos[2:4]+"\n")
print("3: "+kilos[4:6]+"\n")
def formatear_desarrollo(desarrollo_carrera):
    uno = int(desarrollo_carrera[0:2])
    dos = int(desarrollo_carrera[2:4])
    tre = int(desarrollo_carrera[4:6])
    return f"{uno}º\t{dos}º\t{tre}º"

print(formatear_desarrollo(kilos))