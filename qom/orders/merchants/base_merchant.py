class BaseMerchant:

    def start_payment(self):
        raise NotImplementedError

    def verify_payment(self,authority):
        raise NotImplementedError