

from pipeline import DataPipeline

if __name__ == "__main__":
    pipeline = DataPipeline()
    input_csv = "input_files/input.csv"
    output_dir = "output_files"
    pipeline.process_pipeline(input_csv, output_dir)

