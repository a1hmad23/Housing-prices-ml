"""
Central configuration for data prep and feature engineering.

Everything here is hand-maintained (decisions made in EDA) so that
pipelines and notebooks reference a single source of truth.
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List, Dict, TypedDict
from datetime import datetime

# -----------------------
# Versioning / metadata
# -----------------------

CONFIG_VERSION = "0.1.0"
CONFIG_UPDATED_AT = datetime.utcnow().isoformat(timespec="seconds") + "Z"

# -----------------------
# Imputation
# -----------------------

@dataclass(frozen=True)
class ImputePlan:
    structural_none: List[str]  # absence is informative → fill with string "None"
    mode_fill: List[str]        # nominal/ordinal → most_frequent
    zero_fill: List[str]        # zero-inflated numerics → 0
    median_fill: List[str]      # continuous numerics → median
    year_cols: List[str]        # year-like numerics (may also get median)


# NOTE: These lists come from EDA section.
IMPUTE_PLAN = ImputePlan(
    structural_none=[
        "MasVnrType","GarageType","BsmtFinType1","BsmtFinType2",
        "BsmtQual","BsmtCond","BsmtExposure","FireplaceQu",
        "GarageQual","GarageCond","GarageFinish","Fence"
    ],
    mode_fill=[
        # nominal
        "MSSubClass","MSZoning","Neighborhood","Exterior1st",
        "RoofStyle","RoofMatl","Heating","Foundation","LotConfig",
        "Electrical", "MoSold", "BldgType", "SaleType",
        "Condition1", "Condition2", "SaleCondition", "HouseStyle",
        # ordinal
        "ExterQual","ExterCond","HeatingQC","KitchenQual", "CentralAir",
        "Functional","LandContour","LotShape","LandSlope","PavedDrive"
    ],
    zero_fill=[
        "2ndFlrSF","OpenPorchSF","WoodDeckSF","MasVnrArea","LowQualFinSF",
        "MiscVal","3SsnPorch","PoolArea","BsmtFullBath","HalfBath",
        "BsmtHalfBath","BsmtFinSF2","EnclosedPorch","ScreenPorch"
    ],
    median_fill=[
        "LotArea","GrLivArea","BsmtUnfSF","1stFlrSF","TotalBsmtSF","LotFrontage"
    ],
    year_cols=["YearBuilt","YearRemodAdd","GarageYrBlt","YrSold"],
)



# -----------------------
# EDA classification lists (updated)
# -----------------------

NOMINAL_COLS: List[str] = [
    "MSSubClass", "MoSold", "BldgType", "MasVnrType", "GarageType", "SaleType", "Condition1",
    "Condition2", "SaleCondition", "Neighborhood", "Exterior1st", "HouseStyle", "RoofMatl",
    "BsmtFinType2", "RoofStyle", "BsmtFinType1", "Heating", "Foundation", "LotConfig", "MSZoning",
    "Electrical"
]

COLLAPSE_TO_BINARY_COLS: List[str] = [
    "LowQualFinSF", "MiscVal", "3SsnPorch", "PoolArea", "BsmtFullBath", "HalfBath",
    "BsmtHalfBath", "BsmtFinSF2", "EnclosedPorch", "ScreenPorch"
]

RIGHT_SKEWED_COLS: List[str] = [
    "LotArea", "GrLivArea", "BsmtUnfSF", "1stFlrSF", "TotalBsmtSF", "LotFrontage"
]

SKEWED_AND_BINARY_COLS: List[str] = [
    "2ndFlrSF", "OpenPorchSF", "WoodDeckSF", "MasVnrArea"
]

DROP_COLS: List[str] = [
    "PoolQC", "MiscFeature", "Utilities", "Id", "GarageArea",
    "TotRmsAbvGrd", "Alley", "Exterior2nd", "Street"
]

# Object columns that are truly ordinal 
ORDINAL_OBJECTS: List[str] = [
    "ExterQual", "ExterCond", "BsmtQual", "BsmtCond", "HeatingQC", "KitchenQual", "FireplaceQu",
    "GarageQual", "GarageCond", "Functional", "LandContour", "LotShape", "BsmtExposure",
    "LandSlope", "GarageFinish", "PavedDrive", "Fence", "CentralAir"
]


YEAR_COLS: List[str] = ["YearBuilt", "YearRemodAdd", "GarageYrBlt", "YrSold"]


# -----------------------
# Ordinal mappings
# -----------------------

qual_map: Dict[str, int] = {
    "Ex": 5,
    "Gd": 4,
    "TA": 3,
    "Fa": 2,
    "Po": 1,
    "None": 0   # e.g. BsmtQual, GarageQual, FireplaceQu
}

functional_map: Dict[str, int] = {
    "Typ": 0,
    "Mod": 1,
    "Min1": 2,
    "Min2": 3,
    "Maj1": 4,
    "Maj2": 5,
    "Sev": 6,
    "None": -1  # structural missing is unusual here, but safe fallback
}

LandContour_map: Dict[str, int] = {
    "Low": 0,
    "HLS": 1,
    "Bnk": 2,
    "Lvl": 3
    # No "None" — this column doesn’t get structural None imputation
}

LotShape_map: Dict[str, int] = {
    "IR3": 0,
    "IR2": 1,
    "IR1": 2,
    "Reg": 3
    # No "None"
}

bsmtExposure_map: Dict[str, int] = {
    "No": 0,
    "Mn": 1,
    "Av": 2,
    "Gd": 3,
    "None": -1  # structural absence of basement
}

landSlope_map: Dict[str, int] = {
    "Gtl": 0,
    "Mod": 1,
    "Sev": 2
    # No "None"
}

GarageFinish_map: Dict[str, int] = {
    "Unf": 0,
    "RFn": 1,
    "Fin": 2,
    "None": -1   # no garage
}

PavedDrive_map: Dict[str, int] = {
    "N": 0,
    "P": 1,
    "Y": 2
    # No "None"
}

CentralAir_map: Dict[str, int] = {
    "Y": 1,
    "N": 0
    # No "None"
}

Fence_map: Dict[str, int] = {
    "MnPrv": 1,
    "GdPrv": 1,
    "GdWo": 1,
    "MnWw": 1,
    "None": 0   # no fence
}

ordinal_mappings: Dict[str, Dict[str, int]] = {
    "ExterQual": qual_map,
    "ExterCond": qual_map,
    "BsmtQual": qual_map,
    "BsmtCond": qual_map,
    "HeatingQC": qual_map,
    "KitchenQual": qual_map,
    "FireplaceQu": qual_map,
    "GarageQual": qual_map,
    "GarageCond": qual_map,
    "Functional": functional_map,
    "LandContour": LandContour_map,
    "LotShape": LotShape_map,
    "BsmtExposure": bsmtExposure_map,
    "LandSlope": landSlope_map,
    "GarageFinish": GarageFinish_map,
    "PavedDrive": PavedDrive_map,
    "CentralAir": CentralAir_map,
    "Fence": Fence_map,
}

# Keep the uppercase alias your config exports/uses
ORDINAL_MAPS: Dict[str, Dict[str, int]] = ordinal_mappings


#Engineered features from EDA 
ENGINEERED_FEATURES = [
    "TotalLivingArea",
    "TotalPorchSF",
    "OverallGrade",
    "TotalBathrooms",
    "HouseAge",
]


class ExportDict(TypedDict):
    version: str
    impute_plan: Dict[str, List[str]]
    drop_cols: List[str]
    ordinal_objects: List[str]
    ordinal_maps: Dict[str, Dict[str, int]]
    features: Dict[str, object]
    

def as_dict() -> ExportDict:
    return ExportDict(
        version=CONFIG_VERSION,
        impute_plan=asdict(IMPUTE_PLAN),
        drop_cols=DROP_COLS,
        ordinal_objects=ORDINAL_OBJECTS,
        ordinal_maps=ORDINAL_MAPS,
        features={"keep": FEATURES.keep,
                  "add_zero_inflated_flags": FEATURES.add_zero_inflated_flags,
                  "add_ratios": FEATURES.add_ratios,
                  "add_ages": FEATURES.add_ages,
                 "engineered_features": ENGINEERED_FEATURES,}
    )

__all__ = [
    "CONFIG_VERSION","CONFIG_UPDATED_AT",
    "IMPUTE_PLAN","DROP_COLS",
    "ORDINAL_OBJECTS","ORDINAL_MAPS",
    "FEATURES","as_dict",
]