from redminelib import Redmine
import re

redmine = Redmine('https://host', key='KEY', requests={'timeout': 10})

def listar_projetos():
    projetos = redmine.project.all()
    for idx, projeto in enumerate(projetos, start=1):
        print(f"{idx} - {projeto.name}")

def escolher_projeto():
    listar_projetos()
    escolha = int(input("Escolha o número do projeto: "))
    projeto = list(redmine.project.all())[escolha - 1]
    return projeto

def listar_issues(project_identifier):
    issues = redmine.issue.filter(project_id=project_identifier)
    for issue in issues:
        print(f"Issue ID: {issue.id} - Subject: {issue.subject}")

def salvar_issue(issue):
    safe_subject = re.sub(r'[\\/*?:"<>|]', "", issue.subject[:50])  
    filename = f"{safe_subject}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"Issue ID: {issue.id}\n")
        file.write(f"Subject: {issue.subject}\n")
        file.write(f"Description:\n{issue.description}\n")
    print(f"Issue '{issue.subject}' salva em '{filename}'")

def main():
    print("Carregando projetos...")
    projeto = escolher_projeto()
    print(f"Projeto escolhido: {projeto.name}")
    print("Carregando issues...")
    listar_issues(projeto.identifier)
    opcao = input("Digite 'tudo' para extrair todas as issues ou o ID de uma issue específica: ")
    if opcao == 'tudo':
        issues = redmine.issue.filter(project_id=projeto.identifier)
        for issue in issues:
            salvar_issue(issue)
    else:
        issue = redmine.issue.get(opcao)
        salvar_issue(issue)

main()
