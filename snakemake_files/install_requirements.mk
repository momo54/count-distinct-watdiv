rule install_requirements:
    output:
        touch("requirements_installed")
    shell:
        """
        pip install rdflib
        pip install click
        pip install pandas
        pip install SPARQLWrapper
        pip install requests
        pip install colorlog
		touch {output}
        """
rule all:
    input:
        "requirements_installed"