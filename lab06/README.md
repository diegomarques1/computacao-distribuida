# Explicação - Lab06 - Webservices e balanceamento de carga #

- O serviço foi implementado em Python com Flask. Executamos na conta da AWS do Diego.
- No arquivo .py, basicamente, temos a definição para a URL padrão e para a /convertemoeda/VALOR.
- API externa utilizada: https://docs.awesomeapi.com.br/api-de-moedas
- A implementação do webservice de conversão consiste em: pegar de uma API externa o valor do dólar e do euro em comparação ao real ->  multiplicar pelo VALOR fornecido -> criar dicionário com valores em real, dólar e euro -> retornar conversão para JSON e código de sucesso (200).
- Criamos uma página home para mostrar as nossas informações, como nome e TIA. 
- Na AWS, editamos o arquivo .py para mostrar "Webserver 01" e "Webserver 02" também, para provar o funcionamento do load balancer.
- Essa página é acessável pelo DNS público do load balancer, ou então pelo IPv4/DNS público de cada máquina individualmente (mas aí sem o balanceamento).
- Além disso, conforme a atividade proposta, também colocamos uma url para /convertemoeda/VALOR, em que VALOR pode ser substituído por qualquer número.
- Como resposta, a página retorna um .json com o valor digitado (real), bem como suas conversões para dólar e euro.
- Para executar a aplicação, utilizamos tais comandos:
- source env/bin/activate # para ativar nosso ambiente virtual
- export FLASK_APP=lab06.py
- export FLASK_DEBUG=true # OPCIONAL - usamos para o formato do JSON ficar mais agradável visualmente
- python -m flask run --host=0.0.0.0
- Após a execução em ambas as instâncias, o load balancer vai começar a direcionar o balanceamento de carga. Por isso, quando acessamos as URLs, ele direciona às vezes para o webserver 01, às vezes para o 02.
