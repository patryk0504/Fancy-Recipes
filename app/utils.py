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
        result = None
        fromLiquid = LiquidUnits.objects.filter(unit=fromUnitName)
        toLiquid = LiquidUnits.objects.filter(unit=toUnitName)
        fromSolid = SolidUnits.objects.filter(unit=fromUnitName)
        toSolid = SolidUnits.objects.filter(unit=toUnitName)
        if fromLiquid.exists() and toLiquid.exists():
            result = UnitCalculator.convert(fromLiquid.first(), toLiquid.first(), float(amount))
        elif fromSolid.exists() and toSolid.exists():
            result = UnitCalculator.convert(fromSolid.first(), toSolid.first(), float(amount))
        return result