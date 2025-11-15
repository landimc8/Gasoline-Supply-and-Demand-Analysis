print("Python in VSCode is working!")
print("Let's analyze some gasoline data!")

# Test basic imports
try:
    import pandas as pd
    import matplotlib.pyplot as plt
    print("✓ Pandas and Matplotlib imported successfully!")
except ImportError as e:
    print(f"✗ Import error: {e}")