
class BaseMerchant:
    def __init__(self,amount,*args,**kwargs):
        self.amount = amount


    def start_payment(self):
        raise NotImplementedError

    def verify_payment(self,authority):
        raise NotImplementedError