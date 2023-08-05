# wikme

`wikme` is a Python package that allows you to convert a folder of Markdown files into a simple wiki-style website. It supports parsing and converting wikilinks, both regular and with custom titles, and includes additional features like last edited date retrieved from git log or file modification timestamp, depending on your needs.

## Features

- Convert a folder of Markdown files into a simple wiki-style website
- Automatically handles wikilinks and converts them to HTML anchor tags
- Supports custom titles for wikilinks
- Detects last edited date, either from Git log or file modified timestamp
- Allows users to provide their own HTML templates for a customized look and feel

## Installation

You can install the package via pip:

```shell
pip install wikme
```

## Usage

You can use wikme package in your Python scripts as follows:

```python
from wikme import main

# Define input and output directories and the template file
input_folder = "./markdown_files/"
output_folder = "./generated_html/"
template_file = "./template.html"

main(input_folder, output_folder, template_file)
```

You can also use it as a command-line tool:

```shell
wikme --input "./markdown_files" --output "./generated_html" --template "./template.html"
```

## Arguments

- `--input`: Path to the input folder containing the Markdown files.
- `--output`: Path to the output folder where the generated HTML files will be saved.
- `--template`: Path to the HTML template file used for rendering the Markdown files.

## HTML Template

You can create a custom HTML template to style the generated files. The content of the Markdown files will be inserted into the designated placeholder.

An example template:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="pygment.css">
</head>
<body>
    <header>
        <h1>{{ title }}</h1>
    </header>
    <main>
        {{ content }}
    </main>
    <footer>
        <small>Last Edited: {{ last_edited }}</small>
    </footer>
</body>
</html>
```

Placeholders:

- `{{ title }}`: Will be replaced with the title of the Markdown file.
- `{{ content }}`: Will be replaced with the HTML converted content of the Markdown file.
- `{{ last_edited }}`: Will be replaced with the last edited date of the file.

## Wikilinks Syntax

Wikilinks are used to create links between pages within the generated wiki-style website. The `wikme` package supports several variations of wikilink syntax.

### Regular Wikilinks

- Standard wikilinks without custom titles: `[[Page Name]]`

This syntax will create a link to the specified page with the same text as the page name.

Example: `[[Home Page]]` creates a link to the "Home Page" with the text "Home Page".

- Wikilinks with custom titles: `[[Page Name|Custom Title]]`

This syntax allows you to create a link to a page with a custom display text for the link.

Example: `[[Home Page|Visit our home page]]` creates a link to the "Home Page" with the text "Visit our home page".

### Tilde-prefixed Wikilinks

These are useful when you want to link to files outside of the input folder or link to a different directory assuming you are on a pubnix or tilde server.

- Tilde-prefixed wikilinks without custom titles: `[[~path/to/page]]`

Example: `[[~docs/section-01]]` creates a link to the "/docs/section-01" page with the text "docs/section-01".

- Tilde-prefixed wikilinks with custom titles: `[[~path/to/page|Custom Title]]`

Example: `[[~docs/section-01|Section 1]]` creates a link to the "/docs/section-01" page with the text "Section 1".

### Notes

The parser will process the wikilinks within your Markdown files and convert them into the corresponding HTML anchor tags.

## Syntax Highlighting and CSS Generation

The `wikme` package uses the `markdown` library with the `codehilite` extension for syntax highlighting. This extension adds color highlighting to code blocks within your Markdown files, making it easier to read and understand code snippets.

### Syntax Highlighting in Markdown

To enable syntax highlighting for a code block, you can use the the 4 space indent syntax with a language identifier. Here's an example:

<pre>
Check out this code:

    #!python
    msg = "Hello, world"
    print(msg)

</pre>

In this example, the language identifier is `python`. This will tell the `codehilite` extension to apply syntax highlighting for the Python language to this code block.

You can use any language identifier supported by the `Pygments` library. A list of supported languages can be found in the [Pygments documentation](https://pygments.org/docs/lexers/).

### Generating CSS for Syntax Highlighting

The `codehilite` extension uses the `Pygments` library for syntax highlighting. To generate a CSS file for syntax highlighting, you can use the `pygmentize` command-line tool provided by the `Pygments` library.

First, ensure that you have the 'Pygments' library installed. You can install it using `pip`:

```shell
pip install pygments
```

Next, you can generate the CSS file with the following command:

```shell
pygmentize -S <style-name> -f html -a .codehilite > pygment.css
```

Replace `<style-name>` with the desired syntax highlighting style. Some popular style names include `default`, `monokai`, `vs`, and `xcode`. A list of available styles can be found in the [Pygments documentation](https://pygments.org/styles/).

This command generates a `pygment.css` file with the selected style applied to the `codehilite` class. You can include this CSS file in your HTML template to enable syntax highlighting for your generated wiki-style website.

## License

MD GPL