from numbers import Number
from matplotlib import pyplot
from math import exp

#some unit conversion functions
def kelvin(n : Number) -> Number:
	return n + 273.15

def celsius(n):
	return n - 273.15

height = list(map(lambda x : x * 1e3, range(12))) # height layers in meters, given by task 
temp = [
	18,
	11,
	6,
	1,
	-5,
	-11,
	-17,
	-24,
	-31,
	-39,
	-46,
	-50] # given by task 

pressures = [1e5]

# temperatures are needed in kelvin. bulk conversion is nicer to read
ktemp = list(map(kelvin, temp)) 

#the constant for the mangus formula
magicConst = 6.1078 # hPa

def satIce(v):
	if v > 0.0: return satWater(v)
	return magicConst * exp((21.8745584 * v)/(265.49 + v))

def satWater(v): # for some godforsaken reason v needs to be in degree celsius
	return magicConst * exp((17.2693882 * v)/(237.29 + v))

g = 9.81 # grav. const. for earth
Rg = 287 # unversial gas constant 

waterSats = []
iceSats = []
iceTemps = []

def p(p0, z0, z1, T0, T1):
	y = abs((T1 - T0)/(z1 - z0))
	return p0 * pow((T0-(y*z1))/(T0-(y*z0)), g/(y*Rg))

for n in range(1, 12): # populate pressures. note that we have a starting pressure
	p1 = p(pressures[n - 1], height[n - 1], height[n], ktemp[n - 1], ktemp[n])
	pressures.append(p1)

for n in range(12): # calculate the saturation pressures of water and, for temps below freezing of ice 
	waterSats.append(satWater(temp[n]))
	if temp[n] <= 0:
		iceTemps.append(temp[n])
		iceSats.append(satIce(temp[n]))
		print(temp[n], "\t|",satWater(temp[n]), "\t| ", satIce(temp[n]))
	else:
		print(temp[n], "\t|",satWater(temp[n]))

print()

#"pretty" pringin the table in the task
for n in range(12):
	print(height[n]/1000.0,"\t|\t", celsius(ktemp[n]), "\t|", pressures[n]/100.0)

# just plotting
pyplot.plot(iceTemps, iceSats, label="ice [Millibar]")
pyplot.plot(temp, waterSats, label="water [Millibar]")
pyplot.legend(loc="upper left")
pyplot.title("Saturation pressure, using Magnus formula")
pyplot.xlabel("temperature [C]")
pyplot.ylabel("pressure [Millibar]")
pyplot.show()

print("this is a change")