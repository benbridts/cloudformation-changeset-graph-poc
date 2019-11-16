def label_table(title, **kwargs) -> str:
    return f"""<
    <table border='0' cellborder='0'>
        <tr><td colspan='2'><b>{title}</b></td></tr>
        {''.join([f'<tr><td>{k.title()}:</td><td>{v}</td></tr>' for k, v in kwargs.items()])}
    </table>
    >"""
