import kabbes_smart_documentation
doc_gen = kabbes_smart_documentation.Client()
doc_gen.generate()

if doc_gen.cfg['template.name'] == 'sphinx':
    doc_gen.generate_sphinx()