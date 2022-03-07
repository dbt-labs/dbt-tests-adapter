import pytest
from dbt.tests.adapter.basic.files import (
    test_passing_sql,
    test_failing_sql,
)
from dbt.tests.util import check_result_nodes_by_name, run_dbt


@pytest.fixture
def tests():
    return {
        "passing.sql": test_passing_sql,
        "failing.sql": test_failing_sql,
    }


@pytest.fixture
def project_config_update():
    return {"name": "data_tests"}


def test_data_tests(project):
    # test command
    results = run_dbt(["test"])
    assert len(results) == 2

    # We have the right result nodes
    check_result_nodes_by_name(results, ["passing", "failing"])

    # Check result status
    for result in results:
        if result.node.name == "passing":
            assert result.status == "pass"
        elif result.node.name == "failing":
            assert result.status == "fail"
