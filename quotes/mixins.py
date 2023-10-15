from django.core.exceptions import ValidationError

from decimal import (
    Decimal,
    ROUND_DOWN,
)


def truncate_float(n):
    return int(n * (10**2)) / 10**2


class QuoteMixin:
    """
    mixin to add custom methods to quote model
    """

    def calculate_price(self):
        """
        helper method to calculate the quote price
        price is calculated on a monthly basis
        """

        coverage_type_price_map = {
            "BASIC": 20.0,
            "PREMIUM": 40.0,
        }

        # coverage type initial coverage:
        monthly_subtotal = coverage_type_price_map[self.coverage_type]

        # pet premium:
        if self.include_pet_premium:
            monthly_subtotal += 20.0

        total_coverage_rate_increase_percentage = 1.0

        # modifiers:
        for coverage in self.coverages.all():
            # get the rate based on the coverage and state
            rate = coverage.rates.filter(state=self.state).first()

            # if there is no rate for a given coverage and sate, raise exception:
            if not rate:
                raise ValidationError(
                    f"A rate for {coverage.name} coverage in {self.state.name} does not exist. "
                    f"Either add a rate for this state, or remove the coverage from the quote."
                )

            # update the total rate percentage increase:
            total_coverage_rate_increase_percentage += (
                float(rate.rate_increase_percent) / 100.0
            )

        # update pretax price with additional coerage costs:
        monthly_subtotal *= total_coverage_rate_increase_percentage

        # monthly taxes as amount (dollars):
        monthly_taxes = monthly_subtotal * float(self.state.tax_rate) / 100.0

        # total monthly cost:
        monthly_total = monthly_subtotal + monthly_taxes

        # to properly truncate the values
        # first force trailing zero, then convert to decimal and round
        monthly_subtotal = "%.4f" % monthly_subtotal
        monthly_taxes = "%.4f" % monthly_taxes
        monthly_total = "%.4f" % monthly_total

        TWOPLACES = Decimal(10) ** -2

        monthly_subtotal = Decimal(monthly_subtotal).quantize(
            TWOPLACES,
            rounding=ROUND_DOWN,
        )

        monthly_taxes = Decimal(monthly_taxes).quantize(
            TWOPLACES,
            rounding=ROUND_DOWN,
        )

        monthly_total = Decimal(monthly_total).quantize(
            TWOPLACES,
            rounding=ROUND_DOWN,
        )

        return {
            "monthly_subtotal": monthly_subtotal,
            "monthly_taxes": monthly_taxes,
            "monthly_total": monthly_total,
        }
