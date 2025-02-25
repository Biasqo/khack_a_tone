select loans.loan_id
    , loans.current_overdue
    , loans.current_loan_payments
    , loans.product_name
from loans
where loans.client_id = "{}"