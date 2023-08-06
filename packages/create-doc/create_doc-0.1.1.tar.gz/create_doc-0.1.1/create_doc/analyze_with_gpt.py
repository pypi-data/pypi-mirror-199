import openai
from dotenv import load_dotenv
import os
import tiktoken


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
    return { 'conversation': conversation, 'tokens_consumed': token_consumed }


def init_gpt_html_data_extraction(gpt_prompt):
    return [{'role': 'system',
             'content': gpt_prompt
             }]


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


def get_all_files_in_directory_and_subdirectories(directory, file_filter):
    # get all files in directory and its subdirectories with the given file_filter
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(file_filter):
                file_list.append(os.path.join(root, file))
    return file_list


def check_output_path(output_path):
    # check if output_path exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)


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
    output_file = os.path.join(output_path, directory_path + '.md')
    # if output_file exists, delete it
    if os.path.exists(output_file):
        os.remove(output_file)
    # open output file for text writing
    output_file = open(output_file, 'w')
    # write markdown text
    output_file.write('# ' + directory_path + '\n\n')
    output_file.write(
        'Prikaz strukture komponente:[[' + directory_path + '-module-dependency|' + directory_path + ']]\n\n')
    return output_file


def add_to_component_markdown(output_file, text):
    output_file.write(text + '\n\n')


def close_component_markdown(output_file):
    # close output file

    output_file.close()


def create_title_for_file(file_path):
    # get file name
    file_name = os.path.basename(file_path)
    # remove extension
    file_name = os.path.splitext(file_name)[0]
    # replace _ with space
    file_name = file_name.replace('_', ' ')
    # if file name ends with '.component', remove it
    if file_name.endswith('.component'):
        file_name = file_name[:-len('.component')]
    # capitalize
    file_name = file_name.capitalize()
    return file_name


def analyze_html_files(_project_root_directory, _input_directory, _output_directory, _model_id, _model_token_limit,
                       _gpt_prompt, _skip_router_outlet, _skip_router_outlet_text, _content_title):
    directories = traverse_directory(_input_directory)
    # sort directories
    directories.sort()
    content_file = open_content_markdown(_output_directory, _content_title)

    total_tokens = 0
    for directory in directories:
        print('Processing directory: {0} ----------------------'.format(directory))
        file_list = get_all_files_in_directory_and_subdirectories(os.path.join(_input_directory, directory), '.html')
        # if file list is not empty, process files
        if file_list:
            print('Processing files: ')
            description_file = open_component_markdown(_output_directory, directory)
            add_dependency_markdown(content_file, directory)
            for file in file_list:
                # create relative file path from project root directory and file
                file_relative_path = os.path.relpath(file, _project_root_directory)

                print(file)
                title = create_title_for_file(file)
                print(title)
                file_text = load_text(file)
                # if file_text contains string <router-outlet> show message that this component contains router-outlet
                if '<router-outlet>' in file_text:
                    add_to_component_markdown(description_file, '## ' + title + '\n\n')
                    add_to_component_markdown(description_file, 'File: **' + file_relative_path + '**\n')
                    add_to_component_markdown(description_file, _skip_router_outlet_text)
                else:
                    conversation = init_gpt_html_data_extraction(_gpt_prompt)
                    conversation.append({'role': 'user', 'content': file_text})
                    num_tokens = num_tokens_from_messages(conversation, _model_id)
                    if num_tokens <= _model_token_limit:
                        result = chat_gpt_conversation(conversation, _model_id)
                        print('----------------------')
                        print('{0}\n'.format(result['conversation'][-1]['content'].strip()))

                        add_to_component_markdown(description_file, '# ' + title + '\n\n')
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
