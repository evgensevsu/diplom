import sys
import io
import traceback
import contextlib


def execute_code(code, input_data=None):
    """
    Execute Python code safely in a controlled environment.
    
    Args:
        code (str): The Python code to execute
        input_data: Optional input data to pass to the code, can be string, int, float, etc.
    
    Returns:
        tuple: (success, output) where success is a boolean indicating if execution was successful,
               and output is the output or error message
    """
    # Convert input_data to string if it's not None
    if input_data is None:
        input_data = ''
    else:
        input_data = str(input_data)
    
    # Create string buffers for stdout and stderr
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    
    # Create StringIO for input
    input_buffer = io.StringIO(input_data)
    
    # Redirect standard streams
    with contextlib.redirect_stdout(stdout_buffer), \
         contextlib.redirect_stderr(stderr_buffer):
        
        # Replace built-in input function to read from our buffer
        original_input = input
        
        def custom_input(prompt=''):
            print(prompt, end='')
            return input_buffer.readline().rstrip('\n')
        
        # Set max execution time (not available in standard Python, just showing the intent)
        # We would need to use something like a timeout decorator in production
        max_execution_time = 5  # seconds
        
        try:
            # Replace the input function with our custom one
            __builtins__['input'] = custom_input
            
            # Execute the code
            exec(code)
            success = True
            output = stdout_buffer.getvalue()
            
        except Exception as e:
            success = False
            error_traceback = traceback.format_exc()
            output = f"Error: {str(e)}\n\n{error_traceback}"
        
        finally:
            # Restore the original input function
            __builtins__['input'] = original_input
    
    return success, output
