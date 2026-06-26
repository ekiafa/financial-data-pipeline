select
    rate_date,
    currency,
    rate,
    round(1 / rate, 4) as eur_per_unit
from raw_rates
where rate is not null