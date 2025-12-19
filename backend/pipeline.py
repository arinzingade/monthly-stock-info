import pandas as pd
import logging


class DataPipeline:

    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(self.__class__.__name__)

    def load_data(self, csv_path):
        self.logger.info("Loading data from CSV: %s", csv_path)

        df = pd.read_csv(csv_path, parse_dates=["date"])
        df = df.sort_values(["ticker", "date"])
        df.set_index("date", inplace=True)

        self.logger.info(
            "Loaded %d rows for %d tickers",
            len(df),
            df["ticker"].nunique()
        )
        return df

    def resample_monthly(self, df):
        self.logger.info("Resampling daily data to monthly frequency")

        monthly = (
            df.groupby("ticker")
              .resample("M")
              .agg(
                  open=("open", "first"),
                  high=("high", "max"),
                  low=("low", "min"),
                  close=("close", "last"),
                  volume=("volume", "sum"),
              )
              .reset_index()
        )

        self.logger.info(
            "Monthly resampling complete: %d rows generated",
            len(monthly)
        )
        return monthly

    def add_indicators(self, df):
        self.logger.info("Calculating technical indicators (SMA & EMA)")

        df = df.sort_values(["ticker", "date"])

        df["SMA_10"] = df.groupby("ticker")["close"].transform(
            lambda x: x.rolling(10).mean()
        )
        df["SMA_20"] = df.groupby("ticker")["close"].transform(
            lambda x: x.rolling(20).mean()
        )
        df["EMA_10"] = df.groupby("ticker")["close"].transform(
            lambda x: x.ewm(span=10, adjust=False).mean()
        )
        df["EMA_20"] = df.groupby("ticker")["close"].transform(
            lambda x: x.ewm(span=20, adjust=False).mean()
        )

        self.logger.info("Indicator calculation completed")
        return df

    def write_per_ticker(self, df, output_dir):
        self.logger.info("Writing per-ticker output files to: %s", output_dir)

        for ticker, data in df.groupby("ticker"):
            if len(data) != 24:
                self.logger.error(
                    "Ticker %s has %d months instead of 24",
                    ticker,
                    len(data)
                )
                raise ValueError(f"{ticker} does not have exactly 24 months of data")

            file_path = f"{output_dir}/result_{ticker}.csv"
            data.to_csv(file_path, index=False)

            self.logger.info(
                "Written %s (%d rows)",
                file_path,
                len(data)
            )

    def process_pipeline(self, input_csv, output_dir):
        self.logger.info("Starting data pipeline")

        df = self.load_data(input_csv)
        monthly = self.resample_monthly(df)
        monthly = self.add_indicators(monthly)
        self.write_per_ticker(monthly, output_dir)

        self.logger.info("Data pipeline completed successfully")
