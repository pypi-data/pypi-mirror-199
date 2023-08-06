import os


def traverse_directory(directory_path):
    directories = [d for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d))]
    return directories


def generate_dependency_graph_for_directory_in_svg(root_path, directory_path, output_path):
    # create path from root_path and directory_path
    work_path = os.path.join(root_path, directory_path)
    output_file = os.path.join(output_path, directory_path + '.svg')
    # execute os command to generate svg file
    os.system('cd ' + root_path + ' && npx depcruise src --include-only "^src" --focus ' + directory_path +
              ' --config --output-type ddot | dot -T svg > ' + output_file)


def generate_summary_dependency_graph_for_directory_in_svg(root_path, output_path):
    # create path from root_path and directory_path
    output_file = os.path.join(output_path, 'summary-dependency-graph.svg')
    # execute os command to generate svg file
    print('cd ' + root_path + ' && npx depcruise src --include-only "^src" --max-depth 1 ' +
          ' --config --output-type ddot | dot -T svg > ' + output_file)
    os.system('cd ' + root_path + ' && npx depcruise src --include-only "^src" --max-depth 1 ' +
              ' --config --output-type ddot | dot -T svg -Grankdir=TD > ' + output_file)


def generate_summary_dependency_graph_for_directory_in_html(root_path, output_path):
    # create path from root_path and directory_path
    output_file = os.path.join(output_path, 'summary-dependency-graph.html')
    # execute os command to generate svg file
    print('cd ' + root_path + ' && npx depcruise src --include-only "^src" --max-depth 1 ' +
          ' --config --output-type ddot | dot -T svg > ' + output_file)
    os.system('cd ' + root_path + ' && npx depcruise src --include-only "^src" --max-depth 1 ' +
              ' --config --output-type ddot | dot -T svg | npx depcruise-wrap-stream-in-html > ' + output_file)


def generate_dependency_graph_for_directory_in_html(root_path, directory_path, output_path):
    # create path from root_path and directory_path
    output_file = os.path.join(output_path, directory_path + '.html')
    # execute os command to generate svg file
    os.system('cd ' + root_path + ' && npx depcruise src --include-only "^src" --focus ' + directory_path +
              ' --config --output-type dot | dot -T svg | npx depcruise-wrap-stream-in-html > ' + output_file)


def generate_dependency_markdown(output_path, directory_path, svg_file_path, html_file_path):
    # create path from root_path and directory_path
    output_file = os.path.join(output_path, directory_path + '-module-dependency.md')
    # if output_file exists, delete it
    if os.path.exists(output_file):
        os.remove(output_file)
    # open output file for text writing
    output_file = open(output_file, 'w')
    # write markdown text
    output_file.write('# ' + directory_path + ' module dependency\n\n')
    output_file.write('[[' + directory_path + '.html|' + directory_path + ' details]]\n\n')
    output_file.write('![[' + directory_path + '.svg]]\n\n')
    # close output file
    output_file.close()


def open_content_markdown(output_path):
    # create path from root_path and directory_path
    output_file = os.path.join(output_path, 'Module-dependencies.md')
    # if output_file exists, delete it
    if os.path.exists(output_file):
        os.remove(output_file)
    # open output file for text writing
    output_file = open(output_file, 'w')
    # write markdown text
    output_file.write('# Module dependencies\n\n')
    return output_file


def close_content_markdown(output_file):
    output_file.write('![[summary-dependency-graph.svg]]\n')
    output_file.write('[[summary-dependency-graph.html]]\n')
    output_file.close()


def add_dependency_markdown(output_file, directory_path):
    # write markdown text
    output_file.write('[[' + directory_path + '-module-dependency|'+ directory_path + ']]\n')


def process_directory_dependencies(root_path, webapp_directory_path, output_path):
    # traverse webapp directory
    init_dependecy_cruiser(root_path)
    directories = traverse_directory(webapp_directory_path)
    directories.sort()

    generate_summary_dependency_graph_for_directory_in_svg(root_path, output_path)
    generate_summary_dependency_graph_for_directory_in_html(root_path, output_path)

    for directory in directories:
        # generate dependency graph for directory
        generate_dependency_graph_for_directory_in_svg(root_path, directory, output_path)
        generate_dependency_graph_for_directory_in_html(root_path, directory, output_path)
        # generate markdown file for dependency graph
        generate_dependency_markdown(output_path, directory, directory + '.svg', directory + '.html')

    return 0

def init_dependecy_cruiser(root_path):
    # check root_path to see if .dependency-cruiser.js exists
    if not os.path.exists(os.path.join(root_path, '.dependency-cruiser.js')):
        # if not, execute os command to generate .dependency-cruiser.js
        print('Initialize dependency cruiser:')
        os.system('cd ' + root_path + ' && npx depcruise --init')


