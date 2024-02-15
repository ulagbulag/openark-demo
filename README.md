# OpenARK Python Demo Server

## Run server

```sh
streamlit run Home.py --server.port=8501
# Then, open "http://localhost:8501/" with your browser.
```

## Upload my own Feature

1. Copy the template (`templates/Custom_Feature.py`) into `pages/` directory and rename it into your feature name.
2. Check the TODO-commented lines (`TODO(user): `) and replace them.
3. Run the server.
4. You can edit your code while running the server. The server can automatically detect the changes and reload them.
