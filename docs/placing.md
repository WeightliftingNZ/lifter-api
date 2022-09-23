# Placing

Determining placing (i.e. 1st, 2nd, 3rd) in weightlifting is handed by a property on the lift model.

According to the IWF rules (pls find source), the athlete who achieves the highest total first in placed ahead.

Essentially it is a sort of different values for athletes in a competition, filtering on category:
1. Highest total
2. Lowest clean and jerk
3. Lowest lottery number.

::: api.models.Lift
    options:
      members:
        - placing

## Future

Looking into segragating Junior, Youth etc.
