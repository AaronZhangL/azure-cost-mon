import pytest, responses
import datetime

from azure_billing.scrape import current_month, convert_json_df, extract_metrics_from_df
from azure_billing.scrape import base_columns, cost_column, get_azure_data, data
from azure_billing.metrics import Counter

from data import sample_data


def test_month():
    now = datetime.datetime.now()
    assert current_month() == now.strftime("%Y-%m")


def test_df_conversion():
    df = convert_json_df(sample_data)

    assert df.columns.size == len(base_columns) + len(cost_column)
    assert len(df) == len(sample_data)


def test_df_missing_column():
    with pytest.raises(KeyError):
        df = convert_json_df([dict(AccountName='foo',
                                   ConsumedService='bar',
                                   SubscriptionName='baz',
                                   ExtendedCost=1.2)])


def test_extract_metrics():
    c = Counter('costs', 'desc')
    df = convert_json_df(sample_data)
    extract_metrics_from_df(df, c)

    assert len(c._records) == 2

    expected_0 = 'costs{DepartmentName="engineering",MeterSubCategory="gateway hour",ResourceGroup="",MeterCategory="virtual network",SubscriptionName="production",MeterName="hours",AccountName="platform"} 0.70\n'
    expected_1 = 'costs{DepartmentName="engineering",MeterSubCategory="locally redundant",ResourceGroup="my-group",MeterCategory="windows azure storage",SubscriptionName="production",MeterName="standard io - page blob/disk (gb)",AccountName="platform"} 0.00\n'

    assert c._records[0] == expected_0
    assert c._records[1] == expected_1


@responses.activate
def test_get_azure_data():

    enrollment='12345'

    responses.add(
        method='GET',
        url="https://ea.azure.com/rest/{}/usage-report?month=2017-03&type=detail&fmt=Json".format(enrollment),
        match_querystring=True,
        json=sample_data
    )

    data = get_azure_data(enrollment, 'abc123xyz', '2017-03')
    assert data == sample_data


@responses.activate
def test_data():

    enrollment='12345'
    token='abc123xyz'

    responses.add(
        method='GET',
        url="https://ea.azure.com/rest/{}/usage-report?month=2017-03&type=detail&fmt=Json".format(enrollment),
        match_querystring=True,
        json=sample_data
    )

    prom_data = data(enrollment, token, month='2017-03')
    assert prom_data.count('azure_costs') == 4