select clients.cust_sid
    , clients.name
    , clients.cust_group
    , clients.age
    , client_segments.group_info
from clients
inner join client_segments
    on clients.cust_group = client_segments.cust_group
where clients.cust_sid = "{}"