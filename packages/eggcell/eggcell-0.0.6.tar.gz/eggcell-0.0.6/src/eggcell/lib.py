import dataclasses
import io
import logging
import pathlib

import jinja2
import pkg_resources

_logger = logging.getLogger(__name__)

package = __name__.split(".")[0]
TEMPLATES_PATH = pathlib.Path(pkg_resources.resource_filename(package, "templates/"))
loader = jinja2.FileSystemLoader(searchpath=TEMPLATES_PATH)
env = jinja2.Environment(loader=loader, keep_trailing_newline=True)


@dataclasses.dataclass
class Shell:
    name: str
    want: bool
    extension: str


def want_shell(shell_name: str, shells: list[str]):
    for shell_iter in shells:
        if shell_name in shell_iter.lower():
            return True
    return False


def get_shell_preferences(shell_names: list[str]) -> bool:
    shells = []

    name = "bash"
    s = Shell(name, want_shell(name, shell_names), extension="sh")
    shells.append(s)

    name = "powershell"
    s = Shell(name, want_shell(name, shell_names), extension="ps1")
    shells.append(s)

    return shells


def get_template_names(
    shells: list[Shell], template_fnames: list[str], shell_names: list[str]
) -> list[str]:

    filtered_template_fnames = []
    for shell in shells:
        _logger.debug(type(shell))
        for fname in template_fnames:
            path = pathlib.Path(fname)
            path_tmp = path.stem.replace(".j2", "")
            _logger.debug(f"{path_tmp=}")

            if shell.want and path_tmp.lower().endswith(shell.extension):
                filtered_template_fnames.append(fname)

    return filtered_template_fnames


def render_templates_with_header(templates: list[str], template_data: dict) -> str:
    vfile = io.StringIO()
    vfile.write("#" + "-" * 10)
    vfile.write("\n")
    for fname in templates:
        template = env.get_template(fname)
        rendered = template.render(data=template_data)
        trimmed = rendered.strip()
        out = f"{trimmed}\n"
        vfile.write(out)
        vfile.write("\n")

    return vfile.getvalue()


def main(args):
    template_fnames = [
        "bash1.sh.j2",
        "pwsh.ps1.j2",
        "awscli.sh.j2",
        "github-bash.sh.j2",
        "keychain.sh.j2",
    ]

    shell_names = args.shells
    shells = get_shell_preferences(shell_names)
    filtered_template_fnames = get_template_names(shells, template_fnames, shell_names)
    user_variables = args.variables
    data = {"variables": user_variables}
    out = render_templates_with_header(
        templates=filtered_template_fnames, template_data=data
    )
    print(out)
    _logger.info("Script ends here")
