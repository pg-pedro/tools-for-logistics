with open('requirements.txt', 'r') as f:
    content = f.read()

if 'pyarrow' not in content:
    with open('requirements.txt', 'a') as f:
        f.write('pyarrow\n')
if 'pandas' not in content:
    with open('requirements.txt', 'a') as f:
        f.write('pandas\n')
if 'streamlit\n' not in content:
    with open('requirements.txt', 'a') as f:
        f.write('streamlit\n')
