# Caminhos para solução

- alterar a função associada ao nome "exit": não temos acesso a __main__
- a função com um timer? podemos fazer com que ela "espere" para que o audithoo seja desativado antes de operar
    - sleep não funciona D:
    - talvez um contador interno?
    - ou um else-if para verificação de "onde" ele está sendo chamado
    - o valor é printado, e se mudarmos o repr dele??
        primeiro dar um jeito de circumventar a limitação "_" para mudar __str__ e __repr__
            dir(object) e setattribute()
            herança -> herdar de string ou outro builtin que tenha __str__
            criar um objeto  e mudar o __str__ usando setaatr(obj, dir(myclass)[index-__str__], new_implementation)
            era exatamente isso :)
            profit
        

        
- tentar acessas mro?
    - ainda cai em problemas
    

passos: qual é o escopo que dummy tem acesso? podemos fazer recursão?
- não podemos fazer recursão: dummy não tem acesso a si mesmo
- tem acesso a safe_eval! será que podemos fazer algo com isso?
- conseguimos chamar exit() de dentro do safe_eval sem ativar o audithook -> como?? Porque não é considerado um audit event

