import unittest
from unittest.mock import patch

from main import Group, groups, student_groups, students, get_query_results


class QueryResultsTests(unittest.TestCase):
    def test_data_contains_five_students_four_groups_and_valid_ids(self):
        self.assertEqual(len(students), 5)
        self.assertEqual(len(groups), 4)
        group_ids = {group.id for group in groups}
        student_ids = {student.id for student in students}
        self.assertTrue(all(student.group_id in group_ids for student in students))
        self.assertTrue(all(link.student_id in student_ids and link.group_id in group_ids
                            for link in student_groups))

    def test_one_to_many_query_selects_a_groups_and_students(self):
        res_1, _, _ = get_query_results()
        self.assertEqual(res_1, {
            "Аналитика-01": ["Иванов", "Петров"],
            "Архитектура-02": ["Сидорова"],
        })

    def test_one_to_many_query_keeps_empty_a_group(self):
        with patch("main.groups", groups + [Group(5, "Аудитория-05")]):
            res_1, _, _ = get_query_results()
        self.assertEqual(res_1["Аудитория-05"], [])

    def test_max_scholarship_skips_empty_groups_and_sorts_descending(self):
        _, res_2, _ = get_query_results()
        self.assertEqual(res_2, [
            ("Аналитика-01", 3200),
            ("ИУ5-34", 3200),
            ("Архитектура-02", 1800),
        ])
        scholarships = [scholarship for _, scholarship in res_2]
        self.assertEqual(scholarships, sorted(scholarships, reverse=True))
        self.assertNotIn("Программирование-04", [name for name, _ in res_2])

    def test_many_to_many_query_contains_all_links_sorted_by_group_name(self):
        _, _, res_3 = get_query_results()
        self.assertEqual(len(res_3), len(student_groups))
        self.assertEqual([group_name for _, group_name in res_3],
                         sorted(group_name for _, group_name in res_3))
        self.assertIn(("Иванов", "ИУ5-34"), res_3)
        self.assertIn(("Иванов", "Аналитика-01"), res_3)


if __name__ == "__main__":
    unittest.main()
