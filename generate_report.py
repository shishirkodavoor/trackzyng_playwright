"""Script to generate Excel report after test execution."""
import sys
from pathlib import Path
from utils.report_generator import generate_excel_report
from datetime import datetime

if __name__ == "__main__":
    base_dir = Path(__file__).parent
    allure_dir = base_dir / "reports" / "allure-results"
    output_file = base_dir / "reports" / f"Test_Results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    print("Generating Excel report...")
    generate_excel_report(output_file, allure_dir)
    print(f"Report generated successfully: {output_file}")

