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


def show_shell(shell: str, shells: list[str]):
    for shell_iter in shells:
        if shell in shell_iter.lower():
            return True
    return False


def get_template_names(template_fnames: list[str], shells: list[str]) -> list[str]:
    want_bash = show_shell("bash", shells)
    want_powershell = show_shell("powershell", shells)

    filtered_template_fnames = []
    for fname in template_fnames:
        path = pathlib.Path(fname)
        path_tmp = path.stem.replace(".j2", "")
        _logger.debug(f"{path_tmp=}")
        if want_bash and path_tmp.lower().endswith("sh"):
            filtered_template_fnames.append(fname)
        if want_powershell and path_tmp.lower().endswith("ps1"):
            filtered_template_fnames.append(fname)

    return filtered_template_fnames


def main(args):
    template_fnames = [
        "bash1.sh.j2",
        "pwsh.ps1.j2",
        "github-bash.sh.j2",
        "keychain.sh.j2",
    ]

    shells = args.shells
    filtered_template_fnames = get_template_names(template_fnames, shells)

    vfile = io.StringIO()
    vfile.write("#" + "-" * 10)
    vfile.write("\n")
    for fname in filtered_template_fnames:
        template = env.get_template(fname)
        rendered = template.render(data={"variables": args.variables})
        trimmed = rendered.strip()
        out = f"{trimmed}\n"
        vfile.write(out)
        vfile.write("\n")

    print(vfile.getvalue(), end="")
    _logger.info("Script ends here")
