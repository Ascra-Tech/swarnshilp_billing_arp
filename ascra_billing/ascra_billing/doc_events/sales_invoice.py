import frappe

def before_save(self, method):
    pass
    # for item in self.items:
    #     item.rate = self.custom_gold_rate
    #     item.base_rate = self.custom_gold_rate
    #     item.amount = self.custom_gold_rate * item.qty
    #     item.base_amount = self.custom_gold_rate * item.qty

    #     item.net_rate = self.custom_gold_rate
    #     item.net_base_rate = self.custom_gold_rate
    #     item.net_amount = self.custom_gold_rate * item.qty
    #     item.base_net_amount = self.custom_gold_rate * item.qty