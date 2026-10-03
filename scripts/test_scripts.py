"""Self-check for the data scripts. Run: python scripts/test_scripts.py"""
from import_xlsx import split_names
from enrich import candidates, looks_latin

assert looks_latin("Xerochrysum bracteatum")
assert not looks_latin("közönséges harangláb")
assert not looks_latin("Abrakzab")
assert not looks_latin("Illatos ternye")
assert not looks_latin("Kerti holdviola")
assert not looks_latin("Hópehelyvirág")
assert not looks_latin("piros gyűszűvirág")

assert split_names("mindignyíló begónia v. kerti begónia") == ["mindignyíló begónia", "kerti begónia"]
assert split_names("Chabaud-szegfű vagy egynyári szegfű") == ["Chabaud-szegfű", "egynyári szegfű"]
assert split_names("vaníliavirág, perui kunkor") == ["vaníliavirág", "perui kunkor"]
assert split_names("cseppecskevirág v zivatarvirág") == ["cseppecskevirág", "zivatarvirág"]
assert candidates("Coleus scutellarioides (Solenostemon scutellarioides)")[:2] == ["Coleus scutellarioides", "Solenostemon scutellarioides"]
assert candidates("Salix alba 'Tristis'") == ["Salix alba", "Salix"]
assert candidates("Typha sp.") == ["Typha"]
print("ok")
