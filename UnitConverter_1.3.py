Comments = (
    # This program will attempt to help the user convert between units.
    # The goal will be to include both metric and imperial units.
    # The metric units will be easier due to their nature.
    # https://codereview.stackexchange.com/questions/101348/unit-converter-in-python
    # Using above for tips and/or cheats.
    # https://en.wikipedia.org/wiki/Measurement
    # Use for assigning base units, rework if time
    # Subgoal is to work to correct the dictionaries to have a "base unit" that will ease conversions between imperial and metric.
        # This subgoal will need to make a new function, and will be 'real' coding versus data input.
    # Likely, I plan to work with everything by putting it into a class. This may be easier than having freefloating functions. 
    # Current categories include weight/mass, length, and volume. Other units will need to include force, and maybe area and length-volume.
)

# imports to make it work. Might not need these, honestly.
from datetime import time 
from datetime import date 
from datetime import datetime 
import math

# These units help the program decide if the conversion can take place by determining if they are the same or not.
global fromUnitType 
global toUnitType 
fromUnitType = [None, None, None] # from unit string (unit), imperial or metric, type of measure (len, mass, vol) -- in that order
toUnitType = [None, None, None] # to unit string (unit), imperial or metric, type of measure (len, mass, vol) -- in that order
# Note that value of the specific units will not be used in this list.

class unitDictionaries():
    # Make "help" or 'h' option to give function that prints this dictionary, maybe version, too.
    # def help():

    # Imperial
    # This dictionary gives the conversion values between imperial volume measurements. Gallons are the base measurement.
    imperialVolumeConversions = {
        # Based off of complete unit names. May need to cross-reference to figure out abbreviations.
        # Volume measures based partially off of Wikipedia measurements, taken 08/29/2020
        # https://en.wikipedia.org/wiki/Imperial_units#Volume
        "fluid ounce": 160,
        "Gill": 40,
        "teacup": 40, #same as gill.
        "cups": 16,
        "pints": 8,
        "quarts": 4,
        "gallons": 1,
        "peck": 0.5,
        "bushel": 0.125,
        "quarter": 0.015625, # 1/64
        "fluid drachm": 1280, # Three fluid scruples
        "fluid scruple": 3840, # Twenty minims
        "minim": 76800,
        "teaspoon": 768, # 3 teaspoons in a tablespoon
        "tablespoon": 256, # 16 in a cup
        "dessertspoon": 384, # 2x a teaspoon
        "drop": 73728, # 1/96 teaspoon
        "smidgen": 24576, # 1/32 teaspoon
        "pinch": 12288, # 1/16 teaspoon
        "dash": 6144, # 1/8 tsp
        "scruple": 3072, # 1/4 tsp
        "saltspoon": 3072, # 1/4 tsp; same as scruple.
        "coffeespoon": 1536, # 1/2 tsp
        "fluid dram": 576, # 3/4 tsp
        "pottle": 2, # 2 quarts.
    }
    # This dictionary gives the conversion values between imperial length measurements. Feet are the base measurement.
    imperialLengthConversions = {
        # Measurements from Wikipedia, 8/29/2020.
        # https://en.wikipedia.org/wiki/Imperial_units#Length
        "thou": 1/12000,
        "in": 12,
        "foot": 1,
        "yard": 3,
        "chain": 66,
        "furlong": 660,
        "mile": 5280,
        "league": 15840,
        "fathom": 6.0761,
        "cable": 607.61,
        "nautical mile": 6076.1,
        "link": 0.66,
        "rod":  16.5, # 66/4
    }
    # This dictionary gives the conversion values between imperial weight/mass measurements. Pounds are the base measurement.
    imperialWeightConversions = {
        # Measurements taken from Wikipedia, (Aug) 08/29/2020.
        # https://en.wikipedia.org/wiki/Imperial_units#Mass_and_weight
        "grain": 7000,
        "drachm": 256,
        "ounce": 16,
        "pound": 1,
        "stone": 1/14, # 1/14
        "quarter": 1/28, # 1/28
        "hundredweight": 1/112, # 1/112
        "ton": 1/2240, # 1/2240
        "slug": 1/32.17404856, # 1/32.17404856 Technically a force unit.
    }

    # Metric
    # This dictionary gives the conversion values between metric weight/mass measurements. Grams are the base measurement.
    metricMassConversions = {
        "gram": 1,
        "kg": 1000,
        "hg": 100,
        "dag": 10,
        "g": 1,
        "dg": 0.1,
        "cg": 0.01,
        "mg": 0.001,
        "microg": 0.000001,
        "nanog": 0.000000001,
    }
    # This dictionary gives the conversion values between metric volume measurements. Liters are the base measurement.
    metricVolumeConversions = {
        "liter": 1,
        "L": 1,
        "kL": 1000,
        "hL": 100,
        "daL": 10,
        "dL": 0.1,
        "cL": 0.01,
        "mL": 0.001,
        "microL": 0.000001,
        "nanoL": 0.000000001,
    }
    # This bit of code is a dictionary of metric length conversions that convert within themselves. It uses meters as the base measurement.
    metricLengthConversions = {
        # currently based off unit suffix.
        # Might try expanding from just the abbreviated versions to the fuller versions, so that all valuable string input is received.
        "km": 1000,
        "hm": 100,
        "dam": 10,
        "m": 1,
        "dm": 0.1,
        "cm": 0.01,
        "mm": 0.001,
        "microm": 0.000001,
        "nanom": 0.000000001,
    }

    # Non-specific measurments like ppm or concentration will need to come with the 2d/3d unit converter.

    # The dictionary below will have the conversion factors between imperial and metric units. 
    # The conversion factors are based off of the base measurements for the dictionaries above.
    metricImperialConversions = {
        "foot": 0.3048,
        "gallon": 0.2641729,
        "pounds": 0.002204623,
        "grams": 453.5924,
        "Liters": 3.7854,
        "meters": 3.28084,
    }

