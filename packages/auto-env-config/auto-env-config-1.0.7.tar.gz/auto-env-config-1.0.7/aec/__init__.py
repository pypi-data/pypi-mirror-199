import os
import sys
import json
from pip._internal.cli.main import main as pip

name = 'auto-env-config'


def check_package(
        package_name
):
    """
    Check if the package is installed.
    :param package_name: The name of the package.
    :return: True or False
    """
    python_path = sys.executable
    name_id = 0
    while os.path.exists(f'log_{name_id}.txt'):
        name_id += 1
    os.system(f'{python_path} -m pip show {package_name} > log_{name_id}.txt 2>&1')
    with open(f'log_{name_id}.txt', 'r') as f:
        log = f.read()
    os.remove(f'log_{name_id}.txt')
    if log.startswith('WARNING:'):
        return None
    return {i.split(': ')[0]: i.split(': ')[1].strip() if len(i.split(': ')) > 1 else '' for i in log.split('\n') if i}


def pip_update(pip_index=None):
    """
    Update pip.
    :param pip_index: The index of pip.
    :return: None
    """
    # python_path = sys.executable
    if pip_index:
        pip(f'install --upgrade pip -i {pip_index}'.split(' '))
        # os.system(f'{python_path} -m pip install --upgrade pip -i {pip_index}')
    else:
        pip('install --upgrade pip'.split(' '))
        # os.system(f'{python_path} -m pip install --upgrade pip')


def install_package(
        name,
        version=None,
        pip_index=None,
        install_command=None,
        after_command=None,
        nt_install_command=None,
        nt_after_command=None,
        posix_install_command=None,
        posix_after_command=None
):
    """
    Install the package.
    :param after_command: The command to be executed after the installation is complete.
    :param install_command: The command of installing the package.
    :param posix_after_command: The command to be executed after the installation is complete on posix.
    :param posix_install_command: The command of installing the package on posix.
    :param nt_after_command: The command to be executed after the installation is complete on nt.
    :param nt_install_command: The command of installing the package on nt.
    :param pip_index: The index of pip.
    :param name: The name of the package.
    :param version: The version of the package.
    :return: None
    """
    if check_package(name) is not None:
        return None
    python_path = sys.executable
    if nt_install_command and os.name == 'nt':
        install_command = nt_install_command
    elif posix_install_command and os.name == 'posix':
        install_command = posix_install_command
    if install_command:
        if install_command.startswith('pip'):
            command = install_command.split(' ')
            command[0] = f'{python_path} -m pip'
            install_command = ' '.join(command)
        elif install_command.startswith('python'):
            command = install_command.split(' ')
            command[0] = f'{python_path}'
            install_command = ' '.join(command)
        os.system(install_command)
    elif version:
        if pip_index:
            pip(f'install {name}=={version} -i {pip_index}'.split(' '))
            # os.system(f'{python_path} -m pip install {name}=={version} -i {pip_index}')
        else:
            pip(f'install {name}=={version}'.split(' '))
            # os.system(f'{python_path} -m pip install {name}=={version}')
    elif pip_index:
        pip(f'install {name} -i {pip_index}'.split(' '))
        # os.system(f'{python_path} -m pip install {name} -i {pip_index}')
    else:
        pip(f'install {name}'.split(' '))
        # os.system(f'{python_path} -m pip install {name}')
    if nt_after_command and os.name == 'nt':
        after_command = nt_after_command
    elif posix_after_command and os.name == 'posix':
        after_command = posix_after_command
    if after_command:
        os.system(after_command.format('python', python_path))


def install_script(
        command=None,
        nt_command=None,
        posix_command=None
):
    """
    Run the script.
    :param posix_command: The command of the script on posix.
    :param nt_command: The command of the script on nt.
    :param command: The command of the script.
    :return: None
    """
    python_path = sys.executable
    if nt_command and os.name == 'nt':
        command = nt_command
    elif posix_command and os.name == 'posix':
        command = posix_command
    commands = command.split(' ')
    if commands[0] == 'python':
        commands[0] = f'{python_path}'
    elif commands[0] == 'pip':
        commands[0] = f'{python_path} -m pip'
    command = ' '.join(commands)
    os.system(command)


def install_file(
        path,
        command=None,
        nt_command=None,
        posix_command=None
):
    """
    Check if the file exists.
    :param posix_command: The command to be executed if the file not exists on posix.
    :param nt_command: The command to be executed if the file not exists on nt.
    :param command: The command to be executed if the file not exists.
    :param path: The path of the file.
    :return: True or False
    """
    if not os.path.exists(path):
        os.system(command)


def install(
        config_path,
        pip_index=None,
        lock_config=True
):
    """
    Install the packages listed in the configuration file.
    :param lock_config: Whether to lock the configuration file.
    :param pip_index: The index of pip.
    :param config_path: The path of the configuration file.
    :return: None
    """

    python_path = sys.executable

    # Check if the configuration file exists.
    if not os.path.exists(config_path):
        if os.path.exists(f'{config_path}.lock'):
            return None
        else:
            raise FileNotFoundError(f'File not found: {config_path}')

    # Check if the configuration file is "requirements.txt".
    if os.path.basename(config_path) == 'requirements.txt':
        # Install the packages listed in the configuration file.
        if pip_index:
            os.system(f"{python_path} -m pip install -r {config_path} -i {pip_index}")
        else:
            os.system(f'{python_path} -m pip install -r {config_path}')
        return None

    with open(config_path, 'r') as f:
        config = json.load(f)

    # Update pip index.
    if 'pip_index' in config and pip_index is None:
        pip_index = config['pip_index']

    # Update pip.
    pip_update(pip_index)

    if "packages" in config:
        # Install the packages listed in the configuration file.
        for package in config['packages']:
            if pip_index and 'pip_index' not in package:
                package['pip_index'] = pip_index
            install_package(**package)

    if "files" in config:
        # Check if the files listed in the configuration file exists.
        for file in config['files']:
            install_file(**file)

    if "scripts" in config:
        # Run the scripts listed in the configuration file.
        for script in config['scripts']:
            install_script(**script)

    if lock_config:
        os.rename(config_path, f'{config_path}.lock')
