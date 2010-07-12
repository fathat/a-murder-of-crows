#!/usr/bin/env python

from distutils.core import setup
import py2exe
import glob

opts = {
        "py2exe" : {
                "bundle_files" : 1,
                "optimize" : 2,
                "dist_dir" : "exe",
                "packages":['pyexpat']
        }
}

setup ( name = 'A Murder of Crows',
                version = '1.1',
                description = 'A murder of crows...',
                author = 'Ian Overgard',
                author_email = 'ian.overgard@gmail.com',
                url='http://www.faceh.at',
                windows=["run_game.py"],
                data_files=[
                                ("data", glob.glob("data/*.*")),
                                ("data/bg", glob.glob("data/bg/*.*")),
                                ("data/characters", glob.glob("data/characters/*.*")),
                                ("data/fonts", glob.glob("data/fonts/*.*")),
                                ("data/menu", glob.glob("data/menu/*.*")),
                                ("data/music", glob.glob("data/music/*.*")),
                                ("data/particles", glob.glob("data/particles/*.*"))],
                options = opts)
