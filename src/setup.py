from cx_Freeze import setup, Executable


includefiles = ['resources.cfg',
				'ogre.cfg',
				'plugins.cfg',
				'media',
				]
build_exe_options = {'include_files':includefiles}

setup(
	name="Crustacean Crusaders",
	version="0.1",
	author="Team Lobster Knife Fight",
	description="Shooting game (1-2 people,normal & challenge modes)",
	options = {'build_exe': build_exe_options},
	executables=[Executable(script="main.py")],
	)