#- coding: utf-8
import requests
import re
import collections
import traceback

class Correios():
    URL_VIACEP_CEP = 'https://viacep.com.br/ws/%s/json/'
    URL_VIACEP_END = 'https://viacep.com.br/ws/%s/%s/%s/json/'

    TIMEOUT = 60

    def _parse_data(self, d):
        try:
            return {
                "UF": d.get("uf", None) or "",
                "Logradouro": d.get("logradouro", None) or "",
                "Bairro": d.get("bairro", None) or "",
                "Localidade": d.get("localidade", None) or "",
                "CEP": d.get("cep", None) or "",
                "Complemento": d.get("complemento", None) or "",
                "Numero": d.get("numero", None) or ""
            }
        except:
            traceback.print_exc()

    def consulta(self, **kwargs):
        """Consulta site e retorna lista de resultados"""

        cep = kwargs.get("cep", None) or kwargs.get("consulta", None)
        cidade = kwargs.get("cidade", None)
        uf = kwargs.get("uf", None)
        logradouro = kwargs.get("logradouro", None)

        if cep:
            cep = re.sub('[^0-9]', '', str(cep))
        
        result = []

        try:
            url = None
            if cep and cep.isdigit():
                url = self.URL_VIACEP_CEP % cep
            elif not cep and (cidade and uf and logradouro):
                url = self.URL_VIACEP_END % (uf, cidade, logradouro)

            if url:
                response = requests.get(url,
                                        headers={
                                            'accept': 'application/json',
                                            'cache-control': 'no-store, no-cache, must-revalidate',
                                        },
                                        verify=False,
                                        allow_redirects=True,
                                        timeout=self.TIMEOUT)
                
                print ('------ viacep -------')
                print (response.text)
                
                if response.status_code == 200:
                    rjson = None
                    try:
                        rjson = response.json()
                    except:
                        pass

                    if rjson:
                        if isinstance(rjson, collections.Mapping):  
                            data = self._parse_data(rjson)
                            if data:
                                result.append(data)
                        
                        elif isinstance(rjson, list):
                            for d in rjson:
                                data = self._parse_data(d)
                                if data:
                                    if d not in result:
                                        result.append(data)
        except:
            traceback.print_exc()

        return result
