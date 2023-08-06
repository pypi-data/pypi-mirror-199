import openai
from dotenv import load_dotenv
import os
import tiktoken

from create_doc.utils import check_output_path


def init_env():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    return openai.api_key


def load_text(filepath):
    """
    Load text from the given file path.

    Args:
        filepath (str): The file path of the text.

    Returns:
        str: The content of the text.
    """
    with open(filepath, "r") as f:
        text = f.read()
    return text


def chat_gpt_conversation(conversation, model_id):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )
    api_usage = response['usage']
    print('Token consumed: {0}'.format(api_usage['total_tokens']))
    token_consumed = api_usage['total_tokens']
    # stop means complete
    # print(response['choices'][0].finish_reason)
    # print(response['choices'][0].index)
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return {'conversation': conversation, 'tokens_consumed': token_consumed}


def init_gpt_with_config_prompts(gpt_prompts):
    _conversation = []
    for gpt_prompt in gpt_prompts:
        content_file_path = gpt_prompt.get('content_file_path')
        prompt_content = ""
        if content_file_path:
            prompt_content = load_text(content_file_path)
        else:
            prompt_content = gpt_prompt.get('content')

        role = gpt_prompt.get('role', 'system')
        if prompt_content and len(prompt_content) > 0:
            _conversation.append({'role': role, 'content': prompt_content})

    return _conversation


def num_tokens_from_messages(messages, model):
    """
    Returns the number of tokens used by a list of messages.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo" or model == "gpt-4":  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
        See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")


def traverse_directory(directory_path):
    directories = [d for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d))]
    return directories


def get_all_files_in_directory_and_subdirectories(directory, file_extensions):
    # get all files in directory and its subdirectories with the given file_filter
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            # check if python string ends with a string defined in array file_extensions
            if file.endswith(tuple(file_extensions)):
                file_list.append(os.path.join(root, file))
    return file_list


def open_content_markdown(output_path, content_title):
    # create path from root_path and directory_path
    check_output_path(output_path)
    output_file = os.path.join(output_path, 'content.md')
    # if output_file exists, delete it
    if os.path.exists(output_file):
        os.remove(output_file)
    # open output file for text writing
    output_file = open(output_file, 'w')
    # write markdown text
    output_file.write('# ' + content_title + '\n')
    return output_file


def close_content_markdown(output_file):
    output_file.close()


def add_dependency_markdown(output_file, directory_path):
    # write markdown text
    output_file.write('[[' + directory_path + '-module-dependency|' + directory_path + ']]\n\n')


def open_component_markdown(output_path, directory_path):
    # create path from root_path and directory_path
    check_output_path(output_path)
    output_file = os.path.join(output_path, directory_path + '.md')
    print('Creating markdown file: ' + output_file + '...')
    # if output_file exists, delete it
    if os.path.exists(output_file):
        os.remove(output_file)
    # open output file for text writing
    output_file = open(output_file, 'w')
    # write markdown text
    return output_file


def add_to_component_markdown(output_file, text):
    output_file.write(text + '\n\n')


def close_component_markdown(output_file):
    # close output file
    print('Closing markdown file...')
    output_file.close()


def create_title_for_file(file_path):
    # get file name
    file_name = os.path.basename(file_path)
    # remove extension
    file_name = os.path.splitext(file_name)[0]
    # replace _ with space
    file_name = file_name.replace('_', ' ')
    file_name = file_name.replace('.', ' ')

    # if file_name.endswith('.component'):
    #     file_name = file_name[:-len('.component')]
    # if file_name.endswith('.model'):
    #     file_name = file_name[:-len('.model')]
    # if file_name.endswith('.service'):
    #     file_name = file_name[:-len('.service')]

    # capitalize
    file_name = file_name.capitalize()
    return file_name


def create_filename_for_title(title):
    # replace space with _
    file_name = title.replace(' ', '_')
    # lowercase
    file_name = file_name.lower()
    return file_name


def analyze_files(_project_root_directory, _input_directory, _output_directory, _model_id, _model_token_limit,
                  _gpt_prompts, _skip_router_outlet, _skip_router_outlet_text, _content_title, _file_extensions,
                  _add_dependency_link, _add_file_path, _dependency_link_text
                  ):
    directories = traverse_directory(_input_directory)
    # if length of directories is 0, add _input_directory to directories
    process_directories = True
    if len(directories) == 0:
        directories.append(_input_directory)
        process_directories = False

    # sort directories
    directories.sort()
    content_file = open_content_markdown(_output_directory, _content_title)

    if _add_dependency_link and _dependency_link_text is not None and len(_dependency_link_text) > 0:
            _dependency_link_text = _dependency_link_text + ':'

    total_tokens = 0

    for directory in directories:
        print('Processing directory: {0} ----------------------'.format(directory))
        file_list = get_all_files_in_directory_and_subdirectories(
            os.path.join(_input_directory, directory),
            _file_extensions)
        # if file list is not empty, process files
        if file_list:
            print('Processing files: ')
            file_list.sort()
            description_file = None
            if process_directories:
                description_file = open_component_markdown(_output_directory, directory)
                add_dependency_markdown(content_file, directory)
                add_to_component_markdown(description_file, '# ' + directory + '\n\n')
                if _add_dependency_link:
                    add_to_component_markdown(description_file,
                                              _dependency_link_text +  '[[' + directory + '-module-dependency|' +
                                              directory + ']]\n\n')

            for file in file_list:
                # create relative file path from project root directory and file
                print(file)
                title = create_title_for_file(file)
                print(title)
                file_relative_path = os.path.relpath(file, _project_root_directory)
                if not process_directories:
                    file_name = create_filename_for_title(title)
                    description_file = open_component_markdown(_output_directory, file_name)
                    add_dependency_markdown(content_file, file_name)
                    add_to_component_markdown(description_file, '# ' + title + '\n')
                    if _add_file_path:
                        add_to_component_markdown(description_file, 'File: **' + file_relative_path + '**\n')

                    if _add_dependency_link:
                        add_to_component_markdown(description_file,
                                                  _dependency_link_text + '[[' + directory + '-module-dependency|'
                                                  + directory + ']]\n\n')

                file_text = load_text(file)
                # if file_text contains string <router-outlet> show message that this component contains router-outlet
                if '<router-outlet>' in file_text:
                    add_to_component_markdown(description_file, '# ' + title + '\n\n')

                    add_to_component_markdown(description_file, 'File: **' + file_relative_path + '**\n')
                    add_to_component_markdown(description_file, _skip_router_outlet_text)
                else:
                    conversation = init_gpt_with_config_prompts(_gpt_prompts)
                    conversation.append({'role': 'user', 'content': file_text})
                    num_tokens = num_tokens_from_messages(conversation, _model_id)
                    if num_tokens <= _model_token_limit:
                        result = chat_gpt_conversation(conversation, _model_id)
                        print('----------------------')
                        print('{0}\n'.format(result['conversation'][-1]['content'].strip()))

                        if process_directories:
                            add_to_component_markdown(description_file, '## ' + title + '\n\n')
                            if _add_file_path:
                                add_to_component_markdown(description_file, 'File: **' + file_relative_path + '**\n')

                        add_to_component_markdown(description_file, result['conversation'][-1]['content'].strip())
                        total_tokens += result['tokens_consumed']
                    else:
                        add_to_component_markdown(description_file,
                                                  '## Error processing file: {0} - too many tokens consumed: {1}'
                                                  .format(file, num_tokens))

            close_component_markdown(description_file)
    close_content_markdown(content_file)
    print('Total tokens consumed: {0}'.format(total_tokens))
    return 0
