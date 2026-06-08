import streamlit as st
import tiktoken

# 1. Set up the web page title and icon
st.set_page_config(page_title="PromptPerf", page_icon="⚡")

st.title("⚡ PromptPerf")
st.caption("The AI Engineering Tool for Prompt Optimization & Cost Estimation")
st.write("---")

# 2. Create a big interactive text box for the user to paste their prompt
user_prompt = st.text_area(
    "Paste your AI Prompt here:",
    placeholder="e.g., Act as a professional chef. Give me a 3-ingredient recipe...",
    height=150
)

# 3. Only run the analytics if the user actually typed something
if user_prompt:
    # Token counting logic
    encoder = tiktoken.encoding_for_model("gpt-4")
    token_list = encoder.encode(user_prompt)
    total_tokens = len(token_list)
    
    # Cost math
    estimated_cost = (total_tokens / 1000) * 0.03
    
    # Analytics Engine
    score = 100
    issues_found = []
    
    if "act as" not in user_prompt.lower() and "you are" not in user_prompt.lower():
        score -= 20
        issues_found.append("Missing a distinct AI persona ('Act as...' or 'You are...')")
        
    if "{" not in user_prompt and "[" not in user_prompt:
        score -= 20
        issues_found.append("No variable placeholders found (use [ ] or { } for dynamic data)")
        
    double_space_count = user_prompt.count("  ")
    if double_space_count > 0:
        score -= 10
        issues_found.append(f"Found {double_space_count} token-wasting double-spaces")
        
    # 4. Display the Web Dashboard UI Layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(label="Total AI Tokens", value=total_tokens)
    with col2:
        st.metric(label="Estimated Cost (GPT-4)", value=f"${estimated_cost:.5f}")
        
    st.write("---")
    st.subheader(f"Structure Score: {score} / 100")
    
    # Visual progress bar based on score
    st.progress(score / 100)
    
    st.write("### Audit Logs")
    if len(issues_found) == 0:
        st.success("✨ Pristine structure! No issues detected.")
    else:
        for issue in issues_found:
            st.error(f"⚠️ {issue}")