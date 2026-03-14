import os
import subprocess

schema_get_files_info = types.FunctionDeclaration(
    name="run_python_file",
    description="Lists the content of a file at the provided file path, providing up to 10000 characters of content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Additional arguments to be passed to the python file that will be ran"
            )
        },
    ),
)



def run_python_file(working_directory, file_path, args=None):
    try:
        working_directory_abs = os.path.abspath(working_directory)
  #      return "Built Working Directory"
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
 #       return "Built Target File"
        valid_file_path = os.path.commonpath([working_directory_abs, target_file]) == working_directory_abs
        if not valid_file_path:
            return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
        if not os.path.isfile(target_file):
            return f"Error: \"{file_path}\" does not exist or is not a regular file"
        if not file_path[-3:] == ".py":
            return f"Error: \"{file_path}\" is not a Python file"
        
        command = ["python", target_file]
  #      return "COMMAND BUILT"
    
        if not args == None:
            command.extend(args)
 #       return("ABOUT TO RUN SUBPROCESS")
        result = subprocess.run(
            command,
            cwd=working_directory_abs,
            capture_output=True,
            text=True,
            timeout=30
        )
 #       return ("RESULT OBTAINED")
        if not result.returncode == 0:
            return f"Error: executing Python file: \"{file_path}\""
        
        return_string = ""
  #      return ("Return String started")
        if result.stdout == "":
            return_string += "No output produced.\n"
        else:
            return_string += f"STDOUT: {result.stdout}\n"
        
        if result.stderr == "":
            return_string += "No output produced. \n"
        else:
            return_string += f"STDERR: {result.stderr}\n"
        return return_string
    except:
        return f"Error: excuting python file: \"{file_path}\""
    
    

    

    
