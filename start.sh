export STREAMLIT_HOME=/tmp/.streamlit
mkdir -p $STREAMLIT_HOME
if [ -d ".streamlit" ]; then
    cp -r .streamlit/* $STREAMLIT_HOME/ 2>/dev/null || true
fi
streamlit run app.py --server.port=7860 --server.address=0.0.0.0



STREAMLIT_HOME=/tmp/.streamlit