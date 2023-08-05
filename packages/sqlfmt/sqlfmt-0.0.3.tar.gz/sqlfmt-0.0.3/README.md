<div align="center">
    <h1>SQLFMT</h1>
    <p><strong>SQLFMT</strong> - <em>An uncompromising SQL query formatter.</em></p>
</div>

<div align="center">
    <a href="https://pypi.org/project/sqlfmt/"><img alt="PyPI Latest Release" src="https://img.shields.io/pypi/v/sqlfmt.svg"></a>
    <a href="https://pypi.org/project/sqlfmt/"><img alt="Package Status" src="https://img.shields.io/pypi/status/sqlfmt.svg"></a>
    <a href="https://github.com/psf/black/"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
    <a href="https://pycqa.github.io/isort/"><img alt="Imports: isort" src="https://img.shields.io/badge/%20imports-isort-%231674b1"></a>
</div>

SQLFMT is an uncompromising SQL query formatter, which provides one and only one way to format the SQL query. Our goal is to make code reviews faster by producing the smallest diffs possible. You will save time and mental energy on more important matters.

*Please note this project is still in the planning stage and everything may be changed in the future.*

## How to install SQLFMT?

You can install SQLFMT from [Python Package Index](https://pypi.org/project/sqlfmt/):

```sh
pip install sqlfmt
```

## How to use SQLFMT?

Given a SQL file, you can simply use the following command to format it:

```sh
sqlfmt path/to/file.sql
```

You can install completion for a specfic shell:

```sh
sqlfmt --install-completion bash
```

You can also run the following command to find more other options:

```sh
sqlfmt --help
```

## How does SQLFMT work?

It *formats* your SQL code in place.

For example, if you have a file containing the following SQL code:

```sql
SeLEct  1, blah as  fOO  from myTable
```

after running SQLFMT, the content of that file will become:

```sql
SELECT
  1,
  blah AS foo
FROM mytable
```
