import unittest

from api.dependencies import SessionDep, ShipmentServiceDep, SellerServiceDep
from main import app
from services.seller import SellerService
from services.shipment import ShipmentService


class DependencyImportTest(unittest.TestCase):
    def test_dependencies_and_services_import_cleanly(self):
        self.assertTrue(SessionDep is not None)
        self.assertTrue(ShipmentServiceDep is not None)
        self.assertTrue(SellerServiceDep is not None)
        self.assertTrue(SellerService is not None)
        self.assertTrue(ShipmentService is not None)

    def test_main_app_imports(self):
        self.assertIsNotNone(app)

    def test_password_is_truncated_to_72_bytes(self):
        password = "é" * 40
        normalized = SellerService._normalize_password(password)
        self.assertLessEqual(len(normalized.encode("utf-8")), 72)


if __name__ == "__main__":
    unittest.main()
