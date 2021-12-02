from beet.library.data_pack import Function, FunctionTag
from beet.toolchain.context import Context

call = (
    'execute '
        'if score #smithed.actionbar.major load.status matches {major} '
        'if score #smithed.actionbar.minor load.status matches {minor} '
        'if score #smithed.actionbar.patch load.status matches {patch} '
        'run function {path}'
)

resolve_text = (
    'schedule clear smithed:actionbar/impl/{version}/technical/tick\n'
    'execute '
        'if score #smithed.actionbar.major load.status matches {major} '
        'if score #smithed.actionbar.minor load.status matches {minor} '
        'if score #smithed.actionbar.patch load.status matches {patch} '
        'run function smithed:actionbar/impl/{version}/technical/load'
)

enumerate_text = (
    'scoreboard players add #smithed.actionbar.major load.status 0\n'
    'scoreboard players add #smithed.actionbar.minor load.status 0\n'
    'scoreboard players add #smithed.actionbar.patch load.status 0\n'
    'function smithed:actionbar/calls/{version}/technical/enumerate/major\n'
    'scoreboard players reset #smithed.actionbar.set load.status\n'
)

major_text = (
    'execute '
        'if score #smithed.actionbar.major load.status matches ..{major} '
        'unless score #smithed.actionbar.major load.status matches {major} '
        'run function smithed:actionbar/calls/{version}/technical/enumerate/set_version\n'
    'execute '
        'if score #smithed.actionbar.major load.status matches ..{major} '
        'if score #smithed.actionbar.major load.status matches {major} '
        'unless score #smithed.actionbar.set load.status matches 1 '
        'run function smithed:actionbar/calls/{version}/technical/enumerate/minor'
)

minor_text = (
    'execute '
        'if score #smithed.actionbar.minor load.status matches ..{minor} '
        'unless score #smithed.actionbar.minor load.status matches {minor} '
        'run function smithed:actionbar/calls/{version}/technical/enumerate/set_version\n'
    'execute '
        'if score #smithed.actionbar.minor load.status matches ..{minor} '
        'if score #smithed.actionbar.minor load.status matches {minor} '
        'unless score #smithed.actionbar.set load.status matches 1 '
        'run function smithed:actionbar/calls/{version}/technical/enumerate/patch'
)

patch_text = (
    'execute '
        'if score #smithed.actionbar.patch load.status matches ..{patch} '
        'unless score #smithed.actionbar.patch load.status matches {patch} '
        'run function smithed:actionbar/calls/{version}/technical/enumerate/set_version'
)

set_version = (
    'scoreboard players set #smithed.actionbar.major load.status {major}\n'
    'scoreboard players set #smithed.actionbar.minor load.status {minor}\n'
    'scoreboard players set #smithed.actionbar.patch load.status {patch}\n'
    'scoreboard players set #smithed.actionbar.set load.status 1'
)

def beet_default(ctx: Context):
    version = ctx.template.globals['version'] = f'v{ctx.project_version}'
    major, minor, patch = version.replace('v', '').split('.')

    yield

    for container in ctx.data["smithed"].values():
        for path in list(container):
            container[path.replace("__version__", version)] = container.pop(path)

    for path in ctx.data.functions.match('impl'):
        first_line = ctx.data.functions[path].text.split('\n')[0]
        if first_line.startswith('#') and 'scorepublic' in first_line:
            generate_call(ctx, path, version)

    ctx.data[f'smithed:actionbar/calls/{version}/technical/resolve'] = Function(
        resolve_text.format(version=version, major=major, minor=minor, patch=patch)
    )

    ctx.data[f'smithed:actionbar/calls/{version}/technical/enumerate'] = Function(
        enumerate_text.format(version=version)
    )

    ctx.data[f'smithed:actionbar/calls/{version}/technical/enumerate/major'] = Function(
        major_text.format(version=version, major=major)
    )

    ctx.data[f'smithed:actionbar/calls/{version}/technical/enumerate/minor'] = Function(
        minor_text.format(version=version, minor=minor)
    )

    ctx.data[f'smithed:actionbar/calls/{version}/technical/enumerate/patch'] = Function(
        patch_text.format(version=version, patch=patch)
    )

    ctx.data[f'smithed:actionbar/calls/{version}/technical/enumerate/set_version'] = Function(
        set_version.format(version=version, major=major, minor=minor, patch=patch)
    )


def generate_call(ctx, path: str, version: str):
    print('  api:', '#smithed:actionbar/pub/' + path.split(version)[1][1:])
    major, minor, patch = version.replace('v', '').split('.')

    tag = {
        "values": []
    }

    tag['values'].append(path.replace('impl', 'calls'))

    ctx.data['smithed:actionbar/pub/' + path.split(version)[1][1:]] = FunctionTag(tag)
    ctx.data[path.replace('impl', 'calls')] = Function(call.format(major=major, minor=minor, patch=patch, path=path))