from imap_tools import MailBox, AND
import pandas as pd
import os
import re

# username = "adm.happyenergy@gmail.com"
# password = "mxtl agjv dcsn tcnv" #adm.happyenergy@gmail.com
# _from = "engenhariahappysolar@gmail.com"

username = "engenhariahappysolar@gmail.com"
password = "jtpg hdvr pmat rtap" #engenhariahappysolar@gmail.com
_from = 'noreplyportalgd@neoenergia.com'

# caminhos dos CSVs (mesma pasta do script)
BASE_DIR = os.path.dirname(__file__)
CSV_FILES = [
    os.path.join(BASE_DIR, 'PortalGD_minhas_solicitacoes.csv'),
    os.path.join(BASE_DIR, 'PortalGD_minhas_solicitacoes (1).csv'),
]

def load_active_codes():
    codes = set()
    for path in CSV_FILES:
        if os.path.exists(path):
            try:
                df = pd.read_csv(path, encoding='latin1')
            except Exception:
                df = pd.read_csv(path, encoding='utf-8', errors='ignore')
            if df.shape[1] >= 2:
                vals = df.iloc[:, 1].astype(str).str.strip()
                codes.update(vals.tolist())
    return codes


def sanitize_filename(name: str) -> str:
    name = str(name).strip()
    name = re.sub(r'[\\/*?:"<>|]', '_', name)
    name = name.replace('\n', ' ').replace('\r', '')
    return name


def extract_period(subject: str) -> str:
    if not subject:
        return None
    # busca YYYY-MM ou YYYY/MM primeiro, depois MM/YYYY, depois YYYY
    parts = subject.split("- ")
    return parts[1].split("Demonstrativo do Faturamento")[1]


def extract_cliente(subject: str) -> str:
    if not subject:
        return 'cliente_desconhecido'
    return subject.split("- ")[2].removesuffix(" ")


def main():
    active_codes = load_active_codes()

    mailbox = MailBox('imap.gmail.com').login(username, password)
    lista_emails = mailbox.fetch(AND(from_='engenhariahappysolar@gmail.com'))
    for email in lista_emails:
        if not email.attachments:
            continue
        cliente = extract_cliente(email.subject)
        period = extract_period(email.subject) or 'sem_periodo'
        cliente_s = sanitize_filename(cliente)
        period_s = sanitize_filename(period)

        # verificar presença em listas (comparing stripped strings)
        chave = cliente.strip() if isinstance(cliente, str) else str(cliente)
        if chave in active_codes:
            base_folder = os.path.join(BASE_DIR, 'clientes ativos')
        else:
            base_folder = os.path.join(BASE_DIR, 'cliente não ativos')

        dest_dir = os.path.join(base_folder, cliente_s)
        os.makedirs(dest_dir, exist_ok=True)

        for anexo in email.attachments:
            if 'RelatorioResumo' in anexo.filename:
                filename = f"{cliente_s} - {period_s}.pdf"
                path = os.path.join(dest_dir, filename)
                with open(path, 'wb') as f:
                    f.write(anexo.payload)


if __name__ == '__main__':
    main()