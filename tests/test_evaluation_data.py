"""Meaningful validation and boundary checks, using malformed inputs."""
from pathlib import Path
import sys, unittest
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from generate_evaluation_data import generate
from validate_evaluation_data import validate_evaluations

class EvaluationValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.raw,cls.clean,cls.judges=generate()
    def test_reproducibility(self):
        other=generate()[1]
        self.assertTrue(self.clean.equals(other))
    def test_different_seed_changes_scores(self):
        self.assertFalse(self.clean.score.equals(generate(seed=43)[1].score))
    def test_missing_score_rejected(self):
        x=self.clean.copy();x.loc[0,'score']=np.nan
        with self.assertRaises(AssertionError):validate_evaluations(x)
    def test_out_of_range_rejected(self):
        for value in [-1,101,np.inf]:
            x=self.clean.copy();x.loc[0,'score']=value
            with self.assertRaises(AssertionError):validate_evaluations(x)
    def test_duplicate_id_rejected(self):
        x=self.clean.copy();x.loc[0,'evaluation_id']=x.loc[1,'evaluation_id']
        with self.assertRaises(AssertionError):validate_evaluations(x)
    def test_invalid_date_rejected(self):
        x=self.clean.copy();x.loc[0,'date']='2026-02-30'
        with self.assertRaises(AssertionError):validate_evaluations(x)
    def test_unknown_category_rejected(self):
        x=self.clean.copy();x.loc[0,'category']='reasoninng'
        with self.assertRaises(AssertionError):validate_evaluations(x)
    def test_exact_boundaries(self):
        x=self.clean.copy();x.loc[0,'score']=0;x.loc[1,'score']=100
        validate_evaluations(x)
        scores=np.array([0,9.99,10,89.99,90,99.99,100])
        np.testing.assert_array_equal(np.minimum((scores//10).astype(int)*10,90),[0,0,10,80,90,90,90])
    def test_inclusive_agreement_threshold(self):
        difference=np.array([9.99,10,10.01])
        np.testing.assert_array_equal((difference<=10).astype(int),[1,1,0])
    def test_balanced_paired_examples(self):
        self.assertEqual(len(self.clean),9000)
        self.assertTrue((self.clean.groupby('example_id').model_version.nunique()==4).all())
        self.assertTrue((self.clean.groupby(['category','model_version']).size()==450).all())

if __name__=='__main__':unittest.main()