#################################################################################################################################

# checkUnitDict checks if the argument is part of the conversion dictionaries. Will return 'True' if part of a dictionary, else False.
# Some units are present in multiple dictionaries in imperial. This function will need to be modified to account for that.
# Might be able to nest a function inside of here that will output a global variable for the measurement type.
    # General plan is to carry one variable with an array of data to help unify the results.

class unitLabelFunctions():
    def unitNumberCount(self, parameter_list):
        """
        docstring
        """
        pass

def isLength(UnitL):
    if UnitL in unitDictionaries.metricLengthConversions:
        return True
    elif UnitL in unitDictionaries.imperialLengthConversions:
        return True
    else: 
        return False

def isWeight(UnitW):
    if UnitW in unitDictionaries.metricMassConversions:
        return True
    elif UnitW in unitDictionaries.imperialWeightConversions:
        return True
    else:
        return False

def isVolume(UnitV):
    if UnitV in unitDictionaries.metricVolumeConversions:
        return True
    elif UnitV in unitDictionaries.imperialVolumeConversions:
        return True
    else:
        return False

def checkUnitDict(test_Unit):
    unitType = None
    if isLength(test_Unit):
        return True 
    elif isWeight(test_Unit):
        return True
    elif isVolume(test_Unit):
        return True
    else:
        print("The units input are not known for the conversion. Try again.")
        return False

def assSysDict(reass_Unit):
    if reass_Unit in unitDictionaries.metricLengthConversions:
        return "metric"
    elif reass_Unit in unitDictionaries.imperialLengthConversions:
        return "imperial"
    elif reass_Unit in unitDictionaries.metricMassConversions:
        return "metric"
    elif reass_Unit in unitDictionaries.imperialWeightConversions:
        return "imperial"
    elif reass_Unit in unitDictionaries.metricVolumeConversions:
        return "metric"
    elif reass_Unit in unitDictionaries.imperialVolumeConversions:
        return "imperial"
    else:
        print("An error has occurred while assigning type. Type may not belong to imperial or metric units.")
        return False

def assUnitDict(reass_Unit):
    unitType = None
    if reass_Unit in unitDictionaries.metricLengthConversions:
        return "len"
    elif reass_Unit in unitDictionaries.imperialLengthConversions:
        return "len"
    elif reass_Unit in unitDictionaries.metricMassConversions:
        return "mass"
    elif reass_Unit in unitDictionaries.imperialWeightConversions:
        return "mass"
    elif reass_Unit in unitDictionaries.metricVolumeConversions:
        return "vol"
    elif reass_Unit in unitDictionaries.imperialVolumeConversions:
        return "vol"
    else:
        print("An error has occurred while assigning type.")
        return False

