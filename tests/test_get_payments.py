
from payments import get_payments

payments = get_payments()

print("Payment Records:")

for payment in payments:
    print(payment)
