from __future__ import annotations

import io

import pandas as pd

from universal_transfer_operator.constants import FileType as FileTypeConstants
from universal_transfer_operator.datasets.dataframe.pandas import (
    PandasDataframe,
    convert_columns_names_capitalization,
)
from universal_transfer_operator.datasets.file.types.base import FileTypes


class CSVFileTypes(FileTypes):
    """Concrete implementation to handle CSV file type"""

    # We need skipcq because it's a method overloading so we don't want to make it a static method
    def export_to_dataframe(
        self, stream, columns_names_capitalization="original", **kwargs
    ) -> pd.DataFrame:  # skipcq PYL-R0201
        """
        Read csv file from one of the supported locations and return dataframe.

        :param stream: file stream object
        :param columns_names_capitalization: determines whether to convert all columns to lowercase/uppercase
            in the resulting dataframe
        """
        df = pd.read_csv(stream, **kwargs)
        df = convert_columns_names_capitalization(
            df=df, columns_names_capitalization=columns_names_capitalization
        )
        return PandasDataframe.from_pandas_df(df)

    # We need skipcq because it's a method overloading so we don't want to make it a static method
    def create_from_dataframe(self, df: pd.DataFrame, stream: io.TextIOWrapper) -> None:  # skipcq PYL-R0201
        """
        Write csv file to one of the supported locations

        :param df: pandas dataframe
        :param stream: file stream object
        """
        df.to_csv(stream, index=False)

    @property
    def name(self):
        return FileTypeConstants.CSV
