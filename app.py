{\rtf1\ansi\ansicpg949\cocoartf2865
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # app.py\
# Streamlit + Google Gemini \uc0\u52311 \u48391  \u50696 \u51228 \
# \uc0\u47785 \u51201 : \u44256 \u44061  \u51025 \u45824  \u52311 \u48391  (\u49660 \u54609 \u47792  \u44396 \u47588  \u48520 \u54200  \u49324 \u54637  \u51217 \u49688 /\u51221 \u47532 /\u51060 \u47700 \u51068  \u50836 \u52397 )\
# \uc0\u47784 \u45944  \u44592 \u48376 \u44050 : gemini-2.0-flash\
# \uc0\u54645 \u49900  \u44592 \u45733 : \u45824 \u54868  \u55176 \u49828 \u53664 \u47532 , 429 \u51116 \u49884 \u46020 (\u52572 \u44540  6\u53556  \u50976 \u51648  \u54980  \u51116 \u49884 \u51089 ), CSV \u51088 \u46041  \u44592 \u47197 (\u50741 \u49496 ), \u47196 \u44536  \u45796 \u50868 \u47196 \u46300 , \u45824 \u54868  \u52488 \u44592 \u54868 , \u47784 \u45944 /\u49464 \u49496  \u54364 \u49884 \
\
import streamlit as st\
import time\
import pandas as pd\
import json\
from datetime import datetime\
\
# --- \uc0\u50808 \u48512  \u46972 \u51060 \u48652 \u47084 \u47532 (generative ai) \u49324 \u50857  \u49884  \u51452 \u49437  \u54644 \u51228  ---\
# try:\
#     import google.generativeai as genai\
# except Exception:\
#     genai = None\
\
# --------------------------\
# \uc0\u49444 \u51221  / UI \u52488 \u44592 \u54868 \
# --------------------------\
st.set_page_config(page_title="Customer Support Chatbot (Gemini)", layout="wide")\
\
st.title("\uc0\u44256 \u44061  \u51025 \u45824  \u52311 \u48391  \'97 \u49660 \u54609 \u47792  \u48520 \u54200  \u51217 \u49688  (Gemini)")\
st.markdown("\uc0\u51221 \u51473 \u54616 \u44256  \u44277 \u44048  \u50612 \u47536  \u51025 \u45824 \u47484  \u54616 \u45716  \u52311 \u48391 \u51077 \u45768 \u45796 . (\u47784 \u45944 : gemini-2.0-flash)")\
\
# \uc0\u49324 \u51060 \u46300 \u48148 : \u49444 \u51221 \
with st.sidebar.expander("\uc0\u49444 \u51221 "):\
    api_key_secret = st.text_input("API Key (\uc0\u49440 \u53469 ) \'97 st.secrets['GEMINI_API_KEY'] \u45824 \u49888  \u49324 \u50857  \u44032 \u45733 ", type="password")\
    model_choice = st.selectbox("\uc0\u47784 \u45944  \u49440 \u53469 ", ["gemini-2.0-flash", "gemini-2.0"], index=0)\
    csv_autosave = st.checkbox("\uc0\u45824 \u54868  \u51088 \u46041  CSV \u51200 \u51109  (\u49464 \u49496  \u51333 \u47308  \u49884 )", value=True)\
    max_retries = st.number_input("429 \uc0\u51116 \u49884 \u46020  \u54943 \u49688 ", min_value=1, max_value=5, value=2)\
    system_prompt_preview = st.checkbox("\uc0\u49884 \u49828 \u53596  \u54532 \u47212 \u54532 \u53944  \u48372 \u51060 \u44592 ", value=False)\
\
# \uc0\u49884 \u49828 \u53596  \u54532 \u47212 \u54532 \u53944  (\u50836 \u52397 \u54616 \u49888 \u45824 \u47196 )\
SYSTEM_PROMPT = (\
    "\uc0\u45817 \u49888 \u51008  \u52828 \u51208 \u54616 \u44256  \u44277 \u44048 \u51201 \u51064  \u44256 \u44061  \u51025 \u45824  \u52311 \u48391 \u51077 \u45768 \u45796 . "\
    "\uc0\u49324 \u50857 \u51088 \u45716  \u49660 \u54609 \u47792  \u44396 \u47588  \u44284 \u51221 \u50640 \u49436  \u44202 \u51008  \u48520 \u54200 /\u48520 \u47564 \u51012  \u51060 \u50556 \u44592 \u54633 \u45768 \u45796 . "\
    "\uc0\u45796 \u51020  \u44508 \u52825 \u51012  \u48152 \u46300 \u49884  \u46384 \u47476 \u49464 \u50836 :\\n"\
    "1) \uc0\u51221 \u51473 \u54616 \u44256  \u44277 \u44048  \u50612 \u47536  \u47568 \u53804 \u47196  \u51025 \u45813 \u54633 \u45768 \u45796 .\\n"\
    "2) \uc0\u49324 \u50857 \u51088 \u51032  \u48520 \u54200  \u49324 \u54637 \u51012  \u44396 \u52404 \u51201 \u51004 \u47196  \u51221 \u47532 \u54616 \u50668  (\u47924 \u50631 \u51060  / \u50616 \u51228  / \u50612 \u46356 \u49436  / \u50612 \u46523 \u44172 ) \u54805 \u49885 \u51004 \u47196  \u49688 \u51665 \u54616 \u44256 , "\
    "\uc0\u51060 \u47484  \u44256 \u44061  \u51025 \u45824  \u45812 \u45817 \u51088 \u50640 \u44172  \u51204 \u45804 \u54620 \u45796 \u45716  \u52712 \u51648 \u47196  \u50504 \u45236 \u54633 \u45768 \u45796 .\\n"\
    "3) \uc0\u45824 \u54868  \u47560 \u51648 \u47561 \u50640 \u45716  \u45812 \u45817 \u51088  \u54869 \u51064  \u54980  \u54924 \u49888 \u51012  \u50948 \u54644  \u51060 \u47700 \u51068  \u51452 \u49548 \u47484  \u50836 \u52397 \u54616 \u49464 \u50836 . "\
    "\uc0\u47564 \u51068  \u49324 \u50857 \u51088 \u44032  \u50672 \u46973  \u51228 \u44277 \u51012  \u50896 \u52824  \u50506 \u51004 \u47732 : "\
    "\'93\uc0\u51396 \u49569 \u54616 \u51648 \u47564 , \u50672 \u46973 \u52376  \u51221 \u48372 \u47484  \u48155 \u51648  \u47803 \u54616 \u50668  \u45812 \u45817 \u51088 \u51032  \u44160 \u53664  \u45236 \u50857 \u51012  \u48155 \u51004 \u49892  \u49688  \u50630 \u50612 \u50836 .\'94 \u46972 \u44256  \u51221 \u51473 \u55176  \u50504 \u45236 \u54616 \u49464 \u50836 .\\n"\
)\
\
if system_prompt_preview:\
    st.sidebar.markdown("**SYSTEM PROMPT:**")\
    st.sidebar.code(SYSTEM_PROMPT, language="text")\
\
# API Key \uc0\u50864 \u49440 \u49692 \u50948 : st.secrets -> \u51077 \u47141  UI\
def get_api_key():\
    if "AIzaSyBcUdPpnsr3ZM14JvxUyf8WlMHNbp7Pvs4" in st.secrets:\
        return st.secrets["AIzaSyBcUdPpnsr3ZM14JvxUyf8WlMHNbp7Pvs4"]\
    if api_key_secret:\
        return api_key_secret\
    return None\
\
API_KEY = get_api_key()\
\
# (\uc0\u49440 \u53469 ) \u49892 \u51228  Google Generative AI \u49324 \u50857  \u49884  \u52488 \u44592 \u54868  (\u51452 \u49437  \u54644 \u51228  \u54980  \u49324 \u50857 )\
# if API_KEY and genai:\
#     genai.configure(api_key=API_KEY)\
\
# --------------------------\
# Session state \uc0\u52488 \u44592 \u54868 \
# --------------------------\
if "messages" not in st.session_state:\
    # messages: list of dicts \{role: "system/user/assistant", "content": str, "time": timestamp\}\
    st.session_state.messages = [\{"role": "system", "content": SYSTEM_PROMPT, "time": datetime.utcnow().isoformat()\}]\
if "conversation_log" not in st.session_state:\
    st.session_state.conversation_log = []  # rows for CSV: timestamp, role, text\
if "retry_count" not in st.session_state:\
    st.session_state.retry_count = 0\
if "session_id" not in st.session_state:\
    st.session_state.session_id = datetime.utcnow().strftime("%Y%m%d%H%M%S")\
if "last_status" not in st.session_state:\
    st.session_state.last_status = "ready"\
\
# --------------------------\
# Helper: add message and log\
# --------------------------\
def add_message(role, text):\
    entry = \{"role": role, "content": text, "time": datetime.utcnow().isoformat()\}\
    st.session_state.messages.append(entry)\
    st.session_state.conversation_log.append(\{"timestamp": entry["time"], "role": role, "text": text\})\
\
# --------------------------\
# Mock / API call wrapper\
# --------------------------\
def call_gemini_api(prompt_messages, model=model_choice):\
    """\
    \uc0\u49892 \u51228  \u49324 \u50857  \u49884  \u51060  \u54632 \u49688 \u47484  google.generativeai\u45208  REST \u54840 \u52636 \u47196  \u44396 \u54788 \u54616 \u49464 \u50836 .\
    \uc0\u54788 \u51116 \u45716  \u44592 \u48376 \u51201 \u51004 \u47196  \u47196 \u52972  \u47784 \u51032  \u51025 \u45813 \u51012  \u51228 \u44277 \u54633 \u45768 \u45796 . (\u49892 \u49324 \u50857 : \u51452 \u49437 \u46108  genai \u54840 \u52636 \u51012  \u52280 \u44256 )\
    """\
    # If no API_KEY provided, return mock response\
    if not API_KEY:\
        # simple echo-style mock with empathetic phrasing and request for details\
        user_latest = [m for m in prompt_messages if m["role"] == "user"][-1]["content"]\
        resp = (\
            f"\uc0\u51221 \u47568  \u48520 \u54200 \u54616 \u49512 \u44192 \u50612 \u50836 . \u47568 \u50432 \u54644  \u51452 \u49888  \u45236 \u50857 : \\"\{user_latest\}\\" \u47484  \u51217 \u49688 \u54664 \u49845 \u45768 \u45796 . "\
            "\uc0\u48520 \u54200  \u49324 \u54637 \u51012  \u45908  \u51221 \u54869 \u55176  \u51221 \u47532 \u54616 \u44592  \u50948 \u54644 , \u47924 \u50631 \u51060  \u47928 \u51228 \u50688 \u45716 \u51648 (\u47924 \u50631 \u51060 ), \u50616 \u51228 (\u45216 \u51676 /\u49884 \u44036 ), "\
            "\uc0\u50612 \u46356 \u49436 (\u51452 \u47928 /\u44208 \u51228 /\u48176 \u49569 /\u44592 \u53440 ), \u50612 \u46523 \u44172 (\u51613 \u49345 /\u50724 \u47448  \u47700 \u49884 \u51648  \u46321 )\u47484  \u50508 \u47140 \u51452 \u49892  \u49688  \u51080 \u45208 \u50836 ?"\
        )\
        return \{"status": "ok", "output": resp\}\
\
    # Example of how a real call might be made with google.generativeai (uncomment when configured)\
    # try:\
    #     response = genai.chat.create(\
    #         model=model,\
    #         messages=[\{"role": m["role"], "content": m["content"]\} for m in prompt_messages],\
    #     )\
    #     # parse response text\
    #     text = response.last\
    #     return \{"status": "ok", "output": text\}\
    # except Exception as e:\
    #     # detect rate limit from exception message\
    #     err_text = str(e)\
    #     if "429" in err_text or "rate" in err_text.lower():\
    #         return \{"status": "rate_limit", "error": err_text\}\
    #     return \{"status": "error", "error": err_text\}\
\
    # If API key present but library not configured, fallback mock\
    return \{"status": "ok", "output": "[MOCK RESPONSE] (API key provided but client not configured)"\}\
\
# --------------------------\
# Retry handling: 429 -> keep last 6 turns and restart conversation\
# --------------------------\
def safe_gemini_chat(system_msg_list, user_messages, model):\
    # combine system + history\
    prompt_msgs = system_msg_list + user_messages\
    attempt = 0\
    max_attempts = int(max_retries)\
    while attempt <= max_attempts:\
        result = call_gemini_api(prompt_msgs, model=model)\
        if result.get("status") == "ok":\
            st.session_state.retry_count = 0\
            return result["output"]\
        elif result.get("status") == "rate_limit":\
            attempt += 1\
            st.session_state.retry_count += 1\
            wait_sec = 2 ** attempt\
            st.warning(f"API rate limit detected. \uc0\u51116 \u49884 \u46020  \{attempt\}/\{max_attempts\} \'97 \{wait_sec\}s \u45824 \u44592 \u54633 \u45768 \u45796 .")\
            time.sleep(wait_sec)\
            if attempt > max_attempts:\
                # trim history to last 6 user+assistant pairs (i.e., last 12 entries ignoring system)\
                non_system = [m for m in st.session_state.messages if m["role"] != "system"]\
                trimmed = non_system[-12:]  # last 12 messages ~ 6 turns\
                # rebuild prompt: system + trimmed\
                prompt_msgs = [m for m in st.session_state.messages if m["role"] == "system"] + trimmed\
                st.warning("\uc0\u45824 \u54868 \u44032  \u44600 \u50612 \u49436  \u52572 \u44540  6\u53556 \u47564  \u50976 \u51648 \u54616 \u44256  \u49352  \u49464 \u49496 \u51004 \u47196  \u51116 \u49884 \u51089 \u54633 \u45768 \u45796 .")\
                # try one more time with trimmed\
                result2 = call_gemini_api(prompt_msgs, model=model)\
                if result2.get("status") == "ok":\
                    return result2["output"]\
                return \{"error": "rate_limit_final", "detail": result2\}\
        else:\
            # other errors\
            return \{"error": "api_error", "detail": result.get("error")\}\
    return \{"error": "unknown_failure"\}\
\
# --------------------------\
# UI: main chat area\
# --------------------------\
col1, col2 = st.columns([3,1])\
with col1:\
    st.subheader("\uc0\u45824 \u54868 ")\
    chat_container = st.container()\
    with chat_container:\
        # display history\
        for msg in st.session_state.messages:\
            if msg["role"] == "system":\
                continue\
            if msg["role"] == "user":\
                st.markdown(f"**\uc0\u49324 \u50857 \u51088 :** \{msg['content']\}")\
            elif msg["role"] == "assistant":\
                st.markdown(f"**\uc0\u52311 \u48391 :** \{msg['content']\}")\
\
    st.write("---")\
\
    # input\
    user_input = st.text_area("\uc0\u47700 \u49884 \u51648  \u51077 \u47141 ", value="", height=120, key="user_input")\
    send_col1, send_col2, send_col3 = st.columns([1,1,1])\
    with send_col1:\
        send_btn = st.button("\uc0\u51204 \u49569 ")\
    with send_col2:\
        reset_btn = st.button("\uc0\u45824 \u54868  \u52488 \u44592 \u54868 ")\
    with send_col3:\
        download_log_btn = st.button("\uc0\u53581 \u49828 \u53944  \u47196 \u44536  \u45796 \u50868 \u47196 \u46300 ")\
\
with col2:\
    st.subheader("\uc0\u49464 \u49496  / \u49444 \u51221 ")\
    st.markdown(f"- \uc0\u49464 \u49496  ID: `\{st.session_state.session_id\}`")\
    st.markdown(f"- \uc0\u47784 \u45944 : **\{model_choice\}**")\
    st.markdown(f"- \uc0\u47700 \u49884 \u51648  \u49688 : \{len(st.session_state.messages)\}")\
    st.markdown(f"- \uc0\u47560 \u51648 \u47561  \u49345 \u53468 : \{st.session_state.last_status\}")\
    if st.session_state.retry_count:\
        st.markdown(f"- \uc0\u52572 \u44540  \u51116 \u49884 \u46020  \u49688 : \{st.session_state.retry_count\}")\
\
    st.markdown("---")\
    st.markdown("**CSV / \uc0\u47196 \u44536 **")\
    if csv_autosave:\
        st.info("\uc0\u45824 \u54868 \u44032  \u51088 \u46041 \u51004 \u47196  CSV\u47196  \u51200 \u51109 \u46121 \u45768 \u45796  (\u49464 \u49496  \u51333 \u47308  \u49884 ).")\
    if st.session_state.conversation_log:\
        df_preview = pd.DataFrame(st.session_state.conversation_log).tail(10)\
        st.dataframe(df_preview)\
    st.markdown("---")\
    st.markdown("**\uc0\u45796 \u50868 \u47196 \u46300 **")\
    # CSV download\
    if st.session_state.conversation_log:\
        df_all = pd.DataFrame(st.session_state.conversation_log)\
        csv_bytes = df_all.to_csv(index=False).encode("utf-8")\
        st.download_button("CSV \uc0\u45796 \u50868 \u47196 \u46300 ", csv_bytes, file_name=f"chatlog_\{st.session_state.session_id\}.csv", mime="text/csv")\
    else:\
        st.write("\uc0\u45824 \u54868  \u44592 \u47197 \u51060  \u50630 \u49845 \u45768 \u45796 .")\
\
# --------------------------\
# \uc0\u48260 \u53948  \u46041 \u51089 : reset\
# --------------------------\
if reset_btn:\
    st.session_state.messages = [\{"role": "system", "content": SYSTEM_PROMPT, "time": datetime.utcnow().isoformat()\}]\
    st.session_state.conversation_log = []\
    st.success("\uc0\u45824 \u54868 \u47484  \u52488 \u44592 \u54868 \u54664 \u49845 \u45768 \u45796 .")\
    st.experimental_rerun()\
\
# --------------------------\
# \uc0\u48260 \u53948  \u46041 \u51089 : download text log\
# --------------------------\
if download_log_btn:\
    if st.session_state.conversation_log:\
        lines = []\
        for r in st.session_state.conversation_log:\
            lines.append(f"[\{r['timestamp']\}] \{r['role'].upper()\}: \{r['text']\}")\
        txt = "\\n".join(lines)\
        st.download_button("\uc0\u53581 \u49828 \u53944  \u54028 \u51068 \u47196  \u51200 \u51109 ", txt.encode("utf-8"), file_name=f"chatlog_\{st.session_state.session_id\}.txt", mime="text/plain")\
    else:\
        st.info("\uc0\u51200 \u51109 \u54624  \u47196 \u44536 \u44032  \u50630 \u49845 \u45768 \u45796 .")\
\
# --------------------------\
# Send: handle user input\
# --------------------------\
if send_btn and user_input.strip():\
    user_text = user_input.strip()\
    add_message("user", user_text)\
    st.session_state.last_status = "sending"\
\
    # compile system + recent history for API\
    system_msgs = [m for m in st.session_state.messages if m["role"] == "system"]\
    # send full history (or consider truncation for long sessions)\
    user_and_assistant = [m for m in st.session_state.messages if m["role"] != "system"]\
\
    # call wrapper\
    api_out = safe_gemini_chat(system_msgs, user_and_assistant, model_choice)\
    if isinstance(api_out, dict) and api_out.get("error"):\
        st.error(f"API \uc0\u54840 \u52636  \u50724 \u47448 : \{api_out.get('detail')\}")\
        st.session_state.last_status = "error"\
    else:\
        bot_text = api_out if isinstance(api_out, str) else str(api_out)\
        add_message("assistant", bot_text)\
        st.session_state.last_status = "ok"\
        st.experimental_rerun()\
\
# --------------------------\
# Autosave CSV on unload (simple explicit button)\
# --------------------------\
st.markdown("---")\
if st.button("\uc0\u49464 \u49496  \u51200 \u51109  (CSV\u47196 )"):\
    if st.session_state.conversation_log:\
        df_save = pd.DataFrame(st.session_state.conversation_log)\
        csv_buf = df_save.to_csv(index=False).encode("utf-8")\
        st.download_button("CSV \uc0\u54028 \u51068  \u49373 \u49457 ", csv_buf, file_name=f"chatlog_\{st.session_state.session_id\}.csv", mime="text/csv")\
    else:\
        st.info("\uc0\u51200 \u51109 \u54624  \u45824 \u54868 \u44032  \u50630 \u49845 \u45768 \u45796 .")\
\
# --------------------------\
# \uc0\u45149 : \u49324 \u50857  \u50504 \u45236 \
# --------------------------\
st.info("\uc0\u52280 \u44256 : \u49892 \u51228  Gemini API\u47484  \u49324 \u50857 \u54616 \u47140 \u47732  \u46972 \u51060 \u48652 \u47084 \u47532 \u47484  \u49444 \u52824 \u54616 \u44256  API_KEY\u47484  \u51228 \u44277 \u54644 \u50556  \u54633 \u45768 \u45796 . "\
        "\uc0\u54788 \u51116 \u45716  API\u53412  \u48120 \u49444 \u51221  \u49884  \u47784 \u51032  \u51025 \u45813 \u51004 \u47196  \u46041 \u51089 \u54633 \u45768 \u45796 . \u49892 \u51228  \u48176 \u54252  \u51204  \u48152 \u46300 \u49884  API \u54840 \u52636  \u48512 \u48516 (genai.chat.create \u46321 )\u51012  \u44396 \u54788 \u54616 \u49464 \u50836 .")}