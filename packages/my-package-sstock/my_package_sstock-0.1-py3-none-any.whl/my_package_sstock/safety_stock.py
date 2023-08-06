# safety_stock.py

import math

class SafetyStock:
    def __init__(self, z_score, lead_time_demand_std_dev, avg_demand_lead_time):
        self.z_score = z_score
        self.lead_time_demand_std_dev = lead_time_demand_std_dev
        self.avg_demand_lead_time = avg_demand_lead_time

    def calculate_safety_stock(self):
        safety_stock = self.z_score * self.lead_time_demand_std_dev * self.avg_demand_lead_time
        return math.ceil(safety_stock)

# Usage example
if __name__ == "__main__":
    # Example data
    z_score = 1.645  # Service level of 95%
    lead_time_demand_std_dev = 10  # Standard deviation of lead time demand
    avg_demand_lead_time = 100  # Average demand during lead time

    ss_calculator = SafetyStock(z_score, lead_time_demand_std_dev, avg_demand_lead_time)
    safety_stock = ss_calculator.calculate_safety_stock()

    print(f"The required safety stock is {safety_stock} units.")
