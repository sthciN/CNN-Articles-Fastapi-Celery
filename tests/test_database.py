# import unittest
# from psycopg2 import sql, extras
# from unittest.mock import MagicMock, patch

# class TestDatabaseFunctions(unittest.TestCase):
#     @patch('app.database.connect_to_db')
#     def test_write_result_to_db(self, mock_connect):
#     # with patch('app.database.connect_to_db') as mock_connect:
#     #     mock_connect.return_value.__enter__.return_value.cursor.return_value = MagicMock()
#         # Arrange
#         mock_conn = MagicMock()
#         mock_connect.return_value = mock_conn
#         mock_cur = MagicMock()
#         mock_conn.cursor.return_value = mock_cur

#         from app.database import write_result_to_db

#         result = [{'article_id': 1, 'similar_article_id': 2, 'title': 'Title 1', 'url': 'http://example.com/1', 'similarity': 0.5}]

#         # Act
#         write_result_to_db(mock_conn, 1, result)

#         # Assert
#         mock_cur.execute.assert_called_once()
#         mock_conn.commit.assert_called_once()