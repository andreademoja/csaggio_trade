class PercentageCommissionModel:
    def __init__(self, commission_rate=0.001):  # 0.1% for gold CFD
        self.commission_rate = commission_rate

    def calculate_commission(self, size, price):
        return size * price * self.commission_rate