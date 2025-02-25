select loan_offers.product
    , loan_offers.decision
    , loan_offers.reason
    , loan_offers.approved_sum
    , loan_offers.product_name
    , recommendations.recommendation
from loan_offers
inner join recommendations
    on recommendations.reason = loan_offers.reason
where loan_offers.cust_sid = "{}"