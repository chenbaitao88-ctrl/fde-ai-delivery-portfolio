import unittest
from demo import summarize, run

class CalculationTests(unittest.TestCase):
    def row(self, n, eligible="yes", status="complete", minutes="10"):
        return dict(case_id=str(n), group="A", eligible=eligible, status=status, minutes=minutes)
    def test_actual_input_and_weighted_total(self):
        s=run()["summary"]
        self.assertEqual((s["input_count"],s["eligible"],s["complete"]),(12,11,9))
        self.assertEqual(s["rate_percent"],81.8)
        self.assertEqual([s["groups"][x]["rate_percent"] for x in ["A","B","C"]],[75.0,66.7,100.0])
    def test_missing_field_blocks(self):
        row=self.row(1);del row["status"]
        with self.assertRaisesRegex(ValueError,"missing"):summarize([row])
    def test_zero_denominator_blocks(self):
        with self.assertRaisesRegex(ValueError,"denominator"):summarize([self.row(1,"no")])
    def test_duplicate_blocks(self):
        with self.assertRaisesRegex(ValueError,"unique"):summarize([self.row(1),self.row(1)])
    def test_nonfinite_time_blocks(self):
        for value in ["nan","inf","-1"]:
            with self.subTest(value=value),self.assertRaises(ValueError):summarize([self.row(1,minutes=value)])
    def test_unknown_status_blocks(self):
        with self.assertRaisesRegex(ValueError,"status"):summarize([self.row(1,status="unknown")])

if __name__ == "__main__":unittest.main()
