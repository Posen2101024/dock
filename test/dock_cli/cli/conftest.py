import pytest

@pytest.fixture(scope='function', autouse=True)
def mock_chart_helper(mocker, chart_helper):
    mocker.spy(chart_helper, 'get_section_path')
    mocker.spy(chart_helper, 'get_section_file')
    mocker.spy(chart_helper, 'get_section_type')
    mocker.spy(chart_helper, 'get_section_registry')
    mocker.spy(chart_helper, 'is_valid_section')
    mocker.spy(chart_helper, 'validate_section')
    mocker.spy(chart_helper, 'get_chart_info')
    mocker.spy(chart_helper, 'get_chart_name')
    mocker.spy(chart_helper, 'get_chart_version')
    mocker.spy(chart_helper, 'get_chart')
    mocker.spy(chart_helper, 'get_charts')
    mocker.spy(chart_helper, 'get_updated_charts')
    mocker.spy(chart_helper, 'get_chart_archive_file')
    mock = mocker.patch('dock_cli.utils.helpers.ChartHelper')
    mock.return_value = chart_helper
    return mock

@pytest.fixture(scope='function', autouse=True)
def mock_image_helper(mocker, image_helper):
    mocker.spy(image_helper, 'get_section_path')
    mocker.spy(image_helper, 'get_section_file')
    mocker.spy(image_helper, 'get_section_type')
    mocker.spy(image_helper, 'get_section_name')
    mocker.spy(image_helper, 'get_section_registry')
    mocker.spy(image_helper, 'is_valid_section')
    mocker.spy(image_helper, 'validate_section')
    mocker.spy(image_helper, 'get_image')
    mocker.spy(image_helper, 'get_images')
    mocker.spy(image_helper, 'get_updated_images')
    mock = mocker.patch('dock_cli.utils.helpers.ImageHelper')
    mock.return_value = image_helper
    return mock
