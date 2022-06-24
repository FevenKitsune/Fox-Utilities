import unittest
from utils.findbyname import find_by_name


class FindByNameTestCase(unittest.TestCase):
    def test_standard_matching_functionality(self):
        """Test matching standard Latin alphabet characters with standard Latin alphabet characters."""
        self.search_term = "Febreruauru"
        self.search_domain = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                              "October", "November", "December"]
        self.assertIn(found_term := find_by_name(self.search_term, self.search_domain), self.search_domain)
        print(f"test_standard_matching_functionality Report:\n"
              f"\tSearch term: {self.search_term}\n"
              f"\tSearch domain: {self.search_domain}\n"
              f"\tFound term: {found_term}\n")

    def test_special_character_term_functionality(self):
        """Test matching non-standard Latin alphabet characters with standard Latin alphabet characters."""
        self.search_term = "𝖋𝖊𝖇𝖗𝖚𝖆𝖗𝖞𝖊"
        self.search_domain = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                              "October", "November", "December"]
        self.assertIn(found_term := find_by_name(self.search_term, self.search_domain), self.search_domain)
        print(f"test_special_character_term_functionality Report:\n"
              f"\tSearch term: {self.search_term}\n"
              f"\tSearch domain: {self.search_domain}\n"
              f"\tFound term: {found_term}\n")

    def test_special_character_domain_functionality(self):
        """Test matching standard Latin alphabet characters with non-standard Latin alphabet characters."""
        self.search_term = "Febreruauru"
        self.search_domain = ["𝓙𝓪𝓷𝓾𝓪𝓻𝔂", "𝓕𝓮𝓫𝓻𝓾𝓪𝓻𝔂", "𝓜𝓪𝓻𝓬𝓱", "𝓐𝓹𝓻𝓲𝓵", "𝓜𝓪𝔂", "𝓙𝓾𝓷𝓮",
                              "𝓙𝓾𝓵𝔂", "𝓐𝓾𝓰𝓾𝓼𝓽", "𝓢𝓮𝓹𝓽𝓮𝓶𝓫𝓮𝓻", "𝓞𝓬𝓽𝓸𝓫𝓮𝓻", "𝓝𝓸𝓿𝓮𝓶𝓫𝓮𝓻",
                              "𝓓𝓮𝓬𝓮𝓶𝓫𝓮𝓻"]
        self.assertIn(found_term := find_by_name(self.search_term, self.search_domain), self.search_domain)
        print(f"test_special_character_domain_functionality Report:\n"
              f"\tSearch term: {self.search_term}\n"
              f"\tSearch domain: {self.search_domain}\n"
              f"\tFound term: {found_term}\n")

    def test_conflicting_scores_error_functionality(self):
        """Test an input that has no dominant match."""
        self.search_term = "A"
        self.search_domain = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                              "October", "November", "December"]
        with self.assertRaises(UserWarning):
            find_by_name(self.search_term, self.search_domain)
        print(f"test_conflicting_scores_error_functionality Report:\n"
              f"\tSearch term: {self.search_term}\n"
              f"\tSearch domain: {self.search_domain}\n"
              f"\tFound term: Matching error.\n")


if __name__ == '__main__':
    unittest.main()
