#- coding: utf-8
import requests



class Correios():
    URL_VIACEP_CEP = 'https://viacep.com.br/ws/{cep}/json/'
    URL_VIACEP_END = 'https://viacep.com.br/ws/{uf}/{cidade}/{end}/json/'

    HEADERS = {
        'accept': 'application/json',
        'cache-control': 'no-store, no-cache, must-revalidate',
    }

    TIMEOUT = 30

    def _parse_detalhe(self, d):
        return {
            "UF": d['uf'],
            "Logradouro": d['logradouro'],
            "Bairro": d['bairro'],
            "Localidade": d['localidade'],
            "CEP": d['cep'],
            "Numero": "",
        }


    def consulta_faixa(self, localidade, uf):
        """Consulta site e retorna faixa para localidade"""       
        return filter(lambda x: x['UF'] == uf.upper(), self.consulta(endereco, uf=uf))

    def consulta(self, endereco, primeiro=False, bairro=None,
                 uf=None, localidade=None, tipo='LOG', numero=None):
        """Consulta site e retorna lista de resultados"""

        url = None
        if str(endereco).isdigit():
            url = self.URL_VIACEP_CEP.replace("{cep}",endereco)
        elif "," in str(endereco):
            end = endereco.split(",")
            if len(end) == 3: #Logradouro, Cidade e UF
                url = self.URL_VIACEP_END
                url = url.replace("{end}",end[0].strip())
                url = url.replace("{cidade}",end[1].strip())
                url = url.replace("{uf}",end[2].strip())
            elif len(end) == 4: #Logradouro, Bairro, Cidade e UF
                url = self.URL_VIACEP_END
                url = url.replace("{end}",end[0].strip())
                url = url.replace("{cidade}",end[2].strip())
                url = url.replace("{uf}",end[3].strip())


        result = requests.get(url,
                               headers=self.HEADERS,
                               verify=False,
                               allow_redirects=True,
                               timeout=self.TIMEOUT)

        print (result.status_code, result.text)

        dados = []
        try:
            dados = result.json()
            if isinstance(dados, dict):
                dados = [dados]
            dados = [self._parse_detalhe(d) for d in dados]
            if uf:
                dados = filter(lambda x: x['uf'].upper() == uf.upper(), dados)
            if localidade:
                dados = filter(lambda x: x['logradouro'].upper() == localidade.upper(), dados)
            if bairro:
                dados = filter(lambda x: x['bairro'].upper() == bairro.upper(), dados)
        except Exception as e:
            print(e)

        if primeiro and dados:
            return dados[0]
        else:
            return dados
