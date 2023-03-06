import simpful as sf
from simpful import FuzzySet, Triangular_MF, LinguisticVariable


class MyFuzzy:
    def __init__(self):
        self.FS = sf.FuzzySystem("Sneaker Recommendation")

    def setSystem(self):
        # Define the fuzzy system
        FS = self.FS

        # Define brand level
        b1 = FuzzySet(function=Triangular_MF(0, 0, 0.5), term="low_brand")
        b2 = FuzzySet(function=Triangular_MF(0.5, 1, 1), term="high_brand")
        LVb = LinguisticVariable([b1, b2], concept="brand level", universe_of_discourse=[0, 1])
        FS.add_linguistic_variable("brand_level", LVb)

        # Define fit level
        f1 = FuzzySet(function=Triangular_MF(0, 0, 0.3), term="below_average")
        f2 = FuzzySet(function=Triangular_MF(0.2, 0.5, 0.8), term="average")
        f3 = FuzzySet(function=Triangular_MF(0.7, 1, 1), term="above average")
        LVf = LinguisticVariable([f1, f2, f3], concept="fit level", universe_of_discourse=[0, 1])
        FS.add_linguistic_variable("fit_level", LVf)

        # Define price level
        p1 = FuzzySet(function=Triangular_MF(0, 0, 0.5), term="low_price")
        p2 = FuzzySet(function=Triangular_MF(0.5, 1, 1), term="high_price")
        LVp = LinguisticVariable([p1, p2], concept="price level", universe_of_discourse=[0, 1])
        FS.add_linguistic_variable("price_level", LVp)

        # Define style level
        s1 = FuzzySet(function=Triangular_MF(0, 0, 0.5), term="low_style")
        s2 = FuzzySet(function=Triangular_MF(0.5, 1, 1), term="high_style")
        LVs = LinguisticVariable([s1, s2], concept="style level", universe_of_discourse=[0, 1])
        FS.add_linguistic_variable("style_level", LVs)

        # Define output resale level
        r1 = FuzzySet(function=Triangular_MF(0, 0, 0.5), term="low_resale")
        r2 = FuzzySet(function=Triangular_MF(0.5, 1, 1), term="high_resale")
        LVr = LinguisticVariable([r1, r2], concept="resale value", universe_of_discourse=[0, 1])
        FS.add_linguistic_variable("resale_value", LVr)

        # Define output hype level
        h1 = FuzzySet(function=Triangular_MF(0, 0, 0.5), term="low_hype")
        h2 = FuzzySet(function=Triangular_MF(0.5, 1, 1), term="high_hype")
        LVh = LinguisticVariable([h1, h2], concept="hype level", universe_of_discourse=[0, 1])
        FS.add_linguistic_variable("hype_level", LVh)

        # Define the rules
        FS.add_rules([
            "IF (brand_level IS high_brand) AND (fit_level IS average) AND (price_level IS low_price) THEN (resale_value IS low_resale)",
            "IF (brand_level IS high_brand) AND (fit_level IS average) AND (price_level IS high_price) THEN (resale_value IS high_resale)",
            "IF (brand_level IS low_brand) AND (style_level IS high_style) THEN (hype_level IS high_hype)",
        ])

    def getFuzz(self, brand_level, fit_level, price_level, style_level, query):
        # Define the fuzzy system
        FS = self.FS
        # Add the fuzzy sets to the corresponding variables
        FS.set_variable("brand_level", brand_level)
        FS.set_variable("fit_level", fit_level)
        FS.set_variable("price_level", price_level)
        FS.set_variable("style_level", style_level)
        return FS.Mamdani_inference([query])
