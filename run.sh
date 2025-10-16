export STREAMLIT_HOME=$(pwd)
mkdir -p .streamlit
streamlit run app.py --server.address localhost --server.port 8502