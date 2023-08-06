# blurhashify

[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)

Generate [BlurHash](https://github.com/woltapp/blurhash) images from an existing image.

## Installation

Via [pip](https://github.com/pypa/pip):

```bash
pip install blurhashify
```

Via [pipx](https://github.com/pypa/pipx):

```bash
pipx install blurhashify
```

## Usage

```bash
blurhashify
```

and

```text
Usage: blurhashify [OPTIONS] FILE_PATH

  Generate BlurHash images from an existing image.

Options:
  -w, --width INTEGER   The width of the output images (in px).  [default: input image
                        width]
  -h, --height INTEGER  The height of the output images (in px).  [default: input
                        image height]
  -s, --scale INTEGER   The number to multiply the width and height of the output
                        images by.  [default: 1]
  -p, --punch INTEGER   The punch of output images. This design option adjusts the
                        contrast in output images. Smaller values make the effect more
                        subtle, while larger values make it stronger.  [default: 1]
  -v, --verbose         Enable verbose logging.
  --version             Show the version and exit.
  --help                Show this message and exit.
```

## References

- https://github.com/woltapp/blurhash
- https://github.com/halcy/blurhash-python
- https://github.com/woltapp/blurhash-python
- https://github.com/joaopalmeiro/flake8-import-as-module
- https://python-poetry.org/docs/dependency-specification/#exact-requirements + https://github.com/python-poetry/poetry/issues/1440#issuecomment-1105165877
- https://dataewan.com/blog/poetry-python-command-line/
- https://github.com/alvarobartt/python-package-template
- https://github.com/ofek/hatch-vcs
- https://github.com/aka-raccoon/hatch-aws
- https://hatch.pypa.io/latest/blog/2022/10/08/hatch-v160/#virtual-environment-location + https://github.com/pypa/hatch/issues/715

## Development

VS Code profile: [Python](https://github.com/joaopalmeiro/vscode-profiles/tree/main/Python)

```bash
hatch config set dirs.env.virtual .hatch
```

```bash
hatch config show --all
```

```bash
hatch env create dev
```

```bash
hatch env find
```

```bash
hatch env show
```

```bash
hatch version
```

```bash
hatch -e dev run pip show blurhashify
```

```bash
hatch -e dev run blurhashify --help
```

```bash
hatch -e dev run blurhashify 06_IMG_1974.jpg
```

or

```bash
hatch -e dev run blurhashify 06_IMG_1974.jpg --verbose
```

```bash
hatch run dev:check
```

Copy the output of the help command and paste it in the [Usage](#usage) section.

## Deployment

```bash
hatch project metadata
```

```bash
hatch version
```

```bash
git tag
```

```bash
git ls-remote --tags origin
```

```bash
hatch version micro
```

or

```bash
hatch version minor
```

```bash
git tag "v$(hatch version)"
```

```bash
git tag
```

```bash
git push origin --tags
```
