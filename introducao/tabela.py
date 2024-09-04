import streamlit as st

st.title('Tabela')
st.dataframe(
    st.session_state['df'],
    hide_index=True,
    use_container_width=True,
    column_config={
        'Renda no ano de exibição': st.column_config.NumberColumn(label='Renda', format='R$ %.2f')
    }
)
