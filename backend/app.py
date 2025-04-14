import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

OUTPUT_DIR = os.path.join(os.getcwd(), "static")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def execute_python_code(code):
    """
    Executes the provided Python code.
    The code must generate a visualization and save it as a file.
    For static images (matplotlib) use plt.savefig() and for interactive HTML outputs (Plotly),
    use pyo.plot(). The filename provided by the user will be interpreted as relative to OUTPUT_DIR.
    """
    import os

    safe_globals = {"__builtins__": __builtins__}

    try:
        import matplotlib.pyplot as plt
        orig_savefig = plt.savefig

        def new_savefig(fname, *args, **kwargs):
            if not os.path.isabs(fname):
                fname_new = os.path.join(OUTPUT_DIR, fname)
            else:
                fname_new = fname
            safe_globals["__final_fname__"] = fname_new
            return orig_savefig(fname_new, *args, **kwargs)

        plt.savefig = new_savefig
        safe_globals["plt"] = plt
    except Exception as e:
        return None, "Error importing matplotlib: " + str(e)

    try:
        import plotly.offline as pyo
        orig_plot = pyo.plot

        def new_plot(fig, filename, *args, **kwargs):
            if not os.path.isabs(filename):
                filename_new = os.path.join(OUTPUT_DIR, filename)
            else:
                filename_new = filename
            safe_globals["__final_fname__"] = filename_new
            kwargs.pop("auto_open", None)
            return orig_plot(fig, filename=filename_new, auto_open=False, *args, **kwargs)

        pyo.plot = new_plot
        safe_globals["pyo"] = pyo
    except Exception as e:
        pass

    try:
        exec(code, safe_globals)
    except Exception as e:
        return None, f"Python execution error: {str(e)}"

    if "__final_fname__" not in safe_globals:
        return None, ("Visualization not generated. Please ensure your code includes "
                      "a call to plt.savefig() or pyo.plot().")
    
    final_fname = safe_globals["__final_fname__"]
    if not os.path.exists(final_fname):
        return None, ("Visualization not generated. File not found at " + final_fname)

    return os.path.basename(final_fname), None


def execute_r_code(code):
    """
    Executes the provided R code using Rscript.
    The code must generate a visualization and save it as a file.
    It is expected that the code uses the provided variable 'output_file' for saving.
    
    The function detects if the visualization is interactive (HTML output)
    by checking for keywords in the code and then chooses an appropriate file extension.
    
    IMPORTANT:
    - Do not reassign 'output_file' in your R code. Just specify the file name.
    - The output file will be stored in the OUTPUT_DIR (i.e. the static folder).
    """
    import os, uuid, subprocess, re

    # Define OUTPUT_DIR as the static folder in the project root and ensure it exists.
    OUTPUT_DIR = os.path.join(os.getcwd(), "static")
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Determine file extension:
    # Use ".html" if the code involves htmlwidgets or saveWidget (for interactive outputs)
    # Otherwise, default to ".png" for static images.
    if "htmlwidgets" in code or "saveWidget" in code:
        extension = ".html"
    else:
        extension = ".png"

    # Generate a unique filename and the full path where the file will be stored in OUTPUT_DIR.
    filename = f"{uuid.uuid4().hex}{extension}"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Prevent the user from reassigning output_file in their code.
    if "output_file <-" in code:
        return None, "Do not reassign 'output_file' in your R code. Just specify the file name."

    # Replace any literal assignment for filename= or file= with output_file.
    modified_code = re.sub(r'filename\s*=\s*["\'].*?["\']', 'filename=output_file', code)
    modified_code = re.sub(r'file\s*=\s*["\'].*?["\']', 'file=output_file', modified_code)

    # Prepend the user's (modified) code with an assignment for output_file so that the file is saved to OUTPUT_DIR.
    code_with_filepath = f"output_file <- '{filepath.replace(os.sep, '/')}'\n" + modified_code + "\n"

    # Create a temporary directory for the R script if it does not exist.
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    temp_r_file = os.path.join(temp_dir, f"{uuid.uuid4().hex}.R")

    with open(temp_r_file, "w") as f:
        f.write(code_with_filepath)

    try:
        result = subprocess.run(["Rscript", temp_r_file], capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return None, "R execution error: " + result.stderr
    except Exception as e:
        return None, "Error executing R code: " + str(e)
    finally:
        if os.path.exists(temp_r_file):
            os.remove(temp_r_file)

    if not os.path.exists(filepath):
        return None, ("Visualization not generated. Please ensure your R code writes the image or widget " 
                      "to the file path provided by output_file.")

    return filename, None


@app.route('/api/visualize', methods=['POST'])
def visualize():
    data = request.get_json()
    language = data.get("language", "").lower()
    code = data.get("code", "")
    
    if not language or not code:
        return jsonify({"error": "Please provide both language and code."}), 400
    
    if language == "python":
        filename, error = execute_python_code(code)
    elif language == "r":
        filename, error = execute_r_code(code)
    else:
        return jsonify({"error": "Unsupported language. Please choose Python or R."}), 400
        
    if error:
        return jsonify({"error": error}), 400
        
    file_url = request.host_url + "static/" + filename
    return jsonify({"file_url": file_url})

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(OUTPUT_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)
