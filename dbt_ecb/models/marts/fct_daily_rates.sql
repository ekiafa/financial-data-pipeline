select
    rate_date,
    currency,
    rate,
    eur_per_unit,
    case
        when rate < 1 then 'greater than euro'
        when rate < 10 then 'comparable'
        else 'lower than euro'
    end as strength_vs_eur
from {{ ref('stg_rates') }}