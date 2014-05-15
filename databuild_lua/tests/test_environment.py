from unittest import TestCase
from databuild.adapters.locmem.models import LocMemBook

from databuild import settings as default_settings


class ParserTestCase(TestCase):
    def setUp(self):
        self.settings = default_settings
        self.settings.LANGUAGES['lua'] = 'databuild_lua.lua.LuaEnvironment'

    def test_parse_lua(self):
        expression = {"language": "lua", "content": "return row['a']"}
        book = LocMemBook('project1', settings=self.settings)

        fn = book.operator.parse_expression(expression)
        row = {'a': 2}
        assert fn(row) == 2

        expression['content'] = 'return math.pow(2, 2)'
        fn = book.operator.parse_expression(expression)
        assert fn(row) == 4

    def test_lua_function(self):
        operation = {
            "path": "columns.update_column",
            "description": "",
            "params": {
                "sheet": "a",
                "column": "test column",
                "facets": [],
                "expression": {
                    "language": "lua",
                    "content": "return cross(row, 'b', 'z', 'id')"
                }
            }
        }

        a_data = [
            {'id': 1, 'x': 2, 'y': 3},
            {'id': 2, 'x': 2, 'y': 3.5},
            {'id': 3, 'x': 1, 'y': 3.5},
        ]
        b_data = [
            {'id': 3, 'z': 3},
            {'id': 1, 'z': 4},
            {'id': 2, 'z': 4.5},
        ]

        book = LocMemBook('project1', settings=self.settings)
        sheet_a = book.add_sheet('a', ['id', 'x', 'y'])
        sheet_b = book.add_sheet('b', ['id', 'z'])

        sheet_a.extend(a_data)
        sheet_b.extend(b_data)

        sheet_a.append_column("test column")
        book.apply_operation(operation)
        assert sheet_a.get_column('test column') == [4, 4.5, 3]
