from rest_framework import status
from rest_framework.test import APITestCase

from quotes.choices import CoverageTypeChoices
from quotes.factories import (
    BuyerFactory,
    CoverageFactory,
    QuoteFactory,
    RateFactory,
    StateFactory,
)


class BaseAPITest(APITestCase):
    """
    base api test class, usd to set some default values for each test
    """

    def setUp(self):
        self.buyer = BuyerFactory()

        self.COVERAGES__FLOOD = CoverageFactory(
            name="Flood",
        )

        self.COVERAGES__HURRICANE = CoverageFactory(
            name="Hurricane",
        )

        self.STATES__CA = StateFactory(
            code="CA",
            name="California",
            tax_rate=1.0,
        )
        self.STATES__NY = StateFactory(
            code="NY",
            name="New York",
            tax_rate=2.0,
        )
        self.STATES__TX = StateFactory(
            code="TX",
            name="Texas",
            tax_rate=0.5,
        )

        self.RATES__CA_FLOOD = RateFactory(
            state=self.STATES__CA,
            coverage=self.COVERAGES__FLOOD,
            rate_increase_percent=2.0,
        )
        self.RATES__NY_FLOOD = RateFactory(
            state=self.STATES__NY,
            coverage=self.COVERAGES__FLOOD,
            rate_increase_percent=10.0,
        )
        self.RATES__TX_FLOOD = RateFactory(
            state=self.STATES__TX,
            coverage=self.COVERAGES__FLOOD,
            rate_increase_percent=50.0,
        )

    def test_calculatePrice_isSuccessfulForQuote1(self):
        """
        test basic, CA, pet, and flood
        """

        quote = QuoteFactory(
            buyer=self.buyer,
            state=self.STATES__CA,
            coverage_type=CoverageTypeChoices.BASIC,
            include_pet_premium=True,
        )
        quote.coverages.add(self.COVERAGES__FLOOD)

        response = self.client.get(f"/api/quotes/{quote.uuid}/calculate-price/")
        data = response.json()
        price = data.get("price")

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(data["coverageType"], "BASIC")
        self.assertEquals(data["state"], "CA")
        self.assertTrue(data["includePetPremium"])
        self.assertTrue("Flood" in data["coverages"])

        # almost equals for floats/decimals:
        self.assertAlmostEquals(price["monthlySubtotal"], 40.80)
        self.assertAlmostEquals(price["monthlyTaxes"], 0.40)
        self.assertAlmostEquals(price["monthlyTotal"], 41.20)

    def test_calculatePrice_isSuccessfulForQuote2(self):
        """
        test premium, CA, pet, and flood
        """

        quote = QuoteFactory(
            buyer=self.buyer,
            state=self.STATES__CA,
            coverage_type=CoverageTypeChoices.PREMIUM,
            include_pet_premium=True,
        )
        quote.coverages.add(self.COVERAGES__FLOOD)

        response = self.client.get(f"/api/quotes/{quote.uuid}/calculate-price/")
        data = response.json()
        price = data.get("price")

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(data["coverageType"], "PREMIUM")
        self.assertEquals(data["state"], "CA")
        self.assertTrue(data["includePetPremium"])
        self.assertTrue("Flood" in data["coverages"])

        # almost equals for floats/decimals:
        self.assertAlmostEquals(price["monthlySubtotal"], 61.20)
        self.assertAlmostEquals(price["monthlyTaxes"], 0.61)
        self.assertAlmostEquals(price["monthlyTotal"], 61.81)

    def test_calculatePrice_isSuccessfulForQuote3(self):
        """
        test premium, NY, pet
        """

        quote = QuoteFactory(
            buyer=self.buyer,
            state=self.STATES__NY,
            coverage_type=CoverageTypeChoices.PREMIUM,
            include_pet_premium=True,
        )

        response = self.client.get(f"/api/quotes/{quote.uuid}/calculate-price/")
        data = response.json()
        price = data.get("price")

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(data["coverageType"], "PREMIUM")
        self.assertEquals(data["state"], "NY")
        self.assertTrue(data["includePetPremium"])
        self.assertFalse("Flood" in data["coverages"])

        # almost equals for floats/decimals:
        self.assertAlmostEquals(price["monthlySubtotal"], 60.00)
        self.assertAlmostEquals(price["monthlyTaxes"], 1.20)
        self.assertAlmostEquals(price["monthlyTotal"], 61.20)

    def test_calculatePrice_isSuccessfulForQuote4(self):
        """
        test basic, TX, no pet, and flood
        """

        quote = QuoteFactory(
            buyer=self.buyer,
            state=self.STATES__TX,
            coverage_type=CoverageTypeChoices.BASIC,
            include_pet_premium=False,
        )
        quote.coverages.add(self.COVERAGES__FLOOD)

        response = self.client.get(f"/api/quotes/{quote.uuid}/calculate-price/")
        data = response.json()
        price = data.get("price")

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(data["coverageType"], "BASIC")
        self.assertEquals(data["state"], "TX")
        self.assertFalse(data["includePetPremium"])
        self.assertTrue("Flood" in data["coverages"])

        # almost equals for floats/decimals:
        self.assertAlmostEquals(price["monthlySubtotal"], 30.00)
        self.assertAlmostEquals(price["monthlyTaxes"], 0.15)
        self.assertAlmostEquals(price["monthlyTotal"], 30.15)

    def test_calculatePrice_onCoverageWithoutRate_raisesException(self):
        """
        test that trying to calculate the price for a Quote
        for which a Rate has not been set on a specific
        Coverage and State raises an exception
        """

        quote = QuoteFactory(
            buyer=self.buyer,
            state=self.STATES__TX,
            coverage_type=CoverageTypeChoices.BASIC,
            include_pet_premium=False,
        )
        quote.coverages.add(
            self.COVERAGES__FLOOD,
            self.COVERAGES__HURRICANE,
        )

        response = self.client.get(f"/api/quotes/{quote.uuid}/calculate-price/")

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
