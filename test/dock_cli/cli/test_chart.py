def test_chart_list(runner, dock, mock_chart_helper, chart_list):
    result = runner.invoke(dock, ['chart', 'list'])
    mock_chart_helper.assert_called_once()
    mock_chart_helper.return_value.get_charts.assert_called_once()
    assert result.exit_code == 0
    assert result.output == ''.join(f'{chart}\n' for chart in chart_list)

def test_chart_diff(runner, dock, mock_chart_helper):
    result = runner.invoke(dock, ['chart', 'diff', 'HEAD', 'HEAD'])
    mock_chart_helper.assert_called_once()
    mock_chart_helper.return_value.get_updated_charts.assert_called_once()
    assert result.exit_code == 0
    assert result.output == ''

def test_chart_diff_initial_commit(runner, dock, mock_chart_helper, initial_commit, chart_list):
    result = runner.invoke(dock, ['chart', 'diff', initial_commit, 'HEAD'])
    mock_chart_helper.assert_called_once()
    mock_chart_helper.return_value.get_updated_charts.assert_called_once()
    assert result.exit_code == 0
    assert result.output == ''.join(f'{chart}\n' for chart in chart_list)

def test_chart_show(runner, dock, mock_chart_helper, chart_section):
    result = runner.invoke(dock, ['chart', 'show', chart_section.section])
    mock_chart_helper.assert_called_once()
    mock_chart_helper.return_value.get_chart.assert_called_once_with(chart_section.section)
    assert result.exit_code == 0
    assert result.output == f'{chart_section.registry}/{chart_section.name}\n'

def test_chart_package(runner, dock, mock_chart_helper, mock_commands_run, chart_section, test_repo):
    # pylint: disable=too-many-arguments
    result = runner.invoke(dock, ['chart', 'package', chart_section.section, '--destination', '.'])
    mock_chart_helper.assert_called_once()
    mock_commands_run.assert_called_once_with([mock_chart_helper.return_value.command.helm, 'package',
                                               test_repo / chart_section.section, '--destination', '.'])
    assert result.exit_code == 0

def test_chart_package_list(runner, dock, mock_chart_helper, mock_commands_run, chart_list, test_repo):
    # pylint: disable=too-many-arguments
    result = runner.invoke(dock, ['chart', 'package', *chart_list, '--destination', '.'])
    mock_chart_helper.assert_called_once()
    print(dir(mock_commands_run))
    for section in chart_list:
        mock_commands_run.assert_any_call([mock_chart_helper.return_value.command.helm, 'package',
                                           test_repo / section, '--destination', '.'])
    assert result.exit_code == 0
