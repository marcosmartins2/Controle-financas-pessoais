from models import Conta,engine,Bancos,Status,Historico,Tipos
from sqlmodel import Session,select
from datetime import date,timedelta
import matplotlib.pyplot as plt


def criar_conta(conta : Conta):

    with Session(engine) as session:
        statement = select(Conta).where(Conta.banco==conta.banco)
        results = session.exec(statement).all()

        if results:
            print('Ja existe uma conta nesse banco!')
            return

        session.add(conta)

        session.commit()

        return conta
    

def listar_contas():
    with Session(engine) as session:
        statement = select(Conta)
        results = session.exec(statement).all()
    return results


def desativar_conta(id):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==id)
        conta = session.exec(statement).first()

        if conta.valor>0:
            raise ValueError('Essa conta ainda possui saldo')
        conta.status = Status.INATIVO
        session.commit()


def transferir_saldo(id_conta_saida,id_conta_entrada,valor):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==id_conta_saida)
        conta_saida = session.exec(statement).first()

        if conta_saida.valor < valor:
            raise ValueError('O saldo para transferencia nao é suficiente')
        statement = select(Conta).where(Conta.id==id_conta_entrada)
        conta_entrada = session.exec(statement).first()

        conta_saida.valor -= valor
        conta_entrada.valor += valor
        session.commit()


def movimentar_dinheiro(historico: Historico):

    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==historico.conta_id)
        conta = session.exec(statement).first()

        print(f'Esses sao os dados da sua conta {conta.status}')

        if conta.status == Status.INATIVO:
            raise ValueError('Essa conta está inativa e não pode receber transferências, por favor selecione outra opção')

        if historico.tipo == Tipos.ENTRADA:
            conta.valor += historico.valor
        else:
            if conta.valor < historico.valor:
                raise ValueError('saldo insuficiente')
            conta.valor-= historico.valor

        session.add(historico)
        session.commit()
        return


def total_contas():
    valorTotal = 0
    with Session(engine) as session:
        statement = select(Conta).where(Conta.valor != 0)
        contas = session.exec(statement).all()

        for conta in contas:
            valorTotal += conta.valor

        session.commit()

        return valorTotal

       

def buscar_historicos_entre_datas(data_inicio:date,data_fim:date):
    with Session(engine) as session:
        statement = select(Historico).where(
            Historico.data>=data_inicio,
            Historico.data<=data_fim
                                            )
        
        resultados = session.exec(statement)
        return resultados

def criar_grafico_por_conta():
    with Session(engine) as session:
        statement = select(Conta)
        contas = session.exec(statement).all()
        nome_contas = []
        valor_contas = []
        for conta in contas:
            nome_contas.append(str(conta.banco)[7:])
            valor_contas.append(conta.valor)

        plt.bar(nome_contas,valor_contas)
        plt.show()

        return 
    







