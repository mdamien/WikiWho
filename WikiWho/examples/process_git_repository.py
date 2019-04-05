import sys
from pathlib import Path

from lys import L, render, raw

import git

HEADER = """<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.10/ http://www.mediawiki.org/xml/export-0.10.xsd" version="0.10" xml:lang="fr">
  <siteinfo>
    <sitename>Wikipédia</sitename>
    <dbname>frwiki</dbname>
    <base>https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal</base>
    <generator>MediaWiki 1.33.0-wmf.23</generator>
    <case>first-letter</case>
    <namespaces>
      <namespace key="0" case="first-letter"/>
    </namespaces>
  </siteinfo>"""

FOOTER = """</mediawiki>"""


if __name__ == '__main__':
	path = sys.argv[1]
	repo = git.Repo(path, search_parent_directories=True)
	git_root = repo.git.rev_parse("--show-toplevel")
	file_in_repo = str(Path(path)).replace(git_root + '/', '')

	revisions = []

	for i, commit in enumerate(reversed(list(repo.iter_commits(paths=path)))):
		filecontents = (commit.tree / file_in_repo).data_stream.read().decode('utf-8')
		revision = L.revision / (
			L.id / str(i),
			L.timestamp / '2008-01-26T13:36:54Z',
			L.contributor / (
				L.username / (str(commit.author) + ' ' + str(commit)),
				L.id / str(hash(commit.author))
			),
			L.comment / commit.message,
			L.model / 'wikitext',
			L.format / 'text/x-wiki',
			raw('<text xml:space="preserve" bytes="1181">'),
			render(filecontents),
			raw('</text>'),
		)

		revisions.append(revision)

	xml_tree = (
		raw(HEADER),
		L.page / (
			L.title / '---',
			L.ns / '0',
			L.id / '1',
			revisions,
		),
		raw(FOOTER),
	)

	print(render(xml_tree))
