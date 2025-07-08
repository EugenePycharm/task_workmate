import pytest
from csv_processor.processor import read_csv, apply_filter, apply_aggregation, apply_order
import os

@pytest.fixture
def sample_data(tmp_path):
    csv_content = """name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
poco x5 pro,xiaomi,299,4.4"""
    
    file_path = os.path.join(tmp_path, "test.csv")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(csv_content)
    
    return file_path


def test_read_csv(sample_data):
    data = read_csv(sample_data)
    assert len(data) == 4
    assert data[0]['name'] == 'iphone 15 pro'
    assert data[1]['brand'] == 'samsung'


def test_filter_equals(sample_data):
    data = read_csv(sample_data)
    filtered = apply_filter(data, "brand=xiaomi")
    assert len(filtered) == 2
    assert all(row['brand'].lower() == 'xiaomi' for row in filtered)


def test_filter_greater(sample_data):
    data = read_csv(sample_data)
    filtered = apply_filter(data, "price>300")
    assert len(filtered) == 2
    assert all(float(row['price']) > 300 for row in filtered)


def test_filter_less(sample_data):
    data = read_csv(sample_data)
    filtered = apply_filter(data, "price<500")
    assert len(filtered) == 2
    assert all(float(row['price']) < 500 for row in filtered)


def test_aggregation_avg(sample_data):
    data = read_csv(sample_data)
    avg = apply_aggregation(data, "price=avg")
    assert avg == pytest.approx((999 + 1199 + 199 + 299) / 4)


def test_aggregation_min(sample_data):
    data = read_csv(sample_data)
    min_val = apply_aggregation(data, "price=min")
    assert min_val == 199


def test_aggregation_max(sample_data):
    data = read_csv(sample_data)
    max_val = apply_aggregation(data, "price=max")
    assert max_val == 1199


def test_sort_asc(sample_data):
    data = read_csv(sample_data)
    sorted_data = apply_order(data, "price=asc")
    prices = [float(row['price']) for row in sorted_data]
    assert prices == sorted(prices)


def test_sort_desc(sample_data):
    data = read_csv(sample_data)
    sorted_data = apply_order(data, "price=desc")
    prices = [float(row['price']) for row in sorted_data]
    assert prices == sorted(prices, reverse=True)


def test_invalid_sort_format(sample_data):
    data = read_csv(sample_data)
    with pytest.raises(ValueError, match="Неверный формат сортировки"):
        apply_order(data, "price:asc")