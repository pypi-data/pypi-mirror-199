from tests.setup import test_setup
from src.tkaws import Tks3


def test_s3():
    s3 = Tks3()
    file = s3.get
    return True



test_setup()
test_s3()
