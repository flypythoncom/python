"""Contract tests for the scenario report tool.

The suite is run twice: against ``starter/`` (specific failures expected) and
against ``solution/`` (everything must pass). See ../TASK.md for the contract.
"""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

import report_tool

COURSE_ROOT = Path(__file__).resolve().parent.parent
SCENARIO_ROOT = COURSE_ROOT / "scenario"


class LoadRecordsTest(unittest.TestCase):
    def test_load_csv_records_returns_list_of_dicts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / "rows.csv"
            data.write_text("id,region,amount\n1,emea,10.5\n2,apac,3\n", encoding="utf-8")
            records = report_tool.load_records(data)
        self.assertEqual(records, [{"id": "1", "region": "emea", "amount": "10.5"}, {"id": "2", "region": "apac", "amount": "3"}])

    def test_load_json_records_returns_list_of_dicts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / "rows.json"
            data.write_text('[{"id": "1", "amount": "2"}]', encoding="utf-8")
            records = report_tool.load_records(data)
        self.assertEqual(records, [{"id": "1", "amount": "2"}])

    def test_unsupported_suffix_raises_value_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / "rows.xlsx"
            with self.assertRaises(ValueError):
                report_tool.load_records(data)


class BuildReportTest(unittest.TestCase):
    def test_invalid_records_are_isolated_with_reasons(self) -> None:
        records = [
            {"id": "1", "region": "emea", "amount": "10"},
            {"id": "2", "region": "", "amount": "5"},      # missing group value
            {"id": "", "region": "emea", "amount": "5"},   # missing required id
            {"id": "3", "region": "apac", "amount": "n/a"} # non-numeric amount
        ]
        report = report_tool.build_report(
            records,
            required_fields=["id", "region", "amount"],
            numeric_field="amount",
            group_field="region",
        )
        self.assertEqual(report["total"], 4)
        self.assertEqual(report["valid"], 1)
        self.assertEqual(report["invalid"], 3)
        self.assertEqual([error["index"] for error in report["errors"]], [1, 2, 3])
        self.assertTrue(all(error["reason"] for error in report["errors"]))
        self.assertEqual(report["groups"], {"emea": {"count": 1, "total": 10.0}})

    def test_group_totals_are_rounded_to_two_decimals(self) -> None:
        records = [
            {"id": "1", "region": "emea", "amount": "0.1"},
            {"id": "2", "region": "emea", "amount": "0.2"},
        ]
        report = report_tool.build_report(
            records,
            required_fields=["id", "region", "amount"],
            numeric_field="amount",
            group_field="region",
        )
        self.assertEqual(report["groups"]["emea"]["total"], 0.3)


class WriteReportTest(unittest.TestCase):
    def test_write_report_creates_missing_parent_directories(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "out" / "nested" / "report.json"
            report_tool.write_report({"total": 1}, destination)
            self.assertTrue(destination.exists())
            self.assertEqual(json.loads(destination.read_text(encoding="utf-8"))["total"], 1)
            self.assertFalse(destination.with_name(destination.name + ".tmp").exists())


class ScenarioTest(unittest.TestCase):
    def _copy(self, name: str) -> Path:
        target = Path(tempfile.mkdtemp(prefix="scenario-")) / name
        shutil.copytree(SCENARIO_ROOT / name, target)
        self.addCleanup(shutil.rmtree, target.parent, ignore_errors=True)
        return target

    def test_run_scenario_writes_report_file(self) -> None:
        scenario = self._copy("api-tool")
        report = report_tool.run_scenario(scenario)
        written = json.loads((scenario / "report.json").read_text(encoding="utf-8"))
        self.assertEqual(written, report)
        self.assertEqual(report["total"], 7)
        self.assertEqual(report["invalid"], 2)
        self.assertEqual(sorted(report["groups"]), ["high", "low", "normal"])

    def test_main_prints_summary_and_returns_zero(self) -> None:
        scenario = self._copy("excel-report")
        exit_code = report_tool.main([str(scenario)])
        self.assertEqual(exit_code, 0)
        self.assertTrue((scenario / "report.json").exists())

    def test_main_rejects_missing_argument(self) -> None:
        self.assertEqual(report_tool.main([]), 2)


if __name__ == "__main__":
    unittest.main()
