CREATE TABLE loans (
    loan_id varchar(255) primary key
    , client_id varchar(255)
    , current_overdue float
    , current_loan_payments float
    , product integer
    , product_name varchar(255)
);