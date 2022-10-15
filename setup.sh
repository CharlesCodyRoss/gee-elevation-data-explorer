mkdir -p ~/.streamlit/

echo "\n\
[general]\n\
email = \"charles.cody.ross@gmail.com\"\n\
" >> ~/.streamlit/credentials.toml

echo "\n\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
" >> ~/.streamlit/config.toml