#Further code may need to check which unit a person is testing.
# as an example, "cups" is not in the metric dictionary, and is a volume measurement.
# So, testing where the unit belongs and where the unit will go will need to be a place to invest time into.

def unitSysCompat(fromUnitCompat, toUnitCompat):
    # Input can be a list as an argument.
    if fromUnitCompat[1] == toUnitCompat[1]:
        print("Units are from same measurement system.")
        return True
    else:
        print("Units are from different system.")
        return False

def unitTypeCompat(fromUnitCompat, toUnitCompat):
    # Input can be a list as an argument.
    if fromUnitCompat[2] == toUnitCompat[2]:
        print("Units are the same measurement type.")
        return True
    else:
        print("Units are of a different measurement type.")
        return False

# Functions below (fromUnitConversion & toUnitConversion) get the input from the user for the units to convert to and from.
# Functions use the checkUnitDict function, above.
def fromUnitConversion():
    from_Unit_Bool = False
    while(from_Unit_Bool != True):
        from_Unit = input("What unit do you want to convert from? ")
        from_Unit_Bool = checkUnitDict(from_Unit)
        fromUnitType[0] = from_Unit
        if from_Unit_Bool:
            fromUnitType[1] = assSysDict(from_Unit)
            fromUnitType[2] = assUnitDict(from_Unit)
    return from_Unit # Is this code needed?

def toUnitConversion():
    to_Unit_Bool = False
    while(to_Unit_Bool != True):
        to_Unit = input("What unit do you want to convert to? ")
        to_Unit_Bool = checkUnitDict(to_Unit)
        toUnitType[0] = to_Unit
        if to_Unit_Bool:
            toUnitType[1] = assSysDict(to_Unit)
            toUnitType[2] = assUnitDict(to_Unit)
    return to_Unit # Is this code needed?

# Function below gets the value of the input to be converted.
# Probably needs to have a try/except loop here.
def convValueInput():
    conv_Value_Bool = True
    while(conv_Value_Bool != False):
        conv_Value = float(input("How many of this unit do you want to convert? Input numbers only. "))
        if (conv_Value < 0):
            print("The input value needs to be a number. It cannot have letters.")
            conv_Value_Bool = True
        else:
            # Below is string output to check that the number was received. Not necessary to include.
            # print(f"The float worked. Float is {conv_Value}.")
            conv_Value_Bool = False
    return conv_Value

# The next bit of code will convert the dictionaries into a list that will have adjusted values for easy conversions between systems.
def dictChange(unitTypeConvFactor):
    for i in imperialVolumeConversions:
    newConvList[i] = imperialVolumeConversions * unitTypeConvFactor
    return newConvList

    
# Should trigger the dict change if from different systems.
if(fromUnitType[2] /= toUnitType[2]):


# convF is the conversion function that allows the program to change the units from one conversion to another.
# Needs to have an input about which dictionary to use if not in metricLengthConversions.
def convF(from_Unit, to_Unit, conv_Value):
    # Conversion function works by taking the "from" unit and converting to the "to" unit.
    # Error below after inputting units not in metric length. Only summons metric length.
    # could form string to then summon correct library. 
    convFromValue = unitDictionaries.metricLengthConversions[from_Unit]
    convToValue= unitDictionaries.metricLengthConversions[to_Unit]

    new_value = conv_Value * (convFromValue / convToValue)

    return new_value

# Calls the functions within the convF function, which is printed after it makes a return.
print(convF(fromUnitConversion(), toUnitConversion(), convValueInput()))
unitSysCompat(fromUnitType, toUnitType)
unitTypeCompat(fromUnitType, toUnitType)

def main():
    print(fromUnitType[0])
    print(fromUnitType[1])
    print(fromUnitType[2])
    print(toUnitType[0])
    print(toUnitType[1])
    print(toUnitType[2])

#if __name__ == "__main__": main()


