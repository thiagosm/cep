#- coding: utf-8
import requests

URL_CORREIOS = 'https://buscacepinter.correios.com.br/app/endereco/carrega-cep-endereco.php'

class Correios():

    def _parse_detalhe(self, d):
        return {
                    "UF": d['uf'],
                    "Logradouro": d['logradouroDNEC'],
                    "Bairro": d['bairro'],
                    "Localidade": d['localidade'],
                    "UF": d['uf'],
                    "CEP": d['cep'],
                    "Numero": d['nomeUnidade']
                }


    def consulta_faixa(self, localidade, uf):
        """Consulta site e retorna faixa para localidade"""       
        return filter(lambda x: x['UF'] == uf.upper(), self.consulta(endereco, uf=uf))

    def consulta(self, endereco, primeiro=False, bairro=None,
                 uf=None, localidade=None, tipo='LOG', numero=None):
        """Consulta site e retorna lista de resultados"""
        result = requests.post(URL_CORREIOS, params={'endereco': endereco, 'tipoCEP': tipo})
        dados = []
        try:
            dados = result.json().get('dados')
            dados = [self._parse_detalhe(d) for d in dados]
            if uf:
                dados = filter(lambda x: x['UF'].upper() == uf.upper(), dados)
            if localidade:
                dados = filter(lambda x: x['Localidade'].upper() == localidade.upper(), dados)
            if numero:
                dados = filter(lambda x: x['Numero'] == str(numero), dados)
            if bairro:
                dados = filter(lambda x: x['Bairro'].upper() == bairro.upper(), dados)                
        except Exception as e:
            print(e)
        
        if primeiro and dados:
            return dados[0]
        else:
            return dados
