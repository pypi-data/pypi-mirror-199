from datetime import datetime
from typing import Any, Dict, List, Mapping, Optional, Union
import warnings

import pandas as pd

from nordea_analytics.nalib.data_retrieval_client import (
    DataRetrievalServiceClient,
)
from nordea_analytics.nalib.util import (
    check_json_response,
    check_json_response_error,
    convert_to_variable_string,
    get_config,
)
from nordea_analytics.nalib.value_retriever import ValueRetriever
from nordea_analytics.search_bond_names import (
    AmortisationType,
    AssetType,
    CapitalCentres,
    CapitalCentreTypes,
    InstrumentGroup,
    Issuers,
)

config = get_config()


class BondFinder(ValueRetriever):
    """Retrieves and reformat bonds given a search criteria."""

    def __init__(
        self,
        client: DataRetrievalServiceClient,
        dmb: bool = False,
        country: Optional[str] = None,
        currency: Optional[str] = None,
        issuers: Optional[
            Union[Issuers, str, List[Issuers], List[str], List[Union[Issuers, str]]]
        ] = None,
        asset_types: Optional[
            Union[
                AssetType, str, List[AssetType], List[str], List[Union[str, AssetType]]
            ]
        ] = None,
        instrument_groups: Optional[
            Union[
                InstrumentGroup,
                str,
                List[InstrumentGroup],
                List[str],
                List[Union[str, InstrumentGroup]],
            ]
        ] = None,
        lower_issue_date: Optional[datetime] = None,
        upper_issue_date: Optional[datetime] = None,
        lower_maturity: Optional[datetime] = None,
        upper_maturity: Optional[datetime] = None,
        lower_closing_date: Optional[datetime] = None,
        upper_closing_date: Optional[datetime] = None,
        lower_coupon: Optional[float] = None,
        upper_coupon: Optional[float] = None,
        amortisation_type: Optional[Union[AmortisationType, str]] = None,
        capital_centres: Optional[
            Union[
                CapitalCentres,
                str,
                List[CapitalCentres],
                List[str],
                List[Union[CapitalCentres, str]],
            ]
        ] = None,
        capital_centre_types: Optional[
            Union[
                CapitalCentreTypes,
                str,
                List[CapitalCentreTypes],
                List[str],
                List[Union[CapitalCentreTypes, str]],
            ]
        ] = None,
        lower_outstanding_amount: Optional[float] = None,
        upper_outstanding_amount: Optional[float] = None,
    ) -> None:
        """Initialization of class.

        Args:
            client: DataRetrievalServiceClient
                or DataRetrievalServiceClientTest for testing.
            dmb: Default to False. True if only Danish Mortgage
                Bonds should be found.
            country: Country of issue.
            currency: Issue currency.
            issuers: Name of issuers.
            asset_types: Type of asset.
            instrument_groups: Type of instrument.
            lower_issue_date: Minimum (from) issue date.
            upper_issue_date: Maximum (to) issue date.
            lower_maturity: Minimum (from) maturity.
            upper_maturity: Maximum (to) maturity.
            lower_closing_date: Minimum(from) closing date - only applicable for DMB.
            upper_closing_date: Maximum(to) closing date - only applicable for DMB.
            lower_coupon: Minimum coupon.
            upper_coupon: Maximum coupon.
            amortisation_type: Amortisation type of bond.
            capital_centres: Capital centres names - only applicable for DMB.
            capital_centre_types: Capital centres types - only applicable for DMB.
            lower_outstanding_amount: Minimum outstanding amount - only applicable for DMB.
            upper_outstanding_amount: Maximum outstanding amount - only applicable for DMB.

        """
        super(BondFinder, self).__init__(client)
        self._client = client
        self.dmb = dmb
        self.country = country
        self.currency = currency
        self.issuers = issuers
        _asset_types: List = (
            asset_types if isinstance(asset_types, list) else [asset_types]
        )
        self.asset_types = (
            [
                convert_to_variable_string(asset_type, AssetType)
                if isinstance(asset_type, AssetType)
                else asset_type
                for asset_type in _asset_types
            ]
            if asset_types is not None
            else None
        )
        _instrument_groups: List = (
            instrument_groups
            if isinstance(instrument_groups, list)
            else [instrument_groups]
        )
        self.instrument_groups = (
            [
                convert_to_variable_string(instrument_group, InstrumentGroup)
                if isinstance(instrument_group, InstrumentGroup)
                else instrument_group
                for instrument_group in _instrument_groups
            ]
            if instrument_groups is not None
            else None
        )

        self.lower_issue_date = (
            lower_issue_date.strftime("%Y-%m-%d")
            if lower_issue_date is not None
            else None
        )
        self.upper_issue_date = (
            upper_issue_date.strftime("%Y-%m-%d")
            if upper_issue_date is not None
            else None
        )
        self.lower_maturity = (
            lower_maturity.strftime("%Y-%m-%d") if lower_maturity is not None else None
        )
        self.upper_maturity = (
            upper_maturity.strftime("%Y-%m-%d") if upper_maturity is not None else None
        )
        self.lower_closing_date = (
            lower_closing_date.strftime("%Y-%m-%d")
            if lower_closing_date is not None
            else None
        )
        self.upper_closing_date = (
            upper_closing_date.strftime("%Y-%m-%d")
            if upper_closing_date is not None
            else None
        )
        self.lower_coupon = str(lower_coupon) if lower_coupon is not None else None
        self.upper_coupon = str(upper_coupon) if upper_coupon is not None else None
        self.amortisation_type = (
            convert_to_variable_string(amortisation_type, AmortisationType)
            if isinstance(amortisation_type, AmortisationType)
            else amortisation_type
        )

        self.capital_centres: Union[list[str], None]
        if capital_centres is not None:
            _capital_centres = (
                capital_centres
                if isinstance(capital_centres, list)
                else [capital_centres]
            )

            self.capital_centres = [
                convert_to_variable_string(capital_centre, CapitalCentres)
                if isinstance(capital_centre, CapitalCentres)
                else capital_centre
                for capital_centre in _capital_centres
            ]
        else:
            self.capital_centres = None

        self.capital_centre_types: Union[list[str], None]
        if capital_centre_types is not None:
            _capital_centre_types = (
                capital_centre_types
                if isinstance(capital_centre_types, list)
                else [capital_centre_types]
            )

            self.capital_centre_types = [
                convert_to_variable_string(capital_centre_type, CapitalCentreTypes)
                if isinstance(capital_centre_type, CapitalCentreTypes)
                else capital_centre_type
                for capital_centre_type in _capital_centre_types
            ]
        else:
            self.capital_centre_types = None

        self.lower_outstanding_amount = lower_outstanding_amount
        self.upper_outstanding_amount = upper_outstanding_amount

        self.check_inputs()

        self._data = self.get_search_bonds()

    def get_search_bonds(self) -> Mapping:
        """Retrieves response given the search criteria."""
        _json_response = self.get_response(self.request)
        json_response = _json_response[config["results"]["search"]]

        return json_response

    @staticmethod
    def check_response(json_response: Mapping) -> None:
        """Checks if json_reponse contains output, else throws error."""
        output_found = check_json_response(json_response)

        check_json_response_error(output_found)

    @property
    def url_suffix(self) -> str:
        """Url suffix suffix for a given method."""
        if self.dmb:
            return config["url_suffix"]["search_dmb_bonds"]
        else:
            return config["url_suffix"]["search_bonds"]

    @property
    def request(self) -> Dict:
        """Request dictionary for searched bonds."""
        initial_request = {
            "country": self.country,
            "currency": self.currency,
            "issuers": self.issuers,
            "asset-types": self.asset_types,
            "instrument-groups": self.instrument_groups,
            "lower-issue-date": self.lower_issue_date,
            "upper-issue-date": self.upper_issue_date,
            "lower-maturity": self.lower_maturity,
            "upper-maturity": self.upper_maturity,
            "lower-closing-date": self.lower_closing_date,
            "upper-closing-date": self.upper_closing_date,
            "lower-coupon": self.lower_coupon,
            "upper-coupon": self.upper_coupon,
            "amortisation-type": self.amortisation_type,
            "capital-centres": self.capital_centres,
            "capital-centre-types": self.capital_centre_types,
            "lower-outstanding-amount": self.lower_outstanding_amount,
            "upper-outstanding-amount": self.upper_outstanding_amount,
        }

        request = {
            key: initial_request[key]
            for key in initial_request.keys()
            if initial_request[key] is not None
        }
        if request == {}:
            raise ValueError("You need to input some search criteria")
        return request

    def check_inputs(self) -> None:
        """Check if inputs are given that only apply to dmb."""
        if self.capital_centres is not None:
            if not self.dmb:
                warnings.warn(
                    "capital_centres is only relevant for DMB. "
                    "This variable will be ignored.",
                    stacklevel=2,
                )
        if self.capital_centre_types is not None:
            if not self.dmb:
                warnings.warn(
                    "capital_centre_types is only relevant for DMB."
                    " This variable will be ignored.",
                    stacklevel=2,
                )
        if self.lower_outstanding_amount is not None:
            if not self.dmb:
                warnings.warn(
                    "lower_outstanding_amount is only relevant for DMB. "
                    "This variable will be ignored.",
                    stacklevel=2,
                )
        if self.upper_outstanding_amount is not None:
            if not self.dmb:
                warnings.warn(
                    "upper_outstanding_amount is only relevant for DMB. "
                    "This variable will be ignored.",
                    stacklevel=2,
                )

    def to_dict(self) -> Dict:
        """Reformat the json response to a dictionary."""
        _dict: Dict[Any, Any] = {}
        for i, search_data in enumerate(self._data):
            _dict[i] = {}
            _dict[i]["ISIN"] = search_data["isin"]
            _dict[i]["Name"] = search_data["name"]
        return _dict

    def to_df(self) -> pd.DataFrame:
        """Reformat the json response to a pandas DataFrame."""
        _dict = self.to_dict()
        df = pd.DataFrame.from_dict(_dict).transpose()
        return df
