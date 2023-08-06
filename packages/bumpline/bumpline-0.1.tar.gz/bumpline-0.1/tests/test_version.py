from bumpline.version import Version


class TestCompareVersion:
    def test_compare_equal_major_versions(self):
        assert Version("2") == Version("2.0")
        assert Version("2") == Version("2.0.0")

        assert Version("1.0a") == Version("1.0.0alpha")
        assert Version("1.2b") == Version("1.2.0beta")
        assert Version("2c") == Version("2.0rc")

    def test_compare_lower_major_versions(self):
        assert Version("1") < Version("2")
        assert Version("1") < Version("2.1")

        assert Version("1.5") < Version("2.1")
        assert Version("2.10a") < Version("3")
