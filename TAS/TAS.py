from typing import Text

class CogCompTAS():
    alpha2ToAlpha3 = {"AW": "ABW", "AF": "AFG", "AO": "AGO", "AI": "AIA", "AX": "ALA", "AL": "ALB", "AD": "AND", "AE": "ARE", "AR": "ARG", "AM": "ARM", "AS": "ASM", "AQ": "ATA", "TF": "ATF", "AG": "ATG", "AU": "AUS", "AT": "AUT", "AZ": "AZE", "BI": "BDI", "BE": "BEL", "BJ": "BEN", "BQ": "BES", "BF": "BFA", "BD": "BGD", "BG": "BGR", "BH": "BHR", "BS": "BHS", "BA": "BIH", "BL": "BLM", "BY": "BLR", "BZ": "BLZ", "BM": "BMU", "BO": "BOL", "BR": "BRA", "BB": "BRB", "BN": "BRN", "BT": "BTN", "BV": "BVT", "BW": "BWA", "CF": "CAF", "CA": "CAN", "CC": "CCK", "CH": "CHE", "CL": "CHL", "CN": "CHN", "CI": "CIV", "CM": "CMR", "CD": "COD", "CG": "COG", "CK": "COK", "CO": "COL", "KM": "COM", "CV": "CPV", "CR": "CRI", "CU": "CUB", "CW": "CUW", "CX": "CXR", "KY": "CYM", "CY": "CYP", "CZ": "CZE", "DE": "DEU", "DJ": "DJI", "DM": "DMA", "DK": "DNK", "DO": "DOM", "DZ": "DZA", "EC": "ECU", "EG": "EGY", "ER": "ERI", "EH": "ESH", "ES": "ESP", "EE": "EST", "ET": "ETH", "FI": "FIN", "FJ": "FJI", "FK": "FLK", "FR": "FRA", "FO": "FRO", "FM": "FSM", "GA": "GAB", "GB": "GBR", "GE": "GEO", "GG": "GGY", "GH": "GHA", "GI": "GIB", "GN": "GIN", "GP": "GLP", "GM": "GMB", "GW": "GNB", "GQ": "GNQ", "GR": "GRC", "GD": "GRD", "GL": "GRL", "GT": "GTM", "GF": "GUF", "GU": "GUM", "GY": "GUY", "HK": "HKG", "HM": "HMD", "HN": "HND", "HR": "HRV", "HT": "HTI", "HU": "HUN", "ID": "IDN", "IM": "IMN", "IN": "IND", "IO": "IOT", "IE": "IRL", "IR": "IRN", "IQ": "IRQ", "IS": "ISL", "IL": "ISR", "IT": "ITA", "JM": "JAM", "JE": "JEY", "JO": "JOR", "JP": "JPN", "KZ": "KAZ", "KE": "KEN", "KG": "KGZ", "KH": "KHM", "KI": "KIR", "KN": "KNA", "KR": "KOR", "KW": "KWT", "LA": "LAO", "LB": "LBN", "LR": "LBR", "LY": "LBY", "LC": "LCA", "LI": "LIE", "LK": "LKA", "LS": "LSO", "LT": "LTU", "LU": "LUX", "LV": "LVA", "MO": "MAC", "MF": "MAF", "MA": "MAR", "MC": "MCO", "MD": "MDA", "MG": "MDG", "MV": "MDV", "MX": "MEX", "MH": "MHL", "MK": "MKD", "ML": "MLI", "MT": "MLT", "MM": "MMR", "ME": "MNE", "MN": "MNG", "MP": "MNP", "MZ": "MOZ", "MR": "MRT", "MS": "MSR", "MQ": "MTQ", "MU": "MUS", "MW": "MWI", "MY": "MYS", "YT": "MYT", "NA": "NAM", "NC": "NCL", "NE": "NER", "NF": "NFK", "NG": "NGA", "NI": "NIC", "NU": "NIU", "NL": "NLD", "NO": "NOR", "NP": "NPL", "NR": "NRU", "NZ": "NZL", "OM": "OMN", "PK": "PAK", "PA": "PAN", "PN": "PCN", "PE": "PER", "PH": "PHL", "PW": "PLW", "PG": "PNG", "PL": "POL", "PR": "PRI", "KP": "PRK", "PT": "PRT", "PY": "PRY", "PS": "PSE", "PF": "PYF", "QA": "QAT", "RE": "REU", "RO": "ROU", "RU": "RUS", "RW": "RWA", "SA": "SAU", "SD": "SDN", "SN": "SEN", "SG": "SGP", "GS": "SGS", "SH": "SHN", "SJ": "SJM", "SB": "SLB", "SL": "SLE", "SV": "SLV", "SM": "SMR", "SO": "SOM", "PM": "SPM", "RS": "SRB", "SS": "SSD", "ST": "STP", "SR": "SUR", "SK": "SVK", "SI": "SVN", "SE": "SWE", "SZ": "SWZ", "SX": "SXM", "SC": "SYC", "SY": "SYR", "TC": "TCA", "TD": "TCD", "TG": "TGO", "TH": "THA", "TJ": "TJK", "TK": "TKL", "TM": "TKM", "TL": "TLS", "TO": "TON", "TT": "TTO", "TN": "TUN", "TR": "TUR", "TV": "TUV", "TW": "TWN", "TZ": "TZA", "UG": "UGA", "UA": "UKR", "UM": "UMI", "UY": "URY", "US": "USA", "UZ": "UZB", "VA": "VAT", "VC": "VCT", "VE": "VEN", "VG": "VGB", "VI": "VIR", "VN": "VNM", "VU": "VUT", "WF": "WLF", "WS": "WSM", "YE": "YEM", "ZA": "ZAF", "ZM": "ZMB", "ZW": "ZWE"}
    alpha3ToAlpha2 = {"ABW": "AW", "AFG": "AF", "AGO": "AO", "AIA": "AI", "ALA": "AX", "ALB": "AL", "AND": "AD", "ARE": "AE", "ARG": "AR", "ARM": "AM", "ASM": "AS", "ATA": "AQ", "ATF": "TF", "ATG": "AG", "AUS": "AU", "AUT": "AT", "AZE": "AZ", "BDI": "BI", "BEL": "BE", "BEN": "BJ", "BES": "BQ", "BFA": "BF", "BGD": "BD", "BGR": "BG", "BHR": "BH", "BHS": "BS", "BIH": "BA", "BLM": "BL", "BLR": "BY", "BLZ": "BZ", "BMU": "BM", "BOL": "BO", "BRA": "BR", "BRB": "BB", "BRN": "BN", "BTN": "BT", "BVT": "BV", "BWA": "BW", "CAF": "CF", "CAN": "CA", "CCK": "CC", "CHE": "CH", "CHL": "CL", "CHN": "CN", "CIV": "CI", "CMR": "CM", "COD": "CD", "COG": "CG", "COK": "CK", "COL": "CO", "COM": "KM", "CPV": "CV", "CRI": "CR", "CUB": "CU", "CUW": "CW", "CXR": "CX", "CYM": "KY", "CYP": "CY", "CZE": "CZ", "DEU": "DE", "DJI": "DJ", "DMA": "DM", "DNK": "DK", "DOM": "DO", "DZA": "DZ", "ECU": "EC", "EGY": "EG", "ERI": "ER", "ESH": "EH", "ESP": "ES", "EST": "EE", "ETH": "ET", "FIN": "FI", "FJI": "FJ", "FLK": "FK", "FRA": "FR", "FRO": "FO", "FSM": "FM", "GAB": "GA", "GBR": "GB", "GEO": "GE", "GGY": "GG", "GHA": "GH", "GIB": "GI", "GIN": "GN", "GLP": "GP", "GMB": "GM", "GNB": "GW", "GNQ": "GQ", "GRC": "GR", "GRD": "GD", "GRL": "GL", "GTM": "GT", "GUF": "GF", "GUM": "GU", "GUY": "GY", "HKG": "HK", "HMD": "HM", "HND": "HN", "HRV": "HR", "HTI": "HT", "HUN": "HU", "IDN": "ID", "IMN": "IM", "IND": "IN", "IOT": "IO", "IRL": "IE", "IRN": "IR", "IRQ": "IQ", "ISL": "IS", "ISR": "IL", "ITA": "IT", "JAM": "JM", "JEY": "JE", "JOR": "JO", "JPN": "JP", "KAZ": "KZ", "KEN": "KE", "KGZ": "KG", "KHM": "KH", "KIR": "KI", "KNA": "KN", "KOR": "KR", "KWT": "KW", "LAO": "LA", "LBN": "LB", "LBR": "LR", "LBY": "LY", "LCA": "LC", "LIE": "LI", "LKA": "LK", "LSO": "LS", "LTU": "LT", "LUX": "LU", "LVA": "LV", "MAC": "MO", "MAF": "MF", "MAR": "MA", "MCO": "MC", "MDA": "MD", "MDG": "MG", "MDV": "MV", "MEX": "MX", "MHL": "MH", "MKD": "MK", "MLI": "ML", "MLT": "MT", "MMR": "MM", "MNE": "ME", "MNG": "MN", "MNP": "MP", "MOZ": "MZ", "MRT": "MR", "MSR": "MS", "MTQ": "MQ", "MUS": "MU", "MWI": "MW", "MYS": "MY", "MYT": "YT", "NAM": "NA", "NCL": "NC", "NER": "NE", "NFK": "NF", "NGA": "NG", "NIC": "NI", "NIU": "NU", "NLD": "NL", "NOR": "NO", "NPL": "NP", "NRU": "NR", "NZL": "NZ", "OMN": "OM", "PAK": "PK", "PAN": "PA", "PCN": "PN", "PER": "PE", "PHL": "PH", "PLW": "PW", "PNG": "PG", "POL": "PL", "PRI": "PR", "PRK": "KP", "PRT": "PT", "PRY": "PY", "PSE": "PS", "PYF": "PF", "QAT": "QA", "REU": "RE", "ROU": "RO", "RUS": "RU", "RWA": "RW", "SAU": "SA", "SDN": "SD", "SEN": "SN", "SGP": "SG", "SGS": "GS", "SHN": "SH", "SJM": "SJ", "SLB": "SB", "SLE": "SL", "SLV": "SV", "SMR": "SM", "SOM": "SO", "SPM": "PM", "SRB": "RS", "SSD": "SS", "STP": "ST", "SUR": "SR", "SVK": "SK", "SVN": "SI", "SWE": "SE", "SWZ": "SZ", "SXM": "SX", "SYC": "SC", "SYR": "SY", "TCA": "TC", "TCD": "TD", "TGO": "TG", "THA": "TH", "TJK": "TJ", "TKL": "TK", "TKM": "TM", "TLS": "TL", "TON": "TO", "TTO": "TT", "TUN": "TN", "TUR": "TR", "TUV": "TV", "TWN": "TW", "TZA": "TZ", "UGA": "UG", "UKR": "UA", "UMI": "UM", "URY": "UY", "USA": "US", "UZB": "UZ", "VAT": "VA", "VCT": "VC", "VEN": "VE", "VGB": "VG", "VIR": "VI", "VNM": "VN", "VUT": "VU", "WLF": "WF", "WSM": "WS", "YEM": "YE", "ZAF": "ZA", "ZMB": "ZM", "ZWE": "ZW"}

    # Initialization
    def __init__(self, text="", lang="eng"):
        '''
        Create a TA schema for a document for a given language and with a textual content
        Language must be validated against a list of Alpha-2 / Alpha-3 codes
        Only Alpha-3 code will be stored
        Text cannot be None, but it can eventually be empty ("")
        '''
        self.text = text
        self.lang = self.langReader(lang)

    def getText(self):
        return self.text

    
    def langReader(self, lang):
        if lang.upper() in self.alpha2ToAlpha3:
            return self.alpha2ToAlpha3[lang]
        
        elif lang.upper() in self.alpha3ToAlpha2:
            return lang

        else:
             return "USA"

    # Language
    def getLang(self):
        return self.lang

    def getLangAlpha3(self):
        return self.lang

    def getLangAlpha2(self):
        return self.alpha3ToAlpha2[self.lang]

    def getDCTS(self):
        pass

    def setDCTS(self):
        pass

if __name__ == "__main__":
    TAS = CogCompTAS()
    TAS.langReader('US')