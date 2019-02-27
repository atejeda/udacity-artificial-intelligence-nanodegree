import unittest
from importlib import reload

import asl_test_model_selectors
reload(asl_test_model_selectors)

suite = unittest.TestLoader().loadTestsFromModule(asl_test_model_selectors.TestSelectors())
unittest.TextTestRunner().run(suite)
