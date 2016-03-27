"""A set of test cases for common"""
from __future__ import print_function
import os


def test_sqlite_connection():
    """A simple smoke test"""
    from common import credential_manager, sqlite_manager
    cred_mgr = credential_manager.CredentialManager(
        host=None,
        user=None,
        passwd=None,
        name='test.db'
    )

    db = sqlite_manager.DatabaseAccess(cred_mgr)
    db.connect()
    print(db.execute_all("SELECT * from sqlite_master where type='table'"))
    db.close()
    assert 'test.db' in os.listdir('.')
    os.remove('test.db')


def test_dependency_planning():
    """A simple smoke test"""
    from common import dependency_planning
    depr = dependency_planning.DependencyResolver()
    depr.add_task('arithmetic mean')
    depr.add_task('geometric mean')
    depr.add_task('median')
    depr.add_task('quartiles')
    depr.add_task('standard deviation')
    depr.add_dep('downside standard deviation', 'arithmetic mean')
    depr.add_dep('MAD', 'arithmetic mean')
    depr.add_dep('sharpe ratio', 'standard deviation')
    depr.add_dep('sortino ratio', 'downside standard deviation')
    depr.visualize('out.png')
    assert 'out.png' in os.listdir('.')
    os.remove('out.png')
    depr.generate_solution('MAD')
    print(depr.sol)
    assert depr.validate_solution(depr.sol, [])


def test_config_section():
    """Run tests over the testing section of the config file"""
    from common import config
    test_config = config.Section('testing')
    str_test = test_config.get('s')
    assert str_test == 'abc'
    assert isinstance(str_test, str) or isinstance(str_test, unicode)

    int_test = test_config.getint('x')
    assert isinstance(int_test, int)
    assert int_test == 1

    float_test = test_config.getfloat('f')
    assert isinstance(float_test, float)
    assert float_test == -0.05

    true_test = test_config.getboolean('bt')
    assert true_test
    assert isinstance(true_test, bool)

    false_test = test_config.getboolean('bf')
    assert not false_test
    assert isinstance(false_test, bool)

    list_test = test_config.getlist('li')
    assert len(list_test) == 3
    assert isinstance(list_test, list)
