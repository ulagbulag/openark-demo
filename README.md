# OpenARK Python Demo Server

You can conveniently experience various features of MobileX
and learn how to use the Python API to implement each feature.

## Requirements

- [OpenARK](https://github.com/ulagbulag/OpenARK/tree/master/templates/bootstrap)
- Python
  - Install with your package manager
  - Install with Anaconda environment (recommended)

### Install Python Dependencies

```sh
# Please activate your virtual environment,
# i.e. conda activate <my_env>
pip install -r requirements.txt
```

## Run server

In your OpenARK VINE Desktop (aka. `MobileX Station`),

```sh
# Please activate your virtual environment,
# i.e. conda activate <my_env>
streamlit run Home.py --server.port=8501

# Then, open "http://localhost:8501/" with your browser.
# On Linux: xdg-open "http://localhost:8501/"
# On MacOS: open "http://localhost:8501/"
```

## Upload my own Feature

1. Copy the template (`templates/Custom_Feature.py`) into `pages/` directory and rename it into your feature name.
2. Check the TODO-commented lines (`TODO(user): `) and replace them.
3. Run the server.
4. You can edit your code while running the server. The server can automatically detect the changes and reload them.
