from cx_Freeze import setup, Executable

includefiles = [
    'scores', 
    'InGame.png',
    'Pause.jpg',
    'Over.jpg',
    'Start.jpg',
    'in_game.ogg'
    ]
includes = []
packages = ['pygame','random', 'math', 'sys','os','pickle']

target = Executable(
    script="SatelliteGame.py",
    icon="Icon.ico"
    )

setup(
    name = "Jak 3 - Satellite Game",
    author = 'Nathan PRATS',
    options = {'build_exe': {'includes':includes,'packages':packages,'include_files':includefiles}}, 
    executables = [target]
)