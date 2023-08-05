import os
import re
import argparse
import markdown
import datetime
import subprocess
import shutil
from typing import Optional

def kebab_case(s: str) -> str:
    return re.sub(r"[ _]", "-", s).lower()

def get_title(filename: str, content: Optional[str] = None) -> str:
    if content:
        # Check for a top-level header in the content
        top_level_header = re.search(r"^#\s(.+)$", content, re.MULTILINE)
        if top_level_header:
            return top_level_header.group(1).strip()

    # Extract the inferred title from the filename
    title = filename.replace(".md", "").replace("_", " ")
    return title.capitalize()

def parse_wikilinks(content: str) -> str:
    # Convert wikilinks with tildes and custom titles
    content = re.sub(r'\[\[(~[^|\]]+?)\|([^|\]]+?)\]\]', r'<a href="/\1">\2</a>', content)

    # Convert wikilinks with tildes and without custom titles
    content = re.sub(r'\[\[(~[^|\]]+?)\]\]', r'<a href="/\1">\1</a>', content)

    # Convert regular wikilinks with custom titles
    content = re.sub(r'\[\[([^~|\]]+?)\|([^~|\]]+?)\]\]', lambda match: f'<a href="./{kebab_case(match.group(1))}.html">{match.group(2)}</a>', content)

    # Convert regular wikilinks without custom titles
    content = re.sub(r'\[\[([^~|\]]+?)\]\]', lambda match: f'<a href="./{kebab_case(match.group(1))}.html">{match.group(1)}</a>', content)

    return content

def render_template(template: str, title: str, content: str, last_edited: str) -> str:
    # Insert title, content, and last_edited into the template
    rendered = template.replace("{{ title }}", title)
    rendered = rendered.replace("{{ content }}", content)
    rendered = rendered.replace("{{ last_edited }}", last_edited)
    return rendered

def get_last_edited(path: str) -> str:
    try:
        # Attempt to get the last Git commit date of the file
        last_edited = subprocess.check_output(
            ["git", "log", "-1", "--format=%cd", "--date=local", path])
        return last_edited.decode("utf-8").strip()
    except Exception:
        # Fallback to the file's modified timestamp
        return str(datetime.datetime.fromtimestamp(os.path.getmtime(path)))

def main(input_folder: str, output_folder: str, template_file: str):
    # Load the template
    with open(template_file, "r") as template_f:
        template = template_f.read()

    # Go through each markdown file
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".md"):
                # Process the markdown file
                input_file = os.path.join(root, file)
                output_subfolder = os.path.join(
                    output_folder, os.path.relpath(root, input_folder))
                output_file = os.path.join(
                    output_subfolder, f"{kebab_case(file.replace('.md', ''))}.html")

                # Read the source file
                with open(input_file, "r") as source:
                    markdown_content = source.read()
                    html_content = markdown.markdown(
                        parse_wikilinks(markdown_content), extensions=['codehilite']
                    )

                # Create the output folder if needed
                if not os.path.exists(output_subfolder):
                    os.makedirs(output_subfolder)

                # Render the result
                title = get_title(file, markdown_content)
                last_edited = get_last_edited(input_file)
                rendered_content = render_template(template, title, html_content, last_edited)

                # Save the rendered HTML file
                with open(output_file, "w") as output_f:
                    output_f.write(rendered_content)

def cmd():
    parser = argparse.ArgumentParser(
        description="Convert a folder of Markdown files into a simple wiki-style website.")
    parser.add_argument('--input', dest='input_folder',
                        required=True, help='input folder containing Markdown files')
    parser.add_argument('--output', dest='output_folder',
                        required=True, help='output folder for generated HTML files')
    parser.add_argument('--template', dest='template_file',
                        required=True, help='HTML template for the generated files')
    args = parser.parse_args()

    main(args.input_folder, args.output_folder, args.template_file)

if __name__ == "__main__":
    cmd()