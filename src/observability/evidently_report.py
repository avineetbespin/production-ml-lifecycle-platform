from evidently.report import Report
from evidently.metric_preset import DataDriftPreset


def generate_drift_html(current_data, reference_data, output_path: str = "drift_report.html") -> str:
    report = Report(metrics=[DataDriftPreset()])
    report.run(current_data=current_data, reference_data=reference_data)
    report.save_html(output_path)
    return output_path
