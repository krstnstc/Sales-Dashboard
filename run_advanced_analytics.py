import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os

def run_notebook(notebook_path):
    """Execute a Jupyter notebook and save the output."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    # Configure the notebook execution
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    
    try:
        # Execute the notebook
        ep.preprocess(nb, {'metadata': {'path': os.path.dirname(notebook_path)}})
        
        # Save the executed notebook
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        
        print(f"Successfully executed {notebook_path}")
        return True
    except Exception as e:
        print(f"Error executing {notebook_path}: {str(e)}")
        return False

if __name__ == "__main__":
    # Run the advanced analytics notebook
    notebook_path = os.path.join('notebooks', '02_advanced_analytics.ipynb')
    if os.path.exists(notebook_path):
        print(f"Running {notebook_path}...")
        success = run_notebook(notebook_path)
        
        if success:
            print("\nAdvanced analytics completed successfully!")
            print("You can now proceed to explore the Power BI dashboard.")
        else:
            print("\nThere was an error during advanced analytics. Please check the error messages above.")
    else:
        print(f"Error: {notebook_path} not found.")
