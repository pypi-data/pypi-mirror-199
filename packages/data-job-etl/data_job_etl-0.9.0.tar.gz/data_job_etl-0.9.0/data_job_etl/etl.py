from data_job_etl.extract.extract import Extractor
from data_job_etl.transform.preprocess import Preprocessor
from data_job_etl.transform.process import Processor
from data_job_etl.load.load import Loader
from data_job_etl.load.create_tables import create_tables


def etl():
    """
    ETL pipeline.
    """
    # Create tables
    create_tables()

    # Extraction
    print('Extracting')
    extractor = Extractor()
    raw_jobs = extractor.extract_raw_jobs()

    # Transformation
    print('Transforming')
    preprocessor = Preprocessor(raw_jobs)
    preprocessor.preprocess()
    preprocessed_jobs = preprocessor.jobs

    processor = Processor()
    processed_jobs = processor.process_technos(preprocessed_jobs)
    pivotted_jobs = processor.pivot_technos(processed_jobs)

    print(pivotted_jobs.head())

    # Loading
    print('Loading')
    loader = Loader()
    loader.load_processed(processed_jobs)
    loader.load_pivotted(pivotted_jobs)

