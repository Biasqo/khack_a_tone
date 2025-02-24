CREATE TABLE loan_offers (
    loan_id varchar(255) primary key
    , cust_sid varchar(255)
    , product integer
    , decision varchar(255)
    , reason varchar(255)
    , approved_sum float
);