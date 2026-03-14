import os

schema_get_files_info = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists the content of a file at the provided file path, providing up to 10000 characters of content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)





MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
        valid_file_path = os.path.commonpath([working_directory_abs, target_file]) == working_directory_abs
        if not valid_file_path:
            return f"Error: Cannot read \"{file_path}\" as it is outside the working directory"
        if not os.path.isfile(target_file):
            return f"Error: File not found or is not a regular file: \"{file_path}\""
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f"[...File \"{file_path}\" truncated at {MAX_CHARS}] characters]"
        return file_content_string
    except:
        return f"Error: Unable to execute get_file_content"

