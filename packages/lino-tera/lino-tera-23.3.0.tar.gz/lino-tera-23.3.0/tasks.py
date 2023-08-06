from atelier.invlib import setup_from_tasks

cfg = dict()
cfg.update(revision_control_system='git')
# cfg.update(tolerate_sphinx_warnings=True)
cfg.update(blog_root='/home/luc/work/blog/')
cfg.update(blogref_url='https://luc.lino-framework.org')
cfg.update(languages=['en', 'de', 'fr', 'et'])
cfg.update(locale_dir='lino_tera/lib/tera/locale')
cfg.update(doc_trees=['docs'])
cfg.update(make_docs_command='./make_docs.sh')
cfg.update(selectable_languages='en de'.split())
ns = setup_from_tasks(globals(), "lino_tera", **cfg)
