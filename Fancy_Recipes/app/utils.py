from .models import LiquidUnits, SolidUnits

class UnitCalculator:

    #fromUnit object of model LiquidUnits or SolidUnits
    #toUnit object of model LiquidUnits or SolidUnits

    #example call:
    # a = SolidUnits.objects.get(unit = "kg")
    # b = SolidUnits.objects.get(unit = "dag")
    # c = 1.2
    # UnitCalculator.convert(a,b,c)
    @staticmethod
    def convert(fromUnit ,toUnit , amount):
        if type(fromUnit) != type(toUnit):
            raise TypeError("Cannot convert between other unit types")
        factor = fromUnit.conversionFactorToMainUnit / toUnit.conversionFactorToMainUnit
        return amount * factor

    #do odkomentowania gdy pojawią sie jednostki w bazie
    @staticmethod
    def convertHelper(fromUnitName, toUnitName, amount):
        # fromUnit = LiquidUnits.objects.get(unit=fromUnitName)
        # toUnit = LiquidUnits.objects.get(unit=toUnitName)
        # if fromUnit is None:
        #     fromUnit = SolidUnits.objects.get(unit=fromUnitName)
        #     toUnit = SolidUnits.objects.get(unit=toUnitName)
        # if fromUnit is None:
        #     return None
        #
        # result = UnitCalculator.convert(fromUnit, toUnit, amount)
        # return result
        return 130.33
