from evidently import ColumnMapping
from evidently.report import Report
from evidently.testsuite import TestSuite, TestSuiteResult
from evidently.tests import DataDriftTest


def create_data_drift_report(current_data, reference_data):
    mapping = ColumnMapping()
    report = Report(
        metrics=[DataDriftTest()],
        column_mapping=mapping,
    )
    report.run(current_data=current_data, reference_data=reference_data)
    result = report.as_dict()
    drifts = result.get("metrics", [])
    drift_detected = any(metric.get("result", {}).get("anomaly", False) for metric in drifts)
    return {
        "data_drift_detected": drift_detected,
        "report": result,
    }
