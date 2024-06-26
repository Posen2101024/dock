import pathlib
import pytest
from helpers import ChartSection, ImageSection
from dock_cli.main import cli

CONFIG_FILE = pathlib.Path(__file__).resolve().parent.parent / 'dummy_repo' / 'dock.ini'
CONFIG_FILE_INIT = pathlib.Path(__file__).resolve().parent.parent / 'dummy_repo' / 'dock-does-not-exist.ini'

CONFIG_CHART_SECTIONS = [
    ChartSection('charts/chart-1', 'chart-1'),
    ChartSection('charts/chart-2', 'chart-2'),
    ChartSection('charts/chart-3', 'chart-3'),
    ChartSection('charts/chart-4', 'chart-4'),
]

VALID_CHART_SECTIONS = [
    *CONFIG_CHART_SECTIONS,
    ChartSection('charts/chart-5', 'chart-5'),
]

INVALID_CHART_SECTIONS = [
    ChartSection('charts/chart-mew', 'chart-mew'),
    ChartSection('charts/chart-omg', 'chart-omg'),
]

CONFIG_IMAGE_SECTIONS = [
    ImageSection('images/image-1', 'image-1'),
    ImageSection('images/image-2', 'image-2'),
    ImageSection('images/image-3', 'image-3'),
    ImageSection('images/image-4', 'custom-image-name'),
]

VALID_IMAGE_SECTIONS = [
    *CONFIG_IMAGE_SECTIONS,
    ImageSection('images/image-5', 'image-5'),
]

INVALID_IMAGE_SECTIONS = [
    ImageSection('images/image-mew', 'image-mew'),
    ImageSection('images/image-omg', 'image-omg'),
]

@pytest.fixture(scope='session')
def dock():
    return cli

@pytest.fixture(scope='function',
                params=['-h', '--help'])
def help_option(request):
    return request.param

@pytest.fixture(scope='function')
def config_file():
    return CONFIG_FILE

@pytest.fixture(scope='function')
def config_file_init():
    return CONFIG_FILE_INIT

@pytest.fixture(scope='function',
                params=CONFIG_CHART_SECTIONS,
                ids=[section.name for section in CONFIG_CHART_SECTIONS])
def chart_section(request):
    return request.param

@pytest.fixture(scope='function',
                params=CONFIG_IMAGE_SECTIONS,
                ids=[section.name for section in CONFIG_IMAGE_SECTIONS])
def image_section(request):
    return request.param

@pytest.fixture(scope='function',
                params=VALID_CHART_SECTIONS,
                ids=[section.name for section in VALID_CHART_SECTIONS])
def valid_chart_section(request):
    return request.param

@pytest.fixture(scope='function',
                params=VALID_IMAGE_SECTIONS,
                ids=[section.name for section in VALID_IMAGE_SECTIONS])
def valid_image_section(request):
    return request.param

@pytest.fixture(scope='function',
                params=INVALID_CHART_SECTIONS,
                ids=[section.name for section in INVALID_CHART_SECTIONS])
def invalid_chart_section(request):
    return request.param

@pytest.fixture(scope='function',
                params=INVALID_IMAGE_SECTIONS,
                ids=[section.name for section in INVALID_IMAGE_SECTIONS])
def invalid_image_section(request):
    return request.param

@pytest.fixture(scope='function')
def chart_list():
    return ['charts/chart-1',
            'charts/chart-2',
            'charts/chart-3',
            'charts/chart-4']

@pytest.fixture(scope='function')
def image_list():
    return ['images/image-1',
            'images/image-4',
            'images/image-3',
            'images/image-2']

@pytest.fixture(scope='function')
def initial_commit():
    return '472afe80cb490b6827e775bcc8b0a42eaee27db5'

@pytest.fixture(scope='function')
def mock_commands_run(mocker):
    mock = mocker.patch('dock_cli.utils.commands.run')
    mock.return_value = mocker.MagicMock()
    return mock

@pytest.fixture(scope='function', autouse=True)
def mock_config_open(mocker):
    mock = mocker.patch('dock_cli.utils.utils.open')
    mock.new_callable = mocker.mock_open
    return mock

@pytest.fixture(scope='function')
def mock_subprocess_run(mocker):
    mock = mocker.patch('dock_cli.utils.commands.subprocess.run')
    mock.return_value = mocker.MagicMock(check_returncode=lambda: None)
    return mock

@pytest.fixture(scope='function',
                params=[True, False])
def mock_click_confirm(request, mocker):
    mock = mocker.patch('click.confirm')
    mock.return_value = request.param
    return mock

@pytest.fixture(scope='function')
def mock_click_echo(mocker):
    mock = mocker.patch('click.echo')
    mock.return_value = mocker.MagicMock()
    return mock

@pytest.fixture(scope='function')
def mock_click_prompt(mocker):
    mock = mocker.patch('click.prompt')
    mock.return_value = 'namespace'
    return mock

@pytest.fixture(scope='function')
def mock_update_config(mocker):
    mock = mocker.patch('dock_cli.utils.utils.update_config')
    mock.return_value = mocker.MagicMock()
    return mock
