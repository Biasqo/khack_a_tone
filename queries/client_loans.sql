select loans.loan_id
    , loans.current_overdue
    , loans.current_loan_payments
from loans
where loans.client_id = "{}"