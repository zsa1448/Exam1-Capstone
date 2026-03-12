
"""
Exam 1 - Test Inventory Module
================================
Write your tests below. Each section (Part A through E) is marked.
Follow the instructions in each part carefully.


Run your tests with:
    pytest test_inventory.py -v


Run with coverage:
    pytest test_inventory.py --cov=inventory --cov-report=term-missing -v
"""


import pytest
from unittest.mock import patch
from inventory import (
    add_product,
    get_product,
    update_stock,
    calculate_total,
    apply_bulk_discount,
    list_products,
)




# ============================================================
# FIXTURE: Temporary inventory file (provided for you)
# This ensures each test gets a clean, isolated inventory.
# ============================================================


@pytest.fixture(autouse=True)
def clean_inventory(tmp_path, monkeypatch):
    """Use a temporary inventory file for each test."""
    db_file = str(tmp_path / "inventory.json")
    monkeypatch.setattr("inventory.INVENTORY_FILE", db_file)
    yield


# ============================================================
# PART A - Basic Assertions (18 marks)
# Write at least 8 tests using plain assert statements.
# Cover: add_product, get_product, update_stock,
#        calculate_total, and list_products.
# Follow the AAA pattern (Arrange, Act, Assert).
# ============================================================

def test_add_product():
    # Arrange and Act
    product = add_product("C001", "laptop", 24.99, 50)
    # Assert
    assert product["product_id"] == "C001"
    assert product["name"] == "laptop"
    assert product["price"] == 24.99
    assert product["stock"] == 50


def test_get_product():
    # Arrange 
    add_product("C002", "Keyboard", 13.50, 12)
    #aact
    product = get_product("C002")
    #Assert
    assert product is not None
    assert product["product_id"] == "C002"
    assert product["name"] == "Keyboard"
    assert product["price"] == 13.50
    assert product["stock"] == 12


def test_get_product_nonID():
    #act
    product = get_product("C9999999")
    #assert
    assert product is None


def test_update_stock():
    #arrange
    add_product("C003", "MAC PC", 13.50, 20)
    #act
    new_stock = update_stock("C003", 5)
    #assert
    assert new_stock == 25


def test_update_stock_decreases():
    #arrange
    add_product("C003", "MAC PC", 13.50, 25)
    #act
    new_stock = update_stock("C003", -10)
    #assert
    assert new_stock == 15


def test_list_products():
    #arrange
    add_product("C005", "cam", 19.8, 15)
    add_product("C006", "Headset", 5.99, 22)
    #act
    products = list_products()
    #assert
    assert len(products) == 2


def test_calculate_total():
    #arrange
    add_product("C007", "Monitor", 9.99, 8)
    #act
    total = calculate_total("C007", 3)
    #assert
    assert total==29.97


def test_list_products_2():
    #arrange
    add_product("C008", "Iphone 17", 92.50, 40)
    #act
    products = list_products()
    #assert
    assert len(products) == 1
    item = products[0]
    assert "product_id" in item
    assert "name" in item
    assert "price" in item
    assert "stock" in item




# ============================================================
# PART B - Exception Testing (12 marks)
# Write at least 6 tests using pytest.raises.
# Cover: empty name, negative price, duplicate product,
#        stock going below zero, product not found, etc.
# ============================================================


def test_add_product_emptyID():
    with pytest.raises(ValueError, match="Product ID and name are required"):
        add_product("", "Laptop motherboard", 34.99, 10)


def test_add_product_noname():
    with pytest.raises(ValueError, match="Product ID and name are required"):
        add_product("C009", "", 34.00, 25)


def test_add_product_negprice():
    with pytest.raises(ValueError, match="Price must be positive"):
        add_product("C010", "power bank harger", -5.99, 100)


def test_add_product_dupid():
    add_product("C011", " technology", 10.0, 5)
    with pytest.raises(ValueError, match="already exists"):
        add_product("C011", "duplicate technology", 10.0, 3)


def test_update_negstock():
    add_product("C012", "nokia", 4.99, 4)
    with pytest.raises(ValueError, match="Stock cannot go below zero"):
        update_stock("C012", -10000)


def test_calculate_noquantity():
    add_product("C013", "blackberry", 19.99, 6)
    with pytest.raises(ValueError, match="Quantity must be positive"):
        calculate_total("C013", 0)



# ============================================================
# PART C - Fixtures and Parametrize (10 marks)
#
# C1: Create a @pytest.fixture called "sample_products" that
#     adds 3 products to the inventory and returns their IDs.
#     Write 2 tests that use this fixture.
#
# C2: Use @pytest.mark.parametrize to test apply_bulk_discount
#     with at least 5 different (total, quantity, expected) combos.
# ============================================================

@pytest.fixture
def sample_products():
    add_product("C014", "Laptop Azure", 1000.00, 10)
    add_product("C015", "Mouse pad",30.00, 50)
    add_product("C016", "Keyboard LED", 80.00, 5)
    return ["C014", "C015", "C016"]

def test_list_products_fixturess(sample_products):
    products = list_products()
    assert len(products) == 3

def test_calculate_total_fixturess(sample_products):
    total = calculate_total("C015", 4)
    assert total == 120.00

@pytest.mark.parametrize(
    "total, quantity, expected_result",
    [
        (55.00, 5, 55.00),
        (66.00, 11, 62.70),
        (77.00, 26, 69.30),
        (88.00, 66, 74.80),
        (0.00, 20, 0.00),
    ]
)
def test_apply_bulk_discount(total, quantity, expected_result):
    discount_result = apply_bulk_discount(total, quantity)
    assert discount_result == expected_result




# ============================================================
# PART D - Mocking (5 marks)
# Use @patch to mock _send_restock_alert.
# Write 2 tests:
#   1. Verify the alert IS called when stock drops below 5
#   2. Verify the alert is NOT called when stock stays >= 5
# ============================================================


def test_restock_alert():
    add_product("C016", "apple aripods", 5.99, 6)
    with patch("inventory._send_restock_alert") as mock_alert:
        update_stock("C016", -3)           
        mock_alert.assert_called_once_with("C016", "apple aripods", 3)


def test_restock__alertnotcalled():
    add_product("C017", "portable", 9.99, 20)
    with patch("inventory._send_restock_alert") as mock_alert:
        update_stock("C017", -5)           
        mock_alert.assert_not_called()




# ============================================================
# PART E - Coverage (5 marks)
# Run: pytest test_inventory.py --cov=inventory --cov-report=term-missing -v
# You must achieve 90%+ coverage on inventory.py.
# If lines are missed, add more tests above to cover them.
# ============================================================




# ============================================================
# BONUS (5 extra marks)
# 1. Add a function get_low_stock_products(threshold) to
#    inventory.py that returns all products with stock < threshold.
# 2. Write 3 parametrized tests for it below.
# ============================================================


# TODO: Write your bonus tests here (optional)
