from data_extractor import PropertyHTML
from extractors import SummaryExtractor, OwnerExtractor, AppraisalExtractor, DwellingExtractor, OtherBuildingExtractor, \
    CommercialExtractor, MarketLandExtractor


class Property:
    def __init__(self, init_property_data: dict[str, str]) -> None:
        """
        Initializes the Property object with the provided initial property data.

        :param init_property_data:
        """
        self.init_property_data = init_property_data
        self.property_html = PropertyHTML(init_property_data['Geocode'])
        self.data = self._populate_data()

    def _populate_data(self) -> dict:
        """
        Fetch all property data, parse it, and populate the data attribute.

        :return: a dictionary containing all property data
        """
        # fetch all data of property
        self.property_html.fetch_all_data()

        # initialize extractors
        summary_extractor = SummaryExtractor(self.property_html.summary_data)
        owner_extractor = OwnerExtractor(self.property_html.owner_data)
        appraisal_extractor = AppraisalExtractor(self.property_html.appraisal_data)
        dwelling_extractor = DwellingExtractor(self.property_html.dwelling_data)
        other_building_extractor = OtherBuildingExtractor(self.property_html.other_building_data)
        commercial_extractor = CommercialExtractor(self.property_html.commercial_data)
        market_land_extractor = MarketLandExtractor(self.property_html.market_land_data)

        # aggregate data
        return {
            "initial": self.init_property_data,
            "summary": summary_extractor.data,
            "owner": owner_extractor.data,
            "appraisal": appraisal_extractor.data,
            "dwelling": dwelling_extractor.data,
            "other_building": other_building_extractor.data,
            "commercial": commercial_extractor.data,
            "market_land": market_land_extractor.data
        }
