class HotelRoomCalc(object):
    'hotel room rate calculator'
    def __init__(self,rt,sales=0.085,rm=0.1):
        self.salesTax = sales
        self.roomTax = rm
        self.roomRate = rt
        
    def calcTotal(self,days = 1):
        daily = round((self.roomRate *(1+self.roomTax + self.salesTax)),2)
        return float(days)*daily